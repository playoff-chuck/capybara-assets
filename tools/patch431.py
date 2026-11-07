#!/usr/bin/env python3
# V431 (/neu-Chat): Hall-of-fame-Titel wie die anderen Panels (MEDAL ALBUM, SQUAD FILE) – <h2> statt alHead/alTag.
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:80])
    s = s.replace(a, b)

rep('const GAME_VER = "V430";', 'const GAME_VER = "V431";')
rep('<div class="alHead"><span class="alTag">HALL OF FAME</span><span></span></div>\n        <div class="hs" id="hsList">',
    '<h2>HALL OF FAME</h2>\n        <div class="hs" id="hsList">')
rep('body.awOn #ovHs .hsBox{padding:14px 12px 16px!important}',
    'body.awOn #ovHs .hsBox{padding:14px 12px 16px!important}#ovHs .hsBox h2{font-family:Bangers,system-ui!important;letter-spacing:1px!important;font-size:30px!important;margin:0 0 2px!important;text-align:center;color:var(--hero,#4fa3ff)!important;-webkit-text-stroke:1px #3a2a1a;text-shadow:none!important}   /* V431: Titel wie albBox */')
open(dst, "w", encoding="utf-8").write(s)
print("ok")
