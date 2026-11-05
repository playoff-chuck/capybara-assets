"""V251: Afrika (Welle 31–60) leichter (Martin 05.11. 10:37 «beide auf 25 %»): 25 % weniger Monster je Welle,
Monster 25 % langsamer, Steine fallen 25 % langsamer (Fallzeit ×1,333). Nicht im Nuts-Abstecher."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V250";', 'const GAME_VER = "V251";')
rep('const sp = ordv("monSpdMul") * Math.min(G.spMax, G.spBase + G.spGrow * w) *', 'const sp = ordv("monSpdMul") * (!S.nuts && w >= 31 && w <= 60 ? 0.75 : 1) * Math.min(G.spMax, G.spBase + G.spGrow * w) *')
rep('S.toSpawn = Math.min(L.monsters, G.waveBase + G.wavePer * S.wave); S.waveTotal = S.toSpawn;', 'S.toSpawn = Math.max(1, Math.round(Math.min(L.monsters, G.waveBase + G.wavePer * S.wave) * (S.wave >= 31 && S.wave <= 60 ? 0.75 : 1))); S.waveTotal = S.toSpawn;   // V251: Afrika −25 % Monster')
rep('* ordv("gravMul") / (S.wave >= 60 ? 0.7716', '* ordv("gravMul") * (!S.nuts && S.wave >= 31 && S.wave <= 60 ? 1.3333 : 1) / (S.wave >= 60 ? 0.7716')
open(dst, 'w', encoding='utf-8').write(s); print('ok')
