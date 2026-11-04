"""V233: Ortswechsel (alle 5 Wellen) feierlich und ~3× länger (≈ 8,5 s): BOOM-Feier «<Ort> CLEARED!» mit Konfetti,
Strahlen und Fanfare über dem Spielfeld → Karte blendet ein (doppelt so lang) → der Held fliegt hörbar (Rauschen +
Motor) im Bogen zum nächsten Ort → Ankunftsgeräusch, Stecknadel ploppt, «Welcome to <Ort>» → neue Stadt startet.
Kontinentwechsel bekommt dieselbe Feier, Motor- und Ankunftsgeräusch und läuft etwas länger. Antippen überspringt."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V232";', 'const GAME_VER = "V233";')
a = s.index('    function playPlace(w, done) {'); e = s.index('    function playIntro(done) {', a)
s = s[:a] + r'''    const fx = k => { try { snd(k); } catch (e) {} };
    const whoosh = () => { try { if (typeof swoosh === "function") swoosh(); } catch (e) {} };
    function celebrate(title, sub) { const c = document.createElement("div"); c.className = "mapCel";
      let conf = ""; for (let i = 0; i < 46; i++) conf += `<i style="--x:${(Math.random() * 2 - 1).toFixed(2)};--y:${(-.4 - Math.random() * .9).toFixed(2)};--r:${Math.floor(Math.random() * 720 - 360)}deg;--d:${(Math.random() * .35).toFixed(2)}s;--c:${["#ffd84d", "#ff6fb5", "#5cbf4a", "#4aa8ff", "#ff9a2a", "#fff"][i % 6]}"></i>`;
      c.innerHTML = `<div class="celRays"></div><div class="celConf">${conf}</div><div class="celTxt"><b>${title}</b><span>${sub}</span><em>★ ★ ★</em></div>`;
      ov.appendChild(c); ov.classList.add("cel"); requestAnimationFrame(() => c.classList.add("on"));
      fx("boom"); setTimeout(() => fx("jingle"), 180); setTimeout(() => fx("hkWin"), 650);
      return () => { c.classList.add("out"); ov.classList.remove("cel"); setTimeout(() => c.remove(), 700); }; }
    function playPlace(w, done) { const P = posOf(w), prev = MAP_PTS[P.c][P.p - 1], nxt = MAP_PTS[P.c][P.p], oldN = nice(CONTS[P.c][2][P.p - 1]), newN = nice(CONTS[P.c][2][P.p]);
      seqDone = done; show("auto"); drawPins(P.g - 1); setMe(prev, true); go(contCam(P.c), 0);
      label(contName(P.c), `Next stop: ${newN}`, P.p === 5 ? "The landmark · the boss lives here" : `Waves ${w}–${w + 4}`);
      const end = celebrate(`${oldN.toUpperCase()} CLEARED!`, `Place ${P.g} of 30 done · onward!`);
      at(2300, end);
      at(3200, () => { fx("engine"); whoosh(); me.classList.add("fly"); hopMe(prev, nxt, 2600); });
      at(4300, whoosh);
      at(5850, () => { me.classList.remove("fly"); drawPins(P.g); const pin = pinsEl.querySelector(`.mPin[data-g="${P.g}"]`); pin && pin.classList.add("pop");
        label(contName(P.c), `Welcome to ${newN}!`, P.p === 5 ? "The landmark · the boss lives here" : `Waves ${w}–${w + 4}`); fx("tonHit"); setTimeout(() => fx("powerup"), 120); setTimeout(() => fx("coin"), 420); });
      at(8600, hide); }
    function playCont(w, done) { const P = posOf(w), oc = Math.max(0, P.c - 1); seqDone = done; show("auto"); drawPins(P.g); setMe(MAP_PTS[oc][5], true);
      label(contName(oc), "Continent cleared!", `Next: ${contName(P.c)}`); go(contCam(oc), 0);
      const end = celebrate(`${contName(oc)} CLEARED!`, `Continent ${P.c} of 5 · the world tour goes on`);
      at(2400, end);
      at(3300, () => { me.classList.remove("on"); go(worldCam(), 1300); });
      at(4400, () => { label("", "Flying to " + nice(contName(P.c)), ""); fx("engine"); whoosh(); flyPlane(cen(oc), cen(P.c), 3000); });
      at(5600, whoosh);
      at(7200, () => { go(contCam(P.c), 1300); });
      at(8600, () => { setMe(MAP_PTS[P.c][0], true); label(contName(P.c), `Welcome to ${nice(contName(P.c))}!`, `First stop: ${nice(CONTS[P.c][2][0])}`); fx("tonHit"); setTimeout(() => fx("powerup"), 120); setTimeout(() => fx("coin"), 420); });
      at(11000, hide); }
''' + s[e:]
rep('const txt = S.alert ? "" : S.drop ? "" : S.paused ? "Paused"', 'const txt = S.alert ? "" : S.drop ? "" : S.mapShow ? "" : S.paused ? "Paused"')
# Held fliegt höher im Bogen
rep("y = a[1] + (b[1] - a[1]) * t - Math.sin(Math.PI * t) * .05;", "y = a[1] + (b[1] - a[1]) * t - Math.sin(Math.PI * t) * .09;")
css = '''<style id="v233">
#ovMap.cel{background:transparent!important}
body.mapUp #bWave,body.mapUp #waveNum,body.mapUp #bPauseTop{visibility:hidden!important}
#ovMap .mapVp,#ovMap .mapTop{transition:opacity .7s ease}
#ovMap.cel .mapVp,#ovMap.cel .mapTop,#ovMap.cel .mapSkip{opacity:0}
#ovMap .mapCel{position:absolute;inset:0;z-index:6;display:grid;place-items:center;background:radial-gradient(circle at 50% 45%,rgba(255,216,77,.35),rgba(20,28,16,.55) 70%);opacity:0;transition:opacity .35s ease;overflow:hidden;pointer-events:none}
#ovMap .mapCel.on{opacity:1}#ovMap .mapCel.out{opacity:0;transition:opacity .7s ease}
#ovMap .celRays{position:absolute;left:50%;top:45%;width:200vmax;height:200vmax;margin:-100vmax 0 0 -100vmax;background:repeating-conic-gradient(rgba(255,240,180,.28) 0 9deg,transparent 9deg 22deg);animation:celSpin 9s linear infinite}
@keyframes celSpin{to{transform:rotate(360deg)}}
#ovMap .celTxt{position:relative;display:grid;gap:8px;justify-items:center;text-align:center;transform:scale(.2);opacity:0;padding:0 14px}
#ovMap .mapCel.on .celTxt{animation:celPop .7s cubic-bezier(.2,1.7,.4,1) forwards}
@keyframes celPop{to{transform:scale(1);opacity:1}}
#ovMap .celTxt b{font:400 clamp(38px,11vw,60px)/1 var(--f-display,"Bangers",sans-serif);letter-spacing:.03em;color:#ffd84d;-webkit-text-stroke:3px #3a2414;paint-order:stroke fill;text-shadow:0 5px 0 #3a2414,0 0 24px rgba(255,200,60,.6)}
#ovMap .celTxt span{font:800 14px/1.2 "Baloo 2",sans-serif;color:#3a2414;background:#fff7e8;border:2.5px solid #3a2414;border-radius:999px;padding:7px 14px 6px;box-shadow:0 3px 0 #3a2414}
#ovMap .celTxt em{font-style:normal;font-size:34px;color:#ffd84d;-webkit-text-stroke:1.5px #3a2414;letter-spacing:.2em;animation:celStar 1s ease-in-out infinite alternate}
@keyframes celStar{to{transform:scale(1.15)}}
#ovMap .celConf{position:absolute;left:50%;top:45%;width:0;height:0}
#ovMap .celConf i{position:absolute;width:10px;height:14px;border-radius:2px;background:var(--c);border:1.5px solid rgba(58,36,20,.6);opacity:0}
#ovMap .mapCel.on .celConf i{animation:celConf 1.9s cubic-bezier(.15,.7,.3,1) var(--d) forwards}
@keyframes celConf{0%{opacity:1;transform:translate(0,0) rotate(0)}70%{opacity:1}100%{opacity:0;transform:translate(calc(var(--x) * 46vw),calc(var(--y) * 42vh + 30vh)) rotate(var(--r))}}
#ovMap .mapMe.fly img{animation:mFly .45s ease-in-out infinite alternate!important;box-shadow:0 3px 0 #3a2414,0 14px 14px rgba(0,0,0,.25)}
@keyframes mFly{from{transform:rotate(-8deg) translateY(-3px)}to{transform:rotate(8deg) translateY(-9px)}}
#ovMap .mPin.pop i{animation:mPinPop .6s cubic-bezier(.2,1.8,.4,1)}
@keyframes mPinPop{0%{transform:scale(.2)}100%{transform:scale(1)}}
@media (prefers-reduced-motion:reduce){#ovMap .celRays{animation:none}}
</style>
'''
i = s.rfind('</body>'); s = s[:i] + css + s[i:]
open(dst, 'w', encoding='utf-8').write(s); print('ok')
