#!/usr/bin/env python3
# V613 (Martin 11.11. 12:16 Ortszeit): Tutorial-Werbebanner bekommt das Wort «Ликбез» (EN Crash Course) als Aufkleber oben rechts.
import sys, os, json
site = sys.argv[1]; p = os.path.join(site, "index.html"); s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V612";', 'const GAME_VER = "V613";')
rep('<button id="setReTut" class="tutBanner" type="button"><span class="tbTxt">',
    '<button id="setReTut" class="tutBanner" type="button"><span class="tbTag">CRASH COURSE</span><span class="tbTxt">')
rep('#ovSettings .tutBanner .tbGo{', '''#ovSettings .tutBanner .tbTag{position:absolute;top:-12px;right:12px;padding:3px 10px 1px;background:#ff5a5f;color:#fff;border:2px solid var(--ink,#3a1d10);border-radius:8px;transform:rotate(4deg);font-family:var(--f-display,Bangers,Impact,sans-serif);font-size:17px;line-height:1.1;letter-spacing:.06em;text-shadow:0 2px 0 #8a1f22;box-shadow:0 3px 0 var(--ink,#3a1d10);white-space:nowrap;pointer-events:none}
#ovSettings .tutBanner .tbGo{''')
open(p, "w", encoding="utf-8").write(s)
T = {"en": "CRASH COURSE", "ru": "ЛИКБЕЗ", "de": "CRASHKURS", "es": "CURSO EXPRÉS", "pt": "CURSO RÁPIDO"}
for l, v in T.items():
    q = os.path.join(site, "lang", l + ".json"); d = json.loads(open(q, encoding="utf-8").read()); d["CRASH COURSE"] = v
    open(q, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=0))
print("ok V613")
