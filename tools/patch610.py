#!/usr/bin/env python3
# V610 (Martin 11.11. 11:27): Lektion 2 «Block drehen» – nie den quadratischen O-Block (sieht gedreht gleich aus).
# Aufruf: patch610.py <site-Ordner>
import sys, os
p = os.path.join(sys.argv[1], "index.html"); s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V609";', 'const GAME_VER = "V610";')
rep('S.piece.x = Math.floor(VW() / 2) - (S.piece.k === "I" ? 2 : 1); S.piece.y = 0;',
    'S.piece.x = Math.floor(VW() / 2) - (S.piece.k === "I" ? 2 : 1); S.piece.y = 0;\n  try { if (TUT.on && TUT_STEPS[TUT.step] && TUT_STEPS[TUT.step].rot && S.piece.k === "O") { S.piece = makePiece(["T", "L", "J", "S", "Z"][Math.floor(Math.random() * 5)]); S.piece.x = Math.floor(VW() / 2) - 1; S.piece.y = 0; } } catch (e) {}   /* V610: Drehen-Lektion ohne O-Block */')
rep('if (st.rot) { TUT.rb = TUT.rot || 0;',
    'if (st.rot) { try { if (S.piece && S.piece.k === "O") { S.piece = makePiece("T"); S.piece.x = Math.floor(VW() / 2) - 1; S.piece.y = 0; } if (S.next && S.next.k === "O") S.next = makePiece("L"); } catch (e) {}   /* V610 */ TUT.rb = TUT.rot || 0;')
open(p, "w", encoding="utf-8").write(s); print("ok V610")
