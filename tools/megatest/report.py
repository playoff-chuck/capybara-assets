#!/usr/bin/env python3
"""Megatest-Bericht: python3 report.py PHASE  → runs/report_PHASE.md (PHASE = p1…p6 oder all)."""
import json, os, sys, glob, collections
R = "/root/megatest/runs"; PH = sys.argv[1]
SEV = {"A1": "K", "A2": "K", "A6": "K", "B1": "K", "B13": "K", "C5": "K", "D1": "K", "D8": "K", "D14": "K", "D17": "K", "D19": "K", "E1": "K", "E5": "K", "F5": "K", "B16": "K", "C14": "K",
       "A5": "M", "A7": "M", "A8": "M", "A15": "M", "A16": "M", "B4": "M", "B5": "M", "B6": "M", "B8": "M", "B10": "M", "B14": "M", "B19": "M", "C1": "M", "C7": "M", "C10": "M", "C12": "M", "D2": "M", "D3": "M", "D4": "M", "D16": "M", "E2": "M", "E3": "M", "F1": "M", "F6": "M", "A14": "M"}
NAMES = {"A1": "Knacken in Datei", "A2": "Lautstärkesprung Synth", "A5": "Lautstärkesprung Audio", "A6": "Abtastrate", "A7": "Musikpegel fällt ab", "A8": "Musik sinkt bei Sprechblase", "A13": "doppeltes Wort", "A14": "Sprachclip fehlt",
         "A15": "Doppel-Jubel Boss-Hack", "A16": "zu viele Sprüche", "B1": "Doppelfenster", "B4": "Blase/Pille über Fenster", "B5": "Wellennummer verdeckt", "B6": "Boss-Pille über Hack", "B8": "über Game-over", "B10": "Kartenschilder überlappen",
         "B13": "Knopf über Spielfeld", "B14": "Diplom-Rahmen", "B16": "Bild fehlt", "B19": "Spielfeld zu dunkel", "C1": "Text abgeschnitten", "C5": "Hack-Fenster außerhalb", "C7": "nicht übersetzt", "C10": "RU-Anrede/Gold",
         "C12": "Schrift fehlt", "C13": "Schrift < 11 px", "C14": "Marke im Text", "D1": "Hänger", "D2": "Fenster zu dicht", "D3": "2. Hack-Angebot", "D4": "Fensterkette", "D8": "Spiel läuft hinter Fenster", "D14": "Kontinent nicht leer",
         "D16": "Boss-Signal nach W150", "D17": "Nuts-Sperre verletzt", "D19": "Welle startet nicht", "E1": "Knopf außerhalb", "E2": "Knopf zu klein", "E3": "Anzeige verrutscht", "E5": "Knöpfe gesperrt", "F1": "FPS", "F5": "JS-Fehler", "F6": "Ladezeit 3G"}
FALSE_C7 = ("English", "Español", "Português", "Русский", "DEV", "dev:", "Blue #", "Rosie #", "HQ-#", "TT-#", "AA")
runs = sorted(d for d in glob.glob(R + "/*/") if (PH == "all" or os.path.basename(d.rstrip("/")).startswith(PH + "_")))
out = [f"# Megatest – Bericht {PH} ({len(runs)} Läufe)\n"]
tot = collections.Counter(); ex = collections.defaultdict(list); runrows = []
for d in runs:
    p = d + "result.json"; name = os.path.basename(d.rstrip("/"))
    if not os.path.exists(p): runrows.append(f"| {name} | – | kein Ergebnis | | | |"); continue
    r = json.load(open(p)); f = r.get("find", []); w = r.get("waves", []); last = w[-1]["w"] if w else "–"; mins = round((w[-1]["real"] if w else 0) / 60)
    f = [x for x in f if not (x["cat"] == "C7" and x.get("key", "").startswith(FALSE_C7))]
    c = collections.Counter(x["cat"] for x in f); tot.update(c)
    for x in f:
        if len(ex[x["cat"]]) < 6 and x["msg"] not in [e[0] for e in ex[x["cat"]]]: ex[x["cat"]].append((x["msg"], f"{name} W{x['w']}"))
    hang = "HÄNGER W%s" % r["stall"]["w"] if r.get("stall") else ""
    con = len(r.get("console", [])); net = [n for n in r.get("netfail", []) if "favicon" not in str(n) and "assetlinks" not in str(n) and "ERR_ABORTED" not in str(n)]
    if con: tot["F5"] += con; ex["F5"] += [(m[:160], name) for m in r["console"][:3]]
    if net: tot["A17/F6 Ladefehler"] += len(net); ex["A17/F6 Ladefehler"] += [(str(n)[:120], name) for n in net[:3]]
    if hang: tot["D1"] += 1; ex["D1"].append((json.dumps(r["stall"])[:200], name))
    ints = [i for i in r.get("interrupt", []) if i.get("paused") is False and i.get("open")]
    runrows.append(f"| {name} | {r['group']['name']} {r['group']['w']}×{r['group']['h']} | {r['lang']} | bis {last} | {mins} min | {sum(c.values())} Funde {hang} |")
out.append("## Läufe\n| Lauf | Gerät | Sprache | erreicht | Dauer | Ergebnis |\n|---|---|---|---|---|---|\n" + "\n".join(runrows) + "\n")
for extra in (["static.json"] if PH in ("all", "p1") else []):
    fp = os.path.join("/root/megatest", extra)
    if os.path.exists(fp):
        for x in json.load(open(fp)): tot[x["cat"]] += 1; ex[x["cat"]].append((x["msg"], "statisch"))
pp = "/root/megatest/perf.json"
if PH in ("all", "p1") and os.path.exists(pp):
    out.append("## Leistung (echte Uhr, CPU-Bremse je Gerät)\n| Gerät | Laden | FPS W5 | FPS W45 | FPS W95 | Grafikstufe |\n|---|---|---|---|---|---|")
    for r in json.load(open(pp)):
        if r.get("f6"): out.append(f"\n**3G-Ladezeit (F6):** spielbereit nach {r.get('ready_s', '?')} s, alles geladen nach {r.get('idle_s', '?')} s → {'ok' if r.get('ok') else 'ZU LANGSAM (> 35 s)'}"); continue
        if r.get("error"): out.append(f"| {r['name']} | Fehler: {r['error'][:60]} | | | | |"); continue
        ws = r["waves"]; out.append(f"| {r['name']} | {r['load_local_s']} s | " + " | ".join(f"{m['fps']:.0f}{'' if m['ok'] else ' ⚠'}" for m in ws) + f" | {ws[-1].get('lite') or 'voll'} |")
        for m in ws:
            if not m["ok"]: tot["F1"] += 1; ex["F1"].append((f"{r['name']} W{m['w']}: {m['fps']:.0f} FPS (max. Lücke {m['maxGap']:.0f} ms)", "perf"))
    out.append("")
out.append("## Funde nach Prüfpunkt\n| Punkt | Schwere | Anzahl | Beispiele |\n|---|---|---|---|")
for cat, n in sorted(tot.items(), key=lambda kv: ({"K": 0, "M": 1}.get(SEV.get(kv[0], "N"), 2), -kv[1])):
    eg = "<br>".join(f"{m} ({w})" for m, w in ex[cat][:4]).replace("|", "/")
    out.append(f"| {cat} {NAMES.get(cat, '')} | {SEV.get(cat, 'N')} | {n} | {eg} |")
open(f"{R}/report_{PH}.md", "w").write("\n".join(out) + "\n"); print(f"report_{PH}.md", sum(tot.values()), "Funde")
