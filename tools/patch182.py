s=open('v181.html',encoding='utf-8').read()
def rep(a,b,cnt=1):
    global s
    n=s.count(a); assert n==cnt,(n,a[:60]); s=s.replace(a,b)
# 1 Pause-Knopf auf Höhe der oberen Kapsel-Reihe
rep('if (rr) { x = tr ? tr.left + (tr.width - d) / 2 : rr.right - d; y = dr2 ? dr2.top - d : rr.top - d + 8; }',
    'if (rr) { x = rr.left + (rr.width - d) / 2; y = dr2 ? dr2.top + (dr2.height - d) / 2 : rr.top - d + 8; }   /* V182: auf Höhe der oberen Kapsel-Reihe (Runter), über «Rechts» */')
# 2 rosa Punkt: versteckter Nachhol-Knopf war wegen display:flex!important sichtbar
rep('#hkMiss[hidden]{display:none}','#hkMiss[hidden]{display:none!important}')
# 4 nach Boss-Hack 2 s Zeitlupe (30 %)
rep('function closeHack() { HK.coach = false;','function closeHack() { window.__hackBack = true; HK.coach = false;')
rep('function resumeK() { if (performance.now() < (window.__holdUntil || 0)) return 0;','function resumeK() { if (performance.now() < (window.__holdUntil || 0)) return 0; if (performance.now() < (window.__slowUntil || 0)) return 0.3;   /* V182: nach Boss-Hack 2 s Zeitlupe */')
rep('if (was && !blocked) { window.__holdUntil = performance.now() + 900; RESUME_UNTIL = performance.now() + 900 + 1800; }','if (was && !blocked) { window.__holdUntil = performance.now() + 900; RESUME_UNTIL = performance.now() + 900 + 1800; if (window.__hackBack) { window.__hackBack = false; window.__slowUntil = window.__holdUntil + 2000; RESUME_UNTIL = window.__slowUntil + 1500; } }')
# 5 Boss-Signal als Sprechblase des Generals (kein Banner über dem Feld, kein zusätzlicher Hinweis)
rep(' setTimeout(() => hint("hack", "BOSS SIGNAL", "Tap the banner within 20 s to bet gold on a hack duel.", "hackPill"), 500);','')
# 6 Coach-Training kostet 99 Gold
rep('const COACH_COST = 100;','const COACH_COST = 99;')
rep('ver: "V181", wave: S.wave','ver: "V182", wave: S.wave')
# 3 Anzeige oben: feste Breiten, damit nichts mehr seitlich wandert
css='''<style id="v182">
/* V182: Anzeige oben stabil – feste Breiten, Zahlen zentriert */
html body:has(.bar) .bar>div.score.score{width:96px!important;min-width:96px!important;max-width:96px!important;box-sizing:border-box!important;justify-content:center!important;align-items:center!important}
html body .bar>div.score.score b{font-variant-numeric:tabular-nums}
html body:has(.bar) .bar>div.grp.grp{width:104px!important;min-width:104px!important;max-width:104px!important;box-sizing:border-box!important;justify-content:center!important}
.bar>.grp b{font-variant-numeric:tabular-nums}
html body:has(.bar) .bar>div.cell.cell{width:56px!important;min-width:56px!important;max-width:56px!important;box-sizing:border-box!important;justify-content:center!important}
/* V182: Tutorial und Erstes-Mal-Hinweise als Sprechblase des Generals – oben neben ihm, das Feld bleibt frei */
#coach.genTalk .coachCard{position:fixed!important;left:var(--gtL)!important;top:var(--gtT)!important;width:var(--gtW)!important;right:auto!important;bottom:auto!important;box-sizing:border-box!important;transform:none!important;margin:0!important;z-index:70!important;background:#fff!important;color:#3a2414!important;border:3px solid #3a2414!important;border-radius:16px!important;box-shadow:0 4px 0 #3a2414,0 10px 22px rgba(0,0,0,.35)!important;padding:6px 10px 6px 12px!important;display:grid!important;grid-template-columns:1fr auto;grid-template-areas:"st sk" "t t" "s s";align-items:center;gap:1px 8px!important;text-align:left!important;max-width:none!important;animation:popInL .28s cubic-bezier(.2,1.3,.4,1) both}
#coach.genTalk .coachCard::before{content:"";position:absolute;left:-15px;top:16px;width:16px;height:20px;background:#3a2414;clip-path:polygon(100% 0,0 50%,100% 100%)}
#coach.genTalk .coachCard::after{content:"";position:absolute;left:-9px;top:20px;width:11px;height:12px;background:#fff;clip-path:polygon(100% 0,0 50%,100% 100%)}
#coach.genTalk .coachStep{grid-area:st;justify-self:start;background:#ffd166!important;color:#3a2414!important}
#coach.genTalk #coachT{grid-area:t;color:#3a2414!important;font-size:clamp(15px,4.4vw,18px)!important;line-height:1.05!important;text-shadow:none!important;-webkit-text-stroke:0!important}
#coach.genTalk #coachS{grid-area:s;color:#5a4030!important;font-size:12px!important;line-height:1.2!important}
#coach.genTalk #coachSkip{grid-area:sk;margin:0!important;min-height:22px!important;height:22px!important;font-size:10px!important;padding:0 8px!important;opacity:.75}
html body #hackPill.genTalk{position:fixed!important;left:var(--gtL)!important;top:var(--gtT)!important;width:var(--gtW)!important;right:auto!important;bottom:auto!important;transform:none!important;margin:0!important;box-sizing:border-box!important;z-index:69!important;height:auto!important;min-height:0!important;background:#fff!important;border:3px solid #3a2414!important;border-radius:16px!important;box-shadow:0 4px 0 #3a2414,0 10px 22px rgba(0,0,0,.35)!important;padding:5px 10px 5px 8px!important;display:flex!important;flex-direction:row!important;align-items:center!important;justify-content:flex-start!important;gap:8px!important;animation:popInL .28s cubic-bezier(.2,1.3,.4,1) both!important}
html body #hackPill.genTalk[hidden]{display:none!important}
html body #hackPill.genTalk::before{content:"";position:absolute;left:-15px;top:16px;width:16px;height:20px;background:#3a2414;clip-path:polygon(100% 0,0 50%,100% 100%)}
html body #hackPill.genTalk::after{content:"";position:absolute;left:-9px;top:20px;width:11px;height:12px;background:#fff;clip-path:polygon(100% 0,0 50%,100% 100%)}
html body #hackPill.genTalk .hpFace{width:30px!important;height:28px!important;flex:0 0 auto!important;position:static!important;margin:0!important}
html body #hackPill.genTalk .hpFace svg{width:30px!important;height:28px!important}
html body #hackPill.genTalk .hpTxt{display:flex!important;flex-direction:column!important;align-items:flex-start!important;flex:1 1 auto!important;min-width:0!important}
html body #hackPill.genTalk .hpTxt small{color:#b0328c!important;-webkit-text-fill-color:#b0328c!important;font-size:10px!important;letter-spacing:.12em!important;text-shadow:none!important}
html body #hackPill.genTalk .hpTxt b{color:#3a2414!important;-webkit-text-fill-color:#3a2414!important;font-size:clamp(15px,4.4vw,18px)!important;line-height:1.05!important;text-shadow:none!important;-webkit-text-stroke:0!important}
html body #hackPill.genTalk .hpT{margin:0 0 0 auto!important;align-self:center!important;color:#3a2414!important;-webkit-text-fill-color:#3a2414!important;font-size:20px!important;padding:0!important}
html body #hackPill.genTalk.hot .hpT{color:#c0392b!important;-webkit-text-fill-color:#c0392b!important}
html body #hackPill.genTalk.fly{animation:hpAwayL .6s ease-in forwards!important}
@keyframes hpAwayL{to{transform:translateX(-40px) scale(.2)!important;opacity:0}}
/* V182: Ergebnis-Screen nach unten verlängert (über die ausgeblendete Kapsel), Scrollen bleibt für kleine Handys */
.board:has(#ovOver:not([hidden])){overflow:visible!important}
html body #ovOver:not([hidden]){bottom:auto!important;height:var(--ovH,100%)!important;box-sizing:border-box!important;z-index:45!important;border-radius:0 0 14px 14px}
/* V182: Werbebanner für Coach Ollie oben im Shop (3 Varianten im Wechsel), Abschnitt TRAINING unten entfällt */
#sheet .shopCat.cTra,#sheet .shopItem.cTra{display:none!important}
.coachAd{grid-column:1/-1!important;position:relative;display:block;width:100%;margin:2px 0 10px;padding:0;border:0;background:none;cursor:pointer;text-align:left;font:inherit;-webkit-tap-highlight-color:transparent;min-height:0!important;box-shadow:none!important}
.coachAd .ad{position:relative;overflow:hidden;border-radius:14px;border:3px solid #3a2414;box-shadow:0 4px 0 #3a2414;padding:9px 92px 9px 12px;min-height:66px;display:flex;flex-direction:column;justify-content:center;gap:2px}
.coachAd .k{font:800 10px/1 "Baloo 2",system-ui,sans-serif;letter-spacing:.16em;text-transform:uppercase}
.coachAd .h{font-family:"Bangers","Impact",sans-serif;font-size:clamp(22px,6.6vw,28px);line-height:.95;letter-spacing:.03em}
.coachAd .s{font:700 12px/1.2 "Baloo 2",system-ui,sans-serif}
.coachAd .p{position:absolute;right:8px;top:50%;width:76px;height:76px;margin-top:-38px;display:grid;place-items:center;text-align:center;font-family:"Bangers","Impact",sans-serif;line-height:.9}
.coachAd .p b{display:block;font-size:30px;font-weight:400}
.coachAd .p i{display:block;font-style:normal;font-size:13px;letter-spacing:.06em}
.coachAd .own{position:absolute;left:10px;bottom:-11px;z-index:2;font:800 11px/1 "Baloo 2",sans-serif;letter-spacing:.08em;padding:4px 9px;border-radius:99px;border:2px solid #3a2414;background:#fff;color:#3a2414}
.coachAd.poor .ad{filter:saturate(.55)}
.coachAd.shake{animation:adShake .4s}
@keyframes adShake{20%,60%{transform:translateX(-6px)}40%,80%{transform:translateX(6px)}}
/* A: Mega-Deal – Warnstreifen, Starburst */
.coachAd.vA .ad{background:repeating-linear-gradient(-45deg,#ffd23f 0 14px,#ffc400 14px 28px);color:#3a2414}
.coachAd.vA .ad::before{content:"";position:absolute;left:0;right:0;top:0;height:7px;background:repeating-linear-gradient(-45deg,#3a2414 0 8px,#ffd23f 8px 16px)}
.coachAd.vA .k{color:#d0281c}
.coachAd.vA .h{color:#d0281c;-webkit-text-stroke:1px #3a2414;text-shadow:2px 2px 0 #fff}
.coachAd.vA .p{background:#e8331f;color:#fff;clip-path:polygon(50% 0,61% 18%,82% 10%,80% 31%,100% 38%,86% 54%,98% 74%,76% 76%,70% 98%,52% 85%,32% 100%,27% 78%,4% 76%,15% 56%,0 38%,20% 30%,18% 9%,39% 18%);animation:adSpin 6s linear infinite}
.coachAd.vA .p span{display:block;animation:adSpin 6s linear infinite reverse}
/* B: Teleshopping – Pink, «CALL NOW» blinkt, Streichpreis */
.coachAd.vB .ad{background:linear-gradient(135deg,#ff4fa3,#ff7a3d);color:#fff}
.coachAd.vB .k{color:#fff;background:#3a2414;align-self:flex-start;padding:3px 7px;border-radius:4px;animation:adBlink .7s steps(2) infinite}
.coachAd.vB .h{color:#fff;-webkit-text-stroke:1px #3a2414;text-shadow:0 3px 0 #3a2414}
.coachAd.vB .s{color:#fff}
.coachAd.vB .p{background:#fff;color:#ff2d7a;border:3px solid #3a2414;border-radius:50%;transform:rotate(-12deg);animation:adWob 1.2s ease-in-out infinite}
.coachAd.vB .p s{display:block;font-size:13px;color:#3a2414;text-decoration-thickness:2px}
/* C: Arcade – dunkel, Neonrand pulsiert */
.coachAd.vC .ad{background:radial-gradient(120% 140% at 0 0,#3b2a6b,#160f2e);color:#e9fff4;border-color:#3a2414;animation:adNeon 1.1s ease-in-out infinite}
.coachAd.vC .k{color:#7dffb2}
.coachAd.vC .h{color:#ffe14d;text-shadow:0 0 10px rgba(255,225,77,.7),0 2px 0 #3a2414}
.coachAd.vC .s{color:#c9b8ff}
.coachAd.vC .p{background:#7dffb2;color:#160f2e;border:3px solid #3a2414;border-radius:16px;transform:rotate(6deg);animation:adPop 1s ease-in-out infinite}
@keyframes adSpin{to{transform:rotate(360deg)}}
@keyframes adBlink{50%{opacity:.25}}
@keyframes adWob{0%,100%{transform:rotate(-12deg) scale(1)}50%{transform:rotate(-6deg) scale(1.1)}}
@keyframes adNeon{0%,100%{box-shadow:0 4px 0 #3a2414,0 0 0 0 rgba(125,255,178,.0)}50%{box-shadow:0 4px 0 #3a2414,0 0 14px 4px rgba(125,255,178,.75)}}
@keyframes adPop{0%,100%{transform:rotate(6deg) scale(1)}50%{transform:rotate(2deg) scale(1.08)}}
@media (prefers-reduced-motion:reduce){.coachAd *{animation:none!important}}
@keyframes popInL{0%{transform:scale(.3);opacity:0;transform-origin:0 26px}100%{transform:scale(1);opacity:1}}
</style>
'''
i=s.rfind('</body>'); s=s[:i]+css+s[i:]
js='''
/* V182: Tutorial-Karte sitzt als Sprechblase rechts neben dem General */
(() => {
  const place = () => { const c = document.getElementById("coach"), g = document.getElementById("genAv"); if (!c || c.hidden || !g) return;
    const gr = g.getBoundingClientRect(); if (!gr.width) { c.classList.remove("genTalk"); return; }
    const card = c.querySelector(".coachCard"), left = Math.round(gr.right + 14), pt = document.getElementById("bPauseTop"), pr = pt && pt.getClientRects().length ? pt.getBoundingClientRect() : null, edge = pr && pr.left > left + 180 ? pr.left - 6 : innerWidth - 8, w = Math.max(180, edge - left);
    c.classList.add("genTalk"); card.style.setProperty("--gtL", left + "px"); card.style.setProperty("--gtT", Math.round(Math.max(4, gr.top + 2)) + "px"); card.style.setProperty("--gtW", w + "px"); };
  const placeHack = () => { const h = document.getElementById("hackPill"), g = document.getElementById("genAv"), c = document.getElementById("coach"); if (!h || !g) return; const gr = g.getBoundingClientRect(); if (!gr.width) { h.classList.remove("genTalk"); return; }
    const left = Math.round(gr.right + 14), pt = document.getElementById("bPauseTop"), pr = pt && pt.getClientRects().length ? pt.getBoundingClientRect() : null, edge = pr && pr.left > left + 180 ? pr.left - 6 : innerWidth - 8;
    h.classList.add("genTalk"); h.style.setProperty("--gtL", left + "px"); h.style.setProperty("--gtW", Math.max(180, edge - left) + "px");
    const cardUp = c && !c.hidden && c.classList.contains("genTalk"), ch = cardUp ? c.querySelector(".coachCard").getBoundingClientRect() : null; h.style.setProperty("--gtT", Math.round(ch ? ch.bottom + 8 : Math.max(4, gr.top + 2)) + "px"); };
  setInterval(() => { try { placeHack(); } catch (e) {} }, 200);
  /* Coach-Werbebanner oben im Shop */
  const ADS = {
    vA: (n) => `<span class="k">Mega deal · today only</span><span class="h">BEAT THE BOSS!</span><span class="s">Coach Ollie trains you: 10 practice hacks, no stake.</span><span class="p"><span><b>99</b><i>GOLD</i></span></span>`,
    vB: (n) => `<span class="k">Call now!</span><span class="h">HACK LIKE A PRO</span><span class="s">Book Coach Ollie · 10 duels · zero risk!</span><span class="p"><span><s>200</s><b>99</b><i>GOLD</i></span></span>`,
    vC: (n) => `<span class="k">Boss keeps winning?</span><span class="h">GET COACHED!</span><span class="s">Coach Ollie · 10 training duels · tips after every round</span><span class="p"><span><b>99</b><i>GOLD</i></span></span>` };
  let adSeq = 0; try { adSeq = +(localStorage.getItem("tarnturm-adseq") || 0); } catch (e) {}
  const putAd = () => { const sh = document.getElementById("sheet"); if (!sh || sh.hidden) return; const tile = sh.querySelector('.shopItem.cTra'), first = sh.querySelector(".shopCat"); if (!tile || !first || sh.querySelector(".coachAd")) return;
    const v = ["vA", "vB", "vC"][adSeq % 3]; adSeq++; try { localStorage.setItem("tarnturm-adseq", String(adSeq)); } catch (e) {}
    const n = typeof coachLeft === "function" ? coachLeft() : 0, poor = typeof S !== "undefined" && S && S.gold < COACH_COST;
    const b = document.createElement("button"); b.type = "button"; b.className = "coachAd " + v + (poor ? " poor" : ""); b.setAttribute("aria-label", "Book Coach Ollie for 99 gold");
    b.innerHTML = `<span class="ad">${ADS[v](n)}</span>${n ? `<span class="own" data-train="1">TRAIN NOW ▶ ×${n}</span>` : ""}`;
    first.parentNode.insertBefore(b, first);
    };
  window.addEventListener("click", e => { const b = e.target && e.target.closest && e.target.closest(".coachAd"); if (!b) return; e.stopImmediatePropagation(); e.preventDefault();
      if (e.target.closest("[data-train]")) { if (coachLeft() > 0) { closeSheet(); startCoach(); } return; }
      if (!S || S.gold < COACH_COST) { try { snd("nope"); } catch (x) {} b.classList.remove("shake"); void b.offsetWidth; b.classList.add("shake"); return; }
      S.gold -= COACH_COST; coachSet(coachLeft() + 10); try { snd("shopBuy"); } catch (x) {} toast(`COACH OLLIE · ${coachLeft()} practice hacks`, "ARMORY"); renderShop(); }, true);
  setInterval(() => { try { putAd(); } catch (e) {} }, 120);
  const growOver = () => { const o = document.getElementById("ovOver"), bd = document.getElementById("board"); if (!o || o.hidden || !bd) return; const br = bd.getBoundingClientRect(), sab = parseFloat(getComputedStyle(document.documentElement).paddingBottom) || 0, k = br.height ? bd.offsetHeight / br.height : 1, h = Math.round(Math.max(bd.offsetHeight, (innerHeight - br.top - 6 - sab) * k)); const v = h + "px"; if (o.style.getPropertyValue("--ovH") !== v) o.style.setProperty("--ovH", v); };
  setInterval(() => { try { growOver(); } catch (e) {} }, 150); addEventListener("resize", growOver);
  { const f1 = tutPlace; tutPlace = function () { const r = f1.apply(this, arguments); try { place(); } catch (e) {} return r; }; const f2 = hint; hint = function () { const r = f2.apply(this, arguments); try { place(); } catch (e) {} return r; }; }
  setInterval(() => { try { place(); } catch (e) {} }, 250);
})();
'''
k=s.rfind('})();\n</script>'); assert k>0; s=s[:k]+js+s[k:]
open('v182.html','w',encoding='utf-8').write(s)
print('ok')
