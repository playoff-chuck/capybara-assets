#!/usr/bin/env python3
"""Baut die Schlüsselliste der Sprachschicht: gesehene Texte (i18n_crawl keys.json) + statische Literale aus site/index.html.
Zahlen werden zu «#», bekannte Namen (Orte, Kontinente, Monster, Waffen) in Mustern zu «@».
Aufruf: python3 tools/i18n_keys.py site/index.html crawl/keys.json site/lang/en.json [weitere keys.json …]
Schreibt en.json (Identität) und gibt die Zahl der Schlüssel aus. Bestehende Einträge anderer Sprachen bleiben unberührt."""
import sys, re, json, html as H
src, out = sys.argv[1], sys.argv[3]; crawls = [sys.argv[2]] + sys.argv[4:]
s = open(src, encoding="utf-8").read()
NUM = re.compile(r"\d[\d.,:/]*\d|\d")
WS = re.compile(r"\s+")
def norm(t): return WS.sub(" ", H.unescape(re.sub(r"\{[nv]\}", "#", str(t)).replace("{p}", "@"))).strip()
def ok(t):
    if not t or len(t) < 2 or len(t) > 240: return False
    if not re.search(r"[A-Za-zÀ-ÿ]{2}", t): return False
    if re.search(r"(img|bg|sign|sfx|music|lang|icons|fonts)/|\.(webp|png|mp3|json|svg|js|css|html)\b|https?:|rgba?\(|px\b|#[0-9a-f]{3,8}\b|\b(var|const|let|function|return|document|window|localStorage|classList|querySelector|addEventListener|innerHTML|textContent|setTimeout|data-|aria-)\b|[{};<>=]|^\s*[\w-]+\s*:\s*[\w-]+\s*$", t): return False
    if re.match(r"^[.#\[]|^[a-z]+[A-Z]|^[a-z_]+\d*$|\\u|^[\w-]+\s+\.[\w-]+", t): return False   # Selektoren, camelCase, Bezeichner
    if re.search(r"\w\(|\)\.|\|\||&&|=>|/g\b|cubic-bezier|\d+ms\b|^\W*[,)]|\bString\(|toLocale|padStart|replace\(", t): return False   # Code-Reste
    if " " not in t and not re.fullmatch(r"[A-Z][A-Za-z'’\-]+!?|[A-Z][A-Z'’\-]+!?|[A-Z][a-z]+[A-Z][a-z]+", t): return False   # Einzelwort nur Title-/GROSS
    if re.fullmatch(r"[A-Z][a-z]+[A-Z][a-z]+", t): return False
    if re.search(r"\b(true|false|null|undefined|none|auto|block|flex|hidden|visible|absolute|relative|center|left|right|top|bottom)\b", t) and " " not in t: return False
    return True
keys = set()
# 1 gesehene Texte
for f in crawls:
    try:
        for k in json.load(open(f, encoding="utf-8")):
            k = norm(k)
            if k and len(k) <= 300 and re.search(r"[A-Za-zÀ-ÿ]{2}", k) and not re.search(r"\\u|[{}<>]", k): keys.add(k); keys.add(NUM.sub("#", k))   # gesehene Texte gelten immer
    except Exception as e: print("warn", f, e)
# 2 statische Texte im HTML (Textknoten zwischen Tags, ohne Script/Style)
body = re.sub(r"<script[\s\S]*?</script>|<style[\s\S]*?</style>", " ", s)
for m in re.finditer(r">([^<>]{2,240})<", body):
    k = norm(m.group(1))
    if ok(k): keys.add(k)
for m in re.finditer(r'(?:placeholder|aria-label|title)="([^"]{2,160})"', body):
    k = norm(m.group(1))
    if ok(k): keys.add(k)
# 3 String-Literale im Script: "…" und `…` (Templates: ${…} → #)
scripts = "\n".join(re.findall(r"<script[^>]*>([\s\S]*?)</script>", s))
for m in re.finditer(r'"((?:[^"\\\n]|\\.){2,240})"', scripts):
    k = norm(re.sub(r"\\u([0-9a-fA-F]{4})", lambda mm: chr(int(mm.group(1), 16)), m.group(1)).replace('\\"', '"').replace("\\n", " "))
    if ok(k) and re.search(r"[A-Z]|[a-z]+ [a-z]+", k): keys.add(k)
for m in re.finditer(r'"([^"\n]{1,240})"', scripts):
    k = norm(re.sub(r"\\u([0-9a-fA-F]{4})", lambda mm: chr(int(mm.group(1), 16)), m.group(1)))
    if ok(k) and re.search(r"[A-Z]|[a-z]+ [a-z]+", k): keys.add(k)
for m in re.finditer(r"`((?:[^`\\]|\\.){2,400})`", scripts):
    raw = m.group(1)
    if "<" in raw and ">" in raw:   # HTML-Template: Textknoten herausziehen
        for t in re.finditer(r">([^<>]{2,240})<", raw):
            k = norm(re.sub(r"\$\{[^}]*\}", "#", t.group(1)))
            if ok(k): keys.add(k)
        for t in re.finditer(r'(?:placeholder|aria-label|title)="([^"]{2,160})"', raw):
            k = norm(re.sub(r"\$\{[^}]*\}", "#", t.group(1)))
            if ok(k): keys.add(k)
    else:
        k = norm(re.sub(r"\$\{[^}]*\}", "#", raw))
        if ok(k) and re.search(r"[A-Z]|[a-z]+ [a-z]+", k): keys.add(k)
# 3b Platzhalter {n}/{v} → #, {p} → @
for k in list(keys):
    if "{" in k: keys.add(re.sub(r"\{[nv]\}", "#", k).replace("{p}", "@"))
# 4 Muster «#» für alles mit Zahlen, zusätzlich «@»-Muster für Namen
names = set()
for m in re.finditer(r'const CONTS = (\[[\s\S]*?\]\]\]);', s):
    try:
        for c in json.loads(m.group(1)): names.add(c[1]); names.update(c[2])
    except Exception: pass
for m in re.finditer(r'const MON_INFO = (\[[\s\S]*?\]\]);', s):
    try:
        for x in json.loads(m.group(1)): names.add(x[1])
    except Exception: pass
nice = lambda t: t.lower().title()
names |= {nice(n) for n in list(names)} | {n.title() for n in list(names)}
names |= {"Sniper strike", "Concrete mixer", "Tesla storm", "Chomper", "Ten-ton drop", "Lockdown", "Wolf call", "MG", "Cannon", "Frost", "Elite tower", "Rosie", "Blue"}
names = {n for n in names if len(n) >= 3}
extra = set()
for k in list(keys):
    if NUM.search(k): extra.add(NUM.sub("#", k))
    if k in names: continue
    for n in sorted(names, key=len, reverse=True):
        if n in k and n != k and re.search(r"(^|[^A-Za-z])" + re.escape(n) + r"($|[^A-Za-z])", k): extra.add(k.replace(n, "@")); break
keys |= extra | names
# bisherige Übersetzungen anderer Sprachen bleiben; en.json = Identität
keys = sorted(keys)
json.dump({k: k for k in keys}, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
json.dump(sorted(names), open(out.replace("en.json", "names.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print("keys", len(keys), "names", len(names))
