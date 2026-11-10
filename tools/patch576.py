#!/usr/bin/env python3
# V576 (Martin 11.11. 00:19): Admin wieder frei (neue Geräte-ID R47V-R8F3; bei ungültigem Schlüssel neu holen)
# + Olli-Werbung passt immer auf einen Bildschirm (Größen nach Bildschirmhöhe, nichts scrollt)
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V575";', 'const GAME_VER = "V576";')
rep('["M2HL-KCQH", "5478-BQ27", "BEEM-MGDC"].includes(capyUid())', '["M2HL-KCQH", "5478-BQ27", "BEEM-MGDC", "R47V-R8F3"].includes(capyUid())')
rep('''      if (r.status === 403) { info.textContent = "kein Zugang";''',
    '''      if (r.status === 403 && !load.re) { load.re = 1; try { localStorage.removeItem("capy-adm"); } catch (e) {} return load(); }   /* V576: alter Schlüssel → neu holen */
      if (r.status === 403) { info.textContent = "kein Zugang";''')
CSS = '''<style id="v576">
#ovCoachAd{height:100vh;height:100dvh;overflow:hidden}
#ovCoachAd .caTop{flex:0 1 auto;padding:max(1.6vh,env(safe-area-inset-top)) 14px 0!important}
#ovCoachAd .caK{font-size:min(12px,1.6vh)!important;padding:.7vh 12px .6vh!important}
#ovCoachAd h2{font-size:min(12vw,6.8vh)!important;margin:1vh 0 .5vh!important}
#ovCoachAd .caSub{font-size:min(15px,2.1vh)!important}
#ovCoachAd .caMid{flex:1 1 0!important;min-height:0!important;overflow:hidden}
#ovCoachAd .caMid .caOllie{max-height:100%!important;margin-bottom:-3vh!important}
#ovCoachAd .caCard{flex:0 0 auto;padding:3.4vh 12px 1.4vh!important;margin-bottom:max(1.4vh,env(safe-area-inset-bottom))!important}
#ovCoachAd .caPros{margin-bottom:1.4vh!important;gap:6px!important}
#ovCoachAd .caPros>div{font-size:min(13px,1.8vh)!important;padding:.9vh 8px!important}
#ovCoachAd .caPros b{flex-basis:min(32px,4.2vh)!important;height:min(32px,4.2vh)!important;font-size:min(18px,2.4vh)!important}
#ovCoachAd .caBuy{font-size:min(27px,3.6vh)!important;padding:1.9vh 10px 1.6vh!important}
#ovCoachAd .caLater{font-size:min(13px,1.8vh)!important;margin-top:.6vh!important;padding:.8vh 10px!important}
</style>
'''

# Flugzeug (Martin 00:24): Film wie früher, nur der Motor beginnt 1,5 s vorher (Karte wartet 1,5 s)
rep("return { off, dl, pre: Math.max(0, 1500 - dl) };", "return { off, dl, pre: 1500 };")
rep("const sAt = PL.off ? Math.max(0, PL.pre + PL.dl - 1500) : 0;", "const sAt = 0;")
# Olli-Werbung: eigene Animation, die den Tutorial-Pfeil nicht mehr überschreibt (Namenskonflikt caBob)
rep("animation:caBob 2.4s ease-in-out infinite}", "animation:olBob 2.4s ease-in-out infinite}")
rep("@keyframes caBob{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}", "@keyframes olBob{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}")
rep("</body>", CSS + "</body>")
open(dst, "w", encoding="utf-8").write(s)
print("ok")
