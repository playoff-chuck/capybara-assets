#!/usr/bin/env python3
# V670 (Martin 12.11. 16:00): Zeugnis (US-Urkunde) – Elemente ragten über den Rahmen.
# Titel, Trennlinien, Symbole links und «A+»-Stempel rechts lagen auf/über dem inneren Rahmen.
# Jetzt Innenabstand links/rechts 12,5 % statt 9 % (innerhalb des goldenen Innenrahmens), Titel etwas kleiner,
# Unterschrift nicht mehr über dem Namen, Name unter der Linie statt durchgestrichen.
import sys, os
site = sys.argv[1]; p = os.path.join(site, "index.html"); s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V669";', 'const GAME_VER = "V670";')
rep('#tutSum .cert.us .ctPaper{background-image:url("img/cert_us.webp?v=568");padding:46% 9% 0}', '#tutSum .cert.us .ctPaper{background-image:url("img/cert_us.webp?v=568");padding:46% 12.5% 0}   /* V670 */')
rep('#tutSum .cert.us .ctPaper h3{font-size:5.7cqw;white-space:nowrap}', '#tutSum .cert.us .ctPaper h3{font-size:4.9cqw;white-space:nowrap}')
rep('#tutSum .ctPaper .ctSign em{font-size:6.6cqw}', '#tutSum .ctPaper .ctSign em{font-size:6.6cqw;margin-bottom:1.2cqw!important}')
rep('#tutSum .cert.us .ctPaper .ctFoot{left:38.5%;bottom:13.4%}', '#tutSum .cert.us .ctPaper .ctFoot{left:38.5%;bottom:11.2%}   /* V670: Name unter die Linie */')
open(p, "w", encoding="utf-8").write(s); print("ok V670")
