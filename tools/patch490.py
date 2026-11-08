#!/usr/bin/env python3
"""V490: t143 Sichtbare Effekte je Outfit (Martin 08.11. 23:06 «Outfit-Effekte – zeigen», Kommentar «Bau die und zeige sie mir»).
Reine Optik, 0 $, kein Balancing: dezente Partikel je Outfit (max. 14 gleichzeitig), nicht in Nuts (Disco-Outfit).
Auslöser: s = bei jedem Splat, r = bei jeder vollen Reihe, t = Spur hinter dem fallenden Block.
Squad File zeigt unter jedem Outfit den Effekt. Test-Link ?fx=1…9 (zieht für diese Sitzung Outfit + Effekt an, speichert nichts).
Aufruf: python3 tools/patch490.py site/index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)

rep('const GAME_VER = "V489";', 'const GAME_VER = "V490";')

# 1) Tabelle + Auswahl
rep('function outfitName(k, n) {',
'''const OUTFIT_FX_B = [null, ["s", "gold", "Golden splats"], ["r", "leaf", "Leaf confetti"], ["s", "frost", "Frost glitter"], ["t", "star", "Star trail"]];   /* V490 (t143): Effekt je Outfit · s = Splat, r = volle Reihe, t = Spur */
const OUTFIT_FX = { blue: OUTFIT_FX_B.concat([["s", "glitter", "Pop glitter"], ["r", "note", "Rock notes"], ["r", "goldrain", "Gold rain"], ["s", "bubble", "Sea bubbles"], ["t", "comet", "Comet trail"]]),
  rosie: OUTFIT_FX_B.concat([["s", "golddust", "Gold dust"], ["s", "heart", "Diva hearts"], ["r", "pinkstar", "Princess sparkles"], ["r", "flash", "Star flashes"], ["t", "fairy", "Fairy dust"]]) };
const FX_FORCE = (() => { try { const v = +new URLSearchParams(location.search).get("fx"); return v >= 1 && v <= 9 ? v : null; } catch (e) { return null; } })();   /* V490: Test-Link ?fx=1…9 */
function outfitName(k, n) {''')
rep('function outfitSel(k) { try {', 'function outfitSel(k) { if (FX_FORCE != null) return FX_FORCE; try {')
rep('const HERO_IMG = { get blue()',
'''function outfitFx() { try { if (heroDisco()) return null; const k = heroKey(); return OUTFIT_FX[k][outfitSel(k)] || null; } catch (e) { return null; } }   /* V490 */
const OFX_COL = { gold: ["#ffd84a", "#fff3b0", "#f0b52a"], leaf: ["#7cbf4a", "#4f8f2a", "#e8a33a", "#c9662a"], frost: ["#ffffff", "#cdeeff", "#8fd3ff"], star: ["#ffd84a", "#fff3b0", "#ffb83a"],
  glitter: ["#ff6fb5", "#ffd84a", "#6fd3ff", "#a6f06f", "#c39bff"], note: ["#ffd84a", "#ff6fb5", "#ffffff"], goldrain: ["#ffd84a", "#f2b630", "#fff3b0"], bubble: ["#dff4ff", "#ffffff", "#9fd8ff"],
  comet: ["#9fd8ff", "#ffffff", "#c9b6ff"], golddust: ["#ffd84a", "#fff3b0", "#e8c06a"], heart: ["#ff6fb5", "#ff9ccc", "#ffd1e6"], pinkstar: ["#ff9ccc", "#ffffff", "#ffd84a"], flash: ["#ffffff", "#fff3b0", "#ffe58a"], fairy: ["#ff9ccc", "#c39bff", "#ffffff"] };
const OFX_SH = { gold: "spark", leaf: "leaf", frost: "flake", star: "star", glitter: "dot", note: "note", goldrain: "spark", bubble: "bubble", comet: "dot", golddust: "dot", heart: "heart", pinkstar: "spark", flash: "spark", fairy: "spark" };
function ofxAdd(st, x, y, n, mode) {   /* V490: höchstens 14 Outfit-Partikel gleichzeitig */
  let have = 0; for (const f of S.fx) if (f.type === "ofx") have++;
  const cols = OFX_COL[st] || OFX_COL.gold, sh = OFX_SH[st] || "spark";
  for (let i = 0; i < n && have < 14; i++, have++) {
    const a = Math.random() * 6.283, v = mode === "t" ? 0.4 + Math.random() * 0.6 : 1.6 + Math.random() * 2.6;
    let vx = Math.cos(a) * v, vy = Math.sin(a) * v - (mode === "t" ? 0 : 1.6), g = 3.2;
    if (sh === "bubble" || sh === "note") { g = -2.4; vy = -1 - Math.random() * 1.4; vx *= 0.5; }
    else if (sh === "leaf") { g = 1.6; vy = -2.5 - Math.random() * 2; }
    else if (st === "goldrain") { g = 4; vy = -3 - Math.random() * 2; }
    else if (mode === "t") { g = 0.6; vy = -0.5 - Math.random() * 0.5; }
    S.fx.push({ type: "ofx", sh, col: cols[Math.floor(Math.random() * cols.length)], x: x + (Math.random() - 0.5) * 0.6, y: y + (Math.random() - 0.5) * 0.4, vx, vy, g, rot: Math.random() * 6.283, vr: (Math.random() - 0.5) * 6,
      sz: (sh === "dot" ? 0.12 : st === "flash" ? 0.26 : 0.17) * (0.8 + Math.random() * 0.5), ph: Math.random() * 6.283, t: 0, life: mode === "t" ? 0.55 + Math.random() * 0.3 : 0.8 + Math.random() * 0.5 });
  }
}
function ofxStep(dt) {   /* V490: Auslöser + Bewegung der Outfit-Partikel */
  const e = outfitFx();
  if (e) for (const f of S.fx) {
    if (f.ofx || f.t < 0) continue;
    if (e[0] === "s" && f.type === "splat") { f.ofx = 1; ofxAdd(e[1], f.x, f.y, 4, "s"); }
    else if (e[0] === "r" && f.type === "rowflash") { f.ofx = 1; for (let i = 0; i < 3; i++) ofxAdd(e[1], 1 + Math.random() * (GW - 2), f.y, 2, "r"); }
  }
  if (e && e[0] === "t" && S.piece && !frozen() && !S.ton && !S.nuts) { S._ofxT = (S._ofxT || 0) + dt;
    if (S._ofxT > 0.11) { S._ofxT = 0; const c = S.piece.cells[Math.floor(Math.random() * S.piece.cells.length)]; if (c) ofxAdd(e[1], S.piece.x + c[0], S.piece.y + c[1] - 0.3, 1, "t"); } }
  for (const f of S.fx) { if (f.type !== "ofx" || f.t < 0) continue; f.vy += f.g * dt; f.vx *= (1 - 1.2 * dt); f.x += (f.vx + (f.sh === "leaf" || f.sh === "bubble" ? Math.sin(f.t * 5 + f.ph) * 0.8 : 0)) * dt; f.y += f.vy * dt; f.rot += f.vr * dt; }
}
function drawOfx(f, k, s) {   /* V490 */
  const z = s * f.sz * (f.sh === "spark" ? 0.75 + 0.35 * Math.sin(f.t * 14 + f.ph) : 1);
  ctx.save(); ctx.globalAlpha = Math.min(1, k * 2.2); ctx.translate(C(f.x), C(f.y)); ctx.rotate(f.rot); ctx.fillStyle = f.col; ctx.strokeStyle = f.col; ctx.lineCap = "round";
  if (f.sh === "spark") { ctx.beginPath(); ctx.moveTo(0, -z * 2); ctx.quadraticCurveTo(0, 0, z * 2, 0); ctx.quadraticCurveTo(0, 0, 0, z * 2); ctx.quadraticCurveTo(0, 0, -z * 2, 0); ctx.quadraticCurveTo(0, 0, 0, -z * 2); ctx.fill(); }
  else if (f.sh === "star") { ctx.beginPath(); for (let i = 0; i < 10; i++) { const r = i % 2 ? z * 0.6 : z * 1.5, a = i * Math.PI / 5; ctx.lineTo(Math.sin(a) * r, -Math.cos(a) * r); } ctx.closePath(); ctx.fill(); }
  else if (f.sh === "dot") { ctx.globalAlpha *= 0.35; ctx.beginPath(); ctx.arc(0, 0, z * 2.2, 0, 7); ctx.fill(); ctx.globalAlpha = Math.min(1, k * 2.2); ctx.beginPath(); ctx.arc(0, 0, z, 0, 7); ctx.fill(); }
  else if (f.sh === "leaf") { ctx.beginPath(); ctx.ellipse(0, 0, z * 1.5, z * 0.7, 0, 0, 7); ctx.fill(); ctx.globalAlpha *= 0.5; ctx.strokeStyle = "#2c4416"; ctx.lineWidth = Math.max(1, z * 0.18); ctx.beginPath(); ctx.moveTo(-z * 1.3, 0); ctx.lineTo(z * 1.3, 0); ctx.stroke(); }
  else if (f.sh === "flake") { ctx.lineWidth = Math.max(1, z * 0.35); ctx.beginPath(); for (let i = 0; i < 3; i++) { const a = i * Math.PI / 3; ctx.moveTo(Math.cos(a) * z * 1.5, Math.sin(a) * z * 1.5); ctx.lineTo(-Math.cos(a) * z * 1.5, -Math.sin(a) * z * 1.5); } ctx.stroke(); }
  else if (f.sh === "note") { ctx.rotate(-f.rot); ctx.beginPath(); ctx.ellipse(-z * 0.4, z * 0.9, z * 0.7, z * 0.5, -0.4, 0, 7); ctx.fill(); ctx.lineWidth = Math.max(1, z * 0.3); ctx.beginPath(); ctx.moveTo(z * 0.25, z * 0.8); ctx.lineTo(z * 0.25, -z * 1.4); ctx.lineTo(z * 1.1, -z * 0.9); ctx.stroke(); }
  else if (f.sh === "bubble") { ctx.lineWidth = Math.max(1, z * 0.25); ctx.beginPath(); ctx.arc(0, 0, z * 1.2, 0, 7); ctx.stroke(); ctx.globalAlpha *= 0.8; ctx.beginPath(); ctx.arc(-z * 0.4, -z * 0.4, z * 0.3, 0, 7); ctx.fill(); }
  else if (f.sh === "heart") { ctx.rotate(-f.rot * 0.8); ctx.beginPath(); ctx.moveTo(0, z * 1.2); ctx.bezierCurveTo(-z * 1.8, 0, -z * 0.9, -z * 1.3, 0, -z * 0.4); ctx.bezierCurveTo(z * 0.9, -z * 1.3, z * 1.8, 0, 0, z * 1.2); ctx.fill(); }
  ctx.restore();
}
window.__ofx = { fx: outfitFx, add: ofxAdd };
const HERO_IMG = { get blue()''')

# 2) Update-Schleife
rep('''    else if (f.type === "smoke") { f.vy *= (1 - 0.35 * dt); f.x += (f.vx + Math.sin(f.t * 1.7 + f.ph) * 0.6) * dt; f.y += f.vy * dt; f.r += f.grow * dt; }
  }
  SFX.music.setPaused(''', '''    else if (f.type === "smoke") { f.vy *= (1 - 0.35 * dt); f.x += (f.vx + Math.sin(f.t * 1.7 + f.ph) * 0.6) * dt; f.y += f.vy * dt; f.r += f.grow * dt; }
  }
  try { ofxStep(dt); } catch (e) {}   /* V490: Outfit-Effekte */
  SFX.music.setPaused(''')

# 3) Zeichnen
rep('''    else if (f.type === "splat") {
      ctx.globalAlpha = Math.min(1, k * 1.6); ctx.fillStyle = f.col;''', '''    else if (f.type === "ofx") drawOfx(f, k, s);   /* V490 */
    else if (f.type === "splat") {
      ctx.globalAlpha = Math.min(1, k * 1.6); ctx.fillStyle = f.col;''')

# 4) Squad File: Effekt unter dem Outfit
rep('''<small>${on ? (n === sel ? "wearing" : "tap to wear") : outfitLabel(o)}</small></div>`; }).join("")''',
    '''<small>${on ? (n === sel ? "wearing" : "tap to wear") : outfitLabel(o)}</small><b class="ofFx${n ? "" : " no"}">${n ? OUTFIT_FX[k][n][2] : "no effect"}</b></div>`; }).join("")''')
rep('.ofRow .mcCard small{font-size:8px}', '.ofRow .mcCard small{font-size:8px}.ofRow .mcCard b.ofFx{display:block;font:700 7px/1.15 "Baloo 2",sans-serif;color:#b8561a;margin-top:1px;min-height:16px}.ofRow .mcCard b.ofFx.no{color:#a89a85;font-weight:600}.ofRow .mcCard.off b.ofFx{color:#a89a85}')

open(p, "w", encoding="utf-8").write(s); print("ok V490")
