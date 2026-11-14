# V714: Megatest-Bot korrigiert (Entscheidungen 13.11.2026): D8 misst echte Monster-Bewegung statt S.paused,
#  C7 zählt die eigenen Suchwörter des Bots nicht mehr als «nicht übersetzt», C1 «ragt aus dem Bildschirm» ohne gedrehte Bänder/Animationen.
import re
p = 'tools/megatest/megatest.py'; s = open(p).read()
a = "(()=>{try{const q=String(window.__i18n.T(p)).toUpperCase();"
assert s.count(a) == 1
s = s.replace(a, "(()=>{try{(window.__botW=window.__botW||new Set()).add(p);const q=String(window.__i18n.T(p)).toUpperCase();")
b = "for (const x of m.slice(-20)) add('C7'"
assert s.count(b) == 1
s = s.replace(b, "for (const x of m.slice(-20).filter(x => !(window.__botW && window.__botW.has(x)))) add('C7'")
c = "const r = R(e); if (r.width > 4 && (r.right > innerWidth + 2 || r.left < -2)) add('C1', 'vp:' + txt"
assert s.count(c) == 1
s = s.replace(c, "const r = R(e); if (r.width > 4 && (r.right > innerWidth + 2 || r.left < -2) && cs.transform === 'none' && !e.closest('.adTag,.saleSt') && !e.getAnimations().length) add('C1', 'vp:' + txt")
open(p, 'w').write(s)
p = 'tools/megatest/extra.js'; s = open(p).read()
old = re.search(r"    if \(stopIds\.length && S\.inWave && !S\.paused && !S\.duel\) \{ inWSince \+= 500;[^\n]*\n", s).group(0)
new = ("    if (stopIds.length && S.inWave && !S.duel) { const pos = (S.monsters || []).slice(0, 8).map(m => Math.round((m.x || 0) * 20) + ',' + Math.round((m.y || 0) * 20)).join('|');   /* V714: echte Bewegung messen statt S.paused */\n"
       "      if (d8Pos === null) { d8Pos = pos; inWSince = 0; } else { inWSince += 500; if (inWSince >= 2500) { if (pos !== d8Pos && (S.monsters || []).length) add('D8', stopIds.join('+'), `Monster bewegen sich hinter Fenster ${stopIds.join(', ')}`); d8Pos = pos; inWSince = 0; } } } else { d8Pos = null; inWSince = 0; }\n")
s = s.replace(old, new)
s = s.replace("inWSince = 0", "inWSince = 0, d8Pos = null", 1)
open(p, 'w').write(s)
print("ok")
