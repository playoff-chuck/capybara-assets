#!/usr/bin/env python3
# V602 (Martin 11.11. 08:06): Beim App-Start (PWA-Splash) kein helles Quadrat mehr – Manifest-Icons «any» sind jetzt das freigestellte Logo
# (icons/icon-splash-192/512.png, transparent) auf dem dunklen Hintergrund; Home-Icon bleibt das maskierbare. Manifest-Link ?v=601.
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V601";', 'const GAME_VER = "V602";')
rep('manifest.webmanifest?v=536', 'manifest.webmanifest?v=601')
open(dst, "w", encoding="utf-8").write(s)
print("ok", dst)
