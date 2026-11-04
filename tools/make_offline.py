"""Schreibt site/offline.json: alle Spieldateien (Pfad, Größe) für den Offline-Speicher (sw.js). Vor jedem Deploy laufen lassen."""
import os, json, re, sys
root = sys.argv[1] if len(sys.argv) > 1 else 'site'
html = open(os.path.join(root, 'index.html'), encoding='utf-8').read()
ver = re.search(r'const GAME_VER = "(V\d+)"', html).group(1)
skip = {'index.html', 'sw.js', 'offline.json'}
files = []
for d, _, fs in os.walk(root):
    for f in fs:
        p = os.path.relpath(os.path.join(d, f), root).replace(os.sep, '/')
        if p in skip or p.startswith('logos/') or f.startswith('.'): continue
        files.append({'p': p, 's': os.path.getsize(os.path.join(d, f))})
# Dateien, die das Spiel mit ?v= lädt, auch so speichern
for m in set(re.findall(r'"((?:img|bg|music|sfx|intro|sign|fin)/[^"?]+)\?v=(\d+)"', html)):
    files.append({'p': m[0], 's': 0, 'v': m[1]})
files.sort(key=lambda x: (x['p'].startswith('music/'), x['p']))
json.dump({'ver': ver, 'files': files}, open(os.path.join(root, 'offline.json'), 'w'), separators=(',', ':'))
print(ver, len(files), sum(f['s'] for f in files) // 1024 // 1024, 'MB')
