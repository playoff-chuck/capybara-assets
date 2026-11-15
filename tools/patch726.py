import sys
# V726 (Martin 15.11.2026 22:16): Statistik der .ru-Spieler in Russland (Domain .ru oder russische Zeitzone) auf den RU-Server, sonst Hetzner; Zählung zusammen.
#  Betrifft nur /events und /player (Statistik, Spielerprofil). Bestenliste, Speichern, Feedback bleiben auf Hetzner (eine Rangliste).
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (a[:60], c); s = s.replace(a, b)
rep('const GAME_VER = "V725";', 'const GAME_VER = "V726";')
rep('const API_BASE = /(^|\\.)playcapybarasquad\\.com$/.test(location.hostname) ? "/api" : "https://2-29-147-164.sslip.io/api";',
    'const API_BASE = /(^|\\.)playcapybarasquad\\.com$/.test(location.hostname) ? "/api" : "https://2-29-147-164.sslip.io/api";\n'
    '/* V726: Statistik + Spielerprofil – Spieler in Russland (Seite .ru oder russische Zeitzone) auf den RU-Server, alle anderen Hetzner. Zählung: beide Server zusammen. */\n'
    'const STAT_RU = (() => { if (/(^|\\.)capybarasquad\\.ru$/.test(location.hostname)) return true; try { return /^(Europe\\/(Moscow|Kaliningrad|Samara|Volgograd|Saratov|Ulyanovsk|Astrakhan|Kirov)|Asia\\/(Yekaterinburg|Omsk|Novosibirsk|Barnaul|Tomsk|Novokuznetsk|Krasnoyarsk|Irkutsk|Chita|Yakutsk|Khandyga|Vladivostok|Ust-Nera|Magadan|Sakhalin|Srednekolymsk|Kamchatka|Anadyr))$/.test(Intl.DateTimeFormat().resolvedOptions().timeZone || ""); } catch (e) { return false; } })();\n'
    'const STAT_BASE = STAT_RU ? (/(^|\\.)capybarasquad\\.ru$/.test(location.hostname) ? "/api" : "https://capybarasquad.ru/api") : API_BASE;')
rep('navigator.sendBeacon(API_BASE + "/events", b)', 'navigator.sendBeacon(STAT_BASE + "/events", b)')
rep('fetch(API_BASE + "/events", {', 'fetch(STAT_BASE + "/events", {')
rep('fetch(API_BASE + "/player", {', 'fetch(STAT_BASE + "/player", {')
open(dst, "w", encoding="utf-8").write(s)
print("ok V726")
