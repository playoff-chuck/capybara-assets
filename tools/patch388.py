"""V388: Sniper zeigt beim Schuss das Fadenkreuz am Ziel (0,75 s) – wie der Tesla mit seinem 4×4-Rahmen (Martin, 07.11.).
Aufruf: python3 tools/patch388.py site/index.html site/index.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
m = re.search(r'const GAME_VER = "V(\d+)";', s); old = int(m.group(1)); NEW = old + 1
rep(f'const GAME_VER = "V{old}";', f'const GAME_VER = "V{NEW}";')
rep('''  S.fx.push({ type: "flash", t: 0, life: 0.12 });
  S.fx.push({ type: "tracer", x1: GW + 2, y1: -3,''',
    '''  S.fx.push({ type: "sbox", x, y, t: 0, life: 0.75 });   /* V%d: Fadenkreuz beim Schuss, wie Tesla */
  S.fx.push({ type: "flash", t: 0, life: 0.12 });
  S.fx.push({ type: "tracer", x1: GW + 2, y1: -3,''' % NEW)
rep('''    else if (f.type === "ebox") {''',
    '''    else if (f.type === "sbox") { ctx.globalAlpha = k * 0.95; const cx = (f.x + 1) * s, cy = (f.y + 1) * s, R = s * (1.6 - 0.3 * (1 - k));
      ctx.fillStyle = "rgba(224,74,46,.28)"; ctx.fillRect(f.x * s, f.y * s, 2 * s, 2 * s); ctx.strokeStyle = "#e04a2e"; ctx.lineWidth = Math.max(1.5, s * 0.1); ctx.strokeRect(f.x * s + 1, f.y * s + 1, 2 * s - 2, 2 * s - 2);
      ctx.beginPath(); ctx.arc(cx, cy, R, 0, 7); ctx.stroke(); ctx.beginPath(); ctx.moveTo(cx - R * 1.3, cy); ctx.lineTo(cx - R * 0.5, cy); ctx.moveTo(cx + R * 0.5, cy); ctx.lineTo(cx + R * 1.3, cy); ctx.moveTo(cx, cy - R * 1.3); ctx.lineTo(cx, cy - R * 0.5); ctx.moveTo(cx, cy + R * 0.5); ctx.lineTo(cx, cy + R * 1.3); ctx.stroke(); }
    else if (f.type === "ebox") {''')
open(dst, 'w', encoding='utf-8').write(s); print("ok V%d" % NEW)
