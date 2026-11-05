"""V287 (Martin 17:15): Betonmischer – Randstreifen (Spalte ganz links/rechts) und Hauptfeld sind ein zusammenhängender Hohlraum.
Ein Klick füllt alle verbundenen freien Felder (bis zur obersten Steinreihe), egal ob er im Randstreifen oder im Hauptfeld beginnt."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V286";', 'const GAME_VER = "V287";')
rep('''  if (x === 0 || x === GW - 1) { for (let yy = top; yy < GH; yy++) { const c = yy * GW + x; if (free(c)) cells.push(c); } }
  else {
    let sy''', '''  {
    let sy''')
rep('if (nx < 1 || nx > GW - 2 || ny < top || ny >= GH) continue;', 'if (nx < 0 || nx > GW - 1 || ny < top || ny >= GH) continue;')
rep('function startMix(x, y = GH - 1) {', 'window.__mixCells = (x, y) => mixCells(x, y);\nfunction startMix(x, y = GH - 1) {')
open(dst, 'w', encoding='utf-8').write(s)
