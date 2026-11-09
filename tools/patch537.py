#!/usr/bin/env python3
"""V537 (Martin 09.11. 21:34 + Antwort «Bild bleibt, dann Blende»):
- Ankunftsbild (Intro und neuer Kontinent): kein Zurückschrumpfen in den Punkt mehr. Das Bild bleibt stehen und
  blendet danach weich (0,8 s) direkt in den Spielscreen über – keine Karte mehr dazwischen.
- Spieler-Nummer (capy-uid) und Admin-Schlüssel überstehen den Speicher-Reset (capy-reset).
- Admin-Knopf auch auf Geräten mit hinterlegtem Admin-Schlüssel (Martins neues Gerät nach Reset).
Aufruf: python3 tools/patch537.py site/index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)

rep('const GAME_VER = "V536";', 'const GAME_VER = "V537";')
rep('rkk!=="tarnturm-dev"&&rkk!=="capy-cloud")', 'rkk!=="tarnturm-dev"&&rkk!=="capy-cloud"&&rkk!=="capy-uid"&&rkk!=="capy-adm")')
rep('function capyMe() { try { return localStorage.getItem("tarnturm-dev") === "1" || capyUid() === "M2HL-KCQH"; } catch (e) { return false; } }',
    'function capyMe() { try { return localStorage.getItem("tarnturm-dev") === "1" || capyUid() === "M2HL-KCQH" || !!localStorage.getItem("capy-adm"); } catch (e) { return false; } }   /* V537: + Admin-Schlüssel */')
# weiches Ausblenden der ganzen Karte samt Ankunftsbild
rep('#ovMap[hidden]{display:none!important}', '#ovMap[hidden]{display:none!important}#ovMap.fadeOut{opacity:0;transition:opacity .8s ease;pointer-events:none}')
rep('ov.hidden = true; mode = null; document.body.classList.remove("mapUp");', 'ov.hidden = true; ov.classList.remove("fadeOut"); mode = null; document.body.classList.remove("mapUp");')
rep('at(10400, () => { try { arr && arr.classList.remove("on"); } catch (e) {} });   /* V536: Öffnen 2,8 s statt 1,4 s */\n      at(12000, hide); }',
    'at(10400, () => ov.classList.add("fadeOut"));   /* V537: Bild bleibt, dann Blende in den Spielscreen (kein Zurückschrumpfen) */\n      at(11200, hide); }')
rep('at(13200 - sk, hide); }   /* V536: +1,4 s für das langsamere Öffnen */',
    'at(13200 - sk, () => ov.classList.add("fadeOut"));   /* V537: Blende statt Schnitt */\n      at(14000 - sk, hide); }')
open(p, "w", encoding="utf-8").write(s); print("ok V537")
