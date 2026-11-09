#!/usr/bin/env python3
"""V509: Ten-ton – Druckwelle als weiße, durchsichtige Luftdruck-Welle statt Sand (Martin 09.11. 16:12):
- Beim Fallen baut sich unter/um das Gewicht eine Druckfront auf (wird größer und heller, je näher am Stapel).
- Beim Aufprall platzt sie seitlich über die ganze Breite auf und verblasst (ca. 0,8 s).
Sprite img/fx_airwave.webp (Nano Banana Pro). Aufruf: python3 tools/patch509.py site/index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V508";', 'const GAME_VER = "V509";')
rep('const SHOCK_IMG = new Image(); SHOCK_IMG.src = "img/fx_shockwave.webp";   /* V508 */',
    'const SHOCK_IMG = new Image(); SHOCK_IMG.src = "img/fx_airwave.webp";   /* V508 · V509: Luftdruck statt Sand */')
i = s.find('function drawShock(s, W) {'); j = s.find('function drawTon(s, W) {', i); assert i > 0 and j > i
s = s[:i] + '''function drawShock(s, W) {   /* V509: Luftdruck – baut sich beim Fall um das Gewicht auf, platzt beim Aufprall seitlich über die ganze Breite */
  const T = S.ton; if (!T || !SHOCK_IMG.complete || !SHOCK_IMG.naturalWidth) return;
  const ar = SHOCK_IMG.naturalHeight / SHOCK_IMG.naturalWidth, now = performance.now() / 1000;
  ctx.save(); ctx.globalCompositeOperation = "lighter";
  if (!T.hit) {   // Druck aufbauen: Front unter dem Gewicht, wächst mit der Annäherung
    const tgt = Math.max(1, T.top - 3 + 5), prog = Math.max(0, Math.min(1, (T.y + 5) / tgt)), y = (T.y + 3) * s;
    const ww = W * (0.55 + 0.35 * prog) * (1 + Math.sin(now * 30) * 0.015), hh = ww * ar * 0.55;
    ctx.globalAlpha = 0.25 + 0.6 * prog; ctx.translate(W / 2, y + s * 0.2); ctx.scale(1, -1);   // umgedreht: Bogen zeigt nach unten
    ctx.drawImage(SHOCK_IMG, -ww / 2, -hh * 0.98, ww, hh);
  } else {   // Aufprall: Front reißt seitlich auf
    const th = (T.t || 0) - (T.ht || 0); if (th < 0 || th > 0.85) { ctx.restore(); return; }
    const e = 1 - Math.pow(1 - Math.min(1, th / 0.45), 3), ww = W * (0.9 + 1.1 * e), hh = ww * ar * (0.55 - 0.3 * e);
    const y0 = (T.newTop != null ? T.newTop : T.top) * s; ctx.globalAlpha = th < 0.3 ? 1 : Math.max(0, 1 - (th - 0.3) / 0.55);
    ctx.drawImage(SHOCK_IMG, W / 2 - ww / 2, y0 - hh * 0.95, ww, hh);
    ctx.translate(W / 2, y0); ctx.scale(1, -0.35); ctx.drawImage(SHOCK_IMG, -ww / 2, -hh * 0.95, ww, hh);   // flacher Ring am Boden
  }
  ctx.restore(); }
''' + s[j:]
open(p, "w", encoding="utf-8").write(s); print("ok V509")
