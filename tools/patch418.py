#!/usr/bin/env python3
# V418 (t14 Teil 1, Martin 07.11. 18:20 «t14 komplett umsetzen», Reihenfolge: zuerst Share-Bild):
# SHARE-Knopf auf der Ergebniskarte (Game over / neuer Rekord / Weltreise geschafft) und auf der Replay-Karte «<Ort> CLEARED!».
# Bild 1080×1350 wird im Gerät gezeichnet (Orts-Hintergrund, Logo, Held mit Outfit, Welle/Ort/Score/Sterne, «PLAY FREE · playcapybarasquad.com»)
# und über das System-Teilen-Menü verschickt (Web Share mit Datei; sonst nur Text+Link; sonst PNG herunterladen). Keine fremden Server.
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:80])
    s = s.replace(a, b)

rep('const GAME_VER = "V417";', 'const GAME_VER = "V418";')

# Knopf neben dem Score
rep('<div class="hsScore"><span id="overScore">0</span><small>Score</small></div>',
    '<div class="hsScore"><span id="overScore">0</span><small>Score</small><button type="button" id="btnShare" class="shareBtn" aria-label="Share your result">SHARE</button></div>')

# Replay-Karte: SHARE neben OK, nur wenn geschafft
rep('''+ `<p class="rpSt">${starStr(n)}</p><span>${n > R.best ? "NEW BEST! " : ""}Best: ${starStr(best)}</span><em>Your world tour save is untouched.</em><button type="button" class="btn-accent">OK</button></div>`;''',
    '''+ `<p class="rpSt">${starStr(n)}</p><span>${n > R.best ? "NEW BEST! " : ""}Best: ${starStr(best)}</span><em>Your world tour save is untouched.</em>${ok ? `<button type="button" class="shareBtn rpShare">SHARE</button>` : ""}<button type="button" class="btn-accent">OK</button></div>`;
  window.__shareCtx = { kind: "place", g: R.g, n, wave: R.end };   /* V418 */''')
rep('''d.querySelector("button").addEventListener("click", () => { try { SFX.init(); snd("uiTap"); } catch (e) {} d.remove(); toMenu(); });''',
    '''d.querySelector(".btn-accent").addEventListener("click", () => { try { SFX.init(); snd("uiTap"); } catch (e) {} d.remove(); toMenu(); });
  { const sb = d.querySelector(".rpShare"); if (sb) sb.addEventListener("click", () => { try { SFX.init(); snd("uiTap"); } catch (e) {} shareResult(window.__shareCtx); }); }''')

# Zeichnen + Teilen
rep('''try { window.__TT && Object.assign(window.__TT, { startReplay: g => startReplay(g), replayEnd: w => replayEnd(w), saveGame: () => saveGame(), gameOver: w => gameOver(w) }); } catch (e) {}''',
    '''try { window.__TT && Object.assign(window.__TT, { startReplay: g => startReplay(g), replayEnd: w => replayEnd(w), saveGame: () => saveGame(), gameOver: w => gameOver(w) }); } catch (e) {}
/* V418 (t14): Share-Bild im Gerät zeichnen + System-Teilen */
const SHARE_URL = "https://playcapybarasquad.com";
function shLoad(src) { return new Promise(res => { if (!src) return res(null); const i = new Image(); let done = false; const fin = v => { if (!done) { done = true; res(v); } }; i.onload = () => fin(i); i.onerror = () => fin(null); setTimeout(() => fin(i.complete && i.naturalWidth ? i : null), 3500); i.src = src; }); }
function shRR(g, x, y, w, h, r) { g.beginPath(); g.moveTo(x + r, y); g.arcTo(x + w, y, x + w, y + h, r); g.arcTo(x + w, y + h, x, y + h, r); g.arcTo(x, y + h, x, y, r); g.arcTo(x, y, x + w, y, r); g.closePath(); }
function shFit(g, txt, font, size, maxW) { let z = size; g.font = font.replace("#", z); while (z > 20 && g.measureText(txt).width > maxW) { z -= 4; g.font = font.replace("#", z); } return z; }
function shInfo(o) {
  o = o || { kind: "over" }; const st = starsAll(), tot = Object.values(st).reduce((a, b) => a + (+b || 0), 0);
  if (o.kind === "place") { const P = wherePos(o.wave || (o.g + 1) * 5); return { c: P.c, p: P.p, tag: `${P.cont[1]} · PLACE ${o.g + 1} OF 30`, title: `${P.place} CLEARED!`, stars: o.n || 0, big: null, tot, wave: o.wave, call: "CAN YOU GET 5 STARS?", text: `I cleared ${P.place} with ${o.n || 0}/5 stars in Capybara Squad! Can you get 5? ${SHARE_URL}` }; }
  const w = Math.max(1, S && S.wave || 1), P = wherePos(w), sc = (S && S.score) || 0, win = !!(S && S.won);
  return { c: P.c, p: P.p, tag: `${P.place} · ${P.cont[1]}`, title: win ? "WORLD TOUR COMPLETE!" : `I REACHED WAVE ${w}`, stars: null, big: sc, tot, wave: w,
    stats: [[w, "WAVES"], [(S && S.lines) || 0, "LINES"], [(S && S.kills) || 0, "SPLATS"], [tot, "STARS"]], call: "BEAT MY SCORE!",
    text: win ? `I beat all 150 waves of Capybara Squad with ${sc.toLocaleString("en-US")} points! Can you beat me? ${SHARE_URL}` : `I reached wave ${w} (${P.place}) in Capybara Squad with ${sc.toLocaleString("en-US")} points! Can you beat me? ${SHARE_URL}` };
}
async function shareCard(o) {
  const I = shInfo(o), W = 1080, H = 1350, cv = document.createElement("canvas"); cv.width = W; cv.height = H; const g = cv.getContext("2d");
  try { await Promise.all([document.fonts.load("100px Bangers"), document.fonts.load('800 40px "Baloo 2"')]); } catch (e) {}
  const ck = ["samerica", "africa", "asia", "namerica", "antarctica"][I.c] || "samerica";
  const [bg, logo, hero] = await Promise.all([shLoad((PLACE_BG[ck] || [])[I.p]), shLoad(MAIN_LOGO), shLoad(HERO_IMG[heroKey()])]);
  const gr = g.createLinearGradient(0, 0, 0, H); gr.addColorStop(0, "#f6c477"); gr.addColorStop(1, "#d9772f"); g.fillStyle = gr; g.fillRect(0, 0, W, H);
  if (bg) { const k = Math.max(W / bg.naturalWidth, H / bg.naturalHeight), bw = bg.naturalWidth * k, bh = bg.naturalHeight * k; g.drawImage(bg, (W - bw) / 2, (H - bh) / 2, bw, bh); }
  const sh = g.createLinearGradient(0, 0, 0, H); sh.addColorStop(0, "rgba(20,10,4,.25)"); sh.addColorStop(.45, "rgba(20,10,4,.05)"); sh.addColorStop(1, "rgba(20,10,4,.55)"); g.fillStyle = sh; g.fillRect(0, 0, W, H);
  if (logo) { const lw = 600, lh = logo.naturalHeight * lw / logo.naturalWidth; g.drawImage(logo, (W - lw) / 2, 24, lw, Math.min(lh, 380)); }
  const px = 70, py = 420, pw = W - 140, ph = 500;
  g.fillStyle = "#3a2414"; shRR(g, px, py + 14, pw, ph, 44); g.fill();
  g.fillStyle = "#f3ead6"; shRR(g, px, py, pw, ph, 44); g.fill(); g.lineWidth = 10; g.strokeStyle = "#3a2414"; g.stroke();
  g.textAlign = "center"; g.textBaseline = "alphabetic"; const cx = W / 2;
  g.fillStyle = "#9b7a5c"; shFit(g, I.tag, '800 #px "Baloo 2"', 36, pw - 80); g.fillText(I.tag, cx, py + 70);
  g.fillStyle = "#3a2414"; shFit(g, I.title, "#px Bangers", 104, pw - 80); g.fillText(I.title, cx, py + 180);
  g.lineJoin = "round";
  if (I.big != null) {
    const t = I.big.toLocaleString("en-US"); shFit(g, t, "#px Bangers", 150, pw - 260); const tw = g.measureText(t).width; const tf = g.font; g.font = '800 34px "Baloo 2"'; const lw2 = g.measureText("SCORE").width + 18; g.font = tf;
    g.textAlign = "left"; const x0 = cx - (tw + lw2) / 2; g.lineWidth = 12; g.strokeStyle = "#3a2414"; g.strokeText(t, x0, py + 335); g.fillStyle = "#ff8a1f"; g.fillText(t, x0, py + 335);
    g.font = '800 34px "Baloo 2"'; g.fillStyle = "#9b7a5c"; g.fillText("SCORE", x0 + tw + 18, py + 330); g.textAlign = "center";
    g.strokeStyle = "rgba(58,36,20,.25)"; g.lineWidth = 3; g.setLineDash([10, 10]); g.beginPath(); g.moveTo(px + 50, py + 370); g.lineTo(px + pw - 50, py + 370); g.stroke(); g.setLineDash([]);
    I.stats.forEach(([v, l], i) => { const x = px + pw * (i + .5) / 4; g.fillStyle = "#3a2414"; g.font = "70px Bangers"; g.fillText(i === 3 ? `${v}★` : String(v), x, py + 445); g.fillStyle = "#9b7a5c"; g.font = '800 26px "Baloo 2"'; g.fillText(l, x, py + 480); });
  } else {
    const n = I.stars || 0; g.font = "150px Bangers"; const sw = 150;
    for (let i = 0; i < 5; i++) { const x = cx + (i - 2) * sw; g.lineWidth = 12; g.strokeStyle = "#3a2414"; g.strokeText("★", x, py + 360); g.fillStyle = i < n ? "#ffb400" : "#e6dcc6"; g.fillText("★", x, py + 360); }
    g.fillStyle = "#9b7a5c"; g.font = '800 34px "Baloo 2"'; g.fillText(`WORLD TOUR · ${I.tot} / 150 ★`, cx, py + 450);
  }
  if (hero) { const hh = 400, hw = Math.min(460, hero.naturalWidth * hh / hero.naturalHeight); g.drawImage(hero, 40, H - hh - 20, hw, hh); }
  const bx = 470, bw2 = W - bx - 50;
  g.textAlign = "center"; g.font = "78px Bangers"; g.lineWidth = 12; g.strokeStyle = "#3a2414"; g.strokeText(I.call, bx + bw2 / 2, 1050); g.fillStyle = "#fff"; g.fillText(I.call, bx + bw2 / 2, 1050);
  g.fillStyle = "#3a2414"; shRR(g, bx, 1092, bw2, 112, 56); g.fill(); g.fillStyle = "#ff5fa2"; shRR(g, bx, 1080, bw2, 112, 56); g.fill(); g.lineWidth = 7; g.strokeStyle = "#3a2414"; g.stroke();
  g.fillStyle = "#fff"; g.font = "70px Bangers"; g.fillText("PLAY FREE ▶", bx + bw2 / 2, 1160);
  g.font = '800 34px "Baloo 2"'; g.lineWidth = 8; g.strokeStyle = "rgba(30,16,6,.85)"; g.strokeText("playcapybarasquad.com", bx + bw2 / 2, 1268); g.fillStyle = "#fff"; g.fillText("playcapybarasquad.com", bx + bw2 / 2, 1268);
  return cv;
}
let shBusy = false;
async function shareResult(o) {
  if (shBusy) return; shBusy = true; const I = shInfo(o);
  try {
    const cv = await shareCard(o), blob = await new Promise(r => cv.toBlob(r, "image/png"));
    const file = blob && typeof File === "function" ? new File([blob], "capybara-squad.png", { type: "image/png" }) : null;
    if (file && navigator.canShare && navigator.canShare({ files: [file] })) await navigator.share({ files: [file], title: "Capybara Squad", text: I.text });
    else if (navigator.share) await navigator.share({ title: "Capybara Squad", text: I.text, url: SHARE_URL });
    else if (blob) { const a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = "capybara-squad.png"; document.body.appendChild(a); a.click(); setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 4000); try { toast("IMAGE SAVED · share it with your squad!", "HQ", 2200); } catch (e) {} }
  } catch (e) { if (!(e && e.name === "AbortError")) { try { toast("Sharing is not available here", "HQ", 2000); } catch (er) {} } }
  shBusy = false;
}
window.__shareCard = o => shareCard(o); window.__shareInfo = o => shInfo(o);
document.addEventListener("click", e => { if (!e.target.closest("#btnShare")) return; try { SFX.init(); snd("uiTap"); } catch (er) {} shareResult({ kind: "over" }); });''')

# CSS am Ende des letzten Style-Blocks
rep('''#ovMap .mapBar .mapWorldBtn{display:none!important}   /* V416 */
</style>''', '''#ovMap .mapBar .mapWorldBtn{display:none!important}   /* V416 */
/* V418: SHARE */
.shareBtn{align-self:center!important;margin:0 0 0 10px!important;min-height:0!important;height:30px!important;width:auto!important;padding:0 14px!important;border-radius:999px!important;border:2px solid #3a2414!important;background:#ff5fa2!important;color:#fff!important;font-family:Bangers,system-ui!important;font-size:16px!important;letter-spacing:.06em!important;line-height:1!important;box-shadow:0 3px 0 #3a2414!important;display:inline-flex!important;flex-direction:row!important;align-items:center!important;justify-content:center!important;flex:0 0 auto!important;gap:0!important}
.shareBtn::before{content:"";width:14px;height:14px;margin-right:6px;background:no-repeat center/contain url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Ccircle cx='18' cy='5' r='3' fill='white'/%3E%3Ccircle cx='6' cy='12' r='3' fill='white'/%3E%3Ccircle cx='18' cy='19' r='3' fill='white'/%3E%3Cpath d='M8.6 13.5l6.8 4M15.4 6.5l-6.8 4' stroke='white' stroke-width='2.2'/%3E%3C/svg%3E")}
#rpRes .rpShare{margin:6px auto 0!important;height:40px!important;font-size:20px!important;padding:0 20px!important}
</style>''')

open(dst, "w", encoding="utf-8").write(s)
print("ok")
