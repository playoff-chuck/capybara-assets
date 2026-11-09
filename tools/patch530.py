#!/usr/bin/env python3
"""V530 (Martin 09.11. 20:23): Kalenderblatt aufgeräumt – beim Blatt «morgen» kein leerer Balken und keine Zeile
«today ✓ done / tomorrow»; Unterzeile «7-day chain · 1 shield day» entfällt ganz.
Aufruf: python3 tools/patch530.py site/index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V529";', 'const GAME_VER = "V530";')
rep('<div class="dlBar"><b style="width:${Math.round(100 * Math.min(1, (m.p || 0) / m.n))}%"></b></div>${m.nx ? `<div class="num"><span>today ✓ done</span><span>tomorrow</span></div>` :',
    '${m.nx ? "" : `<div class="dlBar"><b style="width:${Math.round(100 * Math.min(1, (m.p || 0) / m.n))}%"></b></div>`}${m.nx ? "" :')
rep('<div class="sub">7-day chain · 1 shield day</div>', '')
open(p, "w", encoding="utf-8").write(s); print("ok V530")
