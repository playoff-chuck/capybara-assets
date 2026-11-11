#!/usr/bin/env python3
# V617 (Martin 11.11. 12:47): Im Tutorial springen fallende Steine (O-Block aus der Mitte plötzlich rechts, I-Block pendelt zwischen den zwei rechten Spalten).
# Ursache: V587/V599-Nachzielen alle 300 ms auf die laufenden Monster. Jetzt nur noch einmal beim Erscheinen des Steins zielen.
import sys, os
site = sys.argv[1]; p = os.path.join(site, "index.html"); s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V616";', 'const GAME_VER = "V617";')
rep('/* V601: auch Lektion 7 */ const p = S.piece;', '/* V601: auch Lektion 7 */ return;   /* V617: kein Nachzielen mehr – Stein sprang */ const p = S.piece;')
open(p, "w", encoding="utf-8").write(s)
print("ok V617")
