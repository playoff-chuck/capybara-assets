import json, sys, random, time
from multiprocessing import Pool
from collections import Counter
sys.path.insert(0, '.')
import sim8
def chunk(a):
    sk, n, seed, over = a; sim8.P.update(over); G = json.load(open('G.json')); rnd = random.Random(seed)
    return [(sk, r["w"], r["why"]) for r in (sim8.run(G, sk, rnd) for _ in range(n))]
def main(total, over, out):
    jobs = []
    for i, (sk, d) in enumerate(sim8.SK.items()):
        n = round(total * d["share"])
        for j in range(0, n, 1000): jobs.append((sk, min(1000, n - j), 7000 * i + j + 11, over))
    with Pool(2) as Pp: parts = Pp.map(chunk, jobs)
    R = {}
    for part in parts:
        for sk, w, why in part:
            for k in (sk, "ALL"): R.setdefault(k, []).append((w, why))
    res = {}
    for k, L in R.items():
        n = len(L); ws = sorted(w for w, _ in L)
        reach = [round(100 * sum(1 for w in ws if w >= x) / n, 2) for x in range(1, 151)]
        db = Counter(w for w, y in L if y == "blocks"); dm = Counter(w for w, y in L if y == "monsters")
        res[k] = dict(n=n, median=ws[n // 2], reach=reach, deadBlocks=[round(100 * db[x] / n, 3) for x in range(1, 151)],
                      deadMonsters=[round(100 * dm[x] / n, 3) for x in range(1, 151)],
                      why={y: round(100 * c / n, 1) for y, c in Counter(y for _, y in L).items()})
    json.dump(res, open(out, "w"))
    a = res["ALL"]; print(out, "median", a["median"], "reach60/90/120/150", a["reach"][59], a["reach"][89], a["reach"][119], a["reach"][149], a["why"])
if __name__ == "__main__":
    t = time.time(); main(int(sys.argv[1]), json.loads(sys.argv[2]), sys.argv[3]); print("s", round(time.time() - t, 1))
