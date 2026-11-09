#!/usr/bin/env python3
"""V494: t143 Outfit-Effekte nutzen (Martin 09.11. 10:26: «1 ja, 2 ja, 3 ja, 4 nein, 5 ja im Zahnradmenü + schwaches Handy erkennen und ausschalten, 6 nein»).
1) Vorschau im Squad File: Antippen eines Outfits (auch gesperrt) spielt 2 s seinen Effekt auf der Karte.
2) Unter SQUAD FRIENDS: nächstes Freunde-Outfit als Schatten + Effekt-Vorschau + Knopf INVITE.
3) INVITE (Zahnrad + Squad File) teilt ein im Gerät gezeichnetes Bild: Held im Outfit + Effekt + Rufzeichen + beste Welle.
5) Zahnrad-Menü: EFFECTS: ON/OFF. Schwaches Gerät (≤ 2 Kerne / ≤ 2 GB oder im Spiel < ~36 fps) → einmalig automatisch aus (Toast).
Aufruf: python3 tools/patch494.py site/index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)

rep('const GAME_VER = "V493";', 'const GAME_VER = "V494";')

# --- 5) Effekte an/aus + Auto-Aus ---
rep('function outfitFx() { try { if (heroDisco()) return null;',
    'function fxPref() { try { return localStorage.getItem("capy-fx"); } catch (e) { return null; } }   /* V494: on | off | auto-off | null */\n'
    'function fxOn() { const p = fxPref(); return p !== "off" && p !== "auto-off"; }\n'
    'function fxLabel() { const b = $("setFx"); if (b) b.textContent = "EFFECTS: " + (fxOn() ? "ON" : fxPref() === "auto-off" ? "OFF (AUTO)" : "OFF"); }\n'
    'const FX_WEAK = (() => { try { return (navigator.hardwareConcurrency > 0 && navigator.hardwareConcurrency <= 2) || (navigator.deviceMemory > 0 && navigator.deviceMemory <= 2); } catch (e) { return false; } })();\n'
    'function fxAutoOff(why) { if (fxPref() != null || FX_FORCE != null) return; try { localStorage.setItem("capy-fx", "auto-off"); } catch (e) {} fxLabel(); try { if (S && S.fx) S.fx = S.fx.filter(f => f.type !== "ofx"); } catch (e) {} try { toast("EFFECTS OFF · smoother play on this phone", "HQ", 2400); } catch (e) {} }\n'
    'const FXM = { t0: 0, n: 0, sum: 0 };   /* V494: Bildrate im Spiel messen */\n'
    'function fxMeasure() { if (fxPref() != null || FX_FORCE != null) return; const now = performance.now(), d = FXM.t0 ? now - FXM.t0 : 0; FXM.t0 = now;\n'
    '  if (!d || d > 200 || document.hidden || !S || !S.started || S.over || frozen()) return; FXM.n++; FXM.sum += d;\n'
    '  if (FXM.n >= 300) { const avg = FXM.sum / FXM.n; FXM.n = 0; FXM.sum = 0; if (avg > 28) fxAutoOff("fps"); } }\n'
    'function outfitFx() { try { if (heroDisco() || (FX_FORCE == null && !fxOn())) return null;')

rep('function ofxStep(dt) {   /* V490: Auslöser + Bewegung der Outfit-Partikel */\n  const e = outfitFx();',
    'function ofxStep(dt) {   /* V490: Auslöser + Bewegung der Outfit-Partikel */\n  try { fxMeasure(); } catch (er) {}\n  const e = outfitFx();')

# ofxAdd: optionales Ziel-Array (Vorschau/Bild)
rep('function ofxAdd(st, x, y, n, mode) {   /* V490: höchstens 14 Outfit-Partikel gleichzeitig */\n  let have = 0; for (const f of S.fx) if (f.type === "ofx") have++;',
    'function ofxAdd(st, x, y, n, mode, arr) {   /* V490: höchstens 14 Outfit-Partikel gleichzeitig · V494: arr = eigene Liste (Vorschau) */\n  const A = arr || S.fx; let have = 0; for (const f of A) if (f.type === "ofx") have++;')
rep('    S.fx.push({ type: "ofx", sh, col:', '    A.push({ type: "ofx", sh, col:')

# drawOfx: optionaler eigener Zeichenkontext (Koordinaten dann in px)
i = s.find('function drawOfx(f, k, s) {'); j = s.find('\n}\n', i)
body = s[i:j]
nb = body.replace('ctx.', 'G.').replace('function drawOfx(f, k, s) {   /* V490 */', 'function drawOfx(f, k, s, g2) {   /* V490 · V494: g2 = eigener Kontext, x/y in px */\n  const G = g2 || ctx;')
nb = nb.replace('G.translate(C(f.x), C(f.y));', 'G.translate(g2 ? f.x : C(f.x), g2 ? f.y : C(f.y));')
assert nb != body and nb.count('g2 ? f.x') == 1
s = s[:i] + nb + s[j:]
# globaler ctx für drawOfx bereitstellen (ctx ist im Spielcode ein Bezeichner im selben Skript)

# --- 1) Vorschau + 2) nächstes Freunde-Outfit ---
rep('''    h += `<div class="albSec">SQUAD FRIENDS<span>${fn}</span></div><div class="sqNote">${nx ? `Friends who reach wave 5 with your link unlock outfits · next at ${nx}` : "All friend outfits unlocked!"}</div>`; setTimeout(sqRefresh, 0); }''',
    '''    h += `<div class="albSec">SQUAD FRIENDS<span>${fn}</span></div><div class="sqNote">${nx ? `Friends who reach wave 5 with your link unlock outfits · next at ${nx}` : "All friend outfits unlocked!"}</div>`; setTimeout(sqRefresh, 0);
    if (nx) { const hk = heroKey(), ni = OUTFIT.findIndex(o => outfitNeed(o).f === nx), fx = OUTFIT_FX[hk][ni];   /* V494 (t143 Nr. 2) */
      if (ni > 0) { h += `<div class="ofNext"><div class="mcCard off ofSil" data-of="${hk}:${ni}"><img src="${outfitImg(hk, ni)}" alt=""></div><div class="ofNextTx"><b>NEXT: ${outfitName(hk, ni)}</b><small>${fx ? fx[2] : ""} · ${nx === 1 ? "1 friend" : nx + " friends"}</small><button type="button" class="shareBtn ofInv">INVITE</button></div></div>`;
        setTimeout(() => ofLoopNext(), 350); } } }''')

rep('''document.addEventListener("click", e => { const c = e.target.closest && e.target.closest("[data-of]"); if (!c || c.classList.contains("off")) return; const [k, n] = c.dataset.of.split(":");
  try { localStorage.setItem("capy-outfit-" + k, n); } catch (er) {} try { snd("uiTap"); } catch (er) {} try { const img = document.querySelector("#startMain .heroImg"); } catch (er) {} openSquad(); });''',
    '''document.addEventListener("click", e => { const c = e.target.closest && e.target.closest("[data-of]"); if (!c) return; const [k, n] = c.dataset.of.split(":");
  if (c.classList.contains("off")) { try { snd("uiTap"); } catch (er) {} ofPreview(c, k, +n); return; }   /* V494: gesperrt = nur Vorschau */
  try { localStorage.setItem("capy-outfit-" + k, n); } catch (er) {} try { snd("uiTap"); } catch (er) {} openSquad();
  const nc = document.querySelector(`#sqBody .ofRow [data-of="${k}:${n}"]`); if (nc) ofPreview(nc, k, +n); });
/* V494 (t143 Nr. 1): 2-s-Effektvorschau auf einer Outfit-Karte */
function ofPreview(card, k, n, dur) { const e = OUTFIT_FX[k] && OUTFIT_FX[k][n]; if (!e || !card) return; dur = dur || 2;
  const old = card.querySelector("canvas.ofPv"); if (old) old.remove();
  const r = card.getBoundingClientRect(); if (!r.width) return; const dpr = Math.min(2, window.devicePixelRatio || 1), cv = document.createElement("canvas");
  cv.className = "ofPv"; cv.width = Math.round(r.width * dpr); cv.height = Math.round(r.height * dpr); card.appendChild(cv);
  const g = cv.getContext("2d"), W = r.width, H = r.height, u = Math.max(10, W / 4), P = [];   /* u = px je Feld */
  let t = 0, last = performance.now(), em = 0, burst = 0;
  const step = now => { if (!cv.isConnected) return; const dt = Math.min(0.05, (now - last) / 1000); last = now; t += dt;
    if (t < dur - 0.5) { em -= dt;
      if (e[0] === "s" && em <= 0) { ofxAdd(e[1], W * (0.3 + Math.random() * 0.4) / u, H * (0.35 + Math.random() * 0.2) / u, 5, "s", P); em = 0.55; }
      else if (e[0] === "r" && em <= 0) { for (let i = 0; i < 3; i++) ofxAdd(e[1], W * (0.15 + 0.35 * i) / u, H * 0.5 / u, 2, "r", P); em = 0.6; }
      else if (e[0] === "t" && em <= 0) { const py = ((t * 0.9) % 1) * H * 0.8 + H * 0.1; ofxAdd(e[1], W * 0.5 / u, py / u, 1, "t", P); em = 0.06; } }
    for (const f of P) { f.t += dt; f.vy += f.g * dt; f.vx *= (1 - 1.2 * dt); f.x += (f.vx + (f.sh === "leaf" || f.sh === "bubble" ? Math.sin(f.t * 5 + f.ph) * 0.8 : 0)) * dt; f.y += f.vy * dt; f.rot += f.vr * dt; }
    for (let i = P.length - 1; i >= 0; i--) if (P[i].t >= P[i].life) P.splice(i, 1);
    g.setTransform(dpr, 0, 0, dpr, 0, 0); g.clearRect(0, 0, W, H);
    for (const f of P) { const q = Object.assign({}, f, { x: f.x * u, y: f.y * u }); drawOfx(q, 1 - f.t / f.life, u, g); }
    if (t < dur || P.length) requestAnimationFrame(step); else cv.remove(); };
  requestAnimationFrame(step); }
function ofLoopNext() { const c = document.querySelector("#sqBody .ofNext .ofSil"), o = $("ovSquad"); if (!c || !o || o.hidden) return; const [k, n] = c.dataset.of.split(":"); ofPreview(c, k, +n);
  clearTimeout(ofLoopNext.t); ofLoopNext.t = setTimeout(ofLoopNext, 3600); }
document.addEventListener("click", e => { const b = e.target.closest && e.target.closest(".ofInv"); if (!b) return; try { SFX.init(); snd("uiTap"); } catch (er) {} sqInviteImg(b); });''')

# --- 3) Einladungs-Bild ---
rep('async function sqInvite() { if (sqBusy) return; sqBusy = true; sqNote("…");',
    '''/* V494 (t143 Nr. 3): Einladungs-Bild – Held im Outfit + Effekt + Rufzeichen + beste Welle, im Gerät gezeichnet */
async function inviteCard() {
  const W = 1080, H = 1350, cv = document.createElement("canvas"); cv.width = W; cv.height = H; const g = cv.getContext("2d");
  try { await Promise.all([document.fonts.load("100px Bangers"), document.fonts.load('800 40px "Baloo 2"')]); } catch (e) {}
  const hk = heroKey(), sel = outfitSel(hk), fx = OUTFIT_FX[hk][sel], bw = msnBestW(), nick = (LS.get("tarnturm-nick") || "").toUpperCase();
  const P = wherePos(Math.max(1, bw || 1)), ck = ["samerica", "africa", "asia", "namerica", "antarctica"][P.c] || "samerica";
  const [bg, logo, hero] = await Promise.all([shLoad((PLACE_BG[ck] || [])[P.p]), shLoad(MAIN_LOGO), shLoad(outfitImg(hk, sel))]);
  const gr = g.createLinearGradient(0, 0, 0, H); gr.addColorStop(0, "#f6c477"); gr.addColorStop(1, "#d9772f"); g.fillStyle = gr; g.fillRect(0, 0, W, H);
  if (bg) { const k = Math.max(W / bg.naturalWidth, H / bg.naturalHeight), w2 = bg.naturalWidth * k, h2 = bg.naturalHeight * k; g.drawImage(bg, (W - w2) / 2, (H - h2) / 2, w2, h2); }
  const sh = g.createLinearGradient(0, 0, 0, H); sh.addColorStop(0, "rgba(20,10,4,.3)"); sh.addColorStop(.5, "rgba(20,10,4,.05)"); sh.addColorStop(1, "rgba(20,10,4,.65)"); g.fillStyle = sh; g.fillRect(0, 0, W, H);
  if (logo) { const lw = 560, lh = logo.naturalHeight * lw / logo.naturalWidth; g.drawImage(logo, (W - lw) / 2, 20, lw, Math.min(lh, 340)); }
  const hy = 385, hh = 585; let hx = W / 2, hw = 0;
  if (hero) { hw = hero.naturalWidth * hh / hero.naturalHeight; hx = (W - hw) / 2; g.save(); g.shadowColor = "rgba(0,0,0,.45)"; g.shadowBlur = 30; g.drawImage(hero, hx, hy, hw, hh); g.restore(); }
  if (fx) { const cols = OFX_COL[fx[1]] || OFX_COL.gold, shp = OFX_SH[fx[1]] || "spark";
    for (let i = 0; i < 46; i++) { const a = Math.random() * 6.283, rr = 240 + Math.random() * 190, x = W / 2 + Math.cos(a) * rr * 1.05, y = hy + hh * 0.48 + Math.sin(a) * rr * 0.9;
      drawOfx({ sh: shp, col: cols[i % cols.length], x, y, rot: Math.random() * 6.283, sz: (shp === "dot" ? 0.12 : 0.17) * (0.8 + Math.random() * 0.7), t: Math.random(), ph: Math.random() * 6.283 }, 0.5 + Math.random() * 0.5, 70, g); } }
  g.textAlign = "center"; g.lineJoin = "round"; const cx = W / 2;
  const t1 = nick || "JOIN MY SQUAD!"; shFit(g, t1, "#px Bangers", 96, W - 120); g.lineWidth = 14; g.strokeStyle = "#3a2414"; g.strokeText(t1, cx, 1040); g.fillStyle = "#fff"; g.fillText(t1, cx, 1040);
  const t2 = (nick ? "JOIN MY SQUAD" : "") + (bw >= 2 ? `${nick ? " · " : ""}BEST WAVE ${Math.min(150, bw)}` : "") + (fx ? ` · ${fx[2].toUpperCase()}` : "");
  if (t2) { shFit(g, t2, '800 #px "Baloo 2"', 40, W - 120); g.lineWidth = 9; g.strokeStyle = "rgba(30,16,6,.9)"; g.strokeText(t2, cx, 1100); g.fillStyle = "#ffe58a"; g.fillText(t2, cx, 1100); }
  const bx = 250, bw2 = W - 500; g.fillStyle = "#3a2414"; shRR(g, bx, 1142, bw2, 104, 52); g.fill(); g.fillStyle = "#ff5fa2"; shRR(g, bx, 1130, bw2, 104, 52); g.fill(); g.lineWidth = 7; g.strokeStyle = "#3a2414"; g.stroke();
  g.fillStyle = "#fff"; g.font = "64px Bangers"; g.fillText("PLAY FREE ▶", cx, 1204);
  g.font = '800 32px "Baloo 2"'; g.lineWidth = 8; g.strokeStyle = "rgba(30,16,6,.85)"; const t3 = "playcapybarasquad.com · free Ten-ton drop for you"; shFit(g, t3, '800 #px "Baloo 2"', 32, W - 100); g.strokeText(t3, cx, 1300); g.fillStyle = "#fff"; g.fillText(t3, cx, 1300);
  return cv; }
window.__inviteCard = () => inviteCard();
async function sqShareImg(url, text) {   /* true = geteilt/abgebrochen, false = kein Bild-Teilen möglich */
  try { const cv = await inviteCard(), blob = await new Promise(r => cv.toBlob(r, "image/png"));
    const file = blob && typeof File === "function" ? new File([blob], "capybara-squad-invite.png", { type: "image/png" }) : null;
    if (file && navigator.canShare && navigator.canShare({ files: [file] })) { await navigator.share({ files: [file], title: "Capybara Squad", text: text + " " + url }); return true; } } catch (e) { if (e && e.name === "AbortError") return true; }
  return false; }
async function sqInviteImg(btn) { const t0 = btn.textContent; const note = t => { btn.textContent = t; setTimeout(() => { btn.textContent = t0; }, 3500); };
  if (sqBusy) return; sqBusy = true; btn.textContent = "…";
  try { const c = await sqMyCode(); if (!c) { note("NO CONNECTION"); return; } const url = SHARE_URL + "/?squad=" + c, text = "Join my squad in Capybara Squad! You get a free Ten-ton drop.";
    if (await sqShareImg(url, text)) { note("INVITE"); return; }
    if (navigator.share) { try { await navigator.share({ title: "Capybara Squad", text, url }); note("SENT!"); } catch (e) { note(e && e.name === "AbortError" ? "INVITE" : "LINK: " + url.replace("https://", "")); } return; }
    try { await navigator.clipboard.writeText(text + " " + url); note("LINK COPIED!"); } catch (e) { note("LINK: " + url.replace("https://", "")); }
  } finally { sqBusy = false; } }
async function sqInvite() { if (sqBusy) return; sqBusy = true; sqNote("…");''')

rep('''    const url = SHARE_URL + "/?squad=" + c, text = "Join my squad in Capybara Squad! You get a free Ten-ton drop.";
    if (navigator.share) { try { await navigator.share({ title: "Capybara Squad", text, url }); sqNote(`Your squad code: ${c}`); }''',
    '''    const url = SHARE_URL + "/?squad=" + c, text = "Join my squad in Capybara Squad! You get a free Ten-ton drop.";
    if (await sqShareImg(url, text)) { sqNote(`Your squad code: ${c}`); return; }   /* V494: mit Bild */
    if (navigator.share) { try { await navigator.share({ title: "Capybara Squad", text, url }); sqNote(`Your squad code: ${c}`); }''')

# Zahnrad-Knopf
rep('<button id="setGuide" class="btn-small" type="button">Guide</button></div>',
    '<button id="setGuide" class="btn-small" type="button">Guide</button><button id="setFx" class="btn-small" type="button">EFFECTS: ON</button></div>')
rep('document.addEventListener("click", e => { if (e.target.closest("#setInvite")) {',
    'document.addEventListener("click", e => { if (e.target.closest("#setFx")) { const on = fxOn(); try { localStorage.setItem("capy-fx", on ? "off" : "on"); } catch (er) {} if (on) { try { if (S && S.fx) S.fx = S.fx.filter(f => f.type !== "ofx"); } catch (er) {} } fxLabel(); try { snd("uiTap"); } catch (er) {} return; }\n  if (e.target.closest("#setInvite")) {')
rep('window.__ofx = { fx: outfitFx, add: ofxAdd };',
    'window.__ofx = { fx: outfitFx, add: ofxAdd, pv: (c, k, n) => ofPreview(c, k, n), fxOn: () => fxOn(), auto: w => fxAutoOff(w) };\nsetTimeout(() => { fxLabel(); if (FX_WEAK) fxAutoOff("hw"); }, 1500); setInterval(() => { const o = $("ovSettings"); if (o && !o.hidden) fxLabel(); }, 700);')

# CSS
rep('.ofRow .mcCard i,.ofRow .mcCard small,.ofRow .mcCard b.ofFx{overflow-wrap:anywhere;hyphens:auto;-webkit-hyphens:auto}\n',
    '.ofRow .mcCard i,.ofRow .mcCard small,.ofRow .mcCard b.ofFx{overflow-wrap:anywhere;hyphens:auto;-webkit-hyphens:auto}\n'
    '.ofRow .mcCard,.ofNext .mcCard{position:relative}canvas.ofPv{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;z-index:2}\n'
    '.ofNext{display:flex;align-items:center;gap:10px;margin:0 0 8px;padding:6px 8px;border-radius:12px;background:#f3e6cc;border:2px dashed #c9a87a}'
    '.ofNext .ofSil{width:64px;flex:0 0 64px;padding:2px;cursor:pointer;overflow:hidden}.ofNext .ofSil img{width:100%;display:block;filter:brightness(0) opacity(.55)}'
    '.ofNextTx{display:flex;flex-direction:column;align-items:flex-start;gap:2px;min-width:0}.ofNextTx b{font-family:Bangers,system-ui;font-size:17px;letter-spacing:.04em;color:#3a2414}'
    '.ofNextTx small{font-size:11px;color:#8a6a4a;overflow-wrap:anywhere}.ofNextTx .shareBtn{margin:4px 0 0!important}\n'
    '#ovSettings .setRow{flex-wrap:wrap}\n')

open(p, "w", encoding="utf-8").write(s); print("ok V494")
