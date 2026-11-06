"""V345 (Martin 07.11. 00:05): Dieb grüßt beim Erscheinen in derselben tiefen Stimme: «Hello... I'm just looking.» (HeyGen 0,0007 $),
statt «Hold the line!»."""
import sys, base64, os, json
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V344";', 'const GAME_VER = "V345";')
VD = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'voice')
b = base64.b64encode(open(os.path.join(VD, 'thief_hello.mp3'), 'rb').read()).decode()
rep('const VOICE_TEXT = {', 'const VOICE_TEXT = {' + json.dumps("thief_hello") + ': ' + json.dumps("Hello... I'm just looking.") + ', ')
rep('const VOICE = {', 'const VOICE = {"thief_hello":"' + b + '",')
rep('if (k === "thief") setTimeout(() => SFX.say("Hold the line!"), 700);', 'if (k === "thief") setTimeout(() => { try { SFX.say("thief_hello", 1.0, 1.0, 0, 0); } catch (e) {} }, 900);')
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
