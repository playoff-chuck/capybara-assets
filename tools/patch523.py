#!/usr/bin/env python3
"""V523 (Martin 09.11. 17:36): Weltkarte – «☠ L27»-Schild am Nuts-Gebiet war zu einem hohen Balken gestreckt
(zwei CSS-Regeln: top und bottom gleichzeitig gesetzt). Jetzt eine Regel, Schild über dem Gebiet.
Aufruf: python3 tools/patch523.py site/index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V522";', 'const GAME_VER = "V523";')
rep('.mNuts span{pointer-events:auto;cursor:pointer}.mNuts .nzL{bottom:auto;top:-12px}', '.mNuts span{pointer-events:auto;cursor:pointer}')
rep('.mNuts .nzL{position:absolute;left:50%;bottom:-6px;', '.mNuts .nzL{position:absolute;left:50%;top:-12px;bottom:auto;height:auto;')
rep('else if (!DAILY.v522) {', 'else if (!DAILY.v523) {')   # Martin: Abreißen nochmal zeigen
rep('DAILY.v522 = 1; }', 'DAILY.v522 = 1; DAILY.v523 = 1; }')
open(p, "w", encoding="utf-8").write(s); print("ok V523")
