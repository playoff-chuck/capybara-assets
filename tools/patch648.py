#!/usr/bin/env python3
# V648 (Martin 12.11. 09:55, Klangvergleich Runde 2): gewählte Klänge als kurze Samples (sfx/fx_*.mp3, selbst synthetisiert, 180–4500 Hz):
# Stein landet B · Reihe A · Splat B (Kette: jeder weitere Splat in 1,6 s einen Halbton höher, max. +7) · MG B (ein Schuss) · Münze B · Kanone (Runde 1).
# Fällt zurück auf den alten Klang, solange die Datei nicht geladen ist.
# Dazu: Diplom-Spruch ohne Funk-Rauschen und 30 % lauter, Fanfare vorher ausgeblendet.
import sys, os
site = sys.argv[1]; p = os.path.join(site, "index.html"); s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V647";', 'const GAME_VER = "V648";')
JS = r'''
/* V648: gewählte Klänge als Samples */
try { (() => { const FX = { lock: 1, lines: 1, splat: 1, mg: 1, coin: 1, kan: 1 }, GAIN = { lock: 0.7, lines: 0.6, splat: 1.1, mg: 0.8, coin: 0.7, kan: 0.7 }, BUFX = {}, last = {}; let loading = false, chainN = 0, chainT = -9;
  function load(ac) { loading = true; for (const k in FX) fetch(`sfx/fx_${k}.mp3?v=648`).then(r => r.arrayBuffer()).then(b => ac.decodeAudioData(b)).then(buf => { BUFX[k] = buf; }).catch(() => {}); }
  const _play = SFX.play;
  SFX.play = (n, ...a) => { try { if (FX[n]) { const ac = SFX._ac(), out = SFX._out(); if (ac && !loading) load(ac); const buf = BUFX[n];
      if (ac && out && buf) { const now = ac.currentTime; if (now - (last[n] == null ? -9 : last[n]) < (n === "mg" ? 0.05 : 0.03)) return; last[n] = now;
        let rate = 1; if (n === "splat") { chainN = now - chainT < 1.6 ? Math.min(7, chainN + 1) : 0; chainT = now; rate = Math.pow(2, chainN / 12); }
        const src = ac.createBufferSource(), g = ac.createGain(), v = GAIN[n] || 1, d = buf.duration / rate; src.buffer = buf; src.playbackRate.value = rate;
        g.gain.setValueAtTime(0, now); g.gain.linearRampToValueAtTime(v, now + 0.003); g.gain.setValueAtTime(v, now + Math.max(0.004, d - 0.01)); g.gain.linearRampToValueAtTime(0, now + d);
        src.connect(g); g.connect(out); src.start(now); src.onended = () => { try { g.disconnect(); } catch (e) {} }; return; } } } catch (e) {} return _play(n, ...a); };
})(); } catch (e) { console.error("v648", e); }
'''
rep('let snd = (n, ...a) => SFX.play(n, ...a);   /* V430: let – V421 umhüllt snd */',
    'let snd = (n, ...a) => SFX.play(n, ...a);   /* V430: let – V421 umhüllt snd */' + JS)

# Diplom (Martin 09:58): Spruch nach der Fanfare ohne Funk-Rauschen/Knistern, klar und 30 % lauter; Fanfare blendet vor dem Spruch aus (4,1–4,4 s)
rep('if (/^thief_/.test(String(text))) {', 'const clean = String(text) === "cert_done"; if (clean) { hp.frequency.value = 70; lp.frequency.value = 12000; pk.gain.value = 0; } else if (/^thief_/.test(String(text))) {')
rep('g.gain.value = 0.324 * [1, 0.72, 0.42, 0.14][Math.min(3, deg)];', 'g.gain.value = 0.324 * [1, 0.72, 0.42, 0.14][Math.min(3, deg)]; if (clean) g.gain.value *= 1.3;   /* V648: Diplom-Spruch +30 % */')
rep('for (let k = 0, at = t0; at < t0 + dur; k++) { const len = 0.12 + Math.random() * 0.25, lvl = 0.82', 'if (!clean) for (let k = 0, at = t0; at < t0 + dur; k++) { const len = 0.12 + Math.random() * 0.25, lvl = 0.82')
i0 = s.index('const hiss = Math.random() < 0.7, f1 = 1800'); end = 'if (hiss) noise(0.14, 0.035, "bandpass", 2400, 1600, dur + 0.14, 0.6, 0, voiceOut || master);'; i1 = s.index(end, i0) + len(end)
seg = s[i0:i1]; n0 = seg.count("noise(")
seg = seg.replace("noise(", "clean || noise(").replace('osc("square"', 'clean || osc("square"')
s = s[:i0] + seg + s[i1:]; assert n0 >= 6, n0
rep('const pr = fa.play(); if (pr && pr.catch) pr.catch(() => {}); return; }',
    'const pr = fa.play(); if (pr && pr.catch) pr.catch(() => {}); const v0 = fa.volume; setTimeout(() => { let i = 0; const iv = setInterval(() => { i++; try { fa.volume = Math.max(0, v0 * (1 - i / 16)); } catch (e) {} if (i >= 16) { clearInterval(iv); try { fa.pause(); } catch (e) {} } }, 20); }, 4100); return; }   /* V648: Fanfare vor dem Spruch aus */')
open(p, "w", encoding="utf-8").write(s)
print("ok V648")
