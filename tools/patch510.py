#!/usr/bin/env python3
"""V510: Betonmischer neu (Martin 09.11. 16:18): «Vom angetippten Block alles, was damit verbunden ist, bis zu seinem höchsten Punkt.»
- Antippen eines Blocks (oder eines Lochs → der nächste Block daneben/darüber/darunter).
- Block = zusammenhängende gleichfarbige Steine (≈ das gelandete Teil).
- Gefüllt werden alle leeren Felder, die mit diesem Block verbunden sind, von unten bis zur Oberkante des Blocks,
  seitlich höchstens eine Spalte über den Block hinaus. Vorschau (grau + Schalung) zeigt genau das.
Aufruf: python3 tools/patch510.py site/index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V509";', 'const GAME_VER = "V510";')
i = s.find('function mixCells(x, y = GH - 1) {'); j = s.find('function concreteCellGhost', i); assert i > 0 and j > i
s = s[:i] + '''function mixCells(x, y = GH - 1) {   /* V510: angetippter Block + alles Leere, was daran hängt, bis zu seinem höchsten Punkt */
  const p = S.piece, pc = new Set(p ? p.cells.filter(([a, b]) => p.y + b >= 0).map(([a, b]) => vIdx(p.x + a, p.y + b)) : []);
  const filled = c => !!S.grid[c], free = c => !S.grid[c] && !pc.has(c);
  x = Math.max(0, Math.min(GW - 1, x)); y = Math.max(0, Math.min(GH - 1, y));
  // 1) Startblock finden: angetippt, sonst darunter, sonst links/rechts (nächster)
  let seed = -1; const at = (cx, cy) => (cx >= 0 && cx < GW && cy >= 0 && cy < GH && filled(cy * GW + cx)) ? cy * GW + cx : -1;
  if (at(x, y) >= 0) seed = at(x, y);
  else { let best = 1e9; for (const [dx, dy] of [[1, 0], [-1, 0], [0, -1], [0, 1]]) for (let d = 1; d < Math.max(GW, GH); d++) { const n = at(x + dx * d, y + dy * d); if (x + dx * d < 0 || x + dx * d >= GW || y + dy * d < 0 || y + dy * d >= GH) break; if (n >= 0) { if (d < best) { best = d; seed = n; } break; } } }   /* Loch angetippt: nächster Block in den 4 Richtungen */
  if (seed < 0) return [];
  // 2) Block = gleichfarbig zusammenhängend (Beton/TNT: nur die Zelle selbst + gleichartige)
  const col = S.grid[seed], blk = new Set([seed]), q = [seed];
  while (q.length) { const c = q.pop(), cx = c % GW, cy = (c / GW) | 0;
    for (const [dx, dy] of DIRS) { const nx = cx + dx, ny = cy + dy; if (nx < 0 || nx >= GW || ny < 0 || ny >= GH) continue; const n = ny * GW + nx; if (!blk.has(n) && S.grid[n] === col) { blk.add(n); q.push(n); } } }
  let top = GH, x0 = GW, x1 = -1; for (const c of blk) { const cx = c % GW, cy = (c / GW) | 0; top = Math.min(top, cy); x0 = Math.min(x0, cx); x1 = Math.max(x1, cx); }
  x0 = Math.max(0, x0 - 1); x1 = Math.min(GW - 1, x1 + 1);
  // 3) leere Felder, die am Block hängen, flutfüllen – nicht höher als die Block-Oberkante, nicht breiter als Block ±1
  const inBox = (cx, cy) => cx >= x0 && cx <= x1 && cy >= top && cy < GH;
  const seen = new Uint8Array(NN), st = [], cells = [];
  for (const c of blk) { const cx = c % GW, cy = (c / GW) | 0; for (const [dx, dy] of DIRS) { const nx = cx + dx, ny = cy + dy; if (!inBox(nx, ny)) continue; const n = ny * GW + nx; if (!seen[n] && free(n)) { seen[n] = 1; st.push(n); } } }
  while (st.length) { const c = st.pop(), cx = c % GW, cy = (c / GW) | 0; cells.push(c);
    for (const [dx, dy] of DIRS) { const nx = cx + dx, ny = cy + dy; if (!inBox(nx, ny)) continue; const n = ny * GW + nx; if (!seen[n] && free(n)) { seen[n] = 1; st.push(n); } } }
  // 4) nur Felder, die von unten getragen werden (Beton fließt nach unten, schwebt nicht): Spalte muss bis zum Boden/Block gefüllt werden können
  const set = new Set(cells), keep = [];
  for (const c of cells) { let r = ((c / GW) | 0) + 1, ok = true; const cx = c % GW; while (r < GH) { const n = r * GW + cx; if (filled(n)) break; if (!set.has(n)) { ok = false; break; } r++; } if (ok) keep.push(c); }
  keep.sort((a, b) => ((b / GW) | 0) - ((a / GW) | 0) || Math.abs(a % GW - x) - Math.abs(b % GW - x));
  return keep;
}
''' + s[j:]
rep('"Fills a hole up to the top block, buries monsters."', '"Tap a block: fills every gap around it up to its top, buries monsters."', 2)
rep('"MIXER READY · tap a hole"', '"MIXER READY · tap a block"')
rep('toast("TAP A HOLE", "DENIED")', 'toast("NOTHING TO FILL · tap a block with gaps", "DENIED")')
open(p, "w", encoding="utf-8").write(s); print("ok V510")
