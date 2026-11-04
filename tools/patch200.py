"""V200: Nach gewonnenem Boss-Hack kein «JACKPOT!/RICH!/GOLD RUSH»-Jingle mehr beim Zurückkehren
(Gold-Meilensteine zählen nur Gold aus dem normalen Spiel); nur noch ein Jubelspruch auf dem Ergebnis."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V199";', 'const GAME_VER = "V200";')
rep('SFX.say(HK.stake >= 200 ? "Jackpot!" : "Nailed it!");',
    'try { const g2 = (S.gold || 0) + (HK.stake || 0) * 2; S.goldMark = Math.max(S.goldMark || 0, ...[500, 1000, 2000, 4000].filter(g => g <= g2)); S.hkGoldQuiet = performance.now() + 15000; } catch (e) {}')
rep('function goldMilestones() {', 'function goldMilestones() {\n  if (S.hkGoldQuiet && performance.now() < S.hkGoldQuiet) { const mk = [500, 1000, 2000, 4000].filter(g => S.gold >= g); if (mk.length) S.goldMark = Math.max(S.goldMark || 0, ...mk); return; }')
open(dst, 'w', encoding='utf-8').write(s); print('ok')
