#!/bin/bash
# Splat Squad – Hetzner-Grundeinrichtung + MCP-Zugang für Claude + Nano Banana (Gemini Bild-API)
set -e
DOMAIN="2-29-147-164.sslip.io"
echo "== 1/6 System aktualisieren"
export DEBIAN_FRONTEND=noninteractive
apt-get update -y && apt-get upgrade -y
apt-get install -y python3-venv python3-pip caddy ufw fail2ban curl openssl
echo "== 2/6 Firewall (SSH, HTTP, HTTPS)"
ufw allow 22/tcp && ufw allow 80/tcp && ufw allow 443/tcp && ufw --force enable
echo "== 3/6 Geheimnisse anlegen (bleiben auf dem Server)"
mkdir -p /etc/splatsquad /srv/media /opt/splatmcp && chmod 700 /etc/splatsquad
[ -f /etc/splatsquad/token ] || openssl rand -hex 20 > /etc/splatsquad/token
touch /etc/splatsquad/gemini.key && chmod 600 /etc/splatsquad/*
echo "== 4/6 Python-Umgebung"
python3 -m venv /opt/splatmcp/venv
/opt/splatmcp/venv/bin/pip install -q --upgrade pip "mcp[cli]<2" httpx pillow uvicorn
cat > /opt/splatmcp/server.py <<'PY'
import base64, io, os, re, subprocess, time, pathlib, httpx
from PIL import Image as PILImage
from mcp.server.fastmcp import FastMCP, Image
TOKEN = open("/etc/splatsquad/token").read().strip()
DOMAIN = os.environ.get("SPLAT_DOMAIN", "2-29-147-164.sslip.io")
MEDIA = pathlib.Path("/srv/media")
kw = dict(host="127.0.0.1", port=8765, streamable_http_path=f"/{TOKEN}/mcp", stateless_http=True)
try:
    from mcp.server.transport_security import TransportSecuritySettings
    kw["transport_security"] = TransportSecuritySettings(enable_dns_rebinding_protection=False)
except Exception:
    pass
mcp = FastMCP("splatsquad", **kw)

@mcp.tool()
def run(cmd: str, timeout: int = 120) -> str:
    """Run a shell command on the splatsquad server (max 180 s). Returns exit code, stdout, stderr (truncated)."""
    t = max(1, min(int(timeout), 180))
    try:
        p = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=t)
        return f"exit {p.returncode}\n--- stdout\n{p.stdout[-12000:]}\n--- stderr\n{p.stderr[-4000:]}"
    except subprocess.TimeoutExpired:
        return f"timeout after {t}s"

@mcp.tool()
def write_file(path: str, content: str) -> str:
    """Write a text file on the server (creates folders)."""
    p = pathlib.Path(path); p.parent.mkdir(parents=True, exist_ok=True); p.write_text(content)
    return f"wrote {len(content)} chars to {path}"

@mcp.tool()
def generate_image(prompt: str, name: str, aspect_ratio: str = "1:1", model: str = "gemini-2.5-flash-image") -> list:
    """Generate an image with Nano Banana (Gemini image model). Saves the full PNG under /srv/media/<name>.png
    (public at https://<domain>/media/<name>.png) and returns a small preview. aspect_ratio e.g. 1:1, 16:9, 9:16, 4:3, 3:4.
    model: gemini-2.5-flash-image (Nano Banana) or gemini-3-pro-image-preview (Nano Banana Pro)."""
    key = open("/etc/splatsquad/gemini.key").read().strip()
    if not key:
        return ["No API key yet: put it into /etc/splatsquad/gemini.key on the server."]
    name = re.sub(r"[^a-zA-Z0-9_-]", "-", name)[:60] or f"img-{int(time.time())}"
    body = {"contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": aspect_ratio}}}
    r = httpx.post(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
                   headers={"x-goog-api-key": key}, json=body, timeout=170)
    if r.status_code != 200:
        return [f"API error {r.status_code}: {r.text[:800]}"]
    parts = r.json().get("candidates", [{}])[0].get("content", {}).get("parts", [])
    imgs = [p["inlineData"]["data"] for p in parts if "inlineData" in p]
    if not imgs:
        return [f"No image returned: {r.text[:800]}"]
    raw = base64.b64decode(imgs[0]); MEDIA.mkdir(exist_ok=True)
    im = PILImage.open(io.BytesIO(raw)).convert("RGB"); im.save(MEDIA / f"{name}.png")
    pv = im.copy(); pv.thumbnail((640, 640)); buf = io.BytesIO(); pv.save(buf, "JPEG", quality=80)
    return [Image(data=buf.getvalue(), format="jpeg"),
            f"saved {im.width}x{im.height} → https://{DOMAIN}/media/{name}.png (server path /srv/media/{name}.png)"]

@mcp.tool()
def media_list() -> str:
    """List generated images."""
    return "\n".join(f"{f.name}  {f.stat().st_size // 1024} KB" for f in sorted(MEDIA.glob("*")))

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
PY
echo "== 5/6 Dienst + HTTPS"
cat > /etc/systemd/system/splatmcp.service <<UNIT
[Unit]
Description=Splat Squad MCP
After=network.target
[Service]
Environment=SPLAT_DOMAIN=$DOMAIN
ExecStart=/opt/splatmcp/venv/bin/python /opt/splatmcp/server.py
Restart=always
[Install]
WantedBy=multi-user.target
UNIT
cat > /etc/caddy/Caddyfile <<CADDY
$DOMAIN {
  handle /media/* {
    root * /srv
    file_server
  }
  handle {
    reverse_proxy 127.0.0.1:8765
  }
}
CADDY
systemctl daemon-reload && systemctl enable --now splatmcp && systemctl restart caddy
sleep 3
echo "== 6/6 Fertig"
systemctl is-active splatmcp caddy
echo
echo "Connector-Adresse (NICHT in den Chat kopieren, nur in claude.ai eintragen):"
echo "https://$DOMAIN/$(cat /etc/splatsquad/token)/mcp"
