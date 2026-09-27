// Offline support for the Paris transit map.
//
// - Page shell and map data are cached on install, so the map works offline
//   after the first visit.
// - Map data (/api/map, /data/map.json) and pages: network first, cached copy
//   when offline, so online visitors always get fresh data.
// - Versioned static files (?v=...) and web fonts: cache first.
//
// Bump CACHE_VERSION to drop old caches after a breaking change.

const CACHE_VERSION = "v1";
const CACHE = `paris-map-${CACHE_VERSION}`;
const PRECACHE = [
  "/",
  "/static/app.js",
  "/static/styles.css",
  "/vendor/d3.min.js",
  "/data/map.json",
];
const DATA_PATHS = new Set(["/api/map", "/data/map.json"]);
const FONT_HOSTS = new Set(["fonts.googleapis.com", "fonts.gstatic.com"]);

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE)
      .then((cache) => Promise.all(PRECACHE.map((url) => cache.add(url).catch(() => null))))
      .then(() => self.skipWaiting()),
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((key) => key.startsWith("paris-map-") && key !== CACHE).map((key) => caches.delete(key))))
      .then(() => self.clients.claim()),
  );
});

async function networkFirst(request, fallbacks = []) {
  const cache = await caches.open(CACHE);
  try {
    const response = await fetch(request);
    if (response.ok) cache.put(request, response.clone());
    return response;
  } catch (error) {
    const cached = await cache.match(request, { ignoreSearch: true });
    if (cached) return cached;
    for (const url of fallbacks) {
      const hit = await cache.match(url, { ignoreSearch: true });
      if (hit) return hit;
    }
    throw error;
  }
}

async function cacheFirst(request) {
  const cache = await caches.open(CACHE);
  const exact = await cache.match(request);
  if (exact) return exact;
  try {
    const response = await fetch(request);
    if (response.ok || response.type === "opaque") cache.put(request, response.clone());
    return response;
  } catch (error) {
    // Offline with a newer ?v= than cached: serve the previous version.
    const older = await cache.match(request, { ignoreSearch: true });
    if (older) return older;
    throw error;
  }
}

self.addEventListener("fetch", (event) => {
  const { request } = event;
  if (request.method !== "GET") return;
  const url = new URL(request.url);

  if (FONT_HOSTS.has(url.hostname)) {
    event.respondWith(cacheFirst(request));
    return;
  }
  if (url.origin !== self.location.origin) return;

  if (request.mode === "navigate") {
    event.respondWith(networkFirst(request, ["/"]));
  } else if (DATA_PATHS.has(url.pathname)) {
    event.respondWith(networkFirst(request, ["/api/map", "/data/map.json"]));
  } else if (url.search.includes("v=")) {
    event.respondWith(cacheFirst(request));
  } else {
    event.respondWith(networkFirst(request));
  }
});
