#!/usr/bin/env python3
# V638 (Martin 11.11. 20:57): Tutorial «Monster plätten» – nur die ersten 4 Steine auf die rechteste Spur, danach normal in der Mitte.
# (V628 stapelte die rechte Spalte bis oben → Lektion 10 «Kanone rechts» hing auf großen Bildschirmen.)
import sys, os
site = sys.argv[1]; p = os.path.join(site, "index.html"); s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V637";', 'const GAME_VER = "V638";')
rep("const p0 = S.piece; let cells = p0.cells.map(c => c.slice());",
    "if ((window.__tutRightN = (window.__tutRightN || 0) + 1) > 4) throw 0;   /* V638: höchstens 4 Steine rechts */\n      const p0 = S.piece; let cells = p0.cells.map(c => c.slice());")
open(p, "w", encoding="utf-8").write(s)
print("ok V638")
