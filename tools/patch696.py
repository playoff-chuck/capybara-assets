# V696 (Martin 13.11. 10:28, Screenshot Zweithandy): Wegweiser am Kontinentende neu.
# 1) Oben kein Titelkasten mehr («… CLEARED!» und Erklärtext entfallen).
# 2) Zwei Infopunkte über den Wegen: rot mit ☠ über Nuts, grün mit i über dem nächsten Kontinent.
#    Antippen (am Rechner: Maus darüber) öffnet ein Infofeld in derselben Farbe, weiße Schrift. Nochmal tippen/irgendwo tippen schließt.
# 3) Unten zwei saubere Knöpfe ohne abgeschnittenen Text: «☠ NUTS / 30 crazy levels» und «AFRICA ▶ / continue the tour».
#    Der Hinweis zur Wertung (erste Runde +1 % je Level) steht jetzt im roten Infofeld.
# 4) Fehler Notfall-Kiste: Sperre (S.rescueW) wird jetzt im Spielstand gespeichert (vorher nach Neustart sofort wieder Kiste).
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf8").read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
rep('GAME_VER = "V695"', 'GAME_VER = "V696"')
# --- HTML
rep('''ovSign.innerHTML = `<div class="signBox" id="signBox"><div class="signTxt"><h2 id="signTitle">CONTINENT CLEARED!</h2><p id="signInfo"></p></div><div class="signRule" id="signRule"></div><div class="signBtns"><button id="signNuts">☠ NUTS DETOUR<small>30 crazy levels</small></button><button id="signNext">NEXT<small>continue the tour</small></button></div></div>`;''',
'''ovSign.innerHTML = `<div class="signBox" id="signBox"><div class="signTxt" hidden><h2 id="signTitle">CONTINENT CLEARED!</h2><p id="signInfo"></p></div><div class="signRule" id="signRule" hidden></div><button type="button" class="sgDot sgNuts" id="sgDotNuts" aria-label="NUTS DETOUR"><span class="sgSk">☠</span></button><button type="button" class="sgDot sgNext" id="sgDotNext" aria-label="Info"><span class="sgI">i</span></button><div class="sgPop" id="sgPop" hidden><h3 id="sgPopT"></h3><p id="sgPopP"></p><p class="sgPopR" id="sgPopR"></p></div><div class="signBtns"><button id="signNuts"><b>☠ NUTS</b><small>30 crazy levels</small></button><button id="signNext"><b>NEXT</b><small>continue the tour</small></button></div></div>`;   /* V696: Infopunkte statt Titelkasten */''')
# --- showSign: Knopftext + Infofeld zurücksetzen
rep('''$("signNext").innerHTML = `NEXT: ${NZ_NEXT[c]}<small>continue the tour</small>`; ovSign.hidden = false; snd("radio");''',
'''$("signNext").innerHTML = `<b>${NZ_NEXT[c]} ▶</b><small>continue the tour</small>`; try { window.__sgC = c; window.__sgShut && window.__sgShut(); const P = [[29, 17.5, 69, 18], [32, 20, 67, 20], [32, 21.5, 68, 21], [19, 25, 84, 35]][c] || [29, 17.5, 69, 18], bx = $("signBox"); ["--nx", "--ny", "--xx", "--xy"].forEach((k, i) => bx.style.setProperty(k, P[i])); } catch (e) {} ovSign.hidden = false; try { window.__sgFit && window.__sgFit(); } catch (e) {} snd("radio");   /* V696 */''')
# --- Infofelder: Logik
rep('''function closeSign() {''',
'''(() => {   /* V696: Infopunkte am Wegweiser */
  const pop = () => document.getElementById("sgPop"), dotN = () => document.getElementById("sgDotNuts"), dotX = () => document.getElementById("sgDotNext");
  let cur = "";
  const shut = () => { cur = ""; const p = pop(); if (p) { p.hidden = true; p.className = "sgPop"; } [dotN(), dotX()].forEach(d => d && d.classList.remove("on")); };
  const open = which => { const p = pop(); if (!p) return; const c = window.__sgC | 0;
    if (which === "nuts") { $("sgPopT").textContent = "☠ NUTS DETOUR"; $("sgPopP").innerHTML = `<span class="sgLi">${NZ_MAX} levels, each harder · ${NZ_KIT.lives} lives</span><span class="sgLi">Same kit for everyone · no shop</span><span class="sgLi">Your main run waits here</span>`;
      $("sgPopR").innerHTML = nzFirstOpen(c) ? `<b>First try: +1 % main score per level (max +${NZ_MAX} %)</b>` : "Replay: Nuts board and medals only"; }
    else { const C = CONTS[c + 1] || CONTS[CONTS.length - 1], a = NZ_BASES[c] + 1, b = NZ_BASES[c] + 30;
      $("sgPopT").textContent = `NEXT STOP: ${NZ_NEXT[c]}`;
      $("sgPopP").innerHTML = `<span class="sgLi">Waves ${a}–${b}</span><span class="sgLi">${C[2].length} new places · new music</span><span class="sgPl">${C[2].join(" · ")}</span>`;
      $("sgPopR").textContent = "Nuts stays open in the pause menu"; }
    cur = which; p.className = "sgPop " + (which === "nuts" ? "nuts" : "next"); p.hidden = false;
    try { const d = which === "nuts" ? dotN() : dotX(), bx = $("signBox"); p.style.top = (d.offsetTop + d.offsetHeight + 12) + "px"; p.style.setProperty("--ax", (d.offsetLeft + d.offsetWidth / 2 - p.offsetLeft - 11) + "px"); } catch (e) {}
    dotN().classList.toggle("on", which === "nuts"); dotX().classList.toggle("on", which !== "nuts"); try { snd("uiTap"); } catch (e) {} };
  window.__sgShut = shut;
  const fit = () => { try { document.querySelectorAll("#ovSign .signBtns b, #ovSign .signBtns small").forEach(el => { el.style.fontSize = ""; let f = parseFloat(getComputedStyle(el).fontSize) || 16; let n = 0; const W = () => el.parentNode.clientWidth - 12; while (el.scrollWidth > W() && f > 9 && n++ < 24) { f -= 0.5; el.style.fontSize = f + "px"; } }); } catch (e) {} };
  window.__sgFit = () => { [60, 300, 900].forEach(t => setTimeout(fit, t)); };
  const hov = matchMedia("(hover: hover)").matches;
  const wire = (el, which) => { if (!el) return; el.addEventListener("click", e => { e.stopPropagation(); if (cur === which) shut(); else open(which); });
    if (hov) { el.addEventListener("pointerenter", () => open(which)); el.addEventListener("pointerleave", () => { setTimeout(() => { if (!el.matches(":hover")) shut(); }, 60); }); } };
  const go = () => { wire(dotN(), "nuts"); wire(dotX(), "next"); const box = document.getElementById("signBox"); if (box) box.addEventListener("click", e => { if (cur && !e.target.closest(".sgDot") && !e.target.closest(".signBtns")) shut(); }); };
  if (document.getElementById("sgDotNuts")) go(); else setTimeout(go, 0);
})();
function closeSign() { try { window.__sgShut && window.__sgShut(); } catch (e) {}''')
# --- CSS: Knöpfe neu, Infopunkte, Infofeld
rep('''.signBtns{position:absolute;left:8px;right:8px;bottom:10px;display:flex;gap:8px}''',
'''.signBtns{position:absolute;left:8px;right:8px;bottom:10px;display:flex;gap:8px;z-index:3}''')
rep('''.signRule b{color:#ffd36a}''',
'''.signRule b{color:#ffd36a}
.signBox .signTxt[hidden],.signBox .signRule[hidden],.sgPop[hidden]{display:none!important}   /* V696 */
.signBtns button{min-height:68px!important;padding:6px 6px 7px!important;gap:3px!important;border-radius:16px!important;box-shadow:0 5px 0 #3a1d10,inset 0 2px 0 rgba(255,255,255,.35)!important;text-shadow:0 2px 0 rgba(0,0,0,.4)!important;overflow:hidden}
.signBtns button b{display:block;align-self:stretch;text-align:center;font-weight:400;font-family:Bangers,var(--f-display),sans-serif;font-size:clamp(19px,6vw,25px);line-height:1.05;letter-spacing:.04em;white-space:nowrap}
.signBtns button small{display:block;align-self:stretch;text-align:center;font-size:12px;line-height:1.15;white-space:nowrap;opacity:.92}
.sgDot{position:absolute!important;z-index:6;width:46px!important;height:46px!important;min-width:0!important;min-height:0!important;border-radius:50%!important;border:3px solid #4a2a14!important;box-shadow:0 3px 0 #2e1a0c,inset 0 2px 0 rgba(255,255,255,.28),0 5px 12px rgba(0,0,0,.4)!important;color:#fff!important;display:flex!important;align-items:center;justify-content:center;padding:0!important;margin:0!important;cursor:pointer;-webkit-tap-highlight-color:transparent;animation:sgPulse 1.8s ease-in-out infinite}
.sgDot.sgNuts{left:calc(var(--nx,29) * 1% - 23px);top:calc(var(--ny,17.5) * 1% - 23px);background:linear-gradient(180deg,#cc5546,#a23e33 55%,#8a3128)!important}
.sgDot.sgNext{left:calc(var(--xx,69) * 1% - 23px);top:calc(var(--xy,18) * 1% - 23px);right:auto!important;background:linear-gradient(180deg,#68a35f,#4b8350 55%,#3a6b44)!important}
.sgDot .sgSk{font-size:25px;line-height:1;color:#fff;filter:drop-shadow(0 2px 0 rgba(0,0,0,.35))}
.sgDot .sgI{font:700 28px/1 Georgia,"Times New Roman",serif;font-style:normal;color:#fff;text-shadow:0 2px 0 rgba(0,0,0,.35);margin-top:-2px}
.sgDot.on{animation:none;transform:scale(1.1);box-shadow:0 3px 0 #2e1a0c,0 0 0 5px rgba(255,255,255,.7)!important}
.sgDot:active{transform:translateY(2px) scale(.98)}
@keyframes sgPulse{0%,100%{transform:scale(1)}50%{transform:scale(1.09)}}
@media (prefers-reduced-motion:reduce){.sgDot{animation:none}}
.sgPop{position:absolute;left:10px;right:10px;top:30%;z-index:5;border:3px solid #4a2a14;border-radius:14px;box-shadow:0 5px 0 #3a1d10,0 10px 24px rgba(0,0,0,.45);padding:11px 13px 12px;color:#fff;text-align:left;font-family:"Baloo 2",system-ui,sans-serif;font-size:14px;line-height:1.3}
.sgPop::before{content:"";position:absolute;top:-12px;left:var(--ax,40px);width:18px;height:18px;transform:rotate(45deg);border-left:3px solid #4a2a14;border-top:3px solid #4a2a14;background:inherit}
.sgPop.nuts{background:linear-gradient(180deg,#c24e40,#9a3a2f)}.sgPop.nuts::before{background:#c24e40}
.sgPop.next{background:linear-gradient(180deg,#5f9a59,#3c6f48)}.sgPop.next::before{background:#5f9a59}
.sgPop h3{margin:0 0 5px;font-family:Bangers,var(--f-display),sans-serif;font-weight:400;font-size:23px;letter-spacing:.04em;line-height:1.05;text-shadow:0 2px 0 rgba(0,0,0,.3)}
.sgPop p{margin:0}.sgPop p+p{margin-top:7px}
.sgPop b{color:#fff;font-weight:800}.sgPop.nuts .sgPopR b{color:#ffe08a}
.sgPop .sgPl{display:block;margin-top:5px;font-size:12px;letter-spacing:.04em;opacity:.9}
.sgPop .sgPopR{font-size:13.5px}
.sgPop .sgLi{display:block;position:relative;padding-left:16px;font-weight:700;font-size:15px;line-height:1.3}.sgPop .sgLi::before{content:"•";position:absolute;left:3px}''')
# --- Notfall-Kiste: Sperre speichern
rep('''SAVE_KEYS.push("adDue");''', '''SAVE_KEYS.push("adDue"); if (!SAVE_KEYS.includes("rescueW")) SAVE_KEYS.push("rescueW");   /* V696: Sperre der Notfall-Kiste überlebt Neustart */''')
# 5) Martin 13.11. 10:30: festes Zehntonnen-Geschenk nach W8/W22 entfällt, wenn in den letzten 3 Wellen schon eine Notfall-Kiste kam.
rep('''const tg = [8, 22].includes(S.wave) && !(S.tonGift || {})[S.wave];''', '''const tg = [8, 22].includes(S.wave) && !(S.tonGift || {})[S.wave] && !((S.rescueW || -99) >= S.wave - 3);   /* V696: nicht direkt nach Notfall-Kiste */''')
# 6) Martin 13.11. 10:44: Nuts-Ende verschwand nach versehentlichem Tippen. Ergebnis-Fenster steht jetzt mindestens 3 s (Knopf gesperrt mit Countdown), danach nur per Knopf zu schließen.
rep('''ovRes.hidden = false; ovRes._c = c; ovRes._cleared = cleared; ovRes._first = n.first;''',
'''ovRes.hidden = false; ovRes._c = c; ovRes._cleared = cleared; ovRes._first = n.first;
  try { const b = $("nrBack"); clearInterval(ovRes._lt); b.disabled = true; b.classList.add("nrLock"); let k = 3; b.dataset.cd = k; ovRes._lt = setInterval(() => { k--; if (k > 0) { b.dataset.cd = k; return; } clearInterval(ovRes._lt); b.disabled = false; b.classList.remove("nrLock"); b.classList.add("nrGo"); }, 1000); } catch (e) {}   /* V696: 3 s Sperre */''')
rep('''$("nrBack").addEventListener("click", () => { SFX.init();''', '''$("nrBack").addEventListener("click", () => { if ($("nrBack").disabled) return; $("nrBack").classList.remove("nrGo"); SFX.init();''')
rep('''.signBox .signTxt[hidden],.signBox .signRule[hidden],.sgPop[hidden]{display:none!important}   /* V696 */''', '''.signBox .signTxt[hidden],.signBox .signRule[hidden],.sgPop[hidden]{display:none!important}   /* V696 */
#nrBack{position:relative}
body:has(#ovSign:not([hidden])) #buddy,body:has(#ovNutsRes:not([hidden])) #buddy{display:none!important}
#nrBack.nrLock{filter:grayscale(.7) brightness(.85);opacity:.7;pointer-events:none}
#nrBack.nrLock::after{content:attr(data-cd);position:absolute;right:10px;top:50%;transform:translateY(-50%);width:28px;height:28px;border-radius:50%;background:#3a1d10;color:#fff;font:400 18px/28px Bangers,var(--f-display),sans-serif;text-align:center}
#nrBack.nrGo{animation:nrGo 1.1s ease-in-out infinite}
@keyframes nrGo{0%,100%{transform:scale(1)}50%{transform:scale(1.04)}}''')
# 7) Martin 13.11. 10:54: Nuts-Endscreen – Knopf weg vom Bedienfeld (direkt unter dem Ergebnis, Fenster mittig), Grund des Endes groß, Titel je Grund, Ende wird mitgeschrieben.
rep('''$("nrTitle").textContent = why === "done" ? "ALL 30 CLEARED!" : rec && best ? "NEW NUTS RECORD!" : "NUTS OVER!";''',
'''$("nrTitle").textContent = why === "done" ? `ALL ${NZ_MAX} CLEARED!` : why === "quit" ? "NUTS DETOUR ENDED" : "OUT OF LIVES!";
  try { let w = $("nrWhy"); if (!w) { w = document.createElement("div"); w.id = "nrWhy"; w.className = "nrWhy"; $("nrBig").after(w); } $("nrBig").after(w); w.after($("nrBack"));
    w.textContent = why === "done" ? `All ${NZ_MAX} levels cleared` : why === "quit" ? `Detour ended at level ${cleared + 1}` : `All ${NZ_KIT.lives} lives lost in level ${cleared + 1}`; w.classList.toggle("ok", why === "done");
    if (rec && best) $("nrTag").textContent = "NEW NUTS RECORD!"; } catch (e) {}
  try { window.__mpush && window.__mpush("nzend", { d: { why: why || "lives", lv: cleared, c, first: !!n.first } }); } catch (e) {}   /* V696 */''')
rep('''$("nrSub").textContent = `${nzName(c)} · Nuts levels cleared · best ${Math.max(best, cleared)}` + (cleared >= 30 ? " · gold skull!" : cleared >= 20 ? " · silver skull!" : cleared >= 10 ? " · bronze skull!" : "");''',
'''$("nrSub").textContent = `${nzName(c)} · best ${Math.max(best, cleared)}` + (cleared >= 30 ? " · gold skull!" : cleared >= 20 ? " · silver skull!" : cleared >= 10 ? " · bronze skull!" : "");''')
rep('''.nutsRes .nutsResBox{position:relative;max-height:62vh!important;padding-top:12px!important}''',
'''.nutsRes .nutsResBox{position:relative;max-height:62vh!important;padding-top:12px!important}
.nutsRes{align-items:center!important;padding-top:24vh!important;padding-bottom:16vh!important}   /* V696: Fenster mittig, Knopf nicht im Bedienfeld */
.nutsRes .nutsResBox{max-height:60vh!important}
#nrWhy{margin:2px 14px 10px!important;padding:7px 10px;border-radius:10px;background:#c23f3f;color:#fff;font:700 15px/1.2 "Baloo 2",system-ui,sans-serif;text-align:center}
#nrWhy.ok{background:#2f8a2a}
.nutsResBox #nrBack{margin-top:0!important;margin-bottom:12px!important}
#nrBack.nrLock::after{left:12px;right:auto!important}
#nrBack.nrLock{padding-left:46px!important}''')
open(dst, "w", encoding="utf8").write(s)
print("ok V696")
