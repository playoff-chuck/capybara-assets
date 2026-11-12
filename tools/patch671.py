# V671: Flugzeug-Geräusch über der Karte wie vor V649 (Sägezahn, Reifenquietschen, Lautstärke 0,05, ohne V664-Obertöne)
import sys, subprocess
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf8").read()
o = subprocess.check_output(["git", "show", "82f663b^:site/index.html"]).decode("utf8")
A, Z = '  try { window.__planeSnd = (ms, fromOff) => {', 'console.error("planeSnd", e); }'
def blk(t):
    assert t.count(A) == 1, "A"
    a = t.index(A); b = t.index(Z, a) + len(Z); return t[a:b]
nb, ob = blk(s), blk(o)
assert "sawtooth" in ob and "triangle" in nb
s = s.replace(nb, ob)
assert s.count('const GAME_VER = "V670"') == 1
s = s.replace('const GAME_VER = "V670"', 'const GAME_VER = "V671"')
open(dst, "w", encoding="utf8").write(s); print("ok")
