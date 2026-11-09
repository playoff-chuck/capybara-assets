#!/usr/bin/env python3
"""V547 (Martin 09.11. 22:50/22:51):
1) Nordamerika: das Nuts-Gebiet (GRUMBLEFANG) lag genau auf dem ersten Ort «Canyon» – Flug landete scheinbar im
   Nuts-Gebiet. Gebiet nach Süden (Mexiko/Mittelamerika) verlegt, frei von allen Orten.
2) Ankunftsbild (alle Kontinente + Start): Kopfkarte oben und Windrose/Sterne blenden aus, solange das Bild offen ist –
   vorher verdeckte die Kopfkarte den Kontinent-Namen und das Orts-Schild des Bildes.
3) Nach der Landung (ohne Figur) sitzt das Orts-Schild direkt über dem rosa Punkt statt weit darüber.
Aufruf: python3 tools/patch547.py site/index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V546";', 'const GAME_VER = "V547";')
rep('const x = P.reduce((a, p) => a + p[0], 0) / P.length, y = P.reduce((a, p) => a + p[1], 0) / P.length;',
    'let x = P.reduce((a, p) => a + p[0], 0) / P.length, y = P.reduce((a, p) => a + p[1], 0) / P.length; if (c === 3) { x = .25; y = .32; }   /* V547: Nordamerika nicht auf «Canyon» */')
rep('#ovMap .mapArrive.on .maTxt{transform:none;opacity:1}',
    '#ovMap .mapArrive.on .maTxt{transform:none;opacity:1}#ovMap:has(.mapArrive.on) .mapTop,#ovMap:has(.mapArrive.on) .mapRose{opacity:0!important;transition:opacity .5s ease}')
rep('#ovMap.auto .mPin.cur em{top:-70px}', '#ovMap.auto .mPin.cur em{top:-70px}#ovMap.auto:not(:has(.mapMe.on)) .mPin.cur:not(.lblDown) em{top:-14px}')   # V547: ohne Figur Schild direkt am rosa Punkt
open(p, "w", encoding="utf-8").write(s); print("ok V547")
