#!/usr/bin/env python3
"""V532 (Martin 09.11. 20:47): Support-Info – Chrome meldet im User-Agent immer «Android 10» (eingefroren);
echte Android-Version aus userAgentData.platformVersion nehmen, wenn verfügbar.
Aufruf: python3 tools/patch532.py site/index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V531";', 'const GAME_VER = "V532";')
rep('  const br = (m = /SamsungBrowser', '  if (DEVX.osv && /^Android/.test(os)) os = "Android " + String(DEVX.osv).split(".")[0];   /* V532 */\n  const br = (m = /SamsungBrowser')
open(p, "w", encoding="utf-8").write(s); print("ok V532")
