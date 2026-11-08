#!/usr/bin/env python3
"""V477 – Tagesmission «Clear 3 rows at once 1 times» (DE «Räume 3-mal 1 Reihen auf einmal», Zahlen vertauscht)
→ «Clear 3 rows at once ×1» wie die übrigen Missionen; Übersetzungen tools/lang_src/*_v477.json.
Nutzung: python3 tools/patch477.py src dst"""
import sys, re
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()

def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (c, a[:80])
    s = s.replace(a, b)

m = re.search(r'const GAME_VER = "V(\d+)";', s); v = int(m.group(1))
rep(m.group(0), f'const GAME_VER = "V{v + 1}";')
rep('["c3", "Clear 3 rows at once {n} times", [1, 1, 2, 3]]', '["c3", "Clear 3 rows at once ×{n}", [1, 1, 2, 3]]')
rep('let DAILY = dailyLoad();', 'let DAILY = dailyLoad(); if (DAILY.m && DAILY.m.k === "c3" && DAILY.m.n) DAILY.m.txt = "Clear 3 rows at once ×" + DAILY.m.n;   /* V477: alter gespeicherter Text */')
open(dst, "w", encoding="utf-8").write(s); print("ok", v + 1)
