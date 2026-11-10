#!/usr/bin/env python3
# V572 (Martin 11.11. 00:01–00:02):
# - Flugzeug: Motor schon 1,5 s hören, BEVOR das Flugzeug ins Bild kommt (V571 war falsch herum)
# - Shop-Banner «Тренер Олли»: Schrift gut lesbar (dunkles Feld hinter dem Text, größere helle Schrift)
# - Nach dem ersten echten Boss-Hack: Vollbild-Werbung für Coach Ollie (Hintergrund aus Nano Banana Pro),
#   3 s nicht wegklickbar, erklärt wozu, Kaufen (99 Gold) oder Später. Einmal pro Gerät.
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V571";', 'const GAME_VER = "V572";')

# --- Flugzeug: erst Ton, 1,5 s später ins Bild
rep('function flyPlane(a, b, ms, nod) { const arc = Math.min(a[1], b[1]) < 0.3 ? -.05 : .12, t0 = performance.now(),',
    'function flyPlane(a, b, ms, nod) { const PL = (() => { const off = a[0] > 1 || a[0] < 0; if (!off || b[0] === a[0]) return { off, pre: 0, dl: 0 }; const bx = a[0] > 1 ? 1 : 0, ee = Math.max(0, Math.min(1, (bx - a[0]) / (b[0] - a[0]))), dl = Math.acos(1 - 2 * ee) / Math.PI * ms; return { off, dl, pre: Math.max(0, 1500 - dl) }; })();   /* V572: Motor 1,5 s vor dem Flugzeug */\n      const arc = Math.min(a[1], b[1]) < 0.3 ? -.05 : .12, t0 = performance.now() + PL.pre,')
_i = s.index("/* V572: Motor 1,5 s vor dem Flugzeug */"); _a = 'const step = now => { if (mode !== "auto") return; const t = Math.min(1, (now - t0) / ms),'; _j = s.index(_a, _i); assert _j - _i < 600
s = s[:_j] + 'const step = now => { if (mode !== "auto") return; const t = Math.max(0, Math.min(1, (now - t0) / ms)),' + s[_j + len(_a):]
a = s.index('      step(t0); try { const off = a[0] > 1 || a[0] < 0; let dl = 0;'); b = s.index('}, dl); } catch (e) {} }', a) + len('}, dl); } catch (e) {} }')
s = s[:a] + '''      step(performance.now()); try { const sAt = PL.off ? Math.max(0, PL.pre + PL.dl - 1500) : 0;
        setTimeout(() => { try { window.__planeSnd && window.__planeSnd(ms + PL.pre - sAt, PL.off); } catch (e) {} }, sAt); } catch (e) {} }''' + s[b:]

# --- Coach-Vollbildwerbung nach dem ersten echten Boss-Hack
rep('function hkFinish() {\n', 'function hkFinish() {\n  try { if (!HK.coach && !HK.trial && S && !S.testRun && !S.nuts && LS.get("capy-coach-ad1") !== "1") window.__coachAdPend = 1; } catch (e) {}   /* V572 */\n')
JS = r'''
/* V572: Vollbild-Werbung «Coach Ollie» nach dem ersten Boss-Hack */
try { (() => {
  const ov = document.createElement("div"); ov.id = "ovCoachAd"; ov.hidden = true;
  ov.innerHTML = '<div class="caBg"></div><div class="caTop"><span class="caK">⚡ BOSS HACK · TRAINING ⚡</span><h2>COACH OLLIE</h2><p class="caSub">Get ready for the next boss!</p></div>'
    + '<div class="caCard"><img class="caOllie" alt=""><p class="caWhy">Every boss challenges you to a wire duel. Win it and you take the boss\'s stake – lose it and the gold is gone. Ollie trains you for it.</p>'
    + '<ul><li><b>10</b><span>10 practice duels – no stake, no risk</span></li><li><b>💡</b><span>A tip from the coach after every round</span></li><li><b>🛒</b><span>Train any time – straight from the SHOP</span></li></ul>'
    + '<button type="button" class="caBuy" disabled><span class="caBuyT">BOOK FOR 99 GOLD</span></button><button type="button" class="caLater" disabled>LATER</button><div class="caLock"><i></i><span>3</span></div></div>';
  document.body.appendChild(ov);
  const buy = ov.querySelector(".caBuy"), later = ov.querySelector(".caLater"), lock = ov.querySelector(".caLock");
  let tI = 0;
  function close() { ov.classList.remove("on"); setTimeout(() => { ov.hidden = true; }, 250); try { S.coachHold = false; } catch (e) {} window.__evtLast = performance.now(); }
  function open() { window.__coachAdPend = 0; try { LS.set("capy-coach-ad1", "1"); } catch (e) {}
    try { ov.querySelector(".caOllie").src = COACH_IMG(); } catch (e) {}
    const poor = !S || (S.gold | 0) < COACH_COST; ov.classList.toggle("poor", poor); ov.querySelector(".caBuyT").textContent = poor ? "NOT ENOUGH GOLD YET" : "BOOK FOR 99 GOLD";
    buy.disabled = true; later.disabled = true; lock.hidden = false; let n = 3; lock.querySelector("span").textContent = n; lock.classList.remove("go"); void lock.offsetWidth; lock.classList.add("go");
    clearInterval(tI); tI = setInterval(() => { n--; if (n > 0) { lock.querySelector("span").textContent = n; return; } clearInterval(tI); lock.hidden = true; buy.disabled = poor; later.disabled = false; }, 1000);
    try { S.coachHold = true; } catch (e) {} ov.hidden = false; requestAnimationFrame(() => ov.classList.add("on")); try { snd("radio"); } catch (e) {} }
  buy.addEventListener("click", e => { e.stopPropagation(); if (buy.disabled || !S || S.gold < COACH_COST) return; S.gold -= COACH_COST; coachSet(coachLeft() + 10); try { snd("shopBuy"); } catch (x) {} close(); setTimeout(() => { try { toast(`COACH OLLIE · ${coachLeft()} practice hacks`, "ARMORY"); hud(); } catch (x) {} }, 300); });
  later.addEventListener("click", e => { e.stopPropagation(); if (later.disabled) return; try { snd("uiTap"); } catch (x) {} close(); });
  window.__coachAd = open;
  setInterval(() => { try {
    if (!window.__coachAdPend || !ov.hidden) return;
    const hk = document.getElementById("ovHack"); if (hk && !hk.hidden) return;
    if (!S || !S.started || S.over || S.nuts || (typeof TUT !== "undefined" && TUT.on) || window.__tutSumOpen || uiWinOpen() || S.shop || S.sel || S.drop || S.mapShow) return;
    open(); } catch (e) {} }, 500);
})(); } catch (e) { console.error("v572 coachAd", e); }
'''
rep('const TUT_SNAP = () =>', JS + 'const TUT_SNAP = () =>')

CSS = '''<style id="v572">
.coachAd .ad3 .shade{background:linear-gradient(90deg,rgba(20,14,8,.1) 0,rgba(20,14,8,.86) 20%,rgba(20,14,8,.82) 70%,rgba(20,14,8,.25) 86%)!important}
.coachAd .ad.ad3 .k{font-size:11px!important;color:#ffe066!important;text-shadow:0 1px 0 #000}
.coachAd .ad.ad3 .h{font-size:clamp(21px,6.2vw,27px)!important;color:#fff!important;text-shadow:0 2px 0 #000,0 0 6px rgba(0,0,0,.6)!important}
.coachAd .ad3 .s{font-size:13.5px!important;font-weight:800!important;color:#fff!important;text-shadow:0 1px 2px #000}
#ovCoachAd{position:fixed;inset:0;z-index:9500;display:flex;flex-direction:column;justify-content:space-between;opacity:0;transition:opacity .25s}
#ovCoachAd.on{opacity:1}
#ovCoachAd .caBg{position:absolute;inset:0;background:#1b140c url("img/coach_ad.webp?v=572") center/cover no-repeat}
#ovCoachAd .caBg::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(15,10,5,.82) 0,rgba(15,10,5,.25) 30%,rgba(15,10,5,.1) 50%,rgba(15,10,5,.55) 100%)}
#ovCoachAd .caTop{position:relative;text-align:center;padding:max(26px,env(safe-area-inset-top)) 16px 0;color:#fff}
#ovCoachAd .caK{display:inline-block;font:800 12px/1 "Baloo 2",sans-serif;letter-spacing:.14em;color:#3a2414;background:#ffd23a;border:2px solid #3a2414;border-radius:999px;padding:6px 12px 5px;box-shadow:0 2px 0 #3a2414}
#ovCoachAd h2{margin:10px 0 4px;font:400 clamp(40px,13vw,58px)/1 Bangers,Impact,sans-serif;letter-spacing:.04em;color:#fff;text-shadow:0 3px 0 #3a2414,0 0 14px rgba(255,210,58,.6)}
#ovCoachAd .caSub{margin:0;font:800 16px/1.2 "Baloo 2",sans-serif;color:#ffe9a8;text-shadow:0 2px 2px #000}
#ovCoachAd .caCard{position:relative;margin:0 12px max(14px,env(safe-area-inset-bottom));padding:16px 14px 14px;background:#fff6dc;border:3px solid #3a2414;border-radius:20px;box-shadow:0 5px 0 #3a2414,0 12px 30px rgba(0,0,0,.5);color:#3a2414}
#ovCoachAd .caOllie{position:absolute;right:8px;top:-92px;width:110px;height:110px;object-fit:contain;filter:drop-shadow(0 4px 4px rgba(0,0,0,.45))}
#ovCoachAd .caWhy{margin:0 104px 10px 0;font:700 14.5px/1.3 "Baloo 2",sans-serif}
#ovCoachAd ul{list-style:none;margin:0 0 12px;padding:0;display:grid;gap:6px}
#ovCoachAd li{display:flex;align-items:center;gap:10px;font:800 14px/1.2 "Baloo 2",sans-serif;background:#f3e3b8;border-radius:12px;padding:7px 10px}
#ovCoachAd li b{flex:0 0 30px;height:30px;display:grid;place-items:center;border-radius:50%;background:#58cc02;color:#fff;font:400 17px/1 Bangers,sans-serif;border:2px solid #2f7d0a}
#ovCoachAd .caBuy{display:block;width:100%;padding:14px 10px 12px;border-radius:14px;border:3px solid #3a2414;background:linear-gradient(#ffcf4a,#f29a1e);box-shadow:0 4px 0 #3a2414;font:400 24px/1 Bangers,Impact,sans-serif;letter-spacing:.05em;color:#3a2414}
#ovCoachAd.poor .caBuy{background:#d9cba8;color:#7a6a50}
#ovCoachAd .caLater{display:block;margin:10px auto 0;background:none;border:0;box-shadow:none;font:800 14px/1 "Baloo 2",sans-serif;letter-spacing:.1em;color:#7a5a3a;text-decoration:underline;padding:6px 14px}
#ovCoachAd button:disabled{opacity:.45}
#ovCoachAd .caLock{position:absolute;right:12px;bottom:12px;width:34px;height:34px;border-radius:50%;display:grid;place-items:center;background:#3a2414;color:#fff;font:400 18px/1 Bangers,sans-serif}
#ovCoachAd .caLock[hidden]{display:none}
#ovCoachAd .caLock i{position:absolute;inset:-3px;border-radius:50%;border:3px solid #ffd23a;clip-path:polygon(50% 50%,50% 0,100% 0,100% 100%,0 100%,0 0,50% 0)}
#ovCoachAd .caLock.go i{animation:caRing 3s linear forwards}
@keyframes caRing{from{transform:rotate(0)}to{transform:rotate(360deg);opacity:0}}
</style>
'''
rep("</body>", CSS + "</body>")
open(dst, "w", encoding="utf-8").write(s)
print("ok")
