# V717: Texte Wischsteuerung. Aufruf: python3 tools/lang717.py site/lang
import sys, json, os
d0 = sys.argv[1]
NEW = {
 "SWIPE CONTROLS: ON": {"en": "SWIPE CONTROLS: ON", "ru": "УПРАВЛЕНИЕ ЖЕСТАМИ: ВКЛ", "de": "WISCHSTEUERUNG: AN", "es": "CONTROL POR GESTOS: SÍ", "pt": "CONTROLE POR GESTOS: LIGADO"},
 "SWIPE CONTROLS: OFF": {"en": "SWIPE CONTROLS: OFF", "ru": "УПРАВЛЕНИЕ ЖЕСТАМИ: ВЫКЛ", "de": "WISCHSTEUERUNG: AUS", "es": "CONTROL POR GESTOS: NO", "pt": "CONTROLE POR GESTOS: DESLIGADO"},
 "DRAG = move · TAP = rotate · SWIPE UP = drop": {"en": "DRAG = move · TAP = rotate · SWIPE UP = drop", "ru": "ВЕДИ = двигать · ТАП = вращать · ВВЕРХ = сброс", "de": "ZIEHEN = bewegen · TIPPEN = drehen · HOCH = fallen", "es": "ARRASTRA = mover · TOCA = girar · ARRIBA = soltar", "pt": "ARRASTE = mover · TOQUE = girar · CIMA = soltar"},
 "SWIPE": {"en": "SWIPE", "ru": "ЖЕСТЫ", "de": "WISCHEN", "es": "GESTOS", "pt": "GESTOS"},
}
for lg in ["en", "ru", "de", "es", "pt"]:
    p = os.path.join(d0, lg + ".json"); d = json.load(open(p, encoding="utf-8"))
    for k, v in NEW.items():
        if k not in d: d[k] = v[lg]
    open(p, "w", encoding="utf8").write(json.dumps(d, ensure_ascii=False, indent=0) + "\n")
