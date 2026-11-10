#!/usr/bin/env python3
# V586 (Martin 11.11. 01:25): Tutorial
# - Abdunkeln bei neuer Aufgabe 5 s statt 3 s; das Bedienfeld unten (Kapsel mit den Knöpfen) bleibt hell
# - Lektion 7 («Monster laufen im Ring»): nicht abdunkeln; der Pfeil aufs Monster verschwindet nach 5 s
# - Lektion «Reihe füllen»: das Spiel schickt Steine, die wirklich eine Reihe schließen (beste Form aus allen
#   Formen/Drehungen/Spalten; wenn keine Reihe schließbar ist: die Form, die die vollste Reihe am weitesten auffüllt)
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V585";', 'const GAME_VER = "V586";')
rep('try { S.tutDimT = performance.now() + 3000; } catch (e) {} t = setTimeout(() => d.classList.remove("on"), 3000); };',
    'try { S.tutDimT = performance.now() + 5000; } catch (e) {} place(); t = setTimeout(() => d.classList.remove("on"), 5000); };   /* V586: 5 s */')
rep('''  let t = null; window.__tutDim = () => {''',
    '''  const place = () => { try { const k = document.querySelector(".deck"), r = k && k.getBoundingClientRect(); d.style.bottom = r && r.height ? Math.max(0, Math.round(innerHeight - r.top)) + "px" : "0px"; } catch (e) {} };   /* V586: Bedienfeld bleibt hell */
  addEventListener("resize", place);
  let t = null; window.__tutDim = () => {''')
# Lektion 3: passende Steine
rep('''function spawnPiece() { S.dropLockUntil = performance.now() + 650;
  S.piece = S.next; S.next = S.next2; S.next2 = makePiece(nextKey());
  S.piece.x = Math.floor(VW() / 2) - (S.piece.k === "I" ? 2 : 1); S.piece.y = 0;''',
'''function tutRowKey() {   /* V586: Stein, der eine Reihe schließt (nur innere Spalten zählen) */
  const W = VW(), H = VH(), occ = new Set(); for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) if (S.grid[vIdx(x, y)]) occ.add(x + "," + y);
  let best = null, bs = -1;
  for (const k of KEYS) { let cells = SHAPES[k].c.map(p => p.slice());
    for (let r = 0; r < 4; r++) { if (r) cells = rotCells(k, cells);
      for (let px = -3; px < W + 3; px++) { if (collide(cells, px, 0)) continue; let py = 0; while (!collide(cells, px, py + 1)) py++;
        const add = new Set(cells.map(([x, y]) => (px + x) + "," + (py + y))), rows = new Set(cells.map(([x, y]) => py + y)); let lines = 0, fill = 0;
        for (const ry of rows) { let n = 0; for (let x = 1; x < W - 1; x++) if (occ.has(x + "," + ry) || add.has(x + "," + ry)) n++; if (n === W - 2) lines++; fill = Math.max(fill, n); }
        const sc = lines * 1000 + fill * 10 + py + Math.random(); if (sc > bs) { bs = sc; best = { k, cells: cells.map(c => c.slice()), px }; } } } }
  return best; }
function spawnPiece() { S.dropLockUntil = performance.now() + 650;
  S.piece = S.next; S.next = S.next2; S.next2 = makePiece(nextKey());
  S.piece.x = Math.floor(VW() / 2) - (S.piece.k === "I" ? 2 : 1); S.piece.y = 0;
  try { if (TUT.on && TUT_STEPS[TUT.step] && /FILL A ROW/.test(TUT_STEPS[TUT.step].t) && !S.rotMode) { const b = tutRowKey(); if (b) { S.piece = makePiece(b.k); S.piece.tnt = -1; S.piece.cells = b.cells; S.piece.x = b.px; } } } catch (e) {}   /* V586: gleich passend gedreht über der Lücke */''')
rep('    if (vis && TUT.step !== last) { last = TUT.step; window.__tutDim(); } }, 150);',
    '    if (vis && TUT.step !== last) { last = TUT.step; if ((TUT_STEPS[TUT.step] || {}).ar !== "ring") window.__tutDim(); } }, 150);   /* V586: Lektion 7 ohne Abdunkeln */')
rep('        if (k === 5) { const bd = document.getElementById("board"); if (!bd) return null;',
    '        if (k === 5) { if ((TUT.t || 0) >= 5) return null;   /* V586: Pfeil aufs Monster nach 5 s weg */ const bd = document.getElementById("board"); if (!bd) return null;')
open(dst, "w", encoding="utf-8").write(s)
print("ok V586")
