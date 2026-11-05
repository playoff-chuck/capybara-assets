"""V280 (Martin 16:28): Kanone 45 % leiser – Abschuss (kan) und Einschlag der Kanonenkugel (boom mit Faktor 0,55).
Andere Explosionen (TNT, Ten-ton usw.) bleiben unverändert."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V279";', 'const GAME_VER = "V280";')
rep('kan()    { if (ok("kan", 0.1)) { smp("kan", 0.7, rnd(0.7, 0.85)); kick(230, 60, 0.12, 0.35); noise(0.08, 0.2, "lowpass", 1800, 200); } },',
    'kan()    { if (ok("kan", 0.1)) { smp("kan", 0.385, rnd(0.7, 0.85)); kick(230, 60, 0.12, 0.1925); noise(0.08, 0.11, "lowpass", 1800, 200); } },')
rep('boom()   { if (ok("boom", 0.08)) { smp("boom", 0.7, rnd(0.9, 1.1), 0, 0.3); smp("boomlow", 0.6, rnd(0.9, 1.1)); kick(120, 28, 0.4, 0.5); } },',
    'boom(k)  { const q = typeof k === "number" && k < 1 ? k : 1; if (ok("boom", 0.08)) { smp("boom", 0.7 * q, rnd(0.9, 1.1), 0, 0.3); smp("boomlow", 0.6 * q, rnd(0.9, 1.1)); kick(120, 28, 0.4, 0.5 * q); } },')
rep('s.done = true; snd("boom");', 's.done = true; snd("boom", 0.55);')
open(dst, 'w', encoding='utf-8').write(s)
