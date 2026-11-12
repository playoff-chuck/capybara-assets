#!/usr/bin/env python3
# V649 «Knackscheck» (Martin 12.11. 09:57: Knacksen beim ersten Flug; ganzes Spiel auf Knackser bei Tonübergängen prüfen):
# 1) Funk-Effekt der Sprachclips: Squelch-Klicks (auf/zu), Knistern, Zischen und Rausch-Stöße entfernt; Träger-Rauschen auf 40 %.
#    Bandpass-Klang (Funkgerät) bleibt.
# 2) Flugzeug: Reifen-Quietscher bei der Landung entfernt, Aufsetz-Wumms weich (30 ms statt 10 ms), Motor Dreieck statt Sägezahn (kein Knattern).
# 3) Effekt-Rauschen weicher Einsatz; Musik-Blenden feiner (15 ms).
# 4) Gewählte Klänge (V648) auch bei laufender Suno-Musik (vorher ersetzte die Percussion-Zuordnung sie).
import sys, os
site = sys.argv[1]; p = os.path.join(site, "index.html"); s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V648";', 'const GAME_VER = "V649";')
# 1) Funk-Effekt ohne Knackser
rep('clean || noise(0.04 + Math.random() * 0.04, 0.16 + Math.random() * 0.06, "bandpass", f1 + 600, f2, 0, 1.5, 0, voiceOut || master);   // Squelch auf',
    '/* V649: Squelch auf entfernt */')
rep('if (hiss) clean || noise(0.12 + Math.random() * 0.12, 0.06 + Math.random() * 0.03, "bandpass", f1, f2, 0.03, 0.6, 0, voiceOut || master);', '')
rep('clean || noise(dur + 0.08, 0.05 + Math.random() * 0.025, "bandpass", f1, f1 * (0.8 + Math.random() * 0.4), 0.06, 0.35 + Math.random() * 0.4, 0, voiceOut || master);   // Träger-Rauschen, driftet',
    'clean || noise(dur + 0.08, 0.02 + Math.random() * 0.01, "bandpass", f1, f1 * (0.8 + Math.random() * 0.4), 0.12, 0.6, 0, voiceOut || master);   // Träger-Rauschen, leise, weich ein/aus (V649)')
rep('clean || noise(dur + 0.08, 0.02 + Math.random() * 0.015, "highpass", 3500, 3500, 0.06, 0.8, 0, voiceOut || master);                                                // Zischen', '')
rep('for (let k = 0, at = 0.15 + Math.random() * 0.25; at < dur; at += 0.18 + Math.random() * 0.45) clean || noise(0.02 + Math.random() * 0.05, 0.04 + Math.random() * 0.05, "bandpass", 1800 + Math.random() * 2800, 900, at, 2, 0, voiceOut || master);   // Knistern', '')
rep('clean || noise(0.05, 0.1, "bandpass", 1800, 3500, dur + 0.1, 1.5, 0, voiceOut || master); clean || osc("square", 1900, 1700, 0.025, 0.02, dur + 0.12, { dest: voiceOut || master });   // Squelch zu', '/* V649: Squelch zu entfernt */')
rep('if (hiss) clean || noise(0.14, 0.035, "bandpass", 2400, 1600, dur + 0.14, 0.6, 0, voiceOut || master);', '')
# 2) Flugzeug
rep('o1.type = "sawtooth"; o2.type = "sawtooth";', 'o1.type = "triangle"; o2.type = "triangle";   /* V649: kein Knattern */')
rep('[0, 0.13].forEach((dt, i) => { const s2 = ac.createBufferSource()', '[].forEach((dt, i) => { const s2 = ac.createBufferSource()')   # V649: keine Reifen-Quietscher
rep('tg.gain.exponentialRampToValueAtTime(0.22, td + 0.01);', 'tg.gain.exponentialRampToValueAtTime(0.14, td + 0.03);')

# 3) Effekt-Rauschen (noise) setzte mit voller Lautstärke ein → 4 ms weicher Einsatz
rep('    g.gain.setValueAtTime(v, t); g.gain.exponentialRampToValueAtTime(0.0001, t + dur);\n    src.connect(f); f.connect(g); out(g, wet, dest); src.start(t, Math.random() * 0.5); src.stop(t + dur + 0.02);',
    '    g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(v, t + Math.min(0.004, dur * 0.2)); g.gain.exponentialRampToValueAtTime(0.0001, t + dur);   /* V649: kein Knack-Einsatz */\n    src.connect(f); f.connect(g); out(g, wet, dest); src.start(t, Math.random() * 0.5); src.stop(t + dur + 0.02);')
# 4) Musik-Blenden: Lautstärke in 15-ms-Schritten statt 50 ms (kein «Treppen-Knistern» beim Ein-/Ausblenden)
rep('n = Math.max(1, Math.round(sec * 20)); let i = 0;\n  tpFadeT = setInterval(() => { i++; try { a.volume = Math.max(0, Math.min(1, from + (target - from) * i / n)); } catch (e) {} if (i >= n) { clearInterval(tpFadeT); tpFadeT = null; } }, 50); }',
    'n = Math.max(1, Math.round(sec * 66)); let i = 0;\n  tpFadeT = setInterval(() => { i++; try { a.volume = Math.max(0, Math.min(1, from + (target - from) * i / n)); } catch (e) {} if (i >= n) { clearInterval(tpFadeT); tpFadeT = null; } }, 15); }   /* V649: feinere Blende */')

# 5) Gewählte Klänge (V648) gelten auch, wenn Suno-Musik läuft – die Percussion-Zuordnung (PERC_MAP) übergeht sie nicht mehr
rep('const m = PERC_MAP[n]; if (!m || !TP.key) return play1.call(this, n, ...a);',
    'const m = /^(lock|lines|splat|mg|kan|coin)$/.test(n) ? null : PERC_MAP[n]; if (!m || !TP.key) return play1.call(this, n, ...a);   /* V649: gewählte Klänge immer */')
open(p, "w", encoding="utf-8").write(s)
print("ok V649")
