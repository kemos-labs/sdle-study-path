/* SDLE Study Path — light service worker for installability + shell cache.
   Progress stays in localStorage (not cached here). */
const CACHE = "sdle-shell-v48";
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
      .then((c) => c.addAll(SHELL.map((u) => new Request(u, { cache: "reload" }))))
      .then(() => self.skipWaiting())
      .catch(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (event) => {
  const req = event.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;

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
      .catch(() => caches.match(req).then((hit) => hit || caches.match("./index.html")))
  );
});
