#!/usr/bin/env python3
# V424: Testlink ?test=weed5 → Welle 124, Unkraut-Feld mit 5 Samen.
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:80])
    s = s.replace(a, b)
rep('const GAME_VER = "V423";', 'const GAME_VER = "V424";')
rep('const map = { blk: 65, mag: 80, weed: 92,', 'const map = { blk: 65, mag: 80, weed: 92, weed5: 124,')
open(dst, "w", encoding="utf-8").write(s)
print("ok")
