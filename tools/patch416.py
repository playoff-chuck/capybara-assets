#!/usr/bin/env python3
# V416 (Martin 07.11. 22:15): Knopf «WORLD / MY CONTINENT» auf der Karte entfernt (nicht nötig; Weltansicht geht weiter per Zoom/Wischen).
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:80])
    s = s.replace(a, b)
rep('const GAME_VER = "V415";', 'const GAME_VER = "V416";')
rep("body.awOn #ovHs[hidden],body.awOn #ovAlbum[hidden],body.awOn #ovSquad[hidden]{display:none!important}\n</style>",
    "body.awOn #ovHs[hidden],body.awOn #ovAlbum[hidden],body.awOn #ovSquad[hidden]{display:none!important}\n#ovMap .mapBar .mapWorldBtn{display:none!important}   /* V416 */\n</style>")
open(dst, "w", encoding="utf-8").write(s)
print("ok")
