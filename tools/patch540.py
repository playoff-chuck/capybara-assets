#!/usr/bin/env python3
"""V540 (Martin 09.11. 21:45): Ankunftsbild – Zoom beginnt zusammen mit dem Aufgehen des Bildes und läuft ohne Pause
durch bis in die Blende (ein fließender Zoom 1 → 1,25 über ~4,6 s, langsam beginnend, gegen Ende schneller).
Aufruf: python3 tools/patch540.py site/index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V539";', 'const GAME_VER = "V540";')
rep('#ovMap .mapArrive.fromPt.on.zin img{transform:scale(1.22);transition:transform 2.2s cubic-bezier(.3,0,.7,1)}',
    '#ovMap .mapArrive.fromPt.on.zin img{transform:scale(1.25);transition:transform 4.6s cubic-bezier(.45,0,.8,.85)}')
rep('setTimeout(() => { try { arrC && arrC.classList.add("zin"); } catch (e) {} }, 2700);   /* V539 */',
    'setTimeout(() => { try { arrC && arrC.classList.add("zin"); } catch (e) {} }, 60);   /* V540: Zoom startet mit dem Aufgehen */')
rep('at(9400, () => { try { arr && arr.classList.add("zin"); } catch (e) {} });   /* V539: nach dem Öffnen langsam hineinzoomen */',
    'at(6760, () => { try { arr && arr.classList.add("zin"); } catch (e) {} });   /* V540: Zoom startet mit dem Aufgehen, ohne Pause */')
open(p, "w", encoding="utf-8").write(s); print("ok V540")
