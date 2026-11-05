"""V300 (Martin 19:44): Air-Drops sehen nicht mehr aus wie Werbung. Eigenes ruhiges Blau, Bezeichnung «AIR DROP»,
keine Sternplaketten, kein Schrägband, keine durchgestrichenen Preise, keine Reklame-Sprüche."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V299";', 'const GAME_VER = "V300";')

# Texte ruhig, ohne Reklame
old_start = s.index('      const D = { ton: { img: "img/ad_drop_free.webp"')
old_end = s.index('}[kind];', old_start) + len('}[kind];')
s = s[:old_start] + '''      const D = { ton: { img: "img/ad_drop_free.webp", name: "TEN-TON DROP", line: "HQ sent you a Ten-ton drop. It's already in your Pocket.", met: ["+1 Ten-ton", "In your Pocket"], btn: "THANKS! ▶" },
                 sweep: { img: "img/ad_drop_free.webp", name: "CLEAN SWEEP", line: "You cleared the whole field. HQ sent gold and a medal.", met: [`${gold} gold`, "+1 medal"], btn: "COLLECT ▶" },
                 med: { img: "img/ad_med_free.webp", name: "MEDKIT", line: "Doc Hazel patched you up. You can see clearly again.", met: ["Vision clear"], btn: "THANKS, DOC ▶" },
                 rot: { img: "img/ad_drop_free.webp", name: `${o.rp || "+90°"} PACKAGE`, line: "The field is upright again. Blocks fall down as usual.", met: ["Field upright"], btn: "LET'S GO ▶" } }[kind];''' + s[old_end:]

# Kein Sale/Free-Look: nur Klasse «drop», keine Plaketten-/Preisfelder
rep('''      if (!D) return; cur = "drop"; saleMode = true; isFree = true; dropBtn = D.btn; late = true; S.intro = true; S.adOpen = true;
      const card = $a("adCard"); card.classList.add("sale", "free", "drop"); const PS = [[14, 40], [14, 76], [52, 86]];
      [1, 2, 3].forEach(n => { const el = card.querySelector(".saleSt.s" + n); if (el) { el.style.left = PS[n - 1][0] + "%"; el.style.top = PS[n - 1][1] + "%"; el.textContent = D.st[n - 1]; } });
      $a("adPic").style.backgroundImage = `url(${D.img})`; $a("adPic").style.backgroundPosition = ""; $a("adTag").textContent = "FREE"; $a("adWave").textContent = `WAVE ${S.wave}`; $a("adPrice").textContent = D.price;
      $a("adName").textContent = D.name; $a("adLine").textContent = D.line; $a("adMet").innerHTML = D.met.map(x => `<span>${x}</span>`).join("");
      $a("saleWas").textContent = D.was; $a("saleWas").hidden = !D.was; $a("saleNow").textContent = D.now; $a("salePct").textContent = D.pct;
      card.querySelector(".saleMega").textContent = D.mega; card.querySelector(".saleOnly").textContent = D.only;''',
'''      if (!D) return; cur = "drop"; saleMode = false; isFree = true; dropBtn = D.btn; late = true; S.intro = true; S.adOpen = true;
      const card = $a("adCard"); card.classList.remove("sale", "free"); card.classList.add("drop");
      $a("adPic").style.backgroundImage = `url(${D.img})`; $a("adPic").style.backgroundPosition = ""; $a("adTag").textContent = "✈ AIR DROP"; $a("adWave").textContent = `WAVE ${S.wave}`; $a("adPrice").textContent = "";
      $a("adName").textContent = D.name; $a("adLine").textContent = D.line; $a("adMet").innerHTML = D.met.map(x => `<span>${x}</span>`).join("");''')
rep('if (k === "drop") { bought = false; $a("adCard").classList.remove("drop"); $a("saleWas").hidden = false; }',
    'if (k === "drop") { bought = false; $a("adCard").classList.remove("drop"); }')

rep('''<style id="v299drop">
.adCard.drop #saleWas[hidden]{display:none}
.adCard.drop .salePrice #salePct{white-space:nowrap}
</style>''', '''<style id="v300drop">
#ovAd:has(.adCard.drop){background:rgba(10,30,55,.62)}
.adCard.drop{background:linear-gradient(180deg,#eef7ff,#d6ebff);border-color:#123a63}
.adCard.drop .adPic{border-bottom-color:#123a63}
.adCard.drop .adPic:after{background:linear-gradient(180deg,rgba(0,0,0,0) 65%,rgba(18,58,99,.3))}
.adCard.drop .saleSt,.adCard.drop .saleHead,.adCard.drop .salePrice,.adCard.drop .adPrice{display:none!important}
.adCard.drop .adTag{background:#2f7fd1!important;color:#fff!important;border:2px solid #123a63!important;animation:none!important;transform:none!important;left:10px!important;top:10px!important;width:auto!important;letter-spacing:1px}
.adCard.drop .adWave{background:#eef7ff;color:#123a63;border-color:#123a63}
.adCard.drop .adBody h2{font-size:34px;color:#2f7fd1;-webkit-text-stroke:1.2px #123a63;text-shadow:none}
.adCard.drop .adBody p{color:#123a63;min-height:0;margin:6px 0 10px}
.adCard.drop .adMet{display:flex!important}
.adCard.drop .adMet span{background:#cfe4fa;color:#123a63}
.adCard.drop #adFree{background:linear-gradient(180deg,#5aa7f0,#2f7fd1)!important;color:#fff!important;border:3px solid #123a63!important;box-shadow:0 4px 0 #123a63!important}
.adCard.drop #adFree:after{display:none!important}
</style>''')
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
