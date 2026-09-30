#!/usr/bin/env python3
"""Rebuild line geometry and stop lists from paris_map.pdf.

Reads `resources/build/pdf_raw.json` (see `pdf_network.py`) and the MySQL
tables, then:

1. assigns PDF route strokes to database lines by stroke color and width,
2. finds the per-line stop markers drawn on those strokes,
3. matches each stop to a database station (position first, then name),
4. writes `resources/build/network.json` plus a human-readable audit report.

Nothing is written to MySQL here; `apply_network.py` does that after review.
"""

from __future__ import annotations

import json
import math
import re
import unicodedata
from collections import defaultdict
from pathlib import Path

import pymysql


ROOT = Path(__file__).resolve().parent
BUILD = ROOT / "build"
RAW_PATH = BUILD / "pdf_raw.json"
OVERRIDES_PATH = ROOT / "network_overrides.json"

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "test001**",
    "database": "paris_map",
    "charset": "utf8mb4",
}

METRO_W = 3.5
TRAM_W = 4.37
RAIL_W = 7.0

# (type, code) -> list of (PDF stroke CMYK key, stroke width)
LINE_STYLES: dict[tuple[str, str], list[tuple[str, float]]] = {
    ("METRO", "1"): [("0,0.19,1,0", METRO_W)],
    ("METRO", "2"): [("1,0.54,0,0", METRO_W)],
    ("METRO", "3"): [("0.46,0.33,1,0", METRO_W)],
    ("METRO", "3b"): [("0.44,0,0.12,0", METRO_W)],
    ("METRO", "4"): [("0.26,0.85,0,0", METRO_W)],
    ("METRO", "5"): [("0,0.53,0.78,0", METRO_W)],
    ("METRO", "6"): [("0.54,0,0.54,0", METRO_W)],
    ("METRO", "7"): [("0,0.47,0.11,0", METRO_W)],
    ("METRO", "7b"): [("0.54,0,0.54,0", METRO_W)],
    ("METRO", "8"): [("0.21,0.38,0,0", METRO_W)],
    ("METRO", "9"): [("0.23,0.11,1,0", METRO_W)],
    ("METRO", "10"): [("0.13,0.3,0.9,0", METRO_W)],
    ("METRO", "11"): [("0.54,0.68,1,0", METRO_W)],
    ("METRO", "12"): [("1,0.24,0.87,0", METRO_W)],
    ("METRO", "13"): [("0.44,0,0.12,0", METRO_W)],
    ("METRO", "14"): [("0.75,1,0,0", METRO_W)],
    ("RER", "A"): [("0,1,0.94,0", RAIL_W)],
    ("RER", "B"): [("0.69,0.34,0,0", RAIL_W)],
    ("RER", "C"): [("0,0.19,1,0", RAIL_W)],
    ("RER", "D"): [("1,0.24,0.87,0", RAIL_W)],
    ("RER", "E"): [("0.26,0.85,0,0", RAIL_W)],
    ("TRAIN", "H"): [("0.54,0.68,1,0", RAIL_W)],
    ("TRAIN", "J"): [("0.23,0.11,1,0", RAIL_W)],
    ("TRAIN", "K"): [("0.46,0.33,1,0", RAIL_W)],
    ("TRAIN", "L"): [("0.21,0.38,0,0", RAIL_W)],
    ("TRAIN", "N"): [("0.82,0,0.54,0", RAIL_W)],
    ("TRAIN", "P"): [("0,0.53,0.78,0", RAIL_W)],
    ("TRAIN", "R"): [("0,0.47,0.11,0", RAIL_W)],
    ("TRAIN", "U"): [("0.05,1,0.48,0.22", RAIL_W)],
    ("TRAM", "1"): [("1,0.54,0,0", TRAM_W)],
    ("TRAM", "2"): [("0.26,0.85,0,0", TRAM_W)],
    ("TRAM", "3A"): [("0,0.53,0.78,0", TRAM_W)],
    ("TRAM", "3B"): [("1,0.24,0.87,0", TRAM_W)],
    ("TRAM", "4"): [("0.13,0.3,0.9,0", TRAM_W)],
    ("TRAM", "5"): [("0.75,1,0,0", TRAM_W)],
    ("TRAM", "6"): [("0,1,0.94,0", TRAM_W)],
    ("TRAM", "7"): [("0.54,0.68,1,0", TRAM_W)],
    ("TRAM", "8"): [("0.46,0.33,1,0", TRAM_W)],
    ("TRAM", "9"): [("0.69,0.34,0,0", TRAM_W)],
    ("TRAM", "10"): [("0.46,0.33,1,0", TRAM_W)],
    ("TRAM", "11"): [("0,0.53,0.78,0", RAIL_W, (1700, 450, 2800, 760)), ("0,0.53,0.78,0", TRAM_W, (1700, 450, 2800, 760))],
    ("TRAM", "12"): [("0.05,1,0.48,0.22", TRAM_W), ("0.05,1,0.48,0.22", RAIL_W)],
    ("TRAM", "13"): [("0.54,0.68,1,0", TRAM_W)],
    ("TRAIN", "V"): [("0.46,0.33,1,0", RAIL_W, (1100, 2080, 1960, 2330))],
    ("TRAM", "14"): [("0.82,0,0.54,0", TRAM_W)],
    ("NAVETTE", "CDG"): [("0.6,0,0,0", METRO_W, (2800, 100, 3200, 400))],
    ("NAVETTE", "ORL"): [("0.6,0,0,0", METRO_W, (2000, 2100, 2400, 2400))],
    ("CABLE", "C1"): [("0.69,0.34,0,0", METRO_W)],
}

# PDF CMYK stroke colors -> IDFM RGB palette. The PDF reuses one CMYK value
# per color family (e.g. M12, RER D and T3b share the dark green).
PALETTE = {
    "0,0.19,1,0": "#FFCE00",
    "1,0.54,0,0": "#0064B0",
    "0.46,0.33,1,0": "#9F9825",
    "0.44,0,0.12,0": "#98D4E2",
    "0.26,0.85,0,0": "#C04191",
    "0,0.53,0.78,0": "#F28E42",
    "0.54,0,0.54,0": "#83C491",
    "0,0.47,0.11,0": "#F3A4BA",
    "0.21,0.38,0,0": "#CEADD2",
    "0.23,0.11,1,0": "#D5C900",
    "0.13,0.3,0.9,0": "#E3B32A",
    "0.54,0.68,1,0": "#8D5E2A",
    "1,0.24,0.87,0": "#00814F",
    "0.75,1,0,0": "#662483",
    "0,1,0.94,0": "#E3051C",
    "0.69,0.34,0,0": "#5291CE",
    "0.82,0,0.54,0": "#00A88F",
    "0.05,1,0.48,0.22": "#B90845",
    "0.6,0,0,0": "#5BC2E7",
    "0,0.9,0.9,0": "#E2231A",
}


def palette_color(key: str | None) -> str | None:
    """RGB hex for a PDF CMYK color key, falling back to a plain conversion."""
    if not key:
        return None
    if key in PALETTE:
        return PALETTE[key]
    c, m, y, k = (float(v) for v in key.split(","))
    return "#{:02X}{:02X}{:02X}".format(
        round(255 * (1 - c) * (1 - k)), round(255 * (1 - m) * (1 - k)), round(255 * (1 - y) * (1 - k))
    )


# Lines that exist on the PDF but not (yet) in the database.
NEW_LINES = {
    ("TRAIN", "V"): {"name": "TRAIN V"},
    ("TRAM", "14"): {"name": "TRAM 14"},
    ("CABLE", "C1"): {"name": "CABLE C1"},
}


def style_key(style) -> tuple[str, float]:
    return (style[0], style[1])


def style_region(style):
    return style[2] if len(style) > 2 else None


def in_region(points, region) -> bool:
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    cx = (min(xs) + max(xs)) / 2
    cy = (min(ys) + max(ys)) / 2
    return region[0] <= cx <= region[2] and region[1] <= cy <= region[3]


def normalize(value: str | None) -> str:
    value = (value or "").replace("’", "'").replace("`", "'").replace("´", "'")
    value = value.replace("œ", "oe").replace("Œ", "OE").replace("æ", "ae")
    value = unicodedata.normalize("NFKD", value)
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    value = value.casefold()
    value = re.sub(r"[^a-z0-9]+", " ", value)
    tokens = []
    for token in value.split():
        token = {"st": "saint", "ste": "sainte", "pte": "porte", "av": "avenue", "pdt": "president"}.get(token, token)
        tokens.append(token)
    return " ".join(tokens)


def canonical_type(value: str) -> str:
    value = str(value or "").upper()
    return "TRAM" if value == "TRAMWAY" else value


# --- geometry helpers -------------------------------------------------------

def project(point, a, b):
    ax, ay = a
    bx, by = b
    dx, dy = bx - ax, by - ay
    length2 = dx * dx + dy * dy
    t = 0.0 if length2 == 0 else max(0.0, min(1.0, ((point[0] - ax) * dx + (point[1] - ay) * dy) / length2))
    px, py = ax + t * dx, ay + t * dy
    return math.hypot(point[0] - px, point[1] - py), (px, py), t


def polyline_nearest(point, points):
    best = (float("inf"), None, 0.0)
    walked = 0.0
    for a, b in zip(points, points[1:]):
        dist, proj, t = project(point, a, b)
        seg = math.dist(a, b)
        if dist < best[0]:
            best = (dist, proj, walked + t * seg)
        walked += seg
    return best


def polyline_length(points):
    return sum(math.dist(a, b) for a, b in zip(points, points[1:]))


def dedupe_pieces(pieces):
    """Drop pieces drawn twice: a piece whose whole length lies within 1.5pt
    of another (longer or equal) piece adds no geometry."""
    pts_list = [[tuple(p) for p in piece] for piece in pieces if len(piece) > 1]
    order = sorted(range(len(pts_list)), key=lambda i: -polyline_length(pts_list[i]))
    kept: list[list[tuple[float, float]]] = []
    for i in order:
        pts = pts_list[i]
        samples = []
        for a, b in zip(pts, pts[1:]):
            n = max(1, int(math.dist(a, b) / 2))
            samples.extend((a[0] + (b[0] - a[0]) * k / n, a[1] + (b[1] - a[1]) * k / n) for k in range(n))
        samples.append(pts[-1])
        contained = any(
            all(polyline_nearest(p, other)[0] <= 1.5 for p in samples)
            for other in kept
        )
        if not contained:
            kept.append(pts)
    return kept


def merge_pieces(pieces: list[list[tuple[float, float]]], tol: float = 1.5) -> list[list[tuple[float, float]]]:
    """Join polylines whose endpoints touch into longer chains (no branching)."""
    chains = [list(map(tuple, p)) for p in dedupe_pieces(pieces)]
    changed = True
    while changed:
        changed = False
        for i in range(len(chains)):
            for j in range(len(chains)):
                if i == j or not chains[i] or not chains[j]:
                    continue
                a, b = chains[i], chains[j]
                joined = None
                if math.dist(a[-1], b[0]) <= tol:
                    joined = a + b[1:]
                elif math.dist(a[-1], b[-1]) <= tol:
                    joined = a + b[::-1][1:]
                elif math.dist(a[0], b[-1]) <= tol:
                    joined = b + a[1:]
                elif math.dist(a[0], b[0]) <= tol:
                    joined = b[::-1] + a[1:]
                if joined is None:
                    continue
                # Only merge when the join point is not a junction of 3+ ends.
                ends = [c[k] for c in chains if c for k in (0, -1)]
                join_point = a[-1] if joined[: len(a)] == a else a[0]
                if sum(1 for e in ends if math.dist(e, join_point) <= tol) > 2:
                    continue
                chains[i] = joined
                chains[j] = []
                changed = True
        chains = [c for c in chains if c]
    return chains


def simplify(points, tol=0.35):
    """Ramer-Douglas-Peucker to keep output compact."""
    if len(points) < 3:
        return points
    first, last = points[0], points[-1]
    index, dmax = 0, 0.0
    for i in range(1, len(points) - 1):
        d, _, _ = project(points[i], first, last)
        if d > dmax:
            index, dmax = i, d
    if dmax > tol:
        left = simplify(points[: index + 1], tol)
        right = simplify(points[index:], tol)
        return left[:-1] + right
    return [first, last]


# --- data loading -----------------------------------------------------------

def load_db():
    conn = pymysql.connect(**DB_CONFIG, cursorclass=pymysql.cursors.DictCursor)
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM line")
            lines = cur.fetchall()
            cur.execute("SELECT * FROM stations")
            stations = cur.fetchall()
            cur.execute("SELECT * FROM line_stations ORDER BY line_id, station_order IS NULL, station_order, id")
            memberships = cur.fetchall()
    finally:
        conn.close()
    return lines, stations, memberships


def load_overrides() -> dict:
    if OVERRIDES_PATH.exists():
        return json.loads(OVERRIDES_PATH.read_text())
    return {}


# --- stop detection -----------------------------------------------------------

def marker_rings(markers, color):
    """Stop markers of one line: colored ring (white fill) or colored dot."""
    out = []
    for m in markers:
        size = max(m["w"], m["h"])
        if size < 2.6 or size > 9.5 or abs(m["w"] - m["h"]) > 1.2:
            continue
        if size < 3.4 and m["fill"] != color:
            continue
        if m["stroke"] == color and m["fill"] is None and m["lw"] in (1.09, 1.53, 0.98, 1.31, 0.88):
            out.append((m["x"], m["y"], size, "ring"))
        elif m["fill"] == color and m["stroke"] is None and size <= 8:
            out.append((m["x"], m["y"], size, "dot"))
    uniq = []
    for item in out:
        if not any(math.dist(item[:2], u[:2]) < 1.2 for u in uniq):
            uniq.append(item)
    return uniq


def point_in_polygon(point, polygon) -> bool:
    x, y = point
    inside = False
    for (x1, y1), (x2, y2) in zip(polygon, polygon[1:] + polygon[:1]):
        if (y1 > y) != (y2 > y):
            xin = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if x < xin:
                inside = not inside
    return inside


def interchange_shapes(markers):
    """Black-rimmed station shapes: circles and capsules (as polygons)."""
    from pdf_network import flatten_path

    shapes = []
    for m in markers:
        if m["stroke"] != "0,0,0,1" or m["lw"] not in (0.71, 0.88, 0.98, 1.09, 1.31):
            continue
        size = max(m["w"], m["h"])
        if size < 5.5 or size > 60:
            continue
        if m.get("path"):
            polys = flatten_path([tuple([c[0]] + [tuple(v) for v in c[1:]]) for c in m["path"]])
            if polys:
                poly = polys[0]
                area = abs(sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(poly, poly[1:] + poly[:1]))) / 2
                perimeter = sum(math.dist(a, b) for a, b in zip(poly, poly[1:] + poly[:1]))
                thickness = 2 * area / perimeter if perimeter else size
                shapes.append({"x": m["x"], "y": m["y"], "size": size, "poly": poly, "area": m["w"] * m["h"], "thickness": thickness})
                continue
        if abs(m["w"] - m["h"]) <= 1.2:
            shapes.append({"x": m["x"], "y": m["y"], "size": size, "r": size / 2, "area": m["w"] * m["h"], "thickness": size})
    return shapes


def resample(points, step=0.5):
    out = []
    walked = 0.0
    for a, b in zip(points, points[1:]):
        seg = math.dist(a, b)
        n = max(1, int(seg / step))
        for i in range(n):
            t = i / n
            out.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, walked + seg * t))
        walked += seg
    out.append((points[-1][0], points[-1][1], walked))
    return out


def shape_stops(chains, shapes):
    stops = []
    for ci, chain in enumerate(chains):
        samples = resample(chain)
        xs = [s[0] for s in samples]
        ys = [s[1] for s in samples]
        x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
        for shape in shapes:
            if shape["x"] < x0 - 40 or shape["x"] > x1 + 40 or shape["y"] < y0 - 40 or shape["y"] > y1 + 40:
                continue
            if "r" in shape:
                inside = [s for s in samples if math.hypot(s[0] - shape["x"], s[1] - shape["y"]) <= shape["r"]]
            else:
                inside = [s for s in samples if abs(s[0] - shape["x"]) <= shape["size"] and abs(s[1] - shape["y"]) <= shape["size"]
                          and point_in_polygon(s[:2], shape["poly"])]
            if len(inside) < 2:
                continue
            # A line running along a capsule (not across it) does not stop there.
            run = inside[-1][2] - inside[0][2]
            if run > shape["thickness"] * 1.6 + 2.5:
                continue
            mid = inside[len(inside) // 2]
            stops.append({"x": mid[0], "y": mid[1], "size": shape["size"], "kind": "shape", "chain": ci, "along": mid[2], "area": shape["area"]})
    return stops


def label_words_near(words, x, y, radius=70):
    near = []
    for w in words:
        cx = (w["x0"] + w["x1"]) / 2
        cy = (w["top"] + w["bottom"]) / 2
        dx = max(w["x0"] - x, 0, x - w["x1"])
        dy = max(w["top"] - y, 0, y - w["bottom"])
        d = math.hypot(dx, dy)
        if d <= radius:
            near.append((d, w))
    near.sort(key=lambda item: item[0])
    return near


def main() -> int:
    raw = json.loads(RAW_PATH.read_text())
    overrides = load_overrides()
    lines, stations, memberships = load_db()
    station_by_id = {s["id"]: s for s in stations}

    routes_by_style: dict[tuple[str, float], list[dict]] = defaultdict(list)
    for index, route in enumerate(raw["routes"]):
        route["index"] = index
        routes_by_style[(route["color"], route["width"])].append(route)

    db_line_key = {}
    for line in lines:
        db_line_key[line["id"]] = (canonical_type(line["type"]), str(line["code"]))

    members_by_line: dict[int, list[dict]] = defaultdict(list)
    for row in memberships:
        members_by_line[row["line_id"]].append(row)

    # Lines keyed by (type, code); includes lines that exist only in overrides.
    spec_lines = {}
    for line in lines:
        key = db_line_key[line["id"]]
        spec_lines[key] = {"db": line, "key": key}
    for key in NEW_LINES:
        spec_lines.setdefault(key, {"db": None, "key": key})

    # ---- assign pieces --------------------------------------------------------
    style_owners: dict[tuple[str, float], list[tuple[str, str]]] = defaultdict(list)
    regional: dict[tuple[str, float], list[tuple[tuple, tuple[str, str]]]] = defaultdict(list)
    for key, styles in LINE_STYLES.items():
        for style in styles:
            if style_region(style):
                regional[style_key(style)].append((style_region(style), key))
            else:
                style_owners[style_key(style)].append(key)

    def db_points_for(key):
        item = spec_lines.get(key)
        if not item or not item["db"]:
            return []
        pts = []
        for m in members_by_line.get(item["db"]["id"], []):
            s = station_by_id.get(m["station_id"])
            if s and s["x"] is not None:
                pts.append((s["x"], s["y"]))
        return pts

    forced = {}
    for rule in overrides.get("piece_owner", []):
        forced[rule["index"]] = (rule["type"], rule["code"])

    pieces_by_line: dict[tuple[str, str], list[dict]] = defaultdict(list)
    unassigned = []
    for style, routes in routes_by_style.items():
        owners = style_owners.get(style, [])
        for route in routes:
            if route["index"] in forced:
                owner = forced[route["index"]]
                if owner[0] != "SKIP":
                    pieces_by_line[owner].append(route)
                continue
            if route["dashed"]:
                unassigned.append(route)
                continue
            region_owner = next((key for region, key in regional.get(style, []) if in_region(route["points"], region)), None)
            if region_owner:
                pieces_by_line[region_owner].append(route)
                continue
            if not owners:
                unassigned.append(route)
                continue
            if len(owners) == 1:
                pieces_by_line[owners[0]].append(route)
                continue
            scores = []
            for key in owners:
                pts = db_points_for(key)
                hits = sum(1 for p in pts if polyline_nearest(p, route["points"])[0] < 8)
                nearest = min((polyline_nearest(p, route["points"])[0] for p in pts), default=1e9)
                scores.append((-hits, nearest, key))
            scores.sort()
            pieces_by_line[scores[0][2]].append(route)

    # ---- stops ------------------------------------------------------------------
    words = raw["words"]
    shapes = interchange_shapes(raw["markers"])
    network_lines = []
    report = []
    used_station_ids = set()
    for key, item in sorted(spec_lines.items()):
        pieces = pieces_by_line.get(key, [])
        styles = LINE_STYLES.get(key, [])
        color = styles[0][0] if styles else None
        width = styles[0][1] if styles else None
        chains = merge_pieces([p["points"] for p in pieces])
        stops = []
        if color:
            for x, y, size, kind in marker_rings(raw["markers"], color):
                best = min((polyline_nearest((x, y), c) + (ci,) for ci, c in enumerate(chains)), default=None, key=lambda v: v[0])
                if best is None or best[0] > 3.2:
                    continue
                stops.append({"x": x, "y": y, "size": size, "kind": kind, "chain": best[3], "along": best[2]})
            # Interchange shapes crossed by the line, unless a ring is already there.
            for stop in sorted(shape_stops(chains, shapes), key=lambda s: s["area"]):
                if any(s["chain"] == stop["chain"] and abs(s["along"] - stop["along"]) < 12 for s in stops):
                    continue
                if any(math.dist((s["x"], s["y"]), (stop["x"], stop["y"])) < 12 for s in stops):
                    continue
                stops.append(stop)
        # One stop per station marker cluster on a line (rings drawn twice,
        # ring + surrounding shape, or two branch dots in one capsule).
        priority = {"ring": 0, "dot": 1, "shape": 2}
        kept = []
        for stop in sorted(stops, key=lambda s: (priority.get(s["kind"], 3), s["x"], s["y"])):
            if any(math.dist((stop["x"], stop["y"]), (k["x"], k["y"])) < 10 for k in kept):
                continue
            kept.append(stop)
        stops = sorted(kept, key=lambda s: (s["chain"], s["along"]))
        db = item["db"]
        members = members_by_line.get(db["id"], []) if db else []
        report.append({"key": key, "pieces": len(pieces), "chains": len(chains), "stops": len(stops), "db_members": len(members)})
        network_lines.append(
            {
                "type": key[0],
                "code": key[1],
                "dbId": db["id"] if db else None,
                "color": color,
                "width": width,
                "chains": [[[round(x, 2), round(y, 2)] for x, y in simplify(c)] for c in chains],
                "stops": stops,
                "pieceIndexes": [p["index"] for p in pieces],
            }
        )

    BUILD.mkdir(exist_ok=True)
    future = [
        {"color": r["color"], "width": r["width"], "points": [[round(x, 2), round(y, 2)] for x, y in simplify([tuple(p) for p in r["points"]])]}
        for r in unassigned
        if r["dashed"] or (r["color"], r["width"]) == ("0,0.9,0.9,0", RAIL_W)
    ]
    (BUILD / "network_geometry.json").write_text(json.dumps({"lines": network_lines, "unassigned": [r["index"] for r in unassigned], "future": future}, ensure_ascii=False))
    for row in report:
        print(row)
    print("unassigned pieces:", len(unassigned))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
