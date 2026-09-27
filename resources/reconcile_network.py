#!/usr/bin/env python3
"""Reconcile PDF stops with the MySQL stations/line_stations tables.

Inputs:  build/network_geometry.json, build/network_nodes.json, MySQL,
         network_overrides.json (manual decisions)
Output:  build/network_final.json and build/reconcile_report.txt

Per line, each PDF stop gets a station:
  A. a DB member of the line at the stop position (<= 24pt, unique),
  B. a leftover DB member whose name matches the stop's PDF label,
  C. any DB station whose name matches the label (reused interchange row),
  D. otherwise a new station named from the PDF label.
DB members that still have no stop are kept as "implied" stops when their
coordinates sit on the line geometry (grey interchange hubs have no marker),
snapped onto the line; the rest are reported as not on the PDF.
"""

from __future__ import annotations

import json
import math
import sys
from collections import defaultdict
from difflib import SequenceMatcher
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_network import BUILD, NEW_LINES, OVERRIDES_PATH, canonical_type, load_db, normalize, palette_color, polyline_nearest  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from network_graph import components, line_edges  # noqa: E402


POSITION_TOL = 24.0
IMPLIED_TOL = 34.0


def similarity(a: str | None, b: str | None) -> float:
    na, nb = normalize(a), normalize(b)
    if not na or not nb:
        return 0.0
    if na == nb:
        return 1.0
    ta, tb = na.replace(" ", ""), nb.replace(" ", "")
    if ta == tb:
        return 1.0
    ratio = SequenceMatcher(None, ta, tb).ratio()
    if len(ta) >= 5 and len(tb) >= 5 and (ta in tb or tb in ta):
        ratio = max(ratio, 0.9)
    return ratio


def chain_graph_order(chains, stops):
    """Order stops by walking the line's chains depth-first from a terminus."""
    if not chains:
        return sorted(stops, key=lambda s: (s["chain"], s["along"]))
    tol = 6.0
    ends = []
    for ci, chain in enumerate(chains):
        ends.append((ci, 0, tuple(chain[0])))
        ends.append((ci, 1, tuple(chain[-1])))

    # adjacency: chain -> list of (neighbor chain, entry end or None, attach along on this chain)
    links = defaultdict(list)
    for ci, end, point in ends:
        for cj, chain in enumerate(chains):
            if cj == ci:
                continue
            dist, _, along = polyline_nearest(point, [tuple(p) for p in chain])
            if dist <= tol:
                links[cj].append((ci, end, along))
                links[ci].append((cj, None, 0.0 if end == 0 else float("inf")))

    degree = defaultdict(int)
    for ci, end, point in ends:
        for cj, end2, point2 in ends:
            if (ci, end) != (cj, end2) and math.dist(point, point2) <= tol:
                degree[(ci, end)] += 1
        for cj, chain in enumerate(chains):
            if cj != ci and polyline_nearest(point, [tuple(p) for p in chain])[0] <= tol:
                degree[(ci, end)] += 1
    termini = [(ci, end) for ci, end, _ in ends if degree[(ci, end)] == 0]
    start = termini[0] if termini else (0, 0)

    visited = set()
    order = []

    def walk(ci, reverse):
        if ci in visited:
            return
        visited.add(ci)
        order.append((ci, reverse))
        length = sum(math.dist(a, b) for a, b in zip(chains[ci], chains[ci][1:]))
        nexts = []
        for cj, entry_end, along in links[ci]:
            if cj in visited:
                continue
            position = along if along != float("inf") else length
            key = (length - position) if reverse else position
            nexts.append((key, cj, entry_end))
        for _, cj, entry_end in sorted(nexts, key=lambda t: (t[0], t[1])):
            walk(cj, entry_end == 1)

    walk(start[0], start[1] == 1)
    for ci in range(len(chains)):
        if ci not in visited:
            walk(ci, False)
    rank = {ci: (i, rev) for i, (ci, rev) in enumerate(order)}

    def key(stop):
        i, rev = rank.get(stop["chain"], (len(chains), False))
        return (i, -stop["along"] if rev else stop["along"])

    return sorted(stops, key=key)


def main() -> int:
    geometry = json.loads((BUILD / "network_geometry.json").read_text())
    nodes = json.loads((BUILD / "network_nodes.json").read_text())["nodes"]
    overrides = json.loads(OVERRIDES_PATH.read_text()) if OVERRIDES_PATH.exists() else {}
    db_lines, stations, memberships = load_db()
    station_by_id = {s["id"]: s for s in stations}

    stop_node = {}
    for node in nodes:
        for s in node["stops"]:
            stop_node[(s["line"], round(s["x"], 2), round(s["y"], 2))] = node

    members_by_line = defaultdict(list)
    for row in memberships:
        members_by_line[row["line_id"]].append(row)

    rename = {int(k): v for k, v in overrides.get("station_names", {}).items() if k.isdigit()}
    forced_stop = overrides.get("stop_station", [])
    drop_members = {(r["line"], r["station_id"]) for r in overrides.get("drop_members", [])}
    # Stations the reconciler must not reuse by name for other stops.
    keep_members = {(r["line"], r["station_id"]): r for r in overrides.get("keep_members", [])}
    drop_stops = overrides.get("drop_stops", [])
    add_stops = overrides.get("add_stops", [])
    drop_lines = {r["line"] for r in overrides.get("drop_lines", [])}

    report = []
    final_lines = []
    new_station_seq = 0
    new_stations: dict[str, dict] = {}

    for line in geometry["lines"]:
        key = f"{line['type']}:{line['code']}"
        chains = [[tuple(p) for p in c] for c in line["chains"]]
        members = members_by_line.get(line["dbId"], []) if line["dbId"] else []
        # Deduplicate DB members (some lines list a station twice).
        seen = set()
        member_rows = []
        for m in members:
            if m["station_id"] in seen:
                continue
            seen.add(m["station_id"])
            member_rows.append(m)
        member_ids = [m["station_id"] for m in member_rows]
        if key in drop_lines:
            report.append(f"=== {key} DROPPED LINE ({len(member_ids)} members)")
            final_lines.append({"type": line["type"], "code": line["code"], "dbId": line["dbId"], "dropped": True,
                                "removedMembers": [{"stationId": sid, "reason": "line-dropped"} for sid in member_ids]})
            continue

        def dropped(stop):
            for r in drop_stops:
                if r["line"] != key:
                    continue
                if "point" in r and math.dist((stop["x"], stop["y"]), tuple(r["point"])) < 3:
                    return True
                if "region" in r:
                    x0, y0, x1, y1 = r["region"]
                    if x0 <= stop["x"] <= x1 and y0 <= stop["y"] <= y1:
                        return True
            return False

        stops = []
        for s in line["stops"]:
            if dropped(s):
                continue
            node = stop_node.get((key, round(s["x"], 2), round(s["y"], 2)))
            stops.append({**s, "label": node["label"] if node else None, "node": node["id"] if node else None})
        for rule in add_stops:
            if rule["line"] != key:
                continue
            x, y = rule["point"]
            best = min((polyline_nearest((x, y), c) + (ci,) for ci, c in enumerate(chains)), key=lambda v: v[0])
            stops.append({"x": x, "y": y, "size": 0, "kind": "added", "chain": best[3], "along": best[2],
                          "label": None, "node": None, "forced": rule.get("station_id") or f"new:{rule['name']}"})

        assigned: dict[int, tuple] = {}
        taken: set = set()

        for i, stop in enumerate(stops):
            if stop.get("forced"):
                assigned[i] = (stop["forced"], "override")
                taken.add(stop["forced"])
                continue
            for rule in forced_stop:
                if rule["line"] != key:
                    continue
                if "point" in rule:
                    hit = math.dist((stop["x"], stop["y"]), tuple(rule["point"])) < 4
                else:
                    hit = normalize(stop["label"]) == normalize(rule["label"])
                if hit:
                    target = rule.get("station_id") or f"new:{rule['name']}"
                    assigned[i] = (target, "override")
                    taken.add(target)
                    if rule.get("name") and rule.get("station_id"):
                        rename[rule["station_id"]] = rule["name"]

        def assign(pairs, how):
            for _, i, sid in sorted(pairs, key=lambda p: (p[0], p[1], str(p[2]))):
                if i in assigned or sid in taken:
                    continue
                assigned[i] = (sid, how)
                taken.add(sid)

        pairs = []
        for i, stop in enumerate(stops):
            for sid in member_ids:
                s = station_by_id[sid]
                if s["x"] is None:
                    continue
                d = math.hypot(s["x"] - stop["x"], s["y"] - stop["y"])
                if d <= POSITION_TOL:
                    # Small preference for a matching label on ties.
                    sim = similarity(stop["label"], s["name2"] or s["name"])
                    pairs.append((d - 4 * sim, i, sid))
        assign(pairs, "position")

        pairs = []
        for i, stop in enumerate(stops):
            if i in assigned or not stop["label"]:
                continue
            for sid in member_ids:
                if sid in taken:
                    continue
                s = station_by_id[sid]
                sim = max(similarity(stop["label"], s["name2"]), similarity(stop["label"], s["name"]))
                if sim >= 0.72:
                    pairs.append((1 - sim, i, sid))
        assign(pairs, "member-name")

        pairs = []
        for i, stop in enumerate(stops):
            if i in assigned or not stop["label"]:
                continue
            for s in stations:
                if s["id"] in taken:
                    continue
                sim = max(similarity(stop["label"], s["name2"]), similarity(stop["label"], s["name"]))
                if sim < 0.86:
                    continue
                if s["x"] is not None and math.hypot(s["x"] - stop["x"], s["y"] - stop["y"]) > 80:
                    continue
                pairs.append((1 - sim, i, s["id"]))
        assign(pairs, "db-name")

        for i, stop in enumerate(stops):
            if i in assigned:
                continue
            name = stop["label"] or f"Unnamed {round(stop['x'])},{round(stop['y'])}"
            ref = f"new:{name}"
            if ref in taken:
                ref = f"new:{name}#{i}"
            assigned[i] = (ref, "new")
            taken.add(ref)

        final_stops = []
        for i, stop in enumerate(stops):
            ref, how = assigned[i]
            final_stops.append({**stop, "ref": ref, "how": how})

        # Leftover DB members.
        leftovers = []
        for sid in member_ids:
            if sid in taken:
                continue
            s = station_by_id[sid]
            if (key, sid) in drop_members:
                leftovers.append((sid, "dropped-override"))
                continue
            rule = keep_members.get((key, sid))
            if rule and rule.get("point"):
                x, y = rule["point"]
                best = min(
                    (polyline_nearest((x, y), c) + (ci,) for ci, c in enumerate(chains)),
                    key=lambda v: v[0],
                    default=(0.0, (x, y), 0.0, 0),
                )
                final_stops.append({"x": x, "y": y, "kind": "implied", "chain": best[3], "along": best[2],
                                    "label": s["name2"] or s["name"], "node": None, "ref": sid, "how": "keep-override"})
                taken.add(sid)
                continue
            if s["x"] is None or not chains:
                leftovers.append((sid, "no-coordinates"))
                continue
            best = min((polyline_nearest((s["x"], s["y"]), c) + (ci,) for ci, c in enumerate(chains)), key=lambda v: v[0])
            if best[0] <= IMPLIED_TOL:
                px, py = best[1]
                if any(math.dist((px, py), (f["x"], f["y"])) < 6 for f in final_stops):
                    leftovers.append((sid, "duplicate of a detected stop"))
                    continue
                final_stops.append({"x": px, "y": py, "kind": "implied", "chain": best[3], "along": best[2],
                                    "label": s["name2"] or s["name"], "node": None, "ref": sid, "how": "implied"})
                taken.add(sid)
            else:
                leftovers.append((sid, f"off-line {best[0]:.0f}pt"))

        ordered = chain_graph_order(chains, final_stops)
        extra = []
        for rule in overrides.get("connect", []):
            if rule["line"] != key:
                continue
            ia = next((i for i, st in enumerate(ordered) if st["ref"] == rule["a"]), None)
            ib = next((i for i, st in enumerate(ordered) if st["ref"] == rule["b"]), None)
            if ia is not None and ib is not None:
                extra.append((ia, ib))
        edges = line_edges(chains, ordered, extra=extra)
        comp = components(len(ordered), [(a, b) for a, b, _ in edges]) if ordered else 0

        lines_out = {
            "type": line["type"],
            "code": line["code"],
            "dbId": line["dbId"],
            "color": palette_color(line["color"]),
            "segments": line["chains"],
            "stops": [
                {"ref": s["ref"], "x": round(s["x"], 3), "y": round(s["y"], 3), "how": s["how"], "label": s["label"], "kind": s["kind"]}
                for s in ordered
            ],
            "edges": [[a, b, round(w, 1)] for a, b, w in edges],
            "components": comp,
            "removedMembers": [{"stationId": sid, "reason": why} for sid, why in leftovers],
        }
        final_lines.append(lines_out)

        # ---- report -----------------------------------------------------------
        report.append(f"=== {key} stops={len(ordered)} db={len(member_ids)} components={comp}")
        for s in ordered:
            ref = s["ref"]
            if isinstance(ref, int):
                row = station_by_id[ref]
                dbname = row["name2"] or row["name"]
                sim = similarity(s["label"], dbname) if s["label"] else 1.0
                flag = ""
                if s["how"] not in ("position", "override") or sim < 0.6:
                    flag = f"   <-- {s['how']} sim={sim:.2f} label={s['label']!r}"
                report.append(f"   {ref:5d} {dbname}{flag}")
            else:
                report.append(f"   NEW   {ref[4:]}   <-- {s['how']} at ({s['x']:.1f},{s['y']:.1f})")
        for sid, why in leftovers:
            row = station_by_id[sid]
            report.append(f"   DROP  {sid}:{row['name2'] or row['name']} ({why})")

    extra_lines = [k for k in NEW_LINES]
    out = {"lines": final_lines, "future": geometry.get("future", []), "newLines": [list(k) for k in extra_lines], "renames": rename}
    (BUILD / "network_final.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
    (BUILD / "reconcile_report.txt").write_text("\n".join(report) + "\n")
    total_new = sum(1 for l in final_lines for s in l.get("stops", []) if isinstance(s["ref"], str))
    total_drop = sum(len(l["removedMembers"]) for l in final_lines)
    total_implied = sum(1 for l in final_lines for s in l.get("stops", []) if s["how"] == "implied")
    print(f"lines={len(final_lines)} new_stops={total_new} dropped_members={total_drop} implied={total_implied}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
