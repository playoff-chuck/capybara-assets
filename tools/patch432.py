#!/usr/bin/env python3
# V432 (/neu-Chat, Martin 08.11.): Elite-Turm-Wow (W6): Doppeldecker flog mit dem Heck voran (Bild schaut nach links, Flug nach rechts) → gespiegelt.
# Absprung von Rosie & Blue: starten jetzt wirklich aus dem Cockpit (Position zur Sprungzeit berechnet), kleiner Hüpfer nach oben,
# Schirm geht erst nach 0,4 s auf, Pendeln am Schirm bis zur Landung. Elite-Aktivierung 3,6 s (nach der zweiten Landung).
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:80])
    s = s.replace(a, b)

rep('const GAME_VER = "V431";', 'const GAME_VER = "V432";')
rep('''  d.innerHTML = `<img class="wpPlane" src="img/biplane.webp" alt=""><div class="wpChute" style="--tx:${pt.x}px;--ty:${pt.y}px"><span class="cA"></span><img src="${HERO_IMG[h]}" alt=""></div><div class="wpChute b2" style="--tx:${pt.x + 26}px;--ty:${pt.y}px"><span class="cA"></span><img src="${HERO_IMG[b]}" alt=""></div>`;''',
'''  /* V432: Absprung aus dem Cockpit – Position des Flugzeugs zur Sprungzeit (1 s / 1,25 s von 3,4 s Flug) */
  const px = tt => -160 + (innerWidth + 330) * tt / 3.4 + 72, py = innerHeight * 0.09 + 52;
  const ch = (k, tt, dx, cls) => `<div class="wpChute${cls}" style="--sx:${Math.round(px(tt))}px;--sy:${Math.round(py)}px;--tx:${pt.x + dx}px;--ty:${pt.y}px"><div class="wpSw"><span class="cA"></span><img src="${HERO_IMG[k]}" alt=""></div></div>`;
  d.innerHTML = `<img class="wpPlane" src="img/biplane.webp" alt="">` + ch(h, 1.0, 0, "") + ch(b, 1.25, 26, " b2");''')
rep('''t.eliteT = 60; snd("powerup"); wowBuzz([40, 40, 90]); announce("ELITE TOWER", "Rosie & Blue on board · 2× fire rate for 60 s", "SQUAD", 2400); }, 3300);''',
    '''t.eliteT = 60; snd("powerup"); wowBuzz([40, 40, 90]); announce("ELITE TOWER", "Rosie & Blue on board · 2× fire rate for 60 s", "SQUAD", 2400); }, 3600);''')
rep('.wowPlane .wpPlane{position:absolute;top:9%;left:-160px;width:150px;max-width:none;animation:wowFly 3.4s linear forwards}',
    '.wowPlane .wpPlane{position:absolute;top:9%;left:-160px;width:150px;max-width:none;transform:scaleX(-1);animation:wowFly 3.4s linear forwards}   /* V432: Bild schaut nach links → gespiegelt */')
rep('@keyframes wowFly{to{transform:translateX(calc(100vw + 330px))}}', '@keyframes wowFly{from{transform:scaleX(-1)}to{transform:translateX(calc(100vw + 330px)) scaleX(-1)}}')
rep('.wowPlane .wpChute{position:absolute;left:0;top:0;width:0;height:0;opacity:0;animation:wowChute 2.3s ease-in 1s forwards}',
    '.wowPlane .wpChute{position:absolute;left:0;top:0;width:0;height:0;opacity:0;animation:wowChute 2.3s cubic-bezier(.3,.6,.5,1) 1s forwards}'
    '.wowPlane .wpSw{position:absolute;left:0;top:0;transform-origin:0 -70px;animation:wowSway .85s ease-in-out infinite alternate}'
    '.wowPlane .wpChute .cA{transform:scale(0);transform-origin:50% 100%;animation:wowOpen .3s ease-out 1.4s forwards}.wowPlane .wpChute.b2 .cA{animation-delay:1.65s}')
rep('@keyframes wowChute{0%{opacity:1;transform:translate(42vw,13vh) scale(.6)}100%{opacity:1;transform:translate(var(--tx),var(--ty)) scale(1)}}',
    '@keyframes wowChute{0%{opacity:1;transform:translate(var(--sx),var(--sy)) scale(.45)}14%{opacity:1;transform:translate(calc(var(--sx) + 22px),calc(var(--sy) - 46px)) scale(.6)}100%{opacity:1;transform:translate(var(--tx),var(--ty)) scale(1)}}'
    '@keyframes wowSway{from{transform:rotate(-13deg)}to{transform:rotate(13deg)}}@keyframes wowOpen{to{transform:scale(1)}}')
rep('window.__wow = { W: WOW, done: k => wowDone(k), drop: () => hardDrop(), frozen: () => frozen(), tut: () => TUT.on };',
    'window.__wow = { W: WOW, done: k => wowDone(k), drop: () => hardDrop(), frozen: () => frozen(), tut: () => TUT.on, elite: t => wowElite(t || { x: 4, y: 10 }) };')
open(dst, "w", encoding="utf-8").write(s)
print("ok")
