"""V304 (To-do 17): fehlende Sprachclips in Martins Stimme (HeyGen, voice/lines6.json, 0,0034 $):
«Like this?» (Lautstärke-Regler), «Full salvo!» und 4 Air-Drop-Sprüche; die Air-Drop-Karte spricht beim Erscheinen."""
import sys, json, base64
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V303";', 'const GAME_VER = "V304";')
L = json.load(open('/srv/capy-assets/voice/lines6.json'))
vt = ''.join(f'{json.dumps(k)}: {json.dumps(t)}, ' for k, t in L.items())
vb = ''.join(f'"{k}":"' + base64.b64encode(open(f'/srv/capy-assets/voice/{k}.mp3', 'rb').read()).decode() + '",' for k in L)
rep('const VOICE_TEXT = {', 'const VOICE_TEXT = {' + vt)
rep('const VOICE = {', 'const VOICE = {' + vb)
rep('try { snd("crate"); if (kind === "sweep" || kind === "ton")',
    'try { const vl = { ton: "ad_drop", sweep: "ad_sweep", med: "ad_med", rot: "ad_upright" }[kind]; if (vl) setTimeout(() => { try { if (!ov.hidden) SFX.say(vl, 1.0, 1.0, 0, 0); } catch (e) {} }, 700); } catch (e) {}\n      try { snd("crate"); if (kind === "sweep" || kind === "ton")')
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
