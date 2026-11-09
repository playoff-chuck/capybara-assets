#!/usr/bin/env python3
"""V525 (Martin 09.11. 17:48): Russisch – Eigennamen und Service-Texte kyrillisch.
Erzeugt tools/lang_src/ru_v525.json aus site/lang/ru.json (Ersetzungen in allen Werten) + neue Namens-Schlüssel.
Spielname «Capybara Squad», Sprachnamen und Rufzeichen der Spieler bleiben unverändert.
Nur auf dem Stand VOR V525 laufen lassen (liest site/lang/ru.json). Aufruf: python3 tools/ru_names525.py
Zusätzlich: Texte des Support-Kastens (V525) in ru/es/pt/de als <lang>_v525b.json."""
import json, re
ru = json.load(open("site/lang/ru.json", encoding="utf-8"))
SUB = [  # (Regex, Ersatz) – in dieser Reihenfolge auf alle Werte
 (r"NUTS-", "НАТС-"), (r"Nuts-", "Натс-"), (r"\bNUTS\b", "НАТС"), (r"\bNuts\b", "Натс"),
 (r"^\+# XP$", "+# ОП"), (r"(\d|#) XP\b", r"\1 опыта"), (r"\bXP\b", "опыт"), (r"\bTNT\b", "ТНТ"), (r"(\d|#) BPM\b", r"\1 уд/мин"),
 (r"\bLucky Supply\b", "«Счастливая посылка»"), (r"\bLUCKY SUPPLY\b", "СЧАСТЛИВАЯ ПОСЫЛКА"),
 (r"жми DROP", "жми «СБРОС»"), (r"Жми DROP", "Жми «СБРОС»"), (r"\bPRO ВОЛНА\b", "ПРО-ВОЛНА"), (r"в Pro\b", "в режиме Про"),
 (r"\bRosie\b", "Рози"), (r"\bBlue\b", "Блу"), (r"\bGORKAZAR\b", "ГОРКАЗАР"),
]
NAMES = {
 "NUTS": "НАТС", "Nuts": "Натс", "DROP": "СБРОС", "PRO": "ПРО", "HP ×#": "ОЗ ×#", "SOS": "SOS", "XL": "XL", "TNT": "ТНТ", "+# XP": "+# ОП", "NUTS #": "НАТС #", "# BPM": "# уд/мин",
 "Rosie": "Рози", "ROSIE": "РОЗИ", "Blue": "Блу", "BLUE": "БЛУ", "Captain Noodle": "Капитан Нудл", "Doc Hazel": "Док Хейзел", "DOC HAZEL": "ДОК ХЕЙЗЕЛ",
 "General Bristle": "Генерал Брисл", "Major Ledger": "Майор Леджер", "Ollie": "Олли", "Coach Ollie": "Тренер Олли",
 "SKULLGROG": "СКАЛЛГРОГ", "GORKAZAR": "ГОРКАЗАР", "FROSTGNAW": "ФРОСТГНОУ", "GRUMBLEFANG": "ГРАМБЛФАНГ",
 "Skullgrog": "Скаллгрог", "Gorkazar": "Горказар", "Frostgnaw": "Фростгноу", "Grumblefang": "Грамблфанг",
 "SNI #": "СНА #", "MIX #": "МИКС #", "TES #": "ТЕС #", "LCK #": "СТОП #", "CHO #": "ЧОМ #", "#T #": "#Т #",
 "Rio lounge": "лаунж Рио", "@ Disco": "@ · диско", "@ Downtempo": "@ · даунтемпо", "@ Groove": "@ · грув", "@ Loop": "@ · луп", "@ Lounge": "@ · лаунж", "@ Ride": "@ · скачка",
 # Musiktitel
 "Airport Bossa": "Босса в аэропорту", "Andes Lounge": "Андский лаунж", "Barracks Lounge": "Лаунж в казарме", "Cartoon Trail": "Мультяшная тропа",
 "Chill Disco Rio": "Расслабленное диско Рио", "Copacabana": "Копакабана", "Copacabana Sunset": "Закат на Копакабане", "Dorian Dust": "Дорийская пыль",
 "Dune Dub": "Даб дюн", "Dune Dub II": "Даб дюн II", "Frozen Retro Groove": "Ледяной ретро-грув", "Funky Disco": "Фанки-диско", "Hi-NRG": "Хай-энерджи",
 "Ice Port Disco": "Диско ледяного порта", "Ipanema": "Ипанема", "Italo Disco": "Итало-диско", "Jungle Downtempo": "Даунтемпо джунглей", "Lagoa": "Лагоа",
 "Lido": "Лидо", "Lounge Disco": "Лаунж-диско", "Miami Nights": "Ночи Майами", "Midtown Shuffle": "Шаффл в центре", "New Wave": "Новая волна",
 "Nu-Disco Riviera": "Ню-диско Ривьера", "Oasis Blues": "Блюз оазиса", "Odd-Phased": "Не в фазе", "Parade Disco": "Парадное диско", "Prairie Loop": "Петля прерий",
 "Pyramid Disco": "Диско пирамид", "Rio Disco": "Диско Рио", "Riviera": "Ривьера", "Rumba Lounge": "Румба-лаунж", "Samba Lounge": "Самба-лаунж",
 "Savanna Groove": "Грув саванны", "Steppe Ride": "Скачка по степи", "Synth-Pop": "Синти-поп", "Synthwave": "Синтвейв", "Taiga Lounge": "Таёжный лаунж",
 "Winter Lantern": "Зимний фонарь", "Frostgnaw Sprint": "Спринт Фростгноу", "Gorkazar Groove": "Грув Горказара", "Grumblefang Stampede": "Топот Грамблфанга",
 "Skullgrog Rush": "Натиск Скаллгрога", 
 "Nuts Detour": "Натс-объезд",
}
out = {}
for k, v in ru.items():
    n = v
    for a, b in SUB: n = re.sub(a, b, n)
    if n != v: out[k] = n
for k, v in NAMES.items():
    if ru.get(k) != v: out[k] = v
json.dump(out, open("tools/lang_src/ru_v525.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print("ru_v525:", len(out), "Einträge")
K = ["SUPPORT INFO", "Version", "Player no.", "Device", "COPY", "COPIED · paste it into your message to us"]
T = {'ru': ["ИНФО ДЛЯ ПОДДЕРЖКИ", "Версия", "Номер игрока", "Устройство", "КОПИРОВАТЬ", "СКОПИРОВАНО · вставь в сообщение нам"],
     'es': ["INFO DE SOPORTE", "Versión", "N.º de jugador", "Dispositivo", "COPIAR", "COPIADO · pégalo en tu mensaje"],
     'pt': ["INFO DE SUPORTE", "Versão", "Nº do jogador", "Aparelho", "COPIAR", "COPIADO · cole na sua mensagem"],
     'de': ["SUPPORT-INFO", "Version", "Spieler-Nr.", "Gerät", "KOPIEREN", "KOPIERT · füge es in deine Nachricht an uns ein"]}
for l, v in T.items(): json.dump(dict(zip(K, v)), open(f"tools/lang_src/{l}_v525b.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
