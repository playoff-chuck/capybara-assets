#!/usr/bin/env python3
# V663 (Martin 12.11. 14:16): General in Parade-Uniform (Nano Banana Pro) = volle Grafik; Sprechblasen kürzer.
import sys, os
site = sys.argv[1]; p = os.path.join(site, "index.html"); s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V662";', 'const GAME_VER = "V663";')
rep('const GEN_FULL_IMG = "";', 'const GEN_FULL_IMG = "img/d83c175c56.webp";')
rep('toast("PARADE\'S OVER! · Lite graphics for smoother play – tap me for full graphics", "HQ", 4200);', 'toast("LITE GRAPHICS · Tap me for full graphics", "HQ", 4200);')
rep('toast("DRESS UNIFORM ON! · Full graphics are back – medals polished", "HQ", 3600);', 'toast("FULL GRAPHICS ARE BACK · Medals polished", "HQ", 3600);')
open(p, "w", encoding="utf-8").write(s); print("ok V663")
