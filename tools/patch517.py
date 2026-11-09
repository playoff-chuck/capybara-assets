#!/usr/bin/env python3
"""V517: Druckwelle weich statt ruckelig (Martin 09.11. 16:46): kein Zittern/Pulsieren mehr, durchgehende Überblendung der 4 Phasen
(Summe immer 100 %), weiches Wachsen in die Breite, am Ende flacht die Welle zu einem feinen Strich ab und verblasst. Kein harter Blitz.
Aufruf: python3 tools/patch517.py site/index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V516";', 'const GAME_VER = "V517";')
i = s.find('function shkFrame(f, cx, gy, w, al) {'); j = s.find('function drawTon(s, W) {', i); assert i > 0 and j > i
s = s[:i] + '''function shkFrame(f, cx, gy, w, al, sy = 1) {   /* Phase f (0–3), Breite w, Bodenlinie gy, vertikale Stauchung sy */
  if (al <= 0.005) return; const k = w / SHK.cw, h = SHK.ch * k * sy;
  ctx.globalAlpha = Math.min(1, al); ctx.drawImage(SHOCK_IMG, f * SHK.cw, 0, SHK.cw, SHK.ch, cx - w / 2, gy - SHK.by * k * sy, w, h); }
const smooth = x => { x = Math.max(0, Math.min(1, x)); return x * x * (3 - 2 * x); }, eOut = x => { x = Math.max(0, Math.min(1, x)); return 1 - Math.pow(1 - x, 3); };
function drawShock(s, W) {   /* V517: weiche Luftdruck-Welle */
  const T = S.ton; if (!T || !SHOCK_IMG.complete || !SHOCK_IMG.naturalWidth) return;
  const cx = W / 2; ctx.save(); ctx.globalCompositeOperation = "screen";
  if (!T.hit) {   // Druck baut sich ruhig unter dem Gewicht auf
    const tgt = Math.max(1, T.top - 3 + 5), prog = smooth((T.y + 5) / tgt), gy = (T.y + 3.25) * s, w = W * (0.3 + 0.4 * prog);
    ctx.translate(0, gy * 2); ctx.scale(1, -1);
    shkFrame(0, cx, gy, w, (0.15 + 0.4 * prog) * (1 - smooth((prog - 0.6) / 0.4) * 0.5)); shkFrame(1, cx, gy, w * 1.08, 0.45 * smooth((prog - 0.6) / 0.4));
    ctx.restore(); return; }
  const D = 1.3, th = (T.t || 0) - (T.ht || 0); if (th < 0 || th > D) { ctx.restore(); return; }
  const gy = (T.newTop != null ? T.newTop : T.top) * s;
  const fpos = 3 * eOut(th / 0.85), f0 = Math.min(3, Math.floor(fpos)), fr = smooth(fpos - f0);   // laufende Phase, weich überblendet
  const w = W * (0.6 + 1.5 * eOut(th / 0.95)), sy = 1 - 0.9 * smooth((th - 0.3) / 0.85), fade = 1 - smooth((th - D + 0.45) / 0.45);
  shkFrame(f0, cx, gy, w, (1 - fr) * fade, sy); if (f0 < 3) shkFrame(f0 + 1, cx, gy, w, fr * fade, sy);
  // zwei feine Druckringe, gleiten nach außen und werden zu Strichen
  for (let r = 0; r < 2; r++) { const t = (th - r * 0.12) / 0.95; if (t <= 0 || t >= 1) continue; const e = eOut(t), rx = W * (0.15 + 0.95 * e), ry = s * (0.9 - 0.75 * e);
    ctx.globalAlpha = 0.55 * (1 - smooth(t)) * (r ? 0.7 : 1); ctx.strokeStyle = "#eef7ff"; ctx.lineWidth = Math.max(1, s * 0.12 * (1 - e) + 0.8); ctx.beginPath(); ctx.ellipse(cx, gy, rx, Math.max(0.5, ry), 0, 0, Math.PI * 2); ctx.stroke(); }
  // feiner Strich am Ende
  const ln = smooth((th - 0.55) / 0.35) * fade; if (ln > 0.01) { const lw = W * (0.9 + 0.3 * eOut(th / D)), g = ctx.createLinearGradient(cx - lw / 2, 0, cx + lw / 2, 0);
    g.addColorStop(0, "rgba(238,247,255,0)"); g.addColorStop(0.5, `rgba(238,247,255,${0.7 * ln})`); g.addColorStop(1, "rgba(238,247,255,0)"); ctx.globalAlpha = 1; ctx.fillStyle = g; ctx.fillRect(cx - lw / 2, gy - Math.max(1, s * 0.05), lw, Math.max(1.5, s * 0.1)); }
  ctx.restore(); }
''' + s[j:]
open(p, "w", encoding="utf-8").write(s); print("ok V517")
