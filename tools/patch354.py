"""V354 (Martin 07.11. 00:46): Dieb ohne Umdrehen, ohne «?»/«!» und ohne Countdown-Zahl. Hält noch etwas früher vor der Gold-Anzeige.
Sagt «Thank you!» genau in dem Moment, in dem er das Gold nimmt, und läuft weiter."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V353";', 'const GAME_VER = "V354";')
rep('else if (ph === "back") { fi = 2; const p = t - 6; sx = p < 0.35 ? Math.cos(Math.PI * ease(p / 0.35)) : p < 0.95 ? -1 : Math.cos(Math.PI * (1 - ease((p - 0.95) / 0.35))); }',
    'else if (ph === "back") { fi = 2; bob = (1 - Math.cos(t * 4)) * 0.6; }')
rep('const mark = P.ph === "back" && t > 6.3 ? "?" : P.ph === "eye" ? "!" : "";', 'const mark = "";')
rep('if (!T.stolen && t < 10) { g.fillStyle = "#ff4a3a";', 'if (false) { g.fillStyle = "#ff4a3a";')
rep('stop = r.left - 84, reach = r.left - 56', 'stop = r.left - 112, reach = r.left - 84')
rep('setTimeout(() => { try { SFX.say("thief_laugh", 1.0, 1.0, 0, 0); } catch (e) {} }, 750);', 'try { SFX.say("thief_laugh", 1.0, 1.0, 0, 0); } catch (e) {}')
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
