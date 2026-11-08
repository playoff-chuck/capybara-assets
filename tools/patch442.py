#!/usr/bin/env python3
"""V442: Reichweiten-Vorschau nachgebessert (Martin 08.11. 11:57):
- Turm-Menü öffnet unten, wenn der Turm in der oberen Bildhälfte steht (sonst oben wie bisher) → der Turm ist nie verdeckt
- beim Halten verschwindet das Menü ganz (opacity 0)
- Zone schöner: weicher Farbverlauf in Waffenfarbe, leuchtender Rand, leichtes Pulsieren
Nutzung: python3 tools/patch442.py src dst"""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()

def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (c, a[:80])
    s = s.replace(a, b)

rep('GAME_VER = "V441"', 'GAME_VER = "V442"')
rep('.sheet{transition:opacity .18s}.sheet.peek{opacity:.14}', '.sheet{transition:opacity .18s}.sheet.peek{opacity:0}')
rep('body:has(#sheet:not([hidden])) #sheet{max-height:calc(100dvh - 66px - env(safe-area-inset-top,0px))!important;bottom:auto!important}',
    'body:has(#sheet:not([hidden])) #sheet{max-height:calc(100dvh - 66px - env(safe-area-inset-top,0px))!important;bottom:auto!important}\n'
    'body:has(#sheet:not([hidden])) #sheet.atBottom{top:auto!important;bottom:0!important;border-radius:22px 22px 0 0}   /* V442: Menü unten, wenn der Turm oben steht */')
rep('function openSheet(t) { S.shop = false; S.sel = t; renderSheet(); $("sheet").hidden = false; }',
    'function openSheet(t) { S.shop = false; S.sel = t; renderSheet(); $("sheet").hidden = false; try { const p = cvPt(t.x + 0.5, t.y + 0.5); $("sheet").classList.toggle("atBottom", p.y < innerHeight * 0.52); } catch (e) {} }   /* V442 */')
rep('''      ctx.fillStyle = `rgba(${rgb},${pk ? .18 : .1})`; ctx.strokeStyle = `rgba(${rgb},${pk ? .95 : .7})`; ctx.lineWidth = (pk ? 3 : 1.5) * DPR; if (pk) ctx.setLineDash([9 * DPR, 7 * DPR]);
      ctx.beginPath(); ctx.arc(C(S.sel.x), C(S.sel.y), r * s, 0, 7); ctx.fill(); ctx.stroke(); ctx.setLineDash([]);''',
'''      const rr = r * s * (pk ? 1 + 0.012 * Math.sin(performance.now() / 260) : 1), cx0 = C(S.sel.x), cy0 = C(S.sel.y);   /* V442: weiche Zone, leuchtender Rand, Pulsieren */
      if (pk) { const g = ctx.createRadialGradient(cx0, cy0, rr * 0.15, cx0, cy0, rr); g.addColorStop(0, `rgba(${rgb},.06)`); g.addColorStop(0.75, `rgba(${rgb},.16)`); g.addColorStop(1, `rgba(${rgb},.42)`); ctx.fillStyle = g; } else ctx.fillStyle = `rgba(${rgb},.1)`;
      ctx.beginPath(); ctx.arc(cx0, cy0, rr, 0, 7); ctx.fill();
      if (pk) { ctx.lineWidth = 12 * DPR; ctx.strokeStyle = `rgba(${rgb},.16)`; ctx.stroke(); ctx.lineWidth = 3 * DPR; ctx.strokeStyle = `rgba(${rgb},.95)`; ctx.stroke(); ctx.lineWidth = 1 * DPR; ctx.strokeStyle = "rgba(255,255,255,.55)"; ctx.stroke(); }
      else { ctx.strokeStyle = `rgba(${rgb},.7)`; ctx.lineWidth = 1.5 * DPR; ctx.stroke(); }''')
rep('ty = C(S.sel.y) - r * s - 8 * DPR;', 'ty0 = C(S.sel.y) - rr - 10 * DPR, ty = ty0 < 18 * DPR ? C(S.sel.y) + rr + 20 * DPR : ty0;')
open(dst, "w", encoding="utf-8").write(s)
print("ok", dst)
