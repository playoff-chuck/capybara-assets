#!/usr/bin/env python3
"""V539 (Martin 09.11. 21:42): Ankunftsbild – sobald der Kreis offen ist, zoomt das Bild langsam hinein (1 → 1,22)
und zoomt während der Blende in den Spielscreen weiter hinein (gleiche Richtung, kein Zurück).
Aufruf: python3 tools/patch539.py site/index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V538";', 'const GAME_VER = "V539";')
rep('#ovMap .mapArrive.fromPt.on img{transform:none}',
    '#ovMap .mapArrive.fromPt.on img{transform:none}#ovMap .mapArrive.fromPt.on.zin img{transform:scale(1.22);transition:transform 2.2s cubic-bezier(.3,0,.7,1)}')
rep('arrOrigin(arrC); ov.appendChild(arrC); requestAnimationFrame(() => requestAnimationFrame(() => arrC.classList.add("on")));',
    'arrOrigin(arrC); ov.appendChild(arrC); requestAnimationFrame(() => requestAnimationFrame(() => arrC.classList.add("on"))); setTimeout(() => { try { arrC && arrC.classList.add("zin"); } catch (e) {} }, 2700);   /* V539 */')
rep('at(10400, () => ov.classList.add("fadeOut"));',
    'at(9400, () => { try { arr && arr.classList.add("zin"); } catch (e) {} });   /* V539: nach dem Öffnen langsam hineinzoomen */\n      at(10400, () => ov.classList.add("fadeOut"));')
open(p, "w", encoding="utf-8").write(s); print("ok V539")
