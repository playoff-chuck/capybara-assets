#!/usr/bin/env python3
"""V453: Blue am echten Fallschirm-Sprite (chuteb_1..6), wenn man Rosie spielt (Martin 08.11. 13:09 freigegeben, 0,14 $).
Nutzung: python3 tools/patch453.py src dst"""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V452";', 'const GAME_VER = "V453";')
rep('  const spr = b === "rosie";   /* V447: Rosie mit echtem Fallschirm-Sprite */',
    '  const spr = true, sp = b === "rosie" ? "chute" : "chuteb";   /* V447: Rosie mit echtem Fallschirm-Sprite · V453: Blue auch */')
rep('<img class="wpSpr" src="img/chute_1.webp" alt=""></div>`\n    : ch(b, 1.0, 0, ""));',
    '<img class="wpSpr" src="img/${sp}_1.webp" alt=""></div>`\n    : ch(b, 1.0, 0, ""));')
rep('im.src = `img/chute_${seq[i]}.webp`; }, 150); }', 'im.src = `img/${sp}_${seq[i]}.webp`; }, 150); }')
open(dst, "w", encoding="utf-8").write(s); print("ok", dst)
