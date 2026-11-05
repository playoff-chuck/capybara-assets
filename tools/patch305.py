"""V305 (To-do 16, Paket groß, Nano Banana Pro 1,93 $): Monster ohne Zombie-Look und in voller Auflösung.
norm = grüner Sumpf-Knubbel (statt Zombie), fast = gelber Gecko-Sprinter, runner = Panzer-Gürteltier auf Rollschuhen;
jaguar/mummy/tiger/bear in 512 px neu (Design wie in den Einführungsbildern). Einführungsbilder Sprinter/Läufer mit Blue/Rosie neu.
Neue Dateien unter Inhalts-Hash in site/img, Verweise ersetzt (alte Dateien bleiben liegen)."""
import sys, hashlib, shutil, os
src, dst = sys.argv[1], sys.argv[2]
root = os.path.dirname(os.path.abspath(src))
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=None):
    global s
    n = s.count(a); assert n >= 1 and (cnt is None or n == cnt), (n, a[:70]); s = s.replace(a, b); return n
rep('const GAME_VER = "V304";', 'const GAME_VER = "V305";', 1)
R = '/srv/media/pro/v305/'
MAP = {'norm': '4a68aa4fcd', 'fast': '8cfb3691d3', 'runner': 'c5dfcdbb82', 'jaguar': '3317ee962d', 'mummy': '0826a8aed4',
       'tiger': '6c7759a976', 'bear': '6f4aee52bd', 'in_blue_fast': 'e54c388475', 'in_rosie_fast': 'e2417c2161',
       'in_blue_runner': '20ec90d62e', 'in_rosie_runner': '6954857b7c'}
for k, old in MAP.items():
    data = open(R + k + '.webp', 'rb').read(); h = hashlib.md5(data).hexdigest()[:10]
    shutil.copyfile(R + k + '.webp', os.path.join(root, 'img', h + '.webp'))
    n = rep(f'img/{old}.webp', f'img/{h}.webp')
    print(k, old, '->', h, n, 'Verweise')
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
