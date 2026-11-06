"""V309: Weltkarte (Ortswechsel / Kontinentflug) erst 5 s nach dem letzten Fenster.
Fund aus dem automatischen Testlauf W1–W60 (06.11.): In Welle 20 schloss sich die Wild-Card-Wahl und im selben
Moment ging die Weltkarte auf (Ortswechsel zu Welle 21) – Regel «nie zwei Screens kurz hintereinander» / 5 s Ruhe.
Ursache: Der Wellen-Countdown war beim Wählen schon abgelaufen; der Kartenhaken vor startWave prüfte keine Ruhezeit.
Jetzt: Liegt das letzte Fenster < 5 s zurück, wird der Countdown auf die Restzeit gesetzt und der Wellenstart
(samt Karte) kommt danach von selbst."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)

rep('const GAME_VER = "V308";', 'const GAME_VER = "V309";')
rep('''          if (play) { busy = true; const was = S.paused; S.paused = true; S.mapShow = true;''',
    '''          if (play) { const calm = performance.now() - (window.__evtLast || -1e9); if (calm < 5000) { S.waveCD = Math.max(S.waveCD || 0, (5000 - calm) / 1000 + 0.1); return; }   /* V309: 5 s Ruhe vor der Karte */
            busy = true; const was = S.paused; S.paused = true; S.mapShow = true;''')
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
