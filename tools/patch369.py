"""V369 (Martin 07.11. 08:49): Beim Flug nach Afrika «landet er in einer anderen Stadt als der Punkt, von dem es weitergeht».
Ursache: Das Ortsschild des aktuellen Ortes (z. B. «OASIS CAMP») steht 70 px über dem rosa Landepunkt – genau auf dem weißen
Punkt eines Nachbarorts (Dune Sea). Jetzt: Steht das Schild über einem fremden Punkt (oder unter der Titelkarte), rückt es unter
den eigenen Punkt; dazu ein Zipfel, der auf den eigenen Punkt zeigt."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V368";', 'const GAME_VER = "V369";')
rep('''      const need = down ? pr.top - (p.classList.contains("cur") ? 70 : 14) - em.offsetHeight < tb : em.getBoundingClientRect().top < tb; if (need !== down) p.classList.toggle("lblDown", need); }); }, 200); })(); } catch (e) { console.error("v321 lbl", e); }''',
'''      const off = p.classList.contains("cur") && ov.classList.contains("auto") ? 70 : 14, ew = em.offsetWidth, eh = em.offsetHeight, up = { l: pr.left - ew / 2 - 4, r: pr.left + ew / 2 + 4, t: pr.top - off - eh - 4, b: pr.top - off + 12 };
      const hit = [...ov.querySelectorAll(".mPin")].some(q => { if (q === p) return false; const r = q.getBoundingClientRect(); return r.left > up.l && r.left < up.r && r.top > up.t && r.top < up.b; });   /* V369: Schild nie auf einem fremden Ortspunkt */
      const need = up.t < tb || hit; if (need !== down) p.classList.toggle("lblDown", need); }); }, 200); })(); } catch (e) { console.error("v321 lbl", e); }''')
rep('#ovMap.auto .mPin.cur em{top:-70px}', '#ovMap.auto .mPin.cur em{top:-70px}#ovMap .mPin.cur em::before{content:"";position:absolute;left:50%;bottom:-9px;margin-left:-7px;border:7px solid transparent;border-top-color:#3a2414;border-bottom:0}#ovMap .mPin.cur.lblDown em::before{bottom:auto;top:-9px;border-top:0;border-bottom:7px solid #3a2414}')
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
