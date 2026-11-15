#!/usr/bin/env python3
"""Capybara Squad – täglicher Speicher-Check (Martin 14.11.2026 16:03).
Löscht nur Zwischendateien: /tmp älter als 1 Tag, Test-Lab-Downloads älter als 14 Tage, Megatest-Läufe älter als 14 Tage,
Review-Videos älter als 30 Tage, Systemprotokolle über 300 MB, apt-Cache. Danach Plattenplatz prüfen (Hetzner + RU-Server);
wird es eng, Meldung in die Telegram-Gruppe. Aufruf: capy_cleanup.py [--dry]"""
import os, sys, time, shutil, subprocess, json

DRY = '--dry' in sys.argv
NOW = time.time(); freed = 0; log = []

def size(p):
    if os.path.isfile(p) or os.path.islink(p): return os.path.getsize(p) if os.path.isfile(p) else 0
    t = 0
    for r, _, fs in os.walk(p):
        for f in fs:
            try: t += os.path.getsize(os.path.join(r, f))
            except OSError: pass
    return t

def newest(p):
    if not os.path.isdir(p): return os.path.getmtime(p)
    m = os.path.getmtime(p)
    for r, ds, fs in os.walk(p):
        for x in fs + ds:
            try: m = max(m, os.path.getmtime(os.path.join(r, x)))
            except OSError: pass
    return m

def in_use(p):
    try: return subprocess.run(['fuser', '-s', p], timeout=10).returncode == 0 if os.path.isfile(p) else bool(subprocess.run(['lsof', '+D', p], capture_output=True, timeout=20).stdout.strip())
    except Exception: return True

def sweep(base, days, keep=()):
    global freed
    if not os.path.isdir(base): return
    for n in os.listdir(base):
        p = os.path.join(base, n)
        if n in keep or n.startswith(('.', 'systemd-', 'snap')): continue
        try:
            if NOW - newest(p) < days * 86400 or in_use(p): continue
            s = size(p)
            if not DRY: shutil.rmtree(p) if os.path.isdir(p) and not os.path.islink(p) else os.remove(p)
            freed += s; log.append(f"{p} ({s / 1e6:.0f} MB)")
        except Exception as e: log.append(f"Fehler {p}: {e}")

sweep('/tmp', 1)
sweep('/root/tlw', 14, keep=('daily',))
sweep('/root/tlw/daily', 60)
sweep('/root/megatest/runs', 14, keep=('status.txt',))
sweep('/srv/site/www/review', 30)
if not DRY:
    subprocess.run(['journalctl', '--vacuum-size=300M'], capture_output=True)
    subprocess.run(['apt-get', 'clean'], capture_output=True)

def df(path):
    st = os.statvfs(path); tot = st.f_blocks * st.f_frsize; free = st.f_bavail * st.f_frsize
    return tot, free

warn = []
for path, name, lim in (('/', 'Hetzner-Platte', 0.80), ('/tmp', 'Hetzner-Zwischenspeicher (/tmp, RAM)', 0.70)):
    tot, free = df(path); used = 1 - free / tot
    log.append(f"{name}: {used * 100:.0f} % belegt, {free / 1e9:.1f} GB frei")
    if used > lim: warn.append(f"{name}: {used * 100:.0f} % belegt, nur {free / 1e9:.1f} GB frei")
try:
    out = subprocess.run(['ssh', '-i', '/root/.ssh/ru_server', '-o', 'ConnectTimeout=10', 'root@177.177.219.65',
                          "find /tmp -mindepth 1 -maxdepth 1 -mtime +1 ! -name 'systemd-*' -exec rm -rf {} + 2>/dev/null; journalctl --vacuum-size=200M >/dev/null 2>&1; df -P / | tail -1"],
                         capture_output=True, text=True, timeout=60).stdout.split()
    used = int(out[4].rstrip('%')); free = int(out[3]) * 1024
    log.append(f"RU-Server: {used} % belegt, {free / 1e9:.1f} GB frei")
    if used > 80: warn.append(f"RU-Server: {used} % belegt, nur {free / 1e9:.1f} GB frei")
except Exception as e: log.append(f"RU-Server nicht geprüft: {e}")

log.insert(0, f"{time.strftime('%Y-%m-%d %H:%M')} UTC – gelöscht {freed / 1e6:.0f} MB")
open('/root/capy_cleanup.log', 'a').write('\n'.join(log) + '\n\n')
print('\n'.join(log))
if warn and not DRY:
    subprocess.run(['python3', '/root/capy_tg.py', 'send', "⚠️ Speicher wird knapp – bitte mehr Speicher einplanen:\n" + '\n'.join(warn) +
                    f"\n(Heute automatisch aufgeräumt: {freed / 1e6:.0f} MB, mehr alte Dateien gibt es nicht.)"], timeout=60)
