import sys
# V725 (Prüfung V724 EN/360): Karten-Knopf «REACHED … · MAP» – letzter Buchstabe der schrägen Schrift wurde abgeschnitten.
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (a[:60], c); s = s.replace(a, b)
rep('const GAME_VER = "V724";', 'const GAME_VER = "V725";')
rep('#btnOMap span{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}',
    '#btnOMap span{white-space:nowrap;overflow:hidden;text-overflow:ellipsis;padding-right:.22em}')
open(dst, "w", encoding="utf-8").write(s)
print("ok V725")
