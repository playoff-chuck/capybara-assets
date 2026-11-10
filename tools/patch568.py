#!/usr/bin/env python3
# V568 (Martin 10.11. 21:25): Urkunde mit gemaltem Blatt aus Nano Banana Pro (img/cert_ru.webp = Похвальный лист,
# img/cert_us.webp = US-Urkunde). Text bleibt HTML (alle Sprachen), skaliert mit dem Blatt (cqw).
# Gezeichneter Lorbeer, Stempel und Heldenbild entfallen – sind im Bild. Preis + Knopf unter dem Blatt.
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V567";', 'const GAME_VER = "V568";')
rep('<div class="tsCard cert"><div class="ctRib">', '<div class="tsCard cert"><div class="ctPaper"><div class="ctRib">')
rep('<b>PASSED</b></div></div><div class="ctPrize">', '<b>PASSED</b></div></div></div><div class="ctPrize">')
CSS = '''<style id="v568cert">
#tutSum .tsCard.cert{background:none!important;box-shadow:none!important;padding:0!important;width:min(94vw,380px,64vh);overflow:visible;max-height:none}
#tutSum .cert::before,#tutSum .cert::after{display:none}
#tutSum .ctPaper{position:relative;container-type:inline-size;aspect-ratio:720/964;background:url("img/cert_ru.webp?v=568") center/100% 100% no-repeat;filter:drop-shadow(0 12px 22px rgba(0,0,0,.55));padding:28% 14% 0;box-sizing:border-box;margin-bottom:12px}
#tutSum .cert.us .ctPaper{background-image:url("img/cert_us.webp?v=568");padding:46% 9% 0}
#tutSum .ctPaper>img.ctHero,#tutSum .ctPaper .ctLaur,#tutSum .ctPaper .ctStamp{display:none!important}
#tutSum .ctPaper .ctRib{background:none;clip-path:none;border:0;padding:0;margin:0 0 1cqw;color:#8a1f1f;font:700 3.2cqw/1 Georgia,serif;letter-spacing:.2em}
#tutSum .cert.us .ctPaper .ctRib{position:absolute;left:0;right:0;top:27.6%;margin:0;color:#f3d77a;font-size:3.4cqw;text-shadow:0 1px 0 #0f2142}
#tutSum .ctPaper h3{font-size:7.2cqw;margin:0 0 1cqw}
#tutSum .cert.us .ctPaper h3{font-size:5.7cqw;white-space:nowrap}
#tutSum .cert.us .ctPaper .ctSub{margin-bottom:1.5cqw}
#tutSum .cert.us .ctPaper li{padding:.7cqw .5cqw}
#tutSum .cert.us .ctPaper li span{font-size:2.95cqw;line-height:1.18}
#tutSum .cert.us .ctPaper .ctSub{font-size:3.3cqw}
#tutSum .cert.us .ctPaper li i{font-size:4.2cqw}
#tutSum .cert.us .ctPaper .ctMark{width:10cqw}#tutSum .cert.us .ctPaper .ctMark em{min-width:7cqw;height:7cqw;font-size:3.8cqw}#tutSum .cert.us .ctPaper .ctMark small{display:none}
#tutSum .ctPaper .ctSub{font-size:3.7cqw;margin:0 0 2.5cqw}
#tutSum .ctPaper ul{margin:0 0 2cqw}
#tutSum .ctPaper li{padding:1.6cqw .5cqw;gap:2cqw}
#tutSum .ctPaper li i{font-size:5cqw}
#tutSum .ctPaper li span{font-size:3.45cqw;line-height:1.25}
#tutSum .ctPaper .ctMark{width:13cqw}
#tutSum .ctPaper .ctMark em{min-width:8.5cqw;height:8.5cqw;font-size:4.8cqw}
#tutSum .ctPaper .ctMark small{font-size:2.6cqw}
#tutSum .ctPaper .ctFoot{position:absolute;left:18%;bottom:13.6%;margin:0}
#tutSum .cert.us .ctPaper .ctFoot{left:38.5%;bottom:13.4%}
#tutSum .ctPaper .ctSign em{font-size:6.6cqw}
#tutSum .ctPaper .ctSign small{font-size:2.8cqw;border-top:0;padding-top:1.4cqw}
#tutSum .cert>.ctPrize{display:block;width:max-content;margin:0 auto 10px}
#tutSum .cert>button{display:block;width:100%}
</style>
'''
rep("</body>", CSS + "</body>")
open(dst, "w", encoding="utf-8").write(s)
print("ok")
