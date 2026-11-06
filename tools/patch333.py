"""V333 (Martin 06.11. 23:23 «Bildausfall-Version ganz cool, vielleicht noch feiner»): Rauschen im Bildausfall feiner –
Körnung ca. 2 px statt ~4×16 px, passt sich der Spielfeldgröße an, leicht bläuliches Flimmern, feinere Zeilen. Martin 23:24: Rauschen-Ton −30 % (0,05 → 0,035)."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V332";', 'const GAME_VER = "V333";')
rep('if (now - nT > 60) { nT = now; const id = nx.createImageData(nc.width, nc.height);',
    'if (now - nT > 50) { nT = now; const fw = Math.max(64, Math.round(cv.width / 2)), fh = Math.max(16, Math.round(b.n * CELL / 2)); if (nc.width !== fw || nc.height !== fh) { nc.width = fw; nc.height = fh; } const id = nx.createImageData(nc.width, nc.height);')
rep('id.data[i] = id.data[i + 1] = id.data[i + 2] = v; id.data[i + 3] = 255; }',
    'id.data[i] = v; id.data[i + 1] = v; id.data[i + 2] = Math.min(255, v + 18); id.data[i + 3] = 255; }')
rep('ctx.fillStyle = "rgba(0,0,0,.18)"; for (let y = b.r0 * CELL; y < (b.r0 + b.n) * CELL; y += 4) ctx.fillRect(0, y, cv.width, 2);',
    'ctx.fillStyle = "rgba(0,0,0,.14)"; for (let y = b.r0 * CELL; y < (b.r0 + b.n) * CELL; y += 3) ctx.fillRect(0, y, cv.width, 1);')
rep('noiseLevel(inside ? 0.05 : 0);', 'noiseLevel(inside ? 0.035 : 0);')
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
