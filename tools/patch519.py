#!/usr/bin/env python3
"""V519 (Martin 09.11. 16:53):
- Ten-ton: Ring oben innen durchsichtig (neues Bild) → Cache-Bust.
- Tagesmission geschafft: beim nächsten Besuch des Startbildschirms (gleicher Tag oder später) kommt ein großes grünes Häkchen
  über das alte Kalenderblatt, dann wird es abgerissen und das nächste Blatt ist zu sehen.
  Gleicher Tag: nächstes Blatt = morgen («New mission tomorrow»). Späterer Tag: das neue Tagesblatt.
- Testlink ?test=tear (Antippen des Blatts spielt es nochmal).
Aufruf: python3 tools/patch519.py site/index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V518";', 'const GAME_VER = "V519";')
rep('TON_IMG.src = "img/ton_weight.webp";', 'TON_IMG.src = "img/ton_weight.webp?v=519";')
# Mission erfüllt → Feier vormerken (altes Blatt merken)
rep('if (DAILY.m.p >= DAILY.m.n) { DAILY.m.done = true; DAILY.m.xp = true;',
    'if (DAILY.m.p >= DAILY.m.n) { DAILY.m.done = true; DAILY.m.xp = true; DAILY.celeb = { day: DAILY.day, dn: dailyDay(), txt: DAILY.m.txt, n: DAILY.m.n };   /* V519 */')
# Test-Modus
rep('function dailyGate() { return dailyBestW() >= DAILY_DROP_W; }',
    '''const DL_TEST = /[?&]test=tear\\b/.test(location.search);   /* V519 */
if (DL_TEST) { DAILY.celeb = { day: dailyKey(), dn: Math.max(1, dailyDay()), txt: "Splat 25 monsters", n: 25 }; }
else if (!DAILY.v519) { if (DAILY.m && DAILY.m.done && DAILY.day && !DAILY.celeb) DAILY.celeb = { day: DAILY.day, dn: dailyDay(), txt: DAILY.m.txt, n: DAILY.m.n }; DAILY.v519 = 1; }   /* schon vor V519 geschafft: einmal nachholen */
function dailyGate() { return DL_TEST || dailyBestW() >= DAILY_DROP_W; }''')
rep('function dailySave() { try {', 'function dailySave() { if (DL_TEST) return; try {')
rep('function dailyMsnGate() { return dailyBestW() >= DAILY_MSN_W; }', 'function dailyMsnGate() { return DL_TEST || dailyBestW() >= DAILY_MSN_W; }')
# Blatt: gleicher Tag nach der Feier → Blatt von morgen
rep('''  const now = new Date(), day = dailyDay(), d = dailyDrop(), m = dailyMsnGate() ? DAILY.m : null,''',
    '''  const nx = DAILY.m && DAILY.m.done && DAILY.torn === DAILY.day && !DAILY.celeb;   /* V519: abgerissen → morgen */
  const now = new Date(Date.now() + (nx ? 864e5 : 0)), day = nx ? dailyDay() % 7 + 1 : dailyDay(), d = dailyDrop(), m = dailyMsnGate() ? (nx ? { txt: "New mission tomorrow", p: 0, n: 1, nx: 1 } : DAILY.m) : null,''')
rep('''<div class="num"><span>${m.p || 0} / ${m.n}</span><span>${m.done ? "done ✓" : "today"}</span></div>`''',
    '''${m.nx ? `<div class="num"><span>today ✓ done</span><span>tomorrow</span></div>` : `<div class="num"><span>${m.p || 0} / ${m.n}</span><span>${m.done ? "done ✓" : "today"}</span></div>`}`''')
rep('<div class="rew${DAILY.claimed ? " got" : ""}">', '<div class="rew${DAILY.claimed ? " got" : ""}${nx ? " nx" : ""}">')
rep('''    + `<div class="streak">${dots}</div><div class="sub">7-day chain · 1 shield day</div><i class="corner"></i></div>`;
  dailyFit();
}''', '''    + `<div class="streak">${dots}</div><div class="sub">7-day chain · 1 shield day</div><i class="corner"></i></div>`;
  dailyFit(); dailyTear(el);
}
/* V519: altes Blatt mit grünem Häkchen abreißen */
function dailyTear(el) { try {
  const c = DAILY.celeb, st = document.getElementById("ovStart"); if (!c || !el || !st || st.hidden || el.querySelector(".dlOld")) return;
  if (document.body.classList.contains("awOn") || document.getElementById("splash")) return;   /* erst wenn das Startmenü wirklich sichtbar ist */
  delete DAILY.celeb; if (DL_TEST && DAILY.m) DAILY.m.done = true; if (c.day === DAILY.day) DAILY.torn = DAILY.day; if (!DL_TEST) dailySave();
  if (c.day === DAILY.day) { dailyLeaf(); el = document.getElementById("dailyLeaf"); if (!el) return; }   /* darunter schon das nächste Blatt */
  const dt = new Date(c.day + "T12:00:00"), o = document.createElement("div"); o.className = "dlOld";
  o.innerHTML = `<i class="ring l"></i><i class="ring r"></i><div class="head">${DAILY_WD[dt.getDay()]} · ${DAILY_MON[dt.getMonth()]} ${dt.getDate()}<b>DAY ${c.dn}</b></div><div class="body"><div class="tag">DAILY MISSION</div><div class="task">${c.txt}</div><div class="dlBar"><b style="width:100%"></b></div><div class="num"><span>${c.n} / ${c.n}</span><span>done ✓</span></div></div><svg class="dlChk" viewBox="0 0 100 100"><path d="M18 54 L42 76 L84 24"/></svg>`;
  el.appendChild(o);
  setTimeout(() => { o.classList.add("chk"); try { SFX.init(); snd("confirm"); } catch (e) {} }, 500);
  setTimeout(() => { o.classList.add("tear"); try { snd("uiTap"); } catch (e) {} }, 1900);
  setTimeout(() => o.remove(), 3100);
} catch (e) {} }
if (DL_TEST) document.addEventListener("click", e => { if (e.target.closest && e.target.closest("#dailyLeaf")) { e.stopPropagation(); e.preventDefault(); DAILY.celeb = { day: dailyKey(), dn: Math.max(1, dailyDay()), txt: "Splat 25 monsters", n: 25 }; DAILY.torn = null; const el = document.getElementById("dailyLeaf"); const o = el && el.querySelector(".dlOld"); if (o) o.remove(); dailyLeaf(); } }, true);
{ const st = document.createElement("style"); st.textContent = `
#dailyLeaf .dlOld{position:absolute;left:0;right:0;top:0;transform-origin:50% 0;z-index:3}
#dailyLeaf .dlChk{position:absolute;left:50%;top:52%;width:120%;height:120%;transform:translate(-50%,-50%) scale(.4);opacity:0;pointer-events:none;overflow:visible;filter:drop-shadow(0 3px 0 #1d5e1d)}
#dailyLeaf .dlChk path{fill:none;stroke:#35c435;stroke-width:16;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:110;stroke-dashoffset:110}
#dailyLeaf .dlOld.chk .dlChk{opacity:1;transform:translate(-50%,-50%) scale(1);transition:transform .35s cubic-bezier(.2,1.6,.4,1),opacity .15s}
#dailyLeaf .dlOld.chk .dlChk path{stroke-dashoffset:0;transition:stroke-dashoffset .45s ease-out .1s}
#dailyLeaf .dlOld.tear{animation:dlTear 1.15s cubic-bezier(.45,0,.8,.6) forwards}
@keyframes dlTear{0%{transform:rotate(0)}18%{transform:rotate(-7deg) translate(-2px,2px)}35%{transform:rotate(-14deg) translate(-6px,6px);opacity:1}100%{transform:rotate(-38deg) translate(-60px,520px);opacity:0}}
#dailyLeaf .rew.nx{opacity:.75}`; document.head.appendChild(st); }''')
rep('dailyLeaf(); else dailyFit(); } catch (e) {} }, 800);', 'dailyLeaf(); else { dailyFit(); if (DAILY.celeb) dailyTear(document.getElementById("dailyLeaf")); } } catch (e) {} }, 800);')
open(p, "w", encoding="utf-8").write(s); print("ok V519")
