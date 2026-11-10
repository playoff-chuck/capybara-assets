#!/usr/bin/env python3
# V582 (Martin 11.11. 01:09): Admin bleibt – «Street player» (Dev-Knopf) löscht den Admin-Schlüssel nicht mehr.
# Die Geräte-ID wird weiter neu erzeugt (neuer Spieler für die Statistik), der Schlüssel capy-adm bleibt und gilt weiter.
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V581";', 'const GAME_VER = "V582";')
rep('try { const keep = ["tarnturm-dev"]; const ks = [];', 'try { const keep = ["tarnturm-dev", "capy-adm"]; const ks = [];   /* V582: Admin-Schlüssel bleibt */')
open(dst, "w", encoding="utf-8").write(s)
print("ok V582")
