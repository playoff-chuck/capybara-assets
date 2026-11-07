#!/usr/bin/env python3
# V420 (Martin 07.11. 23:01): Easter Egg – in Südamerika 5× gegen die Wand stoßen, je Kontinent eins mehr (Afrika 6, Asien 7, Nordamerika 8, Antarktis 9).
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:80])
    s = s.replace(a, b)
rep('const GAME_VER = "V419";', 'const GAME_VER = "V420";')
rep("if (push.n >= 5) { push.n = 0; const c = wherePos(S.wave).c;", "if (push.n >= 5 + wherePos(S.wave).c) { push.n = 0; const c = wherePos(S.wave).c;   /* V420: 5 + Kontinent */")
rep('toast("TEST · EASTER EGG: push a block 5× into the left or right wall", "HQ", 3500)', 'toast(`TEST · EASTER EGG: push a block ${5 + wherePos(S.wave).c}× into the left or right wall`, "HQ", 3500)')
open(dst, "w", encoding="utf-8").write(s)
print("ok")
