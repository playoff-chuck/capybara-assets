"""V329 (Martin 06.11. 22:28 «Sprüche ok»): Lob-Wörter nach Leistung gestaffelt, nie dasselbe Wort zweimal hintereinander.
1 Linie: Nice! · Smooth! · Good job, partner! (max. 1 Wort je 6 s)
2 Linien: Great! · Awesome! · Nailed it!
3 Linien: Fantastic! · Brilliant! · Superb!
4 Linien: Splatastic! · Incredible! · Phenomenal!
Combo: Legendary! · Unstoppable! · Flawless!"""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V328";', 'const GAME_VER = "V329";')
rep('''  if (c && cr) praise("COMBO!", 3, ["Combo! Incredible!", "Hell yeah!", "Boom shakalaka!"][Math.floor(Math.random() * 3)]);
  else if (c >= 4) praise("FULL SALVO!", 4, ["Spectacular!", "Phenomenal!", "Magnificent!", "Unbelievable!", "Boom shakalaka!"][Math.floor(Math.random() * 5)]);
  else if (c === 3) { const w = ["Amazing!", "Fantastic!", "Outstanding!", "Brilliant!", "Incredible!"][Math.floor(Math.random() * 5)]; praise(w.toUpperCase(), 3, w); }
  else if (c === 2) { const w = ["Great!", "Awesome!", "Terrific!", "Superb!"][Math.floor(Math.random() * 4)]; praise(w.toUpperCase(), 2, w); }
  else if (c === 1 && ++S.lineStreak >= 3) { S.lineStreak = 0; praise("NICE!", 1); }
  else if (c === 1 && Math.random() < 0.6) setTimeout(() => SFX.say(["Yes!", "Sweet!", "Wow!", "Nice!", "Smooth!", "Nailed it!", "Awesome!"][Math.floor(Math.random() * 7)]), 350);''',
'''  if (c && cr) praise("COMBO!", 3, lobWord(5));   /* V329: Lob-Wörter gestaffelt */
  else if (c >= 4) praise("FULL SALVO!", 4, lobWord(4));
  else if (c === 3) { const w = lobWord(3); praise(w.toUpperCase(), 3, w); }
  else if (c === 2) { const w = lobWord(2); praise(w.toUpperCase(), 2, w); }
  else if (c === 1 && ++S.lineStreak >= 3) { S.lineStreak = 0; praise("NICE!", 1, lobWord(1)); }
  else if (c === 1 && Math.random() < 0.6 && performance.now() - (window.__lob1T || -1e9) > 6000) { window.__lob1T = performance.now(); const w = lobWord(1); setTimeout(() => SFX.say(w), 350); }''')
rep('function lockPiece(dropped) {', '''const LOB = { 1: ["Nice!", "Smooth!", "Good job, partner!"], 2: ["Great!", "Awesome!", "Nailed it!"], 3: ["Fantastic!", "Brilliant!", "Superb!"], 4: ["Splatastic!", "Incredible!", "Phenomenal!"], 5: ["Legendary!", "Unstoppable!", "Flawless!"] };
let lobLast = "";
function lobWord(t) { const a = LOB[t].filter(w => w !== lobLast); const w = a[Math.floor(Math.random() * a.length)]; lobLast = w; return w; }
function lockPiece(dropped) {''')
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
