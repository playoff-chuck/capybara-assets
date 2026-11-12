#!/usr/bin/env python3
# V668 (Martin 12.11. 15:56): Knacken in der General-Stimme + Flugzeug kaum hörbar.
# Knacken – Ursachen im Funk-Effekt:
#  1) Verzerrer (WaveShaper) sehr stark (Faktor 3,4) und ohne Oversampling → harte Aliasing-Knackser bei Konsonanten.
#     Jetzt Faktor 1,8 mit 4-fach-Oversampling: weiter Funk-Klang, aber weich.
#  2) Bei gestörten Meldungen sprang die Lautstärke für Aussetzer hart auf 2 % und zurück → Klicks. Jetzt 8-ms-Rampen.
#  3) Kurze Rausch-Stöße (20–80 ms) = «Knistern» bei gestörten Meldungen → entfernt. Das gleichmäßige leise Rauschen bleibt.
#  4) Kompressor-Ansprechzeit 2 ms → 6 ms (kein Zerren an Silbenanfängen).
# Flugzeug: Pegel 0,075 → 0,16, Obertöne kräftiger (weiter ohne Knattern und ohne Luftrauschen).
import sys, os
site = sys.argv[1]; p = os.path.join(site, "index.html"); s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V667";', 'const GAME_VER = "V668";')
rep('cu[i] = Math.tanh(x * 3.4) / Math.tanh(3.4); } ws.curve = cu;', 'cu[i] = Math.tanh(x * 1.8) / Math.tanh(1.8); } ws.curve = cu; ws.oversample = "4x";   /* V668: weich, ohne Knacken */')
rep('comp.attack.value = 0.002;', 'comp.attack.value = 0.006;')
rep('if (Math.random() < 0.18 * deg) { dg.gain.setValueAtTime(0.02, at); dg.gain.setValueAtTime(1, at + gap); }',
    'if (Math.random() < 0.18 * deg) { dg.gain.setValueAtTime(1, at); dg.gain.linearRampToValueAtTime(0.05, at + 0.008); dg.gain.setValueAtTime(0.05, at + gap); dg.gain.linearRampToValueAtTime(1, at + gap + 0.008); }   /* V668: Rampen statt Sprung */')
rep('for (let at = 0.05; at < dur; at += 0.06 + Math.random() * (0.25 - 0.05 * deg)) noise(0.02 + Math.random() * 0.06, 0.05 + 0.05 * deg, "bandpass", 1500 + Math.random() * 3200, 800, at, 2.5, 0, voiceOut || master); }',
    '/* V668: kurze Knister-Stöße entfernt */ }')
# Flugzeug
rep('const v = 0.075; g.gain.setValueAtTime(0.0001, T);   /* V664: etwas lauter */', 'const v = 0.16; g.gain.setValueAtTime(0.0001, T);   /* V664/V668: lauter */')
rep('const hs = [[3, 0.55], [4.5, 0.3]].map(', 'const hs = [[3, 0.9], [4.5, 0.6]].map(')
open(p, "w", encoding="utf-8").write(s); print("ok V668")
