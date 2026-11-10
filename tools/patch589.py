#!/usr/bin/env python3
# V589 (Martin 11.11. 01:51, Screenshot): Fehler – der fallende Block wurde im Tutorial über den Laden/das Turm-Menü gezeichnet.
# Die Block-Kopie über Karte/Streifen ist jetzt aus, solange Laden oder Turm-Menü offen sind (und der Einflug pausiert nicht das Spiel dort).
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V588";', 'const GAME_VER = "V589";')
rep('coach && !coach.hidden && !cv.classList.contains("rot") && !cv.classList.contains("rotR") && !S.rotMode;',
    'coach && !coach.hidden && !cv.classList.contains("rot") && !cv.classList.contains("rotR") && !S.rotMode && !S.shop && !S.sel && (() => { const sh = document.getElementById("sheet"); return !sh || sh.hidden; })();   /* V589: nie über dem Laden */')
open(dst, "w", encoding="utf-8").write(s)
print("ok V589")
