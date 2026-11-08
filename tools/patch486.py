#!/usr/bin/env python3
"""V486: Tutorial-Sicherheitsnetz. Seit V483 fallen die Blöcke im Tutorial weiter; ein neuer Spieler, der die
Schritte langsam liest, bekam nach ~58 s «TOWER FULL» (Game over vor Welle 1, Playwright-Test Dauer-Arbeiter d-1942).
Jetzt: Erreicht der Stapel im Tutorial die Decke, wird er wie vom Ten-ton zusammengedrückt (tonCompress) statt Game over.
Aufruf: python3 tools/patch486.py site/index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V485";', 'const GAME_VER = "V486";')
rep('if (collide(S.piece.cells, S.piece.x, S.piece.y) && !(S.rotMode && findEntry(S.piece))) gameOver("The stack hit the ceiling.");',
    'if (collide(S.piece.cells, S.piece.x, S.piece.y) && !(S.rotMode && findEntry(S.piece))) { if (TUT.on) { for (let k = 0; k < 3 && collide(S.piece.cells, S.piece.x, S.piece.y); k++) tonCompress(); snd("tonFall"); }   /* V486: im Tutorial kein Game over – Stapel wird zusammengedrückt */\n    if (collide(S.piece.cells, S.piece.x, S.piece.y)) gameOver("The stack hit the ceiling."); }')
open(p, "w", encoding="utf-8").write(s); print("ok V486")
