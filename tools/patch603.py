#!/usr/bin/env python3
# V603 (Martin 11.11. 08:01/08:04): neues Suno-Stück «Carnival Boss Battle» (Südamerika, schnell, motivierend; Drive) als Musik nach dem Diplom
# statt «Frostgnaw Sprint». Datei music/sa_carnival.mp4 (−20 LUFS wie die übrigen, AAC 96k).
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V602";', 'const GAME_VER = "V603";')
rep('const TRK = { skullgrog: ["Skullgrog Rush", 170],', 'const TRK = { carnival: ["Carnival Boss Battle", 150], skullgrog: ["Skullgrog Rush", 170],')
rep('const TRK_FILE = { skullgrog: "nz_skullgrog",', 'const TRK_FILE = { carnival: "sa_carnival", skullgrog: "nz_skullgrog",')
rep('''TP.certHold = "frostgnaw"; tpPlay("frostgnaw");''', '''TP.certHold = "carnival"; tpPlay("carnival");''')
open(dst, "w", encoding="utf-8").write(s)
print("ok", dst)
