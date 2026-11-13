# V695: fehlende Schlüssel in site/lang/*.json ergänzen (hinten anhängen, vorhandene nie überschreiben). Aufruf: python3 tools/lang695.py site/lang
import sys, json, os
d0 = sys.argv[1]
NEW = {  # Schlüssel: (ru, es, pt)
 "Bug": ("Баг", "Error", "Bug"),
 "Good": ("Хорошо", "Bien", "Bom"),
 "Okay": ("Нормально", "Regular", "Mais ou menos"),
 "Not good": ("Плохо", "Mal", "Ruim"),
 "Full screen": ("Полный экран", "Pantalla completa", "Tela cheia"),
 "# of #": ("# из #", "# de #", "# de #"),
 "GRAPHICS: MINIMAL": ("ГРАФИКА: МИНИМУМ", "GRÁFICOS: MÍNIMOS", "GRÁFICOS: MÍNIMOS"),
 "GRAPHICS: MINIMAL (AUTO)": ("ГРАФИКА: МИНИМУМ (АВТО)", "GRÁFICOS: MÍNIMOS (AUTO)", "GRÁFICOS: MÍNIMOS (AUTO)"),
 "MINIMAL GRAPHICS": ("МИНИМАЛЬНАЯ ГРАФИКА", "GRÁFICOS MÍNIMOS", "GRÁFICOS MÍNIMOS"),
 "Tap me for full graphics": ("Нажми на меня – верну полную графику", "Tócame para gráficos completos", "Toque em mim para gráficos completos"),
 "CHECKPOINT": ("ЧЕКПОИНТ", "PUNTO DE CONTROL", "CHECKPOINT"),
 "wave # saved": ("волна # сохранена", "oleada # guardada", "onda # salva"),
 "BOSS DOWN": ("БОСС ГОТОВ", "JEFE ABATIDO", "CHEFE ABATIDO"),
 "#° PACKAGE": ("ПАКЕТ #°", "PAQUETE #°", "PACOTE #°"),
 "+#° PACKAGE": ("ПАКЕТ +#°", "PAQUETE +#°", "PACOTE +#°"),
 "FROM ROSIE WITH LOVE": ("ОТ РОЗИ С ЛЮБОВЬЮ", "DE ROSIE CON CARIÑO", "DA ROSIE COM CARINHO"),
 "FROM BLUE WITH LOVE": ("ОТ БЛУ С ЛЮБОВЬЮ", "DE BLUE CON CARIÑO", "DO BLUE COM CARINHO"),
 "SALE": ("СКИДКА", "OFERTA", "OFERTA"),
 "WORLD RESTORED": ("МИР ВЫРОВНЕН", "MUNDO RESTAURADO", "MUNDO RESTAURADO"),
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
