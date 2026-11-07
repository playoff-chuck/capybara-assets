#!/usr/bin/env python3
# V433 (/neu-Chat, Martin 08.11.: «manchmal knackt es»): Klick-Schutz im Audio.
# Analyse aller 245 Clips: ~60 Sprachclips beginnen hart (erster Sample bis 0,2), einige Samples (move, build2, sell, nom) sind übersteuert.
# Code-seitig: (1) Sprachclips mit 10 ms Ein- und 25 ms Ausblende statt hartem Start/Stop; ein unterbrochener Spruch wird 25 ms ausgeblendet statt sofort gestoppt.
# (2) Samples (smp) mit 3 ms Einblende und 6 ms Ausblende am Ende (kein DC-Sprung mehr beim Start/Ende).
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:80])
    s = s.replace(a, b)

rep('const GAME_VER = "V432";', 'const GAME_VER = "V433";')
# (2) Samples
rep('''    src.buffer = list[Math.random() * list.length | 0]; src.playbackRate.value = rate; g.gain.value = v;
    src.connect(g); out(g, wet, dest); src.start(t); return true;''',
'''    src.buffer = list[Math.random() * list.length | 0]; src.playbackRate.value = rate;
    { const d = src.buffer.duration / Math.max(0.05, rate); g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(v, t + 0.003);   /* V433: Klick-Schutz */
      if (d > 0.02) { g.gain.setValueAtTime(v, t + d - 0.006); g.gain.linearRampToValueAtTime(0, t + d); } }
    src.connect(g); out(g, wet, dest); src.start(t); return true;''')
# (1) Stimme: sanft unterbrechen
rep('''    if (curVoice) { try { curVoice.stop(); } catch (e) {} curVoice = null; }''',
'''    if (curVoice) { try { const cv = curVoice, n = ac.currentTime; if (cv.__g) { cv.__g.gain.cancelScheduledValues(n); cv.__g.gain.setValueAtTime(cv.__g.gain.value, n); cv.__g.gain.linearRampToValueAtTime(0, n + 0.025); cv.stop(n + 0.03); } else cv.stop(); } catch (e) {} curVoice = null; }   /* V433: ausblenden statt hart stoppen */''')
# (1) Stimme: Ein-/Ausblende
rep('''      g.gain.value = 0.324 * [1, 0.72, 0.42, 0.14][Math.min(3, deg)]; src.connect(hp);''',
'''      g.gain.value = 0.324 * [1, 0.72, 0.42, 0.14][Math.min(3, deg)]; src.connect(hp); src.__g = g;''')
rep('''      src.start(t0); curVoice = src; src.__rb = /^rb_/.test(String(text));''',
'''      { const gv = g.gain.value; g.gain.setValueAtTime(0, t0); g.gain.linearRampToValueAtTime(gv, t0 + 0.01); g.gain.setValueAtTime(gv, t0 + dur - 0.025); g.gain.linearRampToValueAtTime(0, t0 + dur); }   /* V433: Klick-Schutz */
      src.start(t0); curVoice = src; src.__rb = /^rb_/.test(String(text));''')
open(dst, "w", encoding="utf-8").write(s)
print("ok")
