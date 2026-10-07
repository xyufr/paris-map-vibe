(() => {
  "use strict";

  // ---------------------------------------------------------------------------
  // i18n
  // ---------------------------------------------------------------------------

  const I18N = {
    en: {
      title: "Paris Transit",
      pageTitle: "Paris Transit Map · Métro, RER, Tram & Transilien",
      pageDescription: "Interactive Île-de-France transit map drawn from the official IDFM plan: Métro, RER, Transilien, tram and cable lines, 997 stations, accent-insensitive station search, journey planning and offline use, in English, French and Chinese.",
      titleAccent: "en transports",
      interchanges: "interchanges",
      subtitle: "Île-de-France · PDF plan 2026",
      tabExplore: "Explore",
      tabRoute: "Route",
      tabLines: "Lines",
      searchPlaceholder: "Search a station or line  ( / )",
      from: "From",
      to: "To",
      swap: "Swap",
      metroOnly: "Metro & tram only (no RER / train)",
      linesHint: "Click to focus a line · Ctrl/⌘-click to combine",
      showAll: "Show all",
      showFuture: "Show lines under construction (dashed)",
      zoomIn: "Zoom in",
      zoomOut: "Zoom out",
      resetView: "Reset view",
      share: "Copy link",
      theme: "Theme",
      loading: "Loading…",
      loadError: "Could not load map data",
      stations: "stations",
      lines: "lines",
      emptyTitle: "Explore the network",
      emptyBody: "Search a station, click a stop or a line on the map, or plan a route.",
      shortcuts: "Shortcuts",
      linesAtStation: "Lines",
      nextStops: "Next stops",
      nearby: "Nearby connections",
      routeFrom: "Route from here",
      routeTo: "Route to here",
      zoomHere: "Zoom here",
      stationsOnLine: "Stations",
      branches: "branches",
      fitLine: "Fit line",
      routeEmpty: "Choose a departure and a destination.",
      routeNone: "No route found with these options.",
      minutes: "min",
      estimate: "estimate",
      transfers: "transfers",
      transfer: "transfer",
      stops: "stops",
      stop: "stop",
      direction: "towards",
      walk: "Walk to",
      board: "Board at",
      fastest: "Fastest",
      fewerTransfers: "Fewer transfers",
      arrive: "Arrive",
      linkCopied: "Link copied",
      clear: "Clear",
      construction: "under construction",
      resetAll: "Reset map",
      offline: "Offline · saved data",
      groups: { METRO: "Metro", RER: "RER", TRAIN: "Transilien", TRAM: "Tram", CABLE: "Cable car", NAVETTE: "Shuttles" },
    },
    zh: {
      title: "巴黎公共交通",
      pageTitle: "巴黎公共交通地图 · 地铁、RER、有轨电车与 Transilien",
      pageDescription: "根据 IDFM 官方线路图绘制的法兰西岛公共交通互动地图：地铁、RER、Transilien、有轨电车与缆车线路，997 个车站，支持不区分重音的车站搜索、路线规划和离线使用，提供英文、法文和中文界面。",
      titleAccent: "公共交通",
      interchanges: "换乘站",
      subtitle: "法兰西岛 · 2026 年 PDF 线路图",
      tabExplore: "浏览",
      tabRoute: "路线",
      tabLines: "线路",
      searchPlaceholder: "搜索车站或线路（/）",
      from: "出发站",
      to: "到达站",
      swap: "交换",
      metroOnly: "仅地铁和有轨电车（不乘 RER / 火车）",
      linesHint: "点击聚焦线路 · Ctrl/⌘ 点击可多选",
      showAll: "全部显示",
      showFuture: "显示在建线路（虚线）",
      zoomIn: "放大",
      zoomOut: "缩小",
      resetView: "重置视图",
      share: "复制链接",
      theme: "主题",
      loading: "加载中…",
      loadError: "无法加载地图数据",
      stations: "个车站",
      lines: "条线路",
      emptyTitle: "探索路网",
      emptyBody: "搜索车站，点击地图上的车站或线路，或规划一条路线。",
      shortcuts: "快捷键",
      linesAtStation: "经过线路",
      nextStops: "相邻车站",
      nearby: "步行换乘",
      routeFrom: "从这里出发",
      routeTo: "到这里",
      zoomHere: "放大到这里",
      stationsOnLine: "车站列表",
      branches: "条支线",
      fitLine: "显示整条线",
      routeEmpty: "请选择出发站和到达站。",
      routeNone: "在当前条件下找不到路线。",
      minutes: "分钟",
      estimate: "估算",
      transfers: "次换乘",
      transfer: "次换乘",
      stops: "站",
      stop: "站",
      direction: "开往",
      walk: "步行至",
      board: "上车",
      fastest: "最快",
      fewerTransfers: "少换乘",
      arrive: "到达",
      linkCopied: "链接已复制",
      clear: "清除",
      construction: "在建",
      resetAll: "重置地图",
      offline: "离线 · 使用已缓存数据",
      groups: { METRO: "地铁", RER: "RER", TRAIN: "Transilien 火车", TRAM: "有轨电车", CABLE: "缆车", NAVETTE: "机场接驳" },
    },
    fr: {
      title: "Plan des transports",
      pageTitle: "Plan des transports de Paris · Métro, RER, Tram et Transilien",
      pageDescription: "Plan interactif des transports d’Île-de-France tracé d’après le plan officiel IDFM : Métro, RER, Transilien, tramway et câble, 997 stations, recherche de station sans accents, calcul d’itinéraire et usage hors ligne, en anglais, français et chinois.",
      titleAccent: "en transports",
      interchanges: "correspondances",
      subtitle: "Île-de-France · plan PDF 2026",
      tabExplore: "Explorer",
      tabRoute: "Itinéraire",
      tabLines: "Lignes",
      searchPlaceholder: "Rechercher une gare ou une ligne  ( / )",
      from: "Départ",
      to: "Arrivée",
      swap: "Inverser",
      metroOnly: "Métro et tram uniquement (sans RER / train)",
      linesHint: "Cliquez pour isoler une ligne · Ctrl/⌘-clic pour combiner",
      showAll: "Tout afficher",
      showFuture: "Afficher les lignes en travaux (pointillés)",
      zoomIn: "Zoomer",
      zoomOut: "Dézoomer",
      resetView: "Vue initiale",
      share: "Copier le lien",
      theme: "Thème",
      loading: "Chargement…",
      loadError: "Impossible de charger le plan",
      stations: "gares",
      lines: "lignes",
      emptyTitle: "Explorer le réseau",
      emptyBody: "Recherchez une gare, cliquez sur un arrêt ou une ligne, ou calculez un itinéraire.",
      shortcuts: "Raccourcis",
      linesAtStation: "Lignes",
      nextStops: "Arrêts voisins",
      nearby: "Correspondances à pied",
      routeFrom: "Partir d’ici",
      routeTo: "Aller ici",
      zoomHere: "Zoomer ici",
      stationsOnLine: "Arrêts",
      branches: "branches",
      fitLine: "Voir la ligne",
      routeEmpty: "Choisissez un départ et une arrivée.",
      routeNone: "Aucun itinéraire avec ces options.",
      minutes: "min",
      estimate: "estimation",
      transfers: "correspondances",
      transfer: "correspondance",
      stops: "arrêts",
      stop: "arrêt",
      direction: "direction",
      walk: "Marcher jusqu’à",
      board: "Monter à",
      fastest: "Le plus rapide",
      fewerTransfers: "Moins de correspondances",
      arrive: "Arrivée",
      linkCopied: "Lien copié",
      clear: "Effacer",
      construction: "en travaux",
      resetAll: "Réinitialiser le plan",
      offline: "Hors ligne · données enregistrées",
      groups: { METRO: "Métro", RER: "RER", TRAIN: "Transilien", TRAM: "Tramway", CABLE: "Câble", NAVETTE: "Navettes" },
    },
  };

  // English by default; ?lang=en|fr|zh or the saved choice overrides it.
  let LANG = (() => {
    let saved = null;
    try { saved = localStorage.getItem("pm.lang"); } catch (_) { /* ignore */ }
    const wanted = (new URLSearchParams(location.search).get("lang") || saved || "en").slice(0, 2).toLowerCase();
    return I18N[wanted] ? wanted : "en";
  })();
  let T = I18N[LANG];

  function applyI18n() {
    document.documentElement.lang = LANG === "zh" ? "zh-CN" : LANG;
    // Title, description and canonical URL follow the language (each has its own ?lang= entry in sitemap.xml).
    document.title = T.pageTitle;
    document.querySelector('meta[name="description"]').content = T.pageDescription;
    document.querySelector('link[rel="canonical"]').href = LANG === "en" ? "https://map.xyufr.com/" : `https://map.xyufr.com/?lang=${LANG}`;
    document.querySelectorAll(".lang-switch [data-lang]").forEach((button) => {
      const active = button.dataset.lang === LANG;
      button.classList.toggle("is-active", active);
      button.setAttribute("aria-pressed", active ? "true" : "false");
    });
    document.querySelectorAll("[data-i18n]").forEach((el) => { el.textContent = T[el.dataset.i18n] ?? el.textContent; });
    document.querySelectorAll("[data-i18n-placeholder]").forEach((el) => { el.placeholder = T[el.dataset.i18nPlaceholder] ?? el.placeholder; });
    document.querySelectorAll("[data-i18n-title]").forEach((el) => {
      el.title = T[el.dataset.i18nTitle] ?? el.title;
      el.setAttribute("aria-label", el.title);
    });
  }

  // ---------------------------------------------------------------------------
  // constants & state
  // ---------------------------------------------------------------------------

  const TYPE_ORDER = ["METRO", "RER", "TRAIN", "TRAM", "CABLE", "NAVETTE"];
  const STROKE = { METRO: 3.5, RER: 7, TRAIN: 7, TRAM: 4.4, CABLE: 3, NAVETTE: 3.2 };
  const MIN_SCREEN_STROKE = { METRO: 2.2, RER: 3.4, TRAIN: 3, TRAM: 2, CABLE: 1.6, NAVETTE: 1.6 };
  const WALK_RADIUS = 34;
  const WALK_NAME_RADIUS = 90;
  const LABEL_FONT = 12;
  const MEASURE = document.createElement("canvas").getContext("2d");

  const state = {
    data: null,
    stationById: new Map(),
    lineById: new Map(),
    selectedStationId: null,
    focusLineIds: new Set(),
    hoverStationId: null,
    hoverLineId: null,
    journey: null,
    journeyOptions: [],
    journeyIndex: 0,
    routeFrom: null,
    routeTo: null,
    transform: d3.zoomIdentity,
    defaultTransform: d3.zoomIdentity,
    labelBoxes: [],
  };

  // ---------------------------------------------------------------------------
  // DOM & layers
  // ---------------------------------------------------------------------------

  const $ = (sel) => document.querySelector(sel);
  const svg = d3.select("#metroMap");
  const viewport = svg.append("g").attr("class", "viewport");
  const landLayer = viewport.append("g");
  const futureLayer = viewport.append("g").attr("class", "future");
  const casingLayer = viewport.append("g").attr("class", "casings");
  const routeLayer = viewport.append("g").attr("class", "routes");
  const transferLayer = viewport.append("g").attr("class", "transfers");
  const journeyLayer = viewport.append("g").attr("class", "journey");
  // Line hit areas sit under the stations, so a stop shows its own name on hover.
  const hitLayer = viewport.append("g").attr("class", "route-hits");
  const stationLayer = viewport.append("g").attr("class", "stations");
  const overlayLayer = viewport.append("g").attr("class", "overlay");
  const badgeLayer = svg.append("g").attr("class", "line-badges");
  const labelLayer = svg.append("g").attr("class", "labels");
  const focusLayer = svg.append("g").attr("class", "focus-layer");

  const tooltip = $("#tooltip");
  const statusChip = $("#status");
  const details = $("#details");
  const routeResult = $("#routeResult");
  const lineFilters = $("#lineFilters");

  // ---------------------------------------------------------------------------
  // helpers
  // ---------------------------------------------------------------------------

  function escapeHtml(value) {
    return String(value ?? "").replace(/[&<>"']/g, (ch) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[ch]));
  }

  function normalizeText(value) {
    return String(value || "")
      .replace(/[œŒ]/g, "oe")
      .replace(/[æÆ]/g, "ae")
      .normalize("NFD")
      .replace(/\p{Diacritic}/gu, "")
      .toLowerCase()
      .replace(/[’'`´]/g, " ")
      .replace(/[^a-z0-9]+/g, " ")
      .trim()
      .split(" ")
      .map((w) => ({ st: "saint", ste: "sainte", pte: "porte", av: "avenue" }[w] || w))
      .join(" ");
  }

  // Termini that get no line badge (station ids), as on the PDF: CDG Express
  // is only named at the airport, not at Gare de l'Est.
  const NO_END_BADGE = { CDGX: [860] };

  function hasEndBadge(line, p) {
    return !(NO_END_BADGE[line.code] || []).some((id) => {
      const s = state.stationById.get(id);
      return s && dist([s.x, s.y], p) < 30;
    });
  }

  function lineShortLabel(line) {
    if (line.type === "METRO") return line.code;
    if (line.type === "TRAM") return `T${line.code}`;
    if (line.type === "NAVETTE") return line.code === "ORL" ? "ORY" : line.code;
    if (line.code === "CDGX") return "CDG Express";
    return line.code;
  }

  function lineLongLabel(line) {
    const names = {
      METRO: `Métro ${line.code}`,
      RER: `RER ${line.code}`,
      TRAIN: line.code === "CDGX" ? "CDG Express" : `Transilien ${line.code}`,
      TRAM: `Tram T${line.code}`,
      CABLE: `Câble ${line.code}`,
      NAVETTE: line.code === "CDG" ? "CDGVAL" : line.code === "ORL" ? "Orlyval" : line.name,
    };
    const name = names[line.type] || line.name;
    return line.status === "construction" ? `${name} (${T.construction})` : name;
  }

  function badgeHtml(line, { large = false, button = false } = {}) {
    const cls = `badge ${line.type.toLowerCase()}${large ? " large" : ""}`;
    const style = `background:${line.color};color:${line.textColor}`;
    const label = escapeHtml(lineShortLabel(line));
    const title = escapeHtml(lineLongLabel(line));
    return button
      ? `<button type="button" class="${cls}" style="${style}" data-line="${line.id}" title="${title}">${label}</button>`
      : `<span class="${cls}" style="${style}" title="${title}">${label}</span>`;
  }

  function compareLines(a, b) {
    const ta = TYPE_ORDER.indexOf(a.type);
    const tb = TYPE_ORDER.indexOf(b.type);
    if (ta !== tb) return ta - tb;
    const na = parseInt(a.code, 10);
    const nb = parseInt(b.code, 10);
    if (!Number.isNaN(na) && !Number.isNaN(nb) && na !== nb) return na - nb;
    return String(a.code).localeCompare(String(b.code));
  }

  function stationLines(station) {
    return station.lines.map((id) => state.lineById.get(id)).filter(Boolean).sort(compareLines);
  }

  function dist(a, b) {
    return Math.hypot(a[0] - b[0], a[1] - b[1]);
  }

  function projectOnPolyline(point, points) {
    let best = { d: Infinity, p: points[0], along: 0 };
    let walked = 0;
    for (let i = 0; i < points.length - 1; i += 1) {
      const a = points[i];
      const b = points[i + 1];
      const dx = b[0] - a[0];
      const dy = b[1] - a[1];
      const len2 = dx * dx + dy * dy;
      let t = len2 ? ((point[0] - a[0]) * dx + (point[1] - a[1]) * dy) / len2 : 0;
      t = Math.max(0, Math.min(1, t));
      const p = [a[0] + t * dx, a[1] + t * dy];
      const d = dist(point, p);
      const seg = Math.sqrt(len2);
      if (d < best.d) best = { d, p, along: walked + t * seg };
      walked += seg;
    }
    return best;
  }

  function slicePolyline(points, from, to) {
    const reverse = from > to;
    const lo = Math.min(from, to);
    const hi = Math.max(from, to);
    const out = [];
    let walked = 0;
    for (let i = 0; i < points.length - 1; i += 1) {
      const a = points[i];
      const b = points[i + 1];
      const seg = dist(a, b);
      const start = walked;
      const end = walked + seg;
      if (end >= lo && start <= hi) {
        const t0 = seg ? Math.max(0, (lo - start) / seg) : 0;
        const t1 = seg ? Math.min(1, (hi - start) / seg) : 1;
        const p0 = [a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0];
        const p1 = [a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1];
        if (!out.length) out.push(p0);
        out.push(p1);
      }
      walked = end;
    }
    return reverse ? out.reverse() : out;
  }

  const pathOf = d3.line().curve(d3.curveLinear);

  function toast(message) {
    const el = $("#toast");
    el.textContent = message;
    el.hidden = false;
    clearTimeout(toast.timer);
    toast.timer = setTimeout(() => { el.hidden = true; }, 1600);
  }

  // ---------------------------------------------------------------------------
  // data preparation
  // ---------------------------------------------------------------------------

  function prepare(data) {
    state.data = data;
    data.lines.forEach((line) => {
      line.stationSet = new Set(line.stations);
      line.bbox = boundsOf(line.segments.flat());
      line.adjacency = new Map(line.stations.map((id) => [id, []]));
      line.edges.forEach(([a, b, w]) => {
        line.adjacency.get(a)?.push({ id: b, w });
        line.adjacency.get(b)?.push({ id: a, w });
      });
      state.lineById.set(line.id, line);
    });
    data.stations.forEach((station) => {
      station.norm = normalizeText(`${station.name} ${station.rawName || ""}`);
      station.nameNorm = normalizeText(station.name);
      station.onLine = new Map();
      state.stationById.set(station.id, station);
    });

    data.lines.forEach((line) => { line.anchors = lineAnchors(line); });

    // Where each station sits on each of its lines (the ring on the PDF).
    data.lines.forEach((line) => {
      line.stations.forEach((id) => {
        const station = state.stationById.get(id);
        if (!station) return;
        let best = null;
        line.segments.forEach((segment, chain) => {
          const hit = projectOnPolyline([station.x, station.y], segment);
          if (!best || hit.d < best.d) best = { ...hit, chain };
        });
        station.onLine.set(line.id, best && best.d < 30 ? best : { d: 0, p: [station.x, station.y], along: 0, chain: -1 });
      });
    });

    // Marker shape: a capsule spanning the per-line points, like the PDF.
    data.stations.forEach((station) => {
      const pts = [...station.onLine.values()].map((v) => v.p);
      let a = [station.x, station.y];
      let b = a;
      let best = 0;
      for (let i = 0; i < pts.length; i += 1) {
        for (let j = i + 1; j < pts.length; j += 1) {
          const d = dist(pts[i], pts[j]);
          if (d > best && d < 40) { best = d; a = pts[i]; b = pts[j]; }
        }
      }
      station.capsule = best > 3 ? [a, b] : null;
      station.major = station.lines.length >= 3 || station.lines.some((id) => ["RER", "TRAIN"].includes(state.lineById.get(id)?.type)) && station.lines.length >= 2;
      station.labelPriority = station.lines.length * 10 +
        (station.lines.some((id) => ["RER", "TRAIN"].includes(state.lineById.get(id)?.type)) ? 6 : 0) -
        station.name.length * 0.05;
    });

    // Walking connections between distinct stations.
    const walks = [];
    for (let i = 0; i < data.stations.length; i += 1) {
      const a = data.stations[i];
      for (let j = i + 1; j < data.stations.length; j += 1) {
        const b = data.stations[j];
        const d = dist([a.x, a.y], [b.x, b.y]);
        const sameName = a.nameNorm === b.nameNorm;
        if (d > (sameName ? 160 : WALK_NAME_RADIUS)) continue;
        if (d <= WALK_RADIUS || sameName || sharesNameToken(a, b)) walks.push({ a: a.id, b: b.id, d });
      }
    }
    state.walks = walks;
    state.walksByStation = new Map();
    walks.forEach((w) => {
      if (!state.walksByStation.has(w.a)) state.walksByStation.set(w.a, []);
      if (!state.walksByStation.has(w.b)) state.walksByStation.set(w.b, []);
      state.walksByStation.get(w.a).push({ id: w.b, d: w.d });
      state.walksByStation.get(w.b).push({ id: w.a, d: w.d });
    });
  }

  function polylineLength(points) {
    let total = 0;
    for (let i = 1; i < points.length; i += 1) total += dist(points[i - 1], points[i]);
    return total;
  }

  function pointAlong(points, target) {
    let walked = 0;
    for (let i = 1; i < points.length; i += 1) {
      const seg = dist(points[i - 1], points[i]);
      if (walked + seg >= target) {
        const t = seg ? (target - walked) / seg : 0;
        return [points[i - 1][0] + (points[i][0] - points[i - 1][0]) * t, points[i - 1][1] + (points[i][1] - points[i - 1][1]) * t];
      }
      walked += seg;
    }
    return points[points.length - 1];
  }

  // Where to draw the line number: beyond each terminus (pointing outward,
  // as on the PDF) and in the middle of long stretches of line.
  function lineAnchors(line) {
    const ends = [];
    line.segments.forEach((segment, index) => {
      const length = polylineLength(segment);
      [0, 1].forEach((side) => {
        const pts = side ? segment.slice().reverse() : segment;
        const p = pts[0];
        const joined = line.segments.some((other, j) => j !== index && projectOnPolyline(p, other).d < 8);
        if (joined) return;
        const q = pointAlong(pts, Math.min(18, length));
        const d = dist(p, q) || 1;
        ends.push({ p, dir: [(p[0] - q[0]) / d, (p[1] - q[1]) / d] });
      });
    });
    const uniqueEnds = [];
    ends.forEach((e) => { if (!uniqueEnds.some((o) => dist(o.p, e.p) < 40)) uniqueEnds.push(e); });
    // Several candidate spots per long stretch; the first free one is used.
    const mids = line.segments
      .filter((segment) => polylineLength(segment) > 320)
      .map((segment) => [0.5, 0.38, 0.62, 0.27, 0.73].map((f) => ({ p: pointAlong(segment, polylineLength(segment) * f), dir: [0, 0] })));
    return { ends: uniqueEnds, mids };
  }

  // Stops of one line are already joined by it, so no dotted walk link is drawn between them.
  function shareLine(aId, bId) {
    const b = state.stationById.get(bId);
    return state.stationById.get(aId).lines.some((id) => b.lines.includes(id));
  }

  function sharesNameToken(a, b) {
    const stop = new Set(["gare", "porte", "saint", "sainte", "place", "pont", "rue", "avenue", "les", "des", "du", "de", "la", "le", "et", "sur", "sous"]);
    const ta = a.nameNorm.split(" ").filter((t) => t.length >= 5 && !stop.has(t));
    const tb = new Set(b.nameNorm.split(" ").filter((t) => t.length >= 5 && !stop.has(t)));
    return ta.some((t) => tb.has(t));
  }

  function boundsOf(points) {
    let x0 = Infinity; let y0 = Infinity; let x1 = -Infinity; let y1 = -Infinity;
    points.forEach(([x, y]) => {
      if (x < x0) x0 = x; if (y < y0) y0 = y;
      if (x > x1) x1 = x; if (y > y1) y1 = y;
    });
    return [x0, y0, x1, y1];
  }

  // ---------------------------------------------------------------------------
  // rendering
  // ---------------------------------------------------------------------------

  function renderMap() {
    const data = state.data;
    landLayer.append("rect")
      .attr("class", "map-land")
      .attr("x", 655).attr("y", 118)
      .attr("width", 2829).attr("height", 2542)
      .attr("rx", 240);

    futureLayer.selectAll("path")
      .data(data.future || [])
      .join("path")
      .attr("class", "future-line")
      .attr("d", (d) => pathOf(d.points))
      .attr("stroke", (d) => d.color)
      .attr("stroke-width", (d) => (d.width >= 6 ? 4 : 2.6));
    futureLayer.attr("display", $("#showFuture").checked ? null : "none");

    const segments = data.lines
      .slice()
      .sort((a, b) => STROKE[b.type] - STROKE[a.type] || compareLines(b, a))
      .flatMap((line) => line.segments.map((points, index) => ({ line, points, key: `${line.id}-${index}` })));

    casingLayer.selectAll("path")
      .data(segments.filter((s) => s.line.type !== "TRAM" && s.line.status !== "construction"), (d) => d.key)
      .join("path")
      .attr("class", "route-casing")
      .attr("d", (d) => pathOf(d.points));

    const routes = routeLayer.selectAll("g.route")
      .data(segments, (d) => d.key)
      .join("g")
      .attr("class", (d) => `route ${d.line.type.toLowerCase()}`);
    routes.append("path")
      .attr("class", (d) => `route-line ${d.line.type.toLowerCase()}${d.line.status === "construction" ? " construction" : ""}`)
      .attr("d", (d) => pathOf(d.points))
      .attr("stroke", (d) => d.line.color);
    routes.filter((d) => d.line.type === "TRAM")
      .append("path")
      .attr("class", "route-inner")
      .attr("d", (d) => pathOf(d.points));

    hitLayer.selectAll("path")
      .data(segments, (d) => d.key)
      .join("path")
      .attr("class", "route-hit")
      .attr("d", (d) => pathOf(d.points))
      .on("pointerenter", (event, d) => { state.hoverLineId = d.line.id; showLineTooltip(event, d.line); highlightHover(); })
      .on("pointermove", (event, d) => showLineTooltip(event, d.line))
      .on("pointerleave", () => { state.hoverLineId = null; hideTooltip(); highlightHover(); })
      .on("click", (event, d) => {
        event.stopPropagation();
        if (event.metaKey || event.ctrlKey || event.shiftKey) toggleLineFocus(d.line.id);
        else selectLine(d.line.id);
      });

    transferLayer.selectAll("line")
      .data(state.walks.filter((w) => w.d > 8 && w.d <= WALK_RADIUS && !shareLine(w.a, w.b)))
      .join("line")
      .attr("class", "transfer-link")
      .attr("x1", (d) => state.stationById.get(d.a).x)
      .attr("y1", (d) => state.stationById.get(d.a).y)
      .attr("x2", (d) => state.stationById.get(d.b).x)
      .attr("y2", (d) => state.stationById.get(d.b).y);

    const stations = stationLayer.selectAll("g.station")
      .data(data.stations, (d) => d.id)
      .join("g")
      .attr("class", "station")
      .on("pointerenter", (event, d) => { state.hoverStationId = d.id; showStationTooltip(event, d); highlightHover(); })
      .on("pointermove", (event, d) => showStationTooltip(event, d))
      .on("pointerleave", () => { state.hoverStationId = null; hideTooltip(); highlightHover(); })
      .on("click", (event, d) => {
        event.stopPropagation();
        selectStation(d.id, { zoom: false });
      });
    stations.each(function (d) {
      const g = d3.select(this);
      if (d.capsule || d.lines.length > 1) {
        const [a, b] = d.capsule || [[d.x, d.y], [d.x, d.y]];
        const path = `M${a[0]},${a[1]}L${b[0] + (a[0] === b[0] && a[1] === b[1] ? 0.01 : 0)},${b[1]}`;
        g.append("path").attr("class", "station-outline").attr("d", path)
          .attr("stroke", "var(--station-ink)").attr("stroke-linecap", "round").attr("fill", "none");
        g.append("path").attr("class", "station-inner").attr("d", path)
          .attr("stroke", "var(--station-fill)").attr("stroke-linecap", "round").attr("fill", "none");
      } else {
        const line = state.lineById.get(d.lines[0]);
        const p = d.onLine.get(d.lines[0])?.p || [d.x, d.y];
        g.append("circle").attr("class", "station-shape simple")
          .attr("cx", p[0]).attr("cy", p[1])
          .style("stroke", line?.color || "var(--station-ink)");
      }
    });

    svg.on("click", () => clearSelection());
    updateSymbolSizes();
  }

  function updateSymbolSizes() {
    const k = state.transform.k || 1;
    routeLayer.selectAll("path.route-line").attr("stroke-width", (d) => Math.max(STROKE[d.line.type], MIN_SCREEN_STROKE[d.line.type] / k));
    routeLayer.selectAll("path.route-line.construction").attr("stroke-dasharray", (d) => {
      const w = Math.max(STROKE[d.line.type], MIN_SCREEN_STROKE[d.line.type] / k);
      return `${w * 2.2} ${w * 1.6}`;
    });
    routeLayer.selectAll("path.route-inner").attr("stroke-width", (d) => Math.max(STROKE[d.line.type], MIN_SCREEN_STROKE[d.line.type] / k) * 0.32);
    casingLayer.selectAll("path").attr("stroke-width", (d) => Math.max(STROKE[d.line.type], MIN_SCREEN_STROKE[d.line.type] / k) + 2.2 / k);
    hitLayer.selectAll("path").attr("stroke-width", (d) => Math.max(STROKE[d.line.type] + 4, 12 / k));
    transferLayer.selectAll("line").attr("stroke-width", 1.4 / k).attr("stroke-dasharray", `${1.5 / k} ${3 / k}`);
    const r = Math.min(Math.max(3.1, 2.6 / k), 7.5 / k);
    stationLayer.selectAll("circle.station-shape").attr("r", r).style("stroke-width", `${Math.max(1.1, 1.3 / k)}px`);
    stationLayer.selectAll("path.station-outline").attr("stroke-width", 2 * r + 2.4 / k);
    stationLayer.selectAll("path.station-inner").attr("stroke-width", 2 * r);
    overlayLayer.selectAll("circle.station-pulse").attr("r", r * 2.2).style("stroke-width", `${2.5 / k}px`);
    journeyLayer.selectAll(".journey-casing").attr("stroke-width", (d) => (STROKE[d.type] || 4) * 1.35 + 6 / k);
    journeyLayer.selectAll(".journey-line").attr("stroke-width", (d) => Math.max((STROKE[d.type] || 4) * 1.35, 4 / k));
    journeyLayer.selectAll(".journey-walk").attr("stroke-width", 3 / k).attr("stroke-dasharray", `${0.1} ${6 / k}`);
    journeyLayer.selectAll(".endpoint").attr("r", 7 / k).attr("stroke-width", 3 / k);
  }

  // ---------------------------------------------------------------------------
  // highlight / selection visuals
  // ---------------------------------------------------------------------------

  function activeLineSet() {
    if (state.journey) return new Set(state.journey.legs.filter((l) => l.lineId).map((l) => l.lineId));
    return state.focusLineIds;
  }

  function highlightHover() {
    const focus = activeLineSet();
    const hoverLine = state.hoverLineId;
    const hoverStation = state.hoverStationId ? state.stationById.get(state.hoverStationId) : null;
    const hoverLines = hoverStation ? new Set(hoverStation.lines) : hoverLine ? new Set([hoverLine]) : null;
    const lit = (id) => {
      if (hoverLines && !focus.size && !state.journey) return hoverLines.has(id);
      return !focus.size || focus.has(id) || (hoverLines && hoverLines.has(id) && !state.journey);
    };
    const dimAll = !!(focus.size || hoverLines);
    routeLayer.selectAll("g.route").classed("is-dim", (d) => dimAll && !lit(d.line.id));
    casingLayer.selectAll("path").classed("is-dim", (d) => dimAll && !lit(d.line.id));
    futureLayer.classed("is-dim", dimAll);
    transferLayer.classed("is-dim", dimAll);
    stationLayer.selectAll("g.station")
      .classed("is-dim", (d) => {
        if (state.journey) return !state.journey.stationIds.has(d.id);
        if (!focus.size) return false;
        return !d.lines.some((id) => focus.has(id));
      })
      .classed("is-hover", (d) => d.id === state.hoverStationId)
      .classed("is-selected", (d) => d.id === state.selectedStationId);
    if (hoverLine != null) {
      routeLayer.selectAll("g.route").filter((d) => d.line.id === hoverLine).raise();
    }
    updateLineChips();
    scheduleLabels();
  }

  // Selected station: pulse rings, a map pin and a name tag, drawn in screen
  // space so they stay the same size at every zoom level.
  const PIN_PATH = "M0,0 C-3,-9 -13,-15 -13,-27 A13,13 0 1 1 13,-27 C13,-15 3,-9 0,0 Z";

  function selectedTag(station) {
    const w = measure(station.name, 700) * 1.08 + 22;
    return { w, h: 26, y: -44 - 26 };
  }

  function updatePulse() {
    overlayLayer.selectAll("*").remove();
    focusLayer.selectAll("*").remove();
    const station = state.stationById.get(state.selectedStationId);
    if (!station) { scheduleLabels(); return; }
    const tag = selectedTag(station);
    const g = focusLayer.append("g").attr("class", "focus-marker").datum(station);
    g.append("circle").attr("class", "focus-ring").attr("r", 12);
    g.append("circle").attr("class", "focus-ring delay").attr("r", 12);
    g.append("circle").attr("class", "focus-halo").attr("r", 9);
    const pin = g.append("g").attr("class", "focus-pin");
    pin.append("ellipse").attr("class", "focus-pin-shadow").attr("rx", 7).attr("ry", 2.5);
    pin.append("path").attr("class", "focus-pin-body").attr("d", PIN_PATH);
    pin.append("circle").attr("class", "focus-pin-dot").attr("cy", -27).attr("r", 5.5);
    const label = g.append("g").attr("class", "focus-tag").attr("transform", `translate(0,${tag.y})`);
    label.append("rect").attr("x", -tag.w / 2).attr("width", tag.w).attr("height", tag.h).attr("rx", tag.h / 2);
    label.append("text").attr("y", tag.h / 2).text(station.name);
    moveFocus();
    scheduleLabels();
  }

  function moveFocus() {
    focusLayer.selectAll("g.focus-marker").attr("transform", (d) => {
      const [sx, sy] = toScreen(d.x, d.y);
      return `translate(${sx},${sy})`;
    });
  }

  // ---------------------------------------------------------------------------
  // zoom
  // ---------------------------------------------------------------------------

  // Useful PDF map area (the default view fits it).
  const MAP_CONTENT = [560, 70, 3600, 2700];
  let gestureStart = null;

  const zoom = d3.zoom()
    .scaleExtent([0.12, 14])
    .on("start", (event) => {
      if (event.sourceEvent) gestureStart = event.transform;
    })
    .on("end", (event) => {
      const start = gestureStart;
      gestureStart = null;
      if (!event.sourceEvent || !start) return;
      const t = event.transform;
      const moved = Math.abs(t.x - start.x) > 3 || Math.abs(t.y - start.y) > 3 || Math.abs(t.k - start.k) > 1e-3;
      if (moved) settleView();
    })
    .on("zoom", (event) => {
      state.transform = event.transform;
      viewport.attr("transform", event.transform);
      updateSymbolSizes();
      moveLabels();
      scheduleLabels();
    });
  svg.call(zoom).on("dblclick.zoom", null);
  svg.on("dblclick", (event) => {
    const [x, y] = d3.pointer(event);
    svg.transition().duration(250).call(zoom.scaleBy, 2, [x, y]);
  });

  function computeDefaultTransform() {
    const node = svg.node();
    const width = node.clientWidth || 1000;
    const height = node.clientHeight || 700;
    const [x0, y0, x1, y1] = MAP_CONTENT;
    const mobile = window.matchMedia("(max-width: 760px)").matches;
    const usableHeight = mobile ? height * 0.62 : height;
    const scale = Math.min(width / (x1 - x0), usableHeight / (y1 - y0)) * 0.98;
    const tx = (width - (x1 - x0) * scale) / 2 - x0 * scale;
    const ty = (usableHeight - (y1 - y0) * scale) / 2 - y0 * scale;
    state.defaultTransform = d3.zoomIdentity.translate(tx, ty).scale(scale);
    constrainZoom(width, height, [x0, y0, x1, y1]);
    return state.defaultTransform;
  }

  // Keep the map on screen: no panning far past the content and no zooming
  // out much beyond the full-map view. The extent always contains the default
  // view (on phones that includes the area under the bottom sheet).
  function constrainZoom(width, height, [x0, y0, x1, y1]) {
    const t = state.defaultTransform;
    const pad = 150;
    const view = [-t.x / t.k, -t.y / t.k, (width - t.x) / t.k, (height - t.y) / t.k];
    zoom
      .scaleExtent([t.k * 0.85, 14])
      .translateExtent([
        [Math.min(x0 - pad, view[0]), Math.min(y0 - pad, view[1])],
        [Math.max(x1 + pad, view[2]), Math.max(y1 + pad, view[3])],
      ]);
  }

  // After a drag or wheel zoom: near the full-map scale, go back to the whole
  // map; when zoomed in, spring back so no empty area shows past the map edge.
  function settleView() {
    const t = state.transform;
    const def = state.defaultTransform;
    if (t.k <= def.k * 1.05) {
      resetZoom(320);
      return;
    }
    const node = svg.node();
    const width = node.clientWidth;
    const mobile = window.matchMedia("(max-width: 760px)").matches;
    const height = mobile ? node.clientHeight * 0.62 : node.clientHeight;
    const [x0, y0, x1, y1] = MAP_CONTENT;
    const fit = (lo, hi, size, offset) => {
      const a = lo * t.k + offset;
      const b = hi * t.k + offset;
      if (b - a <= size) return (size - (b - a)) / 2 - lo * t.k;
      if (a > 0) return -lo * t.k;
      if (b < size) return size - hi * t.k;
      return offset;
    };
    const tx = fit(x0, x1, width, t.x);
    const ty = fit(y0, y1, height, t.y);
    if (Math.abs(tx - t.x) < 1 && Math.abs(ty - t.y) < 1) return;
    svg.transition().duration(280).ease(d3.easeCubicOut)
      .call(zoom.transform, d3.zoomIdentity.translate(tx, ty).scale(t.k));
  }

  function resetZoom(duration = 450) {
    svg.transition().duration(duration).call(zoom.transform, computeDefaultTransform());
  }

  function fitBounds([x0, y0, x1, y1], { padding = 60, maxScale = 5, duration = 600 } = {}) {
    const node = svg.node();
    const width = node.clientWidth;
    const mobile = window.matchMedia("(max-width: 760px)").matches;
    const height = mobile ? node.clientHeight * 0.4 : node.clientHeight;
    const w = Math.max(x1 - x0, 1);
    const h = Math.max(y1 - y0, 1);
    const scale = Math.min(maxScale, (width - padding * 2) / w, (height - padding * 2) / h);
    const tx = width / 2 - ((x0 + x1) / 2) * scale;
    const ty = height / 2 - ((y0 + y1) / 2) * scale;
    svg.transition().duration(duration).call(zoom.transform, d3.zoomIdentity.translate(tx, ty).scale(scale));
  }

  function zoomToStation(station) {
    fitBounds([station.x - 90, station.y - 90, station.x + 90, station.y + 90], { maxScale: 4 });
  }

  // ---------------------------------------------------------------------------
  // labels (screen space, collision aware)
  // ---------------------------------------------------------------------------

  function measure(text, weight) {
    const key = `${weight}|${text}`;
    measure.cache = measure.cache || new Map();
    if (!measure.cache.has(key)) {
      MEASURE.font = `${weight} ${LABEL_FONT}px Inter, system-ui, sans-serif`;
      measure.cache.set(key, MEASURE.measureText(text).width);
    }
    return measure.cache.get(key);
  }

  function splitLabel(name) {
    if (name.length <= 16) return [name];
    const parts = name.split(/ (?=[–-] )| – /);
    if (parts.length > 1 && parts.every((p) => p.length <= 22)) return parts.map((p) => p.replace(/^[–-] /, ""));
    const words = name.split(" ");
    const lines = [];
    let current = "";
    words.forEach((word) => {
      const next = current ? `${current} ${word}` : word;
      if (next.length > 16 && current) { lines.push(current); current = word; } else current = next;
    });
    if (current) lines.push(current);
    return lines.slice(0, 3);
  }

  function scheduleLabels() {
    clearTimeout(scheduleLabels.timer);
    scheduleLabels.timer = setTimeout(placeLabels, 90);
  }

  function toScreen(x, y) {
    const t = state.transform;
    return [x * t.k + t.x, y * t.k + t.y];
  }

  function placeLabels() {
    if (!state.data) return;
    const node = svg.node();
    const width = node.clientWidth;
    const height = node.clientHeight;
    const k = state.transform.k;
    const zoomRatio = k / (state.defaultTransform.k || k);
    const focus = activeLineSet();
    const journeyIds = state.journey ? state.journey.stationIds : null;

    const candidates = [];
    state.data.stations.forEach((station) => {
      const [sx, sy] = toScreen(station.x, station.y);
      if (sx < -80 || sy < -40 || sx > width + 80 || sy > height + 40) return;
      let priority = station.labelPriority;
      let forced = false;
      if (station.id === state.selectedStationId || station.id === state.hoverStationId) { priority += 1000; forced = true; }
      if (journeyIds) {
        if (!journeyIds.has(station.id)) return;
        priority += state.journey.keyStations.has(station.id) ? 500 : 200;
        forced = forced || state.journey.keyStations.has(station.id);
      } else if (focus.size) {
        if (!station.lines.some((id) => focus.has(id))) return;
        priority += 300;
      } else {
        if (zoomRatio < 1.25 && station.lines.length < 2) return;
        if (zoomRatio < 0.8 && !station.major) return;
      }
      candidates.push({ station, sx, sy, priority, forced });
    });
    candidates.sort((a, b) => b.priority - a.priority);

    const placed = [];
    const grid = new Map();
    const cell = 64;
    const keyOf = (x, y) => `${Math.floor(x / cell)},${Math.floor(y / cell)}`;
    const collides = (box) => {
      for (let gx = Math.floor(box[0] / cell); gx <= Math.floor(box[2] / cell); gx += 1) {
        for (let gy = Math.floor(box[1] / cell); gy <= Math.floor(box[3] / cell); gy += 1) {
          const list = grid.get(`${gx},${gy}`);
          if (list && list.some((o) => box[0] < o[2] && box[2] > o[0] && box[1] < o[3] && box[3] > o[1])) return true;
        }
      }
      return false;
    };
    const insert = (box) => {
      for (let gx = Math.floor(box[0] / cell); gx <= Math.floor(box[2] / cell); gx += 1) {
        for (let gy = Math.floor(box[1] / cell); gy <= Math.floor(box[3] / cell); gy += 1) {
          const key = `${gx},${gy}`;
          if (!grid.has(key)) grid.set(key, []);
          grid.get(key).push(box);
        }
      }
    };
    // Station markers are obstacles too.
    candidates.forEach((c) => insert([c.sx - 4, c.sy - 4, c.sx + 4, c.sy + 4, c.station.id]));

    // Screen-space index of the drawn route segments, so labels stay off lines.
    const segCell = 48;
    const segGrid = new Map();
    const activeLines = focus.size ? state.data.lines.filter((l) => focus.has(l.id)) : state.data.lines;
    activeLines.forEach((line) => {
      const half = Math.max(STROKE[line.type], MIN_SCREEN_STROKE[line.type] / k) * k / 2;
      line.segments.forEach((points) => {
        let prev = toScreen(points[0][0], points[0][1]);
        for (let i = 1; i < points.length; i += 1) {
          const cur = toScreen(points[i][0], points[i][1]);
          const x0 = Math.min(prev[0], cur[0]) - half;
          const x1 = Math.max(prev[0], cur[0]) + half;
          const y0 = Math.min(prev[1], cur[1]) - half;
          const y1 = Math.max(prev[1], cur[1]) + half;
          if (x1 >= -40 && y1 >= -40 && x0 <= width + 40 && y0 <= height + 40) {
            const seg = [prev[0], prev[1], cur[0], cur[1], half];
            for (let gx = Math.floor(x0 / segCell); gx <= Math.floor(x1 / segCell); gx += 1) {
              for (let gy = Math.floor(y0 / segCell); gy <= Math.floor(y1 / segCell); gy += 1) {
                const key = `${gx},${gy}`;
                if (!segGrid.has(key)) segGrid.set(key, []);
                segGrid.get(key).push(seg);
              }
            }
          }
          prev = cur;
        }
      });
    });

    // Line number badges go first; labels then avoid them.
    const badges = [];
    const badgeBoxes = [];
    // Keep the selected station's pin, rings and name tag clear of badges and labels.
    const selected = state.stationById.get(state.selectedStationId);
    if (selected) {
      const [sx, sy] = toScreen(selected.x, selected.y);
      const tag = selectedTag(selected);
      const focusBox = [Math.min(sx - tag.w / 2, sx - 22) - 4, sy + tag.y - 4, Math.max(sx + tag.w / 2, sx + 22) + 4, sy + 22, "focus"];
      insert(focusBox);
      badgeBoxes.push(focusBox);
    }
    const badgeCollides = (box) => badgeBoxes.some((o) => box[0] < o[2] && box[2] > o[0] && box[1] < o[3] && box[3] > o[1]);
    const badgeSize = (line) => {
      const text = lineShortLabel(line);
      return { text, w: line.type === "METRO" ? 19 : Math.max(19, measure(text, 800) * 0.92 + 9), h: 19 };
    };
    const tryPlace = (items, anchor, candidates, avoidLines = true) => {
      // items: [{ line, text, w, h }] drawn side by side; anchor: map point.
      const gap = 3;
      const total = items.reduce((sum, it) => sum + it.w, 0) + gap * (items.length - 1);
      const h = 19;
      const [px, py] = toScreen(anchor[0], anchor[1]);
      const boxes = candidates
        .filter(([cx, cy]) => !(cx - total / 2 < 6 || cy < 10 || cx + total / 2 > width - 6 || cy > height - 10))
        .map(([cx, cy]) => [cx - total / 2 - 2, cy - h / 2 - 2, cx + total / 2 + 2, cy + h / 2 + 2, `b${items.map((it) => it.line.id).join("-")}`])
        .filter((box) => !badgeCollides(box));
      // Prefer a spot that does not cover a drawn line.
      const clear = avoidLines ? boxes.find((box) => !lineCrossings(box)) : null;
      for (const box of clear ? [clear] : boxes.slice(0, 1)) {
        const cx = (box[0] + box[2]) / 2;
        const cy = (box[1] + box[3]) / 2;
        badgeBoxes.push(box);
        insert(box);
        let x = cx - total / 2;
        items.forEach((it) => {
          const bx = x + it.w / 2;
          badges.push({
            line: it.line, text: it.text, w: it.w, h,
            box: [bx - it.w / 2 - 1, cy - h / 2 - 1, bx + it.w / 2 + 1, cy + h / 2 + 1],
            map: anchor, dx: bx - px, dy: cy - py, key: `${it.line.id}:${anchor[0]}:${anchor[1]}`,
          });
          x += it.w + gap;
        });
        return true;
      }
      return false;
    };

    // Terminus badges: lines ending at the same place share one row, as on
    // the PDF (e.g. "9 15" at Pont de Sèvres).
    const ends = [];
    state.data.lines.slice().sort(compareLines).forEach((line) => {
      if (focus.size && !focus.has(line.id)) return;
      line.anchors.ends.forEach((a) => {
        if (!hasEndBadge(line, a.p)) return;
        const [px, py] = toScreen(a.p[0], a.p[1]);
        ends.push({ line, a, px, py, cx: px + a.dir[0] * 14, cy: py + a.dir[1] * 14, ...badgeSize(line) });
      });
    });
    const clusters = [];
    ends.forEach((e) => {
      const cluster = clusters.find((c) => c.some((o) => Math.hypot(o.cx - e.cx, o.cy - e.cy) < 30 && o.line.id !== e.line.id));
      if (cluster) cluster.push(e); else clusters.push([e]);
    });
    clusters.forEach((cluster) => {
      const anchor = cluster[0].a.p;
      const [px, py] = toScreen(anchor[0], anchor[1]);
      const mx = cluster.reduce((sum, e) => sum + e.cx, 0) / cluster.length;
      const my = cluster.reduce((sum, e) => sum + e.cy, 0) / cluster.length;
      const total = cluster.reduce((sum, e) => sum + e.w + 3, 0);
      // Several lines: a row under or over the station, like the PDF.
      const around = [
        [px, py + 20],
        [px, py - 20],
        [px + total / 2 + 12, py],
        [px - total / 2 - 12, py],
      ];
      tryPlace(cluster, anchor, cluster.length > 1 ? [...around, [mx, my]] : [[mx, my], ...around]);
    });

    // Mid-line roundels when zoomed in or when the line is focused.
    state.data.lines.forEach((line) => {
      const inFocus = focus.has(line.id);
      if (focus.size && !inFocus) return;
      if (!inFocus && zoomRatio < 1.8) return;
      const size = badgeSize(line);
      line.anchors.mids.forEach((spots) => {
        spots.some((a) => {
          const [px, py] = toScreen(a.p[0], a.p[1]);
          return tryPlace([{ line, ...size }], a.p, [[px, py]], false);
        });
      });
    });

    const limit = focus.size || journeyIds ? 400 : Math.min(420, 70 + zoomRatio * 90);
    for (const c of candidates) {
      if (c.station.id === state.selectedStationId) continue;
      if (placed.length >= limit && !c.forced) break;
      const lines = splitLabel(c.station.name);
      const weight = c.station.major ? 700 : 560;
      const w = Math.max(...lines.map((line) => measure(line, weight))) + 4;
      const h = lines.length * (LABEL_FONT + 1.5) + 2;
      // Half extents of the station marker on screen (capsules span lines).
      let hx = 6;
      let hy = 6;
      if (c.station.capsule) {
        const [a, b] = c.station.capsule;
        hx = Math.min(24, Math.abs(a[0] - b[0]) * k / 2 + 6);
        hy = Math.min(24, Math.abs(a[1] - b[1]) * k / 2 + 6);
      }
      // As on the PDF: above or below the line first, then beside it.
      const options = [
        { dx: -w / 2, dy: -hy - h - 1 },
        { dx: -w / 2, dy: hy + 1 },
        { dx: hx + 2, dy: -h / 2 },
        { dx: -hx - 2 - w, dy: -h / 2 },
        { dx: hx - 1, dy: -hy - h + 2 },
        { dx: -hx - w + 1, dy: -hy - h + 2 },
        { dx: hx - 1, dy: hy - 2 },
        { dx: -hx - w + 1, dy: hy - 2 },
      ];
      // Second ring a little farther out, for stations inside line bundles.
      const far = 12;
      options.push(
        { dx: -w / 2, dy: -hy - h - 1 - far },
        { dx: -w / 2, dy: hy + 1 + far },
        { dx: hx + 2 + far, dy: -h / 2 },
        { dx: -hx - 2 - w - far, dy: -h / 2 },
        { dx: hx - 1 + far * 0.7, dy: -hy - h + 2 - far * 0.7 },
        { dx: -hx - w + 1 - far * 0.7, dy: -hy - h + 2 - far * 0.7 },
        { dx: hx - 1 + far * 0.7, dy: hy - 2 + far * 0.7 },
        { dx: -hx - w + 1 - far * 0.7, dy: hy - 2 + far * 0.7 },
      );
      // Farther still, straight above/below/beside, to clear a wide bundle
      // passing next to the stop (e.g. a line that does not stop there).
      for (const d of [far * 2, far * 3]) {
        options.push(
          { dx: -w / 2, dy: -hy - h - 1 - d },
          { dx: -w / 2, dy: hy + 1 + d },
          { dx: hx + 2 + d, dy: -h / 2 },
          { dx: -hx - 2 - w - d, dy: -h / 2 },
        );
      }
      let chosen = null;
      let fallback = null;
      // First try spots clear of everything, then let the name cover a line badge.
      for (const softBadges of [false, true]) {
        for (const o of options) {
          const box = [c.sx + o.dx, c.sy + o.dy, c.sx + o.dx + w, c.sy + o.dy + h];
          if (collidesIgnoring(box, c.station.id, softBadges)) continue;
          const crossings = lineCrossings(box);
          if (!crossings) { chosen = { ...o, box }; break; }
          if (!fallback || crossings < fallback.crossings) fallback = { ...o, box, crossings };
        }
        if (chosen) break;
      }
      // Only must-show labels (selected, hovered, journey ends) may sit on a line.
      if (!chosen && c.forced) {
        const o = fallback || options[0];
        chosen = { ...o, box: o.box || [c.sx + o.dx, c.sy + o.dy, c.sx + o.dx + w, c.sy + o.dy + h] };
      }
      if (!chosen) continue;
      insert(chosen.box);
      placed.push({ ...c, lines, w, h, weight, ...chosen });
    }

    // Line badges hidden by a station name are dropped (the name matters more).
    const overlaps = (a, b) => a[0] < b[2] && a[2] > b[0] && a[1] < b[3] && a[3] > b[1];
    renderBadges(badges.filter((badge) => !placed.some((label) => overlaps(label.box, badge.box))));

    // Only single badges are "soft"; a shared terminus row ("9 15") stays whole.
    function isBadgeBox(o) {
      return typeof o[4] === "string" && o[4].startsWith("b") && !o[4].includes("-");
    }

    function lineCrossings(box) {
      const pad = 1.5;
      const b = [box[0] + pad, box[1] + pad, box[2] - pad, box[3] - pad];
      const seen = new Set();
      let count = 0;
      for (let gx = Math.floor(b[0] / segCell); gx <= Math.floor(b[2] / segCell); gx += 1) {
        for (let gy = Math.floor(b[1] / segCell); gy <= Math.floor(b[3] / segCell); gy += 1) {
          const list = segGrid.get(`${gx},${gy}`);
          if (!list) continue;
          for (const seg of list) {
            if (seen.has(seg)) continue;
            seen.add(seg);
            if (segmentHitsBox(seg, b)) count += 1;
          }
        }
      }
      return count;
    }

    function collidesIgnoring(box, id, softBadges = false) {
      for (let gx = Math.floor(box[0] / cell); gx <= Math.floor(box[2] / cell); gx += 1) {
        for (let gy = Math.floor(box[1] / cell); gy <= Math.floor(box[3] / cell); gy += 1) {
          const list = grid.get(`${gx},${gy}`);
          if (list && list.some((o) => o[4] !== id && !(softBadges && isBadgeBox(o)) &&
            box[0] < o[2] && box[2] > o[0] && box[1] < o[3] && box[3] > o[1])) return true;
        }
      }
      return false;
    }

    const labels = labelLayer.selectAll("text.label")
      .data(placed, (d) => d.station.id)
      .join((enter) => enter.append("text").attr("class", "label"))
      .attr("class", (d) => `label${d.station.major ? " major" : ""}${d.station.id === state.selectedStationId ? " is-focus" : ""}`)
      .style("font-size", `${LABEL_FONT}px`)
      .style("stroke-width", "3.2px")
      .attr("text-anchor", "start");
    labels.each(function (d) {
      const text = d3.select(this);
      text.selectAll("tspan")
        .data(d.lines)
        .join("tspan")
        .attr("x", 2)
        .attr("dy", (_, i) => (i === 0 ? LABEL_FONT : LABEL_FONT + 1.5))
        .attr("text-anchor", "start")
        .text((line) => line);
    });
    state.labels = placed;
    moveLabels();
  }

  function renderBadges(badges) {
    const groups = badgeLayer.selectAll("g.line-badge")
      .data(badges, (d) => d.key)
      .join((enter) => {
        const g = enter.append("g")
          .on("click", (event, d) => { event.stopPropagation(); selectLine(d.line.id); })
          .on("pointerenter", (event, d) => showLineTooltip(event, d.line))
          .on("pointerleave", hideTooltip);
        g.append("rect").attr("class", "badge-shape");
        g.append("text");
        return g;
      })
      .attr("class", (d) => `line-badge ${d.line.type.toLowerCase()}${d.line.status === "construction" ? " construction" : ""}`);
    groups.select("rect")
      .attr("x", (d) => -d.w / 2).attr("y", (d) => -d.h / 2)
      .attr("width", (d) => d.w).attr("height", (d) => d.h)
      .attr("rx", (d) => (d.line.type === "METRO" ? d.h / 2 : d.line.type === "TRAM" ? 4 : 3))
      .attr("fill", (d) => d.line.color);
    groups.select("text")
      .attr("fill", (d) => d.line.textColor)
      .text((d) => d.text);
    state.badges = badges;
  }

  // Does a (thick) screen segment [x0, y0, x1, y1, halfWidth] touch the box?
  function segmentHitsBox(seg, box) {
    const [x0, y0, x1, y1, half] = seg;
    const bx0 = box[0] - half;
    const by0 = box[1] - half;
    const bx1 = box[2] + half;
    const by1 = box[3] + half;
    // Liang-Barsky clip of the segment against the inflated box.
    let t0 = 0;
    let t1 = 1;
    const dx = x1 - x0;
    const dy = y1 - y0;
    const checks = [[-dx, x0 - bx0], [dx, bx1 - x0], [-dy, y0 - by0], [dy, by1 - y0]];
    for (const [p, q] of checks) {
      if (p === 0) {
        if (q < 0) return false;
      } else {
        const t = q / p;
        if (p < 0) { if (t > t1) return false; if (t > t0) t0 = t; }
        else { if (t < t0) return false; if (t < t1) t1 = t; }
      }
    }
    return true;
  }

  function moveLabels() {
    moveFocus();
    badgeLayer.selectAll("g.line-badge").attr("transform", (d) => {
      const [sx, sy] = toScreen(d.map[0], d.map[1]);
      return `translate(${sx + d.dx},${sy + d.dy})`;
    });
    labelLayer.selectAll("text.label").attr("transform", (d) => {
      const [sx, sy] = toScreen(d.station.x, d.station.y);
      return `translate(${sx + d.dx},${sy + d.dy})`;
    });
  }

  // ---------------------------------------------------------------------------
  // tooltip
  // ---------------------------------------------------------------------------

  function placeTooltip(event, html) {
    tooltip.innerHTML = html;
    tooltip.hidden = false;
    const pad = 14;
    const rect = tooltip.getBoundingClientRect();
    let left = event.clientX + pad;
    let top = event.clientY + pad;
    if (left + rect.width > window.innerWidth - 8) left = event.clientX - rect.width - pad;
    if (top + rect.height > window.innerHeight - 8) top = event.clientY - rect.height - pad;
    tooltip.style.left = `${left}px`;
    tooltip.style.top = `${top}px`;
  }

  function showStationTooltip(event, station) {
    if (event.pointerType === "touch") return;
    placeTooltip(event, `<strong>${escapeHtml(station.name)}</strong><span class="badges">${stationLines(station).map((l) => badgeHtml(l)).join("")}</span>`);
  }

  function showLineTooltip(event, line) {
    if (event.pointerType === "touch") return;
    placeTooltip(event, `<span class="badges">${badgeHtml(line)}</span> ${escapeHtml(lineLongLabel(line))}`);
  }

  function hideTooltip() {
    tooltip.hidden = true;
  }

  // ---------------------------------------------------------------------------
  // selection: station / line
  // ---------------------------------------------------------------------------

  function selectStation(id, { zoom: zoomMode = "reset", updateHash = true } = {}) {
    const station = state.stationById.get(id);
    if (!station) return;
    state.selectedStationId = id;
    state.focusLineIds = new Set(station.lines);
    if (state.journey) clearJourney({ keepInputs: true });
    switchTab("explore");
    renderStationDetails(station);
    updatePulse();
    highlightHover();
    if (zoomMode === "reset") resetZoom();
    else if (zoomMode === "station") zoomToStation(station);
    if (updateHash) writeHash();
  }

  function selectLine(id, { fit = true, updateHash = true } = {}) {
    const line = state.lineById.get(id);
    if (!line) return;
    const already = state.focusLineIds.size === 1 && state.focusLineIds.has(id) && !state.selectedStationId;
    if (already) { clearSelection(); return; }
    if (state.journey) clearJourney({ keepInputs: true });
    state.selectedStationId = null;
    state.focusLineIds = new Set([id]);
    updatePulse();
    renderLineDetails(line);
    switchTab("explore");
    highlightHover();
    if (fit) fitBounds(line.bbox, { padding: 50, maxScale: 3 });
    if (updateHash) writeHash();
  }

  function toggleLineFocus(id) {
    if (state.journey) clearJourney({ keepInputs: true });
    state.selectedStationId = null;
    const next = new Set(state.focusLineIds);
    if (next.has(id)) next.delete(id); else next.add(id);
    state.focusLineIds = next;
    updatePulse();
    if (next.size === 1) renderLineDetails(state.lineById.get([...next][0]));
    else renderEmptyDetails();
    highlightHover();
    writeHash();
  }

  function clearSelection() {
    state.selectedStationId = null;
    state.focusLineIds = new Set();
    if (state.journey) clearJourney({ keepInputs: true });
    updatePulse();
    renderEmptyDetails();
    highlightHover();
    writeHash();
  }

  function renderEmptyDetails() {
    details.innerHTML = `
      <div class="empty-state">
        <strong>${escapeHtml(T.emptyTitle)}</strong><br>${escapeHtml(T.emptyBody)}
        ${statsHtml()}
        <div class="section-label">${escapeHtml(T.shortcuts)}</div>
        <span class="kbd">/</span> ${escapeHtml(T.searchPlaceholder.replace(/\s*\(.*\)/, ""))}<br>
        <span class="kbd">+</span> <span class="kbd">−</span> ${escapeHtml(T.zoomIn)} / ${escapeHtml(T.zoomOut)}
        · <span class="kbd">0</span> ${escapeHtml(T.resetView)} · <span class="kbd">Esc</span> ${escapeHtml(T.clear)}
      </div>`;
  }

  function statsHtml() {
    const data = state.data;
    if (!data) return "";
    const interchanges = data.stations.filter((s) => s.lines.length > 1).length;
    const format = (n) => n.toLocaleString(LANG === "zh" ? "zh-CN" : LANG);
    return `<div class="stats-row">
      <div><span class="stat-number">${format(data.stats.stationCount)}</span><span class="stat-label">${escapeHtml(T.stations)}</span></div>
      <div><span class="stat-number">${format(data.stats.lineCount)}</span><span class="stat-label">${escapeHtml(T.lines)}</span></div>
      <div><span class="stat-number">${format(interchanges)}</span><span class="stat-label">${escapeHtml(T.interchanges)}</span></div>
    </div>`;
  }

  function neighborsOnLine(line, stationId) {
    return (line.adjacency.get(stationId) || [])
      .map((n) => state.stationById.get(n.id))
      .filter(Boolean);
  }

  function renderStationDetails(station) {
    const lines = stationLines(station);
    const neighborRows = lines.map((line) => {
      const next = neighborsOnLine(line, station.id);
      return `<div class="neighbor-row">${badgeHtml(line, { button: true })}<div class="links">${
        next.map((s) => `<button type="button" class="link-button" data-station="${s.id}">${escapeHtml(s.name)}</button>`).join(" · ") || "—"
      }</div></div>`;
    }).join("");
    const walks = (state.walksByStation.get(station.id) || [])
      .map((w) => state.stationById.get(w.id))
      .filter(Boolean)
      .map((s) => `<div class="neighbor-row"><span class="badges">${stationLines(s).map((l) => badgeHtml(l)).join("")}</span><div class="links"><button type="button" class="link-button" data-station="${s.id}">${escapeHtml(s.name)}</button></div></div>`)
      .join("");
    details.innerHTML = `
      <div class="card">
        <div class="card-title"><h2>${escapeHtml(station.name)}</h2></div>
        <div class="badges" style="margin-top:8px">${lines.map((l) => badgeHtml(l, { large: true, button: true })).join("")}</div>
        <div class="actions">
          <button type="button" class="pill-button primary" data-action="route-from">● ${escapeHtml(T.routeFrom)}</button>
          <button type="button" class="pill-button" data-action="route-to">◆ ${escapeHtml(T.routeTo)}</button>
          <button type="button" class="pill-button" data-action="zoom-station">⌕ ${escapeHtml(T.zoomHere)}</button>
        </div>
        <div class="section-label">${escapeHtml(T.nextStops)}</div>
        <div class="neighbors">${neighborRows}</div>
        ${walks ? `<div class="section-label">${escapeHtml(T.nearby)}</div><div class="neighbors">${walks}</div>` : ""}
      </div>`;
    details.dataset.station = station.id;
  }

  function renderLineDetails(line) {
    const termini = line.stations.filter((id) => (line.adjacency.get(id) || []).length === 1);
    const list = line.stations.map((id) => {
      const s = state.stationById.get(id);
      const others = stationLines(s).filter((l) => l.id !== line.id);
      return `<li class="${others.length ? "interchange" : ""}"><button type="button" class="stop-name" data-station="${s.id}">
        <span>${escapeHtml(s.name)}</span><span class="mini-badges">${others.map((l) => badgeHtml(l)).join("")}</span></button></li>`;
    }).join("");
    const terminusNames = termini.map((id) => state.stationById.get(id)?.name).filter(Boolean);
    details.innerHTML = `
      <div class="card" style="--line-color:${line.color}">
        <div class="card-title">
          <h2><span class="badges">${badgeHtml(line, { large: true })}</span> ${escapeHtml(lineLongLabel(line))}</h2>
        </div>
        <div class="card-sub">${line.status === "construction" ? `⚠ ${escapeHtml(T.construction)} · ` : ""}${line.stations.length} ${escapeHtml(T.stations)}${terminusNames.length ? ` · ${terminusNames.map(escapeHtml).join(" ⇄ ")}` : ""}</div>
        <div class="actions"><button type="button" class="pill-button" data-action="fit-line" data-line="${line.id}">⤢ ${escapeHtml(T.fitLine)}</button></div>
        <div class="section-label">${escapeHtml(T.stationsOnLine)}</div>
        <ol class="stop-list">${list}</ol>
      </div>`;
    details.dataset.station = "";
  }

  details.addEventListener("click", (event) => {
    const stationButton = event.target.closest("[data-station]");
    const lineButton = event.target.closest("[data-line]");
    const action = event.target.closest("[data-action]")?.dataset.action;
    const current = state.stationById.get(Number(details.dataset.station));
    if (action === "route-from" && current) { setRouteEndpoint("from", current); return; }
    if (action === "route-to" && current) { setRouteEndpoint("to", current); return; }
    if (action === "zoom-station" && current) { zoomToStation(current); return; }
    if (action === "fit-line" && lineButton) { fitBounds(state.lineById.get(Number(lineButton.dataset.line)).bbox, { padding: 50, maxScale: 3 }); return; }
    if (stationButton) { selectStation(Number(stationButton.dataset.station), { zoom: "station" }); return; }
    if (lineButton) selectLine(Number(lineButton.dataset.line));
  });

  // ---------------------------------------------------------------------------
  // line filters
  // ---------------------------------------------------------------------------

  function renderLineFilters() {
    const groups = TYPE_ORDER.map((type) => ({ type, lines: state.data.lines.filter((l) => l.type === type).sort(compareLines) }))
      .filter((g) => g.lines.length);
    lineFilters.innerHTML = groups.map((g) => `
      <div class="line-group">
        <div class="line-group-title"><span>${escapeHtml(T.groups[g.type] || g.type)}</span>
          <button type="button" class="text-button" data-group="${g.type}">${escapeHtml(T.showAll.split(" ")[0])} ✓</button></div>
        <div class="line-group-buttons">${g.lines.map((l) => `<button type="button" class="line-chip ${l.type.toLowerCase()}${l.status === "construction" ? " construction" : ""}" data-line="${l.id}"
          style="background:${l.color};color:${l.textColor}" title="${escapeHtml(lineLongLabel(l))}">${escapeHtml(lineShortLabel(l))}</button>`).join("")}</div>
      </div>`).join("");
  }

  function updateLineChips() {
    const focus = activeLineSet();
    lineFilters.querySelectorAll(".line-chip").forEach((chip) => {
      const id = Number(chip.dataset.line);
      chip.classList.toggle("is-active", focus.has(id));
      chip.classList.toggle("is-dimmed", focus.size > 0 && !focus.has(id));
    });
  }

  lineFilters.addEventListener("click", (event) => {
    const chip = event.target.closest(".line-chip");
    const group = event.target.closest("[data-group]");
    if (chip) {
      const id = Number(chip.dataset.line);
      if (event.metaKey || event.ctrlKey || event.shiftKey) toggleLineFocus(id);
      else selectLine(id);
    } else if (group) {
      if (state.journey) clearJourney({ keepInputs: true });
      state.selectedStationId = null;
      state.focusLineIds = new Set(state.data.lines.filter((l) => l.type === group.dataset.group).map((l) => l.id));
      updatePulse();
      renderEmptyDetails();
      highlightHover();
      writeHash();
    }
  });

  $("#clearLines").addEventListener("click", clearSelection);
  $("#showFuture").addEventListener("change", (event) => {
    futureLayer.attr("display", event.target.checked ? null : "none");
    try { localStorage.setItem("pm.future", event.target.checked ? "1" : "0"); } catch (_) { /* ignore */ }
  });

  // ---------------------------------------------------------------------------
  // search / autocomplete
  // ---------------------------------------------------------------------------

  function searchStations(query, limit = 8) {
    const q = normalizeText(query);
    if (!q) return [];
    const tokens = q.split(" ");
    const results = [];
    state.data.stations.forEach((s) => {
      const name = s.nameNorm;
      let score = -1;
      if (name === q) score = 100;
      else if (name.startsWith(q)) score = 80;
      else if (name.split(" ").some((w) => w.startsWith(q))) score = 60;
      else if (s.norm.includes(q)) score = 40;
      else if (tokens.length > 1 && tokens.every((t) => s.norm.split(" ").some((w) => w.startsWith(t)))) score = 30;
      if (score >= 0) results.push({ s, score: score + Math.min(s.lines.length, 5) - name.length * 0.01 });
    });
    return results.sort((a, b) => b.score - a.score).slice(0, limit).map((r) => r.s);
  }

  function searchLines(query) {
    const q = normalizeText(query).replace(/\s+/g, "");
    if (!q) return [];
    const forms = (l) => {
      const code = l.code.toLowerCase();
      const out = [lineShortLabel(l).toLowerCase(), normalizeText(lineLongLabel(l)).replace(/\s+/g, "")];
      if (l.type === "METRO") out.push(`m${code}`, `metro${code}`, `ligne${code}`, `line${code}`);
      if (l.type === "RER") out.push(`rer${code}`);
      if (l.type === "TRAM") out.push(`t${code}`, `tram${code}`);
      if (l.type === "TRAIN") out.push(`ligne${code}`, `train${code}`, `transilien${code}`);
      return out;
    };
    return state.data.lines.filter((l) => forms(l).some((f) => f === q)).sort(compareLines).slice(0, 4);
  }

  function highlightMatch(name, query) {
    const q = normalizeText(query);
    const norm = normalizeText(name);
    const idx = norm.indexOf(q);
    if (!q || idx < 0 || norm.length !== name.length) return escapeHtml(name);
    return `${escapeHtml(name.slice(0, idx))}<mark>${escapeHtml(name.slice(idx, idx + q.length))}</mark>${escapeHtml(name.slice(idx + q.length))}`;
  }

  function autocomplete(input, { onStation, onLine = null, onClear = null, autoExact = false }) {
    const box = input.parentElement.querySelector(".suggestions");
    let items = [];
    let active = 0;

    function render() {
      const query = input.value.trim();
      const lines = onLine ? searchLines(query) : [];
      const stations = searchStations(query, lines.length ? 6 : 8);
      items = [...lines.map((l) => ({ kind: "line", l })), ...stations.map((s) => ({ kind: "station", s }))];
      active = 0;
      if (!items.length || !query) { box.hidden = true; box.innerHTML = ""; return; }
      box.innerHTML = items.map((item, i) => {
        if (item.kind === "line") {
          return `<button type="button" role="option" class="suggestion${i === active ? " is-active" : ""}" data-i="${i}">
            <span class="suggestion-name">${escapeHtml(lineLongLabel(item.l))}</span><span class="badges">${badgeHtml(item.l)}</span></button>`;
        }
        return `<button type="button" role="option" class="suggestion${i === active ? " is-active" : ""}" data-i="${i}">
          <span class="suggestion-name">${highlightMatch(item.s.name, query)}</span>
          <span class="badges">${stationLines(item.s).map((l) => badgeHtml(l)).join("")}</span></button>`;
      }).join("");
      box.hidden = false;
    }

    function setActive(i) {
      if (!items.length) return;
      active = (i + items.length) % items.length;
      box.querySelectorAll(".suggestion").forEach((el, idx) => el.classList.toggle("is-active", idx === active));
      box.querySelectorAll(".suggestion")[active]?.scrollIntoView({ block: "nearest" });
    }

    function choose(i) {
      const item = items[i];
      if (!item) return;
      box.hidden = true;
      if (item.kind === "line") { input.value = lineLongLabel(item.l); onLine(item.l); } else { input.value = item.s.name; onStation(item.s); }
    }

    input.addEventListener("input", () => {
      render();
      if (!input.value.trim() && onClear) onClear();
      clearTimeout(input.exactTimer);
      if (!autoExact) return;
      // An exact station name selects that station once typing pauses.
      input.exactTimer = setTimeout(() => {
        const q = normalizeText(input.value);
        const exact = q ? state.data.stations.filter((st) => st.nameNorm === q) : [];
        if (exact.length === 1 && state.selectedStationId !== exact[0].id) {
          box.hidden = true;
          onStation(exact[0]);
        }
      }, 650);
    });
    input.addEventListener("focus", () => { if (input.value.trim()) render(); });
    input.addEventListener("keydown", (event) => {
      if (event.key === "ArrowDown") { event.preventDefault(); setActive(active + 1); }
      else if (event.key === "ArrowUp") { event.preventDefault(); setActive(active - 1); }
      else if (event.key === "Enter") { event.preventDefault(); if (box.hidden) render(); choose(active); }
      else if (event.key === "Escape") { box.hidden = true; input.blur(); }
    });
    box.addEventListener("pointerdown", (event) => {
      const el = event.target.closest(".suggestion");
      if (!el) return;
      event.preventDefault();
      choose(Number(el.dataset.i));
    });
    input.addEventListener("blur", () => setTimeout(() => { box.hidden = true; }, 120));
  }

  // ---------------------------------------------------------------------------
  // route planning
  // ---------------------------------------------------------------------------

  function edgeCost(line, w) {
    return line.type === "RER" || line.type === "TRAIN" ? 1.6 + w * 0.009 : 1.1 + w * 0.014;
  }

  function planRoute(fromId, toId, { transferPenalty = 5, excludeHeavy = false } = {}) {
    if (fromId === toId) return null;
    const allowed = (line) => line.status !== "construction" && !(excludeHeavy && (line.type === "RER" || line.type === "TRAIN"));
    const dist = new Map();
    const prev = new Map();
    const heap = new MinHeap();
    const start = `S${fromId}`;
    dist.set(start, 0);
    heap.push(0, start);
    const target = `S${toId}`;
    while (heap.size) {
      const [d, node] = heap.pop();
      if (d > (dist.get(node) ?? Infinity)) continue;
      if (node === target) break;
      const relax = (next, cost, info) => {
        const nd = d + cost;
        if (nd < (dist.get(next) ?? Infinity)) {
          dist.set(next, nd);
          prev.set(next, { node, ...info });
          heap.push(nd, next);
        }
      };
      if (node[0] === "S") {
        const sid = Number(node.slice(1));
        const station = state.stationById.get(sid);
        station.lines.forEach((lid) => {
          const line = state.lineById.get(lid);
          if (line && allowed(line)) relax(`L${sid}:${lid}`, node === start ? 0 : transferPenalty, { kind: "board" });
        });
        (state.walksByStation.get(sid) || []).forEach((w) => relax(`S${w.id}`, 2.5 + w.d * 0.05 + (node === start ? 0 : 1), { kind: "walk" }));
      } else {
        const [sidText, lidText] = node.slice(1).split(":");
        const sid = Number(sidText);
        const line = state.lineById.get(Number(lidText));
        relax(`S${sid}`, 0, { kind: "alight" });
        (line.adjacency.get(sid) || []).forEach((n) => relax(`L${n.id}:${line.id}`, edgeCost(line, n.w), { kind: "ride", line: line.id }));
      }
    }
    if (!prev.has(target)) return null;
    const path = [];
    let node = target;
    while (node !== start) {
      const p = prev.get(node);
      path.push({ kind: p.kind, line: p.line, at: node });
      node = p.node;
    }
    path.reverse();
    return buildJourney(fromId, path, dist.get(target));
  }

  function buildJourney(fromId, path, cost) {
    const legs = [];
    let current = null;
    let lastStation = fromId;
    path.forEach((step) => {
      if (step.kind === "ride") {
        const [sidText] = step.at.slice(1).split(":");
        const sid = Number(sidText);
        if (!current || current.lineId !== step.line) {
          current = { lineId: step.line, stations: [lastStation] };
          legs.push(current);
        }
        current.stations.push(sid);
        lastStation = sid;
      } else if (step.kind === "walk") {
        const sid = Number(step.at.slice(1));
        legs.push({ walk: true, stations: [lastStation, sid] });
        current = null;
        lastStation = sid;
      } else if (step.kind === "alight") {
        current = null;
      }
    });
    const stationIds = new Set();
    const keyStations = new Set();
    legs.forEach((leg) => {
      leg.stations.forEach((id) => stationIds.add(id));
      keyStations.add(leg.stations[0]);
      keyStations.add(leg.stations[leg.stations.length - 1]);
    });
    const transfers = Math.max(0, legs.filter((l) => !l.walk).length - 1);
    return { legs, stationIds, keyStations, minutes: Math.round(cost), transfers };
  }

  class MinHeap {
    constructor() { this.items = []; }
    get size() { return this.items.length; }
    push(priority, value) {
      const items = this.items;
      items.push([priority, value]);
      let i = items.length - 1;
      while (i > 0) {
        const parent = (i - 1) >> 1;
        if (items[parent][0] <= items[i][0]) break;
        [items[parent], items[i]] = [items[i], items[parent]];
        i = parent;
      }
    }
    pop() {
      const items = this.items;
      const top = items[0];
      const last = items.pop();
      if (items.length) {
        items[0] = last;
        let i = 0;
        for (;;) {
          const l = i * 2 + 1;
          const r = l + 1;
          let m = i;
          if (l < items.length && items[l][0] < items[m][0]) m = l;
          if (r < items.length && items[r][0] < items[m][0]) m = r;
          if (m === i) break;
          [items[m], items[i]] = [items[i], items[m]];
          i = m;
        }
      }
      return top;
    }
  }

  function directionOf(line, stations) {
    const last = stations[stations.length - 1];
    const before = stations[stations.length - 2];
    const seen = new Set(stations);
    let node = last;
    let from = before;
    for (let guard = 0; guard < 200; guard += 1) {
      const next = (line.adjacency.get(node) || []).map((n) => n.id).filter((id) => id !== from && !seen.has(id));
      if (!next.length) break;
      seen.add(next[0]);
      from = node;
      node = next[0];
    }
    return state.stationById.get(node)?.name;
  }

  function legGeometry(leg) {
    if (leg.walk) {
      const a = state.stationById.get(leg.stations[0]);
      const b = state.stationById.get(leg.stations[1]);
      return [[[a.x, a.y], [b.x, b.y]]];
    }
    const line = state.lineById.get(leg.lineId);
    const parts = [];
    for (let i = 0; i < leg.stations.length - 1; i += 1) {
      const a = state.stationById.get(leg.stations[i]).onLine.get(line.id);
      const b = state.stationById.get(leg.stations[i + 1]).onLine.get(line.id);
      if (a && b && a.chain === b.chain && a.chain >= 0) {
        const slice = slicePolyline(line.segments[a.chain], a.along, b.along);
        const direct = dist(a.p, b.p);
        const sliceLen = slice.reduce((sum, p, j) => (j ? sum + dist(slice[j - 1], p) : 0), 0);
        parts.push(sliceLen <= direct * 3 + 30 ? slice : [a.p, b.p]);
      } else {
        const pa = a?.p || [state.stationById.get(leg.stations[i]).x, state.stationById.get(leg.stations[i]).y];
        const pb = b?.p || [state.stationById.get(leg.stations[i + 1]).x, state.stationById.get(leg.stations[i + 1]).y];
        parts.push([pa, pb]);
      }
    }
    return parts;
  }

  function drawJourney() {
    journeyLayer.selectAll("*").remove();
    const journey = state.journey;
    if (!journey) { updateSymbolSizes(); return; }
    const pieces = journey.legs.flatMap((leg) => {
      const line = leg.walk ? null : state.lineById.get(leg.lineId);
      return legGeometry(leg).map((points) => ({ points, walk: !!leg.walk, color: line?.color, type: line?.type || "METRO" }));
    });
    journeyLayer.selectAll("path.journey-casing")
      .data(pieces.filter((p) => !p.walk))
      .join("path").attr("class", "journey-casing").attr("d", (d) => pathOf(d.points));
    journeyLayer.selectAll("path.journey-line")
      .data(pieces.filter((p) => !p.walk))
      .join("path").attr("class", "journey-line").attr("d", (d) => pathOf(d.points)).attr("stroke", (d) => d.color);
    journeyLayer.selectAll("path.journey-walk")
      .data(pieces.filter((p) => p.walk))
      .join("path").attr("class", "journey-walk").attr("d", (d) => pathOf(d.points));
    const first = state.stationById.get(journey.legs[0].stations[0]);
    const lastLeg = journey.legs[journey.legs.length - 1];
    const last = state.stationById.get(lastLeg.stations[lastLeg.stations.length - 1]);
    journeyLayer.append("circle").attr("class", "endpoint from").attr("cx", first.x).attr("cy", first.y);
    journeyLayer.append("circle").attr("class", "endpoint to").attr("cx", last.x).attr("cy", last.y);
    updateSymbolSizes();
  }

  function renderJourney() {
    const journey = state.journey;
    if (!state.routeFrom || !state.routeTo) {
      routeResult.innerHTML = `<div class="empty-state">${escapeHtml(T.routeEmpty)}</div>`;
      return;
    }
    if (!journey) {
      routeResult.innerHTML = `<div class="empty-state">${escapeHtml(T.routeNone)}</div>`;
      return;
    }
    const options = state.journeyOptions.length > 1
      ? `<div class="route-options">${state.journeyOptions.map((opt, i) => `
          <button type="button" class="route-option${i === state.journeyIndex ? " is-active" : ""}" data-option="${i}">
            <strong>${i === 0 ? escapeHtml(T.fastest) : escapeHtml(T.fewerTransfers)}</strong>
            ~${opt.minutes} ${escapeHtml(T.minutes)} · ${opt.transfers} ${escapeHtml(opt.transfers === 1 ? T.transfer : T.transfers)}
          </button>`).join("")}</div>`
      : "";
    const legs = journey.legs.map((leg) => {
      const from = state.stationById.get(leg.stations[0]);
      const to = state.stationById.get(leg.stations[leg.stations.length - 1]);
      if (leg.walk) {
        return `<li class="leg walk"><span class="leg-badge badge" style="background:var(--panel-2);color:var(--ink)">🚶</span>
          <div class="leg-head">${escapeHtml(T.walk)} ${escapeHtml(to.name)}</div></li>`;
      }
      const line = state.lineById.get(leg.lineId);
      const n = leg.stations.length - 1;
      const middle = leg.stations.slice(1, -1).map((id) => `<li>${escapeHtml(state.stationById.get(id).name)}</li>`).join("");
      return `<li class="leg" style="--leg-color:${line.color}">
        <span class="leg-badge">${badgeHtml(line, { button: true })}</span>
        <div class="leg-head"><button type="button" class="link-button" data-station="${from.id}">${escapeHtml(from.name)}</button></div>
        <div class="leg-meta">${escapeHtml(T.direction)} <strong>${escapeHtml(directionOf(line, leg.stations) || "")}</strong> · ${n} ${escapeHtml(n === 1 ? T.stop : T.stops)}</div>
        ${middle ? `<details><summary>${n - 1} ${escapeHtml(T.stops)}</summary><ol>${middle}</ol></details>` : ""}
      </li>`;
    }).join("");
    const lastLeg = journey.legs[journey.legs.length - 1];
    const end = state.stationById.get(lastLeg.stations[lastLeg.stations.length - 1]);
    routeResult.innerHTML = `
      <div class="route-summary"><span><strong>~${journey.minutes}</strong> ${escapeHtml(T.minutes)} <small>(${escapeHtml(T.estimate)})</small></span>
        <span>${journey.transfers} ${escapeHtml(journey.transfers === 1 ? T.transfer : T.transfers)}</span></div>
      ${options}
      <ol class="legs">${legs}</ol>
      <div class="leg-end">◆ <button type="button" class="link-button" data-station="${end.id}">${escapeHtml(end.name)}</button></div>`;
  }

  routeResult.addEventListener("click", (event) => {
    const option = event.target.closest("[data-option]");
    if (option) {
      state.journeyIndex = Number(option.dataset.option);
      state.journey = state.journeyOptions[state.journeyIndex];
      drawJourney(); renderJourney(); highlightHover();
      return;
    }
    const station = event.target.closest("[data-station]");
    if (station) {
      const s = state.stationById.get(Number(station.dataset.station));
      zoomToStation(s);
      return;
    }
    const line = event.target.closest("[data-line]");
    if (line) fitBounds(state.lineById.get(Number(line.dataset.line)).bbox, { padding: 50, maxScale: 3 });
  });

  function computeRoute({ fit = true } = {}) {
    state.journeyOptions = [];
    state.journey = null;
    if (state.routeFrom && state.routeTo && state.routeFrom !== state.routeTo) {
      const excludeHeavy = $("#avoidTrain").checked;
      const fastest = planRoute(state.routeFrom, state.routeTo, { excludeHeavy });
      if (fastest) {
        state.journeyOptions.push(fastest);
        const fewer = planRoute(state.routeFrom, state.routeTo, { excludeHeavy, transferPenalty: 16 });
        if (fewer && fewer.transfers < fastest.transfers) state.journeyOptions.push(fewer);
        state.journey = fastest;
        state.journeyIndex = 0;
      }
    }
    state.selectedStationId = null;
    state.focusLineIds = new Set();
    updatePulse();
    drawJourney();
    renderJourney();
    highlightHover();
    if (fit && state.journey) {
      const pts = [...state.journey.stationIds].map((id) => state.stationById.get(id)).map((s) => [s.x, s.y]);
      fitBounds(boundsOf(pts), { padding: 70, maxScale: 3.5 });
    }
    writeHash();
  }

  function clearJourney({ keepInputs = false } = {}) {
    state.journey = null;
    state.journeyOptions = [];
    drawJourney();
    if (!keepInputs) {
      state.routeFrom = null; state.routeTo = null;
      $("#routeFrom").value = ""; $("#routeTo").value = "";
    }
    renderJourney();
  }

  function setRouteEndpoint(which, station) {
    if (which === "from") { state.routeFrom = station.id; $("#routeFrom").value = station.name; }
    else { state.routeTo = station.id; $("#routeTo").value = station.name; }
    switchTab("route");
    if (state.routeFrom && state.routeTo) computeRoute();
    else {
      renderJourney();
      (which === "from" ? $("#routeTo") : $("#routeFrom")).focus();
    }
  }

  $("#routeSwap").addEventListener("click", () => {
    [state.routeFrom, state.routeTo] = [state.routeTo, state.routeFrom];
    const a = $("#routeFrom").value;
    $("#routeFrom").value = $("#routeTo").value;
    $("#routeTo").value = a;
    computeRoute({ fit: false });
  });
  $("#avoidTrain").addEventListener("change", () => computeRoute({ fit: false }));

  // ---------------------------------------------------------------------------
  // tabs, theme, panel, keyboard
  // ---------------------------------------------------------------------------

  function switchTab(name) {
    document.querySelectorAll(".tab").forEach((tab) => {
      const active = tab.dataset.tab === name;
      tab.classList.toggle("is-active", active);
      tab.setAttribute("aria-selected", active ? "true" : "false");
    });
    document.querySelectorAll(".tab-panel").forEach((panel) => {
      const active = panel.dataset.panel === name;
      panel.hidden = !active;
      panel.classList.toggle("is-active", active);
    });
    $("#rail").classList.remove("is-collapsed");
  }

  document.querySelectorAll(".tab").forEach((tab) => tab.addEventListener("click", () => {
    switchTab(tab.dataset.tab);
    if (tab.dataset.tab === "route" && state.journeyOptions.length && !state.journey) {
      state.journey = state.journeyOptions[state.journeyIndex];
      drawJourney();
      highlightHover();
    }
  }));

  function applyTheme(theme) {
    document.documentElement.dataset.theme = theme;
    document.querySelector('meta[name="theme-color"]').content = theme === "dark" ? "#0d131d" : "#ffffff";
  }

  (() => {
    let saved = null;
    try { saved = localStorage.getItem("pm.theme"); } catch (_) { /* ignore */ }
    applyTheme(saved || (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light"));
    try { $("#showFuture").checked = localStorage.getItem("pm.future") === "1"; } catch (_) { /* ignore */ }
  })();

  $("#themeToggle").addEventListener("click", () => {
    const next = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
    applyTheme(next);
    try { localStorage.setItem("pm.theme", next); } catch (_) { /* ignore */ }
  });

  $("#railToggle").addEventListener("click", () => {
    const rail = $("#rail");
    rail.classList.toggle("is-collapsed");
    $("#railToggle").setAttribute("aria-expanded", rail.classList.contains("is-collapsed") ? "false" : "true");
  });

  // Switch the interface language in place, re-rendering text-bearing parts.
  function setLanguage(lang) {
    if (!I18N[lang] || lang === LANG) return;
    LANG = lang;
    T = I18N[lang];
    try { localStorage.setItem("pm.lang", lang); } catch (_) { /* ignore */ }
    const params = new URLSearchParams(location.search);
    if (params.has("lang")) {
      params.set("lang", lang);
      history.replaceState(null, "", `${location.pathname}?${params}${location.hash}`);
    }
    applyI18n();
    if (!state.data) return;
    renderLineFilters();
    updateLineChips();
    const station = state.stationById.get(state.selectedStationId);
    if (station) renderStationDetails(station);
    else if (state.focusLineIds.size === 1) renderLineDetails(state.lineById.get([...state.focusLineIds][0]));
    else renderEmptyDetails();
    renderJourney();
    renderStatus();
    placeLabels();
  }

  document.querySelectorAll(".lang-switch [data-lang]").forEach((button) => {
    button.addEventListener("click", () => setLanguage(button.dataset.lang));
  });

  function renderStatus() {
    const data = state.data;
    if (!data) return;
    const offline = navigator.onLine === false ? `${T.offline} · ` : "";
    statusChip.textContent = `${offline}${data.stats.stationCount} ${T.stations} · ${data.stats.lineCount} ${T.lines} · ${data.source || "PDF"}`;
  }

  window.addEventListener("online", renderStatus);
  window.addEventListener("offline", renderStatus);

  // Offline support: cache the page and map data in the browser (public/sw.js).
  if ("serviceWorker" in navigator && (location.protocol === "https:" || location.hostname === "localhost" || location.hostname === "127.0.0.1")) {
    window.addEventListener("load", () => {
      navigator.serviceWorker.register("/sw.js").catch(() => { /* offline mode unavailable */ });
    });
  }

  // Back to the state right after page load (saved theme / layer prefs stay).
  function resetAll({ tab = "explore" } = {}) {
    ["#stationSearch", "#routeFrom", "#routeTo"].forEach((sel) => { $(sel).value = ""; });
    document.querySelectorAll(".suggestions").forEach((box) => { box.hidden = true; });
    $("#avoidTrain").checked = false;
    state.hoverStationId = null;
    state.hoverLineId = null;
    clearJourney();
    clearSelection();
    hideTooltip();
    switchTab(tab);
    history.replaceState(null, "", location.pathname + location.search);
    resetZoom();
  }

  $("#resetAll").addEventListener("click", () => resetAll());
  $("#resetRoute").addEventListener("click", () => {
    resetAll({ tab: "route" });
    $("#routeFrom").focus();
  });

  $("#zoomIn").addEventListener("click", () => svg.transition().duration(220).call(zoom.scaleBy, 1.5));
  $("#zoomOut").addEventListener("click", () => svg.transition().duration(220).call(zoom.scaleBy, 1 / 1.5));
  $("#zoomReset").addEventListener("click", () => resetZoom());
  $("#shareLink").addEventListener("click", async () => {
    writeHash();
    try {
      await navigator.clipboard.writeText(location.href);
      toast(T.linkCopied);
    } catch (_) {
      toast(location.href);
    }
  });

  document.addEventListener("keydown", (event) => {
    const typing = /INPUT|TEXTAREA/.test(document.activeElement?.tagName || "");
    if (event.key === "/" && !typing) {
      event.preventDefault();
      switchTab("explore");
      $("#stationSearch").focus();
      $("#stationSearch").select();
    } else if (event.key === "Escape" && !typing) {
      clearSelection();
    } else if (!typing && (event.key === "+" || event.key === "=")) {
      svg.transition().duration(200).call(zoom.scaleBy, 1.5);
    } else if (!typing && (event.key === "-" || event.key === "_")) {
      svg.transition().duration(200).call(zoom.scaleBy, 1 / 1.5);
    } else if (!typing && event.key === "0") {
      resetZoom();
    }
  });

  window.addEventListener("resize", () => {
    clearTimeout(window.__resizeTimer);
    window.__resizeTimer = setTimeout(() => {
      const wasDefault = Math.abs(state.transform.k - state.defaultTransform.k) < 1e-6;
      computeDefaultTransform();
      if (wasDefault) resetZoom(0);
      placeLabels();
    }, 120);
  });

  // ---------------------------------------------------------------------------
  // URL state
  // ---------------------------------------------------------------------------

  function writeHash() {
    let hash = "";
    if (state.journey && state.routeFrom && state.routeTo) hash = `route=${state.routeFrom}-${state.routeTo}${$("#avoidTrain").checked ? "-m" : ""}`;
    else if (state.selectedStationId) hash = `station=${state.selectedStationId}`;
    else if (state.focusLineIds.size) hash = `line=${[...state.focusLineIds].join(",")}`;
    const next = hash ? `#${hash}` : " ";
    if (location.hash !== (hash ? `#${hash}` : "")) history.replaceState(null, "", hash ? next : location.pathname + location.search);
  }

  function readHash() {
    const params = new URLSearchParams(location.hash.slice(1));
    if (params.get("route")) {
      const [a, b, m] = params.get("route").split("-");
      const from = state.stationById.get(Number(a));
      const to = state.stationById.get(Number(b));
      if (from && to) {
        $("#avoidTrain").checked = m === "m";
        state.routeFrom = from.id; state.routeTo = to.id;
        $("#routeFrom").value = from.name; $("#routeTo").value = to.name;
        switchTab("route");
        computeRoute();
        return true;
      }
    }
    if (params.get("station")) {
      const s = state.stationById.get(Number(params.get("station")));
      if (s) { selectStation(s.id, { zoom: "station", updateHash: false }); return true; }
    }
    if (params.get("line")) {
      const ids = params.get("line").split(",").map(Number).filter((id) => state.lineById.has(id));
      if (ids.length === 1) { selectLine(ids[0], { updateHash: false }); return true; }
      if (ids.length > 1) { state.focusLineIds = new Set(ids); highlightHover(); return true; }
    }
    return false;
  }

  // ---------------------------------------------------------------------------
  // boot
  // ---------------------------------------------------------------------------

  applyI18n();
  statusChip.textContent = T.loading;
  renderEmptyDetails();

  fetch("/api/map")
    .then((response) => {
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return response.json();
    })
    .catch(() => fetch("/data/map.json").then((response) => {
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return response.json();
    }))
    .then((data) => {
      prepare(data);
      renderMap();
      renderLineFilters();
      renderEmptyDetails();
      renderJourney();
      autocomplete($("#stationSearch"), {
        onStation: (s) => selectStation(s.id, { zoom: "station" }),
        onLine: (l) => selectLine(l.id),
        onClear: () => clearSelection(),
        autoExact: true,
      });
      autocomplete($("#routeFrom"), { onStation: (s) => { state.routeFrom = s.id; computeRoute(); if (!state.routeTo) $("#routeTo").focus(); } });
      autocomplete($("#routeTo"), { onStation: (s) => { state.routeTo = s.id; computeRoute(); } });
      renderStatus();
      svg.call(zoom.transform, computeDefaultTransform());
      if (!readHash()) highlightHover();
      window.parisMap = { state, planRoute, selectStation, selectLine };
    })
    .catch((error) => {
      statusChip.textContent = `${T.loadError}: ${error.message}`;
    });
})();
