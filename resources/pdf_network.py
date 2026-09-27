#!/usr/bin/env python3
"""Extract raw transit geometry from paris_map.pdf.

Produces route polylines (grouped by stroke color and width), station marker
candidates and text words, all in PDF top-left coordinate space. The output is
consumed by `resources/audit_network.py` and `resources/build_static_data.py`.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import pdfplumber


ROOT = Path(__file__).resolve().parent
DEFAULT_PDF = ROOT / "paris_map.pdf"
DEFAULT_OUT = ROOT / "build" / "pdf_raw.json"

MAP_MIN_X = 538.0
ROUTE_WIDTHS = {3.06, 3.5, 4.37, 7.0}


def rounded_color(color) -> list[float] | None:
    if not isinstance(color, (tuple, list)) or len(color) != 4:
        return None
    return [round(float(v), 3) for v in color]


def color_key(color) -> str | None:
    value = rounded_color(color)
    return None if value is None else ",".join(f"{v:g}" for v in value)


def is_neutral(color: list[float] | None) -> bool:
    if color is None:
        return True
    c, m, y, k = color
    return max(c, m, y) < 0.05


def cubic(p0, p1, p2, p3, steps: int) -> list[tuple[float, float]]:
    out = []
    for i in range(1, steps + 1):
        t = i / steps
        u = 1 - t
        x = u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0]
        y = u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1]
        out.append((x, y))
    return out


def flatten_path(path) -> list[list[tuple[float, float]]]:
    """Turn pdfplumber path commands into polylines, flattening Beziers."""
    subpaths: list[list[tuple[float, float]]] = []
    current: list[tuple[float, float]] = []
    for command in path or []:
        op = command[0]
        if op == "m":
            if len(current) > 1:
                subpaths.append(current)
            current = [tuple(command[1])]
        elif op == "l" and current:
            current.append(tuple(command[1]))
        elif op == "c" and current:
            p0 = current[-1]
            p1, p2, p3 = (tuple(v) for v in command[1:4])
            length = math.dist(p0, p1) + math.dist(p1, p2) + math.dist(p2, p3)
            current.extend(cubic(p0, p1, p2, p3, max(4, min(40, int(length / 1.2)))))
        elif op == "h" and current:
            current.append(current[0])
    if len(current) > 1:
        subpaths.append(current)
    return subpaths


def resample_by_length(points, count):
    lengths = [0.0]
    for a, b in zip(points, points[1:]):
        lengths.append(lengths[-1] + math.dist(a, b))
    total = lengths[-1]
    if total == 0:
        return [points[0]] * count
    out = []
    j = 0
    for i in range(count):
        target = total * i / (count - 1)
        while j < len(lengths) - 2 and lengths[j + 1] < target:
            j += 1
        seg = lengths[j + 1] - lengths[j]
        t = 0 if seg == 0 else (target - lengths[j]) / seg
        a, b = points[j], points[j + 1]
        out.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
    return out


def band_centerline(path) -> tuple[list[tuple[float, float]], float] | None:
    """Centerline of a filled band polygon (an outlined stroke).

    The outline is edge A, a short straight cap, edge B (reversed) and a second
    cap. Returns (centerline, band width) or None when it is not a band.
    """
    commands = [c for c in (path or []) if c[0] != "h"]
    if len(commands) < 4 or commands[0][0] != "m" or any(c[0] == "m" for c in commands[1:]):
        return None
    verts = [tuple(commands[0][1])] + [tuple(c[-1]) for c in commands[1:]]
    if math.dist(verts[0], verts[-1]) < 0.05:
        verts = verts[:-1]
        commands = commands[:-1]
    n = len(verts)
    if n < 4:
        return None

    def segment(k):
        """Command drawing segment k (verts[k] -> verts[k+1]); None = straight."""
        return commands[k + 1] if k + 1 < n else None

    caps = []
    for k in range(n):
        cmd = segment(k)
        if cmd is not None and cmd[0] != "l":
            continue
        length = math.dist(verts[k], verts[(k + 1) % n])
        if 2.5 <= length <= 8.0:
            caps.append((length, k))
    best = None
    for x in range(len(caps)):
        for y in range(x + 1, len(caps)):
            (la, ka), (lb, kb) = caps[x], caps[y]
            if abs(la - lb) > 0.6:
                continue
            balance = min((kb - ka) % n, (ka - kb) % n)
            if best is None or balance > best[0]:
                best = (balance, ka, kb, (la + lb) / 2)
    if best is None or best[0] < 1:
        return None
    _, ka, kb, width = best

    def walk(start, end):
        seq = [verts[start]]
        k = start
        while k != end:
            cmd = segment(k)
            if cmd is not None and cmd[0] == "c":
                seq.extend(cubic(seq[-1], tuple(cmd[1]), tuple(cmd[2]), tuple(cmd[3]), 16))
            else:
                seq.append(verts[(k + 1) % n])
            k = (k + 1) % n
        return seq

    edge_a = walk((ka + 1) % n, kb)
    edge_b = walk((kb + 1) % n, ka)[::-1]
    if len(edge_a) < 2 or len(edge_b) < 2:
        return None
    count = max(len(edge_a), len(edge_b), 8) * 2
    ra = resample_by_length(edge_a, count)
    rb = resample_by_length(edge_b, count)
    if math.dist(ra[0], rb[0]) > width * 1.6 or math.dist(ra[-1], rb[-1]) > width * 1.6:
        return None
    center = [((p[0] + q[0]) / 2, (p[1] + q[1]) / 2) for p, q in zip(ra, rb)]
    if polyline_length(center) < 6:
        return None
    return center, width


def polyline_length(points):
    return sum(math.dist(a, b) for a, b in zip(points, points[1:]))


def snap_width(width: float) -> float | None:
    for target in sorted(ROUTE_WIDTHS):
        if abs(width - target) <= 0.45:
            return target
    return None


def extract(pdf_path: Path) -> dict:
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[0]
        routes = []
        markers = []
        for kind in ("curves", "lines", "rects"):
            for obj in getattr(page, kind):
                if obj["x1"] < MAP_MIN_X:
                    continue
                stroke = rounded_color(obj.get("stroking_color"))
                fill = rounded_color(obj.get("non_stroking_color"))
                width = round(float(obj.get("linewidth") or 0), 2)
                w = obj["x1"] - obj["x0"]
                h = obj["bottom"] - obj["top"]
                if obj.get("stroke") and width in ROUTE_WIDTHS and not is_neutral(stroke) and stroke[3] < 0.3:
                    dash = obj.get("dash")
                    dashed = bool(dash and dash[0] and any(v for v in dash[0]))
                    for poly in flatten_path(obj.get("path")):
                        routes.append(
                            {
                                "color": color_key(obj.get("stroking_color")),
                                "width": width,
                                "dashed": dashed,
                                "points": [[round(x, 2), round(y, 2)] for x, y in poly],
                            }
                        )
                fill_color = rounded_color(obj.get("non_stroking_color"))
                if (
                    obj.get("fill")
                    and not obj.get("stroke")
                    and not is_neutral(fill_color)
                    and fill_color[3] < 0.3
                    and max(w, h) > 30
                ):
                    band = band_centerline(obj.get("path"))
                    if band:
                        center, band_width = band
                        snapped = snap_width(band_width)
                        if snapped:
                            routes.append(
                                {
                                    "color": color_key(obj.get("non_stroking_color")),
                                    "width": snapped,
                                    "dashed": False,
                                    "band": True,
                                    "points": [[round(x, 2), round(y, 2)] for x, y in center],
                                }
                            )
                            continue
                if obj.get("fill") and 2.5 <= w <= 40 and 2.5 <= h <= 40:
                    markers.append(
                        {
                            "x": round((obj["x0"] + obj["x1"]) / 2, 3),
                            "y": round((obj["top"] + obj["bottom"]) / 2, 3),
                            "w": round(w, 2),
                            "h": round(h, 2),
                            "fill": color_key(obj.get("non_stroking_color")),
                            "stroke": color_key(obj.get("stroking_color")) if obj.get("stroke") else None,
                            "lw": width if obj.get("stroke") else 0,
                            "path": [
                                [c[0]] + [[round(v[0], 2), round(v[1], 2)] for v in c[1:]]
                                for c in (obj.get("path") or [])
                            ] if w > 9 or h > 9 else None,
                        }
                    )
                elif obj.get("stroke") and 2.5 <= w <= 40 and 2.5 <= h <= 40 and not obj.get("fill"):
                    markers.append(
                        {
                            "x": round((obj["x0"] + obj["x1"]) / 2, 3),
                            "y": round((obj["top"] + obj["bottom"]) / 2, 3),
                            "w": round(w, 2),
                            "h": round(h, 2),
                            "fill": None,
                            "stroke": color_key(obj.get("stroking_color")),
                            "lw": width,
                            "path": None,
                        }
                    )

        words = [
            {
                "text": w["text"],
                "x0": round(w["x0"], 2),
                "x1": round(w["x1"], 2),
                "top": round(w["top"], 2),
                "bottom": round(w["bottom"], 2),
                "size": round(float(w.get("size") or (w["bottom"] - w["top"])), 2),
                "font": w.get("fontname"),
            }
            for w in page.extract_words(
                x_tolerance=1.5,
                y_tolerance=2,
                keep_blank_chars=False,
                use_text_flow=False,
                extra_attrs=["fontname", "size"],
            )
            if w["x0"] >= MAP_MIN_X
        ]
        return {
            "page": {"width": float(page.width), "height": float(page.height)},
            "routes": routes,
            "markers": markers,
            "words": words,
        }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", default=str(DEFAULT_PDF))
    parser.add_argument("--out", default=str(DEFAULT_OUT))
    args = parser.parse_args()
    data = extract(Path(args.pdf))
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, ensure_ascii=False))
    print(f"routes={len(data['routes'])} markers={len(data['markers'])} words={len(data['words'])} -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
