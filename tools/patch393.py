"""V393: Wild Cards zählen als Fenster für Meldungen (Meldungs-Analyse R_4/R_54, V391).
In W20 lief die Lob-/Medaillen-Meldung unter dem Wild-Cards-Fenster weiter bzw. kam während es offen war.
uiWinOpen() kannte ovOrders nicht → jetzt mit S.ordersOpen / ovOrders (Wächter V386, Warteschlange, Angebote, Stimme).
Aufruf: python3 tools/patch393.py site/index.html site/index.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
m = re.search(r'const GAME_VER = "V(\d+)";', s); old = int(m.group(1)); NEW = old + 1
rep(f'const GAME_VER = "V{old}";', f'const GAME_VER = "V{NEW}";')
rep('|| !!(S && (S.joinOpen || S.signOpen || S.banditOpen)); }', '|| v("ovOrders") || !!(S && (S.joinOpen || S.signOpen || S.banditOpen || S.ordersOpen)); }')
open(dst, 'w', encoding='utf-8').write(s); print("ok V%d" % NEW)
