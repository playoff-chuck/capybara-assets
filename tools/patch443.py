#!/usr/bin/env python3
"""V443: Reichweiten-Vorschau für jede Waffe – auch Frost und auch, wenn die Waffe gesperrt ist oder das Gold nicht reicht
(Knöpfe sind dann nicht mehr «disabled», sondern grau «off»: Halten zeigt die Zone, Tippen kauft nicht). (Martin 08.11. 12:05)
Nutzung: python3 tools/patch443.py src dst"""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()

def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (c, a[:80])
    s = s.replace(a, b)

rep('GAME_VER = "V442"', 'GAME_VER = "V443"')
rep('.peekTip{font-size:12px;', '#sheet button.off{filter:grayscale(.7) brightness(.7);opacity:.6;cursor:default}#sheet button.off:active{transform:none}\n.peekTip{font-size:12px;')
rep('<button data-buy="${k}" data-slot="${i}" ${S.gold < b.cost ? "disabled" : ""}>',
    '<button data-buy="${k}" data-slot="${i}" class="${S.gold < b.cost ? "off" : ""}">')
rep(': `<button disabled><span style="color:${b.col}">${b.name}</span><small>🔒 wave ${unlockedAt(k)}</small></button>`',
    ': `<button class="off" data-peek="${k}"><span style="color:${b.col}">${b.name}</span><small>🔒 wave ${unlockedAt(k)}</small></button>`')
rep('<button data-up="${i}" ${max || S.gold < c ? "disabled" : ""}>',
    '<button data-up="${i}" ${max ? "disabled" : ""} class="${!max && S.gold < c ? "off" : ""}">')
# Tippen auf grauen Knopf: nichts kaufen
rep('''$("sheet").addEventListener("click", e => {
  const b = e.target.closest("button"); if (!b) return;
  if (b.dataset.shop) {''',
'''$("sheet").addEventListener("click", e => {
  const b = e.target.closest("button"); if (!b) return;
  if (b.classList.contains("off")) { snd("nope"); return; }   /* V443: gesperrt / zu wenig Gold – nur Vorschau */
  if (b.dataset.shop) {''')
# Halten auch auf gesperrten Waffen
rep('const b = e.target.closest("button[data-buy],button[data-up],.wline"); if (!b || !S || !S.sel) return;\n    let type, lvl; if (b.dataset.buy) { type = b.dataset.buy; lvl = 1; }',
    'const b = e.target.closest("button[data-buy],button[data-peek],button[data-up],.wline"); if (!b || !S || !S.sel) return;\n    let type, lvl; if (b.dataset.buy || b.dataset.peek) { type = b.dataset.buy || b.dataset.peek; lvl = 1; }')
open(dst, "w", encoding="utf-8").write(s)
print("ok", dst)
