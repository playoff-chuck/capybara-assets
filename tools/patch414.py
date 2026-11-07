#!/usr/bin/env python3
# V414 (Martin 07.11. 22:10): Beton füllt nur bis zum höchsten Punkt des Blocks, an dem man füllt – also bis zur Oberkante
# des zusammenhängenden Blockstücks direkt neben dem Loch (links/rechts in der Tipp-Reihe; bei zwei Wänden die niedrigere, damit nichts überläuft). Gebilde darüber (nach einer Lücke)
# und höhere Blöcke weiter weg werden ignoriert. Vorher: höchste Kante in den 3 Spalten ums Loch.
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:80])
    s = s.replace(a, b)
rep('const GAME_VER = "V413";', 'const GAME_VER = "V414";')
rep("""  if (top === GH) top = GH - 1;
  const p = S.piece, pc = new Set(p ? p.cells.filter(([a, b]) => p.y + b >= 0).map(([a, b]) => vIdx(p.x + a, p.y + b)) : []);
  const free = c => !S.grid[c] && !pc.has(c);
  let cells = [];
  {
    let sy = Math.max(y, top); while (sy < GH && !free(sy * GW + x)) sy++;
    if (sy < GH) {""",
"""  if (top === GH) top = GH - 1;
  const p = S.piece, pc = new Set(p ? p.cells.filter(([a, b]) => p.y + b >= 0).map(([a, b]) => vIdx(p.x + a, p.y + b)) : []);
  const free = c => !S.grid[c] && !pc.has(c);
  let cells = [];
  {
    let sy = Math.max(y, top); while (sy < GH && !free(sy * GW + x)) sy++;
    /* V414: Höhe = Oberkante des Blockstücks direkt neben dem Loch (zusammenhängend nach oben), nicht die 3-Spalten-Höhe */
    if (sy < GH) { let lv = -1; for (const nx of [x - 1, x + 1]) { if (nx < 0 || nx > GW - 1 || !S.grid[sy * GW + nx]) continue; let r = sy; while (r > 0 && S.grid[(r - 1) * GW + nx]) r--; lv = Math.max(lv, r); }   /* niedrigere Wand = kein Überlaufen */
      if (lv < 0) { for (let r = sy + 1; r < GH; r++) if (S.grid[r * GW + x]) { lv = r; break; } }   /* kein Nachbar: nur bis zum Boden unter dem Loch */
      if (lv >= 0) top = Math.max(top, lv); }
    if (sy < GH) {""")
open(dst, "w", encoding="utf-8").write(s)
print("ok")
