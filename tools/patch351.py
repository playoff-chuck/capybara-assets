"""V351 (Martin 07.11. 00:29): Easter Eggs im Stil von Afrika (Capybara-Gesicht) für alle Kontinente:
Südamerika Capybara mit Blüte im Dschungel · Asien Capybara mit Strohhut, Kirschblüten, rotes Gewand ·
Nordamerika Capybara mit Cowboyhut und Halstuch · Antarktis Capybara mit Wintermütze und Schal im Schnee.
(Jeder Kontinent weiterhin nur 1× pro Spiel.)"""
import sys, re
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V350";', 'const GAME_VER = "V351";')
NEW = {
 "samerica": '{ k: "samerica", m: ["GgggpppgGg", "gTTgpypTTg", "ggttttttgg", "gtkttttktg", "gttttttttg", "gttTTTTttg", "gttTkkTttg", "ggttttttgg", "GGGttttGGG", "GGttttttGG", "GgttttttgG", "GGGGGGGGGG"], gap: [[3, 4], [4, 4], [5, 4], [6, 4]] }',
 "asia": '{ k: "asia", m: ["aaaasaaapa", "apasssaaaa", "assssssssa", "annnnnnnna", "aattttttaa", "atkttttkta", "atttttttta", "attTTTTtta", "attTkkTtta", "aattttttaa", "arrrrrrrra", "rrrrrrrrrr"], gap: [[3, 6], [4, 6], [5, 6], [6, 6]] }',
 "namerica": '{ k: "namerica", m: ["aaaaaaaaya", "aaaNNNNaaa", "aaNyyyyNaa", "nnnnnnnnnn", "aTttttttTa", "atkttttkta", "atttttttta", "attTTTTtta", "attTkkTtta", "aattttttaa", "arrrrrrrra", "gggggggggg"], gap: [[3, 6], [4, 6], [5, 6], [6, 6]] }',
 "antarctica": '{ k: "antarctica", m: ["ccccwwcccc", "cccbbbbccc", "ccbbbbbbcc", "cwwwwwwwwc", "cTttttttTc", "ctkttttktc", "cttttttttc", "cttTTTTttc", "cttTkkTttc", "ccrrrrrrcc", "wwttrrttww", "wwwwwwwwww"], gap: [[3, 6], [4, 6], [5, 6], [6, 6]] }',
}
for k, v in NEW.items():
    rows = re.findall(r'"([a-zA-Z]{10})"', v.split("m: ")[1]); assert len(rows) == 12, k
    s, n = re.subn(r'\{ k: "' + k + r'", m: \[[^\]]*\], gap: \[(?:\[\d+, \d+\](?:, )?)+\] \}', v, s); assert n == 1, (k, n)
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
