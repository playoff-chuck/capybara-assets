"""V285 (Martin 17:06): Verwundet-Welle neu: «I'm losing control!» → «I can barely see!» → «Ouch! Someone needs a hug!»,
der Funk wird mit jeder Meldung schlechter, danach bricht die Verbindung ab (Rauschen). Statt Mayday + 4× Hug + «seeing double».
Zwei neue Clips in Martins Stimme (HeyGen «Martin 4min», voice/lostctrl.mp3 1,2 s, voice/barelysee.mp3 0,8 s, 0,0009 $).
Aufruf: patch285.py src dst lostctrl.mp3 barelysee.mp3"""
import sys, base64
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V284";', 'const GAME_VER = "V285";')
b1 = base64.b64encode(open(sys.argv[3], 'rb').read()).decode(); b2 = base64.b64encode(open(sys.argv[4], 'rb').read()).decode()
rep('const VOICE_TEXT = {', 'const VOICE_TEXT = {"lostctrl": "I\'m losing control!", "barelysee": "I can barely see!", ')
rep('const VOICE = {', 'const VOICE = {"lostctrl":"' + b1 + '","barelysee":"' + b2 + '",')
rep('    { const vk = SFX.hasVoice("wounded") ? "wounded" : "br_ouch", gap = SFX.voiceDur(vk) + 0.6; let at = 0.9;\n      if (SFX.hasVoice("mayday")) { setTimeout(() => { if (woundOn()) SFX.say("mayday", 1, 1, SFX.reserveVoice(SFX.voiceDur("mayday") * 1000 + 500)); }, 600); at += SFX.voiceDur("mayday") + 0.8; }   // Platzhalter «Ouch!», bis «Soldier wounded!» aufgenommen ist\n      for (let i = 0; i < 4; i++, at += gap) setTimeout(() => { if (!woundOn()) return; const k = SFX.reserveVoice(gap * 1000); SFX.say(vk, 1.0, 1.0, k, i); }, at * 1000);\n      setTimeout(() => { if (woundOn()) SFX.say("hurt2"); }, (at + 3) * 1000); setTimeout(() => { if (woundOn()) SFX.say("medsoon"); }, (at + 22) * 1000); }', '    { const seq = ["lostctrl", "barelysee", "wounded"].filter(k => SFX.hasVoice(k)); let at = 0.9;   /* V285: 2× schlechte Sicht, dann Hug, Funk wird mit jeder Meldung schlechter */\n      seq.forEach((vk, i) => { const d = SFX.voiceDur(vk) + 0.7, t = at; setTimeout(() => { if (!woundOn()) return; SFX.say(vk, 1.0, 1.0, SFX.reserveVoice(d * 1000), i); }, t * 1000); at += d; });\n      setTimeout(() => { if (woundOn()) snd("radio"); }, (at + 0.2) * 1000); setTimeout(() => { if (woundOn()) SFX.say("medsoon"); }, (at + 22) * 1000); }')
open(dst, 'w', encoding='utf-8').write(s)
