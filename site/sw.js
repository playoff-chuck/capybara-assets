/* Capybara Squad – Offline-Speicher.
   index.html: erst Netz (damit Updates sofort ankommen), sonst Speicher.
   Alles andere: erst Speicher, sonst Netz (und dann speichern). /api/ nie speichern.
   Liste aller Dateien: offline.json (tools/make_offline.py). Musik/Audio mit Range-Antworten (206). */
const CACHE = "capy-offline-v2";   /* V559 */   /* V357: neuer Name → alter Speicher (V332 u. a.) wird beim Aktivieren gelöscht */
const CORE = ["/", "/index.html", "/manifest.webmanifest", "/offline.json"];
self.addEventListener("install", e => { self.skipWaiting(); e.waitUntil(caches.open(CACHE).then(c => c.addAll(CORE)).then(() => fillAll(false)).catch(() => {})); });
self.addEventListener("activate", e => { e.waitUntil((async () => { for (const k of await caches.keys()) if (k !== CACHE) await caches.delete(k); await self.clients.claim(); })()); });
let filling = null;
async function fillAll(withMusic, lang) {   /* V552: Sprachclips nur für die eigene Sprache, und nur beim vollen Speichern */
  const r = await fetch("/offline.json", { cache: "no-store" }); const L = await r.json(); const c = await caches.open(CACHE);
  const list = L.files.filter(f => (withMusic || !/^music\//.test(f.p)) && (!/^lang\/voice_/.test(f.p) || (withMusic && lang && f.p === "lang/voice_" + lang + ".json"))); let done = 0, bytes = 0; const total = list.reduce((a, f) => a + f.s, 0);
  const tell = async () => { for (const cl of await self.clients.matchAll()) cl.postMessage({ t: "offline", done: bytes, total, n: done, of: list.length }); };
  let i = 0; const work = async () => { while (i < list.length) { const f = list[i++]; const url = "/" + f.p + (f.v ? "?v=" + f.v : "");
      try { const hit = await c.match(url); const len = hit && +(hit.headers.get("content-length") || 0); if (!hit || (f.s && len && len !== f.s)) { const res = await fetch(url, { cache: "no-cache" }); if (res.ok) await c.put(url, res); } } catch (e) {}
      done++; bytes += f.s; if (done % 4 === 0 || done === list.length) tell(); } };
  await Promise.all([work(), work(), work(), work()]);
  if (withMusic) { const m = await caches.open(CACHE); await m.put("/__offline_ready", new Response(String(L.ver || ""))); }
  await tell(); return { done, total };
}
self.addEventListener("message", e => { const d = e.data || {}; if (d.t === "sync") { if (!filling) filling = caches.open(CACHE).then(c => c.match("/__offline_ready")).then(r => fillAll(!!r, d.l)).finally(() => { filling = null; }); e.waitUntil(filling); }
  if (d.t === "fill") { if (!filling) filling = fillAll(true, d.l).finally(() => { filling = null; }); e.waitUntil(filling); }
  if (d.t === "pre" && Array.isArray(d.list)) e.waitUntil(preload(d.list)); });
/* V552: einzelne Dateien im Hintergrund vorladen (Musik des nächsten Kontinents) */
async function preload(list) { const c = await caches.open(CACHE); for (const p of list.slice(0, 20)) { if (typeof p !== "string" || !/^\/music\/[\w-]+\.mp4$/.test(p)) continue;
  try { if (!(await c.match(p))) { const res = await fetch(p, { cache: "no-cache" }); if (res.ok && res.status === 200) await c.put(p, res); } } catch (e) {} } }
async function ranged(req, res) {
  const rng = req.headers.get("range"); if (!rng || !res || res.status !== 200) return res;
  const buf = await res.arrayBuffer(), m = /bytes=(\d*)-(\d*)/.exec(rng); let a = m && m[1] ? +m[1] : 0, b = m && m[2] ? +m[2] : buf.byteLength - 1; b = Math.min(b, buf.byteLength - 1);
  return new Response(buf.slice(a, b + 1), { status: 206, headers: { "Content-Type": res.headers.get("Content-Type") || "application/octet-stream", "Content-Range": `bytes ${a}-${b}/${buf.byteLength}`, "Content-Length": String(b - a + 1), "Accept-Ranges": "bytes" } });
}
self.addEventListener("fetch", e => {
  const req = e.request, u = new URL(req.url); if (req.method !== "GET" || u.origin !== location.origin || u.pathname.startsWith("/api/") || u.pathname.startsWith("/privacy") || u.pathname.startsWith("/logos/")) return;
  if (u.pathname === "/" || u.pathname === "/index.html") {
    /* V331: erst Netz, aber nach 3,5 s die gespeicherte Fassung zeigen (langsames Handynetz); das Netz aktualisiert im Hintergrund weiter */
    let servedOld = false, oldLen = 0;   /* V356: alte Fassung gezeigt → nach dem Laden «newver» melden */
    const net = (async () => { const c = await caches.open(CACHE); const res = await fetch(req, { cache: "no-cache" }); if (res.ok) { const len = +(res.headers.get("content-length") || 0); await c.put("/index.html", res.clone()); await c.put("/", res.clone());
      if (servedOld) { const etag = res.headers.get("etag") || ""; if (etag !== oldEtag) for (const cl of await self.clients.matchAll({ includeUncontrolled: true })) cl.postMessage({ t: "newver" }); } } return res; })();
    let oldEtag = "";
    e.waitUntil(net.catch(() => {}));
    e.respondWith((async () => { const c = await caches.open(CACHE); const old = (await c.match("/index.html")) || (await c.match("/"));
      if (!old) return net.catch(() => Response.error()); oldEtag = old.headers.get("etag") || "";
      return Promise.race([net.then(r => r.clone()), new Promise(r => setTimeout(() => { servedOld = true; r(old); }, 3500))]).catch(() => { servedOld = true; return old; }); })());
    return; }
  e.respondWith((async () => { const c = await caches.open(CACHE); const key = u.pathname + u.search;
    const strict = !!u.search;   /* V559: versionierte Anfrage (?v=) → keine ältere Fassung aus dem Speicher, außer offline */
    let hit = await c.match(key) || (strict ? null : await c.match(key, { ignoreSearch: true }));
    if (hit) return ranged(req, hit);
    try { const res = await fetch(new Request(key, { cache: "no-cache" })); if (res.ok && res.status === 200) { c.put(key, res.clone()); return ranged(req, res); } if (strict) { const old = await c.match(key, { ignoreSearch: true }); if (old) return ranged(req, old); } return res; }
    catch (er) { const old = strict ? await c.match(key, { ignoreSearch: true }) : null; return old ? ranged(req, old) : Response.error(); } })());
});
