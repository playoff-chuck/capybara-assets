#!/usr/bin/env python3
"""V459 (Martin 08.11. 16:06/16:07):
- Einstellungen: Fenster scrollt und füllt den Bildschirm besser (INVITE FRIENDS war abgeschnitten); Heldenbilder etwas kleiner.
- Weltkarte: Comic-Rahmen oben UND unten (braunes Band mit heller Kante), Ausblenden darüber/darunter; Kopf, Knöpfe, Windrose liegen darüber.
Nutzung: python3 tools/patch459.py src dst"""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()

def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (c, a[:80])
    s = s.replace(a, b)

rep('const GAME_VER = "V458";', 'const GAME_VER = "V459";')

# Einstellungen
rep('#ovSettings{z-index:65}#ovHs{z-index:65}',
    '#ovSettings{z-index:65;overflow-y:auto!important;justify-content:flex-start!important;padding-top:calc(env(safe-area-inset-top,0px) + 56px)!important;padding-bottom:24px!important}'
    '#ovSettings .joinBox{width:min(380px,100%)!important;max-height:none!important;overflow:visible!important;flex:0 0 auto}'
    '#ovSettings .hpAv{width:84px!important;height:98px!important}'
    '#ovHs{z-index:65}')

# Weltkarte: Rahmen oben + unten
rep('#ovMap .mapVp::after{content:"";position:absolute;left:-6px;right:-6px;bottom:-6px;height:calc(env(safe-area-inset-bottom,0px) + 20px);background:#3a2414;border-top:4px solid #fff7e8;box-shadow:0 -4px 0 #3a2414,0 -10px 18px rgba(0,0,0,.35);border-radius:18px 18px 0 0;pointer-events:none;z-index:4}',
    '#ovMap .mapVp::after{content:"";position:absolute;left:-6px;right:-6px;bottom:-6px;height:calc(env(safe-area-inset-bottom,0px) + 86px);background:linear-gradient(0deg,#3a2414 0,#3a2414 calc(env(safe-area-inset-bottom,0px) + 20px),#fff7e8 calc(env(safe-area-inset-bottom,0px) + 20px),#fff7e8 calc(env(safe-area-inset-bottom,0px) + 24px),rgba(58,36,20,.55) calc(env(safe-area-inset-bottom,0px) + 24px),rgba(58,36,20,0) 100%);pointer-events:none;z-index:4}   /* V459: Rahmen unten + Ausblenden */')
rep('#ovMap .mapVp::before{content:"";position:absolute;left:0;right:0;bottom:calc(env(safe-area-inset-bottom,0px) + 12px);height:70px;background:linear-gradient(180deg,rgba(58,36,20,0),rgba(58,36,20,.5));pointer-events:none;z-index:4}',
    '#ovMap .mapVp::before{content:"";position:absolute;left:-6px;right:-6px;top:-6px;height:calc(env(safe-area-inset-top,0px) + 86px);background:linear-gradient(180deg,#3a2414 0,#3a2414 calc(env(safe-area-inset-top,0px) + 20px),#fff7e8 calc(env(safe-area-inset-top,0px) + 20px),#fff7e8 calc(env(safe-area-inset-top,0px) + 24px),rgba(58,36,20,.55) calc(env(safe-area-inset-top,0px) + 24px),rgba(58,36,20,0) 100%);pointer-events:none;z-index:4}   /* V459: Rahmen oben + Ausblenden */')
rep('#ovMap .mapBar,#ovMap .mapRose,#ovMap .mapReplay{z-index:6}', '#ovMap .mapBar,#ovMap .mapRose,#ovMap .mapReplay,#ovMap .mapTop,#ovMap .mapSkip,#ovMap .mapDest{z-index:6}#ovMap.auto .mapVp::before{display:none}')
rep('#ovMap .mapTop{position:absolute;left:12px;right:12px;top:calc(env(safe-area-inset-top,0px) + 12px);',
    '#ovMap .mapTop{position:absolute;left:12px;right:12px;top:calc(env(safe-area-inset-top,0px) + 14px);')

open(dst, "w", encoding="utf-8").write(s)
print("ok", dst)
