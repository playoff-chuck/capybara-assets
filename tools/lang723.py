# V723: Texte «wie weit / weiter ab» beim Tod. Aufruf: python3 tools/lang723.py site/lang
import sys, json, os
d0 = sys.argv[1]
NEW = {  # key: (ru, de, es, pt)
 "YOU REACHED WAVE": ("ТЫ ДОШЁЛ ДО ВОЛНЫ", "DU HAST WELLE ERREICHT", "LLEGASTE A LA OLEADA", "VOCÊ CHEGOU À ONDA"),
 "YOU CONTINUE FROM WAVE": ("ПРОДОЛЖИШЬ С ВОЛНЫ", "WEITER AB WELLE", "SIGUES DESDE LA OLEADA", "CONTINUA DA ONDA"),
 "YOU START AGAIN FROM WAVE": ("НАЧНЁШЬ СНОВА С ВОЛНЫ", "NEUSTART AB WELLE", "EMPIEZAS DE NUEVO EN LA OLEADA", "RECOMEÇA NA ONDA"),
 "▶ CONTINUE FROM WAVE #": ("▶ ДАЛЬШЕ С ВОЛНЫ #", "▶ WEITER AB WELLE #", "▶ SEGUIR DESDE LA OLEADA #", "▶ CONTINUAR DA ONDA #"),
}
for i, lg in enumerate(["ru", "de", "es", "pt", "en"]):
    p = os.path.join(d0, lg + ".json"); d = json.load(open(p, encoding="utf-8")); n = 0
    for k, v in NEW.items():
        if k not in d: d[k] = k if lg == "en" else v[i]; n += 1
    open(p, "w", encoding="utf8").write(json.dumps(d, ensure_ascii=False, indent=0) + "\n"); print(lg, "+", n)
