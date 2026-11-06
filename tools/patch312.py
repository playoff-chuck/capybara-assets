"""V312: Kontinent-Ende in der richtigen Reihenfolge (Martin 06.11. 10:05, «AA» getestet).
Bisher: Wegweiser (Nuts-Abstecher / weiter) → Tippen → Spielscreen noch einmal sichtbar (V309: 5 s Ruhe) →
erst dann auf der Weltkarte die Feier «AFRICA CLEARED» mit Strahlen → Flug.
Jetzt: 1. Feier (Strahlen, Konfetti, «AFRICA CLEARED!») am Spielscreen, 2. danach der Wegweiser,
3. nach «Next» sofort die Weltkarte (kein Spielscreen dazwischen, keine zweite Feier auf der Karte, Flug 2,2 s früher)."""
import sys, re
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)

rep('const GAME_VER = "V311";', 'const GAME_VER = "V312";')

# 1) Feier am Spielscreen vor dem Wegweiser
rep('function showSign(c) {\n  S.intro = true; S.signOpen = c + 1;',
    'function showSign(c) {\n  if (window.__contCel && window.__celFor !== S.wave) { window.__celFor = S.wave; S.intro = true; S.signOpen = c + 1;   /* V312: erst Feier am Spielscreen, dann Wegweiser */\n'
    '    window.__contCel(nzName(c), c, () => { S.signOpen = 0; showSign(c); }); return; }\n'
    '  S.intro = true; S.signOpen = c + 1;')

# 2) Nach «Next»: sofort Karte, ohne 5-s-Ruhe
rep('closeSign(); toast(`NUTS DETOUR · any time later from the pause menu`, "HQ", 2400); if (S && !S.inWave) S.waveCD = Math.min(S.waveCD || 0, 0.3); });',
    'closeSign(); window.__fromSign = true; toast(`NUTS DETOUR · any time later from the pause menu`, "HQ", 2400); if (S && !S.inWave) S.waveCD = Math.min(S.waveCD || 0, 0.02); });   /* V312: Karte sofort */')
rep('if (play) { const calm = performance.now() - (window.__evtLast || -1e9); if (calm < 5000) {',
    'if (play) { const calm = performance.now() - (window.__evtLast || -1e9); if (calm < 5000 && !window.__fromSign) {')

# 3) Auf der Karte keine zweite Feier, wenn sie schon am Spielscreen lief; Ablauf 2,2 s früher
i = s.index('function playCont(w, done) {'); j = s.index('function playIntro(done)', i)
body = s[i:j]
body2 = body.replace('const end = celebrate(`${contName(oc)} CLEARED!`, `Continent ${P.c} of 5 · the world tour goes on`);',
    'const sk = window.__fromSign ? 2200 : 0; window.__fromSign = false;   /* V312: Feier lief schon am Spielscreen */\n'
    '      const end = sk ? (() => {}) : celebrate(`${contName(oc)} CLEARED!`, `Continent ${P.c} of 5 · the world tour goes on`);')
assert body2 != body
body2, n = re.subn(r'at\((\d+), ', lambda m: f'at({m.group(1)} - sk, ', body2)
assert n == 8, n
s = s[:i] + body2 + s[j:]

# 4) Feier-Ebene über dem Spielfeld (gleiche Optik wie auf der Karte)
css = []
for m in re.finditer(r'#ovMap (\.mapCel|\.cel)[^{]*\{[^}]*\}', s):
    css.append(m.group(0).replace('#ovMap ', '#gameCel '))
assert len(css) >= 10, len(css)
css_txt = '\n'.join(css) + '\n#gameCel{position:fixed;inset:0;z-index:80;pointer-events:none}\n#gameCel .mapCel{position:absolute}\n'
k = s.rindex('</body>') if '</body>' in s else len(s)
JS = r'''
/* V312: Kontinent-Feier am Spielscreen (vor dem Wegweiser) */
try { (() => {
  const host = document.createElement("div"); host.id = "gameCel"; host.hidden = true; document.body.appendChild(host);
  const fx = k => { try { snd(k); } catch (e) {} };
  window.__contCel = (name, c, then) => {
    let conf = ""; for (let i = 0; i < 46; i++) conf += `<i style="--x:${(Math.random() * 2 - 1).toFixed(2)};--y:${(-.4 - Math.random() * .9).toFixed(2)};--r:${Math.floor(Math.random() * 720 - 360)}deg;--d:${(Math.random() * .25).toFixed(2)}s;--c:${["#ffd84d", "#ff6fb5", "#5cbf4a", "#4aa8ff", "#ff9a2a", "#fff"][i % 6]}"></i>`;
    const el = document.createElement("div"); el.className = "mapCel";
    el.innerHTML = `<div class="celRays"></div><div class="celConf">${conf}</div><div class="celTxt"><b>${name} CLEARED!</b><span>Continent ${c + 1} of 5 · the world tour goes on</span><em>★ ★ ★</em></div>`;
    host.innerHTML = ""; host.appendChild(el); host.hidden = false; requestAnimationFrame(() => el.classList.add("on"));
    fx("boom"); setTimeout(() => fx("jingle"), 180); setTimeout(() => fx("hkWin"), 650);
    setTimeout(() => el.classList.add("out"), 2600);
    setTimeout(() => { host.hidden = true; host.innerHTML = ""; try { then && then(); } catch (e) { console.error("contCel", e); } }, 3300);
  };
})(); } catch (e) { console.error("contCel", e); }
'''
anchor = '})();\n</script>'
p = s.rindex(anchor)
s = s[:p] + JS + s[p:]
q = s.rindex('</body>')
s = s[:q] + '<style>\n' + css_txt + '</style>\n' + s[q:]
open(dst, 'w', encoding='utf-8').write(s)
print("ok", len(css))
