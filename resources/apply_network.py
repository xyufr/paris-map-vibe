#!/usr/bin/env python3
"""Write the reconciled PDF network (build/network_final.json) to MySQL.

Back up the tables first (see README). Per line this rewrites line_stations
(ordered membership), line.color (from the PDF stroke color) and
line.path_json (segmented PDF geometry). Stations get PDF stop coordinates
and PDF label names; new stations and lines are inserted. Lines not drawn on
the PDF are removed together with their memberships.

    python3 resources/apply_network.py --dry-run
    python3 resources/apply_network.py
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import pymysql

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_network import BUILD, DB_CONFIG, NEW_LINES, load_db, normalize, palette_color  # noqa: E402
from reconcile_network import similarity  # noqa: E402


ROOT = Path(__file__).resolve().parent
FUTURE_PATH = ROOT / "future_lines.json"

TYPE_ORDER = {"METRO": 0, "RER": 1, "TRAIN": 2, "TRAM": 3, "CABLE": 4, "NAVETTE": 5}

# Dashed (under construction) routes on the PDF, identified by stroke style.
FUTURE_NAMES = {
    ("0,0.9,0.9,0", 7.0): "CDG Express",
    ("0.26,0.85,0,0", 7.0): "RER E (prolongement)",
    ("0,0.47,0.11,0", 3.5): "Métro 16",
    ("0.23,0.11,1,0", 3.5): "Métro 17",
    ("0.82,0,0.54,0", 3.5): "Métro 18",
}


def clean_label(text: str | None) -> str | None:
    """Turn a multi-line PDF label into a station name.

    Line breaks were joined with spaces; a following lowercase hyphenated word
    ("le-Grand", "sur-Seine", "lès-Chevreuse") belongs to the previous word.
    """
    if not text:
        return None
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r" (?=(?:le|la|les|sur|sous|en|lès|aux|au|du|de|des)-)", "-", text)
    return text


def reorder_stations() -> None:
    """Rewrite station_order along each line's geometry (trunk, then branches)."""
    sys.path.insert(0, str(ROOT.parent))
    import server
    from network_graph import order_stations

    data = server.fetch_map_data()
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cur:
            for line in data["lines"]:
                order = order_stations(line["stations"], line["edges"], first=line["stations"][0])
                for index, sid in enumerate(order, 1):
                    cur.execute(
                        "UPDATE line_stations SET station_order=%s WHERE line_id=%s AND station_id=%s",
                        (index, line["id"], sid),
                    )
        conn.commit()
    finally:
        conn.close()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    final = json.loads((BUILD / "network_final.json").read_text())
    db_lines, stations, memberships = load_db()
    station_by_id = {s["id"]: s for s in stations}
    renames = {int(k): v for k, v in final.get("renames", {}).items()}

    # ---- resolve station references ----------------------------------------
    new_stations: list[dict] = []

    def new_station_for(name: str, x: float, y: float) -> dict:
        norm = normalize(name)
        for item in new_stations:
            if item["norm"] == norm and math.dist((item["x0"], item["y0"]), (x, y)) < 60:
                return item
        item = {"key": f"new{len(new_stations)}", "name": name, "norm": norm, "x0": x, "y0": y}
        new_stations.append(item)
        return item

    stops_by_station: dict = defaultdict(list)
    label_votes: dict = defaultdict(Counter)
    line_rows = []
    for line in final["lines"]:
        if line.get("dropped"):
            line_rows.append({"line": line, "refs": []})
            continue
        refs = []
        for stop in line["stops"]:
            ref = stop["ref"]
            if isinstance(ref, str):
                name = clean_label(ref[4:].split("#")[0])
                ref = new_station_for(name, stop["x"], stop["y"])["key"]
            refs.append(ref)
            stops_by_station[ref].append((stop["x"], stop["y"]))
            label = clean_label(stop.get("label"))
            if label and isinstance(ref, int):
                row = station_by_id[ref]
                confident = stop["how"] in ("override", "new") or max(
                    similarity(label, row["name2"]), similarity(label, row["name"])
                ) >= 0.75
                if confident and stop["how"] != "implied":
                    label_votes[ref][label] += 1
        line_rows.append({"line": line, "refs": refs})

    # A DB row reused for physically distinct stations with the same name
    # (e.g. Malesherbes on M3 and on RER D): keep the row for the cluster
    # nearest its old coordinate, give other clusters their own new station.
    for row in line_rows:
        refs = row["refs"]
        stops = row["line"].get("stops", [])
        for i, ref in enumerate(refs):
            if not isinstance(ref, int):
                continue
            points = stops_by_station[ref]
            if max(math.dist(a, b) for a in points for b in points) <= 60:
                continue
            old = station_by_id[ref]
            anchor = (old["x"], old["y"]) if old["x"] is not None else points[0]
            here = (stops[i]["x"], stops[i]["y"])
            nearest = min(points, key=lambda p: math.dist(p, anchor))
            if math.dist(here, nearest) <= 60:
                continue
            item = new_station_for(clean_label(stops[i].get("label")) or old["name2"], here[0], here[1])
            refs[i] = item["key"]
            points.remove(here)
            stops_by_station[item["key"]].append(here)

    station_updates = {}
    for ref, points in stops_by_station.items():
        x = sum(p[0] for p in points) / len(points)
        y = sum(p[1] for p in points) / len(points)
        if isinstance(ref, int):
            row = station_by_id[ref]
            name2 = renames.get(ref) or (label_votes[ref].most_common(1)[0][0] if label_votes[ref] else row["name2"])
            name = row["name"]
            if name2 and max(similarity(name2, row["name"]), similarity(name2, row["name2"])) < 0.8:
                name = name2.upper()
            station_updates[ref] = {"x": round(x, 4), "y": round(y, 4), "name2": name2, "name": name}
        else:
            item = next(s for s in new_stations if s["key"] == ref)
            item.update({"x": round(x, 4), "y": round(y, 4)})

    # ---- report -------------------------------------------------------------
    moved = [
        (sid, math.dist((station_by_id[sid]["x"], station_by_id[sid]["y"]), (u["x"], u["y"])))
        for sid, u in station_updates.items()
        if station_by_id[sid]["x"] is not None
    ]
    filled = [sid for sid in station_updates if station_by_id[sid]["x"] is None]
    renamed = [sid for sid, u in station_updates.items() if u["name2"] != station_by_id[sid]["name2"]]
    print(f"stations: updated={len(station_updates)} coordinates_filled={len(filled)} "
          f"moved>5pt={sum(1 for _, d in moved if d > 5)} renamed={len(renamed)} new={len(new_stations)}")
    for item in new_stations:
        print(f"   new station: {item['name']} ({item['x']:.1f},{item['y']:.1f})")
    for sid, d in sorted(moved, key=lambda v: -v[1])[:15]:
        print(f"   moved {d:6.1f}pt  {sid}:{station_by_id[sid]['name2']} -> {station_updates[sid]['name2']}")
    dropped_lines = [r["line"] for r in line_rows if r["line"].get("dropped")]
    print(f"lines: total={len(line_rows)} dropped={[l['type'] + ':' + l['code'] for l in dropped_lines]} "
          f"new={[k for k in NEW_LINES]}")

    future = []
    for item in final.get("future", []):
        name = FUTURE_NAMES.get((item["color"], item["width"]))
        if not name:
            continue
        future.append({"name": name, "color": palette_color(item["color"]), "width": item["width"], "points": item["points"]})

    if args.dry_run:
        print("dry-run: nothing written")
        return 0

    FUTURE_PATH.write_text(json.dumps({"source": "paris_map.pdf dashed routes", "routes": future}, ensure_ascii=False))

    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cur:
            key_to_id = {}
            for item in new_stations:
                cur.execute(
                    "INSERT INTO stations (name, name2, x, y) VALUES (%s, %s, %s, %s)",
                    (item["name"].upper(), item["name"], item["x"], item["y"]),
                )
                key_to_id[item["key"]] = cur.lastrowid
            for sid, u in station_updates.items():
                cur.execute(
                    "UPDATE stations SET x=%s, y=%s, name2=%s, name=%s WHERE id=%s",
                    (u["x"], u["y"], u["name2"], u["name"], sid),
                )

            existing = {(str(l["type"]).upper().replace("TRAMWAY", "TRAM"), str(l["code"])): l for l in db_lines}
            for row in line_rows:
                line = row["line"]
                key = (line["type"], line["code"])
                db_line = existing.get(key)
                if line.get("dropped"):
                    if db_line:
                        cur.execute("DELETE FROM line_stations WHERE line_id=%s", (db_line["id"],))
                        cur.execute("DELETE FROM line WHERE id=%s", (db_line["id"],))
                    continue
                color = line["color"]
                path_json = json.dumps([[[round(x, 2), round(y, 2)] for x, y in seg] for seg in line["segments"]])
                if db_line:
                    line_id = db_line["id"]
                    cur.execute(
                        "UPDATE line SET color=%s, path_json=%s, type=%s WHERE id=%s",
                        (color, path_json, line["type"], line_id),
                    )
                else:
                    cur.execute(
                        "INSERT INTO line (code, name, type, color, path_json) VALUES (%s, %s, %s, %s, %s)",
                        (line["code"], NEW_LINES.get(key, {}).get("name", f"{line['type']} {line['code']}"),
                         line["type"], color, path_json),
                    )
                    line_id = cur.lastrowid
                cur.execute("DELETE FROM line_stations WHERE line_id=%s", (line_id,))
                seen = set()
                order = 0
                for ref in row["refs"]:
                    sid = key_to_id.get(ref, ref)
                    if sid in seen:
                        continue
                    seen.add(sid)
                    order += 1
                    name = station_updates.get(sid, {}).get("name") if isinstance(sid, int) else None
                    if name is None:
                        name = next((s["name"].upper() for s in new_stations if key_to_id.get(s["key"]) == sid), None)
                    cur.execute(
                        "INSERT INTO line_stations (line_id, station_id, station_name, station_order) VALUES (%s, %s, %s, %s)",
                        (line_id, sid, name, order),
                    )
        conn.commit()
    finally:
        conn.close()
    print("written to MySQL")
    reorder_stations()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
