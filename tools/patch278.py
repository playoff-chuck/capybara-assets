"""V278 (Martin 16:18/16:19):
- «Back to back!»-Clip hatte ein zweites «Back» am Ende (0,88–1,18 s) → auf 0,66 s gekürzt mit Ausblendung (ffmpeg, 22,05 kHz mono 48 kbit/s).
  Alle 124 Clips geprüft (Pausen + Lautstärke danach): nur dieser hatte ein Zusatzwort.
- Buchhalter höchstens alle 3 min (übersprungene Marken verfallen).
- Ten-ton-Geschenk W5 als echte Gratis-Werbung (Sale-Stil, FREE, −100 %, «AWESOME! · IT'S FREE ▶»), kein «Not enough gold» mehr."""
import sys, base64, subprocess, tempfile, os
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V277";', 'const GAME_VER = "V278";')
i = s.index('const VOICE = {'); j = s.index('"b2b":"', i) + len('"b2b":"'); k = s.index('"', j)
td = tempfile.mkdtemp(); a, b = os.path.join(td, 'a.mp3'), os.path.join(td, 'b.mp3')
open(a, 'wb').write(base64.b64decode(s[j:k]))
subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', a, '-af', 'atrim=0:0.66,afade=t=out:st=0.56:d=0.1', '-ar', '22050', '-ac', '1', '-b:a', '48k', b], check=True)
s = s[:j] + base64.b64encode(open(b, 'rb').read()).decode() + s[k:]
rep('function bookkeeper(score, mark) { msgPush(',
    'function bookkeeper(score, mark) { const bn = performance.now(); if (bn - (window.__bookLast || -1e9) < 180000) return; window.__bookLast = bn; msgPush(')
rep('show("ton", false)', 'show("ton", "free")')
rep('function show(k, sale) { cur = k; saleMode = !!sale; const a = AD[k], d = INTRO_GEAR[k];',
    'function show(k, sale) { const free = sale === "free"; if (free) sale = true; cur = k; saleMode = !!sale; isFree = free; const a = AD[k], d = INTRO_GEAR[k];')
rep('''      try { snd("radio"); } catch (e) {} }
    function close(bought) {''',
    '''      { const card = $a("adCard"); card.classList.toggle("free", free); const s2 = card.querySelector(".saleSt.s2"), s3 = card.querySelector(".saleSt.s3"), mg = card.querySelector(".saleMega"), on = card.querySelector(".saleOnly");
        if (free) { const p = price(k); $a("saleWas").textContent = `${p} GOLD`; $a("saleNow").textContent = "FREE"; $a("salePct").textContent = "−100%"; $a("saleS1").textContent = "−100%"; s2.textContent = "GIFT!"; s3.textContent = "FREE"; mg.textContent = "FREE GIFT"; on.textContent = "ON THE HOUSE!"; $a("adTag").textContent = "FREE"; $a("adLine").textContent = a.line; $a("adPic").style.backgroundImage = `url(${a.sale})`; }
        else { s2.textContent = "HOT!"; s3.textContent = "DEAL"; mg.textContent = "MEGA DEAL"; on.textContent = "ONLY THIS WAVE!"; }
        paint(); }
      try { snd("radio"); } catch (e) {} }
    function close(bought) {''')
rep('function paint() { const k = cur, w = why(k), act = $a("adAct"), sale = $a("adCard").classList.contains("sale");',
    'function paint() { if (isFree) { $a("adAct").innerHTML = `<button class="btn-accent" id="adFree">AWESOME! · IT\'S FREE ▶</button>`; $a("adLater").textContent = ""; $a("adLater").hidden = true; return; } $a("adLater").hidden = false; const k = cur, w = why(k), act = $a("adAct"), sale = $a("adCard").classList.contains("sale");')
rep('let saleMode = false;', 'let saleMode = false, isFree = false;')
rep('let lastW = null; setInterval(() => { if (!ov.hidden && cur) {', 'let lastW = null; setInterval(() => { if (!ov.hidden && cur && !isFree) {')
rep('if (e.target.closest("#adBuy")) buy();', 'if (e.target.closest("#adFree")) { try { snd("uiTap"); } catch (er) {} isFree = false; close(true); } else if (e.target.closest("#adBuy")) buy();')
css = r'''
<style id="v278free">
.adCard.free .salePrice{display:flex}
.adCard.free #saleNow{color:#1f9d55}
.adCard.free .saleMega{color:#1f9d55}
</style>
'''
i = s.rindex('</body>'); s = s[:i] + css + s[i:]
open(dst, 'w', encoding='utf-8').write(s)
