#!/usr/bin/env python3
# V654 (Martin 12.11. 11:48–11:51):
# 1) Tutorial «ARM IT»: Wer nach dem Turmbau erst zurück ins Spiel geht und dann den SHOP öffnet, landet direkt beim
#    neuen (unbewaffneten) Turm – MG ist sofort kaufbar (vorher «TAP A TOWER», ging nicht weiter). Gilt auch für Lektion «zweiter Turm».
# 2) Shop: Ist der Turm-Knopf gesperrt, steht der Grund auf dem Knopf («ALL SLOTS USED» / «NO BLOCKS YET») statt grauem «PLACE».
# 3) Diplom EN/ES/PT: blauer Streifen «CAPYBARA ACADEMY» nur über dem blauen Band in der Mitte, nicht über die ganze Breite.
import sys, os, json
site = sys.argv[1]; p = os.path.join(site, "index.html"); s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V653";', 'const GAME_VER = "V654";')
# 1
rep('function openShop() { S.lsay = ((S.lsay || 0) + 1 + Math.floor(Math.random() * 9)) % 10; S.sel = null; S.shop = true;',
    'function openShop() { try { const ar = TUT.on && (TUT_STEPS[TUT.step] || {}).ar; if (ar === "arm" || ar === "tower2") { const T = [...S.towers.values()].filter(t => !t.w.length).pop(); if (T) { openSheet(T); return; } } } catch (e) {}   /* V654: Tutorial – direkt zum unbewaffneten Turm */\n'
    '  S.lsay = ((S.lsay || 0) + 1 + Math.floor(Math.random() * 9)) % 10; S.sel = null; S.shop = true;')
# 2
rep('`Place on a landed block · ${S.towers.size}/${L.towers} built`, "PLACE", full || noBlocks || S.gold < TOWER_COST, "btn-accent")]);',
    '`Place on a landed block · ${S.towers.size}/${L.towers} built`, full ? "ALL SLOTS USED" : noBlocks ? "NO BLOCKS YET" : "PLACE", full || noBlocks || S.gold < TOWER_COST, "btn-accent")]);   /* V654: Grund auf dem Knopf */')
# 3
rep('#tutSum .cert.us .ctPaper .ctRib{position:absolute;left:0;right:0;top:27.6%;',
    '#tutSum .cert.us .ctPaper .ctRib{position:absolute;left:27%;right:27%;top:27.6%;letter-spacing:.12em;white-space:nowrap;/* V654: nur über dem blauen Band */')
open(p, "w", encoding="utf-8").write(s)
TR = {"ALL SLOTS USED": {"en": "ALL SLOTS USED", "ru": "ВСЕ МЕСТА ЗАНЯТЫ", "es": "SIN HUECOS LIBRES", "pt": "SEM VAGAS LIVRES"},
      "NO BLOCKS YET": {"en": "NO BLOCKS YET", "ru": "СНАЧАЛА БЛОКИ", "es": "PRIMERO BLOQUES", "pt": "PRIMEIRO BLOCOS"}}
for l in ("en", "ru", "es", "pt"):
    q = os.path.join(site, "lang", f"{l}.json"); d = json.load(open(q, encoding="utf-8"))
    for k, v in TR.items():
        if k not in d: d[k] = v[l]
    with open(q, "w", encoding="utf-8") as f: json.dump(d, f, ensure_ascii=False, indent=0)
print("ok V654")
