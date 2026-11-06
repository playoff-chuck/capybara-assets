"""V337 (Martin 06.11. 23:36): Unkraut wächst kontinuierlich (Spitze schiebt sich stufenlos nach oben) und nochmal 30 % schneller
(1 Feld je 8,85 s statt 11,5 s). Neue, feinere Grafik: verjüngter, leicht schwingender Stängel mit Verlauf, Blätter sitzen fest am Stängel
(Blattform mit Mittelrippe, wachsen an der Spitze nach), Wurzeln unten, Blüte oben."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V336";', 'const GAME_VER = "V337";')
rep('if (S.inWave) w.growT += dt; if (w.growT >= 11.5 && w.h < 12) { w.growT = 0; const ny = w.root - w.h; if (ny >= 1 && weedPush(w.x, ny, p)) w.h++; }',
    'if (S.inWave) w.growT += dt; if (w.growT >= 8.85 && w.h < 12) { const ny = w.root - w.h; if (ny >= 1 && weedPush(w.x, ny, p)) { w.h++; w.growT = 0; } else w.growT = 8.85; }')
i = s.find('  function drawWeed(w, s) {'); j = s.find('  function drawThief(T, s) {'); assert 0 < i < j
NEW = r'''  function drawWeed(w, s) { ctx.save();
    if (w.root == null) { const y = Math.max(0, w.seedY) * s; ctx.fillStyle = "#6b4a1e"; ctx.beginPath(); ctx.ellipse((w.x + 0.5) * s, y + s * 0.5, s * 0.1, s * 0.15, 0.4, 0, 6.29); ctx.fill(); ctx.restore(); return; }
    const now = performance.now() / 1000, cx = (w.x + 0.5) * s, yb = (w.root + 1) * s;
    const nextFree = w.h < 12 && w.root - w.h >= 1 && !S.grid[(w.root - w.h) * GW + w.x];
    const hv = Math.max(0.3, w.h - 0.1 + (nextFree ? Math.min(1, w.growT / 8.85) : 0)), yt = yb - hv * s, L = yb - yt;
    const sx = y => cx + Math.sin((yb - y) / s * 1.6 + now * 1.3) * s * 0.08 * Math.min(1, (yb - y) / s);
    // Wurzeln
    ctx.strokeStyle = "#6b4a22"; ctx.lineWidth = Math.max(1, s * 0.035); ctx.lineCap = "round";
    for (const k of [-1, -0.45, 0.4, 0.95]) { ctx.beginPath(); ctx.moveTo(cx, yb - s * 0.06); ctx.quadraticCurveTo(cx + k * s * 0.18, yb - s * 0.02, cx + k * s * 0.34, yb + s * 0.03); ctx.stroke(); }
    // Stängel (verjüngt, Verlauf)
    const pts = []; for (let y = yb; y > yt; y -= s * 0.08) pts.push(y); pts.push(yt);
    const wd = y => s * (0.14 - 0.09 * (yb - y) / L);
    const gr = ctx.createLinearGradient(0, yb, 0, yt); gr.addColorStop(0, "#2e5e18"); gr.addColorStop(1, "#6fbf3a");
    ctx.fillStyle = gr; ctx.beginPath(); pts.forEach((y, k) => { const x = sx(y) - wd(y) / 2; k ? ctx.lineTo(x, y) : ctx.moveTo(x, y); });
    for (let k = pts.length - 1; k >= 0; k--) ctx.lineTo(sx(pts[k]) + wd(pts[k]) / 2, pts[k]); ctx.closePath(); ctx.fill();
    // Blätter: fest am Stängel, abwechselnd, an der Spitze kleiner
    for (let i = 0, y = yb - s * 0.45; y > yt + s * 0.15; i++, y -= s * 0.55) {
      const side = i % 2 ? 1 : -1, grow = Math.min(1, (y - yt) / (s * 0.7)), len = s * (0.58 - 0.12 * (yb - y) / Math.max(L, s)) * grow;
      if (len < s * 0.05) continue;
      const ax = sx(y), ang = (side > 0 ? -0.55 : Math.PI + 0.55) + Math.sin(now * 2 + i) * 0.08 * side;
      ctx.save(); ctx.translate(ax, y); ctx.rotate(ang);
      const lg = ctx.createLinearGradient(0, -len * 0.3, 0, len * 0.3); lg.addColorStop(0, i % 2 ? "#8fd24e" : "#7cc444"); lg.addColorStop(1, "#3f7d22");
      ctx.fillStyle = lg; ctx.beginPath(); ctx.moveTo(0, 0); ctx.bezierCurveTo(len * 0.25, -len * 0.38, len * 0.75, -len * 0.3, len, 0); ctx.bezierCurveTo(len * 0.7, len * 0.22, len * 0.25, len * 0.22, 0, 0); ctx.fill();
      ctx.strokeStyle = "rgba(220,255,190,.55)"; ctx.lineWidth = Math.max(0.6, s * 0.018); ctx.beginPath(); ctx.moveTo(0, 0); ctx.quadraticCurveTo(len * 0.5, -len * 0.06, len * 0.92, 0); ctx.stroke();
      ctx.restore(); }
    // Blüte an der Spitze
    const bx = sx(yt), by = yt, br = s * 0.13 * Math.min(1, hv);
    ctx.save(); ctx.translate(bx, by); ctx.rotate(Math.sin(now * 1.3) * 0.2);
    for (let k = 0; k < 5; k++) { ctx.rotate(Math.PI * 2 / 5); ctx.fillStyle = k % 2 ? "#c2509f" : "#a63d88"; ctx.beginPath(); ctx.ellipse(0, -br * 0.9, br * 0.55, br * 0.95, 0, 0, 6.29); ctx.fill(); }
    ctx.fillStyle = "#ffd84a"; ctx.beginPath(); ctx.arc(0, 0, br * 0.5, 0, 6.29); ctx.fill(); ctx.restore();
    ctx.restore(); }
'''
s = s[:i] + NEW + s[j:]
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
