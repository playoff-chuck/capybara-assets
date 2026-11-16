# V727: neuer Tutorial-Text. Aufruf: python3 tools/lang727.py site/lang
import sys, json, os
d0 = sys.argv[1]
NEW = {"Tap the orange cart button, then PLACE.": ("Жми оранжевую кнопку с тележкой, потом ПОСТАВИТЬ.", "Tippe den orangen Wagen-Knopf, dann SETZEN.", "Toca el botón naranja del carrito y luego COLOCAR.", "Toque no botão laranja do carrinho e depois em COLOCAR.")}
for i, lg in enumerate(["ru", "de", "es", "pt", "en"]):
    p = os.path.join(d0, lg + ".json"); d = json.load(open(p, encoding="utf-8")); n = 0
    for k, v in NEW.items():
        if k not in d: d[k] = k if lg == "en" else v[i]; n += 1
    open(p, "w", encoding="utf8").write(json.dumps(d, ensure_ascii=False, indent=0) + "\n"); print(lg, "+", n)
