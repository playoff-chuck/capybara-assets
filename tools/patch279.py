"""V279 (Martin 16:21): Weltkarten-Musikübergänge nacheinander statt überlappend.
Karte auf: Level-Musik blendet in 1,5 s aus, danach blendet die Weltkarten-Musik in 2 s ein.
Karte zu (Weitertippen/Ende) oder Ankunftsbild erscheint: Weltkarten-Musik blendet in 1,5 s aus, danach Level-Musik in 2 s ein.
Gilt für Ortswechsel, Kontinentflug, Welttour-Start und die Karte aus dem Menü.
Martin 16:22: Sale-Sticker (−61 %, DEAL, HOT!) haben eigene Sternplakette und wackeln gemeinsam mit ihr (Sternform per clip-path, Größe 23 % der Bildbreite).
Martin 16:23: Sprecherstimme 10 % leiser (0,36 → 0,324), Musik gleich.
Martin 16:24: gelber Comic-Pfeil nur noch im Tutorial."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V278";', 'const GAME_VER = "V279";')
# Karte auf: erst Level aus (1,5 s), dann Karte ein (2 s)
rep('''on = true; bus = ac.createGain(); bus.gain.value = 0.0001; bus.connect(out); step = 0; nextT = ac.currentTime + 0.15; timer = setInterval(sched, 60); sched();
      try { if (typeof TP !== "undefined" && TP.el && TP.key && !TP.el.paused) { heldTP = true; tpFade(0.0001, 0.8); setTimeout(() => { if (on && heldTP && TP.el) TP.el.pause(); }, 850); }''',
    '''on = true; clearTimeout(resumeT); bus = ac.createGain(); bus.gain.value = 0.0001; bus.connect(out); step = 0; nextT = ac.currentTime + 1.5; inAt = ac.currentTime + 1.5; timer = setInterval(sched, 60); sched();
      try { if (typeof TP !== "undefined" && TP.el && TP.key && !TP.el.paused) { heldTP = true; tpFade(0.0001, 1.5); setTimeout(() => { if (on && heldTP && TP.el) TP.el.pause(); }, 1560); }''')
rep('''if (!on) return; const vv = vol(); bus.gain.setTargetAtTime(0.9 * vv + 0.0001, ac.currentTime, 0.3);''',
    '''if (!on) return; const vv = vol(), tn = ac.currentTime; if (tn >= inAt) { if (!rampDone) { rampDone = true; bus.gain.cancelScheduledValues(tn); bus.gain.setValueAtTime(0.0001, tn); bus.gain.linearRampToValueAtTime(0.9 * vv + 0.0001, tn + 2); fadeEnd = tn + 2; } else if (tn > fadeEnd) bus.gain.setTargetAtTime(0.9 * vv + 0.0001, tn, 0.3); }''')
rep('let on = false, ac = null, bus = null, step = 0, nextT = 0, timer = null, nb = null, heldTP = false, heldSyn = false;',
    'let on = false, ac = null, bus = null, step = 0, nextT = 0, timer = null, nb = null, heldTP = false, heldSyn = false, inAt = 0, rampDone = false, fadeEnd = 0, resumeT = null;')
rep('function start() { if (on) return;', 'function start() { if (on) return; rampDone = false;')
# Karte zu: erst Karte aus (1,5 s), dann Level ein (2 s)
rep('''function stop() { if (!on) return; on = false; clearInterval(timer); try { const g = bus; g.gain.setTargetAtTime(0.0001, ac.currentTime, 0.25); setTimeout(() => { try { g.disconnect(); } catch (e) {} }, 1500); } catch (e) {}
      try { if (heldTP) { heldTP = false; if (TP.el && TP.key && !TP.paused) { const p = TP.el.play(); if (p && p.catch) p.catch(() => {}); tpFade(0.5, 1.0); } }''',
    '''function stop() { if (!on) return; on = false; try { const g = bus, t = ac.currentTime; g.gain.cancelScheduledValues(t); g.gain.setValueAtTime(Math.max(0.0001, g.gain.value), t); g.gain.linearRampToValueAtTime(0.0001, t + 1.5); const tm = timer; setTimeout(() => { clearInterval(tm); try { g.disconnect(); } catch (e) {} }, 1600); } catch (e) { clearInterval(timer); }
      try { if (heldTP) { heldTP = false; clearTimeout(resumeT); resumeT = setTimeout(() => { if (on) { heldTP = true; return; } if (TP.el && TP.key && !TP.paused) { TP.el.volume = 0; const p = TP.el.play(); if (p && p.catch) p.catch(() => {}); tpFade(0.5, 2.0); } }, 1500); }''')
# Ankunftsbild zählt als «Karte zu»: Karten-Musik raus, dann Level-Musik
rep('''setInterval(() => { const up = document.body.classList.contains("mapUp") && !document.hidden; if (up && !on) start(); else if (!up && on) stop(); }, 250);''',
    '''setInterval(() => { const up = document.body.classList.contains("mapUp") && !document.hidden && !document.querySelector("#ovMap .mapArrive"); if (up && !on) start(); else if (!up && on) stop(); }, 250);''')
# Welttour-Start: Level-Musik erst nach dem Ausblenden der Karten-Musik
rep('''        try { SFX.music.start(1); } catch (e) {} try { SFX.say && SFX.say("welcome", 1.0, 1.0, "welcome"); } catch (e) {} });''',
    '''        setTimeout(() => { try { if (SFX.music.playing < 1) SFX.music.start(1); } catch (e) {} }, 1500); try { SFX.say && SFX.say("welcome", 1.0, 1.0, "welcome"); } catch (e) {} });''')

rep('const TP = { el: null,', 'window.__tpDbg = () => TP; const TP = { el: null,')
css2 = r'''
<style id="v279badge">
#adPic{container-type:inline-size}
.adCard .saleSt{width:23%;aspect-ratio:1;display:flex!important;align-items:center;justify-content:center;text-align:center;isolation:isolate;font-size:6.2cqw;line-height:1;-webkit-text-stroke:.9px #6a0d0d;color:#fff;text-shadow:0 2px 0 #6a0d0d}
.adCard:not(.sale) .saleSt{display:none!important}
.adCard .saleSt::before,.adCard .saleSt::after{content:"";position:absolute;inset:0;z-index:-1;clip-path:POLY}
.adCard .saleSt::before{background:#ffd23a;transform:scale(1.1)}
.adCard .saleSt::after{background:radial-gradient(circle at 40% 35%,#ff5a4a,#d81e1e 60%,#a51010);inset:4%}
.adCard .saleSt.s2{color:#d81e1e;-webkit-text-stroke:.9px #6a3a08;text-shadow:0 2px 0 #fff3b0;font-size:5.6cqw}
.adCard .saleSt.s2::before{background:#d81e1e}
.adCard .saleSt.s2::after{background:radial-gradient(circle at 40% 35%,#fff3a0,#ffc928 60%,#e8a010)}
.adCard .saleSt.s3{font-size:5.6cqw}
</style>
'''.replace("POLY", "polygon(50.0% 0.0%,59.1% 10.0%,71.7% 5.0%,75.6% 17.9%,89.1% 18.8%,86.9% 32.2%,98.7% 38.9%,91.0% 50.0%,98.7% 61.1%,86.9% 67.8%,89.1% 81.2%,75.6% 82.1%,71.7% 95.0%,59.1% 90.0%,50.0% 100.0%,40.9% 90.0%,28.3% 95.0%,24.4% 82.1%,10.9% 81.2%,13.1% 67.8%,1.3% 61.1%,9.0% 50.0%,1.3% 38.9%,13.1% 32.2%,10.9% 18.8%,24.4% 17.9%,28.3% 5.0%,40.9% 10.0%)")
i = s.rindex('</body>'); s = s[:i] + css2 + s[i:]
# Martin 16:23: Sprecherstimme 10 % leiser, Musik unverändert
rep('g.gain.value = 0.36 * [1, 0.72, 0.42, 0.14]', 'g.gain.value = 0.324 * [1, 0.72, 0.42, 0.14]')
# Martin 16:24: gelber Comic-Pfeil nur noch im Tutorial (bei Erstes-Mal-Hinweisen zeigte er im Shop ins Leere)
rep('const a = document.getElementById("coachArrow"); if (a && a.style.display === "block") {', 'const a = null; if (a && a.style.display === "block") {')
# Plaketten ganz im Bild halten und nicht unter die WAVE-Marke oben rechts legen
rep('if (el && a.st) { el.style.left = a.st[n - 1][0] + "%"; el.style.top = a.st[n - 1][1] + "%"; }',
    'if (el && a.st) { let x = Math.max(13, Math.min(87, a.st[n - 1][0])), y = Math.max(15, Math.min(85, a.st[n - 1][1])); if (x > 66 && y < 30) y = 33; el.style.left = x + "%"; el.style.top = y + "%"; }')
open(dst, 'w', encoding='utf-8').write(s)
