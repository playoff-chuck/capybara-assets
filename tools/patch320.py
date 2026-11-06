"""V320 (Tutorial-Durchlauf 06.11., automatisch als Neuling):
1. Schritt 4 «ARM IT»: der gelbe Pfeil zeigte auf «ALL MG» (224 Gold, mit 100 Gold gesperrt) statt auf den MG-Knopf (30 Gold).
   Jetzt: erster sichtbarer, nicht gesperrter MG-Kaufknopf.
2. Während der Tutorial-Schritte 1–4 fällt der Block nicht von selbst (vorher Stapel voll → «SO CLOSE! TOWER FULL» nach 47 s,
   wenn ein Neuling liest statt tippt; Schritt 1 erledigte sich schon unter der Anflug-Karte). DROP/Links/Rechts/Drehen gehen weiter."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V319";', 'const GAME_VER = "V320";')
rep('''document.querySelector('#sheet [data-buy="mg"]'); return vis(b);''',
    '''[...document.querySelectorAll('#sheet [data-buy="mg"]')].find(x => !x.disabled && vis(x)) || document.querySelector('#sheet [data-buy="mg"]'); return vis(b);   /* V320 */''')
rep('if (TUT.step < 4) { S.waveCD = Math.max(S.waveCD, 6); S.inWave = false; }',
    'if (TUT.step < 4) { S.waveCD = Math.max(S.waveCD, 6); S.inWave = false; S.gravT = 0; }   /* V320: Block wartet im Tutorial */')
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
