#!/usr/bin/env python3
# V608 (Martin 11.11. 10:21 / 10:24 Ortszeit):
# 1) Erster Kartenflug: keine Orts-Tags außer dem ersten Ort, keine NUTS-Tags.
# 2) Erster Ort heißt jetzt «Crash Course» / RU «Ликбез» (Start, wo man das Spiel lernt) – nur Anzeige (Sprachtabellen), Schlüssel bleiben.
# 3) Erster 10T-Airdrop (nach dem Diplom): roter Hinweis «Wird's eng – nimm so eine. Mehr gibt's im Shop.»
# Aufruf: patch608.py <site-Ordner>   (ändert index.html und lang/*.json im Ordner)
import sys, json, os
site = sys.argv[1]
p = os.path.join(site, "index.html")
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V607";', 'const GAME_VER = "V608";')
rep('#ovMap.firstFly .mapRose{display:none!important}',
    '#ovMap.firstFly .mapRose{display:none!important}\n#ovMap.firstFly .mPin em.sub,#ovMap.firstFly .mNuts{display:none!important}   /* V608: erster Flug nur der erste Ort */\n'
    '#adHint{margin:8px 4px 2px;color:#d62828;font-weight:800;font-size:15px;line-height:1.25;text-align:center}')
rep('$a("adName").textContent = D.name; $a("adLine").textContent = D.line;',
    '$a("adName").textContent = D.name; $a("adLine").textContent = D.line;\n'
    '      try { let h = document.getElementById("adHint"); if (!h) { h = document.createElement("div"); h.id = "adHint"; $a("adLine").after(h); } h.textContent = kind === "tut" ? HINT608 : ""; h.hidden = kind !== "tut"; } catch (e) {}   /* V608 */')
rep('    function showDrop(kind, o) {', '    const HINT608 = "Tight spot? Use one of these. You can buy more in the Shop!";\n    function showDrop(kind, o) {')
open(p, "w", encoding="utf-8").write(s)

H = "Tight spot? Use one of these. You can buy more in the Shop!"
NAME = {
 "en": {"@ · River Bank": "@ · Crash Course", "First stop: River Bank": "First stop: Crash Course", "Get # ★ at RIVER BANK": "Get # ★ at CRASH COURSE",
        "Get 5 ★ at RIVER BANK": "Get 5 ★ at CRASH COURSE", "Landed: River Bank": "Landed: Crash Course", "RIVER BANK": "CRASH COURSE", "River Bank": "Crash Course",
        "River Bank · wave #": "Crash Course · wave #", "River Bank · wave 1": "Crash Course · wave 1", "South America · River Bank": "South America · Crash Course", H: H},
 "ru": {"@ · River Bank": "@ · Ликбез", "First stop: River Bank": "Первая остановка: Ликбез", "Get # ★ at RIVER BANK": "Возьми # ★ на ЛИКБЕЗЕ",
        "Landed: River Bank": "Приземлились: Ликбез", "RIVER BANK": "ЛИКБЕЗ", "River Bank": "Ликбез", "River Bank · wave #": "Ликбез · волна #",
        "South America · River Bank": "Южная Америка · Ликбез", H: "Станет туго – сбрось такую. Ещё можно купить в Магазине!"},
 "de": {"@ · River Bank": "@ · Crashkurs", "First stop: River Bank": "Erster Halt: Crashkurs", "Get # ★ at RIVER BANK": "Hol # ★ im CRASHKURS",
        "Landed: River Bank": "Gelandet: Crashkurs", "RIVER BANK": "CRASHKURS", "River Bank": "Crashkurs", "River Bank · wave #": "Crashkurs · Welle #",
        "South America · River Bank": "Südamerika · Crashkurs", H: "Wird's eng? Nimm so einen. Mehr gibt's im Shop!"},
 "es": {"@ · River Bank": "@ · Curso Exprés", "First stop: River Bank": "Primera parada: Curso Exprés", "Get # ★ at RIVER BANK": "Consigue # ★ en CURSO EXPRÉS",
        "Landed: River Bank": "Aterrizaje: Curso Exprés", "RIVER BANK": "CURSO EXPRÉS", "River Bank": "Curso Exprés", "River Bank · wave #": "Curso Exprés · oleada #",
        "South America · River Bank": "Sudamérica · Curso Exprés", H: "¿Apuros? Usa una de estas. ¡Hay más en la Tienda!"},
 "pt": {"@ · River Bank": "@ · Curso Rápido", "First stop: River Bank": "Primeira parada: Curso Rápido", "Get # ★ at RIVER BANK": "Consiga # ★ no CURSO RÁPIDO",
        "Landed: River Bank": "Pousou: Curso Rápido", "RIVER BANK": "CURSO RÁPIDO", "River Bank": "Curso Rápido", "River Bank · wave #": "Curso Rápido · onda #",
        "South America · River Bank": "América do Sul · Curso Rápido", H: "Apertou? Use uma dessas. Tem mais na Loja!"},
}
for l, m in NAME.items():
    q = os.path.join(site, "lang", l + ".json"); d = json.loads(open(q, encoding="utf-8").read())
    d.update(m)
    open(q, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=0))
print("ok V608")
