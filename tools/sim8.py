"""Capybara Squad – Simulation v8 (04.11.2026, Stand V181).
Basis v5 + V179 (Monster-HP x1,15 ab W20 / x1,25 ab W50, Fallzeit-Teiler W30 .95 / W40 .9025 / W50 .857375 / W60 .7716)
+ V181 (Monster-HP x0,75 in W91-100) + Nuts-Abstecher (Start 600 Gold, 5 Leben, keine Tuerme; Level L: 6+2L Monster,
HP x a*g^L, Tempo x(1,05+0,015L), Fallzeit x f*h^L, min 0,07 s; +40+10L Gold je Level)."""
import json, sys, random, statistics as st
from collections import Counter, defaultdict
TOWER, MAXLVL, MAXW = 50, 3, 150
HPM = dict(heavy=2.6, fast=0.6, munch=1.5, runner=2.2, bomber=1.3, kiefer=3.2, volt=1.8, norm=1, jaguar=1.4, mummy=2.4*1.5, tiger=2.2, bear=4.0)
SPM = dict(fast=1.5, heavy=0.7, munch=0.85, runner=1.75, bomber=0.9, kiefer=1.0, volt=0.8, norm=1, jaguar=1.25*1.14, mummy=0.6, tiger=1.3, bear=0.7)
REW = dict(heavy=14, munch=11, runner=22, bomber=16, kiefer=40, volt=26, jaguar=18, mummy=24, tiger=30, bear=45)
SIDE = {45: 0.7, 61: 0.65, 75: 0.65, 89: 0.65, 99: 0.65}
SK = {
  "beginner": dict(share=0.40, e=(0.45, 0.07), lim=(0.56, 0.05), lines=2.6, linegold=40, spend=0.75, splat=0.5, sweep=0.002, hk=(0.42, 0.2), card=1.03, speed=[(1, .95), (1.5, .05)]),
  "martin":   dict(share=0.35, e=(0.62, 0.07), lim=(0.43, 0.04), lines=3.3, linegold=70, spend=0.85, splat=0.9, sweep=0.004, hk=(0.5, 0.25), card=1.05, speed=[(1, .9), (1.5, .1)]),
  "good":     dict(share=0.20, e=(0.75, 0.06), lim=(0.36, 0.03), lines=4.5, linegold=110, spend=0.92, splat=1.1, sweep=0.008, hk=(0.6, 0.3), card=1.08, speed=[(1, .7), (1.5, .2), (2, .1)]),
  "pro":      dict(share=0.05, e=(0.85, 0.05), lim=(0.29, 0.03), lines=6.0, linegold=150, spend=0.95, splat=1.2, sweep=0.012, hk=(0.65, 0.3), card=1.10, speed=[(1, .5), (1.5, .2), (2, .2), (3, .1)]),
}
P = dict(nKit={30:600,60:600,90:600,120:600}, hp20=1.15, hp50=1.25, hp91=0.75, nA=1.3, nG=1.09, nF=0.85, nH=0.955, nSp=0.015, nCnt=2)
def hpmul(w, nuts=False):
    m = P["hp50"] if w >= 50 else P["hp20"] if w >= 20 else 1
    if not nuts and 91 <= w <= 100: m *= P["hp91"]
    if not nuts:
        for lo, hi, f in P.get("hpr", []):
            if lo <= w <= hi: m *= f
    return m
def taper(w): return (1.0 if w <= 20 else max(0.35, 0.95 ** (w - 20))) * (0.95 if w <= 30 else 1.10)
def upc(G, t, l):
    c = round(G["weap"][t]["cost"] * .8 * l); return c * 5 if l >= 3 else c
def wstat(G, t, l):
    b = G["weap"][t]; l -= 1
    if l > 2: l = 2 + (l - 2) * 0.35
    return b["dmg"] * (1 + .6 * l), b["rate"] * (1 + .15 * l), b["range"] + .25 * l
def comp(G, w, N, spawned0):
    F = lambda k: G.get(k, 999)
    run = 1 + (w - F("runnerFrom") + 5) // 10 if w >= F("runnerFrom") else 0
    bom = 1 + (w - F("bomberFrom")) // 10 if w >= F("bomberFrom") else 0
    vol = 1 + (w - F("voltFrom")) // 8 if w >= F("voltFrom") else 0
    c = Counter(); slot = lambda k, n: (N * (k + 1)) // (n + 1)
    for idx in range(N):
        ts = spawned0 + idx + 1
        if w >= F("kieferFrom") and ts % 30 == 0: k = "kiefer"
        elif any(slot(j, run) == idx for j in range(run)): k = "runner"
        elif any(slot(j, bom) + 1 == idx for j in range(bom)): k = "bomber"
        elif any(slot(j, vol) + 2 == idx for j in range(vol)): k = "volt"
        elif w >= F("bearFrom") and idx % 11 == 7: k = "bear"
        elif w >= F("tigerFrom") and idx % 9 == 4: k = "tiger"
        elif w >= F("mummyFrom") and idx % 8 == 6: k = "mummy"
        elif w >= F("jaguarFrom") and idx % 7 == 1: k = "jaguar"
        elif w >= F("munchFrom") and idx % G["munchEvery"] == 2: k = "munch"
        elif w >= F("heavyFrom") and idx % 6 == 5: k = "heavy"
        elif w >= F("fastFrom") and idx % 4 == 3: k = "fast"
        else: k = "norm"
        c[k] += 1
    return c
def grav(G, w, lines):
    K, K2 = G.get("gravKnee", 1e9), G.get("gravKnee2", 1e9)
    we = w if w <= K else K + (min(w, K2) - K) * G.get("gravKneeF", 1) + max(0, w - K2) * G.get("gravKneeF2", 1)
    le = lines if w <= K else lines * we / w
    g = max(G["gravMin"], G["gravBase"] - le * G["gravLine"] - we * G["gravWave"]) / (0.7716 if w >= 60 else 0.857375 if w >= 50 else 0.9025 if w >= 40 else 0.95 if w >= 30 else 1)
    for lo, hi, f in P.get("gm", []):
        if lo <= w <= hi: g *= f
    return g / SIDE.get(w, 1)
def hkWave(w): return w >= 6 and w % 20 != 0 and (w % 6 == 0 or w % 10 == 0)
def pick(rnd, opts):
    x = rnd.random()
    for v, p in opts:
        x -= p
        if x <= 0: return v
    return opts[-1][0]
def buy(G, S, w, gold, towers, unl):
    budget = gold * S["spend"]; gold -= budget
    tier = (w - 1) // 3; capT = 2 + tier; capW = min(4, 2 + tier // 2)
    val = lambda t, l: (lambda d, r, R: d * r * R)(*wstat(G, t, l))
    ml = 5 if w >= 31 else MAXLVL
    while True:
        best = None
        for t in ("mg", "kan"):
            if w < unl.get(t, 1): continue
            c = G["weap"][t]["cost"]
            if len(towers) < capT and TOWER + c <= budget:
                sc = val(t, 1) / (TOWER + c)
                if not best or sc > best[0]: best = (sc, TOWER + c, ("n", t))
            if c <= budget:
                for i, tw in enumerate(towers):
                    if len(tw) < capW:
                        sc = val(t, 1) / c
                        if not best or sc > best[0]: best = (sc, c, ("a", i, t))
                        break
        for i, tw in enumerate(towers):
            for j, (t, l) in enumerate(tw):
                if l < ml:
                    c = upc(G, t, l)
                    if c <= budget:
                        sc = (val(t, l + 1) - val(t, l)) / c
                        if not best or sc > best[0]: best = (sc, c, ("u", i, j))
        if not best: break
        _, c, a = best; budget -= c
        if a[0] == "n": towers.append([[a[1], 1]])
        elif a[0] == "a": towers[a[1]].append([a[2], 1])
        else: towers[a[1]][a[2]][1] += 1
    return gold + budget
def fight(G, S, w, N, spawned, towers, medals, e, cardm, hpx, spx):
    unl = G["unlock"]
    spawnInt = max(G["spawnMin"], G["spawnBase"] - w * .03)
    baseHp = G["hpBase"] * (1 + G.get("hpLin", 0) * (w - 1)) * G["hpGrow"] ** (w - 1) * hpx
    vbase = min(G["spMax"], G["spBase"] + G["spGrow"] * w) * spx
    frost = 1.25 if w >= unl["frost"] else 1.0
    mm = 1 + 0.25 * medals
    ws = [wstat(G, t, l) + (t,) for tw in towers for t, l in tw]
    leaks = 0; inc = 0; cp = comp(G, w, N, spawned)
    for k, n in cp.items():
        v = vbase * SPM[k]; dmg = 0; fr = 1.0 if k == "tiger" else frost
        for d, r, R, t in ws:
            hit = d * mm
            if k == "bear": hit = max(hit * 0.4, hit - 2)
            expo = 2 * R / v * fr
            dmg += hit * r * expo / max(1.0, expo / spawnInt / (1.6 if t == "kan" else 1.0))
        dmg *= e * cardm
        ratio = baseHp * HPM[k] / max(dmg, 1e-9)
        lk = n if ratio > 1.15 else (round(n * (ratio - 0.85) / 0.3) if ratio > 0.85 else 0)
        leaks += lk; inc += (n - lk) * (REW.get(k, G["killBase"]) + w)
    return leaks, inc
def run(G, sk, rnd, stopAt=None):
    S = SK[sk]; e = max(0.15, rnd.gauss(*S["e"])); lim = max(0.12, rnd.gauss(*S["lim"])); spd = pick(rnd, S["speed"])
    gold, lives, medals, mprog, lines, spawned, cardm, tons = G["startGold"], G["lives"], 0, 0, 0, 0, 1.0, 0
    towers = []; unl = G["unlock"]; saves = 0; lifelog = {}
    for w in range(1, MAXW + 1):
        if w == unl.get("ton", 99): tons += 1
        tier = (w - 1) // 3
        N = min(G["capBase"] + G.get("capPer", 4) * tier, G["waveBase"] + G["wavePer"] * w)
        tp = taper(w)
        gold = buy(G, S, w, gold, towers, unl)
        leaks, inc = fight(G, S, w, N, spawned, towers, medals, e, cardm, hpmul(w), 1.0); spawned += N
        inc *= G["goldMul"] * tp
        lives -= leaks; medals = max(0, medals - leaks)
        if leaks: mprog = 0
        mprog += sum(1 for _ in range(4) if rnd.random() < S["splat"] / 4)
        while mprog >= 4 and medals < 4: mprog -= 4; medals += 1
        lines += S["lines"]
        gold += inc + ((20 + 5 * w) * G["goldMul"] + S["linegold"] * G["goldMul"]) * tp
        if rnd.random() < S["sweep"]: gold += 100 + 15 * w; medals = min(4, medals + 1)
        if w % 20 == 0: cardm = S["card"]
        if w in (8, 14, 22): tons += 1
        if hkWave(w):
            p, frac = S["hk"]; stake = min(gold, gold * frac * (0.5 + rnd.random()))
            gold += stake if rnd.random() < p else -stake
        if towers and rnd.random() < 0.02 * len(towers) * (1.2 - e): towers.pop(rnd.randrange(len(towers)))
        if lives <= 0: return dict(w=w, why="monsters", e=e, lim=lim)
        if stopAt and w == stopAt: return dict(w=w, why="base", e=e, lim=lim, towers=towers, gold=gold, lines=lines)
        g = grav(G, w, lines) / spd
        pd = 0.002 if g >= lim else min(0.5, 0.04 + 2.0 * (lim - g) / lim)
        if rnd.random() < pd:
            if tons > 0: tons -= 1; saves += 1
            else: return dict(w=w, why="blocks", e=e, lim=lim)
    return dict(w=MAXW, why="finished", e=e, lim=lim)
def nuts(G, sk, rnd, base, board=None):
    """Ein Nuts-Abstecher; Rueckgabe: geschaffte Level (0-30), Todesursache."""
    S = SK[sk]; e = max(0.15, rnd.gauss(*S["e"])); lim = max(0.12, rnd.gauss(*S["lim"]))
    if board: e, lim = board["e"], board["lim"]
    gold, lives, towers, medals, lines, spawned = P["nKit"][base] if base in P["nKit"] else P["nKit"][str(base)], 5, [], 0, base * S["lines"], 0
    if P.get("nKitL"): towers = [[["mg", P["nKitL"]], ["kan", P["nKitL"]], ["frost", P["nKitL"]]] for _ in range(2)]
    if board and P.get("nCopy"): towers = [[list(x) for x in t] for t in board["towers"]]
    for L in range(1, 31):
        N = 6 + P["nCnt"] * L
        gold = buy(G, S, base, gold, towers, G["unlock"])
        leaks, inc = fight(G, S, base, N, spawned, towers, medals, e, 1.0, hpmul(base, True) * P["nA"] * P["nG"] ** L, 1.05 + P["nSp"] * L); spawned += N
        lives -= leaks; medals = max(0, medals - leaks)
        gold += inc * G["goldMul"] + 40 + 10 * L + S["linegold"] * G["goldMul"] * 0.5
        if rnd.random() < S["splat"] / 4 and medals < 4 and not leaks: medals += 0.25
        if lives <= 0: return L - 1, "monsters"
        g = max(0.07, grav(G, base, lines) * P["nF"] * P["nH"] ** L)
        pd = 0.002 if g >= lim else min(0.5, 0.04 + 2.0 * (lim - g) / lim)
        if rnd.random() < pd: return L - 1, "blocks"
    return 30, "done"
