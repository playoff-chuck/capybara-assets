#!/usr/bin/env python3
"""Auswertung eines autotest60-Laufs gegen die Ablauf-Regeln (Stand V290):
R1 nie zwei Fenster gleichzeitig · R2 Pflicht-Fenster frühestens 5 s nach letztem Fenster/Übergang ·
R3 Angebote frühestens 30 s nach letztem Fenster/Übergang · R4 höchstens 1 Angebot je 95 s (Boss-Hack ausgenommen; V311).
Aufruf: python3 tools/autotest_auswertung.py lauf.json [weitere.json ...]
"""
import json, sys

# Fenster-Arten: Pflicht (5 s), Angebot (30 s / 2 min), Übergang (zählt nur als «letztes Fenster»)
PFLICHT = {"intro", "orders", "drop", "give"}   # give = Orden-Geschenk (V319)
ANGEBOT = {"ad", "bandit", "hackAd", "join"}
UEBERGANG = {"map", "sign", "pause", "duel"}   # map wird in art() als Pflicht geprüft
ALLE = PFLICHT | ANGEBOT | UEBERGANG
GRATIS = ("GIFT", "FREE GIFT", "NEW POWER", "AIR DROP")   # Ten-ton-Geschenk / Elite = Waffen-Vorstellung, Air-Drop-Karte (über __whenCalm 5 s) → Pflicht

def art(e):
    k = e["k"]
    if k == "ad" and any(g in (e.get("ttl") or "").upper() for g in GRATIS): return "pflicht"
    if k == "map": return "pflicht"   # Ortswechsel/Kontinentflug: Stufe 1, «nie zwei Screens kurz hintereinander»
    return "pflicht" if k in PFLICHT else "angebot" if k in ANGEBOT else "uebergang"

def pruefe(ev):
    out, offen, last_close, last_offer = [], {}, -1e9, -1e9
    for e in sorted(ev, key=lambda x: x["t"]):
        k = e["k"]
        if k not in ALLE or e["e"] not in ("open", "close"): continue
        t = e["t"] / 1000
        if e["e"] == "close":
            offen.pop(k, None); last_close = max(last_close, t); continue
        # pause/duel öffnen sich als Folge eines anderen Fensters → nicht doppelt zählen
        andere = [x for x in offen if x not in ("pause",) and x != k]
        a = art(e)
        z = f"W{e['wave']:>3}  {t/60:5.1f} min  {k:<7} {(e.get('ttl') or '')[:48]}"
        if andere and k not in ("pause", "duel"):
            out.append(("R1 zwei Fenster", z + f"  ← offen: {', '.join(andere)}"))
        gap = t - last_close if not offen else 0
        if a == "pflicht" and not andere and gap < 5 - 0.3:
            out.append(("R2 <5 s Ruhe", z + f"  (nur {gap:.1f} s nach letztem Fenster)"))
        if a == "angebot":
            if not andere and gap < 30 - 0.3:
                out.append(("R3 <30 s Abstand", z + f"  (nur {gap:.1f} s)"))
            if k != "hackAd" and t - last_offer < 95 - 0.3:
                out.append(("R4 >1 Angebot/95 s", z + f"  (nur {t-last_offer:.0f} s nach letztem Angebot)"))
            last_offer = t
        offen[k] = t
    return out

def zeitleiste(ev):
    z = []
    for e in sorted(ev, key=lambda x: x["t"]):
        if e["e"] == "open" and e["k"] in ALLE and e["k"] != "pause":
            z.append(f"W{e['wave']:>3}  {e['t']/60000:5.1f} min  {e['k']:<7} {(e.get('ttl') or '')[:60]}")
        if e["k"] == "stuck": z.append(f"W{e['wave']:>3}  {e['t']/60000:5.1f} min  !! hängt: {e['e']}")
    return z

if __name__ == "__main__":
    for f in sys.argv[1:]:
        d = json.load(open(f))
        print(f"### {f}  ({len(d.get('ev', []))} Ereignisse, Ende {d.get('end')})")
        print("\n-- Zeitleiste --"); print("\n".join(zeitleiste(d["ev"])))
        v = pruefe(d["ev"])
        print(f"\n-- Verstöße: {len(v)} --")
        for r, z in v: print(f"{r:<20} {z}")
        print("\n-- JS-Fehler --", d.get("err") or "keine", [c for c in d.get("console", []) if "404" not in c][:10] or "")
