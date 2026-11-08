#!/usr/bin/env python3
"""V474-Sprachprüfung (Martin 08.11. 20:19): alle Screens in allen Sprachen, zwei Fehlerarten:
 (a) englischer Text geblieben – sichtbarer Text ist ein Schlüssel aus en.json, dessen Übersetzung anders lautet
     (ergänzt I18N.miss, das Texte ohne Übersetzung meldet);
 (b) Text geht sich nicht aus – Element breiter als sein Clip-Vorfahre/Viewport, nowrap-abgeschnitten, ungewollter Umbruch.
Aufruf: python3 tools/i18n_crawl2.py <site> <out> <lang> <port> [w h]   → out/<lang>_<w>_*.png, out/report_<lang>_<w>.json"""
import sys, subprocess, time, os, json, re
from playwright.sync_api import sync_playwright
site, out, lang, port = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
W, H = (int(sys.argv[5]), int(sys.argv[6])) if len(sys.argv) > 6 else (412, 915)
os.makedirs(out, exist_ok=True)
EN = json.load(open(os.path.join(site, "lang/en.json"), encoding="utf-8"))
LG = json.load(open(os.path.join(site, f"lang/{lang}.json"), encoding="utf-8")) if lang != "en" else {}
NUM = re.compile(r"\d[\d.,:/]*\d|\d")
NAMES = set("SKULLGROG GORKAZAR FROSTGNAW GRUMBLEFANG Capybara Squad CAPYBARA SQUAD English Español Português Deutsch Русский Rosie Blue ROSIE BLUE XP PTS OK DEV AA Bug KEYS HQ-2 TT-7 Captain Noodle Fuzzy Waffle Mart MG L1 L2 L3".split()) | {"Capybara Squad","Captain Noodle","Fuzzy Waffle","DEV · TEST ACCESS","Airport Bossa","Winter Lantern","Chill Disco Rio","CAPYBARA SQUAD"}
srv = subprocess.Popen([sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1"], cwd=site, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(0.8)
REP = {}; tag = f"{lang}_{W}"
JS_TEXTS = """(()=>{const res=[];const vw=innerWidth,vh=innerHeight;
 function clipAnc(e){let a=e.parentElement;while(a&&a!==document.body){const cs=getComputedStyle(a);if(cs.overflow!=='visible'||cs.overflowX!=='visible')return a;a=a.parentElement;}return null;}
 const walker=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;
 while(n=walker.nextNode()){const t=n.textContent.replace(/\\s+/g,' ').trim();if(!t||t.length<2)continue;const e=n.parentElement;if(!e)continue;
  if(['SCRIPT','STYLE','NOSCRIPT'].includes(e.tagName))continue;const cs=getComputedStyle(e);if(cs.visibility==='hidden'||cs.display==='none'||+cs.opacity===0)continue;
  const r=document.createRange();r.selectNodeContents(n);const b=r.getBoundingClientRect();if(!b.width||!b.height)continue;if(b.bottom<0||b.top>vh||b.right<0||b.left>vw)continue;
  let why=null,ex=0;const ca=clipAnc(e);
  if(ca){const cb=ca.getBoundingClientRect();if(b.right>cb.right+2){why='clipped';ex=Math.round(b.right-cb.right);}else if(b.left<cb.left-2){why='clipped-left';ex=Math.round(cb.left-b.left);}}
  if(!why&&b.right>vw+2){why='offscreen';ex=Math.round(b.right-vw);}
  if(!why&&cs.whiteSpace==='nowrap'&&e.scrollWidth>e.clientWidth+2&&cs.overflow!=='visible'){why='nowrap-cut';ex=e.scrollWidth-e.clientWidth;}
  if(!why){const lh=parseFloat(cs.lineHeight)||parseFloat(cs.fontSize)*1.2;if(['BUTTON','B','EM','SMALL','H2','H4','I'].includes(e.tagName)&&b.height>lh*1.6&&t.length<40&&e.childNodes.length===1&&/[ \-]/.test(t)){why='wrapped';ex=Math.round(b.height/lh);}}
  res.push({t,tag:e.tagName,id:e.id||'',cls:(e.className&&e.className.baseVal!==undefined?e.className.baseVal:e.className||'').toString().slice(0,40),why,ex,notr:!!e.closest('[translate=no]')});}
 return res;})()"""
def check(pg, name):
    pg.screenshot(path=f"{out}/{tag}_{name}.png")
    try: items = pg.evaluate(JS_TEXTS)
    except Exception as e: items = []
    bad = []
    for it in items:
        t = it["t"]
        if it["why"]: bad.append({"why": it["why"], "ex": it["ex"], "t": t[:70], "el": f'{it["tag"]}#{it["id"]}.{it["cls"]}'})
        if lang != "en" and not it["notr"]:
            # englisch geblieben? Text (oder sein #-Muster) ist en-Schlüssel mit abweichender Übersetzung
            keys = [t, NUM.sub("#", t)]
            hit = False
            for k in keys:
                if k in EN and k not in NAMES and not (k in LG and (LG[k] == t or LG[k] == NUM.sub("#", t) or LG[k] == k)):
                    bad.append({"why": "english" if k in LG else "english-nokey", "t": t[:70], "el": f'{it["tag"]}#{it["id"]}.{it["cls"]}', "want": LG.get(k, "")[:60]}); hit = True; break
            if not hit and lang == "ru" and re.search(r"[A-Za-z]{3,}", t) and not re.search(r"[А-Яа-яЁё]", t) and t not in NAMES and not NUM.sub("#", t) in NAMES:
                bad.append({"why": "latin-in-ru", "t": t[:70], "el": f'{it["tag"]}#{it["id"]}.{it["cls"]}'}); hit = True
            if not hit:
                # Teile «A · B»
                if " · " in t:
                    for part in t.split(" · "):
                        pk = NUM.sub("#", part.strip())
                        if pk in LG and LG[pk] != pk and pk != "#" and len(pk) > 2: bad.append({"why": "english-part", "t": t[:70], "part": part, "el": f'{it["tag"]}#{it["id"]}.{it["cls"]}', "want": LG[pk][:60]}); break
    if bad: REP[name] = bad
try:
  with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
    ctx = b.new_context(viewport={"width": W, "height": H}, device_scale_factor=1, is_mobile=True, has_touch=True)
    def api(r):
        u = r.request.url
        if "/nuts" in u: r.fulfill(status=200, content_type="application/json", body=json.dumps({"list": [{"callsign": "Fuzzy Waffle", "level": 12, "kills": 300, "t": 1}]}))
        else: r.fulfill(status=200, content_type="application/json", body=json.dumps({"list": [{"name": "Captain Noodle", "score": 12345, "wave": 42, "t": 1}]}))
    ctx.route("**/api/**", api)
    pg = ctx.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.add_init_script(f"localStorage.setItem('capy-reset','276');localStorage.setItem('tarnturm-terms','1');localStorage.setItem('tarnturm-tut','1');localStorage.setItem('capy-lang','{lang}');localStorage.setItem('tarnturm-hs-pro', JSON.stringify([{{name:'Mart',score:6216,wave:7,t:1}}]));localStorage.setItem('capy-stars', JSON.stringify({{0:5,1:4}}));localStorage.setItem('capy-place-rec', JSON.stringify({{0:{{k:123,l:4}},1:{{k:88,l:2}}}}));localStorage.setItem('tarnturm-cp-pro','25');")
    pg.goto(f"http://127.0.0.1:{port}/index.html?lang={lang}&test=daily"); pg.wait_for_timeout(2500)
    if pg.query_selector("#ovLang"): check(pg, "00_lang"); pg.evaluate(f"document.querySelector('#ovLang [data-lang={lang}]')?.click()"); pg.wait_for_timeout(1200)
    check(pg, "01_splash"); pg.mouse.click(W // 2, int(H * 0.76)); pg.wait_for_timeout(2500)
    check(pg, "02_start")
    if pg.query_selector("#dailyLeaf"):
        pg.evaluate("document.getElementById('dailyLeaf').click()"); pg.wait_for_timeout(600); check(pg, "03_daily")
        pg.evaluate("document.querySelector('#ovDaily .dlClaim')?.click()"); pg.wait_for_timeout(500); check(pg, "03b_daily_claimed")
        pg.evaluate("document.querySelector('#ovDaily .dlX').click()"); pg.wait_for_timeout(400); check(pg, "03c_start_claimed")
    pg.evaluate("document.getElementById('btnSettings') ? document.getElementById('btnSettings').click() : document.querySelector('[aria-label=Settings]')?.click()"); pg.wait_for_timeout(700); check(pg, "04_settings")
    pg.evaluate("document.getElementById('setX').click()"); pg.wait_for_timeout(300)
    pg.evaluate("document.getElementById('btnInfo').click()"); pg.wait_for_timeout(600); check(pg, "05_guide_rules")
    pg.evaluate("document.querySelector('#infoTabs [data-tab=mon]').click()"); pg.wait_for_timeout(500); check(pg, "06_guide_monsters")
    pg.evaluate("document.querySelector('#infoTabs [data-tab=arms]').click()"); pg.wait_for_timeout(500); check(pg, "07_guide_gadgets")
    pg.evaluate("document.querySelector('#ovInfo .manual:not([hidden])') && (document.querySelector('#ovInfo .manual:not([hidden])').scrollTop=9999)"); pg.wait_for_timeout(300); check(pg, "07b_guide_gadgets2")
    pg.evaluate("document.getElementById('btnInfoClose').click()"); pg.wait_for_timeout(300)
    pg.evaluate("document.getElementById('btnHs').click()"); pg.wait_for_timeout(900); check(pg, "08_medals")
    pg.evaluate("document.querySelector('#awBar [data-aw=hof]').click()"); pg.wait_for_timeout(1200); check(pg, "09_hof")
    pg.evaluate("document.querySelector('#awBar [data-aw=squad]').click()"); pg.wait_for_timeout(900); check(pg, "10_squad")
    pg.evaluate("document.getElementById('sqBody').scrollTop=9999; document.querySelector('#ovSquad .albBox').scrollTop=9999"); pg.wait_for_timeout(300); check(pg, "10b_squad2")
    pg.evaluate("document.getElementById('sqX').click()"); pg.wait_for_timeout(300)
    pg.evaluate("document.getElementById('btnMap').click()"); pg.wait_for_timeout(1800); check(pg, "11_map")
    pg.evaluate("document.querySelector('#ovMap .mapWorldBtn')?.click()"); pg.wait_for_timeout(1200); check(pg, "12_map_world")
    pg.evaluate("document.querySelector('#ovMap .mapClose').click()"); pg.wait_for_timeout(400)
    # Spiel: Lauf ab W1 ohne Tutorial
    pg.evaluate("window.__TT.startGame('chill', 1)"); pg.wait_for_timeout(3000); check(pg, "15_game_w1")
    pg.evaluate("document.getElementById('btnShop') ? document.getElementById('btnShop').click() : document.querySelector('[data-k=shop],[aria-label=Shop]')?.click()"); pg.wait_for_timeout(700); check(pg, "16_shop")
    pg.evaluate("document.getElementById('sheetX') ? document.getElementById('sheetX').click() : document.querySelector('#sheet .xBtn')?.click()"); pg.wait_for_timeout(400)
    pg.evaluate("document.getElementById('btnPause') ? document.getElementById('btnPause').click() : document.querySelector('.pauseBtn')?.click()"); pg.wait_for_timeout(600); check(pg, "17_pause")
    pg.evaluate("document.getElementById('btnPResume')?.click()"); pg.wait_for_timeout(400)
    pg.evaluate("window.__TT.S.wave=5; window.__TT.S.waveCD=0.01"); pg.wait_for_timeout(4000); check(pg, "18_game_w6")
    pg.wait_for_timeout(6000); check(pg, "19_game_w6b")
    # gespeicherter Lauf → Startscreen mit CONTINUE (btnResume)
    try:
        pg.evaluate("window.__TT.S.score=10280; Object.defineProperty(document,'hidden',{get:()=>true,configurable:true}); document.dispatchEvent(new Event('visibilitychange'))"); pg.wait_for_timeout(300)
        pg.goto(f"http://127.0.0.1:{port}/index.html?lang={lang}"); pg.wait_for_timeout(2000); pg.mouse.click(W // 2, int(H * 0.76)); pg.wait_for_timeout(2500); check(pg, "22_start_resume")
        pg.evaluate("document.getElementById('btnMap').click()"); pg.wait_for_timeout(1800); check(pg, "23_map_resume"); pg.evaluate("document.querySelector('#ovMap .mapClose').click()"); pg.wait_for_timeout(300)
        pg.evaluate("document.getElementById('btnResume').click()"); pg.wait_for_timeout(1500); check(pg, "24_camp"); pg.wait_for_timeout(5000); check(pg, "25_resumed")
    except Exception as e: errs.append("resume:" + str(e)[:80])
    # Nuts über den Testlink
    try:
        pg.goto(f"http://127.0.0.1:{port}/index.html?lang={lang}&test=nuts"); pg.wait_for_timeout(1500); pg.mouse.click(W // 2, int(H * 0.76)); pg.wait_for_timeout(9000); check(pg, "21_nuts")
        pg.evaluate("document.getElementById('btnPause') ? document.getElementById('btnPause').click() : document.querySelector('.pauseBtn')?.click()"); pg.wait_for_timeout(600); check(pg, "21b_nuts_pause")
        pg.evaluate("document.getElementById('btnPResume')?.click()"); pg.wait_for_timeout(400)
    except Exception as e: errs.append("nuts:" + str(e)[:80])
    pg.evaluate("window.__TT.S.lives=0; window.__TT.S.monsters.push({x:1,y:1,cx:1,cy:1,prog:0,trav:0,hp:1,max:1,speed:1,kind:'norm',slowT:0,next:null,chew:false,dead:false,reward:1,dir:0,ph:0,hits:0})"); pg.wait_for_timeout(3500); check(pg, "20_over")
    try: miss = pg.evaluate("window.__i18n ? window.__i18n.miss() : (window.I18N&&I18N.miss?[...I18N.miss]:[])")
    except Exception: miss = []
    json.dump({"report": REP, "miss": miss, "errors": errs}, open(f"{out}/report_{tag}.json", "w"), ensure_ascii=False, indent=1)
    nbad = sum(len(v) for v in REP.values())
    print("lang", lang, W, "findings", nbad, "miss", len(miss), "errors", errs[:2])
    b.close()
finally: srv.terminate()
