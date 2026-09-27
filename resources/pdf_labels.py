#!/usr/bin/env python3
"""Extract station label blocks from paris_map.pdf.

Station names on this map use the IDFVoyageur font at 10pt (Paris) or 11.6pt
(suburbs), in black, or white inside the dark frame. Bus numbers, place names
and legends use other fonts or colors, so filtering on font/size/color keeps
only station labels. Words are grouped into text lines, and vertically stacked
aligned lines are grouped into multi-line label blocks.

Output: resources/build/pdf_labels.json
"""

from __future__ import annotations

import json
from pathlib import Path

import pdfplumber


ROOT = Path(__file__).resolve().parent
PDF_PATH = ROOT / "paris_map.pdf"
OUT_PATH = ROOT / "build" / "pdf_labels.json"
MAP_MIN_X = 538.0

LABEL_SIZES = (10.0, 11.6)
LABEL_COLORS = ((0.0, 0.0, 0.0, 1.0), (0.0, 0.0, 0.0, 0.0))


def is_label_char(obj) -> bool:
    if obj.get("object_type") != "char":
        return False
    if "IDFVoyageur" not in (obj.get("fontname") or ""):
        return False
    if not any(abs(obj["size"] - size) < 0.15 for size in LABEL_SIZES):
        return False
    color = obj.get("non_stroking_color")
    if not isinstance(color, (tuple, list)) or len(color) != 4:
        return False
    return any(max(abs(a - b) for a, b in zip(color, ref)) < 0.02 for ref in LABEL_COLORS) and obj["x0"] >= MAP_MIN_X


def text_lines(page) -> list[dict]:
    filtered = page.filter(is_label_char)
    words = filtered.extract_words(
        x_tolerance=1.2,
        y_tolerance=1.5,
        keep_blank_chars=False,
        use_text_flow=True,
        extra_attrs=["fontname", "size", "non_stroking_color"],
    )
    words.sort(key=lambda w: (round(w["bottom"], 0), w["x0"]))
    lines: list[dict] = []
    for w in words:
        size = w["size"]
        bold = "Bold" in w["fontname"]
        white = w["non_stroking_color"][3] < 0.5
        for line in lines:
            if (
                abs(line["bottom"] - w["bottom"]) < 1.2
                and abs(line["size"] - size) < 0.2
                and line["bold"] == bold
                and line["white"] == white
                and 0 <= w["x0"] - line["x1"] < size * 0.3
            ):
                line["text"] += " " + w["text"]
                line["x1"] = w["x1"]
                line["top"] = min(line["top"], w["top"])
                break
        else:
            lines.append(
                {
                    "text": w["text"],
                    "x0": w["x0"],
                    "x1": w["x1"],
                    "top": w["top"],
                    "bottom": w["bottom"],
                    "size": size,
                    "bold": bold,
                    "white": white,
                }
            )
    return lines


def aligned(a: dict, b: dict) -> bool:
    tol = 2.5
    if abs(a["x0"] - b["x0"]) <= tol or abs(a["x1"] - b["x1"]) <= tol:
        return True
    if abs((a["x0"] + a["x1"]) / 2 - (b["x0"] + b["x1"]) / 2) <= tol:
        return True
    return False


def join_lines(parts: list[str]) -> str:
    text = ""
    for part in parts:
        if not text:
            text = part
        elif text.endswith("-") or part.startswith("-"):
            text += part
        else:
            text += " " + part
    return text


def blocks_from_lines(lines: list[dict]) -> list[dict]:
    lines = sorted(lines, key=lambda l: (l["top"], l["x0"]))
    used = [False] * len(lines)
    blocks = []
    for i, line in enumerate(lines):
        if used[i]:
            continue
        used[i] = True
        members = [line]
        current = line
        while True:
            candidates = []
            for j, other in enumerate(lines):
                if used[j]:
                    continue
                gap = other["top"] - current["bottom"]
                # Lines of one label use a fixed tight pitch; separate labels
                # stacked vertically are at least ~3pt apart.
                if gap < -1.0 or gap > 1.3:
                    continue
                if abs(other["size"] - current["size"]) > 0.2 or other["white"] != current["white"]:
                    continue
                if other["bold"] != current["bold"]:
                    continue
                overlap = min(current["x1"], other["x1"]) - max(current["x0"], other["x0"])
                if overlap <= 0 and not aligned(current, other):
                    continue
                candidates.append((gap, abs(other["x0"] - current["x0"]), j))
            if not candidates:
                break
            _, _, j = min(candidates)
            used[j] = True
            current = lines[j]
            members.append(current)
        blocks.append(
            {
                "text": join_lines([m["text"] for m in members]),
                "lines": [m["text"] for m in members],
                "x0": round(min(m["x0"] for m in members), 2),
                "x1": round(max(m["x1"] for m in members), 2),
                "top": round(min(m["top"] for m in members), 2),
                "bottom": round(max(m["bottom"] for m in members), 2),
                "size": members[0]["size"],
                "bold": members[0]["bold"],
                "white": members[0]["white"],
            }
        )
    return blocks


def main() -> int:
    with pdfplumber.open(PDF_PATH) as pdf:
        lines = text_lines(pdf.pages[0])
    blocks = blocks_from_lines(lines)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps({"lines": lines, "blocks": blocks}, ensure_ascii=False, indent=1))
    print(f"lines={len(lines)} blocks={len(blocks)} -> {OUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
