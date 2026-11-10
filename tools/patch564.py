#!/usr/bin/env python3
# V564: Tutorial nach Martins Video vom 10.11. (Analyse «Capybara – Tutorial-Video Analyse V563»), alle 10 Punkte:
# 1 Schritte mind. 4 s, Schritt 1 zählt nur echten Tipp auf DROP · 2 Pfeile richtig (DROP von der Seite, Laden → PLACE, Drehen tiefer)
# 3 Schritt 6 «Monster auf dem Ring» (Pfeil auf Leben, Welle startet) · 4 Special-Tutorial für jedes erste Special
# 5 Missions-/Beförderungs-Meldungen in W1–W2 und im Tutorial zurückhalten · 6 englische Reste übersetzt
# 7 Blue-Sprechblase nicht über offenem Menü, «First tower up» nicht im Tutorial · 8 Hinweis erste Reihe + erster TNT
# 9 erster Boss-Hack: kostenloser Proberunde · 10 Abschlusskarte am Ende von Welle 1
# dazu (Martin 17:31): Wolfgeheul −50 %, Dieb klingt tiefer (Filter; die Clips selbst: tools/thief564.py)
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)

rep('const GAME_VER = "V563";', 'const GAME_VER = "V564";')

# ---------- 1 + 3: Schritte ----------
rep('{ t: "DROP A BLOCK", s: "Tap DROP. Blocks are your ground.", at: "bDrop", done: () => S.pieceNo >= ((TUT.b && TUT.b.p) || 0) + 1 },',
    '{ t: "DROP A BLOCK", s: "Tap DROP. Blocks are your ground.", at: "bDrop", done: () => (TUT.dropTap || 0) > 0 },   /* V564: nur echter Tipp zählt */')
rep('''rot: 1, done: () => (TUT.rot || 0) > (TUT.rb || 0) || TUT.t >= 15 },''',
    '''rot: 1, done: () => (TUT.rot || 0) > (TUT.rb || 0) || TUT.t >= 15 },
  { t: "MONSTERS RUN THE RING", s: "They run around the field. Each one that gets all the way round costs a ♥ life – towers and falling blocks splat them.", at: "board", done: () => TUT.t >= 12 || (S.kills | 0) > ((TUT.b && TUT.b.k) || 0) + 2 },   /* V564: Ring-Schritt zurück */''')
rep('function tutStart() { TUT.b = { p: S.pieceNo || 0, tw: S.towers.size,',
    'function tutStart() { TUT.dropTap = 0; TUT.b = { k: S.kills | 0, p: S.pieceNo || 0, tw: S.towers.size,')
rep('if (!skipped) { toast("TUTORIAL DONE · good luck, squad", "HQ", 1800); SFX.say("Nice!"); } }',
    'if (!skipped) { toast("TUTORIAL DONE · good luck, squad", "HQ", 1800); SFX.say("Nice!"); window.__tutSumPend = performance.now(); } }   /* V564: Abschlusskarte am Wellenende */')
rep('if (TUT.step < 4) { S.waveCD = Math.max(S.waveCD, 6); S.inWave = false; }',
    'if (TUT.step < 5) { S.waveCD = Math.max(S.waveCD, 6); S.inWave = false; }   /* V564: Welle erst mit dem Ring-Schritt */')
rep('if (st.done()) { TUT.step++; if (TUT.step >= TUT_STEPS.length) { tutEnd(false); return; } TUT.t = 0; if (TUT.step === 4) S.waveCD = 2; tutShow(); }',
    'if (TUT.t >= 4 && st.done()) { TUT.step++; if (TUT.step >= TUT_STEPS.length) { tutEnd(false); return; } TUT.t = 0; if (TUT.step === 5) S.waveCD = 2; tutShow(); }   /* V564: jeder Schritt mind. 4 s */')

# ---------- 2: Pfeile ----------
rep('''        if (k === 0) return vis(document.getElementById("bDrop"));
        if (k === 4) return vis(document.getElementById("bRot"));''',
    '''        if (k === 0) { const r = vis(document.getElementById("bDrop")); return r ? { left: r.left, right: r.right, top: r.top, bottom: r.bottom, width: r.width, height: r.height, side: 1 } : null; }   /* V564: von links, nicht über dem gelben Knopf */
        if (k === 4) { const r = vis(document.getElementById("bRot")); return r ? { left: r.left, right: r.right, top: r.top, bottom: r.bottom, width: r.width, height: r.height, deep: 1 } : null; }
        if (k === 5) { const bd = document.getElementById("board"); if (!bd) return null; const b = bd.getBoundingClientRect(); let x = b.right - 16, y = b.top + b.height * 0.32;   /* V564: Pfeil auf ein Monster im Ring (die Karte oben deckt die Leben-Anzeige) */
          try { const m = S.monsters.find(q => q && !q.dead && q.cy >= 1); if (m) { const pt = cvPt(m.cx + 0.5, m.cy + 0.5); if (pt && pt.y > b.top + 110) { x = pt.x; y = pt.y; } } } catch (e) {}
          return { left: x - 10, right: x + 10, top: y - 12, bottom: y + 12, width: 20, height: 24 }; }''')
rep('''        if (k === 1) { if (sheetUp() && S.shop) { const b = btnTxt(/PLACE/); if (b) return vis(b); } return vis(document.getElementById("bBuild")); }
        if (k === 2) { if (S.mode === "build") return block(); if (sheetUp() && S.shop) { const b = btnTxt(/PLACE/); if (b) return vis(b); } return vis(document.getElementById("bBuild")); }''',
    '''        const place = () => document.querySelector('#sheet button[data-shop="tower"]');   /* V564: sprachunabhängig (RU «ПОСТАВИТЬ») */
        if (k === 1) { if (sheetUp() && S.shop) { const b = place(); if (b && vis(b)) return vis(b); return null; } return vis(document.getElementById("bBuild")); }
        if (k === 2) { if (S.mode === "build") return block(); if (sheetUp() && S.shop) { const b = place(); if (b && vis(b)) return vis(b); return null; } return vis(document.getElementById("bBuild")); }''')
rep('''if (TONTUT.st === 2) return vis(document.querySelector('#sheetIn [data-pocket="ton"]'));''',
    '''if (TONTUT.st === 2) return vis(document.querySelector(`#sheetIn [data-pocket="${TONTUT.k || "ton"}"]`));''')
rep('''      else { x = r.left + r.width / 2; up = r.top < 96; y = up ? r.bottom + 2 : r.top - 86; }
      x = Math.max(34, Math.min(innerWidth - 34, x));
      const key = Math.round(x) + "," + Math.round(y) + up;
      if (key !== last) { ca.style.display = "block"; ca.classList.toggle("up", up); ca.style.left = x + "px"; ca.style.top = y + "px"; last = key; }''',
    '''      else if (r.side) { x = Math.max(44, r.left - 44); y = r.top + r.height / 2 - 42; up = false; }
      else { x = r.left + r.width / 2; up = r.top < 96; y = up ? r.bottom + 2 : r.top - 86 + (r.deep ? r.height * 0.5 : 0); }
      if (!r.side) x = Math.max(34, Math.min(innerWidth - 34, x));
      const key = Math.round(x) + "," + Math.round(y) + up + (r.side ? "s" : "");
      if (key !== last) { ca.style.display = "block"; ca.classList.toggle("up", up); ca.classList.toggle("side", !!r.side); ca.style.left = x + "px"; ca.style.top = y + "px"; last = key; }''')
rep('''  function place() { if (!cur || !cur.at) { arr.hidden = true; return; } const el = document.getElementById(cur.at); if (!el || !el.offsetParent) { arr.hidden = true; return; } const r = el.getBoundingClientRect(); arr.hidden = false; arr.style.left = (r.left + r.width / 2 - 23) + "px"; arr.style.top = (r.top - 64) + "px"; }''',
    '''  function place() { if (!cur || !cur.at) { arr.hidden = true; return; } const el = document.getElementById(cur.at); if (!el || !el.offsetParent) { arr.hidden = true; return; } const r = el.getBoundingClientRect(); arr.hidden = false;
    const side = cur.at === "bDrop"; arr.classList.toggle("side", side);   /* V564: DROP von links, Drehen mit Spitze im Knopf */
    if (side) { arr.style.left = Math.max(2, r.left - 66) + "px"; arr.style.top = (r.top + r.height / 2 - 30) + "px"; }
    else { arr.style.left = (r.left + r.width / 2 - 23) + "px"; arr.style.top = (r.top - 64 + (cur.at === "bRot" ? r.height * 0.5 : 0)) + "px"; } }''')

# ---------- 4: Special-Tutorial ----------
a = s.index("const TONTUT = { st: 0 };"); b = s.index("setInterval(tonTutTick, 400);", a)
old = s[a:b]
assert old.count("function tonTutTick()") == 1
card_end = old.index("function tonTutTick()")
card = old[:card_end].replace("const TONTUT = { st: 0 };", '''const TONTUT = { st: 0, k: null, base: null, bS: null };
const SP_KEYS = ["ton", "mix", "snipe", "tesla", "chomp", "lock", "wolf"];
const SP_CNT = k => { try { return ({ ton: S.tons, mix: S.mixers, snipe: S.snipes, tesla: S.teslas, chomp: S.chomps, lock: S.locks, wolf: S.wolves }[k] | 0); } catch (e) { return 0; } };
const SP_SUB = { ton: "Tap USE at the Ten-ton drop. It crushes monsters and squeezes your stack to half.", mix: "Tap USE at the Concrete mixer, then tap a hole in your stack – it gets filled.", snipe: "Tap USE at the Sniper strike, then tap a spot – a 2×2 patch is wiped.", tesla: "Tap USE at the Tesla storm, then tap a spot – lightning wipes 4×4.", chomp: "Tap USE at the Chomper – it runs the ring backwards and eats everything.", lock: "Tap USE at the Lockdown – time stops for a few seconds.", wolf: "Tap USE at the Wolf call – the thief runs off and drops your gold." };''')
assert card.count('$("coachStep").textContent = "AIR DROP";') == 1
card = card.replace('$("coachStep").textContent = "AIR DROP";', '$("coachStep").textContent = "SPECIAL";')
tick = '''/* V564: Special-Tutorial für das erste Special, egal woher (Lucky Supply, Air Drop, Geschenk) – Spiel steht, Pfeil SHOP → USE */
function tonTutTick() { try {
  if (!S || !S.started || S.over || S.nuts || S.testRun || S.replay) { if (TONTUT.st && hintKey === "tontut") { hintKey = null; S && (S.coachHold = false); $("coach").hidden = true; coachHi(null); TONTUT.st = 0; } TONTUT.base = null; return; }
  if (TONTUT.bS !== S) { TONTUT.bS = S; TONTUT.base = null; }
  if (!TONTUT.base) { TONTUT.base = {}; SP_KEYS.forEach(k => TONTUT.base[k] = SP_CNT(k)); return; }
  if (!TONTUT.st) {
    if (LS.get("capy-tut-sp") === "1") return;
    if (S.shop) { SP_KEYS.forEach(k => TONTUT.base[k] = SP_CNT(k)); return; }   // selbst gekauft: kennt den Laden schon
    SP_KEYS.forEach(q => { if (SP_CNT(q) < TONTUT.base[q]) TONTUT.base[q] = SP_CNT(q); });
    const k = SP_KEYS.find(q => SP_CNT(q) > TONTUT.base[q]); if (!k) return;
    if (TUT.on || hintKey || S.ton || window.__tutSumOpen) return;
    if (uiWinOpen() || S.drop || S.paused || S.mapShow || S.ordersOpen || S.intro || S.adOpen || S.mode || S.sel) return;
    if (window.__tipBulb && window.__tipBulb.open) return;
    hintKey = "tontut"; TONTUT.st = 1; TONTUT.k = k; TONTUT.n0 = SP_CNT(k); S.coachHold = true;
    tonTutCard("USE YOUR SPECIAL", "A special is waiting for you in the SHOP. Tap SHOP.", $("bBuild")); snd("radio"); return; }
  const k = TONTUT.k || "ton";
  if (SP_CNT(k) < TONTUT.n0 || (k === "ton" && S.ton) || (["mix", "snipe", "tesla"].includes(k) && S.mode === k)) { hintEnd(); toast("NICE! · specials wait in the SHOP – use them any time", "HQ", 2400); try { SFX.say("Nice!"); } catch (e) {} return; }
  const pk = S.shop && $("sheetIn").classList.contains("pk"), btn = pk ? document.querySelector(`#sheetIn [data-pocket="${k}"]`) : null;
  if (TONTUT.st === 1 && btn) { TONTUT.st = 2; try { btn.scrollIntoView({ block: "center" }); } catch (e) {} setTimeout(() => { if (TONTUT.st === 2) tonTutCard("TAP USE!", SP_SUB[k] || SP_SUB.ton, btn); }, 250); }
  else if (TONTUT.st === 2 && !pk) { TONTUT.st = 1; tonTutCard("USE YOUR SPECIAL", "A special is waiting for you in the SHOP. Tap SHOP.", $("bBuild")); }
} catch (e) {} }
'''
s = s[:a] + card + tick + s[b:]
rep('LS.set("capy-tut-ton", "1")', 'LS.set("capy-tut-ton", "1"), LS.set("capy-tut-sp", "1")', 3)

# ---------- 6: englische Reste ----------
rep('''announce("🎖 NEW MEDAL: " + ms[0].name.toUpperCase(), ms[0].line + " · well deserved!", "HQ", 2800)''',
    '''announce("🎖 NEW MEDAL", ms[0].name + " · " + ms[0].line + " · well deserved!", "HQ", 2800)''')

# ---------- 7: Sprechblase ----------
rep('''      if (now - (lastKey[key] || -1e9) < 240000) return;''',
    '''      if (now - (lastKey[key] || -1e9) < 240000) return;
      if (key === "rb_tower1" && typeof TUT !== "undefined" && TUT.on) return;   /* V564: im Tutorial sagt die Karte das schon */''')
rep('''busy = SFX.voiceBusy || !!(bb && bb.classList.contains("on")) || (!force && (uiWinOpen() || S.paused || S.drop || S.intro || S.eggOpen || S.tiltCard));''',
    '''busy = SFX.voiceBusy || !!(bb && bb.classList.contains("on")) || !!(S.sel || S.shop) || (!force && (uiWinOpen() || S.paused || S.drop || S.intro || S.eggOpen || S.tiltCard));   /* V564: nie über offenem Turm-Menü/Laden */''')

# ---------- Wolf leiser, Dieb tiefer ----------
rep('a.volume = Math.min(1, Math.max(0.6, 8 * Math.pow(SFX.vol || 0.3, 2)));',
    'a.volume = 0.5 * Math.min(1, Math.max(0.6, 8 * Math.pow(SFX.vol || 0.3, 2)));   /* V564: −50 % (Martin 10.11.) */')
rep('pk.type = "peaking"; pk.frequency.value = 1700; pk.gain.value = 8; pk.Q.value = 1.2;',
    'pk.type = "peaking"; pk.frequency.value = 1700; pk.gain.value = 8; pk.Q.value = 1.2; if (/^thief_/.test(String(text))) { hp.frequency.value = 75; lp.frequency.value = 5200; pk.frequency.value = 230; pk.gain.value = 5; }   /* V564: Dieb – tiefe Stimme, kein Funkfilter */')

# ---------- neuer Block: 1 (Drop-Zähler), 5, 8, 9, 10 ----------
NEW = r'''
/* V564: Tutorial-Ausbau (Martin 10.11.) */
try { (() => {
  window.__TUTT = { get T() { return TUT; }, start: () => tutStart(), get TON() { return TONTUT; } };   /* Test-Hook */
  /* 1: Schritt 1 zählt nur einen echten Tipp auf DROP */
  const _hd = hardDrop; hardDrop = function () { try { if (TUT.on && TUT.step === 0 && S && !S.duel) TUT.dropTap = (TUT.dropTap || 0) + 1; } catch (e) {} return _hd.apply(this, arguments); };
  /* 5: Missions- und Beförderungs-Meldungen warten im Tutorial und in W1–W2 bis zur Wellenpause */
  const _to = toast, HOLD = []; let relT = 0;
  const holdNow = () => { try { return !!(S && S.started && !S.over && (TUT.on || window.__tutSumOpen || ((S.wave || 1) <= 2 && S.inWave))); } catch (e) { return false; } };
  toast = function (msg, tag, hold) { if ((tag === "SQUAD" || tag === "PROMOTION") && holdNow()) { HOLD.push([msg, tag, hold]); return; } return _to.apply(this, arguments); };
  setInterval(() => { if (!HOLD.length) return; try { if (!S || !S.started || S.over) { HOLD.length = 0; return; } } catch (e) { return; } if (holdNow() || performance.now() - relT < 3200) return; relT = performance.now(); _to.apply(null, HOLD.shift()); }, 400);
  /* 8: erste geräumte Reihe, erster TNT-Block */
  let rowAsk = false, tntAsk = false;
  setInterval(() => { try { if (!S || !S.started || S.over || S.nuts || S.testRun || S.replay || TUT.on || hintKey || window.__tutSumOpen) return;
      if (!rowAsk && (S.lines | 0) > 0 && LS.get("tarnturm-hint-row1") !== "1") { rowAsk = true; hint("row1", "ROW CLEARED!", "Full rows disappear and pay gold. Keep filling them – it also keeps your stack low.", "board"); return; }
      if (!tntAsk && S.piece && S.piece.tnt && LS.get("tarnturm-hint-tnt") !== "1") { tntAsk = true; hint("tnt", "TNT BLOCK!", "It blows up 3×3 when its row clears or a monster bites it. Put it where the monsters run.", "board"); } } catch (e) {} }, 500);
  /* 10: Abschlusskarte am Ende von Welle 1 (bzw. der Welle, in der das Tutorial endet) */
  const st = document.createElement("style"); st.textContent = `#tutSum{position:fixed;inset:0;z-index:96;display:grid;place-items:center;background:rgba(43,30,18,.5);opacity:0;transition:opacity .2s}
#tutSum.on{opacity:1}#tutSum[hidden]{display:none!important}
#tutSum .tsCard{position:relative;width:min(88vw,340px);background:#fff7e8;border:3px solid #3a2414;border-radius:24px;box-shadow:0 6px 0 #3a2414,0 14px 30px rgba(0,0,0,.4);padding:60px 16px 16px;text-align:center;transform:scale(.8) rotate(-2deg);transition:transform .32s cubic-bezier(.2,1.6,.4,1)}
#tutSum.on .tsCard{transform:none}
#tutSum .tsCard>img{position:absolute;left:50%;top:-62px;width:112px;height:112px;object-fit:contain;transform:translateX(-50%);filter:drop-shadow(0 4px 0 rgba(58,36,20,.25))}
#tutSum small{display:inline-block;font:700 12px/1 "Baloo 2",Nunito,system-ui,sans-serif;letter-spacing:.12em;color:#fff;background:#3f9a3a;border:2px solid #3a2414;border-radius:999px;padding:4px 10px 3px}
#tutSum b{display:block;font:400 27px/1.05 var(--f-display,"Bangers",sans-serif);letter-spacing:.04em;color:#3a2414;margin:8px 0 10px}
#tutSum ul{list-style:none;margin:0 0 14px;padding:0;text-align:left;display:grid;gap:8px}
#tutSum li{display:flex;gap:10px;align-items:center;background:#fff;border:2px solid #e3cfae;border-radius:14px;padding:8px 10px}
#tutSum li i{font-style:normal;font-size:24px;line-height:1;flex:0 0 auto}
#tutSum li span{font:600 14.5px/1.3 "Baloo 2",Nunito,system-ui,sans-serif;color:#5a3d22}
#tutSum button{width:100%;min-height:0;font:400 21px/1 var(--f-display,"Bangers",sans-serif);letter-spacing:.05em;background:#7fd35a!important;color:#1f3a12!important;border:2.5px solid #3a2414;border-radius:16px;box-shadow:0 4px 0 #3a2414;padding:12px 8px 10px;transition:opacity .3s}
#tutSum button:disabled{opacity:.45}
#tutSum button:active{transform:translateY(3px);box-shadow:0 1px 0 #3a2414}
#comicArrow.side svg{transform:rotate(-90deg)}#comicArrow.side{transform:translate(-50%,0)}
#tipArrow.side svg{transform:rotate(-90deg)}
#hkTrial{display:block;width:100%;margin:6px 0 4px;font:400 18px/1 var(--f-display,"Bangers",sans-serif);letter-spacing:.05em;background:#ffd23a!important;color:#3a2414!important;border:2.5px solid #3a2414;border-radius:14px;box-shadow:0 4px 0 #3a2414;padding:10px 8px 8px}
#hkTrialP{margin:2px 0 0;font:600 13px/1.3 "Baloo 2",Nunito,system-ui,sans-serif;color:#6b4a2b;text-align:center}
#hkTip{position:absolute;left:12px;right:12px;bottom:calc(14px + env(safe-area-inset-bottom,0px));z-index:30;background:#fff7e8;border:2.5px solid #3a2414;border-radius:16px;box-shadow:0 4px 0 #3a2414;padding:9px 12px;font:600 14px/1.3 "Baloo 2",Nunito,system-ui,sans-serif;color:#3a2414;text-align:center;pointer-events:none}
#hkTip[hidden]{display:none!important}#hkTip em{display:block;font:400 15px/1 var(--f-display,"Bangers",sans-serif);letter-spacing:.06em;color:#c8161b;font-style:normal;margin-bottom:4px}`;
  document.head.appendChild(st);
  const sum = document.createElement("div"); sum.id = "tutSum"; sum.hidden = true;
  sum.innerHTML = '<div class="tsCard"><img alt=""><small>TUTORIAL</small><b>TUTORIAL DONE!</b><ul><li><i>🧱</i><span>Blocks are your ground – full rows disappear and pay gold.</span></li><li><i>🏰</i><span>Towers shoot the monsters on the ring – each one that gets round costs a ♥ life.</span></li><li><i>🎁</i><span>Specials wait in the SHOP – tap USE.</span></li></ul><button type="button" disabled>LET\'S GO!</button></div>';
  document.body.appendChild(sum); const sb = sum.querySelector("button");
  function sumClose() { sum.classList.remove("on"); setTimeout(() => { sum.hidden = true; }, 220); window.__tutSumOpen = false; try { S.coachHold = false; snd("uiTap"); } catch (e) {} window.__evtLast = performance.now(); }
  sb.addEventListener("click", e => { e.stopPropagation(); if (!sb.disabled) sumClose(); });
  setInterval(() => { try {
    const p = window.__tutSumPend; if (!p || window.__tutSumOpen) return;
    if (!S || !S.started || S.over || S.nuts) { window.__tutSumPend = 0; return; }
    const we = window.__waveEndT || 0; if (S.inWave || we < p || performance.now() - we < 2500) return;
    if (hintKey || TUT.on || uiWinOpen() || S.drop || S.paused || S.shop || S.sel || S.duel || S.mapShow || (window.__tipBulb && window.__tipBulb.open)) return;
    { const cr = document.getElementById("crate"), gv = document.getElementById("ovGive"); if ((cr && !cr.hidden) || (gv && !gv.hidden)) return; }
    window.__tutSumPend = 0; window.__tutSumOpen = true; S.coachHold = true;
    try { sum.querySelector(".tsCard>img").src = HERO_IMG[heroKey()]; } catch (e) {}
    sb.disabled = true; setTimeout(() => { sb.disabled = false; }, 1500);
    sum.hidden = false; requestAnimationFrame(() => sum.classList.add("on")); try { snd("powerup"); } catch (e) {}
  } catch (e) {} }, 400);
  /* 9: erster Boss-Hack – kostenlose Proberunde gegen einen leichten Gegner, dann das echte Duell */
  const ov = document.getElementById("ovHack"), bet = document.getElementById("hackBet");
  if (ov && bet) {
    const tb = document.createElement("button"); tb.id = "hkTrial"; tb.type = "button"; tb.textContent = "FREE PRACTICE ROUND ▶"; tb.hidden = true;
    const tp = document.createElement("p"); tp.id = "hkTrialP"; tp.textContent = "First time? Try it once – no stake, easy opponent."; tp.hidden = true;
    const row = bet.querySelector(".hkRow") || bet.lastElementChild; bet.insertBefore(tp, row); bet.insertBefore(tb, tp);
    const tip = document.createElement("div"); tip.id = "hkTip"; tip.hidden = true; tip.innerHTML = "<em>PRACTICE ROUND</em><span></span>"; ov.appendChild(tip);
    const offer = () => { try { return LS.get("capy-hk-trial") !== "1" && !HK.coach && !HK.trial && !(S && (S.nuts || S.testRun)); } catch (e) { return false; } };
    new MutationObserver(() => { const on = !ov.hidden && !bet.hidden && offer(); tb.hidden = !on; tp.hidden = !on; }).observe(bet, { attributes: true, attributeFilter: ["hidden"] });
    new MutationObserver(() => { const on = !ov.hidden && !bet.hidden && offer(); tb.hidden = !on; tp.hidden = !on; }).observe(ov, { attributes: true, attributeFilter: ["hidden"] });
    tb.addEventListener("click", e => { e.stopPropagation(); try { snd("uiTap"); } catch (er) {} HK.trial = true; HK.coach = true; HK.stake = 0; HK.type = "S"; tb.hidden = true; tp.hidden = true; startDuel(true); });
    setInterval(() => { try { const on = !!HK.trial && !ov.hidden && ["pick", "count", "duel"].includes(HK.phase); if (on) { const t = HK.phase === "duel" ? "Tap YOUR buttons: a lit wire claims a core cell. More than 6 of 12 wins!" : "Pick the side with more ∞ and Y, then tap START."; const sp = tip.querySelector("span"); if (sp.dataset.k !== t) { sp.dataset.k = t; sp.textContent = t; } } if (tip.hidden === on) tip.hidden = !on; } catch (e) {} }, 200);
    const _fin = hkFinish; hkFinish = function () { const tr = !!HK.trial; const r = _fin.apply(this, arguments);
      if (tr && HK.phase === "done") { try { $("hkResTag").textContent = "PRACTICE ROUND"; $("hkGoldV").textContent = "NOW FOR REAL"; $("hkGoldS").textContent = "Now the real duel – with your stake."; $("hkAgain").hidden = true; $("hkBack").textContent = "TO THE REAL HACK ▶"; } catch (e) {} } return r; };
    document.addEventListener("click", e => { if (!HK.trial || !e.target.closest || !e.target.closest("#hkBack")) return; e.stopImmediatePropagation(); e.preventDefault();
      HK.trial = false; HK.coach = false; LS.set("capy-hk-trial", "1"); try { snd("uiTap"); } catch (er) {}
      $("hackRes").hidden = true; $("hackCv").hidden = true; HK.phase = "bet"; snd("arcade", false); $("hkBack").textContent = "Back to the game"; $("hackBet").hidden = false; try { hkStakeUI(); } catch (er) {} }, true);
  }
})(); } catch (e) { console.error("v564", e); }
'''
rep('window.__tonTut = { tick: tonTutTick, get st() { return TONTUT.st; } };',
    'window.__tonTut = { tick: tonTutTick, get st() { return TONTUT.st; } };' + NEW)

open(dst, "w", encoding="utf-8").write(s)
print("ok")
