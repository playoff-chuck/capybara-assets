#!/usr/bin/env python3
"""V466 – 80er-Disco-Outfits für Blue und Rosie in den Nuts-Levels (Neon-Stirnband, Schweißbänder; Nano Banana Pro).
Nutzung: python3 tools/patch466.py src dst"""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()

def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (c, a[:80])
    s = s.replace(a, b)

rep('const GAME_VER = "V465";', 'const GAME_VER = "V466";')
rep('const HERO_IMG = { get blue() { return outfitImg("blue", outfitSel("blue")); }, get rosie() { return outfitImg("rosie", outfitSel("rosie")); } };',
    'function heroDisco() { try { const s = window.__TT && window.__TT.S; return !!(s && s.nuts); } catch (e) { return false; } }   /* V466: Nuts = 80er-Disco-Outfit */\n'
    'const HERO_IMG = { get blue() { return heroDisco() ? "img/outfit_blue_disco.webp" : outfitImg("blue", outfitSel("blue")); }, get rosie() { return heroDisco() ? "img/outfit_rosie_disco.webp" : outfitImg("rosie", outfitSel("rosie")); } }; window.__heroImg = HERO_IMG; window.__heroDisco = heroDisco;')
open(dst, "w", encoding="utf-8").write(s)
print("ok V466")
