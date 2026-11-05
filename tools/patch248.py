"""V248: Einarmiger Bandit «LUCKY SUPPLY» (Martin 05.11. 09:31) + Rufzeichen-Abfrage erst nach Welle 7.
- Einmal je Lauf, ca. 1 Minute nach Spielbeginn, an der ersten ruhigen Stelle (zwischen zwei Wellen, kein anderes Fenster,
  kein Tutorial, keine Karte, kein Boss-Signal): Automat im Capybara-Stil, ein Tipp auf SPIN (oder den Hebel) –
  drei Walzen laufen, halten nacheinander an, immer Jackpot: eine zufällige Spezialwaffe (Sniper, Concrete mixer, Tesla,
  Lockdown, Chomper, Ten-ton drop) kommt gratis in die Pocket. Spiel steht, solange der Automat offen ist.
- Dev-Leiste: neuer Knopf «Bandit» (öffnet den Automaten sofort im laufenden Spiel bzw. startet ein Testspiel).
- «Who are you?» (Rufzeichen + Rosie/Blue) erst nach Welle 7 statt 3 (nach 5 kommt die Orts-Feier, nach 8 der Boss-Hack).
Feste Größen: Automat 320×… px fest, nichts verschiebt sich beim Drehen."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V247";', 'const GAME_VER = "V248";')
rep('S.joinOpen || S.intro || S.nuts || S.inWave || S.wave < 3) return;', 'S.joinOpen || S.intro || S.nuts || S.inWave || S.wave < 7) return;')
rep('<div class="dRow dT"><button id="devSpec">Specials</button><button id="devZero">Test from 0</button></div>',
    '<div class="dRow dT"><button id="devSpec">Specials</button><button id="devZero">Test from 0</button><button id="devBandit">Bandit</button></div>')
rep('#devBar .dT{grid-template-columns:1fr 1fr}', '#devBar .dT{grid-template-columns:1fr 1fr 1fr}')
css = r'''
<style id="v248bandit">
#ovBandit{position:fixed;inset:0;z-index:960;display:flex;align-items:center;justify-content:center;padding:16px;background:rgba(40,28,16,.62);-webkit-tap-highlight-color:transparent}
#ovBandit[hidden]{display:none}
.bdBox{position:relative;width:320px;max-width:100%;box-sizing:border-box;background:#fff6e6;border:3px solid #3a2a1a;border-radius:22px;box-shadow:0 12px 34px rgba(0,0,0,.5);padding:14px 14px 16px;text-align:center;color:#3a2a1a;font-family:system-ui,sans-serif;transform:scale(.6);opacity:0;transition:transform .35s cubic-bezier(.2,1.4,.4,1),opacity .2s}
#ovBandit.on .bdBox{transform:none;opacity:1}
.bdTag{display:inline-block;background:#e86fa3;color:#fff;font:900 11px/1 system-ui;letter-spacing:1px;border-radius:8px;padding:5px 8px 4px}
.bdBox h2{font-family:Bangers,system-ui;font-size:34px;letter-spacing:1px;line-height:1;margin:6px 0 2px;color:#ee7a2c;-webkit-text-stroke:1.2px #3a2a1a}
.bdSub{font-size:12px;font-weight:800;opacity:.7;height:16px;line-height:16px;margin-bottom:10px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.bdMach{position:relative;margin:0 34px 0 0;height:150px;border:3px solid #3a2a1a;border-radius:18px;background:linear-gradient(180deg,#f05a3c,#c8402a);box-shadow:inset 0 -6px 0 rgba(0,0,0,.18),0 4px 0 #3a2a1a;padding:10px}
.bdMach:before{content:"";position:absolute;left:10px;right:10px;top:6px;height:10px;border-radius:6px;background:repeating-linear-gradient(90deg,#6f9a3a 0 14px,#4b6e24 14px 22px,#a3c46a 22px 30px,#2c4416 30px 36px);opacity:.9}
.bdLights{position:absolute;left:12px;right:12px;bottom:6px;height:8px;display:flex;justify-content:space-between}
.bdLights i{width:8px;height:8px;border-radius:50%;background:#ffe79a;box-shadow:0 0 6px #ffe79a;opacity:.45}
#ovBandit.spin .bdLights i{animation:bdBlink .4s steps(2) infinite}
#ovBandit.spin .bdLights i:nth-child(2n){animation-delay:.2s}
#ovBandit.win .bdLights i{opacity:1;animation:bdBlink .15s steps(2) infinite}
@keyframes bdBlink{0%{opacity:.25}50%{opacity:1}}
.bdWin{position:absolute;left:10px;right:10px;top:22px;height:96px;display:grid;grid-template-columns:repeat(3,1fr);gap:6px}
.bdReel{position:relative;height:96px;overflow:hidden;border:3px solid #3a2a1a;border-radius:12px;background:linear-gradient(180deg,#d9cdb3,#fff 30%,#fff 70%,#d9cdb3)}
.bdReel:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.28),transparent 28%,transparent 72%,rgba(0,0,0,.28));pointer-events:none}
.bdStrip{position:absolute;left:0;right:0;top:0;will-change:transform}
.bdStrip div{height:96px;display:flex;align-items:center;justify-content:center}
.bdStrip img{width:70px;height:70px;object-fit:contain;filter:drop-shadow(0 2px 2px rgba(0,0,0,.3))}
.bdReel.hit{border-color:#f6c945;box-shadow:0 0 0 3px #f6c945,0 0 18px #ffe79a}
.bdLever{position:absolute;right:-34px;top:8px;width:28px;height:130px;cursor:pointer;touch-action:manipulation}
.bdLever b{position:absolute;left:11px;top:22px;width:7px;height:78px;border-radius:4px;background:linear-gradient(90deg,#9aa3ad,#e6ecf2,#9aa3ad);border:2px solid #3a2a1a;transform-origin:50% 100%;transition:transform .25s}
.bdLever i{position:absolute;left:1px;top:4px;width:26px;height:26px;border-radius:50%;background:radial-gradient(circle at 35% 35%,#ff9bbf,#e86fa3 55%,#a8336a);border:2.5px solid #3a2a1a;transition:transform .25s}
.bdLever u{position:absolute;left:4px;bottom:20px;width:20px;height:16px;border-radius:6px;background:#3a2a1a}
.bdLever.pull b{transform:scaleY(-.55)}
.bdLever.pull i{transform:translateY(92px)}
.bdRes{height:44px;margin:12px 0 10px;display:flex;flex-direction:column;justify-content:center}
.bdRes b{font-family:Bangers,system-ui;font-size:26px;letter-spacing:.6px;line-height:1;color:#3a2a1a;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.bdRes span{font-size:12px;font-weight:800;opacity:.75;margin-top:4px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
#bdGo{width:100%;height:52px!important;min-height:52px!important;margin:0!important;font-size:20px!important;white-space:nowrap}
#bdGo:disabled{filter:grayscale(.6);opacity:.6}
.bdBurst{position:absolute;inset:-40px;pointer-events:none;opacity:0;background:repeating-conic-gradient(from 0deg,rgba(255,231,154,.55) 0 10deg,transparent 10deg 20deg);border-radius:50%;z-index:-1}
#ovBandit.win .bdBurst{opacity:1;animation:bdRot 6s linear infinite}
@keyframes bdRot{to{transform:rotate(360deg)}}
.bdConf{position:absolute;width:9px;height:14px;top:30%;left:50%;border-radius:2px;pointer-events:none}
@media (prefers-reduced-motion:reduce){#ovBandit.win .bdBurst{animation:none}}
</style>
'''
js = r'''
  /* V248: Einarmiger Bandit «LUCKY SUPPLY» */
  try { (() => {
    const IMG = (typeof ICO_SPR !== "undefined" && ICO_SPR) || {};
    const PR = [["snipe", "Sniper strike", "snipes"], ["mix", "Concrete mixer", "mixers"], ["tesla", "Tesla storm", "teslas"],
                ["lock", "Lockdown", "locks"], ["chomp", "Chomper", "chomps"], ["ton", "Ten-ton drop", "tons"]];
    try { if (typeof SAVE_KEYS !== "undefined" && !SAVE_KEYS.includes("banditDone")) SAVE_KEYS.push("banditDone"); } catch (e) {}
    const ov = document.createElement("div"); ov.id = "ovBandit"; ov.hidden = true;
    ov.innerHTML = `<div class="bdBox"><div class="bdBurst"></div><span class="bdTag">FREE SUPPLY DROP</span><h2>LUCKY SUPPLY</h2><div class="bdSub" id="bdSub">One spin on the house, squad!</div>
      <div class="bdMach"><div class="bdWin">${[0, 1, 2].map(i => `<div class="bdReel" id="bdR${i}"><div class="bdStrip" id="bdS${i}"></div></div>`).join("")}</div><div class="bdLights">${"<i></i>".repeat(12)}</div>
        <div class="bdLever" id="bdLever" aria-label="Pull"><u></u><b></b><i></i></div></div>
      <div class="bdRes"><b id="bdResT">&nbsp;</b><span id="bdResS">&nbsp;</span></div>
      <button class="btn-accent" id="bdGo">SPIN ▶</button></div>`;
    document.body.appendChild(ov);
    const $b = id => document.getElementById(id), H = 96, LEN = 30;
    let st = 0, prize = null, wasPaused = false;   // st: 0 bereit, 1 dreht, 2 gewonnen
    const fill = (i, last) => { const s = $b("bdS" + i); let h = ""; for (let k = 0; k < LEN; k++) { const p = k === LEN - 1 && last ? last : PR[(k * 5 + i * 2 + Math.floor(Math.random() * 6)) % 6]; h += `<div><img src="${IMG[p[0]] || ""}" alt=""></div>`; }
      s.innerHTML = h; s.style.transition = "none"; s.style.transform = "translateY(0)"; };
    function open(force) {
      if (!ov.hidden) return; st = 0; prize = PR[Math.floor(Math.random() * PR.length)];
      [0, 1, 2].forEach(i => { fill(i, prize); $b("bdR" + i).classList.remove("hit"); });
      $b("bdResT").innerHTML = "&nbsp;"; $b("bdResS").innerHTML = "&nbsp;"; $b("bdSub").textContent = "One spin on the house, squad!";
      $b("bdGo").textContent = "SPIN ▶"; $b("bdGo").disabled = false; $b("bdLever").classList.remove("pull");
      ov.classList.remove("spin", "win", "on"); ov.querySelectorAll(".bdConf").forEach(e => e.remove());
      if (S) { S.banditDone = true; wasPaused = !!S.intro; S.intro = true; S.banditOpen = true; }
      ov.hidden = false; requestAnimationFrame(() => ov.classList.add("on"));
      try { SFX.init(); snd("radio"); } catch (e) {}
    }
    function spin() {
      if (st !== 0) return; st = 1; ov.classList.add("spin"); $b("bdGo").disabled = true; $b("bdGo").textContent = "SPINNING…";
      const lv = $b("bdLever"); lv.classList.add("pull"); setTimeout(() => lv.classList.remove("pull"), 420);
      try { SFX.init(); snd("uiTap"); } catch (e) {}
      const stops = [1300, 2000, 2900]; let tick = setInterval(() => { try { snd("hkTick", 1); } catch (e) {} }, 110);
      [0, 1, 2].forEach(i => { const s = $b("bdS" + i);
        requestAnimationFrame(() => { s.style.transition = `transform ${stops[i]}ms cubic-bezier(.12,.62,.18,1)`; s.style.transform = `translateY(${-(LEN - 1) * H}px)`; });
        setTimeout(() => { $b("bdR" + i).classList.add("hit"); try { snd(i < 2 ? "confirm" : "coin"); } catch (e) {}
          if (i === 1) $b("bdSub").textContent = "Two of a kind… one more!";
          if (i === 2) { clearInterval(tick); win(); } }, stops[i] + 40); });
    }
    function win() {
      st = 2; ov.classList.remove("spin"); ov.classList.add("win");
      if (S) S[prize[2]] = (S[prize[2]] || 0) + 1;
      $b("bdSub").textContent = "JACKPOT!"; $b("bdResT").textContent = prize[1].toUpperCase();
      $b("bdResS").textContent = `+1 in your Pocket · now ×${S ? S[prize[2]] : 1}`; $b("bdGo").disabled = false; $b("bdGo").textContent = "COLLECT ▶";
      try { snd("hkWin"); setTimeout(() => SFX.say("Jackpot!", 1.0, 1.0), 350); } catch (e) {}
      try { if (navigator.vibrate) navigator.vibrate([30, 60, 30]); } catch (e) {}
      const box = ov.querySelector(".bdBox"), cols = ["#e86fa3", "#6f9a3a", "#4f86c9", "#e6b93a", "#ee7a2c"];
      for (let k = 0; k < 26; k++) { const c = document.createElement("i"); c.className = "bdConf"; c.style.background = cols[k % 5]; box.appendChild(c);
        const a = Math.random() * Math.PI * 2, d = 90 + Math.random() * 120;
        c.animate([{ transform: "translate(-50%,0) rotate(0)", opacity: 1 }, { transform: `translate(${Math.cos(a) * d}px,${Math.sin(a) * d + 60}px) rotate(${Math.random() * 720}deg)`, opacity: 0 }], { duration: 1200 + Math.random() * 700, easing: "cubic-bezier(.2,.7,.4,1)", fill: "forwards" }); }
    }
    function close() { ov.classList.remove("on"); setTimeout(() => { ov.hidden = true; ov.classList.remove("win"); }, 200);
      if (S) { S.banditOpen = false; if (!wasPaused) S.intro = false; } try { snd("uiTap"); renderPocket && !$("sheet").hidden && $("sheetIn").classList.contains("pk") && renderPocket(); } catch (e) {}
      try { toast(`${prize[1].toUpperCase()} · in your Pocket`, "SUPPLY", 2200); } catch (e) {} }
    $b("bdGo").addEventListener("click", e => { e.stopPropagation(); if (st === 0) spin(); else if (st === 2) close(); });
    $b("bdLever").addEventListener("click", e => { e.stopPropagation(); if (st === 0) spin(); });
    ov.addEventListener("click", e => e.stopPropagation());
    // Wann: einmal je Lauf, ab ~60 s Spielzeit, an der ersten ruhigen Stelle
    const calm = () => S && S.started && !S.over && !S.nuts && !S.banditDone && (S.playT || 0) >= 60 && !S.inWave && (S.waveCD || 0) > 2.5
      && !S.intro && !S.drop && !S.alert && !S.ordersOpen && !S.duel && !S.mapShow && !S.mapFly && !S.signOpen && !S.joinOpen && !S.mode && !S.sel && !S.shop && !S.paused && !S.mix
      && !(typeof TUT !== "undefined" && TUT.on) && !(typeof hkOfferOn === "function" && hkOfferOn()) && !S.hackPending && (typeof inPlay !== "function" || inPlay()) && !document.hidden;
    setInterval(() => { try { if (ov.hidden && calm()) open(false); } catch (e) {} }, 500);
    const db = document.getElementById("devBandit");
    if (db) db.addEventListener("click", e => { e.stopPropagation(); if (S && S.started && !S.over) open(true); else { try { devJump(3); } catch (er) {} setTimeout(() => open(true), 2500); } });
    window.__TT && (window.__TT.bandit = { open, spin, close });
  })(); } catch (e) { console.error("bandit", e); }
'''
i = s.rfind('</body>'); s = s[:i] + css + s[i:]
i = s.rfind('})();\n</script>'); s = s[:i] + js + s[i:]
open(dst, 'w', encoding='utf-8').write(s); print('ok')
