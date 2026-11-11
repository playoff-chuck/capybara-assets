#!/usr/bin/env python3
# V621 (Martin 11.11. 13:08): Boss-Tipp 2 neu – nicht «sofort tippen», sondern auf das Timing achten, Gegner beobachten, nur 5 Schüsse.
import sys, os, json
site = sys.argv[1]; p = os.path.join(site, "index.html"); s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V620";', 'const GAME_VER = "V621";')
rep('["2", "TAP RIGHT AWAY", "As soon as it starts, tap your buttons: a lit wire paints a centre cell in your colour."]',
    '["2", "MIND YOUR TIMING", "You only have 5 shots! Watch what your opponent does before you fire."]')
open(p, "w", encoding="utf-8").write(s)
K = ["MIND YOUR TIMING", "You only have 5 shots! Watch what your opponent does before you fire."]
T = {"en": K, "ru": ["СЛЕДИ ЗА ТАЙМИНГОМ", "У тебя всего 5 выстрелов! Смотри, что делает соперник, и только потом стреляй."],
     "de": ["ACHTE AUFS TIMING", "Du hast nur 5 Schüsse! Schau erst, was dein Gegner macht, bevor du feuerst."],
     "es": ["CUIDA EL TIEMPO", "¡Solo tienes 5 disparos! Mira qué hace tu rival antes de disparar."],
     "pt": ["CUIDE DO TIMING", "Você só tem 5 tiros! Veja o que o rival faz antes de atirar."]}
for l, vals in T.items():
    q = os.path.join(site, "lang", l + ".json"); d = json.loads(open(q, encoding="utf-8").read())
    for k, v in zip(K, vals): d[k] = v
    open(q, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=0))
print("ok V621")
