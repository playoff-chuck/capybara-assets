#!/usr/bin/env python3
# V559: Service Worker lieferte alte Sprachdateien (lang/ru.json?v=ALT über ignoreSearch) → neue Übersetzungen kamen auf Handys nicht an
# (Martins Video 10.11. 16:02: «НАЖМИ НА БАШНЮ», «ПРИМЕНИТЬ», «Hold a weapon…» trotz V557).
# Jetzt: Anfrage mit ?v=… → nur genau diese Fassung aus dem Speicher, sonst Netz; ältere Fassung nur, wenn offline.
import sys
src, dst, swsrc, swdst = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V558";', 'const GAME_VER = "V559";')
open(dst, "w", encoding="utf-8").write(s)
s = open(swsrc, encoding="utf-8").read()
rep('''    let hit = await c.match(key) || await c.match(key, { ignoreSearch: true });
    if (hit) return ranged(req, hit);
    try { const res = await fetch(new Request(key, { cache: "no-cache" })); if (res.ok && res.status === 200) { c.put(key, res.clone()); return ranged(req, res); } return res; } catch (er) { return Response.error(); } })());''',
'''    const strict = !!u.search;   /* V559: versionierte Anfrage (?v=) → keine ältere Fassung aus dem Speicher, außer offline */
    let hit = await c.match(key) || (strict ? null : await c.match(key, { ignoreSearch: true }));
    if (hit) return ranged(req, hit);
    try { const res = await fetch(new Request(key, { cache: "no-cache" })); if (res.ok && res.status === 200) { c.put(key, res.clone()); return ranged(req, res); } if (strict) { const old = await c.match(key, { ignoreSearch: true }); if (old) return ranged(req, old); } return res; }
    catch (er) { const old = strict ? await c.match(key, { ignoreSearch: true }) : null; return old ? ranged(req, old) : Response.error(); } })());''')
s = s.replace('const CACHE = "capy-offline-v2";', 'const CACHE = "capy-offline-v2";   /* V559 */', 1)
open(swdst, "w", encoding="utf-8").write(s)
print("ok")
