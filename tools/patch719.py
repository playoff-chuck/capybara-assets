import sys
# V719: Pause-Fenster abgeschnitten/verschoben (Martin 15.11.2026 19:59, Screenshot): Das Spielfeld (#board) schwankt bei schlechter
#  Sicht (.wounded → woundSway mit transform) bzw. hat Filter/Wackel-Animationen. Ein transform/filter macht #board zum Bezugsrahmen
#  für position:fixed → das Pause-Fenster (in #board) wird ins Spielfeld gequetscht, verschoben und rechts abgeschnitten.
#  Lösung: Solange ein Fenster (.overlay) im Spielfeld offen ist, keine Animation/Transform/Filter am Spielfeld.
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (a[:60], c); s = s.replace(a, b)
rep('const GAME_VER = "V718";', 'const GAME_VER = "V719";')
rep('<style id="v718css">', '<style id="v719css">#board:has(.overlay:not([hidden])){animation:none!important;transform:none!important;filter:none!important}</style>\n<style id="v718css">')
open(dst, "w", encoding="utf-8").write(s)
