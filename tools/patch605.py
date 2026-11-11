#!/usr/bin/env python3
# V605 (Martin 11.11. 08:20): «Musik soll vor Diplom ausklingen. Dann bei Diplom einen feierlichen Tusch.»
# Ausklingen jetzt immer (Datei- und Synth-Musik, 3 s über SFX.music.stop(3)); beim Erscheinen des Diploms ein festlicher Tusch
# (Blechbläser-Akkorde «ta-ta-ta-taaa» + Pauken-Wirbel + Becken, WebAudio, Lautstärke nach Ton-Einstellung).
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V604";', 'const GAME_VER = "V605";')
rep('''    let fade = false; try { if (TP.key && TP.el && !TP.el.paused) { tpFade(0.0001, 3); fade = true; } } catch (e) {}''',
    '''    let fade = false; try { if (SFX.music && SFX.music.on) { SFX.music.stop(3); fade = true; } } catch (e) {}   /* V605: Datei- und Synth-Musik */''')
rep('''sum.hidden = false; requestAnimationFrame(() => sum.classList.add("on")); try { snd("powerup"); } catch (e) {} };''',
    '''sum.hidden = false; requestAnimationFrame(() => sum.classList.add("on")); try { certTusch(); } catch (e) { try { snd("powerup"); } catch (x) {} } };''')
rep('''function certQuiet() {''', '''function certTusch() {   /* V605: festlicher Tusch zum Diplom */
  if (SFX.muted || SFX.vol === 0) return; const A = window.__tuschAC || (window.__tuschAC = new (window.AudioContext || window.webkitAudioContext)()); try { A.resume(); } catch (e) {}
  const out = A.createGain(); out.gain.value = Math.min(1, 0.55 * Math.pow(SFX.vol || 0.3, 0.6)); out.connect(A.destination); const t0 = A.currentTime + 0.05;
  const brass = (f, t, d, v) => { for (const det of [-6, 0, 7]) { const o = A.createOscillator(), g = A.createGain(), lp = A.createBiquadFilter(); o.type = "sawtooth"; o.frequency.value = f; o.detune.value = det;
      lp.type = "lowpass"; lp.frequency.setValueAtTime(700, t); lp.frequency.linearRampToValueAtTime(3200, t + 0.06); lp.frequency.exponentialRampToValueAtTime(1400, t + d);
      g.gain.setValueAtTime(0.0001, t); g.gain.linearRampToValueAtTime(v / 3, t + 0.03); g.gain.setValueAtTime(v / 3, t + d - 0.08); g.gain.exponentialRampToValueAtTime(0.0001, t + d + 0.25);
      o.connect(lp); lp.connect(g); g.connect(out); o.start(t); o.stop(t + d + 0.3); } };
  const noise = (t, d, v, type, f) => { const n = A.createBufferSource(), b = A.createBuffer(1, Math.ceil(A.sampleRate * d), A.sampleRate), c = b.getChannelData(0); for (let i = 0; i < c.length; i++) c[i] = Math.random() * 2 - 1;
    n.buffer = b; const fl = A.createBiquadFilter(), g = A.createGain(); fl.type = type; fl.frequency.value = f; g.gain.setValueAtTime(v, t); g.gain.exponentialRampToValueAtTime(0.0001, t + d); n.connect(fl); fl.connect(g); g.connect(out); n.start(t); };
  const M = n => 440 * Math.pow(2, (n - 69) / 12);
  for (let i = 0; i < 10; i++) noise(t0 + i * 0.045, 0.09, 0.22 + i * 0.03, "lowpass", 180);   /* Pauken-Wirbel */
  [[0.45, 0.13], [0.62, 0.13], [0.79, 0.13]].forEach(([dt, d]) => [67, 72, 76].forEach(n => brass(M(n), t0 + dt, d, 0.16)));   /* ta-ta-ta */
  [72, 76, 79, 84].forEach(n => brass(M(n), t0 + 0.96, 1.25, 0.18)); brass(M(48), t0 + 0.96, 1.25, 0.2);   /* taaa (C-Dur) */
  noise(t0 + 0.96, 1.6, 0.35, "highpass", 5000); noise(t0 + 0.96, 0.35, 0.6, "lowpass", 120);   /* Becken + Pauke */
  setTimeout(() => { try { out.disconnect(); } catch (e) {} }, 3500); }
function certQuiet() {''')
open(dst, "w", encoding="utf-8").write(s)
print("ok", dst)
# Nachtrag (Martin 08:21 «erster Kartenflug nach wie vor alles eingeblendet»): Windrose beim ersten Flug jedes Laufs (Welle ≤ 1) aus – unabhängig von Sternen
s = open(dst, encoding="utf-8").read()
rep('if (m !== "browse" && S && (S.wave | 0) <= 1 && Object.values(starsAll()).reduce((a, b) => a + (+b || 0), 0) === 0) ov.classList.add("firstFly");',
    'if (m !== "browse" && S && S.started && (S.wave | 0) <= 1) ov.classList.add("firstFly");')
open(dst, "w", encoding="utf-8").write(s)
print("ok2")
