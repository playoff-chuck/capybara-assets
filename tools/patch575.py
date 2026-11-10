#!/usr/bin/env python3
# V575 (Martin 11.11. 00:14): Russisch «Дурдом» → «Аномалия», die vier Orte → Запретная зона, Терра инкогнита,
# Точка невозврата, Зона турбулентности (nur ru.json, tools/lang_src/ru_v575.json).
# Die alten russischen Sprachaufnahmen «Вылазка в Дурдом» / «Медаль Дурдома» werden auf Russisch nicht mehr abgespielt.
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V574";', 'const GAME_VER = "V575";')
rep('  if (typeof SFX !== "undefined" && SFX.say) { const _ssK = SFX.say; SFX.say = function (k) { try { if (TUT.on && !window.__tutKeys.has(k)) return; } catch (e) {} return _ssK.apply(this, arguments); }; }',
    '  if (typeof SFX !== "undefined" && SFX.say) { const _ssK = SFX.say; SFX.say = function (k) { try { if (TUT.on && !window.__tutKeys.has(k)) return; if ((I18N.lang || "") === "ru" && (k === "nutsgo" || k === "nutsmedal")) return; } catch (e) {} return _ssK.apply(this, arguments); }; }   /* V575: alte RU-Aufnahmen sagen noch «Дурдом» */')
open(dst, "w", encoding="utf-8").write(s)
print("ok")
