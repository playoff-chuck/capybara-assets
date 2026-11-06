"""V331 (Martin 06.11. 22:28 «Sprüche ok», 22:33 «heygen ok»): 19 neue Sprüche von Rosie (frech) und Blue (ruhig),
mit Martins HeyGen-Stimme (voice/lines7.json, 45,9 s, 0,0153 $). Sprechblase wie bei buddyHelp (Partner-Bild + Name).
Regeln: höchstens 1 Spruch je 20 s, jeder Spruch höchstens alle 4 min, nie bei offenem Fenster (außer Kontinent-Ende/Spielende),
wartet bis zu 8 s, wenn gerade eine andere Stimme spricht."""
import sys, json, base64, os
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V330";', 'const GAME_VER = "V331";')
VD = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'voice')
L = json.load(open(os.path.join(VD, 'lines7.json'), encoding='utf-8'))
vt = ''.join(f'{json.dumps(k)}: {json.dumps(t)}, ' for k, t in L.items())
vb = ''.join(f'"{k}":"' + base64.b64encode(open(os.path.join(VD, k + '.mp3'), 'rb').read()).decode() + '",' for k in L)
rep('const VOICE_TEXT = {', 'const VOICE_TEXT = {' + vt)
rep('const VOICE = {', 'const VOICE = {' + vb)
JS = r'''
/* V331: Rosie & Blue sprechen */
try { (() => {
  const ROSIE_K = ["rb_room", "rb_ceiling", "rb_triple", "rb_four", "rb_fancy", "rb_bigone", "rb_byebig", "rb_pancake", "rb_bags"];
  let lastSay = -1e9, bT = 0; const lastKey = {};
  function bubble(key) { const el = document.getElementById("buddy"); if (!el) return; const who = ROSIE_K.includes(key) ? "rosie" : "blue";
    el.className = Math.random() < 0.5 ? "l" : "r"; el.querySelector("img").src = HERO_IMG[who];
    el.querySelector(".say").innerHTML = `${VOICE_TEXT[key]}<small>${who === "rosie" ? "ROSIE" : "BLUE"}</small>`;
    void el.offsetWidth; el.classList.add("on"); clearTimeout(bT); bT = setTimeout(() => el.classList.remove("on"), 2800); }
  function rbSay(key, delay = 0, force = false) {
    const t0 = performance.now() + delay;
    const tryIt = () => { const now = performance.now();
      if (!S || !S.started || (S.over && key !== "rb_tea")) return;
      if (now - (lastKey[key] || -1e9) < 240000) return;
      if (!force && now - lastSay < 20000) return;
      const busy = SFX.voiceBusy || (!force && (uiWinOpen() || S.paused || S.drop || S.intro || S.eggOpen || S.tiltCard));
      if (busy) { if (now - t0 < 8000) setTimeout(tryIt, 700); return; }
      lastSay = now; lastKey[key] = now; bubble(key); try { SFX.say(key); } catch (e) {} };
    setTimeout(tryIt, delay); }
  window.__rbSay = (k, f) => rbSay(k, 0, f);
  // Wellenstart: Stapel tief / hoch / normal
  const _sw = startWave; startWave = function () { const r = _sw.apply(this, arguments);
    try { if (!S.nuts) setTimeout(() => { if (!S.inWave) return; const h = stackHeight(); if (h >= 12) rbSay("rb_ceiling"); else if (h <= 4 && S.wave > 2) rbSay("rb_room"); else if (Math.random() < 0.3) rbSay("rb_steady"); }, 2500); } catch (e) {} return r; };
  // Linien
  let lastClear = performance.now();
  const _cl = clearLines; clearLines = function () { const r = _cl.apply(this, arguments); if (r) { lastClear = performance.now(); if (r === 3) rbSay("rb_triple", 1800); else if (r >= 4) rbSay("rb_four", 1800); } return r; };
  // Der Kiefer (großes Monster) kommt / fällt
  const _sm = spawnMonster; spawnMonster = function () { const n = S.monsters.length; const r = _sm.apply(this, arguments); try { const m = S.monsters[S.monsters.length - 1]; if (S.monsters.length > n && m && m.kind === "kiefer") rbSay("rb_bigone", 600); } catch (e) {} return r; };
  const _km = killMilestones; killMilestones = function (m) { const r = _km.apply(this, arguments); try { if (m && m.kind === "kiefer") rbSay("rb_byebig", 900); } catch (e) {} return r; };
  // Ten-ton
  const _pr = praise; praise = function (text) { const r = _pr.apply(this, arguments); if (text === "SQUASHED!") rbSay("rb_pancake", 1900); return r; };
  // Kontinent geschafft
  const _ss = showSign; showSign = function (c) { if (window.__celFor !== S.wave) rbSay("rb_bags", 1500, true); return _ss.apply(this, arguments); };
  // Leben verloren
  const _lk = leak; leak = function (m) { const r = _lk.apply(this, arguments); try { if (S.lives > 0 && S.lives <= 3 && !S.rbBreath) { S.rbBreath = 1; rbSay("rb_breath", 700); } else if (S.lives > 3) rbSay("rb_slipped", 700); } catch (e) {} return r; };
  // Neue Waffe
  const _au = announceUnlocks; announceUnlocks = function (w) { try { if (Object.keys(UNLOCK_NAME).some(k => unlockedAt(k) === w && w > 1)) rbSay("rb_newtoy", 3500); } catch (e) {} return _au.apply(this, arguments); };
  // Sichtbehinderung
  const _an = announce; announce = function (title) { try { if (/SIGNAL LOST|SIBERIA|BLIZZARD|WHITEOUT|SANDSTORM|FOG/i.test(String(title))) rbSay("rb_trust", 3000); } catch (e) {} return _an.apply(this, arguments); };
  // Spielende
  const _go = gameOver; gameOver = function () { const was = S && !S.over; const r = _go.apply(this, arguments); if (was && !S.won) rbSay("rb_tea", 1800, true); return r; };
  // Laufende Beobachtung: Gold, Elite-Turm, lange keine Linie, Tasche voll, Welle ohne Treffer
  let wasIn = false, goldHi = 0, eliteSeen = false;
  setInterval(() => { try {
    if (!S || !S.started || S.over || frozen()) { if (S && !S.started) { goldHi = 0; eliteSeen = false; } return; }
    if (S.gold >= 1000 && goldHi < 1000) rbSay("rb_loaded", 800); goldHi = S.gold;
    let el = false; for (const t of S.towers.values()) if (t.w && t.w.some(w => w.lvl >= 4)) el = true;
    if (el && !eliteSeen) rbSay("rb_fancy", 600); eliteSeen = el;
    if (S.inWave && performance.now() - lastClear > 60000) { rbSay("rb_anyline"); lastClear = performance.now(); }
    if (!S.inWave) lastClear = performance.now();
    if (S.inWave && ((S.snipes | 0) + (S.teslas | 0) + (S.mixers | 0) + (S.chomps | 0) + (S.tons | 0) + (S.locks | 0)) >= 6) rbSay("rb_pocket", 1500);
    if (wasIn && !S.inWave && S.waveLeaks === 0 && S.wave >= 3 && Math.random() < 0.4) rbSay("rb_scratch", 2600);
    wasIn = S.inWave;
  } catch (e) {} }, 500);
})(); } catch (e) { console.error("v331", e); }
'''
anchor = '})();\n</script>'
p = s.rindex(anchor); s = s[:p] + JS + s[p:]
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
