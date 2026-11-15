from playwright.sync_api import sync_playwright
import time
js=open('/srv/testapp/app/src/main/assets/autoplay.js').read()
logs=[]
with sync_playwright() as p:
    b=p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required","--mute-audio"])
    c=b.new_context(viewport={"width":412,"height":915})
    pg=c.new_page(); pg.on("console",lambda m: logs.append(m.text) if ('CAPYAUTO' in m.text or m.type=='error') else None)
    pg.goto("https://playcapybarasquad.com/"); time.sleep(4)
    try: pg.evaluate(js)
    except Exception as e: print("e1",e)
    time.sleep(6); pg.evaluate(js); time.sleep(80)
    print(pg.evaluate("({w:window.__TT&&window.__TT.S.wave,st:window.__TT&&window.__TT.S.started})"))
    pg.screenshot(path='/root/autoplay_check.png')
print("\n".join(logs[-12:]))
