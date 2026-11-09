#!/usr/bin/env python3
"""V513: Ten-ton-Druckwelle als echte Animation (Martin 09.11. 16:35): 4-Phasen-Bildfolge (Nano Banana Pro, img/fx_airwave_seq.webp)
mit weichem Überblenden, wachsender Breite, Ringen, die nach außen laufen, und Funken.
- Beim Fallen: kleine Druckkuppel unter dem Gewicht, pulsiert und wächst mit der Annäherung.
- Aufprall (1,1 s): Kuppel → flache Welle → breiter Ring mit Wirbeln → feine Wellen, die zerfallen.
Aufruf: python3 tools/patch513.py site/index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V512";', 'const GAME_VER = "V513";')
rep('const SHOCK_IMG = new Image(); SHOCK_IMG.src = "img/fx_airwave.webp";   /* V508 · V509: Luftdruck statt Sand */',
    'const SHOCK_IMG = new Image(); SHOCK_IMG.src = "img/fx_airwave_seq.webp";   /* V508 · V509 · V513: 4 Phasen à 640×320, Bodenlinie y=200 */')
i = s.find('function drawShock(s, W) {'); j = s.find('function drawTon(s, W) {', i); assert i > 0 and j > i
s = s[:i] + '''const SHK = { cw: 640, ch: 320, by: 200, sp: [] };
function shkFrame(f, cx, gy, w, al) {   /* Phase f (0–3) mit Breite w, Bodenlinie bei gy */
  if (al <= 0.01) return; const k = w / SHK.cw, h = SHK.ch * k;
  ctx.globalAlpha = Math.min(1, al); ctx.drawImage(SHOCK_IMG, f * SHK.cw, 0, SHK.cw, SHK.ch, cx - w / 2, gy - SHK.by * k, w, h); }
function drawShock(s, W) {   /* V513: animierte Luftdruck-Welle */
  const T = S.ton; if (!T || !SHOCK_IMG.complete || !SHOCK_IMG.naturalWidth) return;
  const now = performance.now() / 1000, cx = W / 2;
  ctx.save(); ctx.globalCompositeOperation = "screen";
  if (!T.hit) {   // Druck baut sich unter dem Gewicht auf
    const tgt = Math.max(1, T.top - 3 + 5), prog = Math.max(0, Math.min(1, (T.y + 5) / tgt)), gy = (T.y + 3.25) * s;
    const pulse = 1 + Math.sin(now * 26) * 0.05 * (0.4 + prog), w = W * (0.28 + 0.42 * prog) * pulse;
    ctx.translate(0, gy * 2); ctx.scale(1, -1);   // Kuppel zeigt nach unten (vor dem Gewicht her)
    shkFrame(0, cx, gy, w, 0.2 + 0.35 * prog); shkFrame(1, cx, gy, w * 1.1, Math.max(0, prog - 0.55) * 0.9);
    ctx.restore(); return; }
  const th = (T.t || 0) - (T.ht || 0); if (th < 0 || th > 1.15) { ctx.restore(); return; }
  const gy = (T.newTop != null ? T.newTop : T.top) * s;
  // Bildfolge mit Überblenden: 0 → 1 → 2 → 3
  const K = [0, 0.1, 0.28, 0.6, 1.15], ease = x => 1 - Math.pow(1 - x, 3);
  const wAt = t => W * (0.55 + 1.6 * ease(Math.min(1, t / 0.75)));   // wird breiter
  for (let f = 0; f < 4; f++) { const a0 = K[f], a1 = K[f + 1];
    let al = 0; if (th >= a0 - 0.08 && th <= a1 + 0.12) al = th < a0 ? (th - a0 + 0.08) / 0.08 : th > a1 ? 1 - (th - a1) / 0.12 : 1;
    if (f === 3) al *= Math.max(0, 1 - Math.max(0, th - 0.75) / 0.4);
    const jit = 1 + Math.sin(now * 40 + f) * 0.012; shkFrame(f, cx, gy, wAt(th) * (f === 0 ? 0.55 : f === 1 ? 0.8 : 1) * jit, al); }
  // Druckringe, die nach außen laufen
  ctx.globalAlpha = 1; for (let r = 0; r < 3; r++) { const t = th - r * 0.09; if (t <= 0 || t > 0.7) continue; const e = ease(t / 0.7), rx = W * (0.1 + 0.95 * e), ry = s * (0.5 + 0.9 * e);
    ctx.strokeStyle = `rgba(235,246,255,${(1 - e) * (0.75 - r * 0.18)})`; ctx.lineWidth = Math.max(1, s * 0.22 * (1 - e) + 1); ctx.beginPath(); ctx.ellipse(cx, gy, rx, ry, 0, 0, Math.PI * 2); ctx.stroke(); }
  // Funken / Luftschlieren
  if (!T.spk) { T.spk = []; for (let n = 0; n < 26; n++) { const a = (Math.random() < 0.5 ? Math.PI : 0) + (Math.random() - 0.5) * 0.9; T.spk.push({ a, v: 2 + Math.random() * 5, l: 0.25 + Math.random() * 0.5, up: Math.random() * 1.5 }); } }
  for (const p of T.spk) { if (th > p.l) continue; const k = th / p.l, d = p.v * s * th * 3, x = cx + Math.cos(p.a) * d, y = gy - p.up * s * k - Math.abs(Math.sin(p.a)) * d * 0.3;
    ctx.globalAlpha = (1 - k) * 0.9; ctx.strokeStyle = "#f2f9ff"; ctx.lineWidth = Math.max(1, s * 0.07); ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x - Math.cos(p.a) * s * 0.6 * (1 - k), y); ctx.stroke(); }
  // kurzer Blitz am Boden
  if (th < 0.14) { ctx.globalAlpha = (0.14 - th) / 0.14 * 0.5; ctx.fillStyle = "#ffffff"; ctx.fillRect(0, gy - s * 0.5, W, s * 0.8); }
  ctx.restore(); }
''' + s[j:]
open(p, "w", encoding="utf-8").write(s); print("ok V513")
