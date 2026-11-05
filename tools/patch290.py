"""V290 (Martin 17:26–17:29):
- 10 motivierende «Incoming»-Sprüche in Martins Stimme (HeyGen «Martin 4min», voice/inc_m1–10.mp3, 0,0067 $; inc_m7 Pause um 0,18 s gekürzt).
  Am Wellenstart kommt weiter nur in ~20 % der Wellen ein Spruch; davon die Hälfte einer der neuen, die andere Hälfte wie bisher «Incoming! …».
- Neuer Kontinent: Türme ziehen nicht mehr mit, sie werden zum vollen Preis verkauft; der General meldet «TOWERS SOLD · +X GOLD»
  («New continent, fresh start: n towers sold at full price. The gold is in your account.»).
Aufruf: patch290.py src dst <voice-Ordner>"""
import sys, base64, os
src, dst, vd = sys.argv[1], sys.argv[2], sys.argv[3]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V289";', 'const GAME_VER = "V290";')
T = {"inc_m1": "Here they come, we've got this!", "inc_m2": "Stay sharp, squad!", "inc_m3": "Show them what we've got!", "inc_m4": "Bring it on!", "inc_m5": "Ready, set, splat!", "inc_m6": "Together we're unstoppable!", "inc_m7": "Let's make this wave count!", "inc_m8": "Keep calm and splat on!", "inc_m9": "You were born for this!", "inc_m10": "Another wave, another win!"}
import json
vt = ", ".join(json.dumps(k) + ": " + json.dumps(v) for k, v in T.items()) + ", "
vb = ",".join(json.dumps(k) + ":" + json.dumps(base64.b64encode(open(os.path.join(vd, k + ".mp3"), "rb").read()).decode()) for k in T) + ","
rep('const VOICE_TEXT = {', 'const VOICE_TEXT = {' + vt)
rep('const VOICE = {', 'const VOICE = {' + vb)
rep('if (!S.introNow && Math.random() < 0.2) setTimeout(() => SFX.say(S.incomingKey || "Incoming!"), 1300);',
    'if (!S.introNow && Math.random() < 0.2) { const mk = Math.random() < 0.5 ? "inc_m" + (1 + Math.floor(Math.random() * 10)) : (S.incomingKey || "Incoming!"); setTimeout(() => SFX.say(mk), 1300); }')
rep('  window.__contFresh = () => { if (!S) return; const keep = [...S.towers.values()].sort((a, b) => a.x - b.x);\n    S.grid = new Uint8Array(NN); S.towers = new Map(); seedGarbage();\n    const used = new Set();\n    for (const t of keep) { let x = Math.max(1, Math.min(GW - 2, t.x)); for (let k = 0; k < GW && used.has(x); k++) x = x >= GW - 2 ? 1 : x + 1; used.add(x);\n      let y = GH - 1; while (y > 0 && S.grid[y * GW + x]) y--; S.grid[y * GW + x] = 1 + (t.id % 7); t.x = x; t.y = y; S.towers.set(y * GW + x, t); }\n    S.monsters = []; S.shots = []; try { gridChanged(); } catch (e) { S.dirty = true; } };', '  window.__contFresh = () => { if (!S) return; let sum = 0, n = 0; for (const t of S.towers.values()) { sum += towerValue(t); n++; }   /* V290: Türme werden zum vollen Preis verkauft */\n    S.grid = new Uint8Array(NN); S.towers = new Map(); seedGarbage(); try { if (S.sel) closeSheet(); } catch (e) {}\n    S.monsters = []; S.shots = []; try { gridChanged(); } catch (e) { S.dirty = true; }\n    if (n) { S.gold += sum; announce(`TOWERS SOLD · +${sum} GOLD`, `New continent, fresh start: ${n} tower${n > 1 ? "s" : ""} sold at full price. The gold is in your account.`, "HQ", 6500); } };')
open(dst, 'w', encoding='utf-8').write(s)
