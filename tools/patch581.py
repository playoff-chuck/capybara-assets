#!/usr/bin/env python3
# V581 (Martin 11.11. 01:05, Video): Tutorial
# - Neue Blöcke entstehen nicht mehr mitten im Kurs-Streifen: sie kommen vom oberen Bildschirmrand
#   Reihe für Reihe herunter und fliegen über Streifen und Karte, wie auf einem normalen Bildschirm.
#   Solange der Block einfliegt, steht die Schwerkraft; jede Eingabe (bewegen, drehen, fallen lassen) beendet den Einflug sofort.
# - Blue bleibt bis zum Diplom unsichtbar, auch in der Lücke zwischen Lektion 10 und der Urkunde (nur Stimme).
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V580";', 'const GAME_VER = "V581";')

# Schwerkraft steht während des Einflugs
rep('  if (!(S.lockT > 0)) S.gravT += dt;   // Lockdown: nichts fällt',
    '  if (!(S.lockT > 0) && !(S.tutEnter > performance.now())) S.gravT += dt;   // Lockdown: nichts fällt   /* V581: Tutorial-Einflug */')
# echtes Teil während des Einflugs nicht zeichnen (die Kopie fliegt darüber)
rep('    p.cells.forEach(([x, y], i) => { if (p.y + y >= 0) { const [a, b] = v2g(p.x + x, p.y + y); if (i === p.tnt) tntCell(a, b); else block(a, b, p.col); } });',
    '    if (!(S.tutEnter > performance.now())) p.cells.forEach(([x, y], i) => { if (p.y + y >= 0) { const [a, b] = v2g(p.x + x, p.y + y); if (i === p.tnt) tntCell(a, b); else block(a, b, p.col); } });   /* V581 */')

rep('    if (!on) { if (shown) { ox.clearRect(0, 0, oc.width, oc.height); shown = false; } return; }\n    const dpr',
    '    if (!on) { try { if (S) S.tutEnter = 0; } catch (e) {} EN.st = ""; if (shown) { ox.clearRect(0, 0, oc.width, oc.height); shown = false; } return; }\n    const dpr')
rep('''    const k = 1, off = 0;   /* V580: kein Einflug mehr – Block fällt ganz normal */''',
'''    const off = 0, now = performance.now(), sig = p.x + "," + p.y + "," + JSON.stringify(p.cells);
    /* V581: Einflug vom oberen Bildschirmrand, Reihe für Reihe, über Streifen und Karte */
    if (p !== EN.p) { EN.p = p; EN.st = p.y === 0 ? "wait" : ""; EN.c = []; }
    else if (EN.st === "wait") { EN.c = []; let bot = 0, cs = 0;
      for (const [x, y] of p.cells) { const [gx, gy] = v2g(p.x + x, p.y + y); if (gy < 0) continue;
        const a = cvPt(gx, gy), b = cvPt(gx + 1, gy + 1), x0 = Math.min(a.x, b.x), y0 = Math.min(a.y, b.y), w = Math.abs(b.x - a.x), h = Math.abs(b.y - a.y);
        const im = document.createElement("canvas"); im.width = Math.max(1, Math.round(w * sx)); im.height = Math.max(1, Math.round(h * sy)); im.getContext("2d").drawImage(cv, (x0 - r.left) * sx, (y0 - r.top) * sy, w * sx, h * sy, 0, 0, im.width, im.height);
        EN.c.push({ im, x0, y0, w, h }); bot = Math.max(bot, y0 + h); cs = Math.max(cs, h); }
      if (!EN.c.length || !cs) EN.st = ""; else { let gi = 0.8; try { gi = gravityInterval(); } catch (e) {}
        EN.n = Math.ceil(bot / cs); EN.step = Math.max(80, Math.min(250, gi * 1000 / 3)); EN.t0 = now; EN.sig = sig; S.tutEnter = now + EN.n * EN.step; EN.st = "in"; } }
    if (EN.st === "in") { if (sig !== EN.sig || now >= (S.tutEnter || 0)) { EN.st = ""; S.tutEnter = 0; }
      else { const rem = Math.max(0, EN.n - Math.floor((now - EN.t0) / EN.step)); for (const c of EN.c) { const yy = c.y0 - rem * c.h; if (yy + c.h < 0) continue; ox.drawImage(c.im, c.x0 * dpr, yy * dpr, c.w * dpr, c.h * dpr); } return; } }''')

# Blue bis zur Urkunde unsichtbar (auch zwischen Lektion 10 und Urkunde)
rep('  function bubble(key) { if (typeof TUT !== "undefined" && TUT.on) return;   /* V580: bis zum Diplom nur Stimme, kein Bild */',
    '  function bubble(key) { if ((typeof TUT !== "undefined" && TUT.on) || window.__tutSumPend || window.__tutSumNow || window.__tutSumOpen) return;   /* V580/V581: bis zum Diplom nur Stimme, kein Bild */')
open(dst, "w", encoding="utf-8").write(s)
print("ok V581")
