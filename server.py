#!/usr/bin/env python3
"""Local Paris metro map server.

Serves a D3/SVG map and a small JSON API backed by the local MySQL database.
The frontend follows the d3-metro idea: D3 renders a zoomable SVG transit
network from station nodes, route paths, and line membership data.
`resources/export_static.py` writes the same payload to public/data/map.json
for the Cloudflare Worker deployment.
"""

from __future__ import annotations

import json
import math
import mimetypes
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

import pymysql

from network_graph import line_edges, locate_stops


ROOT = Path(__file__).resolve().parent
PUBLIC_DIR = ROOT / "public"
FUTURE_PATH = ROOT / "resources" / "future_lines.json"

PDF_WIDTH = 3600.0
PDF_HEIGHT = 2777.95

DB_CONFIG = {
    "host": os.environ.get("PARIS_MAP_DB_HOST", "localhost"),
    "user": os.environ.get("PARIS_MAP_DB_USER", "root"),
    "password": os.environ.get("PARIS_MAP_DB_PASSWORD", "test001**"),
    "database": os.environ.get("PARIS_MAP_DB_NAME", "paris_map"),
    "charset": "utf8mb4",
}

TYPE_COLORS = {
    "METRO": "#4a5568",
    "RER": "#2563eb",
    "TRAIN": "#64748b",
    "TRAM": "#0f766e",
    "CABLE": "#1e40af",
    "NAVETTE": "#9333ea",
}

TYPE_ORDER = ("METRO", "RER", "TRAIN", "TRAM", "CABLE", "NAVETTE")


def canonical_type(value: str | None) -> str:
    value = str(value or "").upper()
    return "TRAM" if value == "TRAMWAY" else value


def line_color(line_type: str, color: str | None) -> str:
    return color or TYPE_COLORS.get(canonical_type(line_type), "#475569")


def text_color(background: str) -> str:
    value = background.lstrip("#")
    try:
        r, g, b = (int(value[i : i + 2], 16) / 255 for i in (0, 2, 4))
    except ValueError:
        return "#ffffff"
    luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return "#111827" if luminance > 0.6 else "#ffffff"


def json_point(value) -> list[float] | None:
    if not isinstance(value, (list, tuple)) or len(value) < 2:
        return None
    try:
        x = float(value[0])
        y = float(value[1])
    except (TypeError, ValueError):
        return None
    if not math.isfinite(x) or not math.isfinite(y):
        return None
    return [round(x, 2), round(y, 2)]


def parse_path_segments(path_json: str | None) -> list[list[list[float]]]:
    """Accept a single path [[x, y], ...] or segments [[[x, y], ...], ...]."""
    if not path_json:
        return []
    try:
        raw = json.loads(path_json)
    except (TypeError, ValueError):
        return []
    if not isinstance(raw, list):
        return []
    single = [p for p in (json_point(item) for item in raw) if p]
    if len(single) == len(raw) and len(single) >= 2:
        return [single]
    segments = []
    for segment in raw:
        if isinstance(segment, list):
            points = [p for p in (json_point(item) for item in segment) if p]
            if len(points) >= 2:
                segments.append(points)
    return segments


def load_future_routes() -> list[dict]:
    if not FUTURE_PATH.exists():
        return []
    try:
        return json.loads(FUTURE_PATH.read_text()).get("routes", [])
    except (OSError, ValueError):
        return []


def fetch_map_data() -> dict:
    conn = pymysql.connect(**DB_CONFIG, cursorclass=pymysql.cursors.DictCursor)
    try:
        with conn.cursor() as cur:
            cur.execute("SHOW COLUMNS FROM line LIKE 'status'")
            status_column = ", status" if cur.fetchone() else ""
            cur.execute(f"SELECT id, code, name, type, color, text_color, path_json, sort_order{status_column} FROM line")
            raw_lines = cur.fetchall()
            cur.execute(
                """
                SELECT s.id, s.name, s.name2, s.x, s.y
                FROM stations s
                WHERE s.x IS NOT NULL AND s.y IS NOT NULL
                  AND EXISTS (SELECT 1 FROM line_stations ls WHERE ls.station_id = s.id)
                ORDER BY s.id
                """
            )
            stations = cur.fetchall()
            cur.execute(
                """
                SELECT ls.line_id, ls.station_id, ls.station_order
                FROM line_stations ls
                JOIN stations s ON s.id = ls.station_id
                WHERE s.x IS NOT NULL
                ORDER BY ls.line_id, ls.station_order IS NULL, ls.station_order, ls.id
                """
            )
            memberships = cur.fetchall()
    finally:
        conn.close()

    station_by_id = {int(s["id"]): s for s in stations}
    members: dict[int, list[int]] = {}
    for row in memberships:
        sid = int(row["station_id"])
        if sid in station_by_id and sid not in members.setdefault(int(row["line_id"]), []):
            members[int(row["line_id"])].append(sid)

    def sort_key(line):
        line_type = canonical_type(line["type"])
        rank = TYPE_ORDER.index(line_type) if line_type in TYPE_ORDER else len(TYPE_ORDER)
        code = str(line["code"])
        digits = "".join(ch for ch in code if ch.isdigit())
        return (rank, int(digits) if digits else 999, code)

    lines = []
    station_lines: dict[int, list[int]] = {}
    for line in sorted(raw_lines, key=sort_key):
        line_id = int(line["id"])
        station_ids = members.get(line_id, [])
        segments = parse_path_segments(line["path_json"])
        if not segments and len(station_ids) >= 2:
            segments = [[[float(station_by_id[sid]["x"]), float(station_by_id[sid]["y"])] for sid in station_ids]]
        if not segments:
            continue
        positions = [(float(station_by_id[sid]["x"]), float(station_by_id[sid]["y"])) for sid in station_ids]
        chains, stops = locate_stops(segments, positions)
        edges = line_edges(chains, stops) if len(stops) > 1 else []
        color = line_color(line["type"], line["color"])
        for sid in station_ids:
            station_lines.setdefault(sid, []).append(line_id)
        lines.append(
            {
                "id": line_id,
                "code": str(line["code"]),
                "name": line["name"] or f"{line['type']} {line['code']}",
                "type": canonical_type(line["type"]),
                "status": line.get("status") or "open",
                "color": color,
                "textColor": line["text_color"] or text_color(color),
                "segments": segments,
                "stations": station_ids,
                "edges": [[station_ids[a], station_ids[b], round(w, 1)] for a, b, w in edges],
            }
        )

    return {
        "canvas": {"width": PDF_WIDTH, "height": PDF_HEIGHT},
        "source": "paris_map.pdf (Île-de-France Mobilités, 2026-01)",
        "stations": [
            {
                "id": int(s["id"]),
                "name": s["name2"] or s["name"],
                "rawName": s["name"],
                "x": round(float(s["x"]), 2),
                "y": round(float(s["y"]), 2),
                "lines": station_lines.get(int(s["id"]), []),
            }
            for s in stations
            if int(s["id"]) in station_lines
        ],
        "lines": lines,
        "future": [
            route for route in load_future_routes()
            if route.get("name") not in {f"Métro {line['code']}" for line in lines if line["type"] == "METRO"}
        ],
        "stats": {
            "stationCount": sum(1 for s in stations if int(s["id"]) in station_lines),
            "lineCount": len(lines),
            "pathLineCount": sum(1 for line in lines if line["segments"]),
        },
    }


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/api/map":
            self.send_json(fetch_map_data())
            return

        path = "/index.html" if parsed.path == "/" else parsed.path
        candidate = (PUBLIC_DIR / path.lstrip("/")).resolve()
        if not str(candidate).startswith(str(PUBLIC_DIR.resolve())) or not candidate.is_file():
            self.send_error(404)
            return

        content_type = mimetypes.guess_type(candidate.name)[0] or "application/octet-stream"
        body = candidate.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_json(self, data: dict) -> None:
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt: str, *args) -> None:
        print(f"{self.address_string()} - {fmt % args}")


def main() -> int:
    port = int(os.environ.get("PORT", "8000"))
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"Paris map server running at http://127.0.0.1:{port}")
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
