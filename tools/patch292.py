"""V292 (Martin 17:42): In Afrika wird aus dem Schneesturm («Siberia», W35 usw.) ein Sandsturm: honig-goldener Sandschleier,
goldene Sandkörner statt Flocken, goldener Rand statt Frost, keine Eiszapfen/Raureif, Band «DUNE STORM · 52°C», Meldung «SANDSTORM!».
Andere Kontinente behalten den Schneesturm.
Martin 17:43: Hagelsturm fällt 50 % schneller."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V291";', 'const GAME_VER = "V292";')
rep('const SNOW_BASES = [18];', 'const SNOW_BASES = [18];\nwindow.__sandy = () => { try { return !!(S && !S.nuts && wherePos(S.wave).cont[0] === "africa"); } catch (e) { return false; } };   /* V292 */')
rep('S.snowBandT = 5; snd("ice"); setTimeout(() => { if (snowOn()) announce("SIBERIA!", "Whiteout · trust your towers", "ALERT", 2800); }, 250);',
    'S.snowBandT = 5; { const sd = window.__sandy(), sb = $("snowBand"); sb.classList.toggle("sandBand", sd); sb.classList.toggle("snowBand", !sd); sb.innerHTML = sd ? "<span>SANDSTORM</span><i>DUNE STORM · 52°C</i><span>SANDSTORM</span>" : "<span>SIBERIA</span><i>BLIZZARD · −40°</i><span>SIBERIA</span>"; if (!sd) snd("ice");\n      setTimeout(() => { if (snowOn()) announce(sd ? "SANDSTORM!" : "SIBERIA!", sd ? "Sand in your eyes · trust your towers" : "Whiteout · trust your towers", "ALERT", 2800); }, 250); }')
rep('if (on) { S.iceT = (S.iceT ?? 2) - dt; if (S.iceT <= 0) { S.iceT = 2.5 + Math.random() * 4; snd("ice"); } }',
    'if (on && !window.__sandy()) { S.iceT = (S.iceT ?? 2) - dt; if (S.iceT <= 0) { S.iceT = 2.5 + Math.random() * 4; snd("ice"); } }')
rep('$("board").classList.toggle("blizzard", on);', '$("board").classList.toggle("blizzard", on); $("board").classList.toggle("duneStorm", on && window.__sandy());')
rep('''function drawSnow(s, W, HH) {
  if (!snowOn()) { SNOW.length = 0; return; }''', '''function drawSnow(s, W, HH) {
  if (!snowOn()) { SNOW.length = 0; return; }
  const SD = window.__sandy(), FB = SD ? "236,192,112" : "235,242,250";''')
rep('ctx.fillStyle = `rgba(226,236,246,${fogA.toFixed(3)})`;', 'ctx.fillStyle = SD ? `rgba(222,170,88,${(fogA * 0.92).toFixed(3)})` : `rgba(226,236,246,${fogA.toFixed(3)})`;')
rep('gr.addColorStop(0, "rgba(235,242,250,0)"); gr.addColorStop(0.5, `rgba(235,242,250,${(0.25 + 0.45 * g).toFixed(3)})`); gr.addColorStop(1, "rgba(235,242,250,0)");',
    'gr.addColorStop(0, `rgba(${FB},0)`); gr.addColorStop(0.5, `rgba(${FB},${(0.25 + 0.45 * g).toFixed(3)})`); gr.addColorStop(1, `rgba(${FB},0)`);')
rep('ctx.fillStyle = `rgba(255,255,255,${a.toFixed(2)})`; ctx.beginPath(); ctx.arc(f.x * s, f.y * s, r, 0, 7); ctx.fill();',
    'ctx.fillStyle = SD ? `rgba(${f.z > 0.5 ? "190,132,52" : "238,196,118"},${a.toFixed(2)})` : `rgba(255,255,255,${a.toFixed(2)})`; ctx.beginPath(); ctx.arc(f.x * s, f.y * s, SD ? r * 0.7 : r, 0, 7); ctx.fill();')
rep('if (g > 0.55 && f.z > 0.7) { ctx.strokeStyle = `rgba(255,255,255,${(a * 0.5).toFixed(2)})`;',
    'if (g > 0.55 && f.z > 0.7) { ctx.strokeStyle = SD ? `rgba(214,160,80,${(a * 0.5).toFixed(2)})` : `rgba(255,255,255,${(a * 0.5).toFixed(2)})`;')
rep('vg.addColorStop(0, "rgba(200,225,245,0)"); vg.addColorStop(1, `rgba(214,236,252,${(0.55 + 0.25 * g).toFixed(2)})`);',
    'vg.addColorStop(0, SD ? "rgba(214,160,80,0)" : "rgba(200,225,245,0)"); vg.addColorStop(1, SD ? `rgba(200,140,60,${(0.5 + 0.25 * g).toFixed(2)})` : `rgba(214,236,252,${(0.55 + 0.25 * g).toFixed(2)})`);')
rep('  if (!ICICLES || ICICLES.n !== GW) {', '  if (SD) return;\n  if (!ICICLES || ICICLES.n !== GW) {')
# Martin 17:43: Hagelsturm 50 % schneller (Fall-Intervall ÷ 1,5, solange Hagel aktiv)
rep('  { const e = SPEC_AT[((S.wave - 1) % 100) + 1]; if (e && e[0] === 16 && S.inWave && e[1] >= 2) return g / (e[1] === 2 ? 0.7 : 0.65); }',
    '  if (hailOn()) return g / 1.5;   /* V292: Hagel 50 % schneller */\n  { const e = SPEC_AT[((S.wave - 1) % 100) + 1]; if (e && e[0] === 16 && S.inWave && e[1] >= 2) return g / (e[1] === 2 ? 0.7 : 0.65); }')
css = r'''
<style id="v292sand">
.board.blizzard.duneStorm{border-color:#e2b46a!important;box-shadow:0 0 0 2px rgba(240,200,130,.6),0 0 26px rgba(222,170,90,.5) inset!important}
.board.blizzard.duneStorm canvas#cv{filter:saturate(.8) sepia(.25) brightness(1.02)!important}
</style>
'''
i = s.rindex('</body>'); s = s[:i] + css + s[i:]
open(dst, 'w', encoding='utf-8').write(s)
