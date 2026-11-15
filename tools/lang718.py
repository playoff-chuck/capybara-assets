# V718: Texte Gesten-Info (Info-Knopf). Aufruf: python3 tools/lang718.py site/lang
import sys, json, os
d0 = sys.argv[1]
NEW = {  # key: (ru, de, es, pt)
 "Swipe controls": ("Управление жестами", "Wischsteuerung", "Control por gestos", "Controle por gestos"),
 "Tap": ("Тап", "Tippen", "Toca", "Toque"),
 "Rotate": ("Повернуть", "Drehen", "Girar", "Girar"),
 "Drag left": ("Веди влево", "Nach links ziehen", "Arrastra a la izquierda", "Arraste para a esquerda"),
 "Drag right": ("Веди вправо", "Nach rechts ziehen", "Arrastra a la derecha", "Arraste para a direita"),
 "Move": ("Сдвинуть", "Verschieben", "Mover", "Mover"),
 "Swipe up": ("Свайп вверх", "Nach oben wischen", "Desliza hacia arriba", "Deslize para cima"),
 "Drop": ("Сбросить", "Fallen lassen", "Soltar", "Soltar"),
 "Drag down": ("Веди вниз", "Nach unten ziehen", "Arrastra hacia abajo", "Arraste para baixo"),
 "Lower": ("Опустить", "Senken", "Bajar", "Descer"),
 "Swipe controls are off · turn them on in Settings": ("Жесты выключены · включи их в настройках", "Wischsteuerung ist aus · in den Einstellungen einschalten", "Los gestos están desactivados · actívalos en Ajustes", "Os gestos estão desligados · ative-os nas Configurações"),
 "Tap ⓘ to play on": ("Нажми ⓘ, чтобы играть дальше", "Tippe auf ⓘ, um weiterzuspielen", "Toca ⓘ para seguir jugando", "Toque em ⓘ para continuar"),
}
for i, lg in enumerate(["ru", "de", "es", "pt", "en"]):
    p = os.path.join(d0, lg + ".json"); d = json.load(open(p, encoding="utf-8")); n = 0
    for k, v in NEW.items():
        if k not in d: d[k] = k if lg == "en" else v[i]; n += 1
    open(p, "w", encoding="utf8").write(json.dumps(d, ensure_ascii=False, indent=0) + "\n"); print(lg, "+", n)
