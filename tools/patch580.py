#!/usr/bin/env python3
# V580 (Martin 11.11. 00:56): Tutorial – Blöcke kommen ganz normal herunter, wie im normalen Spielscreen,
# als gäbe es den Tutorial-Streifen nicht: kein Einflug von ganz oben (V577 zurück); der fallende Block wird
# über Kurs-Streifen und Tutorial-Karte gezeichnet, nur wo er wirklich im Feld ist.
# + (00:58) Bis zum Diplom ist Blue nicht zu sehen: im Tutorial keine Blue-Sprechblase/Figur, nur seine Stimme.
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V579";', 'const GAME_VER = "V580";')
rep('''    const now = performance.now(); if (p !== EN.p) { EN.p = p; EN.t = now; let top = 1e9, cs = 20; for (const [x, y] of p.cells) { const [gx, gy] = v2g(p.x + x, p.y + y); const q = cvPt(gx, gy); top = Math.min(top, q.y); cs = q.cs || cs; } EN.d = Math.max(0, top + cs); let gi = 0.8; try { gi = gravityInterval(); } catch (e) {} EN.ms = Math.min(1400, Math.max(500, EN.d / cs * gi * 1000)); }   /* V577: Einflug von ganz oben */
    const k = Math.min(1, (now - EN.t) / EN.ms), off = -EN.d * (1 - k);''',
'''    const k = 1, off = 0;   /* V580: kein Einflug mehr – Block fällt ganz normal */
    const tb = document.getElementById("tutBar"), br = tb && !tb.hidden ? tb.getBoundingClientRect() : null;
    const over = (x0, y0, w, h, q) => q && q.width && !(x0 + w < q.left || x0 > q.right || y0 + h < q.top || y0 > q.bottom);''')
rep('''      if (k >= 1 && (x0 + w < cr.left || x0 > cr.right || y0 + h < cr.top || y0 > cr.bottom)) continue;   // nach dem Einflug nur dort, wo die Karte drüberliegt''',
'''      if (!over(x0, y0, w, h, cr) && !over(x0, y0, w, h, br)) continue;   // V580: nur dort, wo Karte oder Kurs-Streifen drüberliegen''')
rep('  function bubble(key) { const el = document.getElementById("buddy"); if (!el) return; const who = "blue";',
    '  function bubble(key) { if (typeof TUT !== "undefined" && TUT.on) return;   /* V580: bis zum Diplom nur Stimme, kein Bild */ const el = document.getElementById("buddy"); if (!el) return; const who = "blue";')
open(dst, "w", encoding="utf-8").write(s)
print("ok V580")
