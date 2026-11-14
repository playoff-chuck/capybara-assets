"""Android-Startbild (TWA-Splash) = Titelbild wie auf der Webseite (#splash ohne «TAP TO START»).
Aufruf: python3 tools/make_splash.py <site-dir> <android-res-dir>
Schreibt res/drawable-<dpi>/splash.webp (360×960 dp, mittig) und löscht die alte splash.png (= Icon).
Braucht Pillow + fontTools + brotli (Bangers-Schrift aus site/fonts/*.woff2)."""
import sys, os, io, glob
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from fontTools.ttLib import TTFont

site, res = sys.argv[1], sys.argv[2]
DW, DH = 360, 960            # dp – lang genug für 20:9-Handys; CENTER schneidet oben/unten
K = 4                         # Arbeitsauflösung 4× (xxxhdpi)
W, H = DW * K, DH * K

# Hintergrund wie CSS: object-fit:cover; object-position:center 60%
bg = Image.open(os.path.join(site, "img/b6f38631c6.webp")).convert("RGB")
s = max(W / bg.width, H / bg.height)
bw, bh = round(bg.width * s), round(bg.height * s)
bg = bg.resize((bw, bh), Image.LANCZOS)
x0, y0 = (bw - W) // 2, round((bh - H) * 0.6)
img = bg.crop((x0, y0, x0 + W, y0 + H))

# Schrift
tt = TTFont(os.path.join(site, "fonts/bangers-400-latin.woff2")); tt.flavor = None
buf = io.BytesIO(); tt.save(buf); buf.seek(0)
fs = 46.8 * K                 # 13vw bei 360 dp
font = ImageFont.truetype(buf, round(fs))

def block(text, fill):
    ls = 0.03 * fs
    widths = [font.getlength(c) for c in text]
    tw = sum(widths) + ls * (len(text) - 1)
    pad = 40 * K
    lay = Image.new("RGBA", (int(tw + 2 * pad), int(fs * 1.4 + 2 * pad)), (0, 0, 0, 0))
    return lay, widths, ls, pad

lines = [("CAPYBARA", (255, 246, 230)), ("SQUAD", (255, 207, 61))]
LH = 0.95 * fs
txt = Image.new("RGBA", (W, int(LH * 2 + 120 * K)), (0, 0, 0, 0))
shadow = Image.new("RGBA", txt.size, (0, 0, 0, 0))
dt, ds = ImageDraw.Draw(txt), ImageDraw.Draw(shadow)
STROKE = (58, 29, 16)
for i, (t, col) in enumerate(lines):
    ls = 0.03 * fs
    tw = sum(font.getlength(c) for c in t) + ls * (len(t) - 1)
    x = (W - tw) / 2; y = 40 * K + i * LH
    for c in t:
        ds.text((x, y + 10 * K), c, font=font, fill=(0, 0, 0, 90), stroke_width=3 * K // 2, stroke_fill=(0, 0, 0, 90))
        dt.text((x, y + 5 * K), c, font=font, fill=STROKE, stroke_width=3 * K // 2, stroke_fill=STROKE)   # harter Schatten
        dt.text((x, y), c, font=font, fill=col, stroke_width=3 * K // 2, stroke_fill=STROKE)
        x += font.getlength(c) + ls
shadow = shadow.filter(ImageFilter.GaussianBlur(9 * K))
comb = Image.alpha_composite(shadow, txt).rotate(3, resample=Image.BICUBIC, center=(W / 2, txt.height / 2))
ty = round(0.21 * DH * K) - 40 * K + round(0.0 * K)
img = img.convert("RGBA"); img.alpha_composite(comb, (0, ty)); img = img.convert("RGB")

for d, f in [("mdpi", 1), ("hdpi", 1.5), ("xhdpi", 2), ("xxhdpi", 3), ("xxxhdpi", 4)]:
    out = os.path.join(res, "drawable-" + d)
    os.makedirs(out, exist_ok=True)
    for old in glob.glob(os.path.join(out, "splash.*")): os.remove(old)
    img.resize((round(DW * f), round(DH * f)), Image.LANCZOS).save(os.path.join(out, "splash.webp"), quality=82, method=6)
print("splash ok", W, H)
