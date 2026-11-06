"""V326 (Martin 06.11. 21:59): Sidewinder – ZUERST ein Screen «+90° / −90°», DANN erst das Spielfeld drehen.
Karte #ovTilt (gelb-schwarz, Pfeil in Drehrichtung, Winkel groß) für 2,2 s oder bis Tipp; währenddessen steht das Spiel (S.tiltCard in frozen()),
Musik läuft weiter. Erst danach setRotMode + Drehanimation + «SIDEWINDER!»-Meldung."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V325";', 'const GAME_VER = "V326";')
# CSS
rep('@media (prefers-reduced-motion: reduce){canvas#cv{transition:none}.board.tilting{animation:none}}',
'''@media (prefers-reduced-motion: reduce){canvas#cv{transition:none}.board.tilting{animation:none}}
#ovTilt{position:fixed;inset:0;z-index:70;display:flex;align-items:center;justify-content:center;background:rgba(10,12,8,.6);padding:16px;cursor:pointer}
#ovTilt[hidden]{display:none}
#ovTilt .tcard{width:min(300px,86vw);display:flex;flex-direction:column;align-items:center;gap:6px;padding:16px 14px 14px;border:3px solid #17150c;border-radius:12px;box-shadow:0 8px 0 #17150c;
  background:repeating-linear-gradient(-45deg,#f0b323 0 14px,#17150c 14px 28px);animation:tcIn .35s cubic-bezier(.3,1.6,.5,1)}
#ovTilt .tin{width:100%;display:flex;flex-direction:column;align-items:center;gap:2px;background:#fff4cf;border:3px solid #17150c;border-radius:8px;padding:10px 8px 8px;color:#17150c}
#ovTilt small{font-family:var(--f-ui);font-weight:800;font-size:12px;letter-spacing:.16em}
#ovTilt b{font-family:var(--f-display);font-weight:400;font-size:64px;line-height:1;letter-spacing:.02em}
#ovTilt svg{width:72px;height:72px;animation:tcSpin 1.4s ease-in-out infinite}
#ovTilt.neg svg{transform:scaleX(-1)}
#ovTilt i{font-style:normal;font-family:var(--f-ui);font-weight:700;font-size:12px;opacity:.75}
@keyframes tcIn{from{transform:scale(.6);opacity:0}to{transform:none;opacity:1}}
@keyframes tcSpin{0%,20%{rotate:0deg}70%,100%{rotate:90deg}}
#ovTilt.neg svg{animation-name:tcSpinN}
@keyframes tcSpinN{0%,20%{rotate:0deg}70%,100%{rotate:-90deg}}
@media (prefers-reduced-motion: reduce){#ovTilt svg,#ovTilt .tcard{animation:none}}''')
# HTML
rep('<div class="mayday tiltBand" id="tiltBand" hidden>',
'<div id="ovTilt" hidden><div class="tcard"><div class="tin"><small>SIDEWINDER</small><svg viewBox="0 0 48 48" aria-hidden="true"><path d="M24 8a16 16 0 1 1-15.2 11" fill="none" stroke="#17150c" stroke-width="5" stroke-linecap="round"/><path d="M2 14l7 9 8-8z" fill="#17150c"/></svg><b id="tiltDeg">+90°</b><i>Field turns · blocks still fall down</i></div></div></div>\n      <div class="mayday tiltBand" id="tiltBand" hidden>')
# frozen + Musik
rep('S.ordersOpen || S.mix; }', 'S.ordersOpen || S.mix || S.tiltCard; }')
rep('!S.drop && !S.alert && !S.mix && !S.duel && !S.mapShow);', '!S.drop && !S.alert && !S.mix && !S.duel && !S.mapShow && !S.tiltCard);')
# uiWinOpen: Meldungen warten
rep('return !!(window.__tipBulb && window.__tipBulb.open) || v("ovIntro")', 'return !!(window.__tipBulb && window.__tipBulb.open) || v("ovTilt") || v("ovIntro")')
# Ablauf: erst Karte, dann drehen
rep('''    S.rotT = S.rotT || 0; if (!S.rotMode) { if (S.rotNW !== S.wave) { S.rotNW = S.wave; S.rotN = (S.rotN || 0) + 1; } setRotMode(S.rotN % 2 === 0 ? 2 : 1); }   /* V293: abwechselnd −90° / +90° */
    snd("siren"); setTimeout(() => { if (rotOn()) announce("SIDEWINDER!", "Field tilts 90° · blocks still fall down", "ALERT", 2800); }, 250);
    setTimeout(() => SFX.say("Hold the line!"), 900);
  }''',
'''    S.rotT = S.rotT || 0; if (!S.rotMode) { if (S.rotNW !== S.wave) { S.rotNW = S.wave; S.rotN = (S.rotN || 0) + 1; } tiltCard(S.rotN % 2 === 0 ? 2 : 1); }   /* V293: abwechselnd −90° / +90° · V326: erst Karte */
    else { snd("siren"); setTimeout(() => { if (rotOn()) announce("SIDEWINDER!", "Field tilts 90° · blocks still fall down", "ALERT", 2800); }, 250); setTimeout(() => SFX.say("Hold the line!"), 900); }
  }''')
rep('function stepRot(dt) {', '''// V326: Ankündigungs-Karte «+90° / −90°»; erst wenn sie zu ist, dreht sich das Feld (rotMode 1 = −90°, 2 = +90°)
function tiltCard(m) {
  const ov = $("ovTilt"); S.tiltCard = { m }; $("tiltDeg").textContent = m === 2 ? "+90°" : "−90°"; ov.classList.toggle("neg", m === 1); ov.hidden = false;
  snd("siren"); try { if (navigator.vibrate) navigator.vibrate(50); } catch (e) {}
  let done = false; const go = () => { if (done) return; done = true; clearTimeout(t); ov.hidden = true; ov.onclick = null; const c = S.tiltCard; S.tiltCard = null;
    if (!c || !S.started || S.over) return; setRotMode(c.m); syncRotView();
    setTimeout(() => { if (rotOn()) announce("SIDEWINDER!", "Blocks still fall down", "ALERT", 2400); }, 1200); setTimeout(() => SFX.say("Hold the line!"), 600); };
  const t = setTimeout(go, 2200); setTimeout(() => { ov.onclick = go; }, 400);
}
window.__tiltCard = () => S && S.tiltCard ? S.tiltCard.m : 0;
function stepRot(dt) {''')
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
# --- Teil 2 (Martin 22:06): App-Start zeigt zuerst das Titelbild, dazu laufende Punkte bis die Seite geladen ist ---
s = open(dst, encoding='utf-8').read()
rep('#splash.out{opacity:0;pointer-events:none}',
'''#splash.out{opacity:0;pointer-events:none}
#splash .spDots{position:absolute;bottom:calc(env(safe-area-inset-bottom,0px) + 6vh + 6px);display:flex;gap:12px}
#splash .spDots i{width:14px;height:14px;border-radius:50%;background:#fff6e6;border:2px solid #3a1d10;animation:spDot 1s ease-in-out infinite}
#splash .spDots i:nth-child(2){animation-delay:.15s}#splash .spDots i:nth-child(3){animation-delay:.3s}
@keyframes spDot{0%,60%,100%{transform:translateY(0);opacity:.55}30%{transform:translateY(-12px);opacity:1}}
#splash.loading .spGo{display:none}#splash:not(.loading) .spDots{display:none}
#splash.twa .spT{animation:none!important}''')
rep('<div class="spGo">TAP TO START</div></div>', '<div class="spGo">TAP TO START</div><div class="spDots" aria-hidden="true"><i></i><i></i><i></i></div></div>')
rep('<div id="splash" role="button" aria-label="Tap to start">', '<div id="splash" class="loading" role="button" aria-label="Tap to start">')
rep('''(function () { const sp = document.getElementById("splash"); if (!sp) return; let done = false;''',
'''(function () { const sp = document.getElementById("splash"); if (!sp) return; let done = false;
  /* V326: in der Android-App (TWA) kommt das Titelbild schon als Startbild – Titel nicht nochmal einfliegen lassen; Punkte laufen bis geladen (mind. 1,2 s) */
  try { if (/^android-app:/.test(document.referrer || "")) sp.classList.add("twa"); } catch (e) {}
  { const t0 = performance.now(), ready = () => setTimeout(() => sp.classList.remove("loading"), Math.max(0, 1200 - (performance.now() - t0)));
    if (document.readyState === "complete") ready(); else window.addEventListener("load", ready, { once: true }); setTimeout(() => sp.classList.remove("loading"), 5000); }''')
open(dst, 'w', encoding='utf-8').write(s)
print("ok2")
