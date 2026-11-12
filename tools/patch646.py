#!/usr/bin/env python3
# V646 (Martin 12.11. 08:13/08:35): Tipp-Karte «Stapel zu hoch» wirbt ab Welle 8 (Ten-ton im Shop) für die Zehntonne
# und hat einen zweiten Knopf «TO THE SHOP ▶» (RU «В МАГАЗИН ▶»), der den Shop öffnet. Vor Welle 8 alter Text, ein Knopf.
import sys, os
site = sys.argv[1]; p = os.path.join(site, "index.html"); s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V645";', 'const GAME_VER = "V646";')
rep('t: "YOUR STACK IS TOO HIGH!", p: "If the blocks reach the top, the game is over. Fill rows to clear them – drop blocks into the gaps." },',
    't: "YOUR STACK IS TOO HIGH!", p: "If the blocks reach the top, the game is over. Fill rows to clear them – drop blocks into the gaps.", shopW: 8, p2: "If the blocks reach the top, the game is over. Fill rows to clear them. Really tight? Drop a Ten-ton – it squashes the stack in half! 🪙 600" },   /* V646 */')
rep("card.innerHTML = '<img src=\"img/tip_bulb.webp\" alt=\"\"><div><small>TIP</small><b></b><p></p><button type=\"button\" disabled>GOT IT</button></div>';",
    "card.innerHTML = '<img src=\"img/tip_bulb.webp\" alt=\"\"><div><small>TIP</small><b></b><p></p><div class=\"tipBtns\"><button type=\"button\" class=\"tipShop\" hidden>TO THE SHOP ▶</button><button type=\"button\" class=\"tipOk\" disabled>GOT IT</button></div></div>';   /* V646 */")
rep('const btn = card.querySelector("button"); let cur = null, armT = 0;',
    'const btn = card.querySelector(".tipOk"), shopB = card.querySelector(".tipShop"); let cur = null, armT = 0;\n'
    '  shopB.addEventListener("click", e => { e.stopPropagation(); try { snd("uiTap"); } catch (er) {} close(); try { openShop(); setTimeout(() => { try { const t = document.querySelector(\'[data-buy="ton"]\'); if (t) { (t.closest(".card,.item,.sp,.row,div") || t).scrollIntoView({ block: "center", behavior: "smooth" }); t.classList.add("tipPulse"); setTimeout(() => t.classList.remove("tipPulse"), 2600); } } catch (e2) {} }, 250); } catch (er) {} });   /* V646: Shop, Zehntonne in die Mitte */')
rep('card.querySelector("b").textContent = T.t; card.querySelector("p").textContent = T.p;',
    'const shopOn = !!(T.shopW && (S.wave | 0) >= T.shopW && !S.nuts); shopB.hidden = !shopOn;   /* V646 */\n'
    '    card.querySelector("b").textContent = T.t; card.querySelector("p").textContent = shopOn && T.p2 ? T.p2 : T.p;')
rep('#tipBulb button:disabled{visibility:hidden;opacity:0}',
    '#tipBulb button:disabled{visibility:hidden;opacity:0}\n'
    '#tipBulb .tipBtns{display:flex;align-items:center;justify-content:flex-end;gap:10px}'
    '#tipBulb .tipBtns .tipShop{margin-left:0!important;margin-right:auto;font-size:16px!important;padding:7px 12px 5px!important;border-width:2.5px!important;box-shadow:0 3px 0 #3a2414!important;background:#ffd84d!important}'
    '@keyframes tipPulse{0%,100%{transform:scale(1)}50%{transform:scale(1.08)}}.tipPulse{animation:tipPulse .65s ease-in-out 3}'
    '#tipBulb .tipBtns .tipOk{margin-left:auto}   /* V646 */')
open(p, "w", encoding="utf-8").write(s)
# Übersetzungen direkt in site/lang/<l>.json einfügen (i18n_merge würde spätere Handkorrekturen zurückdrehen)
import json
K = "If the blocks reach the top, the game is over. Fill rows to clear them. Really tight? Drop a Ten-ton – it squashes the stack in half! 🪙 #"
TR = {"en": {K: K, "TO THE SHOP ▶": "TO THE SHOP ▶"}}
for l in ("ru", "es", "pt"):
    TR[l] = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "lang_src", f"{l}_v646.json"), encoding="utf-8"))
for l, add in TR.items():
    q = os.path.join(site, "lang", f"{l}.json"); d = json.load(open(q, encoding="utf-8")); d.update(add)
    with open(q, "w", encoding="utf-8") as f: json.dump(d, f, ensure_ascii=False, indent=0)
    open(q, "a", encoding="utf-8").write("")
print("ok V646")
