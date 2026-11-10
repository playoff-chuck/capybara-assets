#!/usr/bin/env python3
# V556: Übersetzung findet Texte auch mit Symbol davor/dahinter (▲ ▼ ★ ✈ 👁 🔒 … / ▶ ›) – z. B. Joker-Effekte «▲ Height bonus doubled».
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V555";', 'const GAME_VER = "V556";')
rep('v = i18nLookup(key); if (v == null) v = i18nCI(key); if (v == null) {',
    'v = i18nLookup(key); if (v == null) v = i18nCI(key); if (v == null) v = i18nSym(key); if (v == null) {')
rep('function i18nApplyAll() {', '''function i18nSym(key) {   /* V556: Symbol vorne/hinten abtrennen, Kern übersetzen */
  const m = key.match(/^([\\s▲▼▶►◀•★☆✈♥☠⚡✉🔒🎟👁\\p{Extended_Pictographic}\\uFE0F]+)?(.*?)([\\s▶›]+)?$/u);
  if (!m || !(m[1] || m[3]) || !m[2] || !/[A-Za-z]{2}/.test(m[2])) return null;
  let c = i18nLookup(m[2]); if (c == null) c = i18nCI(m[2]); return c == null ? null : (m[1] || "") + c + (m[3] || ""); }
function i18nApplyAll() {''')
open(dst, "w", encoding="utf-8").write(s)
print("ok")
