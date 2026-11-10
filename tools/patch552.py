#!/usr/bin/env python3
# V552: Lade-Diät (Martin 10.11. 12:40)
# - Service Worker lädt beim Start keine Sprachclip-Pakete mehr (das eigene lädt das Spiel selbst); «Offline speichern» nur noch die eigene Sprache
# - Deutsch (abgeschaltet) nicht mehr im Offline-Paket
# - Musik des aktuellen Kontinents und ab Ortsstufe 4 (Welle x20) des nächsten Kontinents im Hintergrund vorladen (nicht bei Datensparen/2G)
# Aufruf: python3 tools/patch552.py site   (ändert index.html, sw.js, tools/make_offline.py an Ort und Stelle)
import sys, os
site = sys.argv[1]
def patch(path, pairs):
    s = open(path, encoding="utf-8").read()
    for a, b in pairs:
        c = s.count(a); assert c == 1, (path, c, a[:80]); s = s.replace(a, b)
    open(path, "w", encoding="utf-8").write(s)
patch(os.path.join(site, "index.html"), [
 ('const GAME_VER = "V551";', 'const GAME_VER = "V552";'),
 ('r.active && r.active.postMessage({ t: "sync" });', 'r.active && r.active.postMessage({ t: "sync", l: (typeof I18N !== "undefined" && I18N.lang) || "en" });'),
 ('(r.active || navigator.serviceWorker.controller).postMessage({ t: "fill" });', '(r.active || navigator.serviceWorker.controller).postMessage({ t: "fill", l: (typeof I18N !== "undefined" && I18N.lang) || "en" });'),
 ('/* V325: keine «soldier»-Sprüche */', '''/* V552: Lade-Diät – Musik des aktuellen und (ab Welle x20) des nächsten Kontinents im Hintergrund vorladen */
try { (() => { if (!("serviceWorker" in navigator)) return;
  const MUS = [["andes_lounge", "jungle_downtempo", "copacabana_sunset", "rumba_lounge", "samba_lounge", "lounge_disco", "chill_disco_rio", "airport_bossa", "nz_skullgrog", "nz_anthem"],
    ["af_oasis", "af_savanna", "af_dune", "af_dune2", "af_pyramid", "nz_gorkazar"],
    ["as_taiga", "as_frozen", "as_steppe", "as_iceport", "as_icepalace", "nz_frostgnaw"],
    ["na_dorian_dust", "na_odd_phased", "na_game_loop", "na_cartoon_loop", "na_midtown", "na_miami", "nz_grumblefang"],
    ["an_ice_a", "an_ice_b", "an_frozen_retro", "an_glide"]];
  const asked = new Set();
  const pre = k => { if (k < 0 || k >= MUS.length || asked.has(k)) return; asked.add(k);
    try { const c = navigator.connection; if (c && (c.saveData || /2g/.test(c.effectiveType || ""))) return; } catch (e) {}
    navigator.serviceWorker.ready.then(r => { const w = r.active || navigator.serviceWorker.controller; if (w) w.postMessage({ t: "pre", list: MUS[k].map(f => "/music/" + f + ".mp4") }); }).catch(() => {}); };
  setInterval(() => { try { if (!S || !S.started || S.over || S.testRun) return; const w = Math.max(1, S.wave | 0), k = Math.floor((w - 1) / 30); pre(k); if ((w - 1) % 30 >= 19) pre(k + 1); } catch (e) {} }, 5000);
})(); } catch (e) { console.error("v552", e); }

/* V325: keine «soldier»-Sprüche */'''),
])
patch(os.path.join(site, "sw.js"), [
 ('async function fillAll(withMusic) {', 'async function fillAll(withMusic, lang) {   /* V552: Sprachclips nur für die eigene Sprache, und nur beim vollen Speichern */'),
 ("const list = L.files.filter(f => withMusic || !/^music\\//.test(f.p));", "const list = L.files.filter(f => (withMusic || !/^music\\//.test(f.p)) && (!/^lang\\/voice_/.test(f.p) || (withMusic && lang && f.p === \"lang/voice_\" + lang + \".json\")));"),
 ('.then(r => fillAll(!!r)).finally(', '.then(r => fillAll(!!r, d.l)).finally('),
 ('if (!filling) filling = fillAll(true).finally(() => { filling = null; }); e.waitUntil(filling); } });', '''if (!filling) filling = fillAll(true, d.l).finally(() => { filling = null; }); e.waitUntil(filling); }
  if (d.t === "pre" && Array.isArray(d.list)) e.waitUntil(preload(d.list)); });
/* V552: einzelne Dateien im Hintergrund vorladen (Musik des nächsten Kontinents) */
async function preload(list) { const c = await caches.open(CACHE); for (const p of list.slice(0, 20)) { if (typeof p !== "string" || !/^\\/music\\/[\\w-]+\\.mp4$/.test(p)) continue;
  try { if (!(await c.match(p))) { const res = await fetch(p, { cache: "no-cache" }); if (res.ok && res.status === 200) await c.put(p, res); } } catch (e) {} } }'''),
])
patch(os.path.join(os.path.dirname(os.path.abspath(site)), "tools", "make_offline.py") if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(site)), "tools", "make_offline.py")) else "tools/make_offline.py", [
 ("if p in skip or p.startswith('logos/') or f.startswith('.'): continue", "if p in skip or p.startswith('logos/') or f.startswith('.') or p in ('lang/voice_de.json', 'lang/de.json'): continue   # V552: Deutsch abgeschaltet"),
])
print("ok")
