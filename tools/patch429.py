#!/usr/bin/env python3
# V429 (Martin 07.11. 23:58): Outfits neu – jedes als Bearbeitung des Originalbilds (Gesicht/Körper identisch), gemeinsamer Bildausschnitt
# inkl. Standard (img/outfit_<held>_0.webp), damit Hüte nicht abgeschnitten werden. 8 Bilder Nano Banana Pro ≈ 1,10 $.
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:80])
    s = s.replace(a, b)
rep('const GAME_VER = "V428";', 'const GAME_VER = "V429";')
rep("function outfitImg(k, n) { return n ? `img/outfit_${k}_${n}.webp` : HERO_BASE[k]; }", "function outfitImg(k, n) { return `img/outfit_${k}_${n || 0}.webp`; }   /* V429: alle aus einem Ausschnitt */")
open(dst, "w", encoding="utf-8").write(s)
print("ok")
