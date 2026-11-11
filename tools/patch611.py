#!/usr/bin/env python3
# V611 (Martin 11.11. 12:00): Einstellungen → Knopf zur VK-Gruppe vk.ru/playcapybarasquad (unter «Invite friends»).
import sys, os, json
site = sys.argv[1]; p = os.path.join(site, "index.html"); s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V610";', 'const GAME_VER = "V611";')
rep('<small id="setInvN">Friends get a free Ten-ton drop</small></div>',
    '<small id="setInvN">Friends get a free Ten-ton drop</small><a id="setVk" class="vkBtn" href="https://vk.ru/playcapybarasquad" target="_blank" rel="noopener">JOIN US ON VK</a><small>News, records and your ideas</small></div>')
rep('#ovSettings .setInv small{font-size:12px;font-weight:700;color:#9b7a5c;text-align:center;line-height:1.25}',
    '#ovSettings .setInv small{font-size:12px;font-weight:700;color:#9b7a5c;text-align:center;line-height:1.25}\n#ovSettings .setInv .vkBtn{display:inline-flex;align-items:center;justify-content:center;height:38px;padding:0 18px;margin-top:6px;border-radius:12px;background:#0077ff;color:#fff;font-family:var(--f-display,Bangers,system-ui);font-size:18px;letter-spacing:.04em;text-decoration:none;border:3px solid var(--ink,#3a1d10);box-shadow:0 3px 0 var(--ink,#3a1d10)}   /* V611 */')
open(p, "w", encoding="utf-8").write(s)
T = {"en": {"JOIN US ON VK": "JOIN US ON VK", "News, records and your ideas": "News, records and your ideas"},
     "ru": {"JOIN US ON VK": "МЫ ВО ВКОНТАКТЕ", "News, records and your ideas": "Новости, рекорды и ваши идеи"},
     "de": {"JOIN US ON VK": "FOLGE UNS AUF VK", "News, records and your ideas": "News, Rekorde und eure Ideen"},
     "es": {"JOIN US ON VK": "SÍGUENOS EN VK", "News, records and your ideas": "Noticias, récords y tus ideas"},
     "pt": {"JOIN US ON VK": "SIGA-NOS NO VK", "News, records and your ideas": "Novidades, recordes e suas ideias"}}
for l, m in T.items():
    q = os.path.join(site, "lang", l + ".json"); d = json.loads(open(q, encoding="utf-8").read()); d.update(m)
    open(q, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=0))
print("ok V611")
