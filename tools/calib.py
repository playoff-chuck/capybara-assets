import json, random, pickle, sim8, sys, itertools
G=json.load(open('G.json')); W=json.load(open('test.json')); B=pickle.load(open('boards.pkl','rb'))
def zone(base, over, reps=2):
    sim8.P.update(over); tot=[0]*31; ws=0; why={"blocks":0,"monsters":0,"done":0}
    for sk,d in sim8.SK.items():
        wt=d["share"]*W[sk]["reach"][base-1]/100; rnd=random.Random(3+base); res=[]
        for b in B[(base,sk)]:
            for _ in range(reps): res.append(sim8.nuts(G,sk,rnd,base,b))
        n=len(res)
        if not n: continue
        for x in range(31): tot[x]+=wt*sum(1 for l,_ in res if l>=x)/n
        for _,y in res: why[y]+=wt/n
        ws+=wt
    return [round(100*t/ws,1) for t in tot], {k:round(100*v/ws) for k,v in why.items()}
if __name__=="__main__":
    over=json.loads(sys.argv[1]); bases=[int(x) for x in sys.argv[2].split(',')]
    for b in bases:
        c,why=zone(b,over); print(b,over,'L1',c[1],'L5',c[5],'L10',c[10],'L20',c[20],'L30',c[30],why,flush=True)
