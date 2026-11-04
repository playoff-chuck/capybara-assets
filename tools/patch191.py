s=open('v190.html',encoding='utf-8').read()
def rep(a,b,cnt=1):
    global s
    n=s.count(a); assert n==cnt,(n,a[:70]); s=s.replace(a,b)
rep('ver: "V190", wave: S.wave','ver: "V191", wave: S.wave')
js=r'''
/* V191: Shop behält die Scroll-Position nach einem Kauf (nicht wieder nach oben springen) */
(() => {
  const SEL = ["#sheet", "#sheetIn", "#sheet .shopGrid", "#sheet .shopTiles", "#sheet .sheetIn", "#sheet .tabPane"];
  const grab = () => SEL.map(q => { const e = document.querySelector(q); return e ? e.scrollTop : 0; });
  const put = v => SEL.forEach((q, i) => { const e = document.querySelector(q); if (e && v[i]) e.scrollTop = v[i]; });
  const _rs = renderShop;
  renderShop = function () { const v = grab(); const r = _rs.apply(this, arguments); put(v); requestAnimationFrame(() => put(v)); setTimeout(() => put(v), 60); return r; };
})();
'''
k=s.rfind('})();\n</script>'); assert k>0; s=s[:k]+js+s[k:]
open('v191.html','w',encoding='utf-8').write(s); print('ok')
