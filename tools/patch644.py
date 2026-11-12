#!/usr/bin/env python3
# V644 (Martin 12.11. 08:11 «Bilder okay, aufgehellt, passt – für alle umsetzen»), Vorschläge aus «Prüfkriterien Perspektiven (12.11.)»:
# 4.1 Nacht/Abend: Feld nicht mehr fast schwarz (blau/violett, durchscheinend), Nachthimmel heller.
# 4.2 Tag: Ortsbild scheint stärker durchs Feld (Feld-Deckkraft .66/.64 → .30).
# Dazu: die 8 Glühbirnen-Tipps halten das Spiel an (Martin 08:12).
# Monster-Vergrößerung und Anzeige «nächster Stein» kommen separat (Martin 08:14/08:15 will erst Vorschläge sehen).
import sys, os
site = sys.argv[1]; p = os.path.join(site, "index.html"); s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V643";', 'const GAME_VER = "V644";')
# 4.2 Tag
rep('field: "rgba(214,201,160,.66)"', 'field: "rgba(214,201,160,.30)"')
rep('field: "rgba(222,206,160,.64)"', 'field: "rgba(222,206,160,.30)"')
rep('field: "rgba(226,190,135,.66)"', 'field: "rgba(226,190,135,.30)"')
# 4.1 Abend/Nacht
rep('field: "rgba(42,30,40,.84)"', 'field: "rgba(60,46,96,.52)"')
rep('field: "rgba(24,32,22,.88)",    f: "brightness(.5)",                                  night: 1,',
    'field: "rgba(18,34,78,.52)",    f: "brightness(.62) saturate(.75)",                   night: .3,')
# Tipp-Karten: Spiel steht, solange die Karte offen ist
rep('function show(i) { const T = TIPS[i]; cur = T;', 'function show(i) { const T = TIPS[i]; cur = T; try { S.coachHold = true; } catch (e) {}   /* V644: Spiel steht */')
rep('function close() { if (!cur) return; card.classList.remove("on"); arr.hidden = true;', 'function close() { if (!cur) return; try { S.coachHold = false; } catch (e) {}   /* V644 */ card.classList.remove("on"); arr.hidden = true;')
open(p, "w", encoding="utf-8").write(s)
print("ok V644")
