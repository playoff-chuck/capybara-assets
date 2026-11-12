# V677: Coach-Tipps (Boss-Hack) – Karten und Knopf ~10 % höher, Figur unten verdeckt, unten mehr Luft
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf8").read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:60], c); s = s.replace(a, b)
rep('#ovHkTips .htBot{position:relative;padding:0 12px max(12px,env(safe-area-inset-bottom))}', '#ovHkTips .htBot{position:relative;padding:0 12px calc(max(12px,env(safe-area-inset-bottom)) + max(4vh, 56vh - 80vw))}   /* V677: höher, Figur unten verdeckt */')
rep('const GAME_VER = "V676"', 'const GAME_VER = "V677"')
open(dst, "w", encoding="utf8").write(s); print("ok")
