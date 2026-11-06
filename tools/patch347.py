"""V347 (Martin 07.11. 00:09): Unkraut wächst nochmal 30 % schneller (1 Feld je 6,8 s statt 8,85 s).
Test-Welle für Unkraut: W92 (Anfang Nordamerika) statt W90 (Kontinent-Ende mit Feier/Karte) – dort läuft die Welle wirklich 5 Minuten.
Test-Links starten die gewählte Störung in jeder Test-Welle (S.testKind), unabhängig vom normalen Wellenplan."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V346";', 'const GAME_VER = "V347";')
rep('8.85', '6.8', 3)
rep('const sched = k => { const w = S.wave | 0;', 'const sched = k => { const w = S.wave | 0; if (S.testRun && S.testKind === k && w === S.testLongW) return true;   /* V347: Test-Welle */')
rep('S.testLongW = w; S.testLongUntil', 'S.testLongW = w; S.testKind = kind; S.testLongUntil')
rep('["Weeds", "WAVE 90", 90, "weed"]', '["Weeds", "WAVE 92 · TEST", 92, "weed"]')
rep('weed: 90, thief: 100', 'weed: 92, thief: 100')
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
