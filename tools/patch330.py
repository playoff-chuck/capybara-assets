"""V330 (Martin 06.11. 22:32): Test-Zugang für die neuen Störungen.
Dev-Liste «SPECIAL WAVES» + 4 Einträge (Signal lost W65 · Magnet W80 · Weeds W90 · Thief W100) und Easter Egg.
Direkt-Links: ?test=blk|mag|weed|thief|egg1…egg5 (Kontinent 1–5, Easter Egg selbst auslösen) → nach «TAP TO START» springt das Spiel vor die Welle (Testlauf, zählt nicht für Bestenliste),
mit 2× Sniper + 2× Tesla in der Tasche.Lob: WAVE-5er nur «Flawless!» ohne Lecks (sonst «Keep going!»), 100 Splats/Chomper/Mixer/Drehung ohne große Lob-Wörter."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V329";', 'const GAME_VER = "V330";')
rep('["Lucky Supply", "BANDIT · ONE FREE SPIN", 3, "bandit"]];',
    '["Lucky Supply", "BANDIT · ONE FREE SPIN", 3, "bandit"], ["Signal lost", "WAVE 65 · NO SIGNAL", 65, "blk"], ["Magnet", "WAVE 80", 80, "mag"], ["Weeds", "WAVE 90", 90, "weed"], ["Thief", "WAVE 100", 100, "thief"], ["Egg · S. America", "WAVE 2 · PUSH 3× INTO WALL", 2, "egg"], ["Egg · Africa", "WAVE 32", 32, "egg"], ["Egg · Asia", "WAVE 62", 62, "egg"], ["Egg · N. America", "WAVE 92", 92, "egg"], ["Egg · Antarctica", "WAVE 122", 122, "egg"]];')
rep('const o = ["lock", "hack", "chomp", "ton", "radio"].includes(k) ? 0 : specOff;', 'const o = ["lock", "hack", "chomp", "ton", "radio", "blk", "mag", "weed", "thief", "egg"].includes(k) ? 0 : specOff;')
rep('devJump(["lock", "hack", "chomp", "ton", "radio"].includes(k) ? w : w + specOff, k); });', 'devJump(["lock", "hack", "chomp", "ton", "radio", "blk", "mag", "weed", "thief", "egg"].includes(k) ? w : w + specOff, k); });')
# Martin 22:33: große Lob-Wörter nur für echte Leistung des Spielers, nicht für Automatik/Explosionen
rep('praise(`WAVE ${S.wave}!`, 4, S.wave >= 10 ? "Legendary!" : "Dominating!")', 'praise(`WAVE ${S.wave}!`, S.waveLeaks === 0 ? 3 : 2, S.waveLeaks === 0 ? "Flawless!" : "Keep going!")')
rep('praise("SPLATASTIC!", 4, "Splatastic!")', 'praise("100 SPLATS", 2, false)')
rep('praise("FEAST!", 3, "Splatastic!")', 'praise("FEAST!", 2, "Splat!")')
rep('praise("SEALED TIGHT!", 3, "Amazing!")', 'praise("SEALED TIGHT!", 2, "Sweet!")')
rep('setTimeout(() => SFX.say("Unbelievable!"), 1300)', 'setTimeout(() => SFX.say("Well done!"), 1300)')
rep('praise("UNSTOPPABLE!", 4, false)', 'praise("MEGA SPLAT!", 3, false)')
JS = r'''
/* V330: Test-Zugang Störungen + Easter Egg (Dev-Liste und ?test=…) */
try { (() => {
  const DK = ["blk", "mag", "weed", "thief", "egg"];
  const _dj = devJump; devJump = function (w, kind) { const r = _dj.apply(this, arguments);
    if (DK.includes(kind)) { S.snipes = (S.snipes || 0) + 2; S.teslas = (S.teslas || 0) + 2; S.waveCD = 3;
      if (kind === "egg") toast("TEST · EASTER EGG: push a block 3× into the left or right wall", "HQ", 3500);
      else toast(`TEST · ${kind.toUpperCase()} starts a few seconds into wave ${w} · 2 Sniper + 2 Tesla in Pocket`, "HQ", 3000); }
    return r; };
  let q = null; try { q = new URLSearchParams(location.search).get("test"); } catch (e) {}
  const map = { blk: 65, mag: 80, weed: 90, thief: 100, egg1: 2, egg2: 32, egg3: 62, egg4: 92, egg5: 122 };
  if (q && map[q]) { const go = () => { setTimeout(() => { try { history.replaceState(null, "", location.pathname); } catch (e) {} devJump(map[q], q.replace(/\d$/, "")); }, 700); };
    const sp = document.getElementById("splash"); if (sp) sp.addEventListener("click", go, { once: true }); else go(); }
})(); } catch (e) { console.error("v330", e); }
'''
anchor = '})();\n</script>'
p = s.rindex(anchor); s = s[:p] + JS + s[p:]
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
