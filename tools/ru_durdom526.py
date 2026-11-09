#!/usr/bin/env python3
"""V526 (Martin 09.11. 18:50 «Дурдом!»): Russisch NUTS → ДУРДОМ (statt НАТС), mit passender Grammatik.
Liest site/lang/ru.json (Stand V525), schreibt tools/lang_src/ru_v526.json. Aufruf: python3 tools/ru_durdom526.py"""
import json, re
ru = json.load(open("site/lang/ru.json", encoding="utf-8"))
SUB = [
 ("НАТС-ОБЪЕЗДА", "ОБЪЕЗДА ЧЕРЕЗ ДУРДОМ"), ("НАТС-ОБЪЕЗДЫ", "ОБЪЕЗДЫ ЧЕРЕЗ ДУРДОМ"), ("НАТС-ОБЪЕЗД", "ОБЪЕЗД ЧЕРЕЗ ДУРДОМ"),
 ("Натс-объезде", "объезде через Дурдом"), ("Натс-объезд", "объезд через Дурдом"),
 ("НАТС-РЕКОРД", "РЕКОРД ДУРДОМА"), ("НАТС-БОНУС", "БОНУС ДУРДОМА"), ("Натс-бонус", "Бонус Дурдома"), ("НАТС-УРОВЕНЬ", "УРОВЕНЬ ДУРДОМА"),
 ("Натс-уровня", "уровня Дурдома"), ("Натс-вылазка", "Вылазка в Дурдом"), ("Медаль Натс", "Медаль Дурдома"),
 ("таблицу Натс", "таблицу Дурдома"), ("Таблица Натс", "Таблица Дурдома"), ("ТАБЛИЦА НАТС", "ТАБЛИЦА ДУРДОМА"), ("вылазка в Натс", "вылазка в Дурдом"),
 ("ПРАВИЛА НАТС", "ПРАВИЛА ДУРДОМА"), ("НАТС", "ДУРДОМ"), ("Натс", "Дурдом"),
]
out = {}
for k, v in ru.items():
    n = v
    for a, b in SUB: n = n.replace(a, b)
    if n != v:
        if v[:1].isupper() and n[:1].islower(): n = n[0].upper() + n[1:]
        out[k] = n
json.dump(out, open("tools/lang_src/ru_v526.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print("ru_v526:", len(out))
