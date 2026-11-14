import sys, os, json
# V713: Ergebnis-Screen – Bestenliste unter der Karte in eigener Karte (Martin 14.11.2026 22:35 «bitte ordentlich formatieren»);
#  Karte: fehlende Texte «next stop in # wave», «Landmark», «boss waits here», «−#° PACKAGE»; RU «@ ПРОЙДЕНО!» → «@ – ПРОЙДЕНО!» (Gattung egal);
#  RU «через # волн» → «до следующей остановки: #»; Namensschild in der Sprechblase und Join-Formular-Beschriftungen ≥ 11 px (Megatest C13).
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (a[:60], c); s = s.replace(a, b)
rep('const GAME_VER = "V712";', 'const GAME_VER = "V713";')
rep('</head>', '<style id="v713hs">#ovOver #hsOver{width:100%;max-width:300px;box-sizing:border-box;margin:10px auto 0;padding:8px 12px 10px;background:linear-gradient(180deg,#fff6e4,#ffe7b8);border:3px solid #3a1d10;border-radius:18px;box-shadow:0 5px 0 #3a1d10;font-family:"Baloo 2",system-ui,sans-serif;font-size:14px;color:#3a1d10}\n'
    '#ovOver #hsOver:empty{display:none}\n'
    '#ovOver #hsOver h4{color:#3a1d10!important;font:400 17px/1.1 Bangers,system-ui,sans-serif!important;letter-spacing:.04em!important;margin:4px 0 4px!important;text-align:left}\n'
    '#ovOver #hsOver h4:first-child{font:700 12px/1.3 "Baloo 2",system-ui,sans-serif!important;letter-spacing:.02em!important;color:#8a5a2b!important;margin:0 0 4px!important;padding-bottom:6px;border-bottom:1px dashed #d9c3a0}\n'
    '#ovOver #hsOver .row{grid-template-columns:22px minmax(0,1fr) auto 42px;gap:8px;padding:3px 4px;color:#3a1d10!important;font-weight:600;line-height:1.25;align-items:baseline}\n'
    '#ovOver #hsOver .row span:nth-child(1){color:#8a5a2b;font-weight:800}#ovOver #hsOver .row span:nth-child(3){font-variant-numeric:tabular-nums;font-weight:800}#ovOver #hsOver .row span:last-child{color:#8a5a2b;font-weight:700}\n'
    '#ovOver #hsOver .row.me{background:rgba(255,138,31,.22)!important;border-radius:8px}\n'
    '#buddy .say small{font-size:11px!important}.joinBox label{font-size:11px!important}.joinSmall{font-size:11px!important}.joinBox .alHead{font-size:11px!important}</style>\n</head>')
open(dst, "w", encoding="utf-8").write(s)
L = os.path.join(os.path.dirname(os.path.abspath(dst)), "lang")
ADD = {  # key: ru, es, pt, de
 "next stop in # wave": ("до следующей остановки: #", "próxima parada en # oleada", "próxima parada em # onda", "nächster Halt in # Welle"),
 "Landmark": ("Достопримечательность", "Monumento", "Marco", "Wahrzeichen"),
 "boss waits here": ("здесь ждёт босс", "aquí espera el jefe", "o chefe espera aqui", "hier wartet der Boss"),
 "−#° PACKAGE": ("ПАКЕТ −#°", "PAQUETE −#°", "PACOTE −#°", "PAKET −#°"),
 "#° PACKAGE": (None, None, None, "PAKET #°"), "+#° PACKAGE": (None, None, None, "PAKET +#°"),
}
FIX_RU = {"@ CLEARED!": "@ – ПРОЙДЕНО!", "# CLEARED!": "# – ПРОЙДЕНО!", "next stop in # waves": "до следующей остановки: #"}
for i, l in enumerate(["ru", "es", "pt", "de"]):
    p = os.path.join(L, l + ".json"); d = json.load(open(p, encoding="utf8"))
    for k, v in ADD.items():
        if v[i] and k not in d: d[k] = v[i]
    if l == "ru": d.update(FIX_RU)
    open(p, "w", encoding="utf8").write(json.dumps(d, ensure_ascii=False, indent=0) + "\n")
print("ok")
