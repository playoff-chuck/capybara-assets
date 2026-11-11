#!/usr/bin/env python3
# V614 (Martin 11.11. 12:18: Lena bekommt nach «Сохранено» kein Icon): Android ohne Install-Angebot des Browsers
# bekommt nach dem Speichern sofort den Menü-Hinweis statt nur «Saved!».
import sys, os
site = sys.argv[1]; p = os.path.join(site, "index.html"); s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V613";', 'const GAME_VER = "V614";')
rep('prompt && !isInst() ? "Saved! Tap ✈ again for the home-screen icon" : "Saved! Works in flight mode now."',
    'prompt && !isInst() ? "Saved! Tap ✈ again for the home-screen icon" : andr && !isInst() ? "Home-screen icon: browser menu ⋮ → Add to Home screen" : "Saved! Works in flight mode now."')
open(p, "w", encoding="utf-8").write(s)
print("ok V614")
