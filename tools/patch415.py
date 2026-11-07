#!/usr/bin/env python3
# V415 (Martin 07.11. 22:12, Screenshot): Awards-Ansichten (Medals / Hall of fame / Squad) sauber: ein durchgehendes Panel unter der
# Reiterleiste bis über die unteren Knöpfe, dunkel abgedimmter Hintergrund statt halbtransparentem Menü, kein kleines Kärtchen in der Mitte;
# Dev-Leiste und Dev-Knöpfe sind währenddessen ausgeblendet.
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:80])
    s = s.replace(a, b)
rep('const GAME_VER = "V414";', 'const GAME_VER = "V415";')
CSS = """/* V415: Awards-Panels */
body.awOn #devBar,body.awOn .devOnly{display:none!important}
body.awOn #ovHs,body.awOn #ovAlbum,body.awOn #ovSquad{position:fixed!important;inset:0!important;z-index:90!important;display:flex!important;flex-direction:column;align-items:center!important;justify-content:flex-start!important;background:rgba(40,28,16,.62)!important;padding:calc(env(safe-area-inset-top,0px) + 64px) 12px calc(env(safe-area-inset-bottom,0px) + 96px)!important;gap:0!important;border:0!important;box-shadow:none!important;overflow:hidden!important}
body.awOn #ovHs .hsBox,body.awOn #ovAlbum .albBox,body.awOn #ovSquad .albBox{width:min(420px,100%)!important;height:100%!important;max-height:none!important;margin:0!important;overflow-y:auto!important;background:#fff6e6!important;border:3px solid #3a2a1a!important;border-radius:18px!important;box-shadow:0 10px 30px rgba(0,0,0,.45)!important;color:#3a2a1a!important}
body.awOn #ovHs .hsBox{padding:14px 12px 16px!important}
body.awOn #ovHs[hidden],body.awOn #ovAlbum[hidden],body.awOn #ovSquad[hidden]{display:none!important}
</style>"""
rep(".ordHead #ordDur b{color:#ffd84d;font-weight:800}\n</style>", ".ordHead #ordDur b{color:#ffd84d;font-weight:800}\n" + CSS)
open(dst, "w", encoding="utf-8").write(s)
print("ok")
