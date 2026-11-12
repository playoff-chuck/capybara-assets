#!/usr/bin/env python3
# V666 (Martin 12.11. 14:31): Ergebnis-Karte nach Game over unten abgeschnitten (Statistik-Zeile halb weg).
# Ursache: #ovOver ist eine Flex-Spalte mit fester Bildschirmhöhe und overflow:hidden. Wenn «NEW RECORD» + Blue-Spruch + Namensfeld
# + 3 Knöpfe zusammen höher sind als der Bildschirm (z. B. 362×782), schrumpft der Browser die Karte – ihr Inhalt wird abgeschnitten.
# Lösung: Teile schrumpfen nie; ist es zu hoch, lässt sich das Fenster scrollen (oben beginnend statt mittig abgeschnitten); auf niedrigen Bildschirmen etwas kompakter.
import sys, os
site = sys.argv[1]; p = os.path.join(site, "index.html"); s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V665";', 'const GAME_VER = "V666";')
rep('#ovOver .hsEntry label{font-size:10px!important;letter-spacing:.1em!important;line-height:1.35!important}\n</style>',
    '''#ovOver .hsEntry label{font-size:10px!important;letter-spacing:.1em!important;line-height:1.35!important}
/* V666: nichts abschneiden – Teile schrumpfen nicht, zu hohes Fenster scrollt */
#ovOver:not([hidden]):not(.won){overflow-y:auto!important;justify-content:safe center!important;-webkit-overflow-scrolling:touch;overscroll-behavior:contain}
#ovOver:not([hidden])>*{flex-shrink:0!important}
@media (max-height:840px){#ovOver .aar{padding:10px 12px 10px!important}#ovOver .aar h2{margin:0 0 6px!important}#ovOver .comfort{margin:4px auto!important;padding:6px 10px!important}#ovOver .comfort img{width:44px!important;height:44px!important}#ovOver .hsScore{margin:4px 0 2px!important}#ovOver .hsScore span{font-size:clamp(36px,12vw,50px)!important}#ovOver .overBtns>button{height:42px!important}}
</style>''')
open(p, "w", encoding="utf-8").write(s); print("ok V666")
