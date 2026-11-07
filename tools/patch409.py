#!/usr/bin/env python3
# V409 (Martin 07.11. 21:48): Rettungs-Lucky-Supply (hoher Stapel ab W30) hat die Wolf-Werbung überdeckt.
# Jetzt wartet der Rettungs-Lucky wie der normale Lucky, solange ein anderes Fenster offen ist (Werbung, Vorstellung, Orders, Duell …).
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:80])
    s = s.replace(a, b)
rep('const GAME_VER = "V408";', 'const GAME_VER = "V409";')
rep('        if (!window.__playScreen() || performance.now() - (window.__evtLast || -1e9) < 5000) return;\n        open(true, true); } catch (e) {} }, 400);',
    '        if (!window.__playScreen() || performance.now() - (window.__evtLast || -1e9) < 5000) return;\n        if (S.adOpen || S.intro || S.drop || S.ordersOpen || S.duel || S.mapShow || S.mapFly || S.signOpen || S.joinOpen || (typeof uiWinOpen === "function" && uiWinOpen())) return;   /* V409: nie über ein offenes Fenster (Wolf-Werbung) */\n        open(true, true); } catch (e) {} }, 400);')
open(dst, "w", encoding="utf-8").write(s)
print("ok")
