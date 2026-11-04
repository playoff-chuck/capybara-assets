"""V192: Versionsnummer klein oben rechts auf Start/Intro, Shop-Banner neu (Nano-Banana-Hintergründe, flach),
Shop-Lücken zu, Shop-Höhe mit dvh (Handy: unten nichts mehr abgeschnitten, Liste scrollt bis zum Ende)."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)

VER = "V192"
rep('ver: "V191", wave: S.wave', 'ver: GAME_VER, wave: S.wave')

# Banner: neues Markup, gleiche Klick-Logik (coachAd / data-train bleiben)
rep('b.innerHTML = `<span class="ad ad2">${ADS[v](n)}</span>', 'b.innerHTML = `<span class="ad ad3 ${v}">${AD3(v)}</span>')
ad3 = '''  const AD3_TXT = { vA: ["img/ad_a.webp", "BOSS HACK · COACHING", "TRAIN WITH OLLIE", "Coach Ollie shows you the tricks"],
                    vB: ["img/ad_b.webp", "BOSS HACK · COACHING", "BEAT THE BOSS", "10 practice duels · zero risk"],
                    vC: ["img/ad_c.webp", "BOSS HACK · COACHING", "WIN MORE GOLD", "Tips after every round"] };
  function AD3(v) { const t = AD3_TXT[v] || AD3_TXT.vA;
    return `<span class="bg" style="background-image:url(${t[0]})"></span><span class="shade"></span><img class="ollie" src="${COACH_IMG()}" alt=""><span class="txt"><span class="k">${t[1]}</span><span class="h">${t[2]}</span><span class="s">${t[3]}</span></span><span class="p"><b>99</b><i>GOLD</i></span>`; }
'''
rep('let adSeq = 0;', ad3 + '  let adSeq = 0;')

# Boss-Hack gewonnen: Jubel (Stimme + Münzen + Jingle), Hauptmusik läuft auf dem Ergebnis-Screen schon wieder
rep('$("hkScMe").textContent = mine; $("hkScBo").textContent = 12 - mine;\n  $("hkConf")',
    '$("hkScMe").textContent = mine; $("hkScBo").textContent = 12 - mine;\n  if (win) { try { const JOY = ["nailedit", "boomshaka", "hellyeah", "phenomenal", "outstanding", "spectacular"]; setTimeout(() => SFX.say(JOY[Math.floor(Math.random() * JOY.length)]), 650); setTimeout(() => snd("jingle"), 300); [900, 1050, 1200, 1400].forEach(t => setTimeout(() => snd("coin"), t)); } catch (e) {} }\n  $("hkConf")')
rep('const hackUp = (() => { const e = document.getElementById("ovHack"); return !!(e && !e.hidden) || !!(typeof S !== "undefined" && S && S.duel); })();',
    'const hackUp = (() => { const e = document.getElementById("ovHack"), r = document.getElementById("hackRes"); if (r && !r.hidden && r.getClientRects().length) return false; return !!(e && !e.hidden) || !!(typeof S !== "undefined" && S && S.duel); })();')

js = '''
  /* V192: Versionsnummer auf Start- und Intro-Screen */
  try { ["ovStart", "splash"].forEach(id => { const o = document.getElementById(id); if (o && !o.querySelector(".verTag")) { const t = document.createElement("div"); t.className = "verTag"; t.textContent = GAME_VER; o.appendChild(t); } }); } catch (e) {}
  /* V192: Einblendungen während des Spiels (neues Monster, Gadget, Kontinent, Squad, Tipps …) – 2 s gesperrt, dann erscheint der Knopf */
  try {
    const LOCK_IDS = ["ovIntro", "ovJoin", "ovCamp", "ovWave", "ovLines", "ovKills", "ovTime", "ovGive", "ovOrders"];
    const locked = new Set();
    const lockOv = ov => { if (locked.has(ov)) return; locked.add(ov); ov.classList.add("ovLock");
      setTimeout(() => { ov.classList.remove("ovLock"); locked.delete(ov); }, 2000); };
    const mo = new MutationObserver(list => { for (const m of list) { const ov = m.target;
      if (!ov.hidden && m.oldValue !== null && typeof S !== "undefined" && S && S.started && !S.over) lockOv(ov); } });
    LOCK_IDS.forEach(id => { const ov = document.getElementById(id); if (ov) mo.observe(ov, { attributes: true, attributeFilter: ["hidden"], attributeOldValue: true }); });
    const block = e => { const ov = e.target && e.target.closest && e.target.closest(".ovLock"); if (ov) { e.stopImmediatePropagation(); e.preventDefault(); } };
    ["pointerdown", "pointerup", "click", "touchstart", "touchend"].forEach(t => window.addEventListener(t, block, { capture: true, passive: false }));
    window.__TT && (window.__TT.lockOv = lockOv);
  } catch (e) {}
'''
i = s.rfind('})();\n</script>'); assert i > 0
s = s[:i] + js + s[i:]
# GAME_VER ganz oben im ersten Skript definieren
k = s.find('<script>'); assert k > 0
s = s[:k + 8] + f'\nconst GAME_VER = "{VER}";\n' + s[k + 8:]

css = '''<style id="v192">
/* V192 Einblendungen: Knöpfe erst nach 2 s */
.ovLock button,.ovLock [role=button]{opacity:0!important;pointer-events:none!important}
[id^=ov] button{transition:opacity .35s ease}
.ovLock::after{content:"";position:absolute;left:50%;bottom:calc(env(safe-area-inset-bottom,0px) + 18px);width:120px;height:4px;margin-left:-60px;border-radius:4px;background:rgba(255,255,255,.25);overflow:hidden}
.ovLock::before{content:"";position:absolute;left:50%;bottom:calc(env(safe-area-inset-bottom,0px) + 18px);width:120px;height:4px;margin-left:-60px;border-radius:4px;background:#ffd75e;z-index:1;transform-origin:left;animation:ovLockBar 2s linear forwards}
@keyframes ovLockBar{from{transform:scaleX(0)}to{transform:scaleX(1)}}
/* V192 Versionsnummer */
.verTag{position:absolute;top:calc(env(safe-area-inset-top,0px) + 4px);right:8px;z-index:50;font:600 10px/1 ui-monospace,Menlo,monospace;letter-spacing:.04em;color:#fff;opacity:.75;text-shadow:0 1px 2px rgba(0,0,0,.7);pointer-events:none}
/* V192 Shop-Höhe: sichtbare Bildschirmhöhe (dvh) statt 100vh – Handy-Leisten schneiden nichts mehr ab */
body:has(#sheet:not([hidden])) #sheet{max-height:calc(100dvh - 66px - env(safe-area-inset-top,0px))!important;bottom:auto!important}
body:has(#sheet:not([hidden])) #sheetIn{max-height:calc(100dvh - 74px - env(safe-area-inset-top,0px))!important}
#sheetIn.shopV{display:flex!important;flex-direction:column!important}
#sheetIn.shopV .shopGrid{flex:1 1 auto!important;min-height:0!important;padding-bottom:16px!important}
#sheetIn.shopV .sheetFoot{flex:0 0 auto!important}
/* V192 Lücken zu */
#sheet .ledgerTop{margin:10px 0 6px 0!important}
#sheet .coachAd{margin:0 0 6px!important;padding:0!important;display:block;width:100%;background:none!important;border:0!important;box-shadow:none!important}
/* V192 Banner: flach, Bild-Hintergrund, ruhig */
.coachAd .ad.ad3{position:relative;display:block;height:86px;border:3px solid #3a2414;border-radius:16px;overflow:hidden;box-shadow:0 3px 0 #3a2414;text-align:left;animation:none}
.coachAd .ad3 .bg{position:absolute;inset:0;background-size:cover;background-position:center 45%}
.coachAd .ad3.vB .bg{background-position:70% 50%}
.coachAd .ad3 .shade{position:absolute;inset:0;background:linear-gradient(90deg,rgba(20,14,8,.15) 0,rgba(20,14,8,.62) 22%,rgba(20,14,8,.45) 58%,rgba(20,14,8,0) 82%)}
.coachAd .ad3::after{content:"";position:absolute;top:0;bottom:0;width:40%;left:-45%;background:linear-gradient(100deg,transparent,rgba(255,255,255,.18),transparent);animation:ad3Shine 4.5s ease-in-out infinite;pointer-events:none}
.coachAd .ad3 .ollie{position:absolute;left:2px;bottom:-6px;height:96px;width:auto;object-fit:contain;filter:drop-shadow(0 2px 3px rgba(0,0,0,.45))}
.coachAd .ad3 .txt{position:absolute;left:84px;right:76px;top:50%;transform:translateY(-50%);display:flex;flex-direction:column;gap:1px}
.coachAd .ad3 .k{font:800 10px/1 "Baloo 2",sans-serif;letter-spacing:.12em;color:#ffd75e}
.coachAd .ad3 .h{font-family:"Bangers","Impact",sans-serif;font-size:clamp(20px,6vw,26px);line-height:1;letter-spacing:.03em;color:#fff;text-shadow:0 2px 0 rgba(0,0,0,.55)}
.coachAd .ad3 .s{font:700 12px/1.15 "Baloo 2",sans-serif;color:rgba(255,255,255,.9)}
.coachAd .ad3 .p{position:absolute;right:10px;top:50%;transform:translateY(-50%);min-width:56px;padding:6px 8px 5px;border-radius:12px;background:linear-gradient(#ffe57a,#f2b51e);border:2px solid #3a2414;box-shadow:0 2px 0 #3a2414;text-align:center;line-height:.9;color:#3a2414}
.coachAd .ad3 .p b{display:block;font-family:"Bangers","Impact",sans-serif;font-weight:400;font-size:24px}
.coachAd .ad3 .p i{display:block;font:800 10px "Baloo 2",sans-serif;font-style:normal;letter-spacing:.08em}
.coachAd.poor .ad3 .p{filter:saturate(.4) brightness(.92)}
@keyframes ad3Shine{0%,70%{left:-45%}100%{left:110%}}
@media (prefers-reduced-motion:reduce){.coachAd .ad3::after{animation:none;display:none}}
</style>
'''
i = s.rfind('</body>'); s = s[:i] + css + s[i:]
open(dst, 'w', encoding='utf-8').write(s); print('ok', dst)
