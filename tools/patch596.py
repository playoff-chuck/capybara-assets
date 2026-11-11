#!/usr/bin/env python3
# V596 (Martin 11.11. 07:30): General heißt auf Russisch «Генерал Щетинин» (statt «Брисл»). Nur RU-Übersetzung (tools/lang_src/ru_v596.json); keine RU-Sprachaufnahme nennt den Namen.
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V595";', 'const GAME_VER = "V596";')
open(dst, "w", encoding="utf-8").write(s)
print("ok", dst)
