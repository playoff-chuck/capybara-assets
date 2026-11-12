# V674: Waffen ab dem Mischer mit 4 Wellen Abstand – Mischer 9, Sniper 13, Chomper 17, Tesla 21, Frost 31, Lockdown 35; keine 15-s-Abkürzung für gestaute Angebote
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf8").read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:60], c); s = s.replace(a, b)
rep('"unlock": {"mg": 1, "kan": 3, "snipe": 13, "mix": 9, "frost": 11, "ton": 8, "chomp": 17, "tesla": 21, "lock": 25}', '"unlock": {"mg": 1, "kan": 3, "snipe": 13, "mix": 9, "frost": 31, "ton": 8, "chomp": 17, "tesla": 21, "lock": 35}', 3)  # alle 3 Modi
rep('if (!calm() || !(window.__offerOK() || od)) return;', 'if (!calm() || !window.__offerOK()) return;   /* V674: keine 15-s-Abkürzung mehr (od) */')
rep('const GAME_VER = "V673"', 'const GAME_VER = "V674"')
open(dst, "w", encoding="utf8").write(s); print("ok")
