#!/usr/bin/env python3
# V585 (Martin 11.11. 01:16): Zufallsnamen (🎲 beim Namen) auf Russisch, wenn das Spiel auf Russisch läuft
# + Bestenliste: kyrillische Namen gingen bisher als «Anonymous» an den Server (apiNick erlaubte nur A–Z) – jetzt alle Buchstaben
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V584";', 'const GAME_VER = "V585";')
rep('function funNick() { for (let i = 0; i < 20; i++) { const n = FN_A[Math.random() * FN_A.length | 0] + " " + FN_B[Math.random() * FN_B.length | 0]; if (n.length <= 14) return n; } return "Capy " + (100 + Math.random() * 900 | 0); }',
    '''const FN_RU_A = ["Капитан", "Майор", "Сержант", "Лихой", "Шустрый", "Хитрый", "Бравый", "Весёлый", "Ловкий", "Удалой", "Смелый", "Мудрый", "Турбо", "Супер"], FN_RU_B = ["Пряник", "Бублик", "Кекс", "Пончик", "Сырник", "Орешек", "Кокос", "Манго", "Вареник", "Огурчик", "Блинчик", "Пельмень", "Барсук", "Плюх"];   /* V585 */
function funNick() { const ru = (I18N.lang || "") === "ru", A = ru ? FN_RU_A : FN_A, B = ru ? FN_RU_B : FN_B;
  for (let i = 0; i < 30; i++) { const n = A[Math.random() * A.length | 0] + " " + B[Math.random() * B.length | 0]; if (n.length <= 14) return n; } return (ru ? "Капи " : "Capy ") + (100 + Math.random() * 900 | 0); }''')
rep('apiNick = n => (String(n || "").replace(/[^A-Za-z0-9 _-]/g, "").trim().slice(0, 16) || "Anonymous").padEnd(2, "_")',
    'apiNick = n => (String(n || "").replace(/[^\\p{L}0-9 _-]/gu, "").replace(/\\s+/g, " ").trim().slice(0, 16) || "Anonymous").padEnd(2, "_")   /* V585: auch kyrillisch */')
open(dst, "w", encoding="utf-8").write(s)
print("ok V585")
