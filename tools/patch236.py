"""V236: Sprachclips mit angehängtem abgebrochenem Wort gekürzt (z. B. «Excellent! Ex–»). Betroffen laut Analyse
(letztes kurzes Stück klingt wie der Anfang): wave4 «Excellent!», rich «Rich!», jackpot «Jackpot!», muncher
«Muncher down!», boom «Boom!». Schnitt in der ersten Pause nach dem Wort (+90 ms) mit 60 ms Ausblenden – die Clips enthielten das Wort 2–3×."""
import sys, re, json, base64, subprocess, numpy as np
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
s = s.replace('const GAME_VER = "V235";', 'const GAME_VER = "V236";', 1); assert 'GAME_VER = "V236"' in s
FIX = ['wave4', 'rich', 'jackpot', 'muncher', 'boom']
a = s.index('const VOICE = '); e = s.index('};', a) + 1
d = json.loads(s[a + len('const VOICE = '):e])
def pcm(path):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768
for k in FIX:
    v = d[k]; b = v[0] if isinstance(v, list) else v
    open('/tmp/in.mp3', 'wb').write(base64.b64decode(b)); x = pcm('/tmp/in.mp3'); sr = 16000
    o = subprocess.run(['ffmpeg', '-hide_banner', '-i', '/tmp/in.mp3', '-af', 'silencedetect=n=-38dB:d=0.08', '-f', 'null', '-'], capture_output=True, text=True).stderr
    cut = float(re.findall(r'silence_start: ([\d.]+)', o)[0]) + 0.09   # nach dem ersten Wort, vor der Wiederholung
    info = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'stream=bit_rate,sample_rate,channels', '-of', 'json', '/tmp/in.mp3'], capture_output=True, text=True).stdout)['streams'][0]
    br = str(max(32, int(info.get('bit_rate', 64000)) // 1000)) + 'k'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', '/tmp/in.mp3', '-t', f'{cut:.3f}', '-af', f'afade=t=out:st={max(0, cut - 0.06):.3f}:d=0.06',
                    '-ar', str(info.get('sample_rate', 44100)), '-ac', str(info.get('channels', 1)), '-b:a', br, '/tmp/out.mp3'], check=True)
    nb = base64.b64encode(open('/tmp/out.mp3', 'rb').read()).decode()
    assert s.count(b) == 1, (k, s.count(b)); s = s.replace(b, nb)
    print(k, f'{len(x)/sr:.2f}s -> {cut:.2f}s')
open(dst, 'w', encoding='utf-8').write(s); print('ok')
