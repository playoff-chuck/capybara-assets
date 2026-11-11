#!/usr/bin/env python3
# V628 (Martin 11.11. 13:46):
# 1) Diplom: beim Start der Fanfare läuft keine Stimme mehr (laufende Ansage wird ausgeblendet, bis zum Diplom-Spruch keine neue).
# 2) Tutorial «Monster plätten»: jeder neue Stein erscheint auf der rechtesten Spur (schmal gedreht), dort wo die Monster herunterkommen.
import sys, os
site = sys.argv[1]; p = os.path.join(site, "index.html"); s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V627";', 'const GAME_VER = "V628";')
rep('get voiceBusy() { return !!curVoice; }',
    'voiceCut() { if (!curVoice) return; try { const cv = curVoice, n = ac.currentTime; if (cv.__g) { cv.__g.gain.cancelScheduledValues(n); cv.__g.gain.setValueAtTime(cv.__g.gain.value, n); cv.__g.gain.linearRampToValueAtTime(0, n + 0.12); cv.stop(n + 0.13); } else cv.stop(); } catch (e) {} curVoice = null; },   /* V628 */\n    get voiceBusy() { return !!curVoice; }')
rep('  if (SFX.muted || SFX.vol === 0) return;\n  try { const fa = new Audio("sfx/fanfare.mp3?v=623");',
    '  try { SFX.voiceCut && SFX.voiceCut(); } catch (e) {}   /* V628: keine Stimme unter der Fanfare */\n  if (SFX.muted || SFX.vol === 0) return;\n  try { const fa = new Audio("sfx/fanfare.mp3?v=623");')
rep('if (TUT.on && !window.__tutKeys.has(k)) return;', 'if (TUT.on && !window.__tutKeys.has(k)) return; if (window.__tutSumOpen && k !== "cert_done") return;   /* V628: Diplom ohne andere Stimmen */')
rep('const b = tutSplatPlace(); if (b) { S.piece = makePiece(b.k); S.piece.tnt = -1; S.piece.cells = b.cells; S.piece.x = b.px; S.piece.__auto = S.piece.x + "," + JSON.stringify(S.piece.cells); } } }',
    '''const p0 = S.piece; let cells = p0.cells.map(c => c.slice()); for (let r = 0; r < 4; r++) { const xs = cells.map(c => c[0]); if (Math.max(...xs) - Math.min(...xs) <= 1) break; cells = rotCells(p0.k, cells); }   /* V628: immer rechteste Spur, schmal */
      const W = VW(); let bx = -99; for (let px = -3; px < W + 3; px++) { if (collide(cells, px, 0)) continue; if (!cells.every(([x]) => px + x >= 1 && px + x <= W - 1)) continue; if (px > bx) bx = px; }
      if (bx > -99) { p0.cells = cells; p0.x = bx; p0.tnt = -1; } } }''')
open(p, "w", encoding="utf-8").write(s)
print("ok V628")
