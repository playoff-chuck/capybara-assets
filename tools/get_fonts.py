"""Schriften selbst hosten (statt Google Fonts live): lädt die woff2-Dateien (nur latin + latin-ext) nach site/fonts/
und schreibt tools/fonts.css mit @font-face-Regeln (relative Pfade fonts/…). Alle vier Schriften stehen unter der
SIL Open Font License. Aufruf: python3 tools/get_fonts.py <google-css-datei>"""
import re, sys, os, urllib.request
css = open(sys.argv[1], encoding='utf-8').read()
os.makedirs('site/fonts', exist_ok=True)
blocks = re.findall(r'/\* ([a-z-]+) \*/\s*@font-face \{(.*?)\}', css, re.S)
out, seen, files = [], {}, {}
for subset, body in blocks:
    if subset not in ('latin', 'latin-ext'): continue
    fam = re.search(r"font-family: '([^']+)'", body).group(1)
    wght = re.search(r'font-weight: (\d+)', body).group(1)
    url = re.search(r'url\((https://fonts\.gstatic\.com/[^)]+\.woff2)\)', body).group(1)
    rng = re.search(r'unicode-range: ([^;]+);', body).group(1)
    key = (fam, subset, url)
    if key in seen: seen[key].append(wght); continue
    seen[key] = [wght]
for (fam, subset, url), ws in seen.items():
    slug = fam.lower().replace(' ', '')
    name = f"{slug}-{'var' if len(ws) > 1 else ws[0]}-{subset}.woff2"
    path = os.path.join('site/fonts', name)
    if not os.path.exists(path):
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        open(path, 'wb').write(urllib.request.urlopen(req, timeout=30).read())
    files[name] = os.path.getsize(path)
    body = [b for s, b in blocks if s == subset and url in b][0]
    rng = re.search(r'unicode-range: ([^;]+);', body).group(1).replace(' ', '')
    w = f"{min(ws)} {max(ws)}" if len(ws) > 1 else ws[0]
    out.append(f"@font-face{{font-family:'{fam}';font-style:normal;font-weight:{w};font-display:swap;src:url(fonts/{name}) format('woff2');unicode-range:{rng}}}")
open('tools/fonts.css', 'w', encoding='utf-8').write('\n'.join(out) + '\n')
for n, s in sorted(files.items()): print(n, s)
print(len(out), 'rules', sum(files.values()) // 1024, 'KB')
