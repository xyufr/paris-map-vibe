#!/usr/bin/env python3
"""Group per-line PDF stops into station nodes and name them from PDF labels.

Inputs:  build/network_geometry.json (build_network.py)
         build/pdf_labels.json       (pdf_labels.py)
         network_overrides.json      (manual corrections, optional)
Output:  build/network_nodes.json

A node is a set of stops (one per line at most) drawn at the same place:
rings closer than NODE_LINK_TOL, or stops inside the same interchange shape.
Each node receives the nearest station label block, assigned globally so
that a label is used by one node only whenever possible.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_network import BUILD, OVERRIDES_PATH, interchange_shapes, point_in_polygon  # noqa: E402


NODE_LINK_TOL = 10.5
LABEL_MAX_DIST = 42.0


def box_distance(box, x, y) -> float:
    dx = max(box["x0"] - x, 0.0, x - box["x1"])
    dy = max(box["top"] - y, 0.0, y - box["bottom"])
    return math.hypot(dx, dy)


def in_shape(shape, x, y) -> bool:
    if "r" in shape:
        return math.hypot(x - shape["x"], y - shape["y"]) <= shape["r"] + 0.8
    if abs(x - shape["x"]) > shape["size"] or abs(y - shape["y"]) > shape["size"]:
        return False
    return point_in_polygon((x, y), shape["poly"])


def main() -> int:
    geometry = json.loads((BUILD / "network_geometry.json").read_text())
    labels = json.loads((BUILD / "pdf_labels.json").read_text())["blocks"]
    raw = json.loads((BUILD / "pdf_raw.json").read_text())
    overrides = json.loads(OVERRIDES_PATH.read_text()) if OVERRIDES_PATH.exists() else {}
    shapes = [s for s in interchange_shapes(raw["markers"]) if s["size"] <= 45]

    stops = []
    for line in geometry["lines"]:
        for stop in line["stops"]:
            stops.append({**stop, "line": f"{line['type']}:{line['code']}"})

    # Union-find over stops.
    parent = list(range(len(stops)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def union(i, j):
        ri, rj = find(i), find(j)
        if ri != rj:
            parent[rj] = ri

    for i, a in enumerate(stops):
        for j in range(i + 1, len(stops)):
            b = stops[j]
            if a["line"] == b["line"]:
                continue
            if math.dist((a["x"], a["y"]), (b["x"], b["y"])) <= NODE_LINK_TOL:
                union(i, j)
    for shape in shapes:
        inside = [i for i, s in enumerate(stops) if in_shape(shape, s["x"], s["y"])]
        for i in inside[1:]:
            if stops[i]["line"] != stops[inside[0]]["line"]:
                union(inside[0], i)
    for rule in overrides.get("node_merge", []):
        idx = [
            min(range(len(stops)), key=lambda i: math.dist((stops[i]["x"], stops[i]["y"]), tuple(p)))
            for p in rule["points"]
        ]
        for i in idx[1:]:
            union(idx[0], i)

    groups: dict[int, list[int]] = {}
    for i in range(len(stops)):
        groups.setdefault(find(i), []).append(i)

    nodes = []
    for members in groups.values():
        pts = [(stops[i]["x"], stops[i]["y"]) for i in members]
        nodes.append(
            {
                "stops": [
                    {"line": stops[i]["line"], "x": round(stops[i]["x"], 3), "y": round(stops[i]["y"], 3),
                     "chain": stops[i]["chain"], "along": round(stops[i]["along"], 2), "kind": stops[i]["kind"]}
                    for i in members
                ],
                "x": round(sum(p[0] for p in pts) / len(pts), 3),
                "y": round(sum(p[1] for p in pts) / len(pts), 3),
            }
        )
    nodes.sort(key=lambda n: (n["y"], n["x"]))

    # Global label assignment: nearest pairs first, labels used once.
    def node_label_distance(node, block):
        return min(box_distance(block, s["x"], s["y"]) for s in node["stops"])

    pairs = []
    for ni, node in enumerate(nodes):
        for bi, block in enumerate(labels):
            if block["x0"] - node["x"] > LABEL_MAX_DIST + 60 or node["x"] - block["x1"] > LABEL_MAX_DIST + 60:
                continue
            d = node_label_distance(node, block)
            if d <= LABEL_MAX_DIST:
                pairs.append((d, ni, bi))
    pairs.sort()
    node_label: dict[int, int] = {}
    used_blocks: set[int] = set()
    for d, ni, bi in pairs:
        if ni in node_label or bi in used_blocks:
            continue
        node_label[ni] = bi
        used_blocks.add(bi)
    # Second pass: nodes without a free label share their nearest label.
    for d, ni, bi in pairs:
        if ni not in node_label:
            node_label[ni] = bi

    for ni, node in enumerate(nodes):
        bi = node_label.get(ni)
        node["id"] = ni
        if bi is None:
            node["label"] = None
            continue
        block = labels[bi]
        node["label"] = block["text"]
        node["labelLines"] = block["lines"]
        node["labelBox"] = [block["x0"], block["top"], block["x1"], block["bottom"]]
        node["labelDist"] = round(node_label_distance(node, block), 2)
        node["labelShared"] = sum(1 for v in node_label.values() if v == bi) > 1

    names = overrides.get("node_names", [])
    for rule in names:
        target = min(nodes, key=lambda n: math.dist((n["x"], n["y"]), tuple(rule["point"])))
        if math.dist((target["x"], target["y"]), tuple(rule["point"])) < 12:
            target["label"] = rule["name"]
            target["labelOverride"] = True

    (BUILD / "network_nodes.json").write_text(json.dumps({"nodes": nodes}, ensure_ascii=False, indent=1))
    unlabeled = [n for n in nodes if not n["label"]]
    shared = [n for n in nodes if n.get("labelShared")]
    print(f"stops={len(stops)} nodes={len(nodes)} unlabeled={len(unlabeled)} shared={len(shared)} unused_labels={len(labels) - len(used_blocks)}")
    for n in unlabeled:
        print("  unlabeled", n["x"], n["y"], [s["line"] for s in n["stops"]])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
