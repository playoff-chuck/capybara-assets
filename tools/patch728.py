import sys, os, re
# V728 (Martin 16.11.2026, Foto Pause RU): Bestätigungstext auf «Neustart»-Knopf war zu lang («…щё раз, чтобы начат…» abgeschnitten).
# Kürzer in allen Sprachen; Schlüssel bleibt «Tap again to restart», Anzeige EN «Tap again».
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (a[:60], c); s = s.replace(a, b)
rep('const GAME_VER = "V727";', 'const GAME_VER = "V728";')
open(dst, "w", encoding="utf-8").write(s)
L = {"en": ("Tap again to restart", "Tap again"), "ru": ("Нажми ещё раз, чтобы начать заново", "Нажми ещё раз"),
     "de": ("Nochmal tippen für Neustart", "Nochmal tippen"), "es": ("Toca otra vez para reiniciar", "Toca otra vez"),
     "pt": ("Toque de novo para reiniciar", "Toque de novo")}
d = os.path.join(os.path.dirname(dst), "lang")
for k, (a, b) in L.items():
    p = os.path.join(d, k + ".json"); t = open(p, encoding="utf-8").read()
    old = '"Tap again to restart": "%s"' % a; new = '"Tap again to restart": "%s"' % b
    if old in t: t = t.replace(old, new)
    else: assert new in t, (k, "fehlt")
    open(p, "w", encoding="utf-8").write(t)
print("ok V728")
