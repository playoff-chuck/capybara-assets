"""V226: Offline spielen (Flugzeugmodus). Web-App-Manifest + Service Worker (sw.js, Liste offline.json).
Startbildschirm: Knopf «Offline» links neben der Karte: speichert alles (inkl. Musik, ~42 MB) mit Fortschritt,
bietet auf Android «App installieren» an, auf dem iPhone den Hinweis «Teilen → Zum Home-Bildschirm».
Bestenliste/Runden brauchen Netz (fallen offline still weg)."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V225";', 'const GAME_VER = "V226";')
rep('<title>Capybara Squad</title>', '<title>Capybara Squad</title><link rel="manifest" href="manifest.webmanifest"><meta name="theme-color" content="#2b3a22"><link rel="apple-touch-icon" href="icons/icon-192.png"><meta name="apple-mobile-web-app-capable" content="yes"><meta name="mobile-web-app-capable" content="yes">')
js = r'''
  /* ===== V226: offline spielen ===== */
  try { if ("serviceWorker" in navigator && /^https?:$/.test(location.protocol) && !/claude|usercontent/.test(location.hostname)) {
    let prompt = null, state = LS.get("capy-offline") === "1" ? "ready" : "idle";
    const b = document.createElement("button"); b.type = "button"; b.id = "btnOffline"; b.className = "btn-small"; b.setAttribute("aria-label", "Play offline");
    const draw = (pct) => { b.classList.toggle("ok", state === "ready"); b.innerHTML = state === "ready" ? '<svg viewBox="0 0 24 24" width="24" height="24"><path d="M5 12.5l4.5 4.5L19 7.5" fill="none" stroke="#2f7a2a" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></svg><small>OFFLINE</small>'
        : state === "busy" ? `<b>${pct || 0}%</b><small>SAVING</small>` : '<svg viewBox="0 0 24 24" width="24" height="24"><path d="M12 3.5v11M7 10l5 5 5-5" fill="none" stroke="#3a2414" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/><path d="M4.5 16.5v3h15v-3" fill="none" stroke="#3a2414" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg><small>OFFLINE</small>'; };
    draw(); document.body.appendChild(b);
    const place = () => { const h = document.getElementById("btnMap") || document.getElementById("btnHs"); if (!h) return; const r = h.getBoundingClientRect(); if (!r.width) return; b.style.left = Math.round(r.left - 60) + "px"; b.style.top = Math.round(r.top) + "px"; };
    setInterval(place, 400); addEventListener("resize", place); place();
    addEventListener("beforeinstallprompt", e => { e.preventDefault(); prompt = e; });
    const ios = /iP(hone|ad|od)/.test(navigator.userAgent), standalone = matchMedia("(display-mode: standalone)").matches || navigator.standalone;
    navigator.serviceWorker.register("sw.js").then(reg => { navigator.serviceWorker.ready.then(r => { try { r.active && r.active.postMessage({ t: "sync" }); } catch (e) {} }); }).catch(() => {});
    navigator.serviceWorker.addEventListener("message", e => { const d = e.data || {}; if (d.t !== "offline" || state !== "busy") return; const pct = d.total ? Math.min(100, Math.floor(d.done / d.total * 100)) : 0; draw(pct);
      if (d.n >= d.of) { state = "ready"; LS.set("capy-offline", "1"); draw(); try { snd("coin"); } catch (er) {}
        toast(ios && !standalone ? "Saved! Tip: Share → Add to Home Screen" : "Saved! Works in flight mode now.", "OFFLINE", 3200); } });
    b.addEventListener("click", async () => { try { SFX.init(); } catch (e) {}
      if (state === "ready") { toast(navigator.onLine ? "All saved · plays in flight mode" : "Offline mode · leaderboard waits for signal", "OFFLINE", 2400); if (prompt) { prompt.prompt(); prompt = null; } return; }
      if (state === "busy") return;
      if (!navigator.onLine) { toast("Needs internet once to save the game", "OFFLINE", 2400); return; }
      state = "busy"; draw(0); try { snd("uiTap"); } catch (e) {}
      if (prompt) { try { prompt.prompt(); } catch (e) {} prompt = null; }
      const r = await navigator.serviceWorker.ready; (r.active || navigator.serviceWorker.controller).postMessage({ t: "fill" }); });
  } } catch (e) { console.warn("offline", e); }
'''
i = s.rfind('})();\n</script>'); s = s[:i] + js + s[i:]
css = '''<style id="v226">
#btnOffline{display:none;position:fixed!important;width:52px!important;height:52px!important;min-width:0!important;min-height:0!important;padding:0!important;z-index:60;flex-direction:column!important;align-items:center;justify-content:center;gap:0;line-height:1}
#btnOffline small{font:800 8px/1 "Baloo 2",sans-serif;letter-spacing:.08em;color:#3a2414;margin-top:1px}
#btnOffline b{font:800 15px/1 "Baloo 2",sans-serif;color:#d94c8c}
#btnOffline svg{display:block}
body:has(#ovStart:not([hidden])):has(#startMain:not([hidden])) #btnOffline{display:flex!important}
body:has(#ovStart:not([hidden])):has(.overlay.win:not([hidden])) #btnOffline,body:has(#ovAlbum:not([hidden])) #btnOffline,body.mapUp #btnOffline{display:none!important}
</style>
'''
i = s.rfind('</body>'); s = s[:i] + css + s[i:]
open(dst, 'w', encoding='utf-8').write(s); print('ok')
