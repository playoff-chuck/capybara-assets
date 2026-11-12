# V678: Notfall-Kiste – W1–10 alle 3 Wellen (W11–30 alle 6), schon bei 7 Reihen unter der Decke, nur 2 s Ruhe, mitschreiben (rescue: open/blocked + Grund)
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf8").read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:60], c); s = s.replace(a, b)
rep('''        if ((S.wave || 0) < (S.rescueW || -99) + 12) return;   /* V422 */ if (stackTopRow() > 5) return;
        if (!window.__playScreen() || performance.now() - (window.__evtLast || -1e9) < 5000) return;''',
'''        if (stackTopRow() > 6) return;   /* V678: schon bei 7 Reihen unter der Decke */
        const rb = why => { try { const k = (S.wave | 0) + ":" + why; if (window.__rescB !== k) { window.__rescB = k; window.__mpush && window.__mpush("rescue", { d: { r: "blocked", why, top: stackTopRow() } }); } } catch (e) {} };   /* V678: mitschreiben */
        if ((S.wave || 0) < (S.rescueW || -99) + ((S.wave || 0) <= 10 ? 3 : 6)) return rb("cooldown");   /* V678: W1–10 alle 3, sonst alle 6 Wellen */
        if (!window.__playScreen()) return rb("screen"); if (performance.now() - (window.__evtLast || -1e9) < 2000) return rb("msg");''')
rep('''        open(true, true); } catch (e) {} }, 400);''', '''        try { window.__mpush && window.__mpush("rescue", { d: { r: "open", top: stackTopRow() } }); } catch (e) {} open(true, true); } catch (e) {} }, 400);''')
rep('    function push(k, extra) { if (q.length > 60) return;', '    window.__mpush = (k, e) => push(k, e);   /* V678 */\n    function push(k, extra) { if (q.length > 60) return;')
rep('uiWinOpen())) return;   /* V409', 'uiWinOpen())) return rb("window");   /* V409')
rep('const GAME_VER = "V677"', 'const GAME_VER = "V678"')
open(dst, "w", encoding="utf8").write(s); print("ok")
