#!/usr/bin/env python3
# V664 (Martin 12.11. 14:24): Kartenflug (z. B. Südamerika → Afrika) war am Handy stumm.
# Ursache: V649 hat den Motor auf weiche Dreieckswellen bei 58–112 Hz umgestellt (gegen Knattern), V606 das Luftrauschen entfernt.
# So tiefe Töne kann ein Handy-Lautsprecher praktisch nicht wiedergeben → nichts zu hören.
# Lösung: weiche Sinus-Obertöne (3× und 4,5× Grundton ≈ 175–500 Hz) mit Propeller-Pulsieren dazu, etwas lauter; weiterhin kein Knattern.
import sys, os
site = sys.argv[1]; p = os.path.join(site, "index.html"); s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V663";', 'const GAME_VER = "V664";')
rep('''o.frequency.linearRampToValueAtTime(f2 * k, T + D); o.connect(lp); });''',
    '''o.frequency.linearRampToValueAtTime(f2 * k, T + D); o.connect(lp); });
      const hs = [[3, 0.55], [4.5, 0.3]].map(([m, gv]) => { const o = ac.createOscillator(), hg = ac.createGain(); o.type = "sine"; hg.gain.value = gv;   /* V664: hörbare Obertöne für Handy-Lautsprecher */
        o.frequency.setValueAtTime(f0 * m, T); o.frequency.linearRampToValueAtTime(f1 * m, T + up); o.frequency.linearRampToValueAtTime(f1 * 0.94 * m, T + D * 0.55); o.frequency.linearRampToValueAtTime(f2 * m, T + D); o.connect(hg); hg.connect(lp); return o; });''')
rep('const v = 0.05; g.gain.setValueAtTime(0.0001, T);', 'const v = 0.075; g.gain.setValueAtTime(0.0001, T);   /* V664: etwas lauter */')
rep('[o1, o2, lfo, ns].forEach(x => { x.start(T); x.stop(T + D + 0.7); });', '[o1, o2, lfo, ns, ...hs].forEach(x => { x.start(T); x.stop(T + D + 0.7); });')
open(p, "w", encoding="utf-8").write(s); print("ok V664")
