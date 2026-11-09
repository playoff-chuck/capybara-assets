#!/usr/bin/env python3
"""V542 (Martin 09.11. 21:55): Nach der Landung (Start-Intro und jeder neue Kontinent) nur der rosa Punkt – keine
Figur (Blue/Rosie im Kreis) daneben. Die Figur erscheint erst beim Weiterreisen zum nächsten Ort.
Aufruf: python3 tools/patch542.py site/index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V541";', 'const GAME_VER = "V542";')
rep('at(7420 - sk, () => { setMe(MAP_PTS[P.c][0], true); });', 'at(7420 - sk, () => { setMe(MAP_PTS[P.c][0], false); });   /* V542: nur rosa Punkt */')
rep('at(8600 - sk, () => { setMe(MAP_PTS[P.c][0], true); label(', 'at(8600 - sk, () => { setMe(MAP_PTS[P.c][0], false); label(')
rep('at(5300, () => { drawPins(0); setMe(RB, true);', 'at(5300, () => { drawPins(0); setMe(RB, false);   /* V542 */')
open(p, "w", encoding="utf-8").write(s); print("ok V542")
