#!/usr/bin/env python3
# V651 (Martin 12.11. 10:50): Namensfeld in den Einstellungen größer; Erklärungstext einzeilig in schlichter Schrift.
import sys, os
site = sys.argv[1]; p = os.path.join(site, "index.html"); s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V650";', 'const GAME_VER = "V651";')
rep('#ovRate .rBox{width:min(520px,100%)!important}',
    '#ovSettings label[for="setNick"]{display:block;margin:10px 0 0;font:600 13px/1.3 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif!important;letter-spacing:0!important;text-transform:none!important;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;text-align:center;color:#7a5a3e!important}\n'
    '#ovSettings #setNick{box-sizing:border-box!important;width:100%!important;height:56px!important;min-height:56px!important;padding:0 16px!important;font:700 22px/1 "Baloo 2",system-ui,sans-serif!important;border-radius:16px!important;line-height:56px!important}   /* V651 */\n'
    '#ovRate .rBox{width:min(520px,100%)!important}')
rep('<label for="setNick">YOUR PLAYER NAME · made up, never your real name</label>', '<label for="setNick">Your player name · made up, not your real one</label>')
open(p, "w", encoding="utf-8").write(s)
import json
K = "Your player name · made up, not your real one"
TR = {"en": K, "ru": "Твоё имя в игре · выдуманное, не настоящее", "es": "Tu nombre en el juego · inventado, no el real", "pt": "Seu nome no jogo · inventado, não o real"}
for l, v in TR.items():
    q = os.path.join(site, "lang", f"{l}.json"); d = json.load(open(q, encoding="utf-8"))
    if K not in d: d[K] = v
    with open(q, "w", encoding="utf-8") as f: json.dump(d, f, ensure_ascii=False, indent=0)
print("ok V651")
