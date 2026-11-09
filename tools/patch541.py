#!/usr/bin/env python3
"""V541 (Martin 09.11. 21:48):
1) Flug zu jedem neuen Kontinent wie das Start-Intro: kein gelber Zielpfeil, Kamera zoomt im Flug mit und nach der
   Landung nah auf den ersten Ort (statt Kontinent-Übersicht), dann geht das Ankunftsbild auf, zoomt fließend hinein
   und blendet in den Spielscreen über (gleiche Zeiten wie im Intro).
2) Flugzeug liegt auf der Karte immer ganz oben – über Punkten, Ortsschildern, Nuts-Gebieten und dem eigenen Pin.
Aufruf: python3 tools/patch541.py site/index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V540";', 'const GAME_VER = "V541";')
rep('#ovMap .mapPlane{filter:none!important;backface-visibility:hidden}',
    '#ovMap .mapPlane{filter:none!important;backface-visibility:hidden}#ovMap .mapPlane{z-index:60!important}#ovMap .mapMe{z-index:40}')
rep('at(4400 - sk, () => { label("", "Flying to " + nice(contName(P.c)), ""); flyPlane(MAP_PTS[oc][5], MAP_PTS[P.c][0], 3000); });',
    'at(4400 - sk, () => { label("", "Flying to " + nice(contName(P.c)), `First stop: ${nice(CONTS[P.c][2][0])}`); flyPlane(MAP_PTS[oc][5], MAP_PTS[P.c][0], 3000, true); });   /* V541: ohne Zielpfeil */\n'
    '      at(5000 - sk, () => { const a = MAP_PTS[oc][5], b = MAP_PTS[P.c][0]; go({ x: (a[0] + b[0]) / 2, y: (a[1] + b[1]) / 2, k: worldCam().k * 1.3 }, 1800); });   /* V541: im Flug mitzoomen wie im Intro */')
rep('at(7420 - sk, () => { setMe(MAP_PTS[P.c][0], true); });\n      at(7200 - sk, () => { go(contCam(P.c), 1300); });',
    'at(7420 - sk, () => { setMe(MAP_PTS[P.c][0], true); });\n      at(6900 - sk, () => { const b = MAP_PTS[P.c][0]; go({ x: b[0] + .02, y: b[1] - .06, k: Math.min(4.2, worldCam().k * 3) }, 1300); });   /* V541: nah auf den ersten Ort wie im Intro */')
rep('at(13200 - sk, () => ov.classList.add("fadeOut"));   /* V537: Blende statt Schnitt */\n      at(14000 - sk, hide); }',
    'at(12900 - sk, () => ov.classList.add("fadeOut"));   /* V537/V541: Blende statt Schnitt, Zeiten wie im Intro */\n      at(13700 - sk, hide); }')
open(p, "w", encoding="utf-8").write(s); print("ok V541")
