"""V307: Checkpoints auch in Checkpoint-Läufen speichern (Martin 06.11. 01:17: «Ich war in Asien. Jetzt in Afrika.
In Level 40 sollte ich starten können»). Bisher: wer ab Checkpoint 30 startete, bekam bei Welle 40, 50 … keinen neuen
Checkpoint (Bedingung !S.cpRun) und landete nach dem Aus wieder bei 30. Rangliste/Bestwert bleiben für Checkpoint-Läufe
weiter ausgenommen."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V306";', 'const GAME_VER = "V307";')
rep('if (S.wave % 10 === 0 && !S.cpRun && !S.testRun && S.wave > (+LS.get("tarnturm-cp-" + MODE) || 0)) {',
    'if (S.wave % 10 === 0 && !S.nuts && !S.testRun && S.wave > (+LS.get("tarnturm-cp-" + MODE) || 0)) {')
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
