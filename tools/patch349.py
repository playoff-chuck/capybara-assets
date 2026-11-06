"""V349 (Martin 07.11. 00:12): Easter Eggs neu gestaltet – Afrika, Asien, Nordamerika, Antarktis neue Motive mit eigener Farbpalette,
Mosaik-Steine jetzt glatt glänzend (kein Camo), Südamerika-Herz in den neuen Farben.
Auslöser strenger: 5× SCHNELL hintereinander gegen den Rand (jeder Stoß höchstens 0,45 s nach dem vorigen)."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V348";', 'const GAME_VER = "V349";')
# schnell hintereinander
rep('if (wall) { if (push.dir !== dx || push.piece !== S.pieceNo) push = { n: 0, dir: dx, piece: S.pieceNo }; push.n++;',
    'if (wall) { const nowP = performance.now(); if (push.dir !== dx || push.piece !== S.pieceNo || nowP - (push.t || 0) > 450) push = { n: 0, dir: dx, piece: S.pieceNo }; push.t = nowP; push.n++;')
# neue Motive
i = s.find('  const EGG = ['); j = s.find('];', i) + 2; assert 0 < i < j
EGG = r'''  /* V349: Palette – a Himmelblau, b Blau, c Eisblau, g Grün, G Dunkelgrün, y Gelb, o Orange, r Rot, p Rosa, n Braun, N Dunkelbraun,
     t Capybara, T Capybara dunkel, s Sand, w Weiß, k Schwarz */
  const EGG = [
    { k: "samerica", m: ["gggggggggg", "ggrrggrrgg", "grrrrrrrrg", "grrprrrrrg", "grrrrrrrrg", "ggrrrrrrgg", "gggrrrrggg", "ggggrrgggg", "gggggggggg", "ggyggggygg", "gGgggGgggG", "GGGGGGGGGG"], gap: [[4, 2], [4, 3], [4, 4], [4, 5]] },
    { k: "africa", m: ["yyyyyyyyyy", "yTTyyyyTTy", "oottttttoo", "otkttttkto", "otttttttto", "ottTTTTtto", "ottTkkTtto", "oottttttoo", "sssttttsss", "ssttttttss", "GsttttttsG", "GGGGGGGGGG"], gap: [[3, 4], [4, 4], [5, 4], [6, 4]] },
    { k: "asia", m: ["apaaaaaapa", "aaaGGGGaap", "aaGggggGaa", "aGgggyggGa", "GGGGGGGGGG", "aTttttttTa", "atkttttkta", "attTTTTtta", "attTkkTtta", "aattttttaa", "abbbbbbbba", "bbbbbbbbbb"], gap: [[3, 4], [4, 4], [5, 4], [6, 4]] },
    { k: "namerica", m: ["aaaaGaaaaa", "aaaGgGaaya", "aaGgGgGaaa", "aaaGgGaaaa", "aaGgGgGaaa", "aGgGgGgGaa", "aaaGnGaaaa", "aaGgnGGaaa", "aGgGngGGaa", "aaaanaaaaa", "ggggnggggg", "GGGGNGGGGG"], gap: [[4, 7], [4, 8], [4, 9], [4, 10]] },
    { k: "antarctica", m: ["cccccccccc", "cccckkcccc", "ccckkkkccc", "cckwkkwkcc", "cckkookkcc", "ckkwwwwkkc", "kkwwwwwwkk", "kkwwwwwwkk", "ckwwwwwwkc", "cckwwwwkcc", "cccoocoocc", "wwwwwwwwww"], gap: [[4, 5], [4, 6], [4, 7], [4, 8]] } ];
  const EGG_COL = { a: "#7ec8f0", b: "#2f62a8", c: "#c4ecfa", g: "#6cc04a", G: "#2f7a35", y: "#ffd23f", o: "#f39a2e", r: "#e2473a", p: "#f59ac2", n: "#8a5a2b", N: "#5a3a1c", t: "#c07f45", T: "#7d4a22", s: "#e9c98a", w: "#f6f3ec", k: "#22222a" };'''
s = s[:i] + EGG + s[j:]
rep('+E.m[y][x]', 'E.m[y][x]')
rep('gv = +E.m[gy][gx]', 'gv = E.m[gy][gx]')
# glatte, glänzende Mosaik-Steine statt Camo
i = s.find('function tile(x, y, v, a = 1, sc = 1) {'); j = s.find('g.globalAlpha = 1; }', i) + len('g.globalAlpha = 1; }'); assert 0 < i < j
TILE = r'''function tile(x, y, v, a = 1, sc = 1) { const s2 = CW * sc, px = x * CW + (CW - s2) / 2, py = y * CW + (CW - s2) / 2, e = Math.max(1, s2 * 0.12), col = EGG_COL[v] || "#888";
      g.globalAlpha = a; g.fillStyle = col; g.fillRect(px, py, s2, s2);
      const gl = g.createLinearGradient(px, py, px + s2, py + s2); gl.addColorStop(0, "rgba(255,255,255,.28)"); gl.addColorStop(0.5, "rgba(255,255,255,0)"); gl.addColorStop(1, "rgba(0,0,0,.18)"); g.fillStyle = gl; g.fillRect(px, py, s2, s2);
      g.fillStyle = "rgba(255,255,255,.30)"; g.fillRect(px, py, s2, e * 0.8); g.fillRect(px, py, e * 0.8, s2);
      g.fillStyle = "rgba(0,0,0,.30)"; g.fillRect(px, py + s2 - e * 0.8, s2, e * 0.8); g.fillRect(px + s2 - e * 0.8, py, e * 0.8, s2);
      g.strokeStyle = "rgba(10,10,14,.7)"; g.lineWidth = Math.max(1, s2 * 0.04); g.strokeRect(px + 0.5, py + 0.5, s2 - 1, s2 - 1); g.globalAlpha = 1; }'''
s = s[:i] + TILE + s[j:]
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
