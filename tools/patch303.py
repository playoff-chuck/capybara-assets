"""V303 (To-do 18): Lautstärke angleichen.
Gemessen (EBU R128): Musik Südamerika ≈ −18 LUFS, Afrika/Asien ≈ −13 LUFS (5 dB lauter → auf neuen Kontinenten
so laut wie die Stimme). Sprachclips −21,5 … −13,8 LUFS.
1) Alle Musikdateien linear auf −20 LUFS (nur leiser, Dynamik bleibt), AAC neu kodiert.
2) Sprachclips, die mehr als 1,5 LU von −17 LUFS abweichen, auf −17 LUFS (beim Anheben Spitzen weich auf −1 dBFS begrenzt);
   Clips unter 0,5 s bleiben unverändert (nicht messbar).
Aufruf: python3 tools/patch303.py site/index.html site/index.html  (arbeitet im Ordner neben index.html)"""
import sys, os, re, base64, subprocess, tempfile, json
src, dst = sys.argv[1], sys.argv[2]
root = os.path.dirname(os.path.abspath(src))
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V302";', 'const GAME_VER = "V303";')

def meas(path):
    o = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', path, '-af', 'ebur128=peak=sample', '-f', 'null', '-'], capture_output=True, text=True).stderr
    i = re.findall(r'I:\s+(-?[\d.]+) LUFS', o); p = re.findall(r'Peak:\s+(-?[\d.]+) dBFS', o)
    return (float(i[-1]) if i else None), (float(p[-1]) if p else None)
def dur(path):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path], capture_output=True, text=True).stdout.strip() or 0)
def br(path):
    o = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'a:0', '-show_entries', 'stream=bit_rate,sample_rate,channels', '-of', 'json', path], capture_output=True, text=True).stdout
    st = json.loads(o)['streams'][0]; return int(st.get('bit_rate') or 96000), st.get('sample_rate'), st.get('channels')

report = []
# 1) Musik
MUSIC_T = -20.0
mdir = os.path.join(root, 'music')
for f in sorted(os.listdir(mdir)):
    if not f.endswith('.mp4'): continue
    p = os.path.join(mdir, f); L, pk = meas(p)
    if L is None: continue
    g = round(MUSIC_T - L, 1)
    if g > -0.5:
        report.append(f'music {f}: {L} LUFS – bleibt'); continue
    b, sr, ch = br(p); tmp = p + '.tmp.mp4'
    subprocess.run(['ffmpeg', '-y', '-hide_banner', '-loglevel', 'error', '-i', p, '-vn', '-af', f'volume={g}dB', '-c:a', 'aac', '-b:a', str(max(96000, b)), '-movflags', '+faststart', tmp], check=True)
    os.replace(tmp, p); L2, _ = meas(p)
    report.append(f'music {f}: {L} → {L2} LUFS ({g:+} dB)')

# 2) Stimme
VOICE_T = -17.0
i = s.index('const VOICE = {'); j = s.index('};', i)
block = s[i:j]
td = tempfile.mkdtemp()
def fix(m):
    k, b64 = m.group(1), m.group(2)
    a = os.path.join(td, 'a.mp3'); open(a, 'wb').write(base64.b64decode(b64))
    if dur(a) < 0.5: return m.group(0)
    L, pk = meas(a)
    if L is None or abs(L - VOICE_T) <= 1.5: return m.group(0)
    g = round(VOICE_T - L, 1)
    af = f'volume={g}dB' + (',alimiter=limit=0.89:level=false:attack=2:release=40' if g > 0 else '')   # lauter machen: Spitzen weich auf −1 dBFS begrenzen
    bb, sr, ch = br(a); o = os.path.join(td, 'o.mp3')
    subprocess.run(['ffmpeg', '-y', '-hide_banner', '-loglevel', 'error', '-i', a, '-af', af, '-c:a', 'libmp3lame', '-b:a', str(bb), '-ar', str(sr), '-ac', str(ch), o], check=True)
    L2, _ = meas(o); report.append(f'voice {k}: {L} → {L2} LUFS ({g:+} dB)')
    return f'"{k}":"{base64.b64encode(open(o, "rb").read()).decode()}"'
block2 = re.sub(r'"([^"]+)":"([A-Za-z0-9+/=]{200,})"', fix, block)
s = s[:i] + block2 + s[j:]
open(dst, 'w', encoding='utf-8').write(s)
print('\n'.join(report)); print("ok")
