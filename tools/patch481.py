#!/usr/bin/env python3
"""V481 – Rosie bekommt eigene Freunde-Outfits (Martin 08.11. 22:51 «5 weibliche Kostüme mit viel Rosa, Gold, Schmuck, Glamour»):
Queen, Diva, Princess, Movie Star, Fairy Queen (img/outfit_rosie_5…9.webp). Blue behält Pop Star, Rock King, Big Boss, Pirate, Astronaut.
Nutzung: python3 tools/patch481.py src dst"""
import sys, re
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
m = re.search(r'const GAME_VER = "V(\d+)";', s); v = int(m.group(1))
rep(m.group(0), f'const GAME_VER = "V{v + 1}";')
rep('''["Pop Star", { f: 1 }], ["Rock King", { f: 2 }], ["Big Boss", { f: 3 }], ["Pirate", { f: 5 }], ["Astronaut", { f: 8 }]];   /* V413: Name, Sterne · V480: {w} = ab Welle, {f} = geworbene Freunde */''',
    '''["Pop Star", { f: 1 }], ["Rock King", { f: 2 }], ["Big Boss", { f: 3 }], ["Pirate", { f: 5 }], ["Astronaut", { f: 8 }]];   /* V413: Name, Sterne · V480: {w} = ab Welle, {f} = geworbene Freunde */
const OUTFIT_ROSIE = { 5: "Queen", 6: "Diva", 7: "Princess", 8: "Movie Star", 9: "Fairy Queen" };   /* V481: Rosies eigene Freunde-Outfits */
function outfitName(k, n) { return (k === "rosie" && OUTFIT_ROSIE[n]) || OUTFIT[n][0]; }''')
rep('''<img src="${outfitImg(k, n)}" alt=""><i>${o[0]}</i>''', '''<img src="${outfitImg(k, n)}" alt=""><i>${outfitName(k, n)}</i>''')
open(dst, "w", encoding="utf-8").write(s); print("ok", v + 1)
