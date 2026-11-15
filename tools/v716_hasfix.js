/* V716: body:has(…) → Body-Klassen per JS (Stil-Neuberechnung des ganzen Baums vermeiden) */
(() => { try {
  const ARGS = [], IDX = new Map();
  const reg = a => { if (!IDX.has(a)) { IDX.set(a, ARGS.length); ARGS.push(a); } return "hz" + IDX.get(a); };
  const splitTop = s => { const out = []; let d = 0, q = null, cur = ""; for (const ch of s) { if (q) { if (ch === q) q = null; } else if (ch === '"' || ch === "'") q = ch; else if (ch === "(") d++; else if (ch === ")") d--; if (ch === "," && !d && !q) { out.push(cur); cur = ""; } else cur += ch; } out.push(cur); return out; };
  const conv = sel => { let s = sel.trim(), pre = ""; const hm = /^html(\[[^\]]*\])?\s+/.exec(s); if (hm) { pre = hm[0]; s = s.slice(hm[0].length); } if (!/^body(?![\w-])/.test(s)) return null;
    let i = 4, res = pre + "body", ok = false;
    while (i < s.length && !/[\s>+~]/.test(s[i])) {
      let m;
      if (s.startsWith(":has(", i) || s.startsWith(":not(:has(", i)) { const neg = s.startsWith(":not(", i); let j = i + (neg ? 10 : 5), d = 1, st = j; for (; j < s.length && d; j++) { if (s[j] === "(") d++; else if (s[j] === ")") d--; } const arg = s.slice(st, j - 1);
        const w = spec(arg); if (neg) { if (s[j] !== ")") return null; j++; res += ":not(:where(." + reg(arg) + "))" + pad(w); } else res += ":where(." + reg(arg) + ")" + pad(w); i = j; ok = true; continue; }
      if ((m = /^(\.[\w-]+|#[\w-]+|\[[^\]]*\]|:not\([^()]*\)|:[\w-]+(\([^()]*\))?)/.exec(s.slice(i)))) { res += m[0]; i += m[0].length; continue; }
      return null; }
    if (!ok) return null; return res + s.slice(i); };
  const spec = sel => { let best = [0, 0, 0]; for (const part of splitTop(sel)) { const v = [0, 0, 0]; let s = part.trim(), i = 0;
      while (i < s.length) { const ch = s[i];
        if (ch === "#") { v[0]++; i++; while (i < s.length && /[\w-]/.test(s[i])) i++; continue; }
        if (ch === ".") { v[1]++; i++; while (i < s.length && /[\w-]/.test(s[i])) i++; continue; }
        if (ch === "[") { v[1]++; while (i < s.length && s[i] !== "]") i++; i++; continue; }
        if (ch === ":") { if (s[i + 1] === ":") { v[2]++; i += 2; while (i < s.length && /[\w-]/.test(s[i])) i++; continue; }
          let j = i + 1; while (j < s.length && /[\w-]/.test(s[j])) j++; const nm = s.slice(i + 1, j).toLowerCase();
          if (s[j] === "(") { let d = 1, k = j + 1; for (; k < s.length && d; k++) { if (s[k] === "(") d++; else if (s[k] === ")") d--; } const inner = s.slice(j + 1, k - 1);
            if (nm === "where") {} else if (nm === "not" || nm === "is" || nm === "has" || nm === "matches") { const w = spec(inner); v[0] += w[0]; v[1] += w[1]; v[2] += w[2]; } else v[1]++; i = k; continue; }
          v[1]++; i = j; continue; }
        if (/[a-zA-Z]/.test(ch)) { v[2]++; while (i < s.length && /[\w-]/.test(s[i])) i++; continue; }
        i++; }
      if (v[0] > best[0] || (v[0] === best[0] && (v[1] > best[1] || (v[1] === best[1] && v[2] > best[2])))) best = v; }
    return best; };
  const pad = w => ":not(#hzX)".repeat(w[0]) + ":not(.hzX)".repeat(w[1]) + ":not(hzx)".repeat(w[2]);   /* gleiche Spezifität wie :has(…) */
  let n = 0;
  const walk = rules => { for (const r of rules) { if (r.cssRules && !r.selectorText) { walk(r.cssRules); continue; } if (!r.selectorText || !r.selectorText.includes(":has(")) continue;
      const parts = splitTop(r.selectorText); let ch = false; const np = parts.map(p => { const c = p.includes(":has(") ? conv(p) : null; if (c) { ch = true; return c; } return p; });
      if (ch) { const was = r.selectorText; r.selectorText = np.join(", "); if (r.selectorText !== was) n++; } } };
  for (const sh of document.styleSheets) { try { walk(sh.cssRules); } catch (e) {} }
  const st = new Array(ARGS.length).fill(null), B = document.body;
  const ev = () => { for (let k = 0; k < ARGS.length; k++) { let on = false; try { on = !!B.querySelector(ARGS[k]); } catch (e) { on = false; } if (on !== st[k]) { st[k] = on; B.classList.toggle("hz" + k, on); } } };
  ev(); new MutationObserver(ev).observe(B, { subtree: true, childList: true, attributes: true, attributeFilter: ["hidden", "class", "id"] });
  const rew = n => { try { if (n && n.nodeName === "STYLE" && n.sheet) { walk(n.sheet.cssRules); while (st.length < ARGS.length) st.push(null); ev(); } } catch (e) {} };
  new MutationObserver(ms => { for (const m of ms) m.addedNodes.forEach(rew); }).observe(document.documentElement, { subtree: true, childList: true });
  window.__hz = { get n() { return n; }, args: ARGS, ev };
} catch (e) { console.error("hasfix", e); } })();
