#!/usr/bin/env python3
"""V448: Reichweiten-Vorschau erst nach 320 ms Halten – kurzes Tippen (Kaufen) zeigt das Spielfeld nicht mehr kurz (Martin 08.11. 12:58).
Nutzung: python3 tools/patch448.py src dst"""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()

def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (c, a[:80])
    s = s.replace(a, b)

rep('GAME_VER = "V447"', 'GAME_VER = "V448"')
rep('S.peek = { type, lvl }; held = false; sh.classList.add("peek"); document.body.classList.add("peeking"); clearTimeout(tm); tm = setTimeout(() => { held = true; }, 320); }, { passive: true });',
    'const pk = { type, lvl }; held = false; clearTimeout(tm); tm = setTimeout(() => { held = true; if (!S || !S.sel) return; S.peek = pk; sh.classList.add("peek"); document.body.classList.add("peeking"); }, 320); }, { passive: true });   /* V448: erst nach 320 ms Halten */')
open(dst, "w", encoding="utf-8").write(s)
print("ok", dst)
