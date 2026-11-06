"""V338 (Martin 06.11. 23:38): Easter Egg erst nach 5× gegen die Wand (statt 3×); Mosaik-Steine genau so groß wie die Steine im Spielfeld
(Fenster passt sich an), gleiche Camo-Muster und Kanten wie im Spielfeld. Tesla zerstört den Magneten. Magnet-Brummen hörbar gemacht: Grundton 100 Hz statt 50 Hz (Handy-Lautsprecher geben 50 Hz kaum wieder),
mehr Obertöne, lauter (0,05 → 0,14)."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V337";', 'const GAME_VER = "V338";')
rep('if (push.n >= 3) {', 'if (push.n >= 5) {')
rep('const E = EGG[Math.max(0, Math.min(EGG.length - 1, ci))], ov = $("ovEgg"), cvE = $("eggCv"), g = cvE.getContext("2d");',
    'const E = EGG[Math.max(0, Math.min(EGG.length - 1, ci))], ov = $("ovEgg"), cvE = $("eggCv"), g = cvE.getContext("2d");\n    { const cr = cv.getBoundingClientRect(), cc = Math.max(14, Math.min(cr.width, cr.height * GW / GH) / GW || 30); cvE.style.width = Math.round(cc * 10) + "px"; cvE.style.height = Math.round(cc * 12) + "px"; }   /* V338: Steine so groß wie im Spielfeld */')
rep("  function hitArea(x0, y0, w, h, label) {\n    let hit = false;", """  function hitArea(x0, y0, w, h, label) {
    let hit = false;
    if (label === "tesla" && D.mag) { const m = D.mag, mx0 = m.side ? GW - 2 : 0, my0 = Math.round(m.fy != null ? m.fy : m.y);   /* V338: Tesla zerstört den Magneten */
      if (mx0 < x0 + w && mx0 + 2 > x0 && my0 < y0 + h && my0 + 3 > y0) { D.mag = null; if (window.__magHum) window.__magHum(0); fxText(mx0 + 1, my0 + 1, "MAGNET FRIED!", "#ffb3a8"); toast("MAGNET FRIED!", "HQ", 1600); hit = true; } }""")
rep('mag: ["MAGNET!", "It pulls the blocks – steer against it"]', 'mag: ["MAGNET!", "It pulls the blocks – steer against it · Tesla fries it"]')
rep('PUSH 3× INTO WALL', 'PUSH 5× INTO WALL')
rep('push a block 3× into the left or right wall', 'push a block 5× into the left or right wall')
rep('[[50, 1], [100, 0.5], [150, 0.33], [250, 0.2], [350, 0.14]]', '[[100, 1], [200, 0.7], [300, 0.5], [400, 0.3], [500, 0.22], [700, 0.12]]')
rep('hum.g.gain.setTargetAtTime(on ? 0.05 : 0,', 'hum.g.gain.setTargetAtTime(on ? 0.14 : 0,')
open(dst, 'w', encoding='utf-8').write(s)
# Mosaik-Steine wie im Spielfeld: gleiche Auflösung (CELL) und gleiche Camo-Muster/Kanten wie block()
i = s.find('  function openEgg(ci) {'); j = s.find('  window.__egg = c =>', i); assert 0 < i < j
f = s[i:j]
f = f.replace('const CW = 40,', 'const CW = Math.max(12, Math.round(CELL)), EW = CW * 10, EH = CW * 12,', 1)
f = f.replace('order = [...Array(120)', 'o0 = (cvE.width = EW, cvE.height = EH), order = [...Array(120)', 1)
import re
f = re.sub(r'\b400\b', 'EW', f); f = re.sub(r'\b480\b', 'EH', f)
f = f.replace("""function tile(x, y, v, a = 1, sc = 1) { const [c1, c2] = tileCol(v), px = x * CW, py = y * CW, pad = 2 + (1 - sc) * CW / 2;
      g.globalAlpha = a; g.fillStyle = c2; g.fillRect(px + pad, py + pad, CW - 2 * pad, CW - 2 * pad);
      g.fillStyle = c1; g.fillRect(px + pad + 3, py + pad + 3, CW - 2 * pad - 6, CW - 2 * pad - 7);
      g.fillStyle = "rgba(255,255,255,.22)"; g.fillRect(px + pad + 3, py + pad + 3, CW - 2 * pad - 6, 4); g.globalAlpha = 1; }""",
"""function tile(x, y, v, a = 1, sc = 1) { const s2 = CW * sc, px = x * CW + (CW - s2) / 2, py = y * CW + (CW - s2) / 2, e = Math.max(1, s2 * 0.12);
      g.globalAlpha = a; let fill = null; try { fill = v === 8 ? "#d8d2c0" : (patterns[v - 1] || tileCol(v)[0]); } catch (er) { fill = tileCol(v)[0]; }
      g.fillStyle = fill; g.fillRect(px, py, s2, s2);
      g.fillStyle = "rgba(255,248,220,.22)"; g.fillRect(px, py, s2, e); g.fillRect(px, py, e, s2);
      g.fillStyle = "rgba(0,0,0,.38)"; g.fillRect(px, py + s2 - e, s2, e); g.fillRect(px + s2 - e, py, e, s2);
      g.strokeStyle = "rgba(10,14,8,.8)"; g.lineWidth = Math.max(1, s2 * 0.04); g.strokeRect(px + 0.5, py + 0.5, s2 - 1, s2 - 1); g.globalAlpha = 1; }""", 1)
assert 'patterns[v - 1]' in f and 'EW = CW * 10' in f
s = s[:i] + f + s[j:]
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
