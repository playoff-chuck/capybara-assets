"""Wertet sim9-Läufe (jsonl) aus → eine JSON-Zusammenfassung für den Bericht.
Aufruf: sim9_report.py out.json lauf1.jsonl [lauf2.jsonl ...] [--nohack nohack1.jsonl ...]"""
import json, sys, random, statistics as st
from collections import Counter, defaultdict
args = sys.argv[2:]; out = sys.argv[1]
main, nohack, cur = [], [], None
for a in args:
    if a == "--nohack": cur = nohack; continue
    (cur if cur is not None else main).append(a)
def load(fs):
    R = []
    for f in fs:
        for line in open(f): R.append(json.loads(line))
    return R
def summ(R):
    n = len(R); W = [r["w"] for r in R]
    reach = {k: round(100 * sum(1 for x in W if x >= k) / n, 2) for k in (10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150)}
    fin = round(100 * sum(1 for r in R if r["why"] == "finished") / n, 2)
    why = Counter(r["why"] for r in R)
    die = [r for r in R if r["why"] != "finished"]
    dieW = Counter(r["w"] for r in die)
    cont = Counter(((r["w"] - 1) // 30, r["why"]) for r in die)
    lives = Counter(r.get("lv", 0) for r in R if r["why"] == "finished")
    gold = {}
    for w in range(5, 151, 5):
        xs = [r["ga"][str(w)] for r in R if str(w) in r["ga"]]
        if len(xs) >= 30: xs.sort(); gold[w] = dict(p25=xs[len(xs) // 4], med=xs[len(xs) // 2], p75=xs[3 * len(xs) // 4])
    keys = ["kills", "waveGold", "lines", "sweep", "egg", "hack", "thief", "refund", "spent"]
    cash = {k: round(sum(r["cash"].get(k, 0) for r in R) / n) for k in keys}
    return dict(n=n, median=st.median(W), mean=round(st.mean(W), 1), reach=reach, finished=fin, why=dict(why),
                topDeath=dieW.most_common(10), cont={f"{c}:{y}": v for (c, y), v in sorted(cont.items())}, livesEnd=dict(sorted(lives.items())),
                gold=gold, cash=cash)
R = load(main); res = dict(main=summ(R))
# Boss-Hack: alle Duelle aus den Läufen + Stichprobe 10 000
H = [h for r in R for h in r["hk"]]
rnd = random.Random(5); samp = rnd.sample(H, min(10000, len(H)))
def hstat(H):
    n = len(H); win = sum(1 for h in H if h[3])
    byB = {}
    for b in ("S", "M", "L", "XL"):
        x = [h for h in H if h[2] == b]
        if x: byB[b] = dict(n=len(x), share=round(100 * len(x) / n, 1), win=round(100 * sum(1 for h in x if h[3]) / len(x), 1))
    net = [h[1] if h[3] else -h[1] for h in H]
    stakes = sorted(h[1] for h in H)
    byC = {}
    for c in range(5):
        x = [h for h in H if (h[0] - 1) // 30 == c]
        if x: byC[c] = dict(n=len(x), win=round(100 * sum(1 for h in x if h[3]) / len(x), 1), stakeMed=sorted(h[1] for h in x)[len(x) // 2], netAvg=round(st.mean(h[1] if h[3] else -h[1] for h in x)))
    return dict(n=n, win=round(100 * win / n, 1), byBoss=byB, byCont=byC, stakeMed=stakes[n // 2], stakeP90=stakes[9 * n // 10],
                netSum=sum(net), netAvg=round(st.mean(net), 1), gainAvg=round(st.mean([h[1] for h in H if h[3]])), lossAvg=round(st.mean([h[1] for h in H if not h[3]])),
                bigLoss=sum(1 for h in H if not h[3] and h[1] >= 2000))
res["hk10k"] = hstat(samp); res["hkAll"] = hstat(H)
# pro Lauf: Netto Boss-Hack
per = sorted(r["cash"].get("hack", 0) for r in R); n = len(per)
res["hkPerRun"] = dict(p10=per[n // 10], p25=per[n // 4], med=per[n // 2], p75=per[3 * n // 4], p90=per[9 * n // 10], plus=round(100 * sum(1 for x in per if x > 0) / n, 1), avg=round(st.mean(per)))
T = [t for r in R for t in r["th"]]
res["thief"] = dict(n=len(T), perRun=round(len(T) / len(R), 2), avg=round(st.mean(T)) if T else 0, med=sorted(T)[len(T) // 2] if T else 0)
if nohack: res["nohack"] = summ(load(nohack))
json.dump(res, open(out, "w"), indent=1)
print(json.dumps({k: (v if k != "main" else {kk: v[kk] for kk in ("n", "median", "finished", "why", "reach")}) for k, v in res.items() if k in ("main", "hk10k", "hkPerRun", "thief")}, indent=0)[:3000])
