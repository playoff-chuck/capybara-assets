"""V336 (Martin 06.11. 23:32/23:33):
Dieb: läuft jetzt ganz oben über allem (über Sprechblasen und Anzeigen), in Höhe der Gold-Anzeige: 10 s von links bis zum Gold,
dann schnappt er das halbe Gold (Gold-Klang, danach leises hämisches Lachen, HeyGen 0,0005 $) und rennt in 10 s zum rechten Rand.
Abschießen: Sniper oder Tesla wählen (Pocket) und den Dieb antippen → Gold zurück. Ohne Waffe: Hinweis.
Magnet: Sound = Variante 2 nur Brummen (ohne Rauschen), leise, solange der Magnet da ist.
Bildausfall: Rauschen nochmal −30 % (0,035 → 0,0245)."""
import sys, json, base64, os
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V335";', 'const GAME_VER = "V336";')
VD = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'voice')
L = json.load(open(os.path.join(VD, 'lines8.json'), encoding='utf-8'))
rep('const VOICE_TEXT = {', 'const VOICE_TEXT = {' + ''.join(f'{json.dumps(k)}: {json.dumps(t)}, ' for k, t in L.items()))
rep('const VOICE = {', 'const VOICE = {' + ''.join(f'"{k}":"' + base64.b64encode(open(os.path.join(VD, k + '.mp3'), 'rb').read()).decode() + '",' for k in L))
rep('noiseLevel(inside ? 0.035 : 0);', 'noiseLevel(inside ? 0.0245 : 0);')
# Dieb nicht mehr im Spielfeld zeichnen / treffen
rep('const T = D.thief; if (T) { const tx = Math.round(T.x);', 'const T = null; if (T) { const tx = Math.round(T.x);')
rep('      if (D.thief) drawThief(D.thief, s);\n', '')
rep('if (D.thief) { const T = D.thief; T.t += dt; T.x = -0.8 + (GW + 1.6) * (T.t / 20);', 'if (D.thief) { const T = D.thief; T.t += dt; if (window.__thiefPos) window.__thiefPos(T);')
rep('snd("sell"); toast(`THIEF GRABBED ${T.stolen} GOLD!`, "ALERT", 1800);', 'snd("sell"); setTimeout(() => snd("sell"), 140); setTimeout(() => { try { SFX.say("thief_laugh", 1.0, 1.0, 0, 0); } catch (e) {} }, 750); toast(`THIEF GRABBED ${T.stolen} GOLD!`, "ALERT", 1800);')
rep('if (T.t >= 20) { if (T.stolen) toast(`THIEF GOT AWAY · −${T.stolen} gold`, "HQ", 1800); D.thief = null; } }',
    'if (T.t >= 20) { if (T.stolen) toast(`THIEF GOT AWAY · −${T.stolen} gold`, "HQ", 1800); D.thief = null; } }\n    if (!D.thief && window.__thiefPos) window.__thiefPos(null);')
# Magnet-Brummen
rep('if (m.t >= m.life) { D.mag = null; toast("MAGNET GONE", "HQ", 1200); } }', 'if (m.t >= m.life) { D.mag = null; toast("MAGNET GONE", "HQ", 1200); } }\n    if (window.__magHum) window.__magHum(D.mag ? 1 : 0);')
rep('D.weed = null; } noiseLevel(0); return; }', 'D.weed = null; if (window.__thiefPos) window.__thiefPos(null); } noiseLevel(0); if (window.__magHum) window.__magHum(0); return; }')
rep('if (!frozen()) step(dt); else noiseLevel(0);', 'if (!frozen()) step(dt); else { noiseLevel(0); if (window.__magHum) window.__magHum(0); }')
JS = r'''
/* V336: Dieb ganz oben über allem · Magnet-Brummen */
try { (() => {
  const el = document.createElement("canvas"); el.id = "thiefCv"; const SZ = 64, DPR = Math.min(3, window.devicePixelRatio || 1); el.width = SZ * DPR; el.height = SZ * DPR;
  el.style.cssText = `position:fixed;left:0;top:0;width:${SZ}px;height:${SZ}px;z-index:2147483000;display:none;cursor:crosshair;touch-action:none;filter:drop-shadow(0 3px 3px rgba(0,0,0,.5))`;
  document.body.appendChild(el); const g = el.getContext("2d");
  function sprite(T) { g.setTransform(DPR, 0, 0, DPR, 0, 0); g.clearRect(0, 0, SZ, SZ); const s = 30, b = Math.abs(Math.sin(T.t * (T.t >= 10 ? 14 : 9))) * 3;
    g.save(); g.translate(SZ / 2, SZ / 2 + 6 - b); if (T.t >= 10) g.rotate(0.12);
    g.fillStyle = "#16161a"; g.beginPath(); g.ellipse(0, s * 0.15, s * 0.32, s * 0.42, 0, 0, 6.29); g.fill();
    const lp = Math.sin(T.t * (T.t >= 10 ? 14 : 9)) * 5; g.fillRect(-8 + lp * 0.4, s * 0.45, 5, 9); g.fillRect(3 - lp * 0.4, s * 0.45, 5, 9);
    g.fillStyle = "#8a5a2b"; g.beginPath(); g.arc(0, -s * 0.32, s * 0.26, 0, 6.29); g.fill();
    g.fillStyle = "#16161a"; g.fillRect(-s * 0.3, -s * 0.56, s * 0.6, s * 0.16); g.fillRect(0, -s * 0.47, s * 0.45, s * 0.07);
    g.fillRect(-s * 0.26, -s * 0.38, s * 0.52, s * 0.11); g.fillStyle = "#fff"; g.fillRect(s * 0.02, -s * 0.37, s * 0.07, s * 0.06); g.fillRect(s * 0.14, -s * 0.37, s * 0.07, s * 0.06);
    if (T.stolen) { g.fillStyle = "#c9a63a"; g.strokeStyle = "#5a4310"; g.lineWidth = 1.5; g.beginPath(); g.arc(-s * 0.42, s * 0.05, s * 0.24, 0, 6.29); g.fill(); g.stroke(); g.fillStyle = "#3a2a08"; g.font = "bold 11px sans-serif"; g.textAlign = "center"; g.textBaseline = "middle"; g.fillText("$", -s * 0.42, s * 0.06); }
    else { g.fillStyle = "#ff4a3a"; g.strokeStyle = "#fff"; g.lineWidth = 3; g.font = "bold 13px sans-serif"; g.textAlign = "center"; const n = String(Math.max(0, Math.ceil(10 - T.t))); g.strokeText(n, 0, -s * 0.66); g.fillText(n, 0, -s * 0.66); }
    g.restore(); }
  window.__thiefPos = T => { if (!T) { el.style.display = "none"; return; }
    const ge = document.getElementById("sGold"), r = ge ? ge.getBoundingClientRect() : { left: innerWidth / 2, width: 0, top: 40, height: 0 };
    const gx = r.left + r.width / 2, gy = r.top + r.height / 2, x = T.t < 10 ? -SZ + (gx + SZ) * (T.t / 10) : gx + (innerWidth + SZ - gx) * Math.min(1, (T.t - 10) / 10);
    el.style.display = "block"; el.style.transform = `translate(${Math.round(x - SZ / 2)}px,${Math.round(gy - SZ / 2 - 4)}px)`; sprite(T); };
  el.addEventListener("pointerdown", ev => { ev.preventDefault(); ev.stopPropagation(); const D = window.__dist && window.__dist.D, T = D && D.thief; if (!T) return;
    let used = null;
    if (S.mode === "snipe" && S.snipes > 0) { S.snipes--; used = "snipe"; } else if (S.mode === "tesla" && S.teslas > 0) { S.teslas--; used = "tesla"; }
    if (!used) { toast((S.snipes > 0 || S.teslas > 0) ? "POCKET → Sniper or Tesla, then tap the thief" : "Only Sniper or Tesla can stop him!", "HQ", 1800); snd("nopeSoft"); return; }
    S.mode = null; S.aim = null; snd(used); S.shake = 0.5;
    if (T.stolen) { S.gold += T.stolen; toast(`THIEF STOPPED · +${T.stolen} gold back`, "HQ", 2000); } else toast("THIEF STOPPED!", "HQ", 1600);
    D.thief = null; window.__thiefPos(null); praise("GOTCHA!", 2, "Nailed it!"); });
  // Magnet-Brummen (Variante 2 ohne Rauschen): 50 Hz mit Obertönen, leichtes Pulsieren
  let hum = null;
  window.__magHum = on => { try { const ac = AU.ac(), out = AU.out(); if (!ac || !out) return;
      if (!hum) { const g2 = ac.createGain(); g2.gain.value = 0; const lfo = ac.createOscillator(), lg = ac.createGain(); lfo.frequency.value = 3.2; lg.gain.value = 0.25; lfo.connect(lg);
        const mix = ac.createGain(); mix.gain.value = 0.75; lg.connect(mix.gain); mix.connect(g2); g2.connect(out);
        [[50, 1], [100, 0.5], [150, 0.33], [250, 0.2], [350, 0.14]].forEach(([f, a]) => { const o = ac.createOscillator(), og = ac.createGain(); o.type = "sine"; o.frequency.value = f; og.gain.value = a; o.connect(og); og.connect(mix); o.start(); });
        lfo.start(); hum = { g: g2, ac, on: 0 }; }
      if (hum.on !== on) { hum.on = on; hum.g.gain.setTargetAtTime(on ? 0.05 : 0, hum.ac.currentTime, on ? 0.25 : 0.12); } } catch (e) {} };
})(); } catch (e) { console.error("v336", e); }
'''
anchor = '})();\n</script>'
p = s.rindex(anchor); s = s[:p] + JS + s[p:]
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
