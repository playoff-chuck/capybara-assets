#!/usr/bin/env python3
# V612 (Martin 11.11. 12:03/12:04): «Replay tutorial» in den Einstellungen als Werbebanner mit Coach Ollie (Nano Banana Pro, img/tut_banner.webp), ganzer Banner klickbar.
# Vorher: img/tut_banner.webp nach site/img/ kopieren.
import sys, os, json
site = sys.argv[1]; p = os.path.join(site, "index.html"); s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V611";', 'const GAME_VER = "V612";')
rep('<button id="setReTut" class="btn-small" type="button">↺ Replay tutorial</button>',
    '<button id="setReTut" class="tutBanner" type="button"><span class="tbTxt"><small>COACH OLLIE</small><b>10 LESSONS FROM THE PRO</b><em>Brush up your moves – then go for the record!</em></span><span class="tbGo">▶</span></button>')
rep('#ovSettings .setTut small{', '''#ovSettings .tutBanner{position:relative;display:flex;align-items:center;width:100%;max-width:340px;aspect-ratio:720/301;margin-top:10px;padding:8px 40px 8px 44%;border:3px solid var(--ink,#3a1d10)!important;border-radius:16px;background:linear-gradient(90deg,rgba(6,40,30,0) 30%,rgba(6,40,30,.55) 55%,rgba(6,40,30,.75) 100%),url(img/tut_banner.webp) center/cover no-repeat #0d4a3a!important;box-shadow:0 4px 0 var(--ink,#3a1d10)!important;color:#fff;text-align:left;cursor:pointer;overflow:visible;-webkit-tap-highlight-color:transparent;animation:tbPulse 2.4s ease-in-out infinite}
#ovSettings .tutBanner:active{transform:translateY(3px);box-shadow:0 1px 0 var(--ink,#3a1d10)!important}
#ovSettings .tutBanner .tbCoach{position:absolute;left:-4px;bottom:-4px;width:96px;height:96px;object-fit:contain;filter:drop-shadow(0 3px 0 rgba(0,0,0,.35));pointer-events:none}
#ovSettings .tutBanner .tbTxt{display:flex;flex-direction:column;gap:1px;min-width:0}
#ovSettings .tutBanner .tbTxt small{font:800 10px/1 "Baloo 2",system-ui,sans-serif;letter-spacing:.16em;color:#bff3e9;text-transform:uppercase}
#ovSettings .tutBanner .tbTxt b{font-family:var(--f-display,Bangers,Impact,sans-serif);font-weight:400;font-size:20px;line-height:1;letter-spacing:.03em;color:#ffd84d;text-shadow:0 2px 0 #0a3f3c}
#ovSettings .tutBanner .tbTxt em{font:700 12px/1.2 "Baloo 2",system-ui,sans-serif;font-style:normal;color:#fff}
#ovSettings .tutBanner .tbGo{position:absolute;right:10px;top:50%;width:28px;height:28px;margin-top:-14px;border-radius:50%;background:#ffd84d;color:#0a3f3c;display:grid;place-items:center;font-size:14px;border:2px solid var(--ink,#3a1d10)}
@keyframes tbPulse{0%,100%{transform:scale(1)}50%{transform:scale(1.025)}}
@media (prefers-reduced-motion:reduce){#ovSettings .tutBanner{animation:none}}
#ovSettings .setTut small{''')
open(p, "w", encoding="utf-8").write(s)
T = {"en": {"10 LESSONS FROM THE PRO": "10 LESSONS FROM THE PRO", "Brush up your moves – then go for the record!": "Brush up your moves – then go for the record!"},
     "ru": {"10 LESSONS FROM THE PRO": "10 УРОКОВ ОТ ПРОФИ", "Brush up your moves – then go for the record!": "Освежи приёмы – и вперёд за рекордом!"},
     "de": {"10 LESSONS FROM THE PRO": "10 LEKTIONEN VOM PROFI", "Brush up your moves – then go for the record!": "Frisch die Tricks auf – dann auf zum Rekord!"},
     "es": {"10 LESSONS FROM THE PRO": "10 LECCIONES DEL PRO", "Brush up your moves – then go for the record!": "Repasa tus trucos – ¡y a por el récord!"},
     "pt": {"10 LESSONS FROM THE PRO": "10 LIÇÕES DO PROFISSIONAL", "Brush up your moves – then go for the record!": "Revise seus truques – e vá atrás do recorde!"}}
for l, m in T.items():
    q = os.path.join(site, "lang", l + ".json"); d = json.loads(open(q, encoding="utf-8").read()); d.update(m)
    open(q, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=0))
print("ok V612")
