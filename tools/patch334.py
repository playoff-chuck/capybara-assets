"""V334 (Martin 06.11. 23:27 «Unkraut ist cool»): Unkraut wächst weiter, auch wenn Steine darauf liegen –
es schiebt die Steine (samt Türmen) in seiner Spalte nach oben. Wächst 30 % schneller (alle 11,5 s statt 15 s), max. 12 Felder.
Stoppt nur, wenn die Spalte bis oben voll ist oder der fallende Stein im Weg ist."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V333";', 'const GAME_VER = "V334";')
rep('if (S.inWave) w.growT += dt; if (w.growT >= 15 && w.h < 8) { w.growT = 0; const ny = w.root - w.h; let free = ny >= 1 && !S.grid[ny * GW + w.x]; if (free && p) for (const [x, y] of p.cells) if (p.x + x === w.x && p.y + y === ny) free = false; if (free) w.h++; }',
    'if (S.inWave) w.growT += dt; if (w.growT >= 11.5 && w.h < 12) { w.growT = 0; const ny = w.root - w.h; if (ny >= 1 && weedPush(w.x, ny, p)) w.h++; }')
rep('  function landY(x) {', '''  // V334: Unkraut schiebt die Steine darüber eine Reihe hoch (Türme wandern mit)
  function weedPush(x, ny, p) {
    let top = ny; while (top >= 0 && S.grid[top * GW + x]) top--;
    if (top < 1) return false;
    if (p) for (const [cx, cy] of p.cells) if (p.x + cx === x && p.y + cy >= top && p.y + cy <= ny) return false;
    if (top === ny) return true;
    for (let y = top; y < ny; y++) { const from = (y + 1) * GW + x, to = y * GW + x; S.grid[to] = S.grid[from];
      const t = S.towers.get(from); if (t) { S.towers.delete(from); t.y = y; S.towers.set(to, t); } }
    S.grid[ny * GW + x] = 0; snd("move"); gridChanged(); return true; }
  function landY(x) {''')
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
