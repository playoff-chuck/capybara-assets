#!/usr/bin/env python3
"""Sammelt alle sichtbaren Texte des Spiels (Sprachschicht V456) und macht Screenshots aller Screens.
Aufruf: python3 tools/i18n_crawl.py <site-ordner> <out-ordner> [lang] [port]
- lang leer/en: Audit-Modus (?i18n=audit) → out/keys.json (alle gesehenen Texte) + Screenshots en_*.png
- lang xx: ?lang=xx → Screenshots xx_*.png + out/miss_xx.json (Texte ohne Übersetzung) + out/overflow_xx.json (Elemente mit Überlauf/ungewolltem Umbruch)"""
import sys, subprocess, time, os, json
from playwright.sync_api import sync_playwright
site, out = sys.argv[1], sys.argv[2]; lang = sys.argv[3] if len(sys.argv) > 3 else "en"; port = int(sys.argv[4]) if len(sys.argv) > 4 else 8470
os.makedirs(out, exist_ok=True)
srv = subprocess.Popen([sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1"], cwd=site, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(0.8)
Q = "?i18n=audit&lang=en" if lang == "en" else f"?lang={lang}"
shots = []
def shot(pg, name):
    pg.screenshot(path=f"{out}/{lang}_{name}.png"); shots.append(name)
    try:
        ov = pg.evaluate("""(()=>{const bad=[];const els=[...document.querySelectorAll('button,b,em,small,span,div,h2,h4,p,label,i')];
          for(const e of els){ if(!e.offsetParent&&e.tagName!=='BODY')continue; const cs=getComputedStyle(e); if(cs.visibility==='hidden'||cs.display==='none')continue;
            const t=(e.childNodes.length===1&&e.firstChild.nodeType===3)?e.textContent.trim():''; if(!t||t.length<2)continue;
            if(e.scrollWidth>e.clientWidth+2&&cs.overflow!=='visible') bad.push({t,why:'overflow',w:e.clientWidth,sw:e.scrollWidth});
            else if(cs.whiteSpace==='nowrap'&&e.scrollWidth>e.clientWidth+2) bad.push({t,why:'nowrap-cut',w:e.clientWidth,sw:e.scrollWidth});
            else { const lh=parseFloat(cs.lineHeight)||parseFloat(cs.fontSize)*1.2; if(['BUTTON','B','EM','SMALL','H2','H4'].includes(e.tagName)&&e.clientHeight>lh*1.6&&!t.includes('\\n')&&t.length<40) bad.push({t,why:'wrapped',h:e.clientHeight,lh}); } }
          return bad;})()""")
        if ov: OVER[name] = ov
    except Exception as e: pass
OVER = {}
try:
  with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
    ctx = b.new_context(viewport={"width": 412, "height": 915}, device_scale_factor=1, is_mobile=True, has_touch=True)
    def api(r):
        u = r.request.url
        if "/nuts" in u: r.fulfill(status=200, content_type="application/json", body=json.dumps({"list": [{"callsign": "Fuzzy Waffle", "level": 12, "kills": 300, "t": 1}]}))
        else: r.fulfill(status=200, content_type="application/json", body=json.dumps({"list": [{"name": "Captain Noodle", "score": 12345, "wave": 42, "t": 1}]}))
    ctx.route("**/api/**", api)
    pg = ctx.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.add_init_script("localStorage.setItem('capy-reset','276');localStorage.setItem('tarnturm-terms','1');localStorage.setItem('tarnturm-hs-pro', JSON.stringify([{name:'Mart',score:6216,wave:7,t:1}]));localStorage.setItem('capy-stars', JSON.stringify({0:5,1:4}));localStorage.setItem('capy-place-rec', JSON.stringify({0:{k:123,l:4},1:{k:88,l:2}}));localStorage.setItem('tarnturm-cp-pro','25');")
    # 1 Sprachwahl (frisch)
    pg.goto(f"http://127.0.0.1:{port}/index.html" + ("?i18n=audit" if lang == "en" else "")); pg.wait_for_timeout(2500)
    if pg.query_selector("#ovLang"): shot(pg, "00_lang"); pg.evaluate(f"document.querySelector('#ovLang [data-lang={lang}]').click()"); pg.wait_for_timeout(1200)
    shot(pg, "01_splash"); pg.mouse.click(206, 700); pg.wait_for_timeout(2200)
    shot(pg, "02_start")
    # Daily
    if pg.query_selector("#dailyLeaf"): pg.evaluate("document.getElementById('dailyLeaf').click()"); pg.wait_for_timeout(600); shot(pg, "03_daily"); pg.evaluate("document.querySelector('#ovDaily .dlX').click()"); pg.wait_for_timeout(300)
    # Settings
    pg.evaluate("document.getElementById('btnSettings') ? document.getElementById('btnSettings').click() : document.querySelector('[aria-label=Settings]')?.click()"); pg.wait_for_timeout(700); shot(pg, "04_settings")
    pg.evaluate("document.getElementById('setX').click()"); pg.wait_for_timeout(300)
    # Guide
    pg.evaluate("document.getElementById('btnInfo').click()"); pg.wait_for_timeout(600); shot(pg, "05_guide_rules")
    pg.evaluate("document.querySelector('#infoTabs [data-tab=mon]').click()"); pg.wait_for_timeout(500); shot(pg, "06_guide_monsters")
    pg.evaluate("document.querySelector('#infoTabs [data-tab=arms]').click()"); pg.wait_for_timeout(500); shot(pg, "07_guide_gadgets")
    pg.evaluate("document.querySelector('#ovInfo .manual:not([hidden])') && (document.querySelector('#ovInfo .manual:not([hidden])').scrollTop=9999)"); pg.wait_for_timeout(300); shot(pg, "07b_guide_gadgets2")
    pg.evaluate("document.getElementById('btnInfoClose').click()"); pg.wait_for_timeout(300)
    # Awards
    pg.evaluate("document.getElementById('btnHs').click()"); pg.wait_for_timeout(900); shot(pg, "08_medals")
    pg.evaluate("document.querySelector('#awBar [data-aw=hof]').click()"); pg.wait_for_timeout(1200); shot(pg, "09_hof")
    pg.evaluate("document.querySelector('#awBar [data-aw=squad]').click()"); pg.wait_for_timeout(900); shot(pg, "10_squad")
    pg.evaluate("document.getElementById('sqBody').scrollTop=9999; document.querySelector('#ovSquad .albBox').scrollTop=9999"); pg.wait_for_timeout(300); shot(pg, "10b_squad2")
    pg.evaluate("document.getElementById('sqX').click()"); pg.wait_for_timeout(300)
    # Map
    pg.evaluate("document.getElementById('btnMap').click()"); pg.wait_for_timeout(1800); shot(pg, "11_map")
    pg.evaluate("document.querySelector('#ovMap .mapWorldBtn').click()"); pg.wait_for_timeout(1200); shot(pg, "12_map_world")
    pg.evaluate("window.__nzHit=document.querySelector('.mNuts[data-nz=\"1\"]');document.querySelector('#ovMap .mapVp').dispatchEvent(new MouseEvent('click',{bubbles:true,clientX:200,clientY:400}));"); pg.wait_for_timeout(900); shot(pg, "13_map_nuts_locked")
    pg.evaluate("document.querySelector('#ovMap .mapClose').click()"); pg.wait_for_timeout(400)
    # Spiel
    pg.click("#ovStart .playBtn"); pg.wait_for_timeout(2500); shot(pg, "14_tutorial")
    for i in range(6):
        pg.evaluate("(document.querySelector('#tutSkip')||document.querySelector('[data-tut-skip]')||[...document.querySelectorAll('button')].find(b=>/skip tutorial/i.test(b.textContent)))?.click()"); pg.wait_for_timeout(500)
        if not pg.evaluate("typeof TUT!=='undefined'&&TUT.on"): break
    pg.wait_for_timeout(1500); shot(pg, "15_game_w1")
    # Shop
    pg.evaluate("document.getElementById('btnShop') ? document.getElementById('btnShop').click() : document.querySelector('[data-k=shop],[aria-label=Shop]')?.click()"); pg.wait_for_timeout(700); shot(pg, "16_shop")
    pg.evaluate("document.getElementById('sheetX') ? document.getElementById('sheetX').click() : document.querySelector('#sheet .xBtn')?.click()"); pg.wait_for_timeout(400)
    # Pause
    pg.evaluate("document.getElementById('btnPause') ? document.getElementById('btnPause').click() : document.querySelector('.pauseBtn')?.click()"); pg.wait_for_timeout(600); shot(pg, "17_pause")
    pg.evaluate("document.getElementById('btnPResume')?.click()"); pg.wait_for_timeout(400)
    # W6 Elite + Welle laufen lassen
    pg.evaluate("window.__TT.S.wave=5; window.__TT.S.waveCD=0.01"); pg.wait_for_timeout(4000); shot(pg, "18_game_w6")
    pg.wait_for_timeout(6000); shot(pg, "19_game_w6b")
    # Game over
    pg.evaluate("window.__TT.S.lives=0; window.__TT.S.monsters.push({x:1,y:1,cx:1,cy:1,prog:0,trav:0,hp:1,max:1,speed:1,kind:'norm',slowT:0,next:null,chew:false,dead:false,reward:1,dir:0,ph:0,hits:0})"); pg.wait_for_timeout(3500); shot(pg, "20_over")
    keys = pg.evaluate("window.__i18n.seen()") if lang == "en" else []
    miss = pg.evaluate("window.__i18n.miss()")
    if lang == "en": json.dump(keys, open(f"{out}/keys.json", "w"), ensure_ascii=False, indent=0)
    json.dump(miss, open(f"{out}/miss_{lang}.json", "w"), ensure_ascii=False, indent=0)
    json.dump(OVER, open(f"{out}/overflow_{lang}.json", "w"), ensure_ascii=False, indent=1)
    print("lang", lang, "shots", len(shots), "keys", len(keys), "miss", len(miss), "overflow-screens", len(OVER), "errors", errs[:3])
    b.close()
finally: srv.terminate()
