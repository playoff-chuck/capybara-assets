#!/usr/bin/env python3
# V606 (Martin 11.11. 08:30): «Bei Karte gibt es noch Rauschen – entfernen.» Das war das Luftrauschen (Propeller-Wind) beim Kartenflug;
# es wird nicht mehr ausgegeben (Motorbrummen und Landung bleiben).
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V605";', 'const GAME_VER = "V606";')
rep('ns.connect(bp); bp.connect(ng); ng.connect(out);', 'ns.connect(bp); bp.connect(ng);   /* V606: Luftrauschen beim Kartenflug aus (nicht mehr an out) */')
open(dst, "w", encoding="utf-8").write(s)
print("ok", dst)
