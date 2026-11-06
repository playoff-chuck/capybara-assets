"""V353 (Martin 07.11. 00:38): Dieb flüssiger und früher:
- Bildwechsel mit weicher Überblendung (0,16 s), Umdrehen beim Zurückschauen als sanftes Drehen (Spiegeln über cos), weiches Wippen (Sinus statt Hüpfer).
- Weg mit Ease-in/out: bremst sanft ab, schleicht weich an, beschleunigt beim Wegrennen.
- Hält früher an: bleibt deutlich links vor der Gold-Anzeige stehen (überdeckt sie beim Umschauen/Händereiben nicht mehr), greift aus dem Abstand."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V352";', 'const GAME_VER = "V353";')
i = s.find('  const FR = [1, 2, 3'); j = s.find('  el.addEventListener("pointerdown"', i); assert 0 < i < j
NEW = r'''  const FR = [1, 2, 3, 4, 5, 6, 7].map(n => { const im = new Image(); im.decoding = "async"; im.src = "img/thief_" + n + ".webp"; return im; });
  const ease = p => p < 0 ? 0 : p > 1 ? 1 : p * p * (3 - 2 * p);   // weich an und aus
  function pose(t) {   // Bild, Spiegelung (−1…1), Wippen, Neigung
    const ph = phase(t); let fi = 0, sx = 1, bob = 0, tilt = 0;
    if (ph === "walk") { const c = t * 3.6; fi = Math.floor(c) % 2; bob = (1 - Math.cos(c * Math.PI * 2)) * 1.3; }
    else if (ph === "back") { fi = 2; const p = t - 6; sx = p < 0.35 ? Math.cos(Math.PI * ease(p / 0.35)) : p < 0.95 ? -1 : Math.cos(Math.PI * (1 - ease((p - 0.95) / 0.35))); }
    else if (ph === "eye") { fi = 3; bob = (1 - Math.cos(t * 18)) * 0.5; }
    else if (ph === "sneak") { fi = 4; bob = (1 - Math.cos(t * 6.5)) * 1.4; tilt = Math.sin(t * 6.5) * 0.03; }
    else if (ph === "grab") { fi = 5; tilt = 0.04 * Math.sin(Math.min(1, (t - 10) / 0.6) * Math.PI); }
    else { fi = 6; const c = t * 2.6; bob = (1 - Math.cos(c * Math.PI * 2)) * 2.4; tilt = 0.07 + Math.sin(c * Math.PI * 2) * 0.035; }
    return { ph, fi, sx, bob, tilt }; }
  function drawFrame(fi, alpha, P, h) { const im = FR[fi]; if (!im.complete || !im.naturalWidth || alpha <= 0) return;
    const w = h * im.naturalWidth / im.naturalHeight; g.save(); g.globalAlpha = alpha; g.translate(SZ / 2, SZ - 5 - P.bob); g.rotate(P.tilt); g.scale(Math.abs(P.sx) < 0.08 ? 0.08 * Math.sign(P.sx || 1) : P.sx, 1);
    g.drawImage(im, -w / 2, -h, w, h); g.restore(); }
  function sprite(T) {
    g.setTransform(DPR, 0, 0, DPR, 0, 0); g.clearRect(0, 0, SZ, SZ);
    const t = T.t, P = pose(t), h = SZ - 14;
    if (T.fi !== P.fi) { T.prevFi = T.fi == null ? P.fi : T.fi; T.fi = P.fi; T.fadeT = t; }
    const k = ease(Math.min(1, (t - (T.fadeT || 0)) / 0.16));
    g.fillStyle = "rgba(0,0,0,.22)"; g.beginPath(); g.ellipse(SZ / 2, SZ - 5, 22 * (1 - P.bob / 18), 3.5, 0, 0, 6.29); g.fill();
    if (k < 1 && T.prevFi != null && T.prevFi !== P.fi) drawFrame(T.prevFi, 1 - k, P, h);
    drawFrame(P.fi, k < 1 ? Math.max(k, 0.35) : 1, P, h);
    const mark = P.ph === "back" && t > 6.3 ? "?" : P.ph === "eye" ? "!" : "";
    if (mark) { const pop = ease(Math.min(1, (t - (P.ph === "back" ? 6.3 : 7.3)) / 0.2)); g.save(); g.translate(SZ / 2 + 22, 12); g.scale(pop, pop); g.fillStyle = "#fff"; g.strokeStyle = "#16161c"; g.lineWidth = 1.5; g.beginPath(); g.arc(0, 0, 8, 0, 6.29); g.fill(); g.stroke();
      g.fillStyle = mark === "!" ? "#e0412f" : "#16161c"; g.font = "bold 12px sans-serif"; g.textAlign = "center"; g.textBaseline = "middle"; g.fillText(mark, 0, 1); g.restore(); }
    if (!T.stolen && t < 10) { g.fillStyle = "#ff4a3a"; g.strokeStyle = "#fff"; g.lineWidth = 3; g.font = "bold 13px sans-serif"; g.textAlign = "center"; const n = String(Math.max(0, Math.ceil(10 - t))); g.strokeText(n, SZ / 2 - 22, 12); g.fillText(n, SZ / 2 - 22, 12); }
  }
  window.__thiefPos = T => { if (!T) { el.style.display = "none"; return; }
    const ge = document.getElementById("sGold"), r = ge ? ge.getBoundingClientRect() : { left: innerWidth / 2, width: 0, top: 40, height: 0 };
    const gy = r.top + r.height / 2, t = T.t, stop = r.left - 84, reach = r.left - 56, end = innerWidth + SZ;
    const x = t < 6 ? -SZ + (stop + SZ) * (1 - Math.pow(1 - t / 6, 2))                       /* läuft heran und bremst sanft */
      : t < 8.4 ? stop
      : t < 10 ? stop + (reach - stop) * ease((t - 8.4) / 1.6)                                    /* schleicht hin */
      : t < 10.6 ? reach
      : reach + (end - reach) * Math.pow(Math.min(1, (t - 10.6) / 19.4), 1.35);                  /* rennt weg, wird schneller */
    el.style.display = "block"; el.style.transform = `translate(${(x - SZ / 2).toFixed(1)}px,${Math.round(Math.max(gy - SZ + 30, 4))}px)`; sprite(T); };
'''
s = s[:i] + NEW + s[j:]
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
