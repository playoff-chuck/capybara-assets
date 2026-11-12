# V684 (Martin 12.11. 19:31): Ortswechsel – Streifen 50 % länger (4,5 s). In der ersten Hälfte der Streifen blendet der
# Spielscreen nach Schwarz; danach stehen nur die Streifen auf Schwarz, blenden zu Schwarz aus, und aus dem Schwarz blendet die Karte ein.
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf8").read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:70], c); s = s.replace(a, b)
rep('''      at(1500, () => { end = celebrate(`${oldN.toUpperCase()} CLEARED!`, `Place ${P.g} of 30 done · onward!`, host); });   /* 1,5–4,5 s Streifen + Klänge */
      at(3000, () => { fx("powerup"); setTimeout(() => fx("coin"), 260); });
      at(4500, () => { end && end(); });   /* Streifen weg */
      at(5100, () => blk.classList.add("on"));   /* 5,1–5,9 s Level blendet nach Schwarz aus, keine Musik */
      at(6000, () => {''',
'''      at(1500, () => { end = celebrate(`${oldN.toUpperCase()} CLEARED!`, `Place ${P.g} of 30 done · onward!`, host);   /* V684: 1,5–6,0 s Streifen + Klänge */
        blk.style.transitionDuration = "2.25s"; void blk.offsetWidth; blk.classList.add("on"); });   /* 1,5–3,75 s Spielscreen blendet hinter den Streifen nach Schwarz */
      at(3750, () => { fx("powerup"); setTimeout(() => fx("coin"), 260); });
      at(6000, () => { end && end(); });   /* 6,0–6,7 s Streifen blenden zu Schwarz aus */
      at(6800, () => {''')
rep('''`Waves ${w}–${w + 4}`); });   /* 6,0–7,1 s Karte blendet sanft ein */
      at(7200, () => {''', '''`Waves ${w}–${w + 4}`); });   /* 6,8–7,9 s Karte blendet aus dem Schwarz ein */
      at(8000, () => {''')
rep('hopMe(prev, nxt, 2600); });   /* 7,2–9,8 s Flug */\n      at(8300, whoosh);\n      at(9800, () => {', 'hopMe(prev, nxt, 2600); });   /* 8,0–10,6 s Flug */\n      at(9100, whoosh);\n      at(10600, () => {')
rep('''   /* 9,8–10,8 s Landung */
      at(10800, () => ov.classList.add("fadeOut", "q"));   /* 10,8–11,4 s Karte blendet nach Schwarz aus */
      at(11450, () => { ov.classList.remove("q"); blk.classList.remove("on"); hide(); }); }''',
'''   /* 10,6–11,6 s Landung */
      at(11600, () => ov.classList.add("fadeOut", "q"));   /* 11,6–12,2 s Karte blendet nach Schwarz aus */
      at(12250, () => { ov.classList.remove("q"); blk.style.transitionDuration = ""; blk.classList.remove("on"); hide(); }); }''')
rep('const GAME_VER = "V683"', 'const GAME_VER = "V684"')
open(dst, "w", encoding="utf8").write(s); print("ok", len(s))
