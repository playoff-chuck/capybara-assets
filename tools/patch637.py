#!/usr/bin/env python3
# V637 (Martin 11.11. 16:24): Auf grauen Kontinenten auch keine Ortspunkte (weiße Kreise) mehr.
import sys, os
site = sys.argv[1]; p = os.path.join(site, "index.html"); s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V636";', 'const GAME_VER = "V637";')
rep('n.classList.toggle("greyC", g); }), 0);',
    'n.classList.toggle("greyC", g); }), 0);\n  pinsEl.querySelectorAll(".mPin[data-g]").forEach(m => { m.style.display = contGrey(Math.floor(+m.dataset.g / 6)) ? "none" : ""; });   /* V637: keine Ortspunkte auf grauen Kontinenten */')
open(p, "w", encoding="utf-8").write(s)
print("ok V637")
