#!/usr/bin/env python3
# V632 (Martin 11.11. 15:54/15:57, Screenshot Blau-Sprechblase): Bei jeder Sprechblase mit Stimme wurden alle Spielgeräusche auf 10 % gesenkt
# (sfxBus-Ducking während der Stimme) – wirkte wie «Ton wird leiser». Jetzt keine Absenkung mehr bei Sprechblasen.
import sys, os
site = sys.argv[1]; p = os.path.join(site, "index.html"); s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V631";', 'const GAME_VER = "V632";')
rep('sfxBus.gain.cancelScheduledValues(t); sfxBus.gain.setValueAtTime(sfxBus.gain.value, t); sfxBus.gain.linearRampToValueAtTime(0.1, t + 0.05); sfxBus.gain.setValueAtTime(0.1, t + dur); sfxBus.gain.linearRampToValueAtTime(1, t + dur + 0.35);',
    'sfxBus.gain.cancelScheduledValues(t); sfxBus.gain.setValueAtTime(1, t);   /* V632: Sprechblasen senken die Spielgeräusche nicht mehr */')
open(p, "w", encoding="utf-8").write(s)
print("ok V632")
