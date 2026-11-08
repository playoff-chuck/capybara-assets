#!/usr/bin/env python3
"""V445 (Martin 08.11. 12:43):
- Fallschirm-Absprung: Rosie/Blue ohne weißen Kreis (ganzes Bild, kein Rahmen) – bis die neue Fallschirm-Grafik eingebaut ist
- Turm-Menü eines Elite-Turms: Sticker «ELITE TOWER · laser active · nothing to buy here», Waffen-/All-in-Knöpfe ausgeblendet, nur Sell/Done
Nutzung: python3 tools/patch445.py src dst"""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()

def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (c, a[:80])
    s = s.replace(a, b)

rep('GAME_VER = "V444"', 'GAME_VER = "V445"')
rep('.wpChute img{position:absolute;left:-17px;top:-34px;width:34px;height:34px;max-width:none;border-radius:50%;border:2px solid #3a2414;background:#fff7e8;object-fit:cover;object-position:50% 18%}',
    '.wpChute img{position:absolute;left:-24px;top:-44px;width:48px;height:48px;max-width:none;object-fit:contain;filter:drop-shadow(0 2px 2px rgba(0,0,0,.35))}   /* V445: kein weißer Kreis */\n'
    '.eliteTag{display:flex;align-items:center;gap:10px;background:linear-gradient(135deg,#ffd84d,#ff9f1a);border:3px solid #3a2414;border-radius:14px;padding:10px 12px;box-shadow:0 4px 0 #3a2414;transform:rotate(-1.5deg);margin:2px 0 4px}\n'
    '.eliteTag b{font-family:var(--f-display);font-weight:400;font-size:22px;letter-spacing:.06em;color:#3a2414;line-height:1}.eliteTag small{display:block;font:700 12px var(--f-body);color:#5a3a1a;margin-top:2px}.eliteTag i{font-style:normal;font-size:26px;line-height:1}')
rep('''  let h = `<div class="sheetHead"><h3>TOWER ${t.id}</h3><span>Gold: ${S.gold}</span></div>`;
  { const p = allInPlan(t);''',
'''  let h = `<div class="sheetHead"><h3>TOWER ${t.id}</h3><span>Gold: ${S.gold}</span></div>`;
  if (t.eliteT > 0) {   /* V445: Elite-Turm – nichts zu kaufen */
    h += `<div class="eliteTag"><i>★</i><div><b>ELITE TOWER</b><small>Laser active · ${Math.ceil(t.eliteT)} s left · nothing to buy here</small></div></div>`;
    h += `<div class="sheetFoot"><button id="sSell">Sell · +${Math.round(towerValue(t) / 2)}</button><button id="sClose" class="btn-accent">Done</button></div>`;
    $("sheetIn").innerHTML = h; return;
  }
  { const p = allInPlan(t);''')
open(dst, "w", encoding="utf-8").write(s)
print("ok", dst)
