#!/usr/bin/env python3
"""V458 – Einstellungen aufgeräumt (Martin 08.11. 16:03 «Design verbessern»):
Namensfeld hell mit brauner Kontur wie alle Karten, Abschnitt «LANGUAGE» mit Überschrift, 5 Flaggen in einer Reihe (gleich groß),
gewählte Sprache rosa umrandet; Abstände vereinheitlicht.
Nutzung: python3 tools/patch458.py src dst"""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()

def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (c, a[:80])
    s = s.replace(a, b)

rep('const GAME_VER = "V457";', 'const GAME_VER = "V458";')
rep('<div class="setLang" id="setLang" aria-label="Language"></div>',
    '<div class="setLangBox"><div class="hpHead">LANGUAGE</div><div class="setLang" id="setLang" aria-label="Language"></div></div>')
rep('#ovSettings .setLang{display:flex;gap:6px;justify-content:center;flex-wrap:wrap;margin-top:8px}#ovSettings .setLang button{min-height:0;height:40px;padding:0 8px;border:3px solid #3a2414;border-radius:12px;background:#fff!important;background-image:none!important;box-shadow:0 2px 0 #3a2414;font-size:20px;line-height:1;letter-spacing:1px;opacity:.55}#ovSettings .setLang button.on{opacity:1;background:#ffe6a8!important;transform:translateY(1px);box-shadow:0 1px 0 #3a2414}',
    '#ovSettings .setLangBox{margin-top:12px;display:grid;gap:6px;justify-items:center}'
    '#ovSettings .setLang{display:grid;grid-template-columns:repeat(5,1fr);gap:6px;width:100%}'
    '#ovSettings .setLang button{min-height:0;height:46px;padding:0 2px;border:3px solid #3a2414!important;border-radius:12px;background:#fff!important;background-image:none!important;box-shadow:0 2px 0 #3a2414!important;display:flex;align-items:center;justify-content:center;opacity:.6;transition:transform .15s,opacity .15s}'
    '#ovSettings .setLang button span{font-size:18px;line-height:1;letter-spacing:-2px;white-space:nowrap;display:block;transform:translateY(1px)}'
    '#ovSettings .setLang button[data-lang=de] span,#ovSettings .setLang button[data-lang=en] span,#ovSettings .setLang button[data-lang=pt] span{font-size:13px;letter-spacing:-3px}'
    '#ovSettings .setLang button.on{opacity:1;border-color:#e86fa3!important;background:#fff0f6!important;transform:scale(1.06);box-shadow:0 3px 0 #3a2414!important}'
    '#ovSettings #setNick{background:#fff!important;color:#3a2414!important;border:3px solid #3a2414!important;border-radius:12px!important;box-shadow:inset 0 2px 0 rgba(58,36,20,.08);font-weight:700}'
    '#ovSettings label[for=setNick]{font-size:10px;letter-spacing:.2em;color:var(--muted);margin-top:10px;display:block}'
    '#ovSettings .setRow{margin-top:10px}#ovSettings .setInv{margin-top:12px}#ovSettings .hpHead,#ovSettings label[for=setNick]{color:#7a5a3c!important;font-weight:800}')

open(dst, "w", encoding="utf-8").write(s)
print("ok", dst)
