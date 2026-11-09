#!/usr/bin/env python3
"""V526 (Martin 09.11. 18:50/18:51):
- Russisch NUTS → ДУРДОМ (tools/ru_durdom526.py).
- Kalenderblatt: Stift-Geräusch = echte Marker-Aufnahme Nr. 5 (Freesound #751055, SSkiba88, CC0) → sfx/pen.mp3;
  Abreißen = Nr. 8, 20 % leiser (sfx/tear.mp3). Cache-Bust ?v=526. Heute geschaffte Mission wird nochmal einmal gezeigt.
Aufruf: python3 tools/patch526.py site/index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V525";', 'const GAME_VER = "V526";')
rep('const a = new Audio("sfx/" + n + ".mp3");', 'const a = new Audio("sfx/" + n + ".mp3?v=526");')
rep('else if (!DAILY.v523) {', 'else if (!DAILY.v526) {')
rep('DAILY.v522 = 1; DAILY.v523 = 1; }', 'DAILY.v522 = 1; DAILY.v523 = 1; DAILY.v526 = 1; }')
open(p, "w", encoding="utf-8").write(s); print("ok V526")
