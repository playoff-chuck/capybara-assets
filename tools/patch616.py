#!/usr/bin/env python3
# V616 (Martin 11.11. 12:43/12:44): In der RuStore-App (startet capybarasquad.ru/?src=rustore, Paket ru.capybarasquad.game)
# keine Sprachwahl am Anfang und kein Sprachmenü in den Einstellungen – immer Russisch. Merker capy-rustore=1 bleibt.
import sys, os
site = sys.argv[1]; p = os.path.join(site, "index.html"); s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V615";', 'const GAME_VER = "V616";')
rep('(function () { try { const q = new URLSearchParams(location.search), l = q.get("lang"); if (l && LANGS[l]) { localStorage.setItem("capy-lang", l); }',
    '(function () { try { const q = new URLSearchParams(location.search), l = q.get("lang"); if (l && LANGS[l]) { localStorage.setItem("capy-lang", l); }\n'
    '    try { if (q.get("src") === "rustore" || /^android-app:\\/\\/ru\\.capybarasquad\\.game/.test(document.referrer || "")) localStorage.setItem("capy-rustore", "1");   /* V616: RuStore-App = nur Russisch */\n'
    '      if (localStorage.getItem("capy-rustore") === "1") { localStorage.setItem("capy-lang", "ru"); document.documentElement.classList.add("rustore"); } } catch (e) {}')
rep('#ovSettings .setLangBox{', 'html.rustore #ovSettings .setLangBox{display:none!important}\n#ovSettings .setLangBox{')
open(p, "w", encoding="utf-8").write(s)
print("ok V616")
