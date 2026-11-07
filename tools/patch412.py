#!/usr/bin/env python3
# V412 (Martin 07.11. 22:00): Kontinent-Karte – Pfeil «→» im Knopf «NEXT: …» weg (er brach in eine eigene Zeile um), Inhalt vertikal mittig; beide Knöpfe gleich.
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:80])
    s = s.replace(a, b)
rep('const GAME_VER = "V411";', 'const GAME_VER = "V412";')
rep('<button id="signNext">NEXT →<small>continue the tour</small></button>', '<button id="signNext">NEXT<small>continue the tour</small></button>')
rep('$("signNext").innerHTML = `NEXT: ${NZ_NEXT[c]} →<small>continue the tour</small>`;', '$("signNext").innerHTML = `NEXT: ${NZ_NEXT[c]}<small>continue the tour</small>`;')
rep('.signBtns button{flex:1;min-height:64px;', '.signBtns button{flex:1;min-height:64px;line-height:1.05;gap:2px;')
open(dst, "w", encoding="utf-8").write(s)
print("ok")
