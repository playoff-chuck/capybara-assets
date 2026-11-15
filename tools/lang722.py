# V722: Texte Teilen-Bilder. Aufruf: python3 tools/lang722.py site/lang
import sys, json, os
d0 = sys.argv[1]
NEW = {  # key: (ru, de, es, pt)
 "PLACE # OF #": ("МЕСТО # ИЗ #", "ORT # VON #", "LUGAR # DE #", "LUGAR # DE #"),
 "BEST WAVE #": ("ЛУЧШАЯ ВОЛНА #", "BESTE WELLE #", "MEJOR OLEADA #", "MELHOR ONDA #"),
 "JOIN MY SQUAD": ("ВСТУПАЙ В МОЙ ОТРЯД", "KOMM IN MEINE TRUPPE", "ÚNETE A MI ESCUADRÓN", "ENTRE NO MEU ESQUADRÃO"),
 "free Ten-ton drop for you": ("Десятитонка в подарок", "Zehntonner gratis für dich", "un Diez Toneladas gratis para ti", "um Dez Toneladas grátis para você"),
}
for i, lg in enumerate(["ru", "de", "es", "pt", "en"]):
    p = os.path.join(d0, lg + ".json"); d = json.load(open(p, encoding="utf-8")); n = 0
    for k, v in NEW.items():
        if k not in d: d[k] = k if lg == "en" else v[i]; n += 1
    open(p, "w", encoding="utf8").write(json.dumps(d, ensure_ascii=False, indent=0) + "\n"); print(lg, "+", n)
