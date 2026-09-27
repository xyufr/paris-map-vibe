#!/usr/bin/env python3
"""Add Métro 15 (south section, drawn dashed = under construction on the PDF).

Geometry is the dashed M15 stroke of paris_map.pdf (color 0.05,1,0.48,0.22,
width 3.5); stops are the interchange markers crossed by it, checked on a PDF
crop. The line is stored with line.status = 'construction' so the app draws it
dashed and leaves it out of route planning. Safe to re-run.

    python3 resources/add_line15.py --dry-run
    python3 resources/add_line15.py
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import pymysql

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_network import BUILD, DB_CONFIG, PALETTE, merge_pieces, simplify  # noqa: E402


M15_STYLE = ("0.05,1,0.48,0.22", 3.5)

# West -> east, PDF points on the dashed line; station_id None = new station.
STOPS = [
    ((1517.4, 1950.7), 319, None),  # Pont de Sèvres
    ((1696.0, 1950.5), 143, None),  # Issy
    ((1828.1, 1950.5), 885, None),  # Clamart (Fort d'Issy - Vanves - Clamart)
    ((1896.6, 1950.5), 754, None),  # Châtillon Montrouge
    ((2023.0, 1950.5), 722, None),  # Bagneux Lucie Aubrac
    ((2099.8, 1950.5), 379, None),  # Arcueil Cachan
    ((2222.9, 1950.5), 1018, None),  # Villejuif Gustave Roussy
    ((2325.7, 1950.5), 518, None),  # Villejuif Louis Aragon
    ((2445.8, 1950.5), 725, None),  # Mairie de Vitry-sur-Seine
    ((2561.5, 1950.5), 156, None),  # Les Ardoines
    ((2676.1, 1950.5), 234, None),  # Le Vert de Maisons
    ((2787.9, 1934.3), 854, None),  # Créteil – L'Échat
    ((2883.3, 1821.5), 489, None),  # Saint-Maur Créteil
    ((2889.4, 1698.5), None, "Champigny Centre"),
    ((3015.6, 1622.8), None, "Villiers Champigny Bry"),
    ((3161.7, 1487.9), 633, None),  # Noisy Champs
]


def m15_path() -> list[list[float]]:
    raw = json.loads((BUILD / "pdf_raw.json").read_text())
    pieces = [r["points"] for r in raw["routes"] if (r["color"], r["width"]) == M15_STYLE]
    # The dashed stroke is broken into short pieces at station markers:
    # chain them west to east into one polyline.
    chains = sorted(merge_pieces(pieces, tol=4.0), key=lambda c: min(p[0] for p in c))
    path: list[tuple[float, float]] = []
    for chain in chains:
        chain = list(chain)
        if path and math.dist(path[-1], chain[-1]) < math.dist(path[-1], chain[0]):
            chain.reverse()
        path.extend(chain)
    return [[round(x, 2), round(y, 2)] for x, y in simplify(path)]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    path = m15_path()
    print(f"M15 path: {len(path)} points from {path[0]} to {path[-1]}, {len(STOPS)} stations")
    if args.dry_run:
        return 0

    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cur:
            cur.execute("SHOW COLUMNS FROM line LIKE 'status'")
            if not cur.fetchone():
                cur.execute("ALTER TABLE line ADD COLUMN status VARCHAR(20) DEFAULT NULL")
            cur.execute("SELECT id FROM line WHERE type='METRO' AND code='15'")
            row = cur.fetchone()
            if row:
                line_id = row[0]
                cur.execute(
                    "UPDATE line SET path_json=%s, color=%s, status='construction' WHERE id=%s",
                    (json.dumps([path]), PALETTE[M15_STYLE[0]], line_id),
                )
            else:
                cur.execute(
                    "INSERT INTO line (code, name, type, color, path_json, status) VALUES (%s, %s, %s, %s, %s, %s)",
                    ("15", "METRO 15", "METRO", PALETTE[M15_STYLE[0]], json.dumps([path]), "construction"),
                )
                line_id = cur.lastrowid
            cur.execute("DELETE FROM line_stations WHERE line_id=%s", (line_id,))
            for order, ((x, y), station_id, new_name) in enumerate(STOPS, 1):
                if station_id is None:
                    cur.execute("SELECT id FROM stations WHERE name2=%s", (new_name,))
                    found = cur.fetchone()
                    if found:
                        station_id = found[0]
                    else:
                        cur.execute(
                            "INSERT INTO stations (name, name2, x, y) VALUES (%s, %s, %s, %s)",
                            (new_name.upper(), new_name, x, y),
                        )
                        station_id = cur.lastrowid
                cur.execute("SELECT name FROM stations WHERE id=%s", (station_id,))
                name = cur.fetchone()[0]
                cur.execute(
                    "INSERT INTO line_stations (line_id, station_id, station_name, station_order) VALUES (%s, %s, %s, %s)",
                    (line_id, station_id, name, order),
                )
        conn.commit()
    finally:
        conn.close()
    print(f"M15 written (line id {line_id})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
