"""Nano Banana (Pro) mit Referenzbild über OpenRouter. Aufruf: nb_ref.py <ref.jpg|png> <out.png> <aspect> <model> < prompt.txt
Gibt Größe und Kosten aus. Schlüssel aus /etc/splatsquad/openrouter.key (nie ausgeben)."""
import sys, base64, json, io, httpx
from PIL import Image
ref, out, aspect, model = sys.argv[1:5]
prompt = sys.stdin.read()
key = open("/etc/splatsquad/openrouter.key").read().strip()
im = Image.open(ref).convert("RGB"); buf = io.BytesIO(); im.save(buf, "JPEG", quality=92)
b64 = base64.b64encode(buf.getvalue()).decode()
body = {"model": model, "messages": [{"role": "user", "content": [
          {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64," + b64}},
          {"type": "text", "text": prompt}]}],
        "modalities": ["image", "text"], "image_config": {"aspect_ratio": aspect}, "usage": {"include": True}}
r = httpx.post("https://openrouter.ai/api/v1/chat/completions",
               headers={"Authorization": f"Bearer {key}", "HTTP-Referer": "https://playcapybarasquad.com", "X-Title": "Capybara Squad"},
               json=body, timeout=175)
if r.status_code != 200:
    print("API error", r.status_code, r.text[:500]); sys.exit(1)
j = r.json(); msg = (j.get("choices") or [{}])[0].get("message", {})
imgs = [i.get("image_url", {}).get("url", "") for i in (msg.get("images") or [])]
imgs = [u for u in imgs if u.startswith("data:")]
if not imgs:
    print("no image", str(j)[:500]); sys.exit(1)
raw = base64.b64decode(imgs[0].split(",", 1)[1]); o = Image.open(io.BytesIO(raw)).convert("RGB"); o.save(out)
print("saved", out, o.size, "cost", (j.get("usage") or {}).get("cost"))
