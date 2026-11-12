# V689 (Martin 12.11. 20:24/20:27): Streifen-Musik beim Ortswechsel = Hymne statt Om. Ausschnitt aus Martins Suno-Stück
# «We've Won the Game» (Sekunde 42,2–75,5: der lauteste, vollste Teil, setzt sofort ein). Einblende 0,4 s statt 1,2 s.
# Die Om-Datei (sfx/place_choir.mp3) wird im selben Commit entfernt.
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf8").read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:70], c); s = s.replace(a, b)
rep('a = new Audio("sfx/place_choir.mp3?v=687")', 'a = new Audio("sfx/place_anthem.mp3?v=689")')
rep('(typeof TP_VOL === "function" ? TP_VOL() : 0.4) * 1.15)), 1.2); }', '(typeof TP_VOL === "function" ? TP_VOL() : 0.4) * 1.15)), 0.4); }   /* V689: Hymne setzt fast sofort ein */')
rep('const GAME_VER = "V688"', 'const GAME_VER = "V689"')
open(dst, "w", encoding="utf8").write(s); print("ok", len(s))
