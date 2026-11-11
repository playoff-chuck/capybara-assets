#!/usr/bin/env python3
# V630: Kleinkram aus der Übergabe
# 1) «✕ ОТМЕНА» rutscht unter die Meldung oben (z. B. «СНАЙПЕР ГОТОВ · нажми на цель»), statt sie zu verdecken.
# 2) Untertitel beim Aufbruch in die Аномалия («30 levels · no mercy · boss every 10») übersetzt (Teilstücke).
import sys, os, json
site = sys.argv[1]; p = os.path.join(site, "index.html"); s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V629";', 'const GAME_VER = "V630";')
rep('if (bd) { const r = bd.getBoundingClientRect(); b.style.top = Math.max(8, r.top + 8) + "px"; } }',
    'if (bd) { const r = bd.getBoundingClientRect(); b.style.top = Math.max(8, r.top + 56) + "px"; } }   /* V630: unter das Modus-Banner (auf dem Spielfeld gezeichnet) */')
open(p, "w", encoding="utf-8").write(s)
T = {"ru": {"# levels": "# уровней", "no mercy": "без пощады", "boss every #": "босс каждые #"},
     "de": {"# levels": "# Level", "no mercy": "ohne Gnade", "boss every #": "Boss alle #"},
     "es": {"# levels": "# niveles", "no mercy": "sin piedad", "boss every #": "jefe cada #"},
     "pt": {"# levels": "# níveis", "no mercy": "sem piedade", "boss every #": "chefe a cada #"}}
for l, m in T.items():
    q = os.path.join(site, "lang", l + ".json"); d = json.loads(open(q, encoding="utf-8").read())
    for k, v in m.items(): d.setdefault(k, v)
    open(q, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=0))
print("ok V630")
