#!/usr/bin/env python3
# V625 (Martin 11.11. 13:24): Pause-Knopf «Zz» neu als «Zzz» (Nano Banana Pro, freigestellt img/zzz.webp).
import sys, os, shutil, re
site = sys.argv[1]; p = os.path.join(site, "index.html"); s = open(p, encoding="utf-8").read()
dst = os.path.join(site, "img", "zzz.webp")
if not os.path.exists(dst): shutil.copy("/root/zzz_icon.webp", dst)
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V624";', 'const GAME_VER = "V625";')
pat = r'(\.deckIn \.pad #bWave::before,#bWave::before\{-webkit-mask:none!important;mask:none!important;background:)url\([^)]*\)( center/contain no-repeat!important;)width:66%!important;height:66%!important;'
m = re.findall(pat, s); assert len(m) == 1, len(m)
s = re.sub(pat, r'\1url("img/zzz.webp?v=625")\2width:80%!important;height:80%!important;', s, count=1)
m = re.search(r'const ZZ = `<svg viewBox="0 0 24 24"><g class="ic">.*?</g></svg>`', s); assert m, "ZZ"
s = s.replace(m.group(0), 'const ZZ = `<img class="ic" src="img/zzz.webp?v=625" alt="" style="width:78%;height:78%;object-fit:contain">`', 1)
open(p, "w", encoding="utf-8").write(s)
print("ok V625")
