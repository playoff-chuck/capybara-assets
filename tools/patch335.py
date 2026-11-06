"""V335 (Martin 06.11. 23:30 «Magnet cool»): Der Magnet fährt am Rand mit dem fallenden Stein mit (immer auf dessen Höhe,
links oder rechts halb über der Spur) und zieht ihn bis an den Rand. Kein «Clank»-Festkleben mehr. Sound folgt nach Martins Wahl."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V334";', 'const GAME_VER = "V335";')
rep('D.mag = { side, xs, y: Math.max(3, Math.min(GT - 4, top - 4)), t: 0, life: 30, pullT: 0 }; }',
    'D.mag = { side, xs, y: Math.max(3, Math.min(GT - 4, top - 4)), fy: S.piece ? S.piece.y : 4, t: 0, life: 30, pullT: 0 }; }')
rep('''      if (p) { let touch = false; for (const [x, y] of p.cells) { const gx = p.x + x, gy = p.y + y; if (m.xs.includes(gx) && gy >= m.y && gy < m.y + 3) touch = true; }
        if (touch) { snd("towerLost"); toast("MAGNET CLANK!", "ALERT", 1400); S.shake = 0.4; lockPiece(); } }''',
'''      if (p) { const cy = p.y + p.cells.reduce((a, c) => a + c[1], 0) / p.cells.length - 1; m.fy += (Math.max(0, Math.min(GH - 3, cy)) - m.fy) * Math.min(1, dt * 5); m.y = Math.round(m.fy); }   /* V335: fährt mit dem Stein mit */''')
rep('const x = m.xs[0] * s, slide = Math.min(1, m.t), off = (1 - slide) * 3 * s * (m.side ? 1 : -1), y = m.y * s + Math.sin(m.t * 3) * s * 0.08,',
    'const x = (m.side ? GW - 1.3 : -0.7) * s, slide = Math.min(1, m.t), off = (1 - slide) * 3 * s * (m.side ? 1 : -1), y = (m.fy != null ? m.fy : m.y) * s + Math.sin(m.t * 3) * s * 0.08,')
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
# Magnet liegt quer: Pole zeigen ins Spielfeld, Rücken halb über der Spur; Feldlinien gehen von den Polen ins Feld
s = open(dst, encoding='utf-8').read()
rep('ctx.save(); ctx.translate(x + off, y); ctx.globalAlpha = 0.92;',
    'ctx.save(); ctx.translate((m.side ? (GW - 0.6) * s : 0.6 * s) + off, y + s); ctx.rotate(m.side ? -Math.PI / 2 : Math.PI / 2); ctx.translate(-w / 2, -h / 2); ctx.globalAlpha = 0.92;')
rep('ctx.arc(m.side ? 0 : w, h * 0.4, r, d > 0 ? -0.6 : Math.PI - 0.6, d > 0 ? 0.6 : Math.PI + 0.6)', 'ctx.arc(w / 2, 0, r, Math.PI + 0.5, Math.PI * 2 - 0.5)')
open(dst, 'w', encoding='utf-8').write(s)
print("ok2")
