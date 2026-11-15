# V720: Text Karte Nuts-Fortschritt. Aufruf: python3 tools/lang720.py site/lang
import sys, json, os
d0 = sys.argv[1]
NEW = {"☠ Nuts # / # levels done": {"en": "☠ Nuts # / # levels done", "ru": "☠ Аномалия: пройдено # из # уровней", "de": "☠ Nuts: # / # Level geschafft", "es": "☠ Nuts: # / # niveles superados", "pt": "☠ Nuts: # / # níveis concluídos"}}
for lg in ["en", "ru", "de", "es", "pt"]:
    p = os.path.join(d0, lg + ".json"); d = json.load(open(p, encoding="utf-8")); n = 0
    for k, v in NEW.items():
        if k not in d: d[k] = v[lg]; n += 1
    open(p, "w", encoding="utf8").write(json.dumps(d, ensure_ascii=False, indent=0) + "\n"); print(lg, "+", n)
