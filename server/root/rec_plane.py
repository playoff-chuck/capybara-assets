from playwright.sync_api import sync_playwright
import base64,time
INIT=r"""(()=>{const oc=AudioNode.prototype.connect;AudioNode.prototype.connect=function(d,...r){const res=oc.call(this,d,...r);try{if(d instanceof AudioDestinationNode){const c=this.context;if(!c.__md){c.__md=c.createMediaStreamDestination();window.__mdCtx=c;}oc.call(this,c.__md);}}catch(e){}return res;};})();"""
with sync_playwright() as p:
    b=p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"])
    c=b.new_context(viewport={"width":412,"height":915})
    c.add_init_script(INIT); c.add_init_script("try{localStorage.setItem('capy-reset','276');localStorage.setItem('tarnturm-tut','1');localStorage.setItem('tarnturm-terms','1');localStorage.setItem('capy-lang','ru')}catch(e){}")
    pg=c.new_page(); pg.goto("https://playcapybarasquad.com/"); time.sleep(4); pg.mouse.click(200,450); time.sleep(1.5)
    r=pg.evaluate("""async()=>{ if(!window.__planeSnd) return 'nofn';
      let c=window.__mdCtx; if(!c){ window.__planeSnd(10,false); await new Promise(r=>setTimeout(r,900)); c=window.__mdCtx; } if(!c) return 'noctx';
      await c.resume(); const rec=new MediaRecorder(c.__md.stream,{mimeType:'audio/webm'}); const ch=[]; rec.ondataavailable=e=>ch.push(e.data);
      rec.start(); await new Promise(r=>setTimeout(r,300)); window.__planeSnd(7000,false); await new Promise(r=>setTimeout(r,8200)); rec.stop();
      await new Promise(r=>setTimeout(r,500)); const bl=new Blob(ch,{type:'audio/webm'}); const buf=new Uint8Array(await bl.arrayBuffer());
      let s=''; for(let i=0;i<buf.length;i++) s+=String.fromCharCode(buf[i]); return btoa(s); }""")
    if len(r)<20: print(r)
    else: open('/root/trailer/plane_game.webm','wb').write(base64.b64decode(r)); print('ok',len(r))
    b.close()
