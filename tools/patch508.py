#!/usr/bin/env python3
"""V508: Ten-ton – Druckwelle über die ganze Breite beim Aufprall (Sprite img/fx_shockwave.webp, Nano Banana Pro), Martin 09.11. 15:46.
Test: ?test=ton (Welle 9, 2 Ten-tons im Shop). Aufruf: python3 tools/patch508.py site/index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V507";', 'const GAME_VER = "V508";')
rep('''const TON_IMG = new Image(); TON_IMG.src = "img/ton_weight.webp";
function drawTon(s, W) {
  const T0 = S.ton; if (T0 && TON_IMG.complete && TON_IMG.naturalWidth) {''',
    '''const TON_IMG = new Image(); TON_IMG.src = "img/ton_weight.webp";
const SHOCK_IMG = new Image(); SHOCK_IMG.src = "img/fx_shockwave.webp";   /* V508 */
function drawShock(s, W) {   /* V508: Druckwelle läuft vom Aufprall nach links und rechts über die ganze Breite */
  const T = S.ton; if (!T || !T.hit || !SHOCK_IMG.complete || !SHOCK_IMG.naturalWidth) return;
  const th = (T.t || 0) - (T.ht || 0); if (th < 0 || th > 1.0) return;
  const e = 1 - Math.pow(1 - Math.min(1, th / 0.5), 3), ww = W * (0.3 + 1.15 * e), ar = SHOCK_IMG.naturalHeight / SHOCK_IMG.naturalWidth, hh = ww * ar * (0.75 + 0.25 * e);
  const y0 = (T.newTop != null ? T.newTop : T.top) * s, al = th < 0.55 ? 1 : Math.max(0, 1 - (th - 0.55) / 0.45);
  ctx.save(); ctx.globalAlpha = al; ctx.drawImage(SHOCK_IMG, W / 2 - ww / 2, y0 - hh * 0.92, ww, hh);
  if (th < 0.25) { ctx.globalAlpha = (0.25 - th) / 0.25 * 0.55; ctx.fillStyle = "#fff6d8"; ctx.fillRect(0, y0 - s * 0.6, W, s * 0.9); }   // kurzer heller Blitz am Boden
  ctx.restore(); }
function drawTon(s, W) {
  try { drawShock(s, W); } catch (e) {}
  const T0 = S.ton; if (T0 && TON_IMG.complete && TON_IMG.naturalWidth) {''')
rep('const map = { laser: 44,', 'const map = { ton: 9, laser: 44,')
rep('if (q === "elite") {', 'if (q === "ton") { S.tons = (S.tons || 0) + 2; LS.set("capy-tut-ton", "1"); }   /* V508 */\n        if (q === "elite") {')
open(p, "w", encoding="utf-8").write(s); print("ok V508")
