"""V268 (Martin 05.11. 15:19 «B einbauen»): Balancing-Variante B für ≥ 80 % Durchspieler bis Welle 150
(Simulation v6, 4000 Läufe: alle 86 %, Anfänger 70 %, Martin 97 %, gut 95 %, Profi 92 %).
Ab Welle 21 bis 150 (nicht im Nuts-Abstecher): Monster-HP ×0,4 (zusätzlich zu den bisherigen Faktoren),
45 % weniger Monster je Welle, Monster 35 % langsamer, Steine fallen langsamer (Fallzeit ×1,8).
Ersetzt die Afrika-Regel aus V251 (W31–60: −25 % / −25 % / ×1,333)."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V267";', 'const GAME_VER = "V268";')
rep('w >= 121 && w <= 150 ? 0.90 : 1) * baseHp', 'w >= 121 && w <= 150 ? 0.90 : 1) * (!S.nuts && w >= 21 && w <= 150 ? 0.4 : 1) * baseHp')
rep('(!S.nuts && w >= 31 && w <= 60 ? 0.75 : 1)', '(!S.nuts && w >= 21 && w <= 150 ? 0.65 : 1)')
rep('(S.wave >= 31 && S.wave <= 60 ? 0.75 : 1)', '(!S.nuts && S.wave >= 21 && S.wave <= 150 ? 0.55 : 1)')
rep('(!S.nuts && S.wave >= 31 && S.wave <= 60 ? 1.3333 : 1)', '(!S.nuts && S.wave >= 21 && S.wave <= 150 ? 1.8 : 1)')
open(dst, 'w', encoding='utf-8').write(s); print('ok')
