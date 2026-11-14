/* SDLE Study Path — light service worker for installability + shell cache.
   Progress stays in localStorage (not cached here). */
const CACHE_PREFIX = `sdle:${self.registration.scope}:`;
const CACHE = `${CACHE_PREFIX}v60`;
const SHELL = [
  "./",
  "./index.html",
  "./css/app.css",
  "./css/print.css",
  "./js/app.js",
  "./data/plan_tracks.js",
  "./data/video_links.js",
  "./data/book_index.js",
  "./data/exam_packs.js",
  "./data/topics.js",
  "./data/flash_notes_verdicts.js",
  "./manifest.webmanifest",
  "./icons/icon-192.png",
  "./icons/icon-512.png",
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches
      .open(CACHE)
      .then(async (c) => {
        const indexUrl = new URL("index.html", self.registration.scope).href;
        const response = await fetch(indexUrl, { cache: "reload" });
        if (!response.ok) throw new Error("Cannot cache app index");
        const html = await response.text();
        const assets = [...html.matchAll(/(?:src|href)="([^"]+)"/g)]
          .map((m) => new URL(m[1], indexUrl).href)
          .filter((u) => u.startsWith(self.registration.scope));
        const urls = [...new Set([...SHELL.map((u) => new URL(u, indexUrl).href), ...assets])];
        await c.addAll(urls.map((u) => new Request(u, { cache: "reload" })));
      })
      .then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((keys) => Promise.all(keys.filter((k) => k.startsWith(CACHE_PREFIX) && k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (event) => {
  const req = event.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin || !url.href.startsWith(self.registration.scope)) return;

  /* Network-first for app shell + data so deploys win; cache fallback offline.
     cache: "no-store" bypasses the HTTP cache — GitHub Pages sets max-age=600
     on everything, which would otherwise serve stale data within the TTL.
     The SW cache (below) is the only offline fallback. */
  event.respondWith(
    fetch(req, { cache: "no-store" })
      .then((res) => {
        const copy = res.clone();
        if (res.ok && (url.pathname.endsWith(".js") || url.pathname.endsWith(".css") || url.pathname.endsWith(".html") || url.pathname.endsWith("/"))) {
          caches.open(CACHE).then((c) => c.put(req, copy)).catch(() => {});
        }
        return res;
      })
      .catch(async () => {
        const cache = await caches.open(CACHE);
        const hit = await cache.match(req);
        if (hit) return hit;
        if (req.mode === "navigate") {
          const index = await cache.match(new URL("index.html", self.registration.scope).href);
          if (index) return index;
        }
        return new Response("Unavailable offline", { status: 503, headers: { "Content-Type": "text/plain" } });
      })
  );
});
