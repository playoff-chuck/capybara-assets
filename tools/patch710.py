import sys
# V710: abgeschnittene Texte 360×640 / Schrift 130 % (Megatest C1/C5, Martin 14.11.2026)
#  - SALE/FREE-Band im Angebot: Schrift passt sich der Wortlänge an (БЕСПЛАТНО), Sticker bleiben im Bild (ПОДАРОК!)
#  - General-Sprechblase: Untertitel bis 3 Zeilen (Laser-Hinweis), Song-Schild versteckt, solange die Blase offen ist
#  - Lucky Supply: Gewinnname bricht um (СНАЙПЕРСКИЙ ВЫСТРЕЛ), Satz unter dem Titel darf 2 Zeilen haben
#  - Boss-Hack-Einsatzkarte passt in 360 px
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (a[:60], c); s = s.replace(a, b)
rep('const GAME_VER = "V709";', 'const GAME_VER = "V710";')
rep('      try { snd("radio"); } catch (e) {} }\n    function close(bought)',
    '      try { snd("radio"); } catch (e) {} [80, 400].forEach(ms => setTimeout(fitAd, ms)); }\n'
    '    function fitAd() { try { const pic = $a("adPic"), P = pic.getBoundingClientRect(), t = $a("adTag"); t.style.removeProperty("font-size");   /* V710: Band und Sticker bleiben im Bild */\n'
    '        if ($a("adCard").classList.contains("sale") && !$a("adCard").classList.contains("drop")) { const c = fitAd.c || (fitAd.c = document.createElement("canvas").getContext("2d")); c.font = "19px Bangers"; const w = c.measureText(t.textContent).width; if (w > 70) t.style.setProperty("font-size", Math.max(11, Math.floor(19 * 70 / w)) + "px", "important"); }\n'
    '        pic.querySelectorAll(".saleSt").forEach(el => { el.style.marginLeft = ""; if (!el.offsetParent) return; const r = el.getBoundingClientRect(); let dx = 0; if (r.left < P.left + 6) dx = P.left + 6 - r.left; else if (r.right > P.right - 6) dx = P.right - 6 - r.right; if (dx) el.style.marginLeft = Math.round(dx) + "px"; }); } catch (e) {} }\n'
    '    function close(bought)')
rep('#alert.gen span#alSub,#toast.gen span#tSub{font-size:11.5px!important;line-height:1.15!important;text-align:left!important;display:-webkit-box!important;-webkit-line-clamp:2;',
    '#alert.gen span#alSub,#toast.gen span#tSub{font-size:11.5px!important;line-height:1.15!important;text-align:left!important;display:-webkit-box!important;-webkit-line-clamp:3;')
rep('</head>', '<style id="v710fit">body:has(#alert.gen:not([hidden])) #djSong,body:has(#toast.gen:not([hidden])) #djSong{display:none!important}\n'
    '.bdRes b{white-space:normal!important;overflow:visible!important;text-overflow:clip!important;text-wrap:balance;font-size:clamp(19px,6.6vw,26px)!important}\n'
    '.bdSub{height:auto!important;min-height:16px;white-space:normal!important;overflow:visible!important;line-height:1.2!important;text-wrap:balance}\n'
    '.hackBet,.hackRes{box-sizing:border-box!important;width:min(360px,calc(100vw - 12px))!important;max-width:calc(100vw - 12px)!important}</style>\n</head>')
open(dst, "w", encoding="utf-8").write(s)
print("ok")
