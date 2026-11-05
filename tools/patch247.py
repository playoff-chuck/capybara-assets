"""V247: Monster-Wand W101–150 entschärft (Martin 09:25: Vorschlag umsetzen): Monster-HP W101–110 ×0,75 (vorher 0,85), W111–120 ×0,85 (vorher 0,95), neu W121–150 ×0,90.
Boss-Hack nur noch an ruhigen Stellen (Martin 05.11. 09:24): einmal je Ort, mitten im Ort (Welle 5k+2/5k+3),
nie am Ortsende (Feier + Karte), nie bei Wild Cards (W20/40 …), nie am Kontinentende (Wegweiser + Flug) und nie nach einer Sonderwelle.
Wellen: 8 12 18 22 28 32 38 42 48 52 58 62 68 72 78 82 88 92 98 102 107 112 117 121 127 132 138 142 148 (29 Angebote, vorher 28, davon 23 mit Szene/Fenster kollidiert)."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V246";', 'const GAME_VER = "V247";')
rep('function hkOfferWave(w) { return w >= 6 && w % 20 !== 0 && (w % 6 === 0 || w % 10 === 0); }',
    'const HK_WAVES = new Set([8, 12, 18, 22, 28, 32, 38, 42, 48, 52, 58, 62, 68, 72, 78, 82, 88, 92, 98, 102, 107, 112, 117, 121, 127, 132, 138, 142, 148]);   // V247: nur ruhige Wellen\nfunction hkOfferWave(w) { return HK_WAVES.has(w); }')
rep('w >= 91 && w <= 100 ? 0.75 : w >= 101 && w <= 110 ? 0.85 : w >= 111 && w <= 120 ? 0.95 : 1)', 'w >= 91 && w <= 100 ? 0.75 : w >= 101 && w <= 110 ? 0.75 : w >= 111 && w <= 120 ? 0.85 : w >= 121 && w <= 150 ? 0.90 : 1)')
open(dst, 'w', encoding='utf-8').write(s); print('ok')
