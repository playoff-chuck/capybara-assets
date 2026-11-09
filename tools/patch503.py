#!/usr/bin/env python3
"""V503: LASER SHOW (W44) feiner (Martin 09.11. 15:05):
- Laser endet weich (1,5 s Überblendung), sobald Welle 44 geschafft ist – vor der 90°-Challenge (Sidewinder II, W45); weicher Einstieg 0,8 s.
- Ring (Monsterweg) als Laser: Außen- und Innenkante leuchten rot, Ring abgedunkelt.
- Hintergrund: dunkles Höhlenbild wie in Nuts + rote Lichtkegel (Nuts-Disco-Strahlen, nur rot).
Aufruf: python3 tools/patch503.py site/index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V502";', 'const GAME_VER = "V503";')

# Zustand + Überblendung
rep('function laserOn() { return !!(S && S.started && !S.over && !S.nuts && LASER_WAVES[S.wave]); }\nconst LZ = { fakes: [], t0: 0, next: 0, ann: -1 };',
    '''const LZ = { fakes: [], t0: 0, next: 0, ann: -1, w: -1, seen: false, end: 0, st: 0, k: 0 };
function laserK() {   /* 0 = aus, 1 = voll; weich rein (0,8 s) und raus (1,5 s, sobald die Welle geschafft ist) */
  let k = 0;
  if (S && S.started && !S.over && !S.nuts && LASER_WAVES[S.wave]) { const n = performance.now();
    if (LZ.w !== S.wave) { LZ.w = S.wave; LZ.seen = false; LZ.end = 0; LZ.st = n; }
    if (S.inWave) LZ.seen = true; else if (LZ.seen && !LZ.end) LZ.end = n;
    k = Math.min(1, (n - LZ.st) / 800); if (LZ.end) k = Math.min(k, Math.max(0, 1 - (n - LZ.end) / 1500)); }
  else if (LZ.k > 0 && S && S.started && !S.over && !S.nuts) { const n = performance.now(); if (!LZ.end) LZ.end = n; k = Math.min(LZ.k, Math.max(0, 1 - (n - LZ.end) / 1500)); if (!k) LZ.w = -1; }   /* Welle schon weitergezählt: trotzdem weich ausblenden */
  else LZ.w = -1;
  LZ.k = k; const on = k > 0.02; if (document.body.classList.contains("inLaser") !== on) document.body.classList.toggle("inLaser", on); return k; }
function laserOn() { return laserK() > 0.02; }''')

# Alpha in lzStroke
rep('function lzStroke(loops, s, ox, oy, t, al) {   /* rotes Lauflicht entlang der Kontur */\n  ctx.save(); ctx.globalAlpha = al;',
    'function lzStroke(loops, s, ox, oy, t, al) {   /* rotes Lauflicht entlang der Kontur */\n  ctx.save(); ctx.globalAlpha = al * LZ.k;')
# keine neuen falschen Laser beim Ausblenden
rep('if (run && LZ.fakes.length < 3 && t >= LZ.next) {', 'if (run && !LZ.end && LZ.fakes.length < 3 && t >= LZ.next) {')

# Blöcke: überblenden + Ring als Laser
rep('  if (laserOn()) { try { laserStack(s); } catch (e) {} } else   /* V502 */\n  for (let y = 0; y < GH; y++) for (let x = 0; x < GW; x++) { const v = S.grid[y * GW + x]; if (v === TNT) tntCell(x, y); else if (v === CONCRETE) concreteCell(x, y); else if (v) block(x, y, v - 1); }',
    '  const lzk = laserK(); if (lzk > 0.02) { try { laserRing(s); laserStack(s); } catch (e) {} }   /* V502/V503 */\n  if (lzk < 1) { ctx.save(); ctx.globalAlpha = 1 - lzk;\n  for (let y = 0; y < GH; y++) for (let x = 0; x < GW; x++) { const v = S.grid[y * GW + x]; if (v === TNT) tntCell(x, y); else if (v === CONCRETE) concreteCell(x, y); else if (v) block(x, y, v - 1); }\n  ctx.restore(); }')
# aktives Teil: überblenden
rep('  if (laserOn()) { try { laserDraw(p, s); } catch (e) {} }   /* V502 */\n  else if (p && S.started && !S.over) {',
    '  const lzk2 = LZ.k; if (lzk2 > 0.02) { try { laserDraw(p, s); } catch (e) {} }   /* V502/V503 */\n  if (lzk2 < 1 && p && S.started && !S.over) { ctx.save(); ctx.globalAlpha = 1 - lzk2;')
rep('block(a, b, p.col); } });\n  }\n  // Reichweite', 'block(a, b, p.col); } });\n  ctx.restore(); }\n  // Reichweite')

rep('function laserStack(s) {', '''function laserRing(s) {   /* V503: Monsterweg als Laser-Ring */
  ctx.save(); ctx.globalAlpha = 0.5 * LZ.k; ctx.fillStyle = "#0b0204";
  ctx.fillRect(0, 0, GW * s, s); ctx.fillRect(0, (GH - 1) * s, GW * s, s); ctx.fillRect(0, s, s, (GH - 2) * s); ctx.fillRect((GW - 1) * s, s, s, (GH - 2) * s); ctx.restore();
  const t = performance.now() / 1000;
  lzStroke([[[0, 0], [GW, 0], [GW, GH], [0, GH]]], s, 0, 0, t * 0.8, 0.85);
  lzStroke([[[1, 1], [1, GH - 1], [GW - 1, GH - 1], [GW - 1, 1]]], s, 0, 0, t * 0.8, 0.85); }
function laserStack(s) {''')

# Hintergrund: Nuts-Höhlenbild + Nuts-Licht
rep('  const nb = live && S.nuts ? NUTS_BG[S.nuts.c | 0] : null;   /* V473 */\n  const P = wherePos(live ? S.wave || 1 : 1), D = live ? (S.nuts ? (nb ? NUTS_DI : NUTS_D) : DAY[P.d]) : DAY[1];\n  const key = P.cont[0] + "|" + P.p + "|" + (live ? (S.nuts ? "nuts" + (nb ? "i" : "") : P.d) : "menu");',
    '  const lzb = live && !S.nuts && typeof laserK === "function" && laserK() > 0.5;   /* V503: Laser-Show-Hintergrund */\n  const nb = live && S.nuts ? NUTS_BG[S.nuts.c | 0] : lzb ? NUTS_BG[Math.min(3, wherePos(S.wave || 1).c)] : null;   /* V473 */\n  const P = wherePos(live ? S.wave || 1 : 1), D = live ? (S.nuts || lzb ? (nb ? NUTS_DI : NUTS_D) : DAY[P.d]) : DAY[1];\n  const key = P.cont[0] + "|" + P.p + "|" + (live ? (S.nuts ? "nuts" + (nb ? "i" : "") : lzb ? "laser" : P.d) : "menu");')
rep('    if (!document.body.classList.contains("inNuts")) return;\n    if (!el) mk();',
    '    if (!document.body.classList.contains("inNuts") && !document.body.classList.contains("inLaser")) return;\n    if (!el) mk();')
rep('#nzDisco{position:fixed;inset:0;pointer-events:none;z-index:39;display:none;overflow:hidden}',
    '#nzDisco{position:fixed;inset:0;pointer-events:none;z-index:39;display:none;overflow:hidden}\nbody.inLaser #nzDisco{display:block}body.inLaser:not(.inNuts) #nzDisco>:not(.nzBeam){display:none}body.inLaser:not(.inNuts) #nzDisco .nzBeam.b2{background:linear-gradient(180deg,rgba(255,30,30,.28),rgba(255,30,30,.08) 70%,rgba(255,30,30,0))}')
open(p, "w", encoding="utf-8").write(s); print("ok V503")
