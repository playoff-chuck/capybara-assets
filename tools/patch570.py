#!/usr/bin/env python3
# V570 (Martin 10.11. 23:03–23:12): Tutorial als Kurs mit 10 Lektionen im Duolingo-Stil (Capybara-Design).
# - Streifen oben statt Punkte/Leben/Gold: Logo, «TUTORIAL», 10 Kreise, jede fertige Lektion bekommt ein grünes Häkchen + Lob.
# - Lektionen: 1 Drop · 2 Drehen · 3 Reihe füllen (+ Ränder zählen nicht) · 4 Turm bauen · 5 am Rand · 6 MG · 7 Ring ·
#   8 mit Blöcken zerquetschen · 9 Spezialmittel (Sniper geschenkt, SHOP → USE → Ziel) · 10 zweiter Turm (+ verlorener Turm).
# - Urkunde erst nach Lektion 10 (am Ende der laufenden Welle). Tipps, die der Kurs abdeckt, kommen danach nicht mehr.
# - TNT ohne Hinweis. Monster: W1–10 je +5 % (W10 +50 %), W11–20 je −5 % zurück, ab W20 normal (nicht im Nuts-Modus).
import sys, json
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V569";', 'const GAME_VER = "V570";')

# --- Monster-Tempo
rep('  const spF = ffOn() ? sp * 1.7 : sp;',
    '  const spF = (ffOn() ? sp * 1.7 : sp) * (S.nuts ? 1 : (w => w <= 10 ? 1 + 0.05 * Math.max(0, w) : w <= 20 ? 1 + 0.05 * (20 - w) : 1)(S.wave | 0));   /* V570: W1–10 +5 % je Welle, W11–20 wieder −5 % je Welle */')

# --- TNT ohne Hinweis
rep('  if (TUT.on || LS.get("tarnturm-hint-" + key) === "1" || hintKey) return;',
    '  if (key === "tnt" || TUT.on || LS.get("tarnturm-hint-" + key) === "1" || hintKey) return;   /* V570: TNT ohne Hinweis */')

# --- 10 Lektionen
a = s.index("const TUT_STEPS = ["); b = s.index("\n];\n", a) + 4
LESSONS = r'''const TUT_STEPS = [   /* V570: Kurs mit 10 Lektionen */
  { t: "DROP A BLOCK", s: "Tap DROP. Blocks are your ground.", at: "bDrop", ar: "drop", done: () => (TUT.dropTap || 0) > 0 },
  { t: "TURN YOUR BLOCKS!", s: "Tap the yellow button in the middle to turn the falling block.", at: "bRot", ar: "rot", rot: 1, done: () => (TUT.rot || 0) > (TUT.rb || 0) || TUT.t >= 15 },
  { t: "FILL A ROW – IT DISAPPEARS!", s: "A full row vanishes and pays gold. The outer squares at the left and right edge don't count – leave them free.", at: "board", got: 1, done: () => (S.lines | 0) > TUT.e.lines || TUT.t >= 40 },
  { t: "BUILD A TOWER", s: "Tap SHOP, then PLACE.", at: "bBuild", ar: "build", fast: 1, done: () => S.mode === "build" || S.towers.size > TUT.b.tw },
  { t: "PICK A BLOCK AT THE EDGE", s: "Tap a block at the edge of the field – a tower there reaches the monsters on the ring.", at: "board", ar: "edge", fast: 1, done: () => S.towers.size > TUT.b.tw },
  { t: "ARM IT", s: "Buy the MG. Then tap Done.", at: "sheet", ar: "arm", fast: 1, done: () => [...S.towers.values()].reduce((a, t) => a + t.w.length, 0) > TUT.b.wp && !S.sel },
  { t: "MONSTERS RUN THE RING", s: "They run around the field. Each one that gets all the way round costs a ♥ life – towers and falling blocks splat them.", at: "board", ar: "ring", got: 1, wave: 1, done: () => TUT.t >= 12 || (S.kills | 0) > TUT.e.k + 2 },
  { t: "SPLAT THEM WITH BLOCKS!", s: "Blocks squash monsters. Drop a block right onto them – tap DROP.", at: "bDrop", ar: "splat", got: 1, done: () => (S.splatN | 0) > TUT.e.sp || TUT.t >= 35 },
  { t: "USE A SPECIAL", s: "HQ gives you a Sniper strike. Tap SHOP, then USE – then tap a spot on the field.", at: "bBuild", ar: "spec", enter: () => { S.snipes = (S.snipes | 0) + 1; TUT.e.sn = S.snipes; }, done: () => (S.snipes | 0) < TUT.e.sn || TUT.t >= 60 },
  { t: "BUILD A SECOND TOWER", s: "Towers can fall when their block disappears – then just build a new one. Two towers at the edge hold the ring much better.", at: "bBuild", ar: "tower2", fast: 1, enter: () => { try { S.gold = Math.max(S.gold | 0, TOWER_COST + ((WEAP.mg && WEAP.mg.cost) | 0)); } catch (e) {} }, done: () => S.towers.size > TUT.e.tw || TUT.t >= 45 },
];
const TUT_SNAP = () => ({ lines: S.lines | 0, sp: S.splatN | 0, k: S.kills | 0, tw: S.towers.size, wp: [...S.towers.values()].reduce((a, t) => a + t.w.length, 0), sn: S.snipes | 0 });
/* V570: Kurs-Streifen (Duolingo-Stil, Capybara-Design) */
try { (() => {
  const N = TUT_STEPS.length, bar = document.createElement("div"); bar.id = "tutBar"; bar.hidden = true;
  let dots = ""; for (let i = 0; i < N; i++) dots += '<span class="tbDot" data-i="' + i + '" style="background-image:url(img/tut_ic' + i + '.webp?v=570)">' + (i + 1) + '</span>';
  bar.innerHTML = '<div class="tbMain"><div class="tbHead"><div class="tbLogo"></div><b>TUTORIAL</b><span class="tbCnt"></span></div><div class="tbTrack"><div class="tbLine"><i></i></div>' + dots + '</div></div>';
  document.body.appendChild(bar);
  const pr = document.createElement("div"); pr.id = "tutPraise"; pr.innerHTML = '<img alt=""><span></span>'; document.body.appendChild(pr);
  const PRAISE = ["GREAT!", "NICE ONE!", "WELL DONE!", "SUPER!", "PERFECT!", "THAT'S IT!", "TOP!", "BRAVO!", "AWESOME!", "YOU GOT IT!"];
  let doneN = 0, prT = 0;
  const D = i => bar.querySelector('.tbDot[data-i="' + i + '"]');
  function paint(cur) { for (let i = 0; i < N; i++) { const d = D(i); d.classList.toggle("ok", i < doneN); d.classList.toggle("cur", i === cur && i >= doneN); }
    bar.querySelector(".tbLine i").style.width = (Math.min(doneN, N - 1) / (N - 1) * 100) + "%"; bar.querySelector(".tbCnt").textContent = doneN + "/" + N; }
  function fit() { try { const bd = document.getElementById("board"); if (bd) { const top = bd.getBoundingClientRect().top; if (top > 40) bar.style.minHeight = Math.round(top - 2) + "px"; } document.body.style.setProperty("--tbH", bar.offsetHeight + "px"); bar.classList.toggle("away", !!(S && (S.shop || S.sel))); } catch (e) {} }
  function show() { if (!bar.hidden && bar.classList.contains("on")) return; bar.hidden = false; try { const lg = document.getElementById("logoHero"); bar.querySelector(".tbLogo").style.backgroundImage = 'url("' + ((lg && lg.src) || "icons/icon-192.png") + '")'; } catch (e) {} fit(); document.body.classList.add("tutBarOn"); requestAnimationFrame(() => bar.classList.add("on")); }
  window.__tutBar = {
    set(i) { if (i === 0) doneN = 0; show(); paint(i); },
    done(i) { doneN = Math.max(doneN, i + 1); paint(i + 1); const d = D(i); if (d) { d.classList.remove("pop"); void d.offsetWidth; d.classList.add("pop"); }
      try { snd("powerup"); } catch (e) {}
      pr.querySelector("img").src = "img/tut_cheer.webp?v=570";
      pr.querySelector("span").textContent = PRAISE[i % PRAISE.length];
      pr.style.top = Math.round(window.innerHeight * 0.42) + "px"; pr.classList.add("on"); clearTimeout(prT); prT = setTimeout(() => pr.classList.remove("on"), 1300); },
    hide() { bar.classList.remove("on"); document.body.classList.remove("tutBarOn"); setTimeout(() => { if (!bar.classList.contains("on")) bar.hidden = true; }, 400); }
  };
  setInterval(() => { try { if (!bar.hidden && (typeof TUT === "undefined" || !TUT.on || !S || !S.started || S.over)) window.__tutBar.hide(); else if (!bar.hidden) fit(); } catch (e) {} }, 500);
})(); } catch (e) { console.error("v570 bar", e); }
'''
s = s[:a] + LESSONS + s[b:]

rep('function tutStart() { TUT.dropTap = 0;', 'function tutStart() { TUT.dropTap = 0; TUT.e = TUT_SNAP();')

# tutShow: Basis je Lektion, Enter-Hook, Knopf «Got it» nur bei Lektionen ohne feste Aktion
rep('function tutShow() { const st = TUT_STEPS[TUT.step]; if (st.rot)',
    'function tutShow() { const st = TUT_STEPS[TUT.step]; TUT.e = TUT_SNAP(); try { if (st.enter) st.enter(); } catch (e) {} try { window.__tutBar && window.__tutBar.set(TUT.step); } catch (e) {} if (st.rot)')
rep('const last = TUT.step >= 4;   /* V545: Schritt 5 und 6 mit GOT IT */', 'const last = !!st.got;   /* V570: «Got it» bei Lektionen ohne Pflicht-Aktion */')

# tutTick: Welle erst mit Lektion 7, schnelle Bau-Lektionen, Häkchen + Lob
rep('  if (TUT.step < 5) { S.waveCD = Math.max(S.waveCD, 6); S.inWave = false; }',
    '  if (TUT.step < 6) { S.waveCD = Math.max(S.waveCD, 6); S.inWave = false; }')
rep('if ((TUT.t >= 4 || (TUT.step >= 1 && TUT.step <= 3)) && st.done()) {',
    'if ((TUT.t >= 4 || st.fast) && st.done()) {')
rep('TUT.step++; if (TUT.step >= TUT_STEPS.length) { tutEnd(false); return; } TUT.t = 0; if (TUT.step === 5) S.waveCD = 2; tutShow(); }',
    'tutNext(); }')
rep('function tutTick(dt) {',
    '''function tutNext() { try { window.__tutBar && window.__tutBar.done(TUT.step); } catch (e) {} TUT.step++; if (TUT.step >= TUT_STEPS.length) { tutEnd(false); return; } TUT.t = 0; if (TUT_STEPS[TUT.step].wave) S.waveCD = 2; tutShow(); }   /* V570 */
function tutTick(dt) {''')
rep('if (TUT.on) { if (TUT.step === 4 && TUT_STEPS.length > 5) { TUT.step = 5; TUT.t = 0; tutShow(); return; } tutEnd(TUT.step < 4); }',
    'if (TUT.on) { if (TUT_STEPS[TUT.step].got) { tutNext(); return; } tutEnd(true); }')

# tutEnd: abgedeckte Tipps danach nicht mehr zeigen
rep('function tutEnd(skipped) { TUT.on = false;',
    'function tutEnd(skipped) { if (!skipped) { try { ["rot", "0", "row", "gold", "lost", "1", "2"].forEach(k => LS.set("tarnturm-tipb-" + k, "1")); LS.set("tarnturm-hint-row1", "1"); LS.set("capy-tut-sp", "1"); } catch (e) {} } try { window.__tutBar && window.__tutBar.hide(skipped); } catch (e) {} TUT.on = false;')

# Pfeile: Lektion → Pfeilart
rep('        const k = TUT.step;\n',
    '''        const ar = (TUT_STEPS[TUT.step] || {}).ar; if (!ar) return null;   /* V570: Pfeil je Lektion */
        if (ar === "spec") { const pk = S.shop && document.getElementById("sheetIn") && document.getElementById("sheetIn").classList.contains("pk"); if (pk) return vis(document.querySelector('#sheetIn [data-pocket="snipe"]')); if (S.mode === "snipe" || sheetUp()) return null; return vis(document.getElementById("bBuild")); }
        const k = { drop: 0, splat: 0, build: 1, edge: 2, tower2: 2, arm: 3, rot: 4, ring: 5 }[ar];
''')

# --- Streifen oben + Lob
BAR = r'''<style id="v570bar">
#tutBar{position:fixed;left:0;right:0;top:0;z-index:904;padding:6px 10px 7px;box-sizing:border-box;background:#f3dfae url("img/tut_plank.webp?v=570") center/cover;border-bottom:3px solid #3a2414;box-shadow:0 4px 0 rgba(58,36,20,.3);font-family:Bangers,system-ui,sans-serif;transform:translateY(-115%);transition:transform .35s cubic-bezier(.2,1.4,.4,1)}
#tutBar.on{transform:none}
#tutBar.away{transform:translateY(-115%)}
#tutBar .tbMain{min-width:0}
#tutBar .tbHead{display:flex;align-items:center;gap:8px;color:#3a2414;line-height:1}
#tutBar .tbLogo{flex:0 0 auto;width:30px;height:30px;border-radius:9px;border:2.5px solid #3a2414;background:#7fc04a center/cover no-repeat;box-shadow:0 2px 0 #3a2414}
#tutBar .tbHead b{flex:1;font-weight:400;font-size:21px;letter-spacing:.07em;text-shadow:0 1px 0 #fff6dc}
#tutBar .tbHead span{font-size:16px;letter-spacing:.04em;color:#fff;background:#58cc02;border:2px solid #2f7d0a;border-radius:999px;padding:3px 9px 2px;box-shadow:0 2px 0 #2f7d0a}
#tutBar .tbTrack{position:relative;display:flex;justify-content:space-between;align-items:center;margin-top:7px;height:36px}
#tutBar .tbLine{position:absolute;left:14px;right:14px;top:50%;height:8px;margin-top:-4px;border-radius:4px;background:#e2cfa0;border:2px solid #3a2414;box-sizing:border-box;overflow:hidden}
#tutBar .tbLine i{display:block;height:100%;width:0;background:linear-gradient(180deg,#8fe04a,#58cc02);transition:width .5s ease}
#tutBar .tbDot{position:relative;z-index:1;width:30px;height:30px;border-radius:50%;box-sizing:border-box;background:#fff6dc center/100% 100% no-repeat;filter:grayscale(1) brightness(1.08);opacity:.62;font-size:0;transition:transform .25s,filter .25s,opacity .25s}
#tutBar .tbDot.cur{filter:none;opacity:1;transform:scale(1.28);animation:tbPulse 1s ease-in-out infinite alternate}
#tutBar .tbDot.ok{filter:none;opacity:1}
#tutBar .tbDot.ok::after{content:"✓";position:absolute;right:-4px;bottom:-4px;width:15px;height:15px;border-radius:50%;background:#58cc02;border:2px solid #fff;color:#fff;font:700 10px/15px system-ui,sans-serif;text-align:center;box-shadow:0 1px 0 #2f7d0a}
#tutBar .tbDot.pop{animation:tbPop .55s ease}
@keyframes tbPulse{from{box-shadow:0 0 0 0 rgba(255,210,58,.9)}to{box-shadow:0 0 0 7px rgba(255,210,58,0)}}
@keyframes tbPop{0%{transform:scale(1)}40%{transform:scale(1.7) rotate(-12deg)}100%{transform:scale(1)}}
body.tutBarOn header,body.tutBarOn #genAv,body.tutBarOn .score,body.tutBarOn #hud,body.tutBarOn #waveNum,body.tutBarOn #bPauseTop,body.tutBarOn .djBox,body.tutBarOn #djSong,body.tutBarOn #hkMiss,body.tutBarOn #hackPill,body.tutBarOn #awBar,body.tutBarOn #nutsBadge{visibility:hidden!important}
body.tutBarOn #coach.genTalk .coachCard{top:max(var(--gtT,0px),calc(var(--tbH,86px) + 8px))!important}
#tutPraise{position:fixed;left:50%;z-index:906;transform:translate(-50%,-14px) scale(.7);opacity:0;pointer-events:none;display:flex;align-items:center;gap:6px;padding:4px 18px 4px 4px;border-radius:999px;background:#58cc02;border:3px solid #2f7d0a;box-shadow:0 4px 0 #2f7d0a;color:#fff;font:400 24px/1 Bangers,system-ui,sans-serif;letter-spacing:.06em;text-shadow:0 2px 0 #2f7d0a;transition:opacity .2s,transform .3s cubic-bezier(.2,1.6,.4,1)}
#tutPraise.on{opacity:1;transform:translate(-50%,0) scale(1)}
#tutPraise img{width:54px;height:54px;margin:-14px 0 -8px -8px;object-fit:contain;filter:drop-shadow(0 2px 0 rgba(0,0,0,.25))}
</style>
'''
rep("</body>", BAR + "</body>")
open(dst, "w", encoding="utf-8").write(s)
print("ok")
