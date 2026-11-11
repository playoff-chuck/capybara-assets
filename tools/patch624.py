#!/usr/bin/env python3
# V624 (Martin 11.11. 13:21/13:22):
# 1) Erster echter Boss-Hack: keine Einsatzwahl (Schieber, %-Knöpfe weg), Einsatz fest 10 % des Goldes.
# 2) Testlink ?test=tips: Welle 5 läuft 5 s, dann Coach-Tipps, danach der Hack (wie beim ersten Mal).
import sys, os, json
site = sys.argv[1]; p = os.path.join(site, "index.html"); s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V623";', 'const GAME_VER = "V624";')
rep("hack: 5, blk: 65,", "hack: 5, tips: 5, blk: 65,")
rep('''        if (q === "shock") {''', '''        if (q === "tips") { S.testKind = "tips"; S.waveCD = 0.3; S.gold = Math.max(S.gold | 0, 600); setTimeout(() => { try { window.__hkTips.showThen(() => openHack(true)); } catch (e) {} }, 5300); }   /* V624: Testlink Coach-Tipps */
        if (q === "shock") {''')
rep('window.__hkTips = { show: () => show(null), need };', 'window.__hkTips = { show: () => show(null), showThen: cb => show(cb), need };')
# erster Hack: fester Einsatz 10 %
rep('''  const _sd = startDuel; startDuel = function (keep) {''', '''  const first = () => { try { return (LS.get("capy-hk-first") !== "1" && !S.testRun) || (S.testRun && S.testKind === "tips"); } catch (e) { return false; } };   /* V624 */
  const fst = document.createElement("p"); fst.id = "hkFirstP"; fst.hidden = true; fst.textContent = "First hack: your stake is fixed at 10 % of your gold."; const hb = document.getElementById("hackBet"); if (hb) hb.insertBefore(fst, hb.querySelector(".hkRow"));
  const _oh2 = openHack; openHack = function () { const r = _oh2.apply(this, arguments); try { const f = first(); hb.classList.toggle("hkFirst", f); fst.hidden = !f;
      if (f) { const rg = $("hkRange"); rg.value = Math.max(0, Math.min(+rg.max || 0, Math.round((S.gold | 0) * 0.1 / 10) * 10)); hkStakeUI(); } } catch (e) {} return r; };
  document.getElementById("hkGo").addEventListener("click", () => { try { if (hb.classList.contains("hkFirst") && !S.testRun) LS.set("capy-hk-first", "1"); hb.classList.remove("hkFirst"); fst.hidden = true; } catch (e) {} }, true);
  const _sd = startDuel; startDuel = function (keep) {''')
rep('#ovHkTips[hidden]{display:none!important}', '#ovHkTips[hidden]{display:none!important}\n#hackBet.hkFirst #hkRange,#hackBet.hkFirst .hkChips{display:none!important}#hkFirstP{margin:4px 0 8px;font:800 14px/1.25 "Baloo 2",sans-serif;color:#ffd84d;text-align:center}')
open(p, "w", encoding="utf-8").write(s)
K = ["First hack: your stake is fixed at 10 % of your gold."]
T = {"en": K, "ru": ["Первый взлом: ставка – 10 % твоего золота."], "de": ["Erster Hack: Dein Einsatz ist fest 10 % deines Goldes."],
     "es": ["Primer hackeo: tu apuesta es el 10 % de tu oro."], "pt": ["Primeiro hack: sua aposta é 10 % do seu ouro."]}
for l, vals in T.items():
    q = os.path.join(site, "lang", l + ".json"); d = json.loads(open(q, encoding="utf-8").read())
    for k, v in zip(K, vals): d[k] = v
    open(q, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=0))
print("ok V624")
