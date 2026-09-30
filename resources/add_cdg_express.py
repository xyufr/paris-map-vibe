#!/usr/bin/env python3
"""Add CDG Express (drawn dashed = under construction on the PDF).

Nonstop link Paris Gare de l'Est <-> Aéroport Charles de Gaulle 2 TGV. The
geometry is the dashed red stroke of paris_map.pdf (color 0,0.9,0.9,0, width
7.0). Stored with line.status = 'construction': drawn dashed, excluded from
route planning. Safe to re-run.

    python3 resources/add_cdg_express.py --dry-run
    python3 resources/add_cdg_express.py
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pymysql

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_network import BUILD, DB_CONFIG, PALETTE, merge_pieces, polyline_length, simplify  # noqa: E402


STYLE = ("0,0.9,0.9,0", 7.0)
CODE = "CDGX"
NAME = "CDG Express"
# Paris end first, as on the PDF badge placement; (station id, expected name).
STOPS = [
    (860, "Gare de l’Est"),
    (572, "Aéroport Charles de Gaulle 2 TGV"),
]


def cdgx_path() -> list[list[float]]:
    raw = json.loads((BUILD / "pdf_raw.json").read_text())
    pieces = [r["points"] for r in raw["routes"] if (r["color"], r["width"]) == STYLE]
    # Dashes are separate pieces a few points apart: chain them.
    chain = max(merge_pieces(pieces, tol=8.0), key=polyline_length)
    if chain[0][1] < chain[-1][1]:
        chain = chain[::-1]  # start at Gare de l'Est (south end)
    return [[round(x, 2), round(y, 2)] for x, y in simplify(chain)]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    path = cdgx_path()
    print(f"CDG Express path: {len(path)} points from {path[0]} to {path[-1]}")

    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cur:
            for station_id, expected in STOPS:
                cur.execute("SELECT name2, x, y FROM stations WHERE id=%s", (station_id,))
                row = cur.fetchone()
                if not row:
                    raise SystemExit(f"station {station_id} ({expected}) not found")
                print(f"  stop {station_id}: {row[0]} ({row[1]:.1f}, {row[2]:.1f})")
            if args.dry_run:
                return 0
            cur.execute("SHOW COLUMNS FROM line LIKE 'status'")
            if not cur.fetchone():
                cur.execute("ALTER TABLE line ADD COLUMN status VARCHAR(20) DEFAULT NULL")
            color = PALETTE[STYLE[0]]
            cur.execute("SELECT id FROM line WHERE type='TRAIN' AND code=%s", (CODE,))
            row = cur.fetchone()
            if row:
                line_id = row[0]
                cur.execute(
                    "UPDATE line SET name=%s, path_json=%s, color=%s, status='construction' WHERE id=%s",
                    (NAME, json.dumps([path]), color, line_id),
                )
            else:
                cur.execute(
                    "INSERT INTO line (code, name, type, color, path_json, status) VALUES (%s, %s, %s, %s, %s, %s)",
                    (CODE, NAME, "TRAIN", color, json.dumps([path]), "construction"),
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
    print(f"CDG Express written (line id {line_id})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
