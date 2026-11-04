"""V231: Welttour-Start als richtiger Übergang: rosa Flugzeug fliegt ~4,5 s quer über die Welt und landet an der
River Bank, die Kamera fährt dabei mit nach links und zoomt hinein; danach Ankunftsbild (Rosie & Blue mit dem
Wasserflugzeug am Fluss, «SOUTH AMERICA · River Bank»), erst dann setzt die Musik ein. Antippen überspringt."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V230";', 'const GAME_VER = "V231";')
rep('<link rel="preload" as="image" href="img/worldmap.webp">', '<link rel="preload" as="image" href="img/worldmap.webp"><link rel="preload" as="image" href="img/arrive_samerica.webp">')
PL = ('<svg viewBox="0 0 24 24" width="46" height="46" aria-hidden="true"><path d="M21 16v-2l-8-5V3.5c0-.83-.67-1.5-1.5-1.5S10 2.67 10 3.5V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5l8 2.5z" '
      'fill="#ff6fb5" stroke="#3a2414" stroke-width="1.3" stroke-linejoin="round"/><path d="M11.5 4v4.2" stroke="#fff" stroke-width="1.1" stroke-linecap="round" opacity=".9"/></svg>')
rep('<div class="mapPlane">✈️</div>', '<div class="mapPlane">' + PL + '</div>')
a = s.index('    function playIntro(done) {'); e = s.index('    /* Einhängen vor dem Wellenstart */', a)
s = s[:a] + r'''    function playIntro(done) { let arr = null;
      seqDone = () => { try { arr && arr.remove(); } catch (e) {} try { if (SFX.music.playing < 1) SFX.music.start(1); } catch (e) {} if (done) done(); };
      show("auto"); drawPins(-1); setMe(MAP_PTS[0][0], false); label("", "The world tour begins", "5 continents · 30 places · 150 waves");
      const W0 = worldCam(), RB = MAP_PTS[0][0]; go(W0, 0);
      at(950, () => { try { SFX.music.stop(0.3); } catch (e) {} });   // Spielmusik erst mit dem Ankunftsbild
      at(600, () => { label("", "Flying to South America", "First stop: River Bank"); flyPlane([1.04, .2], RB, 4600); });
      at(700, () => go({ x: .62, y: .42, k: W0.k * 1.12 }, 1800));
      at(2500, () => go({ x: .42, y: .55, k: W0.k * 1.6 }, 1800));
      at(4200, () => go({ x: RB[0] + .02, y: RB[1] - .06, k: Math.min(4.2, W0.k * 3) }, 1300));
      at(5300, () => { drawPins(0); setMe(RB, true); label("SOUTH AMERICA", "Landed: River Bank", "Waves 1–5 · the Jungle Temple waits at wave 26"); try { snd("coin"); } catch (e) {} });
      at(6700, () => { arr = document.createElement("div"); arr.className = "mapArrive"; arr.innerHTML = `<img src="img/arrive_samerica.webp" alt=""><div class="maTxt"><small>WORLD TOUR · STOP 1 OF 30</small><b>SOUTH AMERICA</b><span>River Bank · wave 1</span></div>`;
        ov.appendChild(arr); requestAnimationFrame(() => arr.classList.add("on"));
        try { SFX.music.start(1); } catch (e) {} try { SFX.say && SFX.say("newcont"); } catch (e) {} });
      at(10600, hide); }
''' + s[e:]
css = '''<style id="v231">
#ovMap .mapPlane{opacity:0;transform:translate(-50%,-50%) scale(var(--ik,1)) rotate(calc(var(--a,0deg) + 90deg))!important;font-size:0;line-height:0}
#ovMap .mapPlane.on{opacity:1}
#ovMap .mapPlane svg{display:block;width:46px;height:46px;filter:drop-shadow(0 8px 5px rgba(0,0,0,.28))}
#ovMap .mapArrive{position:absolute;inset:0;z-index:5;opacity:0;transition:opacity .7s ease;background:#2b3a22;overflow:hidden}
#ovMap .mapArrive.on{opacity:1}
#ovMap .mapArrive img{position:absolute;inset:0;width:100%;height:100%;max-width:none!important;object-fit:cover;object-position:50% 60%;transform:scale(1.08);transition:transform 4.5s ease-out}
#ovMap .mapArrive.on img{transform:scale(1)}
#ovMap .maTxt{position:absolute;left:12px;right:12px;top:calc(env(safe-area-inset-top,0px) + 18px);margin:0 auto;max-width:420px;text-align:center;display:grid;gap:4px;transform:translateY(-14px);opacity:0;transition:all .6s ease .5s}
#ovMap .mapArrive.on .maTxt{transform:none;opacity:1}
#ovMap .maTxt small{font:800 11px/1 "Baloo 2",sans-serif;letter-spacing:.18em;color:#fff;text-shadow:0 2px 3px rgba(0,0,0,.5)}
#ovMap .maTxt b{font:400 clamp(40px,12vw,58px)/1 var(--f-display,"Bangers",sans-serif);letter-spacing:.03em;color:#ffd84d;-webkit-text-stroke:3px #3a2414;paint-order:stroke fill;text-shadow:0 4px 0 #3a2414}
#ovMap .maTxt span{justify-self:center;font:800 14px/1 "Baloo 2",sans-serif;color:#3a2414;background:#fff7e8;border:2.5px solid #3a2414;border-radius:999px;padding:6px 14px 5px;box-shadow:0 3px 0 #3a2414}
</style>
'''
i = s.rfind('</body>'); s = s[:i] + css + s[i:]
open(dst, 'w', encoding='utf-8').write(s); print('ok')
