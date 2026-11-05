"""V291 (Martin 17:34): «TOWERS SOLD · +X GOLD» beim neuen Kontinent meldet der Buchhalter (Major Ledger), nicht der General."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V290";', 'const GAME_VER = "V291";')
rep('sold at full price. The gold is in your account.`, "HQ", 6500);', 'sold at full price. The gold is in your account.`, "GOLD", 6500);')
open(dst, 'w', encoding='utf-8').write(s)
