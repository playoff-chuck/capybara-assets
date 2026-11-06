"""V327 (Martin 06.11., To-do 91–94): vier neue Störungen ab Welle 65.
91 Bildausfall: W65, dann alle 18 Wellen · 3–4 Reihen leicht über der Mitte, 25–30 s Fernseh-Rauschen, leises Rauschen solange ein Stein im Bereich ist.
92 Magnet: W80, 92, 105, 117 · 2×3 Felder, metallisch-rot, schwebt unten links/rechts über dem Stapel, zieht den fallenden Stein zur Seite;
   berührt der Stein den Magneten, bleibt er dort kleben (wird abgelegt). 30 s.
93 Unkraut: W90, 110, 130 · Same fällt in eine Spalte, Pflanze wächst 1 Feld je 15 s (max. 8); Steine bleiben darauf stehen.
   Tesla/Sniper kürzen sie (alles ab dem Treffer aufwärts), Treffer an der Wurzel = weg.
94 Dieb: W100, dann abwechselnd +10/+9/+11 · läuft oben links → rechts (20 s), nach 10 s schnappt er das halbe Gold;
   nur Tesla/Sniper stoppen ihn (danach Gold zurück).
Beschreibungen Sniper/Tesla ab W90/W100 ergänzt. Test-Hook window.__dist.start(kind) / .state()."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V326";', 'const GAME_VER = "V327";')
# Shop-Texte
rep('"One shot: 2×2 patch wiped, the blast splats around it."',
    '"One shot: 2×2 patch wiped, the blast splats around it." + (S.wave >= 90 ? " Cuts weeds" + (S.wave >= 100 ? ", stops thieves." : ".") : "")')
rep('"4×4 lightning strike, splats count triple."',
    '"4×4 lightning strike, splats count triple." + (S.wave >= 90 ? " Cuts weeds" + (S.wave >= 100 ? ", stops thieves." : ".") : "")', 2)
JS = r'''
/* V327: Störungen Bildausfall · Magnet · Unkraut · Dieb */
try { (() => {
  const inner = () => S && S.started && !S.over && !S.nuts && !S.rotMode;
  const sched = k => { const w = S.wave | 0;
    if (k === "blk") return w >= 65 && (w - 65) % 18 === 0;
    if (k === "mag") return [80, 92, 105, 117].includes(w);
    if (k === "weed") return [90, 110, 130].includes(w);
    if (k === "thief") { let x = 100, i = 0; const st = [10, 9, 11]; while (x < w) x += st[i++ % 3]; return x === w; }
    return false; };
  const D = { blk: null, mag: null, weed: null, thief: null, done: {} };
  window.__dist = { state: () => ({ blk: !!D.blk, mag: D.mag && { side: D.mag.side, y: D.mag.y }, weed: D.weed && { x: D.weed.x, root: D.weed.root, h: D.weed.h }, thief: D.thief && { x: +D.thief.x.toFixed(2), stolen: D.thief.stolen } }), start: k => start(k), fire: (k, x, y) => (k === "snipe" ? snipe : tesla)(x, y), D };
  const NAMES = { blk: ["SIGNAL LOST!", "Part of the field goes dark"], mag: ["MAGNET!", "It pulls the blocks – steer against it"], weed: ["WEEDS!", "Blocks get stuck on it · Tesla or Sniper cut it"], thief: ["THIEF!", "Stop him with Tesla or Sniper"] };
  function start(k) {
    const GT = GH;
    if (k === "blk") { const n = Math.random() < 0.5 ? 3 : 4; D.blk = { r0: Math.floor(GT * 0.45) - n + 1, n, t: 0, life: 25 + Math.random() * 5 }; }
    if (k === "mag") { const side = Math.random() < 0.5 ? 0 : 1, xs = side ? [GW - 3, GW - 2] : [1, 2]; let top = GT - 1; for (const x of xs) for (let y = 0; y < GT; y++) if (S.grid[y * GW + x]) { top = Math.min(top, y); break; }
      D.mag = { side, xs, y: Math.max(3, Math.min(GT - 4, top - 4)), t: 0, life: 30, pullT: 0 }; }
    if (k === "weed") { let x = 2 + Math.floor(Math.random() * (GW - 4)); D.weed = { x, root: null, h: 0, seedY: -1, growT: 0, waves: 0 }; }
    if (k === "thief") D.thief = { x: -0.8, t: 0, stolen: 0 };
    snd("siren"); announce(NAMES[k][0], NAMES[k][1], "ALERT", 2400);
    if (k === "thief") setTimeout(() => SFX.say("Hold the line!"), 700);
  }
  // Rauschen (leise, nur solange ein Stein im Bildausfall steckt)
  let nz = null;
  function noiseLevel(v) { try { const ac = AU.ac(), out = AU.out(); if (!ac || !out) return;
      if (!nz) { const b = ac.createBuffer(1, ac.sampleRate, ac.sampleRate), d = b.getChannelData(0); for (let i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1;
        const src = ac.createBufferSource(); src.buffer = b; src.loop = true; const f = ac.createBiquadFilter(); f.type = "bandpass"; f.frequency.value = 3200; f.Q.value = 0.6; const g = ac.createGain(); g.gain.value = 0;
        src.connect(f); f.connect(g); g.connect(out); src.start(); nz = { g, ac }; }
      nz.g.gain.setTargetAtTime(v, nz.ac.currentTime, 0.08); } catch (e) {} }
  function landY(x) { for (let y = 0; y < GH; y++) if (S.grid[y * GW + x]) return y - 1; return GH - 1; }
  function weedCells() { const w = D.weed; if (!w || w.root == null) return []; const a = []; for (let i = 0; i < w.h; i++) a.push([w.x, w.root - i]); return a; }
  // Kollision: Steine bleiben auf dem Unkraut stehen
  const _col = collide;
  collide = function (cells, px, py) { if (_col(cells, px, py)) return true;
    if (D.weed && D.weed.root != null && !S.rotMode) { const w = D.weed; for (const [x, y] of cells) { const gx = px + x, gy = py + y; if (gx === w.x && gy <= w.root && gy > w.root - w.h) return true; } }
    return false; };
  // Linien unter der Wurzel → Unkraut rutscht mit
  const _cl = clearLines;
  clearLines = function () { let below = 0;
    if (D.weed && D.weed.root != null && !S.rotMode) for (let y = D.weed.root + 1; y < GH; y++) { let full = true; for (let x = 1; x < GW - 1; x++) if (!S.grid[y * GW + x]) { full = false; break; } if (full) below++; }
    const r = _cl.apply(this, arguments); if (r && below && D.weed) D.weed.root += below; return r; };
  function hitArea(x0, y0, w, h, label) {
    let hit = false;
    const W2 = D.weed; if (W2 && W2.root != null) { const cs = weedCells(); let low = null; cs.forEach(([x, y], i) => { if (x >= x0 && x < x0 + w && y >= y0 && y < y0 + h && low == null) low = i; });
      if (low === 0) { D.weed = null; fxText(W2.x, W2.root, "WEED PULLED!", "#9be36b"); hit = true; } else if (low != null) { W2.h = low; fxText(W2.x, W2.root - low, "WEED CUT", "#9be36b"); hit = true; } }
    const T = D.thief; if (T) { const tx = Math.round(T.x); if (tx >= x0 - (label === "snipe" ? 1 : 0) && tx < x0 + w + (label === "snipe" ? 1 : 0) && y0 <= (label === "snipe" ? 1 : 0)) {
        if (T.stolen) { S.gold += T.stolen; toast(`THIEF STOPPED · +${T.stolen} gold back`, "HQ", 2000); } else toast("THIEF STOPPED!", "HQ", 1600);
        S.fx.push({ type: "splat", x: T.x, y: 0, t: 0, life: 0.8, col: "#1a1a1a" }); D.thief = null; praise("GOTCHA!", 2, "Nailed it!"); hit = true; } }
    return hit; }
  const _ts = tesla; tesla = function (x, y) { const xx = Math.max(0, Math.min(GW - 4, x)), yy = Math.max(0, Math.min(GH - 4, y)); const r = _ts.apply(this, arguments); hitArea(xx, yy, 4, 4, "tesla"); return r; };
  const _sn = snipe; snipe = function (x, y) { const xx = Math.max(0, Math.min(GW - 2, x)), yy = Math.max(0, Math.min(GH - 2, y)); const r = _sn.apply(this, arguments); hitArea(xx, yy, 2, 2, "snipe"); return r; };
  // Ablauf
  let lastWave = 0, inWaveT = 0;
  function step(dt) {
    if (!S || !S.started || S.over) { if (S && S.over) { D.blk = D.mag = D.thief = null; D.weed = null; } noiseLevel(0); return; }
    if (S.wave !== lastWave) { lastWave = S.wave; inWaveT = 0; if (D.weed && ++D.weed.waves > 2) { D.weed = null; toast("WEEDS WITHERED", "HQ", 1400); } }
    if (S.inWave) inWaveT += dt;
    if (S.inWave && inner()) for (const k of ["blk", "mag", "weed", "thief"]) { const key = k + ":" + S.wave; if (!D.done[key] && sched(k) && inWaveT > (k === "thief" ? 12 : k === "weed" ? 9 : 6)) { D.done[key] = 1; start(k); } }
    if (S.rotMode) { D.mag = null; D.blk = null; }
    const p = S.piece;
    if (D.blk) { const b = D.blk; b.t += dt; let inside = false; if (p) for (const [x, y] of p.cells) { const gy = p.y + y; if (gy >= b.r0 && gy < b.r0 + b.n) inside = true; }
      noiseLevel(inside ? 0.05 : 0); if (b.t >= b.life) { D.blk = null; noiseLevel(0); toast("SIGNAL BACK", "HQ", 1200); } } else noiseLevel(0);
    if (D.mag) { const m = D.mag; m.t += dt; m.pullT += dt;
      if (p && m.t > 1 && m.pullT >= 0.8) { m.pullT = 0; const dx = m.side ? 1 : -1; if (!collide(p.cells, p.x + dx, p.y)) { p.x += dx; snd("move"); } }
      if (p) { let touch = false; for (const [x, y] of p.cells) { const gx = p.x + x, gy = p.y + y; if (m.xs.includes(gx) && gy >= m.y && gy < m.y + 3) touch = true; }
        if (touch) { snd("towerLost"); toast("MAGNET CLANK!", "ALERT", 1400); S.shake = 0.4; lockPiece(); } }
      if (m.t >= m.life) { D.mag = null; toast("MAGNET GONE", "HQ", 1200); } }
    if (D.weed) { const w = D.weed;
      if (w.root == null) { w.seedY += dt * 6; const ly = landY(w.x); if (w.seedY >= ly) { w.root = ly; w.h = 1; snd("lock"); } }
      else { if (w.root < GH - 1 && !S.grid[(w.root + 1) * GW + w.x]) w.root++;   /* fällt nach, wenn darunter frei wird */
        if (S.inWave) w.growT += dt; if (w.growT >= 15 && w.h < 8) { w.growT = 0; const ny = w.root - w.h; let free = ny >= 1 && !S.grid[ny * GW + w.x]; if (free && p) for (const [x, y] of p.cells) if (p.x + x === w.x && p.y + y === ny) free = false; if (free) w.h++; } } }
    if (D.thief) { const T = D.thief; T.t += dt; T.x = -0.8 + (GW + 1.6) * (T.t / 20);
      if (!T.stolen && T.t >= 10) { T.stolen = Math.floor(S.gold / 2); S.gold -= T.stolen; snd("sell"); toast(`THIEF GRABBED ${T.stolen} GOLD!`, "ALERT", 1800); const g = $("sGold"); if (g) { g.classList.remove("thiefHit"); void g.offsetWidth; g.classList.add("thiefHit"); } }
      if (T.t >= 20) { if (T.stolen) toast(`THIEF GOT AWAY · −${T.stolen} gold`, "HQ", 1800); D.thief = null; } }
  }
  const _up = update; update = function (dt) { const r = _up.apply(this, arguments); try { if (!frozen()) step(dt); else noiseLevel(0); } catch (e) { console.error("v327", e); } return r; };
  // Zeichnen
  const nc = document.createElement("canvas"); nc.width = 96; nc.height = 24; const nx = nc.getContext("2d"); let nT = 0;
  function drawMag(m, s) { const x = m.xs[0] * s, slide = Math.min(1, m.t), off = (1 - slide) * 3 * s * (m.side ? 1 : -1), y = m.y * s + Math.sin(m.t * 3) * s * 0.08, w = 2 * s, h = 3 * s;
    ctx.save(); ctx.translate(x + off, y); ctx.globalAlpha = 0.92;
    const g = ctx.createLinearGradient(0, 0, w, 0); g.addColorStop(0, "#7d1410"); g.addColorStop(0.45, "#e2473a"); g.addColorStop(0.55, "#ff8f84"); g.addColorStop(1, "#7d1410");
    ctx.fillStyle = g; ctx.strokeStyle = "#2a0806"; ctx.lineWidth = Math.max(2, s * 0.08);
    ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(0, h * 0.62); ctx.arc(w / 2, h * 0.62, w / 2, Math.PI, 0, true); ctx.lineTo(w, 0); ctx.lineTo(w * 0.68, 0); ctx.lineTo(w * 0.68, h * 0.62); ctx.arc(w / 2, h * 0.62, w * 0.18, 0, Math.PI, false); ctx.lineTo(w * 0.32, 0); ctx.closePath(); ctx.fill(); ctx.stroke();
    ctx.fillStyle = "#d9dde2"; ctx.fillRect(0, 0, w * 0.32, h * 0.18); ctx.fillRect(w * 0.68, 0, w * 0.32, h * 0.18); ctx.strokeRect(0, 0, w * 0.32, h * 0.18); ctx.strokeRect(w * 0.68, 0, w * 0.32, h * 0.18);
    ctx.globalAlpha = 0.5 + 0.3 * Math.sin(m.t * 8); ctx.strokeStyle = "#ffd6d0"; ctx.lineWidth = Math.max(1, s * 0.05); const d = m.side ? -1 : 1;
    for (let i = 0; i < 3; i++) { const r = s * (0.6 + i * 0.5 + (m.t * 1.5 % 0.5)); ctx.beginPath(); ctx.arc(m.side ? 0 : w, h * 0.4, r, d > 0 ? -0.6 : Math.PI - 0.6, d > 0 ? 0.6 : Math.PI + 0.6); ctx.stroke(); }
    ctx.restore(); }
  function drawWeed(w, s) { ctx.save();
    if (w.root == null) { const y = Math.max(0, w.seedY) * s; ctx.fillStyle = "#6b4a1e"; ctx.beginPath(); ctx.ellipse((w.x + 0.5) * s, y + s * 0.5, s * 0.12, s * 0.18, 0.4, 0, 6.29); ctx.fill(); ctx.restore(); return; }
    const cx = (w.x + 0.5) * s, yb = (w.root + 1) * s, yt = (w.root - w.h + 1) * s, now = performance.now() / 1000;
    ctx.strokeStyle = "#2f6b1c"; ctx.lineWidth = Math.max(3, s * 0.16); ctx.lineCap = "round"; ctx.beginPath(); ctx.moveTo(cx, yb);
    for (let yy = yb; yy >= yt + s * 0.2; yy -= s * 0.25) ctx.lineTo(cx + Math.sin(yy / s * 2.4 + now * 1.5) * s * 0.12, yy); ctx.stroke();
    for (let i = 0; i < w.h; i++) { const y = (w.root - i + 0.5) * s, sd = i % 2 ? 1 : -1; ctx.fillStyle = i % 2 ? "#57a32c" : "#78c043"; ctx.beginPath(); ctx.ellipse(cx + sd * s * 0.26, y, s * 0.28, s * 0.12, sd * -0.5, 0, 6.29); ctx.fill(); }
    ctx.fillStyle = "#a34a8d"; ctx.beginPath(); ctx.arc(cx, yt + s * 0.12, s * 0.16, 0, 6.29); ctx.fill(); ctx.fillStyle = "#ffd84a"; ctx.beginPath(); ctx.arc(cx, yt + s * 0.12, s * 0.06, 0, 6.29); ctx.fill();
    ctx.fillStyle = "#4a3212"; ctx.fillRect(cx - s * 0.3, yb - s * 0.1, s * 0.6, s * 0.1); ctx.restore(); }
  function drawThief(T, s) { const x = (T.x + 0.5) * s, y = 0.5 * s, b = Math.abs(Math.sin(T.t * 9)) * s * 0.06; ctx.save(); ctx.translate(x, y - b + s * 0.15); ctx.scale(1.5, 1.5);
    ctx.fillStyle = "#16161a"; ctx.strokeStyle = "#000"; ctx.lineWidth = 1;
    ctx.beginPath(); ctx.ellipse(0, s * 0.1, s * 0.22, s * 0.28, 0, 0, 6.29); ctx.fill();                 /* Körper */
    ctx.fillStyle = "#8a5a2b"; ctx.beginPath(); ctx.arc(0, -s * 0.2, s * 0.17, 0, 6.29); ctx.fill();      /* Kopf */
    ctx.fillStyle = "#16161a"; ctx.fillRect(-s * 0.2, -s * 0.36, s * 0.4, s * 0.1); ctx.fillRect(0, -s * 0.31, s * 0.3, s * 0.05);   /* Kappe */
    ctx.fillRect(-s * 0.17, -s * 0.24, s * 0.34, s * 0.07); ctx.fillStyle = "#fff"; ctx.fillRect(s * 0.02, -s * 0.23, s * 0.05, s * 0.04); ctx.fillRect(s * 0.1, -s * 0.23, s * 0.05, s * 0.04);   /* Maske */
    if (T.stolen) { ctx.fillStyle = "#c9a63a"; ctx.beginPath(); ctx.arc(-s * 0.3, s * 0.05, s * 0.16, 0, 6.29); ctx.fill(); ctx.fillStyle = "#3a2a08"; ctx.font = `bold ${Math.round(s * 0.2)}px sans-serif`; ctx.textAlign = "center"; ctx.textBaseline = "middle"; ctx.fillText("$", -s * 0.3, s * 0.06); }
    if (!T.stolen) { ctx.fillStyle = "#ff4a3a"; ctx.font = `bold ${Math.round(s * 0.3)}px sans-serif`; ctx.textAlign = "center"; ctx.fillText(Math.max(0, Math.ceil(10 - T.t)) + "", 0, -s * 0.45); }
    ctx.restore(); }
  const _dr = draw; draw = function () { const r = _dr.apply(this, arguments); try { if (!S || !S.started || S.over) return r; const s = CELL; ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0);
      if (D.weed) drawWeed(D.weed, s);
      if (D.mag) drawMag(D.mag, s);
      if (D.thief) drawThief(D.thief, s);
      if (D.blk) { const b = D.blk, now = performance.now(); if (now - nT > 60) { nT = now; const id = nx.createImageData(nc.width, nc.height); for (let i = 0; i < id.data.length; i += 4) { const v = Math.random() * 255 | 0; id.data[i] = id.data[i + 1] = id.data[i + 2] = v; id.data[i + 3] = 255; } nx.putImageData(id, 0, 0); }
        const fade = Math.min(1, b.t / 0.6, (b.life - b.t) / 0.6); ctx.globalAlpha = Math.max(0, fade); ctx.imageSmoothingEnabled = false; ctx.drawImage(nc, 0, b.r0 * CELL, cv.width, b.n * CELL);
        ctx.fillStyle = "rgba(0,0,0,.18)"; for (let y = b.r0 * CELL; y < (b.r0 + b.n) * CELL; y += 4) ctx.fillRect(0, y, cv.width, 2);
        ctx.globalAlpha = Math.max(0, fade) * (0.6 + 0.4 * Math.sin(now / 180)); ctx.fillStyle = "#fff"; ctx.font = `bold ${Math.round(CELL * 0.42)}px sans-serif`; ctx.textAlign = "center"; ctx.textBaseline = "middle"; ctx.fillText("NO SIGNAL", cv.width / 2, (b.r0 + b.n / 2) * CELL); }
      ctx.restore(); } catch (e) { console.error("v327d", e); } return r; };
  const st = document.createElement("style"); st.textContent = "#sGold.thiefHit{animation:thiefHit .9s ease-out}@keyframes thiefHit{0%,40%{color:#ff3b2f;transform:scale(1.35)}100%{transform:none}}"; document.head.appendChild(st);
})(); } catch (e) { console.error("v327", e); }
'''
anchor = '})();\n</script>'
p = s.rindex(anchor); s = s[:p] + JS + s[p:]
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
