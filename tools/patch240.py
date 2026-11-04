"""V240: Kein schwarzer Leerlauf mehr zwischen Kontinent-Ende und Flug: Nach «NEXT: <Kontinent>» am Wegweiser
(und nach der Rückkehr aus dem Nuts-Abstecher) lief der normale Wellen-Countdown noch Sekunden auf dem dunklen
Nachtfeld von Welle 30. Jetzt startet die Kontinent-Feier mit Flug sofort (bzw. nach 1,2 s für «Back on the main road»)."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V239";', 'const GAME_VER = "V240";')
rep('S.nutsAsk = { ...(S.nutsAsk || {}), [c]: 1 }; closeSign(); toast(`NUTS DETOUR · any time later from the pause menu`, "HQ", 2400); });',
    'S.nutsAsk = { ...(S.nutsAsk || {}), [c]: 1 }; closeSign(); toast(`NUTS DETOUR · any time later from the pause menu`, "HQ", 2400); if (S && !S.inWave) S.waveCD = Math.min(S.waveCD || 0, 0.3); });')
rep('  saveGame(); nzBadgeSync(); lvLabel();\n  setTimeout(() => { SFX.say("nutsback");',
    '  saveGame(); nzBadgeSync(); lvLabel(); if (S && !S.inWave) S.waveCD = Math.min(S.waveCD || 0, 1.2);\n  setTimeout(() => { SFX.say("nutsback");')
open(dst, 'w', encoding='utf-8').write(s); print('ok')
