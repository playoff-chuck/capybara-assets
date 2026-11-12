# V685 (Martin 12.11. 19:42): Ortswechsel – Streifen auf Schwarz 1 s länger (Streifen jetzt 1,5–7,0 s), alles danach 1 s später.
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf8").read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:70], c); s = s.replace(a, b)
rep('at(6000, () => { end && end(); });   /* 6,0–6,7 s Streifen blenden zu Schwarz aus */\n      at(6800, () => {', 'at(7000, () => { end && end(); });   /* V685: 7,0–7,7 s Streifen blenden zu Schwarz aus */\n      at(7800, () => {')
rep('/* 6,8–7,9 s Karte blendet aus dem Schwarz ein */\n      at(8000, () => {', '/* 7,8–8,9 s Karte blendet aus dem Schwarz ein */\n      at(9000, () => {')
rep('/* 8,0–10,6 s Flug */\n      at(9100, whoosh);\n      at(10600, () => {', '/* 9,0–11,6 s Flug */\n      at(10100, whoosh);\n      at(11600, () => {')
rep('/* 10,6–11,6 s Landung */\n      at(11600, () => ov.classList.add("fadeOut", "q"));   /* 11,6–12,2 s Karte blendet nach Schwarz aus */\n      at(12250, () => {', '/* 11,6–12,6 s Landung */\n      at(12600, () => ov.classList.add("fadeOut", "q"));   /* 12,6–13,2 s Karte blendet nach Schwarz aus */\n      at(13250, () => {')
rep('const GAME_VER = "V684"', 'const GAME_VER = "V685"')
open(dst, "w", encoding="utf8").write(s); print("ok", len(s))
