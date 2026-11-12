# V686 (Martin 12.11. 19:53): Ortswechsel – Streifen auf Schwarz noch 1 s länger (Streifen jetzt 1,5–8,0 s), alles danach 1 s später.
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf8").read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:70], c); s = s.replace(a, b)
rep('at(7000, () => { end && end(); });   /* V685: 7,0–7,7 s Streifen blenden zu Schwarz aus */\n      at(7800, () => {', 'at(8000, () => { end && end(); });   /* V686: 8,0–8,7 s Streifen blenden zu Schwarz aus */\n      at(8800, () => {')
rep('/* 7,8–8,9 s Karte blendet aus dem Schwarz ein */\n      at(9000, () => {', '/* 8,8–9,9 s Karte blendet aus dem Schwarz ein */\n      at(10000, () => {')
rep('/* 9,0–11,6 s Flug */\n      at(10100, whoosh);\n      at(11600, () => {', '/* 10,0–12,6 s Flug */\n      at(11100, whoosh);\n      at(12600, () => {')
rep('/* 11,6–12,6 s Landung */\n      at(12600, () => ov.classList.add("fadeOut", "q"));   /* 12,6–13,2 s Karte blendet nach Schwarz aus */\n      at(13250, () => {', '/* 12,6–13,6 s Landung */\n      at(13600, () => ov.classList.add("fadeOut", "q"));   /* 13,6–14,2 s Karte blendet nach Schwarz aus */\n      at(14250, () => {')
rep('const GAME_VER = "V685"', 'const GAME_VER = "V686"')
open(dst, "w", encoding="utf8").write(s); print("ok", len(s))
