#!/usr/bin/env python3
# V588 (Martin 11.11. 01:45): Tutorial Lektion 1–2 – jeder neue Stein kommt seitlich versetzt dort,
# wo er am tiefsten liegt und die unterste offene Reihe am meisten füllt (nicht auf den vorigen Stein),
# damit die Reihe in Lektion 3 leicht zu schließen ist. Form und Drehung bleiben (Drehen übt man selbst). Nie in die Monster-Spur am Rand.
# + (01:46) Streifen: statt des eckigen Generals der Coach (rundes Bild, kein grüner Hintergrund); die Sprechblase steht ruhig
#   (feste Position unter dem Streifen, keine Wackel-Animation) und ihr Zipfel zeigt auf den Coach
# + (01:47) Kein Abdunkeln, solange Laden/Turm-Menü offen ist (geht sofort weg, wenn es aufgeht)
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V587";', 'const GAME_VER = "V588";')
rep('  try { if (TUT.on && TUT_STEPS[TUT.step] && /FILL A ROW/.test(TUT_STEPS[TUT.step].t) && !S.rotMode) {',
'''  try { if (TUT.on && TUT_STEPS[TUT.step] && /DROP A BLOCK|TURN YOUR BLOCKS/.test(TUT_STEPS[TUT.step].t) && !S.rotMode) {   /* V588: Stein versetzt, flach in die unterste Reihe */
    const W = VW(), H = VH(), p = S.piece, filled = y => { let n = 0; for (let x = 1; x < W - 1; x++) if (S.grid[vIdx(x, y)]) n++; return n; };
    let bx = p.x, bs = -1e9; for (let px = -3; px < W + 3; px++) { if (collide(p.cells, px, 0)) continue; let py = 0; while (!collide(p.cells, px, py + 1)) py++;
      const inner = p.cells.every(([x]) => px + x >= 1 && px + x <= W - 2); if (!inner) continue; let low = 0; for (const [x, y] of p.cells) low = Math.max(low, py + y);
      const sc = py * 100 + (inner ? 60 : 0) + filled(low) * 5 + Math.random(); if (sc > bs) { bs = sc; bx = px; } }
    p.x = bx; } } catch (e) {}
  try { if (TUT.on && TUT_STEPS[TUT.step] && /FILL A ROW/.test(TUT_STEPS[TUT.step].t) && !S.rotMode) {''')
rep("bar.querySelector(\".tbLogo\").style.backgroundImage = 'url(\"' + ((lg && lg.src) || \"icons/icon-192.png\") + '\")';",
    "bar.querySelector(\".tbLogo\").style.backgroundImage = 'url(\"' + COACH_IMG() + '\")';   /* V588: Coach statt General */")
CSS = """<style id="v588">
#tutBar .tbLogo{border-radius:50%!important;background-color:transparent!important;background-size:cover!important;border-color:#3a2414!important}
body.tutBarOn #coach.genTalk .coachCard{left:8px!important;width:calc(100vw - 16px)!important;max-width:520px!important;top:calc(var(--tbH,86px) + 12px)!important;animation:none!important;transition:none!important}
body.tutBarOn #coach.genTalk{animation:none!important}
</style>
"""
rep('</body>', CSS + '</body>')
rep('  let last = -1; setInterval(() => { const on = typeof TUT !== "undefined" && TUT.on; if (!on) {',
    '  let last = -1; setInterval(() => { const on = typeof TUT !== "undefined" && TUT.on; const sh = document.getElementById("sheet"), shopUp = !!(S && (S.shop || S.sel)) || !!(sh && !sh.hidden);\n'
    '    if (on && shopUp) { if (d.classList.contains("on")) { clearTimeout(t); d.classList.remove("on"); } try { S.tutDimT = 0; } catch (e) {} last = TUT.step; return; }   /* V588: im Laden nie dunkel */\n'
    '    if (!on) {')
open(dst, "w", encoding="utf-8").write(s)
print("ok V588")
