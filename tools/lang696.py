# V696: Texte für die Infofelder am Wegweiser (hinten anhängen, vorhandene nie überschreiben). Aufruf: python3 tools/lang696.py site/lang
import sys, json, os
d0 = sys.argv[1]
NEW = {  # Schlüssel: (ru, es, pt)
 "☠ NUTS": ("☠ АНОМАЛИЯ", "☠ NUTS", "☠ NUTS"),
 "Waves #–#": ("Волны #–#", "Oleadas #–#", "Ondas #–#"),
 "OUT OF LIVES!": ("ЖИЗНИ КОНЧИЛИСЬ!", "¡SIN VIDAS!", "SEM VIDAS!"),
 "NUTS DETOUR ENDED": ("ОБЪЕЗД ЗАВЕРШЁН", "DESVÍO TERMINADO", "DESVIO ENCERRADO"),
 "All # levels cleared": ("Пройдены все # уровней", "Superaste los # niveles", "Você passou os # níveis"),
 "Detour ended at level #": ("Объезд завершён на уровне #", "Desvío terminado en el nivel #", "Desvio encerrado no nível #"),
 "All # lives lost in level #": ("Все # жизней потеряны на уровне #", "Perdiste las # vidas en el nivel #", "Você perdeu as # vidas no nível #"),
 "best #": ("рекорд #", "récord #", "recorde #"),
 "gold skull!": ("золотой череп!", "¡calavera de oro!", "caveira de ouro!"),
 "silver skull!": ("серебряный череп!", "¡calavera de plata!", "caveira de prata!"),
 "bronze skull!": ("бронзовый череп!", "¡calavera de bronce!", "caveira de bronze!"),
 "# levels, each harder": ("# уровней, каждый сложнее", "# niveles, cada uno más difícil", "# níveis, cada um mais difícil"),
 "# lives": ("# жизней", "# vidas", "# vidas"),
 "Same kit for everyone": ("У всех одинаковый набор", "El mismo equipo para todos", "O mesmo kit para todos"),
 "no shop": ("без магазина", "sin tienda", "sem loja"),
 "Your main run waits here": ("Основная игра подождёт здесь", "Tu partida principal te espera aquí", "Sua partida principal espera aqui"),
 "First try: +# % main score per level (max +# %)": ("Первая попытка: +# % к основному счёту за уровень (макс. +# %)", "Primer intento: +# % a la puntuación principal por nivel (máx. +# %)", "Primeira tentativa: +# % na pontuação principal por nível (máx. +# %)"),
 "Replay: Nuts board and medals only": ("Повтор: только таблица Аномалии и медали", "Repetición: solo tabla Nuts y medallas", "Repetição: só tabela Nuts e medalhas"),
 "Nuts stays open in the pause menu": ("Аномалия останется доступна в меню паузы", "Nuts sigue disponible en el menú de pausa", "Nuts continua disponível no menu de pausa"),
 "# new places": ("# новых мест", "# lugares nuevos", "# lugares novos"),
 "new music": ("новая музыка", "música nueva", "música nova"),
 "tougher monsters": ("монстры сильнее", "monstruos más duros", "monstros mais fortes"),
 "You can take the Nuts detour later from the pause menu.": ("В Аномалию можно свернуть и позже – через меню паузы.", "Puedes hacer el desvío Nuts más tarde desde el menú de pausa.", "Você pode fazer o desvio Nuts depois pelo menu de pausa."),
}
FIX = {"ru": {"NUTS OVER!": "АНОМАЛИЯ ОКОНЧЕНА!"}}   # V696: falsche Übersetzung («пройдена» = geschafft) überschreiben
for i, l in enumerate(["ru", "es", "pt"]):
    p = os.path.join(d0, l + ".json"); d = json.load(open(p, encoding="utf8")); n = 0
    for k, v in NEW.items():
        if k not in d: d[k] = v[i]; n += 1
    for k, v in FIX.get(l, {}).items(): d[k] = v
    open(p, "w", encoding="utf8").write(json.dumps(d, ensure_ascii=False, indent=0) + "\n"); print(l, "+", n)
p = os.path.join(d0, "en.json"); d = json.load(open(p, encoding="utf8")); n = 0
for k in NEW:
    if k not in d: d[k] = k; n += 1
open(p, "w", encoding="utf8").write(json.dumps(d, ensure_ascii=False, indent=0) + "\n"); print("en +", n)
