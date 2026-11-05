"""V258 (Martin 05.11. 13:42–13:45):
- Neues Logo: unverändert, nur der unterste Stein entfernt (Capybara sitzt auf drei Steinen) – img/logo_main.webp/logo_small.webp,
  MAIN_LOGO-Version hochgezählt.
- Flugzeug auf der Weltkarte mit realistischem Geräusch statt Pieps-Effekten: Propellermotor (zwei leicht verstimmte Sägezähne,
  Tiefpass, Propeller-Flattern, Luftrauschen), beim Start Hochlaufen von Drehzahl und Lautstärke, im Flug leichter Doppler,
  beim Landen Gas weg, Reifenquietschen und dumpfes Aufsetzen. Alte «engine»/«whoosh»-Effekte beim Flug entfernt.
- Dev-Leiste: «Street player» (2× tippen) setzt alles auf einen ganz neuen Spieler zurück (Regeln, Tutorial, Onboarding,
  Karten-Intro, Rufzeichen, Fortschritt, Medaillen, Spielstand) – nur der Dev-Modus bleibt an; Seite lädt neu.
  «Intros: on/off» blendet beim Testen alle Neuheiten-Fenster und Anzeigen aus (gilt nur im Dev-Modus)."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V257";', 'const GAME_VER = "V258";')
rep('MAIN_LOGO = "img/logo_main.webp?v=227"', 'MAIN_LOGO = "img/logo_main.webp?v=258"')
s = s.replace('img/logo_small.webp"', 'img/logo_small.webp?v=258"')
# Flugzeug-Geräusch
rep('at(4400, () => { label("", "Flying to " + nice(contName(P.c)), ""); fx("engine"); whoosh(); flyPlane(', 'at(4400, () => { label("", "Flying to " + nice(contName(P.c)), ""); flyPlane(')
rep('      at(5600, whoosh);\n', '')
rep('requestAnimationFrame(step); try { SFX.swoosh && SFX.swoosh(); } catch (e) {} }', 'requestAnimationFrame(step); try { window.__planeSnd && window.__planeSnd(ms, a[0] > 1 || a[0] < 0); } catch (e) {} }')
# Dev-Knöpfe
rep('<div class="dRow dT"><button id="devSpec">Specials</button><button id="devZero">Test from 0</button><button id="devBandit">Bandit</button></div>',
    '<div class="dRow dT"><button id="devSpec">Specials</button><button id="devZero">Test from 0</button><button id="devBandit">Bandit</button></div><div class="dRow dR"><button id="devFresh">Street player</button><button id="devIntro">Intros: on</button></div>')
css = r'''
<style id="v258dev">
#devBar .dR{grid-template-columns:1fr 1fr}
#devBar .dR button{background:#e86fa3!important;color:#fff!important;border:0!important;font-size:11px!important}
#devBar .dR button.armed{background:#e0262a!important}
#devBar .dR #devIntro.off{background:#7a6650!important}
</style>
'''
js = r'''
  /* V258: realistisches Flugzeug-Geräusch */
  try { window.__planeSnd = (ms, fromOff) => {
      const ac = AU.ac(), out = AU.out(); if (!ac || !out) return; const T = ac.currentTime + 0.02, D = Math.max(1.2, ms / 1000);
      const up = fromOff ? 0.25 : 0.9, down = 0.9;   // Hochlauf / Gas weg (s)
      const g = ac.createGain(), lp = ac.createBiquadFilter(), am = ac.createGain(), lfo = ac.createOscillator(), lfoG = ac.createGain();
      lp.type = "lowpass"; lp.Q.value = 0.7; am.gain.value = 1; lfo.frequency.value = 22; lfoG.gain.value = 0.28; lfo.connect(lfoG); lfoG.connect(am.gain);
      const o1 = ac.createOscillator(), o2 = ac.createOscillator(); o1.type = "sawtooth"; o2.type = "sawtooth";
      const f0 = fromOff ? 104 : 62, f1 = 112, f2 = 58;
      [o1, o2].forEach((o, i) => { const k = i ? 1.012 : 1; o.frequency.setValueAtTime(f0 * k, T); o.frequency.linearRampToValueAtTime(f1 * k, T + up); o.frequency.linearRampToValueAtTime(f1 * 0.94 * k, T + D * 0.55); o.frequency.linearRampToValueAtTime(f2 * k, T + D); o.connect(lp); });
      lp.frequency.setValueAtTime(fromOff ? 900 : 350, T); lp.frequency.linearRampToValueAtTime(1100, T + up); lp.frequency.linearRampToValueAtTime(420, T + D);
      const v = 0.05; g.gain.setValueAtTime(0.0001, T); g.gain.exponentialRampToValueAtTime(fromOff ? v * 0.8 : v * 0.35, T + 0.15); g.gain.exponentialRampToValueAtTime(v, T + up); g.gain.setValueAtTime(v, T + D - down); g.gain.exponentialRampToValueAtTime(v * 0.25, T + D); g.gain.exponentialRampToValueAtTime(0.0001, T + D + 0.6);
      lp.connect(am); am.connect(g); g.connect(out);
      // Luftrauschen (Propeller-Wind)
      const n = ac.createBuffer(1, ac.sampleRate * 2, ac.sampleRate), d = n.getChannelData(0); for (let i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1;
      const ns = ac.createBufferSource(), bp = ac.createBiquadFilter(), ng = ac.createGain(); ns.buffer = n; ns.loop = true; bp.type = "bandpass"; bp.frequency.value = 520; bp.Q.value = 0.6;
      ng.gain.setValueAtTime(0.0001, T); ng.gain.exponentialRampToValueAtTime(0.03, T + up); ng.gain.setValueAtTime(0.03, T + D - down); ng.gain.exponentialRampToValueAtTime(0.0001, T + D + 0.4);
      ns.connect(bp); bp.connect(ng); ng.connect(out);
      [o1, o2, lfo, ns].forEach(x => { x.start(T); x.stop(T + D + 0.7); });
      // Landung: zwei kurze Reifen-Quietscher + dumpfes Aufsetzen
      const td = T + D - 0.05;
      [0, 0.13].forEach((dt, i) => { const s2 = ac.createBufferSource(), hp = ac.createBiquadFilter(), sg = ac.createGain(); s2.buffer = n; hp.type = "bandpass"; hp.frequency.value = 2600 + i * 400; hp.Q.value = 4;
        sg.gain.setValueAtTime(0.0001, td + dt); sg.gain.exponentialRampToValueAtTime(i ? 0.03 : 0.045, td + dt + 0.015); sg.gain.exponentialRampToValueAtTime(0.0001, td + dt + 0.16); s2.connect(hp); hp.connect(sg); sg.connect(out); s2.start(td + dt, Math.random()); s2.stop(td + dt + 0.2); });
      const th = ac.createOscillator(), tg = ac.createGain(); th.frequency.setValueAtTime(85, td); th.frequency.exponentialRampToValueAtTime(45, td + 0.18); tg.gain.setValueAtTime(0.0001, td); tg.gain.exponentialRampToValueAtTime(0.22, td + 0.01); tg.gain.exponentialRampToValueAtTime(0.0001, td + 0.3); th.connect(tg); tg.connect(out); th.start(td); th.stop(td + 0.35);
    }; } catch (e) { console.error("planeSnd", e); }
  /* V258: Dev – Street player / Intros aus */
  try { (() => { const fr = document.getElementById("devFresh"), ib = document.getElementById("devIntro"); let arm = 0, armT = null;
      const introsOff = () => LS.get("tarnturm-dev") === "1" && LS.get("tarnturm-devnointro") === "1";
      const paint = () => { if (!ib) return; const off = LS.get("tarnturm-devnointro") === "1"; ib.textContent = off ? "Intros: off" : "Intros: on"; ib.classList.toggle("off", off); }; paint();
      if (ib) ib.addEventListener("click", e => { e.stopPropagation(); LS.set("tarnturm-devnointro", LS.get("tarnturm-devnointro") === "1" ? "0" : "1"); paint(); try { snd("uiTap"); } catch (er) {} });
      if (fr) fr.addEventListener("click", e => { e.stopPropagation(); try { snd("uiTap"); } catch (er) {}
        if (!arm) { arm = 1; fr.textContent = "Tap again"; fr.classList.add("armed"); clearTimeout(armT); armT = setTimeout(() => { arm = 0; fr.textContent = "Street player"; fr.classList.remove("armed"); }, 3000); return; }
        try { const keep = ["tarnturm-dev"]; const ks = []; for (let i = 0; i < localStorage.length; i++) { const k = localStorage.key(i); if (k && /^(tarnturm|capy)/.test(k) && !keep.includes(k)) ks.push(k); } ks.forEach(k => localStorage.removeItem(k)); } catch (er) {}
        try { LS.set = function () {}; Storage.prototype.setItem = function () {}; } catch (er) {}   // nichts mehr zurückschreiben (Spielstand beim Verlassen)
        location.reload(); });
      const _si = showIntro; showIntro = function (q) { if (introsOff()) { try { S.seen = S.seen || {}; S.seen[q.t === "mon" ? q.k : "g:" + q.k] = true; if (q.t === "gear" && q.k === "ton" && !S.tonIntroGift) { S.tonIntroGift = true; S.tons = (S.tons || 0) + 1; } } catch (e) {} return; } return _si.apply(this, arguments); };
    })(); } catch (e) { console.error("devFresh", e); }
'''
i = s.rfind('</body>'); s = s[:i] + css + s[i:]
i = s.rfind('})();\n</script>'); s = s[:i] + js + s[i:]
open(dst, 'w', encoding='utf-8').write(s); print('ok')
