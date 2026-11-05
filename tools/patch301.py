"""V301 (To-do 20): anonymes Fehler- und Ereignis-Log.
Sendet Fehler (window.onerror, unhandledrejection, console.error), Start, Wellen-Meilensteine, Verlassen/Zurückkehren
(Welle + Bildschirm) an /api/events. Zufällige Sitzungsnummer je Spielstart, nicht gespeichert; keine Kennung.
Dazu: API auf der eigenen Domain direkt (/api), Rundenstatistik mit echter Version statt fest «V180»."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V300";', 'const GAME_VER = "V301";')
rep('const API_BASE = "https://2-29-147-164.sslip.io/api";',
    'const API_BASE = /(^|\\.)playcapybarasquad\\.com$/.test(location.hostname) ? "/api" : "https://2-29-147-164.sslip.io/api";')
rep('body: JSON.stringify({ mode: "pro", ...run, ver: "V180" })', 'body: JSON.stringify({ mode: "pro", ...run, ver: GAME_VER })')

JS = r'''
  /* V301: anonymes Fehler- und Ereignis-Log (To-do 20) */
  try { (() => {
    const ON = window.__evForce || /(^|\.)playcapybarasquad\.com$|sslip\.io$/.test(location.hostname);
    const sess = Array.from(crypto.getRandomValues(new Uint8Array(6)), b => b.toString(16).padStart(2, "0")).join("");
    const ua = navigator.userAgent || "";
    const plat = (/Android (\d+)/.exec(ua) || [])[1] ? "Android " + /Android (\d+)/.exec(ua)[1] : /iPhone|iPad/.test(ua) ? "iOS " + ((/OS (\d+)_/.exec(ua) || [])[1] || "") : /Windows/.test(ua) ? "Windows" : /Mac OS/.test(ua) ? "Mac" : /Linux/.test(ua) ? "Linux" : "?";
    const brw = (/(Edg|SamsungBrowser|Firefox|OPR|Chrome)\/(\d+)/.exec(ua) || []); let br = brw[1] ? brw[1].replace("Edg", "Edge").replace("OPR", "Opera") + " " + brw[2] : /Safari/.test(ua) ? "Safari" : "?";
    if (/^android-app:/.test(document.referrer || "") || (matchMedia && matchMedia("(display-mode: standalone)").matches)) br += " app";
    const dev = () => { try { return LS.get("tarnturm-dev") === "1"; } catch (e) { return false; } };
    const q = [], seenErr = {}; let nErr = 0, t0 = performance.now(), hiddenAt = 0, lastWave = 0;
    const wave = () => { try { return (S && S.wave) | 0; } catch (e) { return 0; } };
    const scr = () => { try { if (!S || !S.started) return "menu"; if (S.over) return "over"; if (S.mapShow || S.mapFly || document.body.classList.contains("mapUp")) return "map";
        if (typeof TUT !== "undefined" && TUT.on) return "tutorial"; if (S.nuts) return "nuts"; if (S.shop) return "shop"; if (S.paused) return "pause"; if (S.duel) return "hack";
        const v = id => { const e = document.getElementById(id); return e && !e.hidden; }; if (v("ovAd")) return "ad"; if (S.intro || S.ordersOpen) return "window";
        return S.inWave ? "wave" : "break"; } catch (e) { return "?"; } };
    const mins = () => Math.round((performance.now() - t0) / 600) / 100;
    function body() { return JSON.stringify({ ver: GAME_VER, sess, dev: dev(), plat, br, sw: screen.width | 0, sh: screen.height | 0, mem: navigator.deviceMemory || null, ev: q.splice(0, 12) }); }
    function flush(beacon) { if (!ON || !q.length) return; try { const b = body();
        if (beacon && navigator.sendBeacon && navigator.sendBeacon(API_BASE + "/events", b)) return;
        fetch(API_BASE + "/events", { method: "POST", headers: { "Content-Type": "application/json" }, body: b, keepalive: true }).catch(() => {}); } catch (e) {} }
    function push(k, extra) { if (q.length > 40) return; q.push(Object.assign({ k, w: wave(), scr: scr(), m: mins() }, extra || {})); }
    function err(msg, src) { msg = String(msg || "").slice(0, 300); if (!msg || /ResizeObserver loop|Script error\.?$/.test(msg)) return;
      const key = msg.slice(0, 120) + "|" + (src || ""); seenErr[key] = (seenErr[key] || 0) + 1; if (seenErr[key] > 3 || ++nErr > 25) return;
      push("error", { msg, src: src || "" }); setTimeout(() => flush(false), 1500); }
    window.addEventListener("error", e => { try { const f = String(e.filename || "").split("/").pop().split("?")[0]; err((e.error && e.error.stack ? String(e.error).slice(0, 200) : e.message), f ? `${f}:${e.lineno || 0}:${e.colno || 0}` : ""); } catch (x) {} }, true);
    window.addEventListener("unhandledrejection", e => { try { const r = e.reason; err("Unhandled: " + (r && r.message ? r.message : String(r)), ""); } catch (x) {} });
    const _ce = console.error.bind(console);
    console.error = function (...a) { try { const tag = typeof a[0] === "string" ? a[0] : ""; const ex = a.find(x => x instanceof Error);
        err((tag ? "[" + tag.slice(0, 40) + "] " : "") + (ex ? ex.name + ": " + ex.message : a.map(x => typeof x === "string" ? x : "").join(" ")),
            ex && ex.stack ? ((/index\.html:(\d+):(\d+)/.exec(ex.stack) || [])[0] || "") : ""); } catch (x) {} return _ce(...a); };
    push("start"); setTimeout(() => flush(false), 4000);
    setInterval(() => { try { const w = wave(); if (S && S.started && !S.over && w !== lastWave) { lastWave = w; if (w <= 3 || w === 5 || w % 10 === 0) push("wave"); } } catch (e) {} }, 2000);
    setInterval(() => flush(false), 30000);
    document.addEventListener("visibilitychange", () => { if (document.hidden) { hiddenAt = performance.now(); push("leave"); flush(true); }
      else if (hiddenAt && performance.now() - hiddenAt > 30000) { push("back"); } });
    window.addEventListener("pagehide", () => { if (!document.hidden) push("leave"); flush(true); });
    window.__evLog = { q, flush, push, sess, plat, br, scr };
  })(); } catch (e) {}
'''
end = '})();\n</script>'
i = s.rindex(end)
s = s[:i] + JS + s[i:]
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
