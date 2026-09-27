#!/usr/bin/env python3
"""Export the /api/map payload to public/data/map.json.

The Cloudflare Worker deployment has no MySQL; it serves this file (see
src/worker.js). Run after any database change:

    python3 resources/export_static.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from server import fetch_map_data  # noqa: E402


OUT = ROOT / "public" / "data" / "map.json"


def main() -> int:
    data = fetch_map_data()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")))
    print(f"{OUT.relative_to(ROOT)}: {OUT.stat().st_size / 1024:.0f} KB, "
          f"{data['stats']['stationCount']} stations, {data['stats']['lineCount']} lines")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
