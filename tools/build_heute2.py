"""Baut «Capybara Squad · Heute» (Version 2) aus heute_tpl.html (CSS) + heute_body2.html + Daten.
Aufruf: python3 build_heute2.py <alte_seite.html> <daten.json> <out.html>
Die alte Seite liefert Berichte/Kurven/Einschätzung; daten.json ergänzt meta, tasks, Vorschläge je Bericht."""
import json, re, sys
old_page, data_path, out = sys.argv[1:4]
tpl = open('heute_tpl.html', encoding='utf-8').read()
head = tpl[:tpl.find('</style>') + len('</style>')] + '\n'
body = open('heute_body2.html', encoding='utf-8').read()
s = open(old_page, encoding='utf-8').read()
m = re.search(r"const D = (\{.*?\});\n", s, re.S)
old = json.loads(m.group(1))
new = json.load(open(data_path, encoding='utf-8'))
reps = {r['id']: r for r in old['reports']}
for r in new.get('reports', []):
    reps[r['id']] = dict(reps.get(r['id'], {}), **r)
# Vorschläge des V181-Berichts = alte Diagramm-Punkte
v181 = reps.get('r20261104_1142')
if v181 is not None and not v181.get('props'):
    v181['props'] = [dict(p, chart='main') for p in old['mainMarks']] + [dict(p, chart='nuts', n=len(old['mainMarks']) + p['n']) for p in old['nutsMarks']]
D = dict(meta=new['meta'], tasks=new['tasks'], reports=sorted(reps.values(), key=lambda r: r['at'], reverse=True), rates=new.get('rates', []))
html = head + body.replace('/*DATA*/null', json.dumps(D, ensure_ascii=False))
open(out, 'w', encoding='utf-8').write(html)
print('ok', out, len(html))
