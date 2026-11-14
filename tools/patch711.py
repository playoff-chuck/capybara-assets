import sys, os, subprocess
# V711: ES/PT ~300 fehlende Texte, PT-Clips boom/kaboom, «Vibration: off» (tools/lang711.py)
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (a[:60], c); s = s.replace(a, b)
rep('const GAME_VER = "V710";', 'const GAME_VER = "V711";')
open(dst, "w", encoding="utf-8").write(s)
here = os.path.dirname(os.path.abspath(__file__))
subprocess.run([sys.executable, os.path.join(here, "lang711.py"), os.path.join(os.path.dirname(os.path.abspath(dst)), "lang")], check=True)
print("ok")
