#!/usr/bin/env python3
"""Add the RER E western extension (drawn dashed = under construction on the PDF).

Nanterre La Folie -> Poissy -> Mantes-la-Jolie. The geometry is the dashed
"RER E (prolongement)" stroke of paris_map.pdf (color of RER E, width 7.0),
read from future_lines.json, plus the short solid pieces of it that the
pipeline attached to RER E at stop markers (they are removed from RER E so the
extension is drawn dashed end to end). Stops reuse the Transilien J / RER A
stations crossed by it. Stored with line.status = 'construction': drawn dashed,
excluded from route planning. Safe to re-run.

    python3 resources/add_rer_e_west.py --dry-run
    python3 resources/add_rer_e_west.py
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import pymysql

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_network import DB_CONFIG, merge_pieces, simplify  # noqa: E402


FUTURE = Path(__file__).resolve().parent / "future_lines.json"
ROUTE_NAME = "RER E (prolongement)"
CODE = "E"
NAME = "RER E (prolongement)"
RER_E_ID = 24
# Pieces of RER E west of Nanterre La Folie (x < START_X) belong to the extension.
START_X = 1380.0
START = (1386.19, 1291.95)  # west end of the solid RER E stroke
# East -> west; (station id, expected name).
STOPS = [
    (1023, "Nanterre La Folie"),
    (976, "Poissy"),
    (365, "Villennes-sur-Seine"),
    (439, "Vernouillet Verneuil"),
    (134, "Les Clairières Verneuil"),
    (619, "Les Mureaux"),
    (288, "Aubergenville Élisabethville"),
    (821, "Épône Mézières"),
    (639, "Mantes Station"),
    (446, "Mantes-la-Jolie"),
]


def west_pieces(segments: list) -> tuple[list, list]:
    keep, west = [], []
    for seg in segments:
        (west if max(p[0] for p in seg) < START_X else keep).append(seg)
    return keep, west


def extension_path(stubs: list) -> list[list[float]]:
    routes = json.loads(FUTURE.read_text())["routes"]
    pieces = [r["points"] for r in routes if r["name"] == ROUTE_NAME] + stubs
    # Dashes and stubs are separate pieces a few points apart: chain them.
    chains = merge_pieces(pieces, tol=16.0)
    # Order chains from Nanterre (east) to Mantes (west) along the stroke.
    chains = [list(c) for c in chains]
    start = max(chains, key=lambda c: max(p[0] for p in c))
    if start[0][0] < start[-1][0]:
        start.reverse()
    path, rest = list(start), [c for c in chains if c is not start]
    while rest:
        best = min(rest, key=lambda c: min(math.dist(path[-1], c[0]), math.dist(path[-1], c[-1])))
        rest.remove(best)
        if math.dist(path[-1], best[-1]) < math.dist(path[-1], best[0]):
            best.reverse()
        if math.dist(path[-1], best[0]) > 40:
            raise SystemExit(f"gap in extension path at {path[-1]} -> {best[0]}")
        path.extend(best)
    # The solid RER E ends at Nanterre La Folie: start the dashed part there.
    path = [START] + [p for p in path if p[0] < START[0]]
    return [[round(x, 2), round(y, 2)] for x, y in simplify(path)]


def seg_dist(p: tuple, a: list, b: list) -> float:
    dx, dy = b[0] - a[0], b[1] - a[1]
    t = 0.0 if dx == dy == 0 else max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / (dx * dx + dy * dy)))
    return math.dist(p, (a[0] + t * dx, a[1] + t * dy))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT code, path_json FROM line WHERE id=%s", (RER_E_ID,))
            code, path_json = cur.fetchone()
            if code != "E":
                raise SystemExit(f"line {RER_E_ID} is {code}, expected RER E")
            keep, stubs = west_pieces(json.loads(path_json))
            path = extension_path(stubs)
            print(f"RER E: {len(stubs)} western stub(s) moved to the extension")
            print(f"Extension path: {len(path)} points from {path[0]} to {path[-1]}")
            for station_id, expected in STOPS:
                cur.execute("SELECT name2, x, y FROM stations WHERE id=%s", (station_id,))
                row = cur.fetchone()
                if not row:
                    raise SystemExit(f"station {station_id} ({expected}) not found")
                gap = min(seg_dist((row[1], row[2]), a, b) for a, b in zip(path, path[1:]))
                print(f"  stop {station_id}: {row[0]} ({row[1]:.1f}, {row[2]:.1f}) {gap:.1f}pt from path")
            if args.dry_run:
                return 0
            if stubs:
                cur.execute("UPDATE line SET path_json=%s WHERE id=%s", (json.dumps(keep), RER_E_ID))
            cur.execute("SELECT id FROM line WHERE type='RER' AND code=%s AND status='construction'", (CODE,))
            row = cur.fetchone()
            cur.execute("SELECT color, text_color FROM line WHERE id=%s", (RER_E_ID,))
            color, text_color = cur.fetchone()
            if row:
                line_id = row[0]
                cur.execute(
                    "UPDATE line SET name=%s, path_json=%s, color=%s, text_color=%s WHERE id=%s",
                    (NAME, json.dumps([path]), color, text_color, line_id),
                )
            else:
                cur.execute(
                    "INSERT INTO line (code, name, type, color, text_color, path_json, status) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (CODE, NAME, "RER", color, text_color, json.dumps([path]), "construction"),
                )
                line_id = cur.lastrowid
            cur.execute("DELETE FROM line_stations WHERE line_id=%s", (line_id,))
            for order, (station_id, _) in enumerate(STOPS, 1):
                cur.execute("SELECT name FROM stations WHERE id=%s", (station_id,))
                cur.execute(
                    "INSERT INTO line_stations (line_id, station_id, station_name, station_order) VALUES (%s, %s, %s, %s)",
                    (line_id, station_id, cur.fetchone()[0], order),
                )
        conn.commit()
    finally:
        conn.close()
    print(f"RER E extension written (line id {line_id})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
