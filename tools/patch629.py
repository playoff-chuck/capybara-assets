#!/usr/bin/env python3
# V629 (Martin 11.11. 13:54): Tagesmission zählte schon vor Welle 20 im Hintergrund mit (dailyAdd ohne Sperre) – konnte vorher als «geschafft» aufpoppen.
# Jetzt zählt sie erst, wenn sie freigeschaltet ist (beste Welle ≥ 20).
import sys, os
site = sys.argv[1]; p = os.path.join(site, "index.html"); s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V628";', 'const GAME_VER = "V629";')
rep('function dailyAdd(key, v) { try { if (!DAILY.m || DAILY.m.done',
    'function dailyAdd(key, v) { try { if (!dailyMsnGate()) return;   /* V629: erst ab Welle 20 */ if (!DAILY.m || DAILY.m.done')
open(p, "w", encoding="utf-8").write(s)
print("ok V629")
