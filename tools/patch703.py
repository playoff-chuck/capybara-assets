# V703 (Martin 13.11. 13:44): Versionsprüfung beim Zurückkehren in die App/Seite.
# Rückkehr -> /offline.json (no-store) lesen; neuere Version: im Menü sofort neu laden,
# im Spiel zwischen zwei Wellen speichern + neu laden (mitten in der Welle, in Nuts oder bei offenem Fenster wird gewartet).
# Nach dem Neuladen geht es nach dem Tipp auf den Startbildschirm automatisch mit «Continue» weiter.
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf8").read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
rep('GAME_VER = "V702"', 'GAME_VER = "V703"')
JS = r'''<script>/* V703: Versionsprüfung beim Zurückkehren */
(function(){try{
var num=function(v){return parseInt(String(v||"").replace(/\D/g,""),10)||0};
var want=null,busy=false,timer=null;
function canApply(){try{var S=window.__TT&&window.__TT.S;if(!S||!S.started)return "menu";if(S.over)return false;if(S.testRun||S.replay||S.nuts||S.inWave)return false;
if(window.__vcUi&&window.__vcUi())return false;
if(document.querySelector("#ovHack:not([hidden]),#ovNutsRes:not([hidden]),#ovSign:not([hidden])"))return false;return "game";}catch(e){return false}}
function apply(){if(!want)return;var c=canApply();clearTimeout(timer);if(!c||document.hidden){timer=setTimeout(apply,2000);return;}
try{sessionStorage.setItem("capy-vupd",want);if(c==="game"){try{window.__vcSave()}catch(e){}sessionStorage.setItem("capy-vres","1");}}catch(e){}
location.reload();}
function check(){if(busy||document.hidden||want)return;busy=true;
fetch("/offline.json?vc="+Date.now(),{cache:"no-store"}).then(function(r){return r.json()}).then(function(d){var sv=d&&d.ver;
if(num(sv)>num(GAME_VER)){var tried=null;try{tried=sessionStorage.getItem("capy-vupd")}catch(e){}if(tried===sv)return;want=sv;apply();}}).catch(function(){}).then(function(){busy=false});}
document.addEventListener("visibilitychange",function(){if(!document.hidden)check();});
window.addEventListener("pageshow",function(e){if(e.persisted)check();});
window.__verCheck=check;
var res=null;try{res=sessionStorage.getItem("capy-vres");sessionStorage.removeItem("capy-vres");}catch(e){}
if(res){var go=function(){var n=0,iv=setInterval(function(){var b=document.getElementById("btnResume");
if(b&&!b.hidden&&b.offsetParent){clearInterval(iv);b.click();}else if(++n>40)clearInterval(iv);},250);};
var sp=document.getElementById("splash");if(sp)sp.addEventListener("click",go,{once:true});else go();}
}catch(e){console.warn("v703",e)}})();</script>
</body></html>'''
rep('window.__TT = { get S() { return S; },', 'window.__vcSave = () => saveGame(); window.__vcUi = () => uiWinOpen();   /* V703 */\nwindow.__TT = { get S() { return S; },')
rep('</body></html>', JS)
open(dst, "w", encoding="utf8").write(s)
print("ok V703")
