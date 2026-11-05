"""V281 (Martin 16:45): Kanone noch einmal −35 %. Der hörbare Abschuss kommt aus der PICK-Ebene (thump 65→34 Hz, 0,85),
V280 hatte nur die ungenutzte kan()-Funktion getroffen. Jetzt: Abschuss 0,85 × 0,55 × 0,65 = 0,304; Einschlag-Faktor 0,55 × 0,65 = 0,3575."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V280";', 'const GAME_VER = "V281";')
rep('kan: k => k.thump(65, 34, 0.26, 0.85, "triangle"),', 'kan: k => k.thump(65, 34, 0.26, 0.304, "triangle"),')
rep('s.done = true; snd("boom", 0.55);', 's.done = true; snd("boom", 0.3575);')
rep('smp("kan", 0.385, rnd(0.7, 0.85)); kick(230, 60, 0.12, 0.1925); noise(0.08, 0.11,', 'smp("kan", 0.25, rnd(0.7, 0.85)); kick(230, 60, 0.12, 0.125); noise(0.08, 0.07,')
open(dst, 'w', encoding='utf-8').write(s)
