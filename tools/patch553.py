#!/usr/bin/env python3
# V553: Freemium-Grundgerüst, Schalter AUS (Martin 10.11.: gesperrte Karte jetzt bauen, aktiv erst wenn Ticket kaufbar).
# - FM: W1–60 gratis; World Tour Ticket 299 ₽ schaltet Asien, Nordamerika, Antarktis frei;
#   je 2 Freunde bis Welle 10 schalten den nächsten Kontinent frei (Martin 10.11. 13:22). Australien immer grau (kommt später).
# - Weltkarte: gesperrte Kontinente als Ebenen aus lock_v1 (Nano Banana Pro), ohne Orte/Wege/Nuts; Schloss antippen = Info-Karte.
# - Vorschau: localStorage capy-fm=1 (Freunde-Stub capy-fm-fr, Ticket-Stub capy-ticket=1). Banner-Varianten nur als Vorschau (__fmBanner).
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)

rep('const GAME_VER = "V552";', 'const GAME_VER = "V553";')

FM = r'''/* V553: Freemium – Schalter AUS bis das Ticket kaufbar ist (Vorschau: localStorage capy-fm=1) */
const FM = { on: (() => { try { return localStorage.getItem("capy-fm") === "1"; } catch (e) { return false; } })(), price: "299 ₽", per: 2, fw: 10,
  ticket() { try { return localStorage.getItem("capy-ticket") === "1"; } catch (e) { return false; } },
  friends() { try { return +localStorage.getItem("capy-fm-fr") || 0; } catch (e) { return 0; } },   /* später: Server-Zähler «Freunde ≥ W10» */
  open(c) { if (!FM.on || c < 2 || FM.ticket()) return true; return c - 2 < Math.floor(FM.friends() / FM.per); },
  next() { for (let c = 2; c <= 4; c++) if (!FM.open(c)) return c; return -1; } };
const FM_NAMES = ["SOUTH AMERICA", "AFRICA", "ASIA", "NORTH AMERICA", "ANTARCTICA"];
/* [Kontinent, Bild, x, y, b, h (px auf 1376×768), Schloss x %, Schloss y %] */
const FM_LOCKS = [[2, "asia", 651, 47, 632, 382, 72.3, 21.5], [3, "nam", 13, 38, 595, 432, 17.8, 22.1], [4, "ant", 99, 660, 1129, 108, 54.9, 92.7], ["aus", "aus", 1113, 429, 186, 128, 86.5, 61.2]];
window.__FM = FM;
function fmMapSync(ov, pinsEl) { try { ov.querySelectorAll(".mapLock").forEach(i => { const lc = i.dataset.lc; i.hidden = !FM.on || (lc !== "aus" && FM.open(+lc)); });
  if (!FM.on) return; FM_LOCKS.forEach(L => { if (L[0] !== "aus" && FM.open(L[0])) return; pinsEl.insertAdjacentHTML("beforeend", `<button class="mLock" data-lc="${L[0]}" style="left:${L[6]}%;top:${L[7]}%" aria-label="Locked"></button>`); }); } catch (e) {} }
function fmInfo(lc) { let ov = document.getElementById("ovFm"); if (!ov) { ov = document.createElement("div"); ov.id = "ovFm"; ov.className = "overlay"; document.body.appendChild(ov);
    ov.addEventListener("click", e => { e.stopPropagation(); const b = e.target.closest("button"); if (!b) { if (e.target === ov) ov.hidden = true; return; }
      try { snd("uiTap"); } catch (er) {} if (b.dataset.a === "inv") { try { sqInviteFrom(b); } catch (er) {} return; } if (b.dataset.a === "buy") return; ov.hidden = true; }); }
  const aus = lc === "aus", c = aus ? -1 : +lc, fr = FM.friends(), have = fr % FM.per, nx = FM.next();
  ov.innerHTML = aus ? `<div class="fmCard"><div class="fmPic" style="background-image:url(img/fm_card.webp);background-position:100% 70%"><span class="fmTag">🔒 COMING LATER</span></div><div class="fmBody"><h2>AUSTRALIA</h2><p>A new continent is on its way. Keep an eye on the map!</p><button class="fmOk" data-a="ok">OK ▶</button></div></div>`
    : `<div class="fmCard"><div class="fmPic" style="background-image:url(img/fm_card.webp)"><span class="fmTag">🎟 WORLD TOUR</span><span class="fmLockN">🔒 <span>${FM_NAMES[c]}</span></span></div><div class="fmBody">
      <h2>3 MORE CONTINENTS</h2><p>South America and Africa are free (waves 1–60). Asia, North America and Antarctica (waves 61–150) are waiting for you.</p>
      <div class="fmOpt"><b>🎟 WORLD TOUR TICKET</b><small>All 3 continents at once</small><button class="fmBuy" data-a="buy">${FM.price}</button></div>
      <div class="fmOr">OR</div>
      <div class="fmOpt"><b>👫 INVITE 2 FRIENDS</b><small>${["When 2 friends reach wave 10, ASIA opens. Free!", "When 2 friends reach wave 10, NORTH AMERICA opens. Free!", "When 2 friends reach wave 10, ANTARCTICA opens. Free!"][Math.max(0, nx - 2)]}</small><span class="fmCnt">Friends: ${have}/${FM.per}</span><button class="fmInv" data-a="inv">INVITE ▶</button></div>
      <button class="fmOk" data-a="ok">LATER</button></div></div>`;
  ov.hidden = false; try { i18nApplyAll(); } catch (e) {} try { snd("open"); } catch (e) {} }
window.__fmInfo = fmInfo;
/* Banner-Vorschau (Variante A = Karte, B = Band oben) – Auslösung W46/W54/W60 folgt nach Martins Wahl */
window.__fmBanner = (v, w) => { if (v === "A") { fmInfo(FM.next() >= 0 ? FM.next() : 2); const h = document.querySelector("#ovFm h2"), p = document.querySelector("#ovFm p");
    if (h) h.textContent = w >= 60 ? "END OF THE FREE TOUR" : `${60 - w} WAVES LEFT IN AFRICA`; if (p) p.textContent = "After wave 60 the World Tour goes on: Asia, North America and Antarctica – 90 more waves, new monsters and bosses."; try { i18nApplyAll(); } catch (e) {} return; }
  let b = document.getElementById("fmBand"); if (!b) { b = document.createElement("div"); b.id = "fmBand"; b.setAttribute("role", "button"); document.body.appendChild(b); b.addEventListener("click", e => { e.stopPropagation(); b.classList.remove("on"); fmInfo(FM.next() >= 0 ? FM.next() : 2); }); }
  b.innerHTML = `<i>🔒</i><span><b>${w >= 60 ? "FREE TOUR ENDS HERE" : `${60 - w} WAVES TO ASIA`}</b><small>Ticket ${FM.price} or 2 friends</small></span><em>▶</em>`; try { i18nApplyAll(); } catch (e) {}
  b.classList.add("on"); clearTimeout(b.__t); b.__t = setTimeout(() => b.classList.remove("on"), 9000); };
{ let dn = null; document.addEventListener("pointerdown", e => { const t = e.target.closest && e.target.closest(".mLock"); dn = t ? { lc: t.dataset.lc, x: e.clientX, y: e.clientY, t: performance.now() } : null; }, true);
  document.addEventListener("pointerup", e => { if (!dn) return; const d = dn; dn = null; if (Math.hypot(e.clientX - d.x, e.clientY - d.y) > 10 || performance.now() - d.t > 700) return; setTimeout(() => fmInfo(d.lc), 30); }, true); }
const CONTS = ['''
rep('const CONTS = [', FM)

rep('''<img class="mapImg" src="img/worldmap.webp" alt="World map" draggable="false">''',
    '''<img class="mapImg" src="img/worldmap.webp" alt="World map" draggable="false">${FM_LOCKS.map(L => `<img class="mapLock" data-lc="${L[0]}" src="img/lock_${L[1]}.webp" alt="" draggable="false" hidden style="left:${(L[2] / 13.76).toFixed(3)}%;top:${(L[3] / 7.68).toFixed(3)}%;width:${(L[4] / 13.76).toFixed(3)}%;height:${(L[5] / 7.68).toFixed(3)}%">`).join("")}''')

rep('''MAP_PTS.forEach((P, c) => P.forEach((p, i) => { const gi = c * 6 + i, st =''',
    '''MAP_PTS.forEach((P, c) => P.forEach((p, i) => { if (!FM.open(c)) return; const gi = c * 6 + i, st =''')
rep('''const P = MAP_PTS[c]; if (!P) return "";''', '''const P = MAP_PTS[c]; if (!P || !FM.open(c)) return "";''')
rep('''pathEl.innerHTML = MAP_PTS.map((P, c) => `<polyline''', '''pathEl.innerHTML = MAP_PTS.map((P, c) => !FM.open(c) ? "" : `<polyline''')
rep('''      pinsEl.innerHTML = h;\n''', '''      pinsEl.innerHTML = h; fmMapSync(ov, pinsEl);   /* V553 */\n''')

CSS = '''#ovMap .mapLock{position:absolute;max-width:none!important;display:block;pointer-events:none}
#ovMap .mapLock[hidden]{display:none!important}
#ovMap .mLock{position:absolute;width:64px;height:64px;min-height:0;margin:0;padding:0;border:0;border-radius:50%;background:transparent;transform:translate(-50%,-50%);z-index:4;pointer-events:auto;cursor:pointer}
#ovFm{position:fixed;inset:0;z-index:1500;display:flex;align-items:center;justify-content:center;padding:16px;background:rgba(20,12,4,.62)}
#ovFm[hidden]{display:none!important}
#ovFm .fmCard{width:min(360px,100%);background:#fff6e6;color:#3a2414;border:3px solid #3a2414;border-radius:20px;box-shadow:0 6px 0 #3a2414;overflow:hidden;font-family:"Baloo 2",Nunito,system-ui,sans-serif;animation:fmIn .35s cubic-bezier(.2,1.4,.4,1)}
@keyframes fmIn{from{transform:scale(.8);opacity:0}to{transform:none;opacity:1}}
#ovFm .fmPic{position:relative;height:150px;background:#6faaab center 30%/cover;border-bottom:3px solid #3a2414}
#ovFm .fmTag{position:absolute;left:10px;top:10px;background:#ffc93c;border:2px solid #3a2414;border-radius:10px;padding:2px 9px;font:400 17px/1.2 Bangers,Oswald,system-ui;letter-spacing:.05em}
#ovFm .fmLockN{position:absolute;right:10px;bottom:10px;background:#3a2414;color:#fff6e6;border-radius:10px;padding:2px 9px;font:400 16px/1.2 Bangers,Oswald,system-ui;letter-spacing:.05em}
#ovFm .fmBody{padding:12px 14px 14px;text-align:center}
#ovFm h2{margin:0 0 4px;font:400 30px/1 Bangers,Oswald,system-ui;letter-spacing:.04em}
#ovFm p{margin:0 0 10px;font:600 14px/1.3 "Baloo 2",Nunito,system-ui}
#ovFm .fmOpt{display:grid;grid-template-columns:1fr auto;gap:2px 10px;align-items:center;text-align:left;background:#fffaf0;border:2px solid #3a2414;border-radius:14px;padding:8px 10px;box-shadow:0 2px 0 #3a2414}
#ovFm .fmOpt b{font:400 18px/1.1 Bangers,Oswald,system-ui;letter-spacing:.04em}
#ovFm .fmOpt small{grid-column:1;font:600 12px/1.25 "Baloo 2",Nunito,system-ui;color:#6b4a2b}
#ovFm .fmOpt button{grid-column:2;grid-row:1/4;min-height:0;margin:0;padding:8px 12px;border:2px solid #3a2414;border-radius:12px;font:400 19px/1 Bangers,Oswald,system-ui;letter-spacing:.04em;box-shadow:0 3px 0 #3a2414!important;-webkit-text-stroke:1px #3a2414;paint-order:stroke fill;white-space:nowrap}
#ovFm .fmBuy{background:#ff5fa2!important;color:#fff!important}
#ovFm .fmInv{background:#3fae3f!important;color:#fff!important}
#ovFm .fmCnt{grid-column:1;font:800 13px/1.2 "Baloo 2",Nunito,system-ui;color:#3fae3f}
#ovFm .fmOr{margin:6px 0;font:400 16px/1 Bangers,Oswald,system-ui;color:#8a5a2b;letter-spacing:.08em}
#ovFm .fmOk{margin:12px auto 0;display:block;min-height:0;padding:8px 22px;background:transparent!important;box-shadow:none!important;border:2px solid #3a2414;border-radius:12px;color:#3a2414;font:400 18px/1 Bangers,Oswald,system-ui;letter-spacing:.05em}
#fmBand{position:fixed;left:50%;top:calc(env(safe-area-inset-top,0px) + 132px);box-sizing:border-box;cursor:pointer;z-index:960;display:flex;align-items:center;gap:10px;width:min(340px,calc(100% - 32px));min-height:0;margin:0;padding:8px 12px;background:#3a2414;color:#fff6e6;border:2px solid #ffc93c;border-radius:16px;box-shadow:0 4px 0 rgba(0,0,0,.35);text-align:left;transform:translate(-50%,-160%);opacity:0;transition:transform .45s cubic-bezier(.2,1.4,.4,1),opacity .3s;pointer-events:none}
#fmBand.on{transform:translate(-50%,0);opacity:1;pointer-events:auto}
#fmBand i{font-style:normal;font-size:26px}
#fmBand span{flex:1;display:flex;flex-direction:column}
#fmBand b{font:400 19px/1.05 Bangers,Oswald,system-ui;letter-spacing:.05em;color:#ffc93c}
#fmBand small{font:600 12px/1.2 "Baloo 2",Nunito,system-ui}
#fmBand em{font-style:normal;font:400 20px/1 Bangers,Oswald,system-ui;background:#ff5fa2;border:2px solid #fff6e6;border-radius:10px;padding:5px 9px}
#ovMap{position:fixed;inset:0;z-index:990;'''
rep('#ovMap{position:fixed;inset:0;z-index:990;', CSS)

# Aufnahme-Links für den Trailer: ?test=wNN springt zu Welle NN, ?test=hack = Boss-Hack-Duell; Testläufe speichern nicht
rep('laser134: 134, blk: 65,', 'laser134: 134, hack: 5, blk: 65,')
rep('  if (q && map[q]) { const go = () => { setTimeout(() => { try { history.replaceState(null, "", location.pathname); } catch (e) {} devJump(map[q], q.replace(/\\d$/, ""));',
    '  if (q && /^w\\d{1,3}$/.test(q) && +q.slice(1) >= 1 && +q.slice(1) <= 150) map[q] = +q.slice(1);   /* V553: Aufnahme-Links */\n'
    '  if (q && map[q]) { const go = () => { setTimeout(() => { try { history.replaceState(null, "", location.pathname); } catch (e) {} const bak = LS.get("tarnturm-save"); devJump(map[q], /^w\\d/.test(q) ? "" : q.replace(/\\d$/, "")); try { if (bak) LS.set("tarnturm-save", bak); } catch (e) {}')
rep('function saveGame() { if (S && S.replay) {', 'function saveGame() { if (S && S.testRun) return;   /* V553: Test-/Aufnahme-Läufe überschreiben den echten Spielstand nicht */ if (S && S.replay) {')

open(dst, "w", encoding="utf-8").write(s)
print("ok")
