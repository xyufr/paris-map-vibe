# AGENTS.md

## Project Overview

This project renders a Paris transit map from local PDF-derived coordinates.

- `server.py` serves `public/` and exposes `/api/map` (stations in use, PDF route segments, line adjacency `edges`, future lines).
- `network_graph.py` computes stop adjacency and station order from a line's `path_json` segments and station positions (shared by `server.py` and the pipeline).
- `public/static/app.js` renders the D3/SVG map, zooming, station search, labels, line filters, station/line panels, and the route planner.
- `public/static/styles.css` controls the app layout, themes (light/dark) and SVG styling.
- `src/worker.js` + `wrangler.jsonc` deploy `public/` to Cloudflare Workers; `/api/map` is served from `public/data/map.json`.
- `resources/pdf_network.py`, `pdf_labels.py`, `build_network.py`, `resolve_network.py`, `reconcile_network.py`, `apply_network.py` form the PDF → MySQL pipeline; `export_static.py` writes `public/data/map.json`.
- `resources/network_overrides.json` holds manual decisions verified on PDF crops; `resources/future_lines.json` holds dashed (under construction) routes.
- `resources/update_station_coords_from_pdf.py` is the older label-based coordinate extractor (kept for reference).
- `resources/coordinate_picker.py` is a local Mac coordinate picker for manually validating PDF coordinates.
- `resources/db/*.sql` are database dump files.

The app uses PDF coordinate space directly: `(0, 0)` is the top-left of the PDF page. Do not replace these with geographic longitude/latitude.

## Local Data Sources

Use the local MySQL database, not the internet, for station and line data.

Default database config:

```python
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "test001**",
    "database": "paris_map",
    "charset": "utf8mb4",
}
```

`server.py` also supports these environment overrides:

- `PARIS_MAP_DB_HOST`
- `PARIS_MAP_DB_USER`
- `PARIS_MAP_DB_PASSWORD`
- `PARIS_MAP_DB_NAME`

The PDF is the IDFM regional plan of January 2026 ("Region_GF_RATP_2026_01").

Primary PDF sources:

- `/Users/xyu/Desktop/paris_map.pdf`
- `resources/paris_map.pdf`

When coordinates are needed, derive or validate them from the PDF, not from web maps.

## Running The App

Start the local app with:

```sh
python3 server.py
```

Then open:

```text
http://127.0.0.1:8000/
```

If static JS/CSS changes do not appear, update the cache-busting query string in `public/index.html`.

Cloudflare deployment (no MySQL in production):

```sh
python3 resources/export_static.py
npx wrangler dev      # http://localhost:8787
npx wrangler deploy
```

## Database And Path Rules

Important tables:

- `stations`: station names and PDF coordinates in `x`, `y`.
- `line`: transit lines, colors, and optional `path_json`.
- `line_stations`: line membership and `station_order`.

Coordinate and path rules:

- `stations.x` and `stations.y` should be PDF dot centers.
- `line_stations.station_order` controls ordered station membership.
- `line.path_json` can override route geometry.
- `line.status` (nullable): `construction` marks lines drawn dashed on the PDF (Métro 15 sud, added by `resources/add_line15.py`; CDG Express `TRAIN`/`CDGX`, Gare de l'Est ↔ CDG 2, added by `resources/add_cdg_express.py`; RER E western extension `RER`/`E`, Nanterre La Folie ↔ Mantes-la-Jolie, added by `resources/add_rer_e_west.py`); the app draws them dashed, labels them "under construction" and excludes them from route planning.
- A single route path is `[[x, y], [x, y], ...]`.
- A branched or segmented route path is `[[[x, y], [x, y]], [[x, y], [x, y]], ...]`.
- Prefer segmented `path_json` for branched routes, loops, and RER/Train/Tram paths where simple ordering creates wrong direct links.
- Do not remove existing manually corrected coordinates unless the user explicitly asks.

Known examples:

- Metro `M7`, `M13`, `M7b`, and `M10` need branch/loop-aware paths.
- RER, Train, and Tram paths may be segmented to avoid cross-branch straight lines.
- Some station names have duplicates across line systems; if one duplicate has verified PDF coordinates, another duplicate can often reuse them only after name normalization confirms it is the same station on the PDF.

## PDF Network Pipeline

How the PDF encodes the network (verified):

- Routes are stroked paths: Metro width 3.5, Tram 4.37, RER/Transilien 7.0. A few curves are filled outline bands (converted to centerlines). Dashed strokes are lines under construction.
- One CMYK value is shared by a color family (M1 and RER C, M12 / RER D / T3b, ...); width and region disambiguate. `build_network.LINE_STYLES` maps styles to lines and `PALETTE` maps CMYK to IDFM RGB.
- Each line has its own stop ring (white fill, stroke in the line color; 4.4pt metro/tram, 7pt RER) even inside interchange capsules; termini are filled dots. Some interchanges only use black-rimmed circles/capsules, and grey hub areas (Gare du Nord, Magenta, Haussmann-Saint-Lazare) have no marker at all.
- Station labels use IDFVoyageur Regular/Bold at 10pt (Paris) or 11.6pt (suburbs); lines of one label have a fixed tight pitch (gap < 1.3pt).

Pipeline order: `pdf_network.py` → `pdf_labels.py` → `build_network.py` → `resolve_network.py` → `reconcile_network.py` (writes `resources/build/reconcile_report.txt`) → `apply_network.py --dry-run` → back up tables → `apply_network.py` → `export_static.py`. Put manual fixes in `network_overrides.json` (target stops by line + PDF label or point) rather than editing generated files.

`apply_network.py` inserts new stations/lines on every run, so re-running it on an already updated database needs care; small follow-up fixes are better done directly in MySQL (after reading the rows) and mirrored in `network_overrides.json`.

## PDF Coordinate Workflow

Use `resources/update_station_coords_from_pdf.py` for the older automated extraction and reference logic. It includes:

- French/accent-insensitive normalization.
- PDF text box extraction.
- Station dot extraction.
- line-color-aware match scoring.
- a small override list for labels that PDF text extraction cannot recover.

For manual verification on macOS:

```sh
python3 resources/coordinate_picker.py
```

The coordinate picker shows the PDF, displays mouse coordinates, supports zooming and dragging, and copies clicked coordinates to the clipboard.

When automatic extraction misses a station:

1. Render a local crop from the PDF around the station label.
2. Inspect nearby dot clusters.
3. Update `stations.x`, `stations.y` only when the dot is visually confirmed.
4. Re-check `/api/map`.

## Frontend Behavior

Search behavior in `public/static/app.js`:

- Search is accent-insensitive and handles French punctuation.
- Exact station search selects the station.
- Search also matches lines (`14`, `M14`, `RER A`, `T3a`).
- Selecting a station from search highlights only lines that contain that station and zooms smoothly to it (±90pt around the station); clicking a stop on the map keeps the view; "Zoom here" and station links in panels also zoom to the station. Reset / Home returns to the default map view.
- The selected station is marked in screen space (constant size at any zoom): two pulsing accent rings, a drop-in map pin and a navy name tag above it. Labels and line badges keep clear of that marker.

Route planner:

- Dijkstra over (station, line) nodes; ride cost from geometry length, transfer penalty, walking links between stations closer than 34pt or sharing a name token.
- Offers "fastest" and "fewer transfers" options, and a metro & tram only mode.
- The journey is drawn along the line geometry; URL state is `#route=<from>-<to>[-m]`.

Line filter behavior:

- Metro lines sort as `M1`, `M2`, ..., `M14`.
- RER, Train, Tram, Cable, and Navette groups are separated.
- Clicking one line filter selects only that line and fits the map to it; Ctrl/⌘/Shift-click combines lines.

Language:

- The UI is English by default. The header switcher (EN / FR / 中文) changes it in place and saves it in `localStorage` (`pm.lang`); `?lang=en|fr|zh` overrides. All UI strings live in the `I18N` table in `app.js` — add a key to all three languages together. Station names stay in French as on the PDF.

Offline:

- `public/sw.js` precaches the page shell, `/data/map.json` and fonts; pages and map data are network-first with the cached copy as offline fallback, `?v=` assets are cache-first. It registers only on https or localhost.
- If you add a new static file the page needs, add it to `PRECACHE` in `sw.js`; bump `CACHE_VERSION` for breaking changes.

Line badges:

- Each line shows its number badge beyond every terminus (except termini listed in `NO_END_BADGE`: CDG Express has no badge at Gare de l'Est, only at the airport); mid-line roundels appear when zoomed in or when the line is focused. Badges avoid each other and labels avoid badges.
- Termini of several lines at the same place share one row sorted by line (e.g. "9 15" at Pont de Sèvres, as on the PDF). A row is placed under/over/beside the station, avoiding drawn lines, and is never partly covered by a label; a single badge may be hidden by a station name when nothing else fits.

Label behavior:

- Labels live in a screen-space layer; placement is recomputed after zoom/pan with a grid-based collision check.
- As on the PDF, names never sit on a line: candidates are tried above, below, right, left, then diagonals (plus a second ring 12px farther out), and any box crossing a drawn route segment (screen-space segment index, `lineCrossings`) is rejected. Horizontal lines therefore get names above/below, vertical lines beside. Only must-show labels (selected, hovered, journey ends) may fall back to a crossing spot.
- A station name may cover a line-number badge when no other spot is free; that badge is then hidden.
- Priority: selected/hovered station, journey or focused-line stations, then stations by number of lines.
- Do not add one-off station-name placement hacks unless the user explicitly asks. Prefer general collision rules.

Layout behavior:

- The map is initially aligned to the useful PDF map area rather than the full PDF page.
- Zoom and pan are constrained (`constrainZoom` in `app.js`, recomputed with the default view on load/resize): the view cannot move more than 150pt past the map content, and zoom-out stops at 85% of the full-map scale. The extent always includes the default view, so Reset / Home and the phone bottom-sheet layout stay valid.
- After a user drag or wheel zoom ends (`settleView`), the view settles: at or near the full-map scale (≤105% of default) it animates back to the whole-map view; when zoomed in it springs back so no empty area shows past the map content (`MAP_CONTENT`). Plain clicks do not trigger it.
- Keep the sidebar compact so the map begins close to the line list.

## Verification Checklist

After database or rendering changes, verify:

```sh
curl -s http://127.0.0.1:8000/api/map
```

Useful checks:

- `stats.stationCount` and `stats.pathLineCount` are reasonable.
- No target line has missing coordinates unless the PDF cannot confirm them.
- `station_order` is filled for edited lines.
- `path_json` is segmented for branched paths.
- Every line's `edges` form one connected component (metro and tram lines have no cycles except the M10 Auteuil loop).
- `public/data/map.json` was re-exported after database changes.
- No obviously long wrong connection remains in target lines.

For frontend changes:

- Refresh `http://127.0.0.1:8000/?v=<new-version>`.
- Verify search suggestions.
- Verify exact station search selection.
- Verify line filters.
- Verify zoom reset behavior after station search.
- Verify labels at normal and zoomed views.

## Coding Guidelines

- Keep changes scoped to the requested behavior.
- Do not reformat vendored `public/vendor/d3.min.js`.
- Use existing plain JavaScript and D3 patterns; this project has no bundler.
- Prefer small helper functions in `app.js` over broad rewrites.
- Preserve ASCII in new code unless station names or existing data require French characters.
- Update `public/index.html` cache-busting query strings whenever changing `public/static/app.js` or `public/static/styles.css`.

## Safety Notes

- The database is the working source of truth during development; SQL dumps may lag behind manual DB updates.
- Do not run destructive MySQL updates without first reading the current rows.
- Do not reset user changes in the working tree.
- Do not fetch live transit data or web coordinates for station placement.
