#!/usr/bin/env python3
# V633 (Martin 11.11. 15:59): Trainer-Werbung – Kaufknopf gelb wie das Schild oben; nie «ЗОЛОТА» schreiben, immer die Goldmünze.
# Betrifft Preis-/Mengentexte (Knopf, «nicht genug», Boss-Einsatz, Gewinn/Verlust) in allen Sprachen.
import sys, os, json
site = sys.argv[1]; p = os.path.join(site, "index.html"); s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V632";', 'const GAME_VER = "V633";')
rep('#ovCoachAd .caBuy{font-size:min(27px,3.6vh)!important;padding:1.9vh 10px 1.6vh!important}',
    '#ovCoachAd .caBuy{font-size:min(27px,3.6vh)!important;padding:1.9vh 10px 1.6vh!important}\n#ovCoachAd .caBuy,#ovCoachAd .caBuy:disabled{background:linear-gradient(#ffe066,#ffd23a)!important;color:#3a2414!important;border-color:#3a2414!important}#ovCoachAd .caBuy:disabled{opacity:.75}#ovCoachAd .caBuy img.coinI{height:.9em;vertical-align:-.08em}   /* V633 */')
rep("""<div class="caLock"><i></i><span>3</span></div></div>';""", """<div class="caLock"><i></i><span>3</span></div><p class="caNote">Your training sessions wait in the SHOP – start them there anytime.</p></div>';""")
rep('#ovCoachAd .caBuy,#ovCoachAd .caBuy:disabled{', '#ovCoachAd .caNote{margin:8px 0 0;font:800 13px/1.3 "Baloo 2",sans-serif;color:#2f6f4f;text-align:center}\n#ovCoachAd .caBuy,#ovCoachAd .caBuy:disabled{')
open(p, "w", encoding="utf-8").write(s)
C = ""
T = {
 "en": {"BOOK FOR 99 GOLD": "BOOK FOR 99 " + C, "NOT ENOUGH GOLD YET": "NOT ENOUGH " + C + " YET", "NOT ENOUGH GOLD": "NOT ENOUGH " + C, "HACK FOR GOLD ▶": "HACK FOR " + C + " ▶", "BOSS · GOLD BET": "BOSS · " + C + " BET", "gold lost": C + " lost", "gold profit · # paid out": C + " profit · # paid out", "Not enough gold yet · # gold": "Not enough yet · # " + C, "Your training sessions wait in the SHOP – start them there anytime.": "Your training sessions wait in the SHOP – start them there anytime."},
 "ru": {"BOOK FOR 99 GOLD": "НАНЯТЬ ЗА 99 " + C, "NOT ENOUGH GOLD YET": "ПОКА НЕ ХВАТАЕТ " + C, "NOT ENOUGH GOLD": "НЕ ХВАТАЕТ " + C, "HACK FOR GOLD ▶": "ВЗЛОМ НА " + C + " ▶", "BOSS · GOLD BET": "БОСС · СТАВКА " + C, "gold lost": C + " потеряно", "gold profit · # paid out": "прибыль " + C + " · выплачено #", "Not enough gold yet · # gold": "Пока не хватает · # " + C},
 "de": {"BOOK FOR 99 GOLD": "BUCHEN FÜR 99 " + C, "NOT ENOUGH GOLD YET": "NOCH NICHT GENUG " + C, "NOT ENOUGH GOLD": "NICHT GENUG " + C, "HACK FOR GOLD ▶": "FÜR " + C + " HACKEN ▶", "BOSS · GOLD BET": "BOSS · " + C + "-WETTE", "gold lost": C + " verloren", "gold profit · # paid out": C + "-Gewinn · # ausgezahlt", "Not enough gold yet · # gold": "Noch nicht genug · # " + C},
 "es": {"BOOK FOR 99 GOLD": "CONTRATAR POR 99 " + C, "NOT ENOUGH GOLD YET": "AÚN NO TIENES " + C + " SUFICIENTE", "NOT ENOUGH GOLD": C + " INSUFICIENTE", "HACK FOR GOLD ▶": "HACKEA POR " + C + " ▶", "BOSS · GOLD BET": "JEFE · APUESTA " + C, "gold lost": C + " perdido", "gold profit · # paid out": "beneficio " + C + " · # pagados", "Not enough gold yet · # gold": "Aún no alcanza · # " + C},
 "pt": {"BOOK FOR 99 GOLD": "CONTRATAR POR 99 " + C, "NOT ENOUGH GOLD YET": "AINDA FALTA " + C, "NOT ENOUGH GOLD": C + " INSUFICIENTE", "HACK FOR GOLD ▶": "HACKEIE POR " + C + " ▶", "BOSS · GOLD BET": "CHEFE · APOSTA " + C, "gold lost": C + " perdido", "gold profit · # paid out": "lucro " + C + " · # pagos", "Not enough gold yet · # gold": "Ainda não alcança · # " + C}}
for l, m in T.items():
    q = os.path.join(site, "lang", l + ".json"); d = json.loads(open(q, encoding="utf-8").read()); d.update(m)
    open(q, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=0))
NOTE = "Your training sessions wait in the SHOP – start them there anytime."
NT = {"en": NOTE, "ru": "Тренировки ждут тебя в Магазине – запускай их оттуда в любой момент.", "de": "Deine Trainingsstunden warten im SHOP – starte sie dort jederzeit.",
      "es": "Tus entrenamientos te esperan en la TIENDA: empiézalos allí cuando quieras.", "pt": "Seus treinos esperam na LOJA – comece por lá quando quiser."}
for l, v in NT.items():
    q = os.path.join(site, "lang", l + ".json"); d = json.loads(open(q, encoding="utf-8").read()); d[NOTE] = v
    open(q, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=0))
print("ok V633")
