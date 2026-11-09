#!/usr/bin/env python3
"""V502: Sonderwelle «LASER SHOW» in Welle 44 (ruhige Welle, Martin 09.11. 14:51):
- Der fallende Stein ist durchsichtig, nur eine laserrote Kontur läuft im Kreis um ihn herum (Lauflicht). Kein Landeschatten.
- Bis zu 3 falsche Laser-Steine zischen gleichzeitig durchs Bild und verwirren.
- Liegende Blöcke bleiben normal. Test: ?test=laser
Aufruf: python3 tools/patch502.py site/index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V501";', 'const GAME_VER = "V502";')

# Zeichnen: aktives Teil im Laser-Modus
rep('''  // Geist + aktives Teil
  const p = S.piece;
  if (p && S.started && !S.over) {''',
    '''  // Geist + aktives Teil
  const p = S.piece;
  if (laserOn()) { try { laserDraw(p, s); } catch (e) {} }   /* V502 */
  else if (p && S.started && !S.over) {''')

rep('function v2g(u, v) {',
    '''/* ===== V502: LASER SHOW (Welle 44) ===== */
const LASER_WAVES = { 44: 1 };
function laserOn() { return !!(S && S.started && !S.over && !S.nuts && LASER_WAVES[S.wave]); }
const LZ = { fakes: [], t0: 0, next: 0, ann: -1 };
function lzLoop(cells) {   /* Umriss einer Zellmenge als geschlossene Punktfolge (im Uhrzeigersinn) */
  const set = new Set(cells.map(([a, b]) => a + "," + b)), E = new Map();
  const add = (x1, y1, x2, y2) => E.set(x1 + "," + y1, [x2, y2]);
  for (const [a, b] of cells) {
    if (!set.has(a + "," + (b - 1))) add(a, b, a + 1, b);
    if (!set.has((a + 1) + "," + b)) add(a + 1, b, a + 1, b + 1);
    if (!set.has(a + "," + (b + 1))) add(a + 1, b + 1, a, b + 1);
    if (!set.has((a - 1) + "," + b)) add(a, b + 1, a, b); }
  const loops = [], seen = new Set();
  for (const k of E.keys()) { if (seen.has(k)) continue; const L = []; let cur = k, guard = 0;
    while (!seen.has(cur) && guard++ < 200) { seen.add(cur); const [x, y] = cur.split(",").map(Number); L.push([x, y]); const n = E.get(cur); if (!n) break; cur = n[0] + "," + n[1]; }
    loops.push(L); }
  return loops; }
function lzStroke(loops, s, ox, oy, t, al) {   /* rotes Lauflicht entlang der Kontur */
  ctx.save(); ctx.globalAlpha = al; ctx.lineJoin = "round"; ctx.lineCap = "round";
  for (const L of loops) { ctx.beginPath(); L.forEach(([x, y], i) => { const px = ox + x * s, py = oy + y * s; if (i) ctx.lineTo(px, py); else ctx.moveTo(px, py); }); ctx.closePath();
    ctx.setLineDash([]); ctx.shadowColor = "#ff1a1a"; ctx.shadowBlur = s * 0.45; ctx.strokeStyle = "rgba(255,40,40,.35)"; ctx.lineWidth = s * 0.2; ctx.stroke();
    ctx.shadowBlur = s * 0.25; ctx.setLineDash([s * 0.42, s * 0.22]); ctx.lineDashOffset = -t * s * 3.2; ctx.strokeStyle = "#ff2a2a"; ctx.lineWidth = s * 0.13; ctx.stroke();
    ctx.shadowBlur = 0; ctx.strokeStyle = "rgba(255,225,225,.9)"; ctx.lineWidth = s * 0.04; ctx.stroke(); }
  ctx.restore(); }
function laserDraw(p, s) {
  const now = performance.now() / 1000; if (!LZ.t0) LZ.t0 = now; const t = now - LZ.t0, dt = Math.min(0.05, now - (LZ.last || now)); LZ.last = now;
  if (LZ.ann !== S.wave) { LZ.ann = S.wave; LZ.fakes = []; LZ.next = t + 2.5; try { announce("LASER SHOW", "Only the red outline shows your block · watch out for fake lasers", "SPECIAL", 2600); } catch (e) {} }
  // echter Stein: nur Kontur
  if (p) { const cells = []; p.cells.forEach(([x, y]) => { if (p.y + y >= 0) cells.push(v2g(p.x + x, p.y + y)); }); if (cells.length) lzStroke(lzLoop(cells), s, 0, 0, t, 1); }
  // falsche Laser: höchstens 3, nur wenn das Spiel läuft
  const run = !frozen();
  if (run && LZ.fakes.length < 3 && t >= LZ.next) {
    const k = KEYS[(Math.random() * KEYS.length) | 0], c = SHAPES[k].c.map(([a, b]) => [a, b]), mode = Math.random();
    let f; if (mode < 0.45) f = { x: Math.random() * (GW - 3), y: -2, vx: (Math.random() - 0.5) * 1.5, vy: 7 + Math.random() * 5 };
    else if (mode < 0.8) { const l = Math.random() < 0.5; f = { x: l ? -3 : GW, y: 1 + Math.random() * (GH - 5), vx: (l ? 1 : -1) * (8 + Math.random() * 5), vy: (Math.random() - 0.5) * 2 }; }
    else { f = { x: Math.random() * (GW - 3), y: Math.random() * (GH * 0.6), vx: 0, vy: 1.2 + Math.random() * 1.5, blink: 1 }; }
    f.loops = lzLoop(c); f.age = 0; f.life = f.blink ? 1.4 : 2.6; LZ.fakes.push(f); LZ.next = t + 0.9 + Math.random() * 1.6; }
  for (const f of LZ.fakes) { if (run) { f.age += dt; f.x += f.vx * dt; f.y += f.vy * dt; }
    const al = Math.min(1, f.age * 4, (f.life - f.age) * 3) * (f.blink ? 0.75 + 0.25 * Math.sin(f.age * 25) : 0.9);
    lzStroke(f.loops, s, f.x * s, f.y * s, t + f.age, Math.max(0, al)); }
  LZ.fakes = LZ.fakes.filter(f => f.age < f.life && f.x > -5 && f.x < GW + 5 && f.y < GH + 3); }
window.__laser = { on: () => laserOn(), get n() { return LZ.fakes.length; } };
function v2g(u, v) {''')

# Liegende Blöcke als laserrote Skyline (Martin 14:52)
rep('  // Blöcke\n  for (let y = 0; y < GH; y++) for (let x = 0; x < GW; x++) { const v = S.grid[y * GW + x]; if (v === TNT) tntCell(x, y); else if (v === CONCRETE) concreteCell(x, y); else if (v) block(x, y, v - 1); }',
    '  // Blöcke\n  if (laserOn()) { try { laserStack(s); } catch (e) {} } else   /* V502 */\n  for (let y = 0; y < GH; y++) for (let x = 0; x < GW; x++) { const v = S.grid[y * GW + x]; if (v === TNT) tntCell(x, y); else if (v === CONCRETE) concreteCell(x, y); else if (v) block(x, y, v - 1); }')
rep('window.__laser = { on:', '''function laserStack(s) {   /* liegende Blöcke: nur rote Skyline-Kontur, ganz leicht gefüllt */
  const cells = []; for (let y = 0; y < GH; y++) for (let x = 0; x < GW; x++) if (S.grid[y * GW + x]) cells.push([x, y]);
  if (!cells.length) return; ctx.save(); ctx.fillStyle = "rgba(120,10,10,.10)"; for (const [x, y] of cells) ctx.fillRect(x * s, y * s, s, s); ctx.restore();
  const t = performance.now() / 1000; lzStroke(lzLoop(cells), s, 0, 0, t * 0.6, 0.95); }
window.__laser = { on:''')

# Testlink
rep('const map = { blk: 65, mag: 80,', 'const map = { laser: 44, blk: 65, mag: 80,')
open(p, "w", encoding="utf-8").write(s); print("ok V502")
