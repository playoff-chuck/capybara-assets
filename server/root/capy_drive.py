#!/usr/bin/env python3
"""V653: Google-Drive-Aufträge der Spieler-Tabelle (beide Server).
  python3 /root/capy_drive.py check          -> JSON: offene Aufträge je Server (com, ru)
  python3 /root/capy_drive.py csv SRV WEEK F -> CSV-Text (SRV com|ru, F spieler|sitzungen)
  python3 /root/capy_drive.py done SRV       -> Auftrag als erledigt markieren
"""
import json, subprocess, sys, time, re
KEY = re.search(r"ssh -i (\S+)", open("/root/deploy_ru.sh").read()).group(1)
RU = ["ssh", "-i", KEY, "-o", "BatchMode=yes", "root@177.177.219.65"]
D = "/srv/capy-api/reports"
def sh(srv, cmd):
    if srv == "com": return subprocess.run(["bash", "-c", cmd], capture_output=True, text=True, timeout=60).stdout
    return subprocess.run(RU + [cmd], capture_output=True, text=True, timeout=60).stdout
def rj(srv, f):
    try: return json.loads(sh(srv, f"cat {D}/{f} 2>/dev/null") or "null")
    except Exception: return None
a = sys.argv[1:]
if a[0] == "check":
    out = {}
    for srv in ("com", "ru"):
        dr = rj(srv, "drive.json"); last = rj(srv, "last.json")
        out[srv] = {"pending": bool(dr and not dr.get("done")), "drive": dr, "last": last}
    print(json.dumps(out, ensure_ascii=False))
elif a[0] == "csv":
    srv, wk, f = a[1], a[2], a[3]
    assert srv in ("com", "ru") and re.fullmatch(r"\d{4}-KW\d{2}", wk) and f in ("spieler", "sitzungen")
    sys.stdout.write(sh(srv, f"cat {D}/{wk}/{f}.csv"))
elif a[0] == "done":
    srv = a[1]; assert srv in ("com", "ru")
    dr = rj(srv, "drive.json") or {}
    now = int(time.time() * 1000); dr["done"] = now; dr["doneMsk"] = time.strftime("%d.%m.%Y %H:%M", time.gmtime(now / 1000 + 3 * 3600)) + " MSK"
    js = json.dumps(dr).replace("'", "")
    sh(srv, f"echo '{js}' > {D}/drive.json"); print("ok", srv)
