"""V359 (Martin 07.11. 02:38): Dieb «blinkt». Ursache: Überblendung zwischen den Bildern machte ihn kurz durchsichtig.
Jetzt liegt das alte Bild voll darunter und das neue blendet darüber ein; beim Gehen (Bild 1↔2) wird hart gewechselt."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V358";', 'const GAME_VER = "V359";')
rep('if (k < 1 && T.prevFi != null && T.prevFi !== P.fi) drawFrame(T.prevFi, 1 - k, P, h);',
    'const walkSwap = T.prevFi != null && T.prevFi <= 1 && P.fi <= 1;   /* V359: kein Durchscheinen */\n'
    '    if (k < 1 && !walkSwap && T.prevFi != null && T.prevFi !== P.fi) drawFrame(T.prevFi, 1, P, h);')
rep('drawFrame(P.fi, k < 1 ? Math.max(k, 0.35) : 1, P, h);', 'drawFrame(P.fi, k < 1 && !walkSwap ? k : 1, P, h);')
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
