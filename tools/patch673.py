# V673: Diplom – nur ein Strich (Unterschrift), Stempel liegt über der Unterschrift (EN/ES/PT/DE + RU)
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf8").read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:60], c); s = s.replace(a, b)
rep('img/cert_ru.webp?v=569', 'img/cert_ru.webp?v=673')
rep('img/cert_us.webp?v=568', 'img/cert_us.webp?v=673')
A = '#tutSum .ctPaper .ctSign small{font-size:2.8cqw;border-top:0;padding-top:1.4cqw}'
rep(A, A + '\n#tutSum .ctPaper::after{content:"";position:absolute;z-index:3;pointer-events:none;left:24.9%;top:76.2%;width:17%;aspect-ratio:169/168;background:url("img/stamp_ru.webp?v=673") center/contain no-repeat;transform:rotate(-12deg);mix-blend-mode:multiply;opacity:.9}   /* V673: Stempel über der Unterschrift */\n#tutSum .cert.us .ctPaper::after{left:46.5%;top:77.6%;width:16.7%;aspect-ratio:120/116;background-image:url("img/stamp_us.webp?v=673")}')
rep('const GAME_VER = "V672"', 'const GAME_VER = "V673"')
open(dst, "w", encoding="utf8").write(s); print("ok")
