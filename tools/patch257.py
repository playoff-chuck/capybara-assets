"""V257: Eigene Weltkarten-Musik (Martin 05.11. 13:33): ganz entspannter, reduzierter, bassiger Low-Beat (78 BPM, A-Moll):
weicher Kick, warmer Sub-Bass mit Groove, leiser Rimshot, sanfte geswingte Hi-Hats, Rhodes-artige Akkordflächen
(Am7 – Dm9 – Fmaj7 – Em7). Läuft, solange die Weltkarte offen ist (Menü, Pause, Orts- und Kontinent-Szenen); die normale
Musik blendet dabei aus und danach wieder ein. Lautstärke folgt dem Musik-Regler, Stumm-Schalter gilt."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V256";', 'const GAME_VER = "V257";')
js = r'''
  /* V257: Weltkarten-Musik – Low-Beat */
  try { (() => {
    const BPM = 78, ST = 60 / BPM / 4;   // Sechzehntel
    let on = false, ac = null, bus = null, step = 0, nextT = 0, timer = null, nb = null, heldTP = false, heldSyn = false;
    const CH = [[220, 261.6, 329.6, 392], [146.8, 220, 261.6, 329.6], [174.6, 220, 261.6, 329.6], [164.8, 196, 246.9, 293.7]];   // Am7 Dm9 Fmaj7 Em7
    const BASS = [[55, 0], [55, 6], [65.4, 10], [49, 14], [73.4, 0], [73.4, 7], [87.3, 11], [65.4, 14], [87.3, 0], [87.3, 6], [98, 10], [82.4, 14], [82.4, 0], [82.4, 7], [98, 10], [61.7, 13]];
    const vol = () => { try { return SFX.muted ? 0 : Math.min(1, 0.6 * Math.pow(SFX.vol || 0.3, 2) * 1.5) * Math.pow(SFX.ch("m"), 2); } catch (e) { return 0.2; } };
    function noise() { if (nb) return nb; const n = ac.createBuffer(1, ac.sampleRate, ac.sampleRate), d = n.getChannelData(0); for (let i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1; return nb = n; }
    function env(g, t, v, a, d) { g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(Math.max(0.0002, v), t + a); g.gain.exponentialRampToValueAtTime(0.0001, t + a + d); }
    function osc(type, f, t, v, a, d, lp) { const o = ac.createOscillator(), g = ac.createGain(); o.type = type; o.frequency.setValueAtTime(f, t); let n = o; if (lp) { const fl = ac.createBiquadFilter(); fl.type = "lowpass"; fl.frequency.value = lp; o.connect(fl); n = fl; } n.connect(g); g.connect(bus); env(g, t, v, a, d); o.start(t); o.stop(t + a + d + 0.05); return o; }
    function kick(t, v) { const o = ac.createOscillator(), g = ac.createGain(); o.frequency.setValueAtTime(78, t); o.frequency.exponentialRampToValueAtTime(42, t + 0.12); o.connect(g); g.connect(bus); env(g, t, v, 0.004, 0.32); o.start(t); o.stop(t + 0.4); }
    function hiss(t, f, type, v, d) { const sN = ac.createBufferSource(), fl = ac.createBiquadFilter(), g = ac.createGain(); sN.buffer = noise(); fl.type = type; fl.frequency.value = f; fl.Q.value = 0.9; sN.connect(fl); fl.connect(g); g.connect(bus); env(g, t, v, 0.002, d); sN.start(t, Math.random() * 0.5); sN.stop(t + d + 0.05); }
    function bar(b, t0) {
      const c = CH[b % 4];   // Akkordfläche: weich, gefiltert, leicht verstimmt
      c.forEach((f, i) => { osc("sine", f, t0 + i * 0.012, 0.035, 0.35, ST * 15, 1400); osc("triangle", f * 1.003, t0 + i * 0.012, 0.018, 0.4, ST * 14, 900); });
      if (b % 2 === 1) c.slice(1).forEach((f, i) => osc("sine", f * 2, t0 + ST * (10 + i), 0.012, 0.02, 0.5, 2400));   // kleiner Rhodes-Tupfer
    }
    function sched() {
      if (!on) return; const vv = vol(); bus.gain.setTargetAtTime(0.9 * vv + 0.0001, ac.currentTime, 0.3);
      while (nextT < ac.currentTime + 0.25) {
        const s16 = step % 16, b = Math.floor(step / 16), t = nextT + (s16 % 2 ? ST * 0.18 : 0);   // Swing auf den Off-Sechzehnteln
        if (s16 === 0) bar(b, nextT);
        if (s16 === 0 || s16 === 10 || (b % 4 === 3 && s16 === 14)) kick(t, s16 === 0 ? 0.55 : 0.38);
        if (s16 === 4 || s16 === 12) hiss(t, 1900, "bandpass", 0.06, 0.06);
        if (s16 % 2 === 0) hiss(t, 7000, "highpass", s16 % 4 === 2 ? 0.022 : 0.012, 0.03);
        for (const [f, at] of BASS.slice((b % 4) * 4, (b % 4) * 4 + 4)) if (at === s16) { osc("sine", f, t, 0.3, 0.01, ST * 3.2); osc("triangle", f * 2, t, 0.05, 0.01, ST * 2, 500); }
        nextT += ST; step++;
      }
    }
    function start() { if (on) return; try { SFX.init(); } catch (e) {} ac = (typeof AU !== "undefined" && AU.ac()) || null; const out = SFX._out && SFX._out(); if (!ac || !out) return;
      on = true; bus = ac.createGain(); bus.gain.value = 0.0001; bus.connect(out); step = 0; nextT = ac.currentTime + 0.15; timer = setInterval(sched, 60); sched();
      try { if (typeof TP !== "undefined" && TP.el && TP.key && !TP.el.paused) { heldTP = true; tpFade(0.0001, 0.8); setTimeout(() => { if (on && heldTP && TP.el) TP.el.pause(); }, 850); }
            else if (SFX.music && SFX.music.dim) { heldSyn = true; SFX.music.dim(0.12); } } catch (e) {} }
    function stop() { if (!on) return; on = false; clearInterval(timer); try { const g = bus; g.gain.setTargetAtTime(0.0001, ac.currentTime, 0.25); setTimeout(() => { try { g.disconnect(); } catch (e) {} }, 1500); } catch (e) {}
      try { if (heldTP) { heldTP = false; if (TP.el && TP.key && !TP.paused) { const p = TP.el.play(); if (p && p.catch) p.catch(() => {}); tpFade(0.5, 1.0); } }
            if (heldSyn) { heldSyn = false; SFX.music.dim(1); } } catch (e) {} }
    setInterval(() => { const up = document.body.classList.contains("mapUp") && !document.hidden; if (up && !on) start(); else if (!up && on) stop(); }, 250);
    window.__TT && (window.__TT.mapMusic = { start, stop, get on() { return on; } });
  })(); } catch (e) { console.error("mapMusic", e); }
'''
i = s.rfind('})();\n</script>'); s = s[:i] + js + s[i:]
open(dst, 'w', encoding='utf-8').write(s); print('ok')
