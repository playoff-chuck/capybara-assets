"""V294 (Martin 18:12): Boss-Ergebnis ohne «ACCESS DENIED / ACCESS GRANTED»-Schild (passte nicht). Beim Coach-Training bleibt «COACH OLLIE»."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V293";', 'const GAME_VER = "V294";')
rep('$("hkResTag").textContent = win ? "ACCESS GRANTED" : "ACCESS DENIED"; $("hkResTag").classList.toggle("bad", !win);',
    '$("hkResTag").textContent = ""; $("hkResTag").hidden = true; $("hkResTag").classList.toggle("bad", !win);')
rep('$("hkResTag").textContent = "COACH OLLIE"; $("hkResTag").classList.remove("bad");',
    '$("hkResTag").textContent = "COACH OLLIE"; $("hkResTag").hidden = false; $("hkResTag").classList.remove("bad");')
open(dst, 'w', encoding='utf-8').write(s)
