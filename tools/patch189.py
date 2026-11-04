s=open('v188.html',encoding='utf-8').read()
def rep(a,b,cnt=1):
    global s
    n=s.count(a); assert n==cnt,(n,a[:70]); s=s.replace(a,b)
rep('ver: "V188", wave: S.wave','ver: "V189", wave: S.wave')
# Hack-Musik endet sofort statt mit 1 s Nachhall
rep('const st = P._arc; P._arc = null; clearInterval(st.timer); st.bus.gain.setTargetAtTime(0.0001, ac.currentTime, 0.25); setTimeout(() => { try { st.bus.disconnect(); } catch (e) {} }, 1500);',
    'const st = P._arc; P._arc = null; clearInterval(st.timer); st.bus.gain.cancelScheduledValues(ac.currentTime); st.bus.gain.setTargetAtTime(0.0001, ac.currentTime, 0.04); setTimeout(() => { try { st.bus.disconnect(); } catch (e) {} }, 300);')
# beim Verlassen des Hacks: Hack-Musik sicher aus (auch wenn ein anderer Weg das Fenster schließt)
rep('else if (!hackUp && hackHeld) { hackHeld = false;','else if (!hackUp && hackHeld) { hackHeld = false; try { snd("arcade", false); } catch (e) {}')
rep('let hackHeld = false;','let hackHeld = false, wasHack = false;')
rep('tpFade(0.5, 0.8); } } } catch (e) {}','tpFade(0.5, 0.8); } } } catch (e) {} if (wasHack && !hackUp) { try { snd("arcade", false); } catch (e) {} } wasHack = hackUp;')
open('v189.html','w',encoding='utf-8').write(s); print('ok')
