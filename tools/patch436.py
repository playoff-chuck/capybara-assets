#!/usr/bin/env python3
# V436 (/neu-Chat, Befund Video-Analyse W1–60): Boss-Signal-Pille («HACK FOR GOLD ▶ 20») stand sichtbar über der offenen Boss-Hack-Anzeige –
# doppeltes Angebot. Jetzt: solange die Anzeige offen ist, ist die Pille aus; nach dem Schließen kommt sie mit der Restzeit wieder (Uhr steht derweil, hkHold).
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:80])
    s = s.replace(a, b)
rep('const GAME_VER = "V435";', 'const GAME_VER = "V436";')
rep('''  const p = $("hackPill"), on = hkOfferOn();
  if (on) { const left''', '''  const p = $("hackPill"), on = hkOfferOn();
  if (on && S.hackAdOpen) { if (!p.hidden) p.hidden = true; }   /* V436: Pille nicht über der offenen Boss-Hack-Anzeige */
  else if (on) { const left''')
open(dst, "w", encoding="utf-8").write(s)
print("ok")
