#!/usr/bin/env python3
"""V546 (Martin 09.11. 22:42): Test-Links für die Kontinent-Flüge: ?test=fly (Afrika, W31), fly2 (Asien, W61),
fly3 (Nordamerika, W91), fly4 (Antarktis, W121). Springt an das Ende des alten Kontinents; Flug, Landung,
Ankunftsbild mit Zoom und Blende in den Spielscreen laufen wie im echten Spiel.
Aufruf: python3 tools/patch546.py site/index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V545";', 'const GAME_VER = "V546";')
rep('nuts4: 121, thief: 100, wolfad:', 'nuts4: 121, fly: 31, fly2: 61, fly3: 91, fly4: 121, thief: 100, wolfad:')
open(p, "w", encoding="utf-8").write(s); print("ok V546")
