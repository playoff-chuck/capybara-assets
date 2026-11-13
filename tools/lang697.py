# V697: Texte Cuddle Zombie (hinten anhängen, vorhandene nie überschreiben). Aufruf: python3 tools/lang697.py site/lang
import sys, json, os
d0 = sys.argv[1]
NEW = {  # Schlüssel: (ru, es, pt)
 "Cuddle Zombie": ("Натааа", "Abrazona", "Grudenta"),
 "CUDDLE ZOMBIE": ("НАТААА", "ABRAZONA", "GRUDENTA"),
 "Wants to hug everyone. Hugs a tower for 10 s – it can't shoot. Splat her in time or the tower dissolves.": ("Хочет всех обнять. Обнимает башню 10 с – та не стреляет. Не успел расплющить – башня растворится.", "Quiere abrazar a todos. Abraza una torre 10 s y no dispara. Si no la aplastas a tiempo, la torre se deshace.", "Quer abraçar todo mundo. Abraça uma torre por 10 s e ela não atira. Se não esmagar a tempo, a torre se desfaz."),
 "Hugs a tower for 10 s – it stops shooting. Too slow? The tower dissolves.": ("Обнимает башню 10 с – та молчит. Не успел? Башня растворится.", "Abraza una torre 10 s: deja de disparar. ¿Muy lento? La torre se deshace.", "Abraça uma torre por 10 s: ela para de atirar. Demorou? A torre se desfaz."),
 "Hug # s": ("Объятия # с", "Abrazo # s", "Abraço # s"),
 "HP ×#": ("HP ×#", "PV ×#", "PV ×#"),
 "HUG!": ("ОБНИМАШКИ!", "¡ABRAZO!", "ABRAÇO!"),
 "Tower hugged away": ("Башню заобнимали", "Torre abrazada hasta desaparecer", "Torre abraçada até sumir"),
}
for i, l in enumerate(["ru", "es", "pt"]):
    p = os.path.join(d0, l + ".json"); d = json.load(open(p, encoding="utf8")); n = 0
    for k, v in NEW.items():
        if k not in d: d[k] = v[i]; n += 1
    open(p, "w", encoding="utf8").write(json.dumps(d, ensure_ascii=False, indent=0) + "\n"); print(l, "+", n)
p = os.path.join(d0, "en.json"); d = json.load(open(p, encoding="utf8")); n = 0
for k in NEW:
    if k not in d: d[k] = k; n += 1
open(p, "w", encoding="utf8").write(json.dumps(d, ensure_ascii=False, indent=0) + "\n"); print("en +", n)
