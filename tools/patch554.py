#!/usr/bin/env python3
# V554: Freemium-Preise (Martin 10.11. 13:46): Südamerika + Afrika gratis; jeder weitere Kontinent 99 ₽ ODER 2 Freunde bis Welle 15;
# alle 3 Kontinente auf einmal 199 ₽ ODER 4 Freunde bis Welle 15. Schalter bleibt AUS.
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)

rep('const GAME_VER = "V553";', 'const GAME_VER = "V554";')
rep('''price: "299 ₽", per: 2, fw: 10,
  ticket() { try { return localStorage.getItem("capy-ticket") === "1"; } catch (e) { return false; } },''',
    '''price: "199 ₽", one: "99 ₽", per: 2, all: 4, fw: 15,
  ticket() { try { return localStorage.getItem("capy-ticket") === "1"; } catch (e) { return false; } },   /* alle 3 */
  bought() { try { return +localStorage.getItem("capy-ticket-n") || 0; } catch (e) { return 0; } },   /* einzeln gekaufte Kontinente (in Reihenfolge) */''')
rep('''  open(c) { if (!FM.on || c < 2 || FM.ticket()) return true; return c - 2 < Math.floor(FM.friends() / FM.per); },''',
    '''  open(c) { if (!FM.on || c < 2 || FM.ticket()) return true; const fr = FM.friends(); if (fr >= FM.all) return true; return c - 2 < FM.bought() + (fr >= FM.per ? 1 : 0); },''')
rep('''fr = FM.friends(), have = fr % FM.per, nx = FM.next();''', '''fr = FM.friends(), nx = FM.next(), nxi = Math.max(0, nx - 2);''')
rep('''      <div class="fmOpt"><b>🎟 WORLD TOUR TICKET</b><small>All 3 continents at once</small><button class="fmBuy" data-a="buy">${FM.price}</button></div>
      <div class="fmOr">OR</div>
      <div class="fmOpt"><b>👫 INVITE 2 FRIENDS</b><small>${["When 2 friends reach wave 10, ASIA opens. Free!", "When 2 friends reach wave 10, NORTH AMERICA opens. Free!", "When 2 friends reach wave 10, ANTARCTICA opens. Free!"][Math.max(0, nx - 2)]}</small><span class="fmCnt">Friends: ${have}/${FM.per}</span><button class="fmInv" data-a="inv">INVITE ▶</button></div>''',
    '''      <div class="fmOpt"><b>🎟 WORLD TOUR TICKET</b><small>All 3 continents at once</small><button class="fmBuy" data-a="buy">${FM.price}</button></div>
      <div class="fmOpt fmOne"><b>${["🔓 ONLY ASIA", "🔓 ONLY NORTH AMERICA", "🔓 ONLY ANTARCTICA"][nxi]}</b><small>The next continent</small><button class="fmBuy fmBuy1" data-a="buy1">${FM.one}</button></div>
      <div class="fmOr">OR FREE</div>
      <div class="fmOpt"><b>👫 INVITE FRIENDS</b><small>${["2 friends reach wave 15 → ASIA", "2 friends reach wave 15 → NORTH AMERICA", "2 friends reach wave 15 → ANTARCTICA"][nxi]}</small><small>4 friends reach wave 15 → all 3</small><span class="fmCnt">Friends: ${Math.min(fr, FM.all)}/${FM.all}</span><button class="fmInv" data-a="inv">INVITE ▶</button></div>''')
rep('''if (b.dataset.a === "buy") return;''', '''if (b.dataset.a === "buy" || b.dataset.a === "buy1") return;   /* Kauf folgt mit RuStore-Billing */''')
rep('''<small>Ticket ${FM.price} or 2 friends</small>''', '''<small>From ${FM.one} or 2 friends</small>''')
rep('''#ovFm .fmOr{margin:6px 0;''', '''#ovFm .fmOne{margin-top:6px}
#ovFm .fmBuy1{background:#ff9a3c!important}
#ovFm .fmOr{margin:6px 0;''')
open(dst, "w", encoding="utf-8").write(s)
print("ok")
