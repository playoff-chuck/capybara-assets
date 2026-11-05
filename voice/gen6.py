import json, subprocess, urllib.request, os, sys
K = open('/etc/splatsquad/heygen.key').read().strip(); V = sys.argv[1]; D = '/srv/capy-assets/voice'
L = json.load(open(D + '/lines6.json')); tot = 0
for k, txt in L.items():
    out = f'{D}/{k}.mp3'
    if os.path.exists(out): continue
    req = urllib.request.Request('https://api.heygen.com/v3/voices/speech', data=json.dumps({'text': txt, 'voice_id': V}).encode(), headers={'X-API-KEY': K, 'Content-Type': 'application/json'})
    try:
        d = json.load(urllib.request.urlopen(req, timeout=60))['data']; tot += d.get('duration', 0)
        urllib.request.urlretrieve(d['audio_url'], f'/tmp/{k}.wav')
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'/tmp/{k}.wav', '-af', 'silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,loudnorm=I=-17:TP=-1.5', '-ac', '1', '-ar', '44100', '-b:a', '64k', out], check=True)
        print('ok', k, round(d.get('duration', 0), 2), flush=True)
    except Exception as e: print('ERR', k, e, flush=True)
print('total_s', round(tot, 1), 'cost_usd', round(tot * 0.000333, 4))
