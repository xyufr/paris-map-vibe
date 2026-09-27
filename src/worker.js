// Cloudflare Worker for the Paris transit map.
// Static files come from ./public (Workers static assets). The map data is a
// pre-built JSON file, exported from MySQL by resources/export_static.py, and
// is also exposed at /api/map so the frontend works the same as with server.py.

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/api/map") {
      const asset = await env.ASSETS.fetch(new Request(new URL("/data/map.json", url), request));
      const response = new Response(asset.body, asset);
      response.headers.set("Content-Type", "application/json; charset=utf-8");
      response.headers.set("Cache-Control", "public, max-age=300");
      return response;
    }
    return env.ASSETS.fetch(request);
  },
};
