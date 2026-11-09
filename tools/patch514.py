#!/usr/bin/env python3
"""V514 (Martin 09.11. 16:37):
- Betonmischer: Man tippt in eine Lücke. Links und rechts davon stehen Wände (Blöcke). Gefüllt wird alles, was mit der Lücke zusammenhängt,
  zwischen den beiden Wänden bis zum höchsten Punkt der Wände. Fehlt eine Wand (Feldrand), zählt die andere.
- Menü «CONTINUE NUTS»: zeigt das nächste Level (geschafft + 1).
Aufruf: python3 tools/patch514.py site/index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V513";', 'const GAME_VER = "V514";')
i = s.find('function mixCells(x, y = GH - 1) {'); j = s.find('function concreteCellGhost', i); assert i > 0 and j > i
s = s[:i] + '''function mixCells(x, y = GH - 1) {   /* V514: Lücke zwischen zwei Wänden bis zum höchsten Punkt der Wände füllen */
  const p = S.piece, pc = new Set(p ? p.cells.filter(([a, b]) => p.y + b >= 0).map(([a, b]) => vIdx(p.x + a, p.y + b)) : []);
  const filled = (cx, cy) => cx >= 0 && cx < GW && cy >= 0 && cy < GH && !!S.grid[cy * GW + cx];
  const free = (cx, cy) => cx >= 0 && cx < GW && cy >= 0 && cy < GH && !S.grid[cy * GW + cx] && !pc.has(cy * GW + cx);
  x = Math.max(0, Math.min(GW - 1, x)); y = Math.max(0, Math.min(GH - 1, y));
  while (y > 0 && filled(x, y)) y--;   // auf einen Block getippt → Lücke darüber
  if (!free(x, y)) return [];
  let r0 = y; while (r0 + 1 < GH && free(x, r0 + 1)) r0++;   // Boden der Lücke
  // Wände links/rechts auf Höhe des Lückenbodens, dann wie hoch sie hinaufreichen (zusammenhängend)
  const wall = (dir, row) => { let cx = x + dir; while (cx >= 0 && cx < GW && free(cx, row)) cx += dir; if (cx < 0 || cx >= GW || !filled(cx, row)) return null;
    let t = row; while (t > 0 && filled(cx, t - 1)) t--; return { x: cx, top: t }; };
  let L = null, R = null; for (let row = y; row <= r0 && !L && !R; row++) { L = wall(-1, row); R = wall(1, row); }   // von der angetippten Höhe abwärts die ersten Wände
  if (!L && !R) return [];
  const level = Math.min(L ? L.top : GH, R ? R.top : GH), x0 = L ? L.x + 1 : 0, x1 = R ? R.x - 1 : GW - 1;
  if (level > r0) return [];
  // alles Leere, was mit der Lücke zusammenhängt, zwischen den Wänden, bis zur Höhe des höchsten Wandpunkts
  const seen = new Uint8Array(NN), st = [r0 * GW + x], cells = []; seen[st[0]] = 1;
  while (st.length) { const c = st.pop(), cx = c % GW, cy = (c / GW) | 0; cells.push(c);
    for (const [dx, dy] of DIRS) { const nx = cx + dx, ny = cy + dy; if (nx < x0 || nx > x1 || ny < level || ny >= GH || !free(nx, ny)) continue; const n = ny * GW + nx; if (!seen[n]) { seen[n] = 1; st.push(n); } } }
  // Beton schwebt nicht: nur Felder, unter denen bis zum Boden/Block alles mitgefüllt wird
  const set = new Set(cells), keep = [];
  for (const c of cells) { const cx = c % GW; let r = ((c / GW) | 0) + 1, ok = true; while (r < GH) { if (filled(cx, r)) break; if (!set.has(r * GW + cx)) { ok = false; break; } r++; } if (ok) keep.push(c); }
  keep.sort((a, b) => ((b / GW) | 0) - ((a / GW) | 0) || Math.abs(a % GW - x) - Math.abs(b % GW - x));
  return keep;
}
''' + s[j:]
rep('"Tap a block: fills every gap around it up to its top, buries monsters."', '"Tap a gap: fills it between the walls up to their highest point, buries monsters."', 2)
rep('"MIXER READY · tap a block"', '"MIXER READY · tap a gap"')
rep('toast("NOTHING TO FILL · tap a block with gaps", "DENIED")', 'toast("NOTHING TO FILL · tap a gap between blocks", "DENIED")')
rep('return `${nzWord(S.nuts.c)} · level ${Math.max(1, S.nuts.lvl || 1)} of ${NZ_MAX}`;', 'return `${nzWord(S.nuts.c)} · level ${Math.min(NZ_MAX, (S.nuts.cleared || 0) + 1)} of ${NZ_MAX}`;')
rep('return `${nzWord(d.nuts.c)} · level ${Math.max(1, d.nuts.lvl || 1)} of ${NZ_MAX}`; }', 'return `${nzWord(d.nuts.c)} · level ${Math.min(NZ_MAX, (d.nuts.cleared || 0) + 1)} of ${NZ_MAX}`; }')
rep('toast(`BACK IN THE NUTS · ${nzWord(S.nuts.c)} · level ${Math.max(1, S.nuts.lvl || 1)}`', 'toast(`BACK IN THE NUTS · ${nzWord(S.nuts.c)} · level ${Math.min(NZ_MAX, (S.nuts.cleared || 0) + 1)}`')
open(p, "w", encoding="utf-8").write(s); print("ok V514")
