"""V255: Bandit v2 (Martin 05.11. 13:28) + Weltkarte grün (13:31).
- Neuer Automat (Nano Banana Pro) streng frontal, drei große, fast quadratische Fenster (img/bandit_cab2.webp).
- Walzen-Bilder neu gezeichnet und größer: Sniper, Mixer, Tesla, Lockdown, Chomper, Ten-ton (img/slot_*.webp).
- Eigener Automaten-Sound: Hebel-Klack, Walzen-Rattern, das langsamer wird, dumpfer Stopp je Walze mit Klick,
  Jackpot-Fanfare (Arpeggio) mit Münzregen-Klingeln, dazu «Jackpot!».
- Weltkarte: geschaffte Orte und Wegstücke sanft grün statt gelb."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V254";', 'const GAME_VER = "V255";')
# Automat
rep('<img class="bdCabImg" src="img/bandit_cab.webp"', '<img class="bdCabImg" src="img/bandit_cab2.webp"')
old = [(12.25, 37.7, 13.4, 22.5), (31.75, 38.1, 13.6, 22.9), (51.8, 38.5, 14.0, 23.1)]
new = [(10.6, 43.5, 19.2, 17.4), (32.4, 43.5, 19.2, 17.4), (54.1, 43.5, 19.2, 17.4)]
for i, (o, n) in enumerate(zip(old, new)):
    rep(f'style="left:{o[0]}%;top:{o[1]}%;width:{o[2]}%;height:{o[3]}%"', f'style="left:{n[0]}%;top:{n[1]}%;width:{n[2]}%;height:{n[3]}%"')
rep('const IMG = (typeof ICO_SPR !== "undefined" && ICO_SPR) || {};',
    'const IMG = { snipe: "img/slot_snipe.webp", mix: "img/slot_mix.webp", tesla: "img/slot_tesla.webp", lock: "img/slot_lock.webp", chomp: "img/slot_chomp.webp", ton: "img/slot_ton.webp" };')
# Sound
rep('const stops = [1300, 2000, 2900]; let tick = setInterval(() => { try { snd("hkTick", 1); } catch (e) {} }, 110);',
    '''const stops = [1300, 2000, 2900], t0s = performance.now(); let tick = null, stopped = 0;
      const BS = window.__bdSnd; try { BS.lever(); } catch (e) {}
      const tk = () => { const el = performance.now() - t0s; if (stopped >= 3) return; try { BS.tick(1 - stopped * 0.18); } catch (e) {} tick = setTimeout(tk, 55 + Math.min(160, el / 18)); }; tick = setTimeout(tk, 140);''')
rep('setTimeout(() => { $b("bdR" + i).classList.add("hit"); try { snd(i < 2 ? "confirm" : "coin"); } catch (e) {}',
    'setTimeout(() => { $b("bdR" + i).classList.add("hit"); stopped = i + 1; try { BS.stop(i); } catch (e) {}')
rep('if (i === 2) { clearInterval(tick); win(); } }, stops[i] + 40); });', 'if (i === 2) { clearTimeout(tick); win(); } }, stops[i] + 40); });')
rep('try { snd("hkWin"); setTimeout(() => SFX.say("Jackpot!", 1.0, 1.0), 350); } catch (e) {}',
    'try { window.__bdSnd.win(); setTimeout(() => SFX.say("Jackpot!", 1.0, 1.0), 650); } catch (e) {}')
rep('const $b = id => document.getElementById(id), LEN = 30;', '''const $b = id => document.getElementById(id), LEN = 30;
    window.__bdSnd = {   /* V255: eigene Automaten-Geräusche über tone() (Effekt-Lautstärke) */
      lever() { tone(420, 140, 0.12, 0.22, 0, "square", 1800); tone(95, 55, 0.22, 0.4, 0.02, "sine"); tone(2600, 2600, 0.02, 0.06, 0.13, "square"); },
      tick(k) { tone(1500 * k + 500, 1200 * k + 400, 0.022, 0.06, 0, "square", 3200); },
      stop(i) { tone(240 - i * 30, 70, 0.16, 0.42, 0, "triangle"); tone(3200, 3000, 0.03, 0.07, 0.01, "square", 5000); if (i === 1) tone(660, 660, 0.12, 0.12, 0.08, "triangle"); },
      win() { [523, 659, 784, 1047, 1319, 1568].forEach((f, j) => tone(f, f, 0.22, 0.2, j * 0.085, "triangle"));
        tone(1047, 1047, 0.6, 0.16, 0.55, "triangle"); tone(1319, 1319, 0.6, 0.12, 0.55, "triangle"); tone(1568, 1568, 0.6, 0.12, 0.55, "triangle");
        for (let k = 0; k < 14; k++) tone(2400 + Math.random() * 1400, 3000 + Math.random() * 1200, 0.07, 0.07, 0.25 + k * 0.07 + Math.random() * 0.04, "sine"); try { snd("coin"); } catch (e) {} } };''')
css = r'''
<style id="v255bandit">
.bdCab{aspect-ratio:600/881!important;width:min(100%,calc((100vh - 270px) * .681))!important}
#ovBandit .bdCab .bdReel{border-radius:12px}
#ovBandit .bdCab .bdStrip img{width:86%!important;max-height:86%!important}
.bdCab .bdLever{left:82%!important;top:36%!important;width:18%!important;height:42%!important}
#ovMap .mPin.done i{background:#9fd18a!important}
#ovMap .mPin.star.done i::after{background:#9fd18a!important}
#ovMap .mapPath polyline.done{stroke:#6fae58!important;opacity:.8}
</style>
'''
i = s.rfind('</body>'); s = s[:i] + css + s[i:]
open(dst, 'w', encoding='utf-8').write(s); print('ok')
