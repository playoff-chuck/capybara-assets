#!/usr/bin/env python3
# V565 (Martin 10.11. 20:05 «der gelbe Pfeil hinkt nach»): Die 4-s-Mindestzeit galt auch für Bau/Block/Bewaffnen – der Pfeil blieb
# dann noch Sekunden auf dem alten Ziel (z. B. auf SHOP, obwohl man schon einen Block antippen sollte). Jetzt nur noch für DROP und Drehen;
# Pfeil wird alle 60 ms statt 120 ms nachgeführt. Special-Tutorial wartet, bis die Abschlusskarte durch ist. Proberunde: kürzerer Text.
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V564";', 'const GAME_VER = "V565";')
rep('if (TUT.t >= 4 && st.done()) {', 'if ((TUT.t >= 4 || (TUT.step >= 1 && TUT.step <= 3)) && st.done()) {   /* V565: Bau-Schritte sofort weiter, sonst hinkt der Pfeil */')
rep('    setInterval(tick, 120);\n    window.__TT && (window.__TT.comicArrow = tick);', '    setInterval(tick, 60);   /* V565 */\n    window.__TT && (window.__TT.comicArrow = tick);')
rep('if (TUT.on || hintKey || S.ton || window.__tutSumOpen) return;', 'if (TUT.on || hintKey || S.ton || window.__tutSumOpen || window.__tutSumPend) return;   /* V565: erst nach der Abschlusskarte */')
rep('$("hkGoldV").textContent = "NOW FOR REAL";', '$("hkGoldV").textContent = "FOR REAL!";')

# Martin 20:08: Turm am Rand bauen (Mitte hilft nicht), Pfeil schlägt einen Randblock vor; Dreh-Pfeil etwas höher
rep('{ t: "PICK A BLOCK", s: "Tap one of your landed blocks.", at: "board",',
    '{ t: "PICK A BLOCK AT THE EDGE", s: "Tap a block at the edge of the field – a tower there reaches the monsters on the ring.", at: "board",')
rep("""    function block() { try { let best = -1; for (let i = 0; i < S.grid.length; i++) { if (!S.grid[i] || S.towers.has(i) || (typeof TNT !== "undefined" && S.grid[i] === TNT)) continue; const x = i % GW, y = (i / GW) | 0; if (best < 0) best = i; else { const by = (best / GW) | 0, bx = best % GW; if (y < by || (y === by && Math.abs(x - 5.5) < Math.abs(bx - 5.5))) best = i; } }""",
    """    function block() { try { let best = -1, bs = 1e9; for (let i = 0; i < S.grid.length; i++) { if (!S.grid[i] || S.towers.has(i) || (typeof TNT !== "undefined" && S.grid[i] === TNT)) continue; const x = i % GW, y = (i / GW) | 0; if (y > 0 && S.grid[i - GW]) continue;   /* V565: oberster Block einer Spalte, möglichst am Rand */
        const sc = Math.min(x, GW - 1 - x) * 100 + y; if (sc < bs) { bs = sc; best = i; } }""")
rep('y = up ? r.bottom + 2 : r.top - 86 + (r.deep ? r.height * 0.5 : 0); }', 'y = up ? r.bottom + 2 : r.top - 86 + (r.deep ? r.height * 0.22 : 0); }   /* V565: Dreh-Pfeil höher */')
rep('arr.style.top = (r.top - 64 + (cur.at === "bRot" ? r.height * 0.5 : 0)) + "px"; } }', 'arr.style.top = (r.top - 64 + (cur.at === "bRot" ? r.height * 0.22 : 0)) + "px"; } }')

# Martin 20:10: Tutorial-Ende mit Stapel über 6 Reihen → Air Drop zum Bestätigen (fällt sofort), nicht erst knapp unter der Decke
rep('if (S && S.started && !S.over && !S.nuts && stackHeight() >= GH - 8 && window.__TT && window.__TT.ad) {', 'if (S && S.started && !S.over && !S.nuts && stackHeight() > 6 && window.__TT && window.__TT.ad) {   /* V565: ab 7 Reihen */')

open(dst, "w", encoding="utf-8").write(s)
print("ok")
