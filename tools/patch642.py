#!/usr/bin/env python3
# V642 (Martin 11.11. 21:49/21:50): Sicherheitsnetz – kein wartendes Ereignis hält andere länger als 2 Wellen auf.
# 1) Wartet Boss-Hack / Lucky / Orden / Rufzeichen seit ≥ 2 Wellen, gibt __offerOK nach 15 s Abstand frei (statt 30 s Ruhe + 95-s-Takt).
# 2) Air-Drop-Angebote warten höchstens 2 (statt 4) Wellen auf Lucky.
import sys, os
site = sys.argv[1]; p = os.path.join(site, "index.html"); s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V641";', 'const GAME_VER = "V642";')
rep('if ((S.wave || 0) <= S.prioW + 4) return;   /* V314: bis zu 4 Wellen */',
    'if ((S.wave || 0) < S.prioW + 2) return;   /* V314/V642: höchstens 2 Wellen */')
rep("/* V325: keine «soldier»-Sprüche */",
    "/* V642: Sicherheitsnetz – nichts wartet länger als 2 Wellen */\n"
    "try { (() => { const o = window.__offerOK, since = {}; let gS = null;\n"
    "  const pend = S => { const w = S.wave | 0, L = []; if (S.hackPending) L.push(\"hack\"); if ((S.banditNext ? w >= S.banditNext : !S.banditDone) && (S.playT || 0) >= 60) L.push(\"lucky\"); if (S.ordDue) L.push(\"ord\");\n"
    "    try { if (localStorage.getItem(\"tarnturm-join\") !== \"1\" && w >= 7) L.push(\"join\"); } catch (e) {} return L; };\n"
    "  setInterval(() => { try { const S = window.__TT && window.__TT.S; if (!S || !S.started || S.over || S.nuts) return; if (S !== gS) { gS = S; for (const k in since) delete since[k]; }\n"
    "    const w = S.wave | 0, L = pend(S); for (const k in since) if (!L.includes(k) || since[k] > w) delete since[k]; for (const k of L) if (!(k in since)) since[k] = w; } catch (e) {} }, 1000);\n"
    "  window.__stuck = () => { try { const w = window.__TT.S.wave | 0; return Object.keys(since).filter(k => w - since[k] >= 2); } catch (e) { return []; } };\n"
    "  window.__offerOK = function (force) { if (o.apply(this, arguments)) return true; try { if (!window.__playScreen() || !window.__stuck().length) return false;\n"
    "    return performance.now() - Math.max(window.__offerLast || -1e9, window.__evtLast || -1e9) >= 15000; } catch (e) { return false; } }; })(); } catch (e) { console.error(\"v642\", e); }\n"
    "/* V325: keine «soldier»-Sprüche */")
open(p, "w", encoding="utf-8").write(s)
print("ok V642")
