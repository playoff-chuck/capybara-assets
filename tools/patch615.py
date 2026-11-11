#!/usr/bin/env python3
# V615 (Martin 11.11. 12:24): Vor dem Icon-Anlegen auf Android ein Hinweis zum Bestätigen –
# bei Honor/Huawei/Xiaomi u. a. muss Chrome erst «Ярлыки на рабочем столе» dürfen. Nach dem Speichern auf Android immer «✈ nochmal für Icon».
import sys, os, json
site = sys.argv[1]; p = os.path.join(site, "index.html"); s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V614";', 'const GAME_VER = "V615";')
rep('const askIcon = () => { if (isInst()) return false;', 'const askIcon0 = () => { if (isInst()) return false;')
rep('''      if (andr) { toast("Home-screen icon: browser menu ⋮ → Add to Home screen", "OFFLINE", 3600); return true; }
      return false; };''', '''      if (andr) { toast("Home-screen icon: browser menu ⋮ → Add to Home screen", "OFFLINE", 3600); return true; }
      return false; };
    /* V615: Hinweis vor dem Icon (Honor, Xiaomi & Co. sperren Chrome-Verknüpfungen) */
    const icHint = go => { if (document.getElementById("icHint")) return;
      if (!document.getElementById("icHintCss")) { const st = document.createElement("style"); st.id = "icHintCss";
        st.textContent = '#icHint{position:fixed;inset:0;z-index:99999;display:grid;place-items:center;background:rgba(20,12,6,.6);padding:16px}#icHint .ihC{width:100%;max-width:360px;background:#fff8ec;border:3px solid #3a1d10;border-radius:18px;box-shadow:0 5px 0 #3a1d10;padding:16px 16px 14px;color:#2a1a0e;font:600 15px/1.4 "Baloo 2",system-ui,sans-serif;text-align:left}#icHint h3{margin:0 0 8px;font:400 24px/1 var(--f-display,Bangers,Impact,sans-serif);letter-spacing:.04em;color:#2f6f4f;text-align:center}#icHint p{margin:6px 0}#icHint .ihS{background:#eef5f0;border:1px solid #cfe3d6;border-radius:10px;padding:8px 10px;font-weight:800}#icHint .ihB{display:flex;gap:10px;margin-top:12px}#icHint button{flex:1;border:3px solid #3a1d10;border-radius:12px;padding:10px 6px;font:400 18px/1 var(--f-display,Bangers,Impact,sans-serif);letter-spacing:.04em;cursor:pointer;box-shadow:0 3px 0 #3a1d10}#icHint .ihOk{background:#ffd84d!important;color:#3a1d10!important}#icHint .ihNo{flex:0 0 34%;background:#fff!important;color:#7a6a4f!important}';
        document.head.appendChild(st); }
      const o = document.createElement("div"); o.id = "icHint";
      o.innerHTML = `<div class="ihC" role="dialog" aria-modal="true"><h3>${T("HOME-SCREEN ICON")}</h3><p>${T("On some phones (Honor, Huawei, Xiaomi, Redmi, Oppo, Vivo) Chrome first needs permission to create icons.")}</p><p class="ihS">${T("Settings → Apps → Chrome → Permissions → allow “Home screen shortcuts”.")}</p><p>${T("Then tap “Create icon”. If nothing appears: Chrome menu ⋮ → Add to Home screen.")}</p><div class="ihB"><button type="button" class="ihNo">${T("Later")}</button><button type="button" class="ihOk">${T("CREATE ICON")}</button></div></div>`;
      document.body.appendChild(o);
      o.querySelector(".ihNo").addEventListener("click", e => { e.stopPropagation(); o.remove(); });
      o.querySelector(".ihOk").addEventListener("click", e => { e.stopPropagation(); o.remove(); try { snd("uiTap"); } catch (er) {} askIcon0(); }); };
    const askIcon = () => { if (isInst()) return false; if (andr) { icHint(); return true; } return askIcon0(); };''')
rep('prompt && !isInst() ? "Saved! Tap ✈ again for the home-screen icon" : andr && !isInst() ? "Home-screen icon: browser menu ⋮ → Add to Home screen" : "Saved! Works in flight mode now."',
    '(prompt || andr) && !isInst() ? "Saved! Tap ✈ again for the home-screen icon" : "Saved! Works in flight mode now."')
open(p, "w", encoding="utf-8").write(s)
K = ["HOME-SCREEN ICON",
     "On some phones (Honor, Huawei, Xiaomi, Redmi, Oppo, Vivo) Chrome first needs permission to create icons.",
     "Settings → Apps → Chrome → Permissions → allow “Home screen shortcuts”.",
     "Then tap “Create icon”. If nothing appears: Chrome menu ⋮ → Add to Home screen.",
     "Later", "CREATE ICON"]
T = {"en": K,
     "ru": ["ИКОНКА НА ЭКРАН",
            "На некоторых телефонах (Honor, Huawei, Xiaomi, Redmi, Oppo, Vivo) Chrome сначала нужно разрешить создавать иконки.",
            "Настройки → Приложения → Chrome → Права → разрешить «Ярлыки на рабочем столе».",
            "Потом нажми «Создать иконку». Если ничего не появилось: меню Chrome ⋮ → «Добавить на главный экран».",
            "Позже", "СОЗДАТЬ ИКОНКУ"],
     "de": ["ICON AUF DEN STARTBILDSCHIRM",
            "Auf manchen Handys (Honor, Huawei, Xiaomi, Redmi, Oppo, Vivo) muss Chrome erst Icons anlegen dürfen.",
            "Einstellungen → Apps → Chrome → Berechtigungen → „Verknüpfungen auf dem Startbildschirm“ erlauben.",
            "Dann auf „Icon erstellen“ tippen. Kommt nichts: Chrome-Menü ⋮ → Zum Startbildschirm hinzufügen.",
            "Später", "ICON ERSTELLEN"],
     "es": ["ICONO EN LA PANTALLA",
            "En algunos móviles (Honor, Huawei, Xiaomi, Redmi, Oppo, Vivo) Chrome necesita permiso para crear iconos.",
            "Ajustes → Aplicaciones → Chrome → Permisos → permitir «Accesos directos en la pantalla de inicio».",
            "Luego toca «Crear icono». Si no aparece nada: menú de Chrome ⋮ → Añadir a pantalla de inicio.",
            "Luego", "CREAR ICONO"],
     "pt": ["ÍCONE NA TELA",
            "Em alguns celulares (Honor, Huawei, Xiaomi, Redmi, Oppo, Vivo) o Chrome precisa de permissão para criar ícones.",
            "Configurações → Apps → Chrome → Permissões → permitir «Atalhos na tela inicial».",
            "Depois toque em «Criar ícone». Se nada aparecer: menu do Chrome ⋮ → Adicionar à tela inicial.",
            "Depois", "CRIAR ÍCONE"]}
for l, vals in T.items():
    q = os.path.join(site, "lang", l + ".json"); d = json.loads(open(q, encoding="utf-8").read())
    for k, v in zip(K, vals):
        if l == "en" or k not in d or k in K[:4] + ["CREATE ICON"]: d[k] = v
    open(q, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=0))
print("ok V615")
