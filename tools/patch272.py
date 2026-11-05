"""V272 (Martin 05.11. 15:43): Kill-Meldungen (First splat, Ten down, Splat spree, Super squish, Splatastic, je 50 Splats)
zählen jetzt die wirklich besiegten Monster (eigener Zähler realK) – Erschlagen mit einem Stein zählt dafür 1, nicht 5.
Die 5 Punkte fürs Erschlagen bleiben für Medaillen/Punkte. Keine Stufe fällt mehr aus."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V271";', 'const GAME_VER = "V272";')
rep('''function killMilestones(m) {
  if (S.kills === 1) praise("FIRST SPLAT", 1, "First splat!");
  else if (S.kills === 10) praise("TEN DOWN", 1, false);
  else if (S.kills === 25) praise("SPLAT SPREE", 2, false);
  else if (S.kills === 50) praise("SUPER SQUISH!", 3, false);
  else if (S.kills === 100) praise("SPLATASTIC!", 4, "Splatastic!");
  else if (S.kills % 50 === 0) praise(`${S.kills} SPLATS`, 3, false);''', '''function killMilestones(m) {
  const K = S.realK = (S.realK || 0) + 1;   // V272: echte besiegte Monster
  if (K === 1) praise("FIRST SPLAT", 1, "First splat!");
  else if (K === 10) praise("TEN DOWN", 1, false);
  else if (K === 25) praise("SPLAT SPREE", 2, false);
  else if (K === 50) praise("SUPER SQUISH!", 3, false);
  else if (K === 100) praise("SPLATASTIC!", 4, "Splatastic!");
  else if (K % 50 === 0) praise(`${K} SPLATS`, 3, false);''')
rep('["incNext", "statNext", "statSeen",', '["realK", "incNext", "statNext", "statSeen",')
open(dst, 'w', encoding='utf-8').write(s); print('ok')
