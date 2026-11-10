#!/usr/bin/env python3
# V590 (Martin 11.11. 01:50/01:55): Ende der Аномалия – schöner Hintergrund für den Ergebnis-Bildschirm (alle Kontinente):
# Weltkugel mit goldener Route, der Trupp jubelt oben drauf, ein erledigtes Monster unten (Nano Banana Pro, 0,14 $).
# Die Ergebnis-Karte sitzt unten, damit Kugel und Trupp oben frei bleiben; das kleine Verfolgungsbild in der Karte entfällt.
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V589";', 'const GAME_VER = "V590";')
CSS = """<style id="v590">
.nutsRes{background:#1d1638 url(img/nuts_result_bg.webp?v=590) center top/cover no-repeat!important;align-items:flex-end!important;padding:14px 14px max(16px,env(safe-area-inset-bottom))!important}
.nutsRes::before{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(18,10,30,0) 0%,rgba(18,10,30,0) 38%,rgba(18,10,30,.55) 62%,rgba(18,10,30,.8) 100%);pointer-events:none}
.nutsRes .nutsResBox{position:relative;max-height:62vh!important;padding-top:12px!important}
.nutsRes .nrPic{display:none!important}
</style>
"""
rep('</body>', CSS + '</body>')
open(dst, "w", encoding="utf-8").write(s)
print("ok V590")
