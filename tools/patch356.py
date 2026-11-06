"""V356: Updates kommen auch bei langsamem Netz an. Wenn der Service Worker nach 3,5 s die gespeicherte (alte) Fassung zeigt
und die neue danach fertig geladen ist, meldet er «newver»; die Seite lädt dann am Startbildschirm einmal neu
(im laufenden Spiel nur ein Hinweis). Martin sah V332 statt V355."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src + "/index.html", encoding='utf-8').read()
w = open(src + "/sw.js", encoding='utf-8').read()
def rep(t, a, b, cnt=1):
    n = t.count(a); assert n == cnt, (n, a[:70]); return t.replace(a, b)
s = rep(s, 'const GAME_VER = "V355";', 'const GAME_VER = "V356";')
s = rep(s, '    navigator.serviceWorker.addEventListener("message", e => { const d = e.data || {}; if (d.t !== "offline"',
    '    navigator.serviceWorker.addEventListener("message", e => { const d = e.data || {}; if (d.t !== "newver") return; let done = false; try { done = sessionStorage.getItem("capy-upd") === "1"; sessionStorage.setItem("capy-upd", "1"); } catch (x) {} if (done) return;   /* V356 */\n'
    '      if (typeof S === "undefined" || !S || !S.started) location.reload(); else try { toast("UPDATE READY · restart to get it", "HQ", 3500); } catch (x) {} });\n'
    '    navigator.serviceWorker.addEventListener("message", e => { const d = e.data || {}; if (d.t !== "offline"')
w = rep(w, 'const net = (async () => { const c = await caches.open(CACHE); const res = await fetch(req, { cache: "no-cache" }); if (res.ok) { await c.put("/index.html", res.clone()); await c.put("/", res.clone()); } return res; })();',
    'let servedOld = false, oldLen = 0;   /* V356: alte Fassung gezeigt → nach dem Laden «newver» melden */\n'
    '    const net = (async () => { const c = await caches.open(CACHE); const res = await fetch(req, { cache: "no-cache" }); if (res.ok) { const len = +(res.headers.get("content-length") || 0); await c.put("/index.html", res.clone()); await c.put("/", res.clone());\n'
    '      if (servedOld) { const etag = res.headers.get("etag") || ""; if (etag !== oldEtag) for (const cl of await self.clients.matchAll({ includeUncontrolled: true })) cl.postMessage({ t: "newver" }); } } return res; })();\n    let oldEtag = "";')
w = rep(w, 'if (!old) return net.catch(() => Response.error());\n      return Promise.race([net.then(r => r.clone()), new Promise(r => setTimeout(() => r(old), 3500))]).catch(() => old); })());',
    'if (!old) return net.catch(() => Response.error()); oldEtag = old.headers.get("etag") || "";\n      return Promise.race([net.then(r => r.clone()), new Promise(r => setTimeout(() => { servedOld = true; r(old); }, 3500))]).catch(() => { servedOld = true; return old; }); })());')
w = rep(w, 'const CACHE = "capy-offline-v1";', 'const CACHE = "capy-offline-v1";   /* V356 */')
import os; os.makedirs(dst, exist_ok=True)
open(dst + "/index.html", 'w', encoding='utf-8').write(s); open(dst + "/sw.js", 'w', encoding='utf-8').write(w)
print("ok")
