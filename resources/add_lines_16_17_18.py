#!/usr/bin/env python3
"""Add Métro 16, 17 and 18 (Grand Paris Express) from paris_map_v2.pdf.

paris_map_v2.pdf is the IDFM plan of February 2026 (same page layout as
paris_map.pdf). Sections drawn dashed are stored with line.status =
'construction' (drawn dashed, excluded from route planning):

- M16 Saint-Denis Pleyel - Clichy Montfermeil, dashed (opening "mars 2027")
- M17 Saint-Denis Pleyel - Le Bourget Aéroport, dashed
- M18 Christ de Saclay - Massy-Palaiseau, solid on the PDF and open; the
  dashed Massy-Palaiseau - Aéroport d'Orly section is a separate
  "METRO 18 (prolongement)" construction line, as for RER E. The Versailles
  section of the January plan is gone.

Geometry is the line's 3.5pt stroke on the v2 PDF; stops are the markers on
it, checked on PDF crops. The v2 plan also moves the Saint-Denis Pleyel
capsule west (M14 terminus) and the Stade de France - Saint-Denis RER D dot
south of the new dashed lines; both stations and the M14 tail follow it.
Safe to re-run.

    python3 resources/add_lines_16_17_18.py --dry-run
    python3 resources/add_lines_16_17_18.py
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import pymysql

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_network import DB_CONFIG, PALETTE, merge_pieces, simplify  # noqa: E402
from pdf_network import extract  # noqa: E402


PDF_V2 = Path(__file__).resolve().parent / "paris_map_v2.pdf"

# (code, line name, status, CMYK of the stroke, dashed strokes only (None =
# any), stops in line order). A stop is (station id, expected name2) or
# (None, new name, (x, y) PDF dot center).
LINES = [
    ("16", "METRO 16", "construction", "0,0.47,0.11,0", None, [
        (1020, "Saint-Denis Pleyel"),
        (529, "La Courneuve Six Routes"),
        (640, "Le Bourget"),
        (None, "Parc du Blanc-Mesnil", (2851.9, 654.7)),
        (None, "Aulnay Val Francilia", (2851.9, 613.4)),
        (158, "Sevran Beaudottes"),
        (663, "Sevran – Livry"),
        (185, "Clichy Montfermeil"),
    ]),
    ("17", "METRO 17", "construction", "0.23,0.11,1,0", None, [
        (1020, "Saint-Denis Pleyel"),
        (529, "La Courneuve Six Routes"),
        (640, "Le Bourget"),
        (None, "Le Bourget Aéroport", (2784.9, 584.7)),
    ]),
    ("18", "METRO 18", None, "0.82,0,0.54,0", False, [
        (None, "Christ de Saclay", (1430.1, 2399.6)),
        (None, "Université Paris – Saclay", (1574.3, 2399.6)),
        (None, "Polytechnique", (1706.6, 2399.6)),
        (757, "Massy – Palaiseau"),
    ]),
    ("18", "METRO 18 (prolongement)", "construction", "0.82,0,0.54,0", True, [
        (757, "Massy – Palaiseau"),
        (None, "Massy Opéra", (2029.5, 2287.6)),
        (None, "Antonypole Wissous Centre", (2102.7, 2287.6)),
        (1015, "Aéroport d’Orly"),
    ]),
]

# Stations moved on the v2 plan: id -> (x, y) PDF dot center.
MOVED_STATIONS = {
    1020: (2071.5, 830.71),  # Saint-Denis Pleyel, M14 dot of the 14/16/17 capsule
    289: (2091.2, 862.1),  # Stade de France - Saint-Denis (RER D)
}
M14_ID = 14
M14_OLD_END = (2111.14, 830.72)
M14_NEW_END = [2072.46, 830.72]


def line_path(raw: dict, color: str, dashed: bool | None, start: tuple[float, float]) -> list[list[float]]:
    pieces = [
        r["points"] for r in raw["routes"]
        if r["color"] == color and r["width"] == 3.5 and dashed in (None, r["dashed"])
    ]
    # Keep only pieces that belong to the new line (the CMYK is shared with
    # M7/M9/T14/N): chain everything, then take the chain that touches start.
    chains = merge_pieces(pieces, tol=4.0)
    chain = min(chains, key=lambda c: min(math.dist(start, c[0]), math.dist(start, c[-1])))
    chain = list(chain)
    if math.dist(start, chain[-1]) < math.dist(start, chain[0]):
        chain.reverse()
    if math.dist(start, chain[0]) > 15:
        raise SystemExit(f"no {color} stroke starts at {start}")
    return [[round(x, 2), round(y, 2)] for x, y in simplify(chain)]


def nearest(path: list[list[float]], point: tuple[float, float]) -> float:
    best = math.inf
    for a, b in zip(path, path[1:]):
        dx, dy = b[0] - a[0], b[1] - a[1]
        length = dx * dx + dy * dy
        t = 0.0 if length == 0 else max(0.0, min(1.0, ((point[0] - a[0]) * dx + (point[1] - a[1]) * dy) / length))
        best = min(best, math.dist(point, (a[0] + t * dx, a[1] + t * dy)))
    return best


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    raw = extract(PDF_V2)
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cur:
            def station(stop):
                if stop[0] is not None:
                    cur.execute("SELECT id, name, name2, x, y FROM stations WHERE id=%s", (stop[0],))
                    row = cur.fetchone()
                    if not row or row[2] != stop[1]:
                        raise SystemExit(f"station {stop[0]} is {row and row[2]!r}, expected {stop[1]!r}")
                    x, y = MOVED_STATIONS.get(row[0], (row[3], row[4]))
                    return row[0], row[1], (x, y)
                cur.execute("SELECT id, name FROM stations WHERE name2=%s", (stop[1],))
                row = cur.fetchone()
                return (row[0] if row else None), (row[1] if row else stop[1].upper()), stop[2]

            plans = []
            for code, name, status, color, dashed, stops in LINES:
                resolved = [station(s) for s in stops]
                path = line_path(raw, color, dashed, resolved[0][2])
                print(f"{name}: {len(path)} points {path[0]} -> {path[-1]}")
                for (sid, _, xy), stop in zip(resolved, stops):
                    gap = nearest(path, xy)
                    flag = "" if gap < 8 else "  <-- far from path"
                    print(f"  {sid or 'new':>4} {stop[1]} ({xy[0]:.1f}, {xy[1]:.1f}) gap {gap:.1f}{flag}")
                plans.append((code, name, status, color, path, stops, resolved))
            if args.dry_run:
                return 0

            for sid, (x, y) in MOVED_STATIONS.items():
                cur.execute("UPDATE stations SET x=%s, y=%s WHERE id=%s", (x, y, sid))
            cur.execute("SELECT path_json FROM line WHERE id=%s", (M14_ID,))
            m14 = json.loads(cur.fetchone()[0])
            for seg in m14:
                for i in (0, -1):
                    if math.dist(seg[i], M14_OLD_END) < 1:
                        seg[i] = M14_NEW_END
            cur.execute("UPDATE line SET path_json=%s WHERE id=%s", (json.dumps(m14), M14_ID))

            for code, line_name, status, color, path, stops, resolved in plans:
                cur.execute("SELECT id FROM line WHERE type='METRO' AND code=%s AND name=%s", (code, line_name))
                row = cur.fetchone()
                if row:
                    line_id = row[0]
                    cur.execute(
                        "UPDATE line SET path_json=%s, color=%s, status=%s WHERE id=%s",
                        (json.dumps([path]), PALETTE[color], status, line_id),
                    )
                else:
                    cur.execute(
                        "INSERT INTO line (code, name, type, color, path_json, status) VALUES (%s, %s, %s, %s, %s, %s)",
                        (code, line_name, "METRO", PALETTE[color], json.dumps([path]), status),
                    )
                    line_id = cur.lastrowid
                cur.execute("DELETE FROM line_stations WHERE line_id=%s", (line_id,))
                for order, (stop, (sid, name, (x, y))) in enumerate(zip(stops, resolved), 1):
                    if sid is None:
                        cur.execute(
                            "INSERT INTO stations (name, name2, x, y) VALUES (%s, %s, %s, %s)",
                            (name, stop[1], x, y),
                        )
                        sid = cur.lastrowid
                    cur.execute(
                        "INSERT INTO line_stations (line_id, station_id, station_name, station_order) VALUES (%s, %s, %s, %s)",
                        (line_id, sid, name, order),
                    )
                print(f"{line_name} written (line id {line_id})")
        conn.commit()
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
