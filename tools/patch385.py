"""V385: Sprachclips und Klang-Samples aus index.html auslagern (Offen Claude «Sprachclips auslagern").
VOICE (~2 MB Base64) und SAMPLES (~0,25 MB) stehen jetzt in site/sfx/voice.json (?v=<Version>), index.html wird
~2,2 MB kleiner (schnellerer Start, index.html laedt bei jedem Start uebers Netz). Der Offline-Speicher (sw.js) nimmt
voice.json ueber offline.json mit. Inline bleiben `const VOICE = {};` und `const SAMPLES = {};` – spaetere Patches,
die 'const VOICE = {' ersetzen, funktionieren weiter (Inline-Eintraege haben Vorrang vor voice.json).
Aufruf: python3 tools/patch385.py site/index.html site/index.html  (schreibt zusaetzlich site/sfx/voice.json)"""
import re, sys, json, os
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
m = re.search(r'const GAME_VER = "V(\d+)";', s); old = int(m.group(1)); NEW = old + 1
rep(f'const GAME_VER = "V{old}";', f'const GAME_VER = "V{NEW}";')

mv = list(re.finditer(r'^const VOICE = (\{"[^\n]*\});$', s, re.M)); assert len(mv) == 1, len(mv)
ms = list(re.finditer(r'^const SAMPLES = (\{"[^\n]*\});$', s, re.M)); assert len(ms) == 1, len(ms)
V = json.loads(mv[0].group(1)); SM = json.loads(ms[0].group(1))
for k in ("firstblood", "brutal", "massacre"): V.pop(k, None)   # werden ohnehin geloescht
out = os.path.join(os.path.dirname(dst), 'sfx', 'voice.json')
json.dump({"v": V, "s": SM}, open(out, 'w', encoding='utf-8'), separators=(',', ':'))
loader = ('const SAMPLES = {};\n'
  '/* V%d: Sprachclips + Samples aus sfx/voice.json (Inline-Eintraege in VOICE/SAMPLES haben Vorrang) */\n'
  '(function loadVoice(n) { fetch("sfx/voice.json?v=%d").then(r => { if (!r.ok) throw 0; return r.json(); }).then(d => {'
  ' for (const k in d.s) if (!(k in SAMPLES)) SAMPLES[k] = d.s[k]; for (const k in d.v) if (!(k in VOICE)) VOICE[k] = d.v[k];'
  ' ["firstblood", "brutal", "massacre"].forEach(k => { delete VOICE[k]; }); window.__voiceReady = Object.keys(VOICE).length;'
  ' try { window.__decAudio && window.__decAudio(); } catch (e) {} }).catch(() => { if (n < 5) setTimeout(() => loadVoice(n + 1), 2500 * (n + 1)); }); })(0);') % (NEW, NEW)
s = s[:ms[0].start()] + loader + s[ms[0].end():]
s = s[:mv[0].start()] + 'const VOICE = {};' + s[mv[0].end():]
# decodeAll: bereits dekodierte Eintraege ueberspringen, nachladbar machen
rep('''    for (const [name, list] of Object.entries(all)) {
      BUF[name] = [];''', '''    for (const [name, list] of Object.entries(all)) {
      if (BUF[name] && BUF[name].__src === list[0]) continue;
      BUF[name] = []; BUF[name].__src = list[0];''')
rep('''  function pickVoice() {''', '''  window.__decAudio = () => { if (ac) decodeAll(); };   /* V385 */
  function pickVoice() {''')
open(dst, 'w', encoding='utf-8').write(s)
print('V%d' % NEW, 'voice.json', os.path.getsize(out) // 1024, 'KB', 'index', len(s.encode()) // 1024, 'KB')
