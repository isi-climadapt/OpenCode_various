# -*- coding: utf-8 -*-
# Amazon A+ Content images for Ocean Friends, modelled on the bestseller pattern
# (Coco Wyo "Ocean Scene"): brand banner with book mockup, features with sample
# pages, single-sided pages explainer, sample page grid.
# Sample pages are rendered from the print interior PDF, so they show the real book.
# Each module is drawn at 2x, then reduced to the exact upload size (KDP doesn't resize).
#
# Usage: py aplus_build.py   -> aplus/aplus_1_banner_970x300.jpg ... (+ _2x masters)

import os, random
import fitz
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")
OUT = os.path.join(HERE, "aplus")
INTERIOR = os.path.join(HERE, "KDP_FINAL_UPLOAD", "01_MANUSCRIPT_INTERIOR_108P.pdf")
COVER = os.path.join(HERE, "cover_option_A.png")

S = 2  # draw scale
SKY = (186, 224, 240)      # soft reef blue (from the cover hero water)
SKY_LIGHT = (214, 238, 247)
CREAM = (246, 237, 225)    # cover background
INK = (35, 25, 20)         # cover dark brown
SUB = (80, 60, 50)

def font(name, px):
    return ImageFont.truetype(os.path.join(FONTS, name), int(px * S))

def page_image(n, width):
    """Art page n (1-50) rendered from the interior PDF, scaled to `width` px."""
    doc = fitz.open(INTERIOR)
    pg = doc[n * 2 + 2]  # pages 1-4 are front matter; art pages alternate with blanks
    pix = pg.get_pixmap(dpi=200, colorspace=fitz.csGRAY)
    im = Image.frombytes("L", (pix.width, pix.height), pix.samples).convert("RGB")
    return im.resize((width, int(width * im.height / im.width)), Image.LANCZOS)

def with_shadow(img, angle=0, radius=10, offset=(6, 10), border=False):
    """RGBA of img rotated by angle, with a soft drop shadow."""
    img = img.convert("RGBA")
    if border:
        ImageDraw.Draw(img).rectangle([0, 0, img.width - 1, img.height - 1], outline=(200, 200, 200, 255), width=S)
    pad = radius * 3 * S
    cv = Image.new("RGBA", (img.width + 2 * pad, img.height + 2 * pad), (0, 0, 0, 0))
    sh = Image.new("RGBA", img.size, (20, 40, 60, 90))
    cv.paste(sh, (pad + offset[0] * S, pad + offset[1] * S), sh)
    cv = cv.filter(ImageFilter.GaussianBlur(radius * S))
    cv.paste(img, (pad, pad), img)
    return cv.rotate(angle, resample=Image.BICUBIC, expand=True)

def paste_center(canvas, rgba, cx, cy):
    canvas.paste(rgba, (int(cx - rgba.width / 2), int(cy - rgba.height / 2)), rgba)

def background(w, h, seed):
    """Reef-blue panel with soft wave bands, bubbles and sparkles."""
    W, H = w * S, h * S
    bg = Image.new("RGB", (W, H), SKY)
    d = ImageDraw.Draw(bg)
    rnd = random.Random(seed)
    for k in range(3):  # soft wave bands
        y = int(H * (0.25 + 0.3 * k)) + rnd.randint(-20, 20) * S
        pts = [(x, y + int(18 * S * __import__("math").sin(x / (90.0 * S) + k))) for x in range(0, W + 10, 10)]
        d.line(pts, fill=SKY_LIGHT, width=10 * S)
    for _ in range(int(w / 40)):  # bubbles
        r = rnd.randint(4, 11) * S
        x, y = rnd.randint(0, W), rnd.randint(0, H)
        d.ellipse([x - r, y - r, x + r, y + r], outline=(255, 255, 255), width=2 * S)
    for _ in range(int(w / 90)):  # sparkles
        x, y, r = rnd.randint(0, W), rnd.randint(0, H), rnd.randint(6, 12) * S
        d.polygon([(x, y - r), (x + r / 4, y - r / 4), (x + r, y), (x + r / 4, y + r / 4),
                   (x, y + r), (x - r / 4, y + r / 4), (x - r, y), (x - r / 4, y - r / 4)], fill=(255, 255, 255))
    return bg

def rounded(canvas, radius=26):
    """Round the panel corners onto white (Amazon's page background)."""
    m = Image.new("L", canvas.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, canvas.width - 1, canvas.height - 1], radius=radius * S, fill=255)
    out = Image.new("RGB", canvas.size, (255, 255, 255))
    out.paste(canvas, (0, 0), m)
    return out

def bubble_text(canvas, text, cx, y, px, fill=(255, 255, 255)):
    """Cover-style title: white Sniglet with a dark outline and drop shadow."""
    f = font("Sniglet-ExtraBold.ttf", px)
    ov = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    bb = od.textbbox((0, 0), text, font=f)
    tx = int(cx - (bb[2] - bb[0]) / 2 - bb[0])
    o = max(2, int(px * S / 40))
    od.text((tx + o, y + 2 * o), text, font=f, fill=INK + (255,))
    for dx in (-o, 0, o):
        for dy in (-o, 0, o):
            if dx or dy:
                od.text((tx + dx, y + dy), text, font=f, fill=INK + (255,))
    od.text((tx, y), text, font=f, fill=fill + (255,))
    canvas.paste(ov, (0, 0), ov)
    return bb[3] - bb[1]

def fit(d, text, name, px, max_w):
    """Largest font size up to px (in 1x units) whose text fits max_w (1x px)."""
    while px > 10:
        f = font(name, px)
        bb = d.textbbox((0, 0), text, font=f)
        if bb[2] - bb[0] <= max_w * S:
            return f, px
        px -= 1
    return font(name, px), px

def centred(d, text, cx, y, f, fill):
    bb = d.textbbox((0, 0), text, font=f)
    d.text((int(cx - (bb[2] - bb[0]) / 2 - bb[0]), y), text, font=f, fill=fill)

def icon(d, kind, cx, cy, r):
    """Simple round badge icons drawn as shapes (no emoji fonts needed)."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255), outline=INK, width=3 * S)
    k = r * 0.5
    if kind == "star":
        import math
        pts = [(cx + (k if i % 2 == 0 else k * 0.45) * math.sin(i * math.pi / 5),
                cy - (k if i % 2 == 0 else k * 0.45) * math.cos(i * math.pi / 5)) for i in range(10)]
        d.polygon(pts, fill=(255, 196, 70), outline=INK)
    elif kind == "bulb":
        d.ellipse([cx - k * 0.7, cy - k, cx + k * 0.7, cy + k * 0.4], fill=(255, 225, 110), outline=INK, width=2 * S)
        d.rectangle([cx - k * 0.35, cy + k * 0.4, cx + k * 0.35, cy + k * 0.85], fill=(170, 170, 170), outline=INK, width=2 * S)
    elif kind == "heart":
        d.ellipse([cx - k, cy - k * 0.7, cx, cy + k * 0.2], fill=(240, 120, 130))
        d.ellipse([cx, cy - k * 0.7, cx + k, cy + k * 0.2], fill=(240, 120, 130))
        d.polygon([(cx - k * 0.97, cy - k * 0.1), (cx + k * 0.97, cy - k * 0.1), (cx, cy + k)], fill=(240, 120, 130))
    elif kind == "page":
        d.rectangle([cx - k * 0.6, cy - k * 0.8, cx + k * 0.6, cy + k * 0.8], fill=(255, 255, 255), outline=INK, width=3 * S)
        for i in range(3):
            yy = cy - k * 0.4 + i * k * 0.4
            d.line([(cx - k * 0.35, yy), (cx + k * 0.35, yy)], fill=(80, 160, 200), width=3 * S)

def save(img, name, w, h):
    os.makedirs(OUT, exist_ok=True)
    img.save(os.path.join(OUT, "%s_%dx%d_2x.jpg" % (name, w, h)), quality=92, subsampling=0)
    small = img.resize((w, h), Image.LANCZOS)
    path = os.path.join(OUT, "%s_%dx%d.jpg" % (name, w, h))
    small.save(path, quality=92, subsampling=0)
    print(name, small.size, "%.0f KB" % (os.path.getsize(path) / 1024))

# --- Module 1: brand banner with book mockup (970 x 300) -----------------------
def banner():
    w, h = 970, 300
    cv = background(w, h, 1)
    d = ImageDraw.Draw(cv)
    centred(d, "Matilda Hayes", 270 * S, 30 * S, font("Pacifico-Regular.ttf", 30), INK)
    centred(d, "GREAT BARRIER REEF", 270 * S, 92 * S, font("Baloo2.ttf", 22), SUB)
    _, tpx = fit(d, "OCEAN FRIENDS", "Sniglet-ExtraBold.ttf", 60, 470)
    bubble_text(cv, "OCEAN FRIENDS", 270 * S, 128 * S, tpx)
    centred(d, "A cute & comfy colouring book", 270 * S, 212 * S, font("Baloo2.ttf", 24), SUB)
    # mockup: inside page behind, cover in front
    pg = page_image(3, 150 * S)
    paste_center(cv, with_shadow(pg, angle=-6, border=True), 785 * S, 150 * S)
    cov = Image.open(COVER).convert("RGB")
    cov = cov.resize((150 * S, int(150 * S * cov.height / cov.width)), Image.LANCZOS)
    paste_center(cv, with_shadow(cov, angle=5), 640 * S, 152 * S)
    save(rounded(cv), "aplus_1_banner", w, h)

# --- Module 2: features with sample pages (970 x 600) --------------------------
def features():
    w, h = 970, 600
    cv = background(w, h, 2)
    d = ImageDraw.Draw(cv)
    paste_center(cv, with_shadow(page_image(1, 225 * S), angle=-5, border=True), 165 * S, 300 * S)
    paste_center(cv, with_shadow(page_image(21, 225 * S), angle=4, border=True), 340 * S, 310 * S)
    items = [("star", "50 big, bold designs", "Extra-thick lines for crayons and markers"),
             ("bulb", "A fun fact on every page", "Kids learn about the reef as they colour"),
             ("heart", "Made for ages 3 to 8", "Simple shapes and large open spaces"),
             ("page", "Single-sided pages", "Every design is on its own page")]
    # one heading size for all four, set by the longest heading
    hf, _ = fit(d, max((i[1] for i in items), key=len), "Sniglet-ExtraBold.ttf", 28, 380)
    y = 112 * S
    for kind, head, sub in items:
        icon(d, kind, 520 * S, y + 22 * S, 30 * S)
        d.text((566 * S, y - 4 * S), head, font=hf, fill=INK)
        d.text((566 * S, y + 36 * S), sub, font=font("Baloo2.ttf", 20), fill=SUB)
        y += 104 * S
    save(rounded(cv), "aplus_2_features", w, h)

# --- Module 3: single-sided pages explainer (970 x 600) ------------------------
def single_sided():
    w, h = 970, 600
    cv = background(w, h, 3)
    d = ImageDraw.Draw(cv)
    cov = Image.open(COVER).convert("RGB")
    cw = 300 * S
    cov = cov.resize((cw, int(cw * cov.height / cov.width)), Image.LANCZOS)
    cx, cy = 225 * S, 300 * S
    paste_center(cv, with_shadow(cov), cx, cy)
    # dimension arrows: 8.5 in across the bottom, 11 in up the left side
    left, right = cx - cw // 2, cx + cw // 2
    top, bot = cy - cov.height // 2, cy + cov.height // 2
    fa = font("Baloo2.ttf", 22)
    yb = bot + 22 * S
    d.line([(left, yb), (right, yb)], fill=INK, width=3 * S)
    for x, s in ((left, 1), (right, -1)):
        d.polygon([(x, yb), (x + s * 14 * S, yb - 7 * S), (x + s * 14 * S, yb + 7 * S)], fill=INK)
    centred(d, "8.5 in", cx, yb + 6 * S, fa, INK)
    xl = left - 26 * S
    d.line([(xl, top), (xl, bot)], fill=INK, width=3 * S)
    for y0, s in ((top, 1), (bot, -1)):
        d.polygon([(xl, y0), (xl - 7 * S, y0 + s * 14 * S), (xl + 7 * S, y0 + s * 14 * S)], fill=INK)
    lab = Image.new("RGBA", (120 * S, 40 * S), (0, 0, 0, 0))
    ImageDraw.Draw(lab).text((0, 0), "11 in", font=fa, fill=INK + (255,))
    lab = lab.rotate(90, expand=True)
    cv.paste(lab, (xl - 44 * S, cy - 30 * S), lab)
    # page with art in front, blank back sheet behind it
    blank = Image.new("RGB", (220 * S, int(220 * S * 11 / 8.5)), (255, 255, 255))
    paste_center(cv, with_shadow(blank, angle=7, border=True), 760 * S, 290 * S)
    paste_center(cv, with_shadow(page_image(31, 220 * S), angle=-3, border=True), 670 * S, 280 * S)
    bubble_text(cv, "Single-sided pages", 690 * S, 22 * S, 38)
    fb = font("Baloo2.ttf", 21)
    centred(d, "Every design has a blank back. Slip a sheet of card", 690 * S, 512 * S, fb, INK)
    centred(d, "underneath to stop markers bleeding through.", 690 * S, 540 * S, fb, INK)
    save(rounded(cv), "aplus_3_single_sided", w, h)

# --- Module 4: sample page grid (970 x 600) ------------------------------------
def grid():
    w, h = 970, 600
    cv = background(w, h, 4)
    bubble_text(cv, "Meet 50 reef friends", w * S // 2, 16 * S, 40)
    pages = [7, 18, 23, 25, 33, 50]
    pw = 180 * S
    for i, n in enumerate(pages):
        col, row = i % 3, i // 3
        cx = (w / 2 + (col - 1) * 290) * S
        cy = (205 + row * 255) * S
        paste_center(cv, with_shadow(page_image(n, pw), angle=(-2, 1.5, -1, 2, -1.5, 1)[i], border=True), cx, cy)
    save(rounded(cv), "aplus_4_sample_grid", w, h)

if __name__ == "__main__":
    banner(); features(); single_sided(); grid()
