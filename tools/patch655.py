#!/usr/bin/env python3
# V655 (Martin 12.11. 11:55): KEINE Begrenzung der Turmanzahl – nie bewilligt. Gilt für alle Versionen (Web, RU, App).
# limits().towers praktisch unendlich; Anzeige «Reinforcements» nennt keine Turmzahl mehr; Shop ohne «x/y built».
import sys, os, json
site = sys.argv[1]; p = os.path.join(site, "index.html"); s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V654";', 'const GAME_VER = "V655";')
rep('  return { towers: 2 + tier, weapons:', '  return { towers: 1e9, weapons:')   # V655: Türme unbegrenzt
rep('announce("REINFORCEMENTS", `${L.towers} towers · ${L.weapons} weapons per tower · up to ${L.monsters} monsters`',
    'announce("REINFORCEMENTS", `${L.weapons} weapons per tower · up to ${L.monsters} monsters`')
rep('`Place on a landed block · ${S.towers.size}/${L.towers} built`', '`Place on a landed block · ${S.towers.size} built`')
open(p, "w", encoding="utf-8").write(s)
K = "# weapons per tower · up to # monsters"
TR = {"en": K, "ru": "оружия на башню: # · монстров: до #", "es": "# armas por torre · hasta # monstruos", "pt": "# armas por torre · até # monstros"}
for l, v in TR.items():
    q = os.path.join(site, "lang", f"{l}.json"); d = json.load(open(q, encoding="utf-8"))
    if K not in d: d[K] = v
    with open(q, "w", encoding="utf-8") as f: json.dump(d, f, ensure_ascii=False, indent=0)
print("ok V655")
