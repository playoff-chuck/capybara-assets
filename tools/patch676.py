# V676: Vollbild – automatisch beim ersten Tipp (Android-Browser), Knopf im Startmenü neben dem Ton, Schalter in den Einstellungen; installierte App startet im Vollbild
import sys, os
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf8").read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:60], c); s = s.replace(a, b)
JS = r'''<script>/* V676: Vollbild */
(function(){try{
var d=document,el=d.documentElement,ua=navigator.userAgent;
var req=el.requestFullscreen||el.webkitRequestFullscreen, can=!!req&&!/iPhone|iPad|iPod/.test(ua), tg=/Telegram/i.test(ua);
var inst=function(){return matchMedia("(display-mode: fullscreen)").matches||matchMedia("(display-mode: standalone)").matches||!!navigator.standalone;};
if(!can||inst())return;
var isFs=function(){return !!(d.fullscreenElement||d.webkitFullscreenElement);};
var lang=function(){try{return (window.I18N&&I18N.lang)||localStorage.getItem("capy-lang")||"en";}catch(e){return "en";}};
var L=function(){return {ru:"ВО ВЕСЬ ЭКРАН",es:"PANTALLA COMPLETA",pt:"TELA CHEIA",de:"VOLLBILD"}[lang()]||"FULL SCREEN";};
var OO=function(on){var l=lang();return on?({ru:"ВКЛ",es:"SÍ",pt:"SIM",de:"AN"}[l]||"ON"):({ru:"ВЫКЛ",es:"NO",pt:"NÃO",de:"AUS"}[l]||"OFF");};
var pref=function(){try{return localStorage.getItem("capy-fs")!=="0";}catch(e){return true;}}, setPref=function(v){try{localStorage.setItem("capy-fs",v?"1":"0");}catch(e){}};
var go=function(){try{var p=req.call(el,{navigationUI:"hide"});if(p&&p.catch)p.catch(function(){});}catch(e){}};
var off=function(){try{(d.exitFullscreen||d.webkitExitFullscreen).call(d);}catch(e){}};
var first=function(){d.removeEventListener("pointerup",first,true);if(pref()&&!tg&&!isFs())go();};
d.addEventListener("pointerup",first,true);
var b=d.createElement("button");b.type="button";b.id="btnFs";b.className="btn-mute";b.setAttribute("aria-label","Full screen");
b.innerHTML='<svg viewBox="0 0 24 24" width="60%" height="60%" aria-hidden="true"><path d="M4 9V4h5M15 4h5v5M20 15v5h-5M9 20H4v-5" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>';
b.style.cssText="position:fixed;z-index:60;display:none;align-items:center;justify-content:center;padding:0";
b.addEventListener("click",function(e){e.stopPropagation();setPref(true);go();});
var place=function(){try{var st=d.getElementById("ovStart"),sd=d.getElementById("stMute")||d.getElementById("bSound"),r=sd&&sd.getBoundingClientRect();var show=st&&!st.hidden&&!isFs()&&r&&r.width>0;b.style.display=show?"flex":"none";if(show){b.style.left=Math.round(r.left-r.width-10)+"px";b.style.top=Math.round(r.top)+"px";b.style.width=Math.round(r.width)+"px";b.style.height=Math.round(r.height)+"px";}}catch(e){}};
var add=function(){d.body.appendChild(b);setInterval(place,500);place();
  var sx=d.getElementById("ovSettings"),hd=sx&&sx.querySelector(".alHead");if(!hd)return;
  var sb=d.createElement("button");sb.type="button";sb.id="setFs";sb.className="btn-small";sb.style.cssText="display:block;width:100%;margin:6px 0 8px";
  var lab=function(){sb.textContent=L()+": "+OO(isFs());};
  sb.addEventListener("click",function(e){e.stopPropagation();if(isFs()){setPref(false);off();}else{setPref(true);go();}setTimeout(lab,400);});
  hd.parentNode.insertBefore(sb,hd.nextSibling);lab();d.addEventListener("fullscreenchange",function(){lab();place();});setInterval(lab,1500);};
if(d.readyState==="loading")d.addEventListener("DOMContentLoaded",add);else add();
}catch(e){console.warn("fs",e);}})();</script>
</body>'''
rep('</body>', JS)
rep('const GAME_VER = "V675"', 'const GAME_VER = "V676"')
open(dst, "w", encoding="utf8").write(s)
m = os.path.join(os.path.dirname(dst), "manifest.webmanifest"); t = open(m, encoding="utf8").read()
assert t.count('"display": "standalone"') == 1; open(m, "w", encoding="utf8").write(t.replace('"display": "standalone"', '"display": "fullscreen",\n  "display_override": ["fullscreen", "standalone"]'))
print("ok")
