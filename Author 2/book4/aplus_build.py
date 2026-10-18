# -*- coding: utf-8 -*-
# STAGE 7 (A+ Content): Amazon A+ images + copy-paste upload guide, modelled on the
# bestseller pattern (Coco Wyo "Ocean Scene"): brand banner with book mockup,
# features with sample pages, single-sided pages explainer, sample page grid.
# Sample pages are rendered from the print interior PDF, so they show the real book.
# Each module is drawn at 2x, then reduced to the exact upload size (KDP doesn't resize).
#
# NEW BOOK: copy this file into the book folder and edit only BOOK below.
#
# Usage: py aplus_build.py
#   -> aplus/aplus_1_banner_1940x600.jpg ... (upload size, 2x Amazon's minimum)
#      + aplus/aplus_1_banner_970x300.jpg ... (minimum-size fallback)
#   -> KDP_FINAL_UPLOAD/03_A_PLUS_CONTENT/ (the 4 upload images)
#   -> KDP_FINAL_UPLOAD/03_A_PLUS_CONTENT_GUIDE.txt (module table + steps; table also printed)

import os, math, random, shutil
import fitz
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

# ---- per-book settings -------------------------------------------------------
BOOK = {
    "style": "author2",
    "upload_dir": "KDP_FINAL_UPLOAD",
    "cover": "cover_option_A.png",
    "imprint": "WATTLE WONDERS PUBLISHING",
    "badge": "AGES 4-8  |  FUN FACTS ON EVERY PAGE",
    "title": "Zoom Wonders",
    "author": "Flora Watt",
    "kicker": "",
    "banner_title": "ZOOM WONDERS",
    "tagline": "",
    "isbn": "",                  # fill in after KDP assigns it, then rerun
    "asin": "",                  # fill in once the book is live, then rerun
    "banner_page": (1, "fire truck"),
    "feature_pages": [(10, "road train"), (32, "submarine")],
    "single_sided_page": (48, "rocket"),
    "grid_title": "Meet 50 amazing vehicles",
    "grid_pages": [(7, "monster truck"), (16, "excavator"), (27, "bullet train"),
                   (31, "sailboat"), (39, "hot air balloon"), (50, "Moon buggy")],
    "features": [("star", "50 big & bold designs", "Trucks, trains, boats, planes and rockets"),
                 ("bulb", "A real vehicle fact on every page", "From road trains to Moon buggies"),
                 ("heart", "Ages 4 to 8", "Thick outlines and huge open spaces"),
                 ("page", "Single-sided pages", "Every design is on its own page")],
    "sky": (240, 120, 110),      # cherry red (Author 2 primaries; fire trucks)
    "sky_light": (248, 166, 156),
    "art_dir": "raw2",           # 1K line art the cards are traced from
    "line_boost": 0.0055,        # line thickening for the cards (fraction of card size)
    "imprint_color": (28, 48, 104),  # navy: house green is ~1.7:1 on the red panel
}
# -----------------------------------------------------------------------------

# Locked brand styles (AGENT-PIPELINE.md rule 0 / each author's publishing/00-brand-identity.md)
STYLES = {
    "author1": {"title_font": "Sniglet-ExtraBold.ttf", "title_fill": (255, 255, 255),
                "title_line": (35, 25, 20), "body": "Baloo2.ttf", "script": "Pacifico-Regular.ttf",
                "ink": (35, 25, 20), "sub": (80, 60, 50), "motif": "bubbles"},
    "author2": {"title_font": "LilitaOne-Regular.ttf", "title_fill": (28, 48, 104),
                "title_line": (255, 255, 255), "body": "Fredoka.ttf", "script": None,
                "ink": (28, 48, 104), "sub": (55, 70, 105), "motif": "stars",
                "badge": (250, 200, 40), "imprint": (60, 130, 60)},
}
ST = STYLES[BOOK["style"]]
if "imprint_color" in BOOK:
    ST = dict(ST, imprint=BOOK["imprint_color"])

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")
OUT = os.path.join(HERE, "aplus")
UPLOAD = os.path.normpath(os.path.join(HERE, BOOK["upload_dir"]))
INTERIOR = os.path.join(UPLOAD, "01_MANUSCRIPT_INTERIOR_108P.pdf")
COVER = os.path.join(HERE, BOOK["cover"])

S = 2  # draw scale
SKY, SKY_LIGHT = BOOK["sky"], BOOK["sky_light"]
INK, SUB = ST["ink"], ST["sub"]
BODY = ST["body"]

def font(name, px):
    f = ImageFont.truetype(os.path.join(FONTS, name), int(px * S))
    try:  # Fredoka's variable font defaults to Light (300); lift light defaults to Medium
        w = [a for a in f.get_variation_axes() if a["name"] == b"Weight"]
        if w and w[0]["default"] < 400:
            f.set_variation_by_name("Medium")
    except (OSError, ValueError):
        pass  # not a variable font
    return f

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
    """Panel in the book's color with soft wave bands, bubbles and sparkles."""
    W, H = w * S, h * S
    bg = Image.new("RGB", (W, H), SKY)
    d = ImageDraw.Draw(bg)
    rnd = random.Random(seed)
    for k in range(3):  # soft wave bands
        y = int(H * (0.25 + 0.3 * k)) + rnd.randint(-20, 20) * S
        pts = [(x, y + int(18 * S * math.sin(x / (90.0 * S) + k))) for x in range(0, W + 10, 10)]
        d.line(pts, fill=SKY_LIGHT, width=10 * S)
    for _ in range(int(w / 40)):  # bubbles (author1) or little planets/dots (author2)
        r = rnd.randint(4, 11) * S
        x, y = rnd.randint(0, W), rnd.randint(0, H)
        if ST["motif"] == "stars":
            d.ellipse([x - r // 2, y - r // 2, x + r // 2, y + r // 2], fill=(255, 255, 255))
        else:
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

def bubble_text(canvas, text, cx, y, px):
    """Cover-style title in the author's title font, outlined, with a drop shadow."""
    f = font(ST["title_font"], px)
    fill, line = ST["title_fill"], ST["title_line"]
    ov = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    bb = od.textbbox((0, 0), text, font=f)
    tx = int(cx - (bb[2] - bb[0]) / 2 - bb[0])
    o = max(2, int(px * S / 40))
    od.text((tx + o, y + 2 * o), text, font=f, fill=INK + (255,))
    for dx in (-o, 0, o):
        for dy in (-o, 0, o):
            if dx or dy:
                od.text((tx + dx, y + dy), text, font=f, fill=line + (255,))
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
    """Write the 2x upload file and a minimum-size fallback. Returns the upload file name.
    Amazon's sizes are minimums: KDP's previews and high-resolution screens enlarge a
    970 px file and it looks pixelated, so the 2x file is the one to upload."""
    os.makedirs(OUT, exist_ok=True)
    big = os.path.join(OUT, "%s_%dx%d.jpg" % (name, w * S, h * S))
    img.save(big, quality=92, subsampling=0)
    img.resize((w, h), Image.LANCZOS).save(os.path.join(OUT, "%s_%dx%d.jpg" % (name, w, h)), quality=92, subsampling=0)
    print(name, img.size, "%.0f KB" % (os.path.getsize(big) / 1024))
    return os.path.basename(big)

# --- Art cards: the sample art large, cropped, with thick lines ----------------
# Amazon shows A+ panels at a fixed 970 px and screens scaled above 100% stretch
# them, so whole pages with tiny captions go soft. Cards show only the art,
# traced from the vector outlines at the exact size and thickened so lines
# survive Amazon's JPEG and the stretch.
def art_image(n, px):
    """Page n's art as a px-square L image: traced at 2x, cropped to the ink, lines thickened."""
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(HERE), "scripts"))
    from vectorize_line_art import vectorize_line_art
    src = os.path.join(HERE, BOOK["art_dir"], "page_%02d.png" % n)
    big = vectorize_line_art(src, None, px * 2, px * 2)
    ink = ImageOps.invert(big).getbbox()
    if ink:
        pad = int(px * 2 * 0.02)
        big = big.crop((max(0, ink[0] - pad), max(0, ink[1] - pad),
                        min(big.width, ink[2] + pad), min(big.height, ink[3] + pad)))
    k = max(3, int(px * 2 * BOOK["line_boost"]) | 1)  # odd MinFilter size grows every black line
    big = big.filter(ImageFilter.MinFilter(k))
    scale = px / max(big.size)
    return big.resize((max(1, int(big.width * scale)), max(1, int(big.height * scale))), Image.LANCZOS)

def art_card(n, px, angle=0):
    """White rounded card with the page's art filling it, dark outline, soft shadow."""
    pad = int(px * 0.06)
    art = art_image(n, px - 2 * pad)
    card = Image.new("RGBA", (px, px), (0, 0, 0, 0))
    m = Image.new("L", (px, px), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, px - 1, px - 1], radius=int(px * 0.07), fill=255)
    card.paste(Image.new("RGBA", (px, px), (255, 255, 255, 255)), (0, 0), m)
    card.paste(Image.new("RGBA", art.size, INK + (255,)), ((px - art.width) // 2, (px - art.height) // 2), ImageOps.invert(art))
    ImageDraw.Draw(card).rounded_rectangle([0, 0, px - 1, px - 1], radius=int(px * 0.07),
                                           outline=INK + (255,), width=max(2, int(px * 0.012)))
    return with_shadow(card, angle=angle)

def sheet(n, w, angle=0):
    """A portrait page (8.5 x 11) showing the art large, no caption."""
    h = int(w * 11 / 8.5)
    pg = Image.new("RGB", (w, h), (255, 255, 255))
    art = art_image(n, int(w * 0.9))
    pg.paste(Image.new("RGB", art.size, INK), ((w - art.width) // 2, int(h * 0.42) - art.height // 2), ImageOps.invert(art))
    return with_shadow(pg, angle=angle, border=True)

# --- Module 1: brand banner with book mockup (970 x 300) -----------------------
def banner():
    w, h = 970, 300
    cv = background(w, h, 1)
    d = ImageDraw.Draw(cv)
    if ST["script"]:  # author1: script author name, kicker, bubble title, tagline
        centred(d, BOOK["author"], 265 * S, 22 * S, font(ST["script"], 34), INK)
        centred(d, BOOK["kicker"], 265 * S, 90 * S, font(BODY, 26), SUB)
        _, tpx = fit(d, BOOK["banner_title"], ST["title_font"], 72, 500)
        bubble_text(cv, BOOK["banner_title"], 265 * S, 124 * S, tpx)
        centred(d, BOOK["tagline"], 265 * S, 222 * S, font(BODY, 28), SUB)
    else:  # author2: imprint line, poster title, yellow age/fact badge
        centred(d, BOOK["imprint"], 265 * S, 28 * S, font(BODY, 24), ST["imprint"])
        _, tpx = fit(d, BOOK["banner_title"], ST["title_font"], 84, 500)
        bubble_text(cv, BOOK["banner_title"], 265 * S, 72 * S, tpx)
        fb, _ = fit(d, BOOK["badge"], BODY, 26, 440)  # badge must stay inside the left half
        bb = d.textbbox((0, 0), BOOK["badge"], font=fb)
        bw, bh = bb[2] - bb[0] + 44 * S, 52 * S
        x0, y0 = 265 * S - bw // 2, 200 * S
        d.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], radius=14 * S, fill=ST["badge"], outline=INK, width=3 * S)
        centred(d, BOOK["badge"], 265 * S, y0 + (bh - (bb[3] - bb[1])) // 2 - bb[1], fb, INK)
    # mockup: big art card behind, cover in front
    paste_center(cv, art_card(BOOK["banner_page"][0], 212 * S, angle=-5), 815 * S, 150 * S)
    cov = Image.open(COVER).convert("RGB")
    cov = cov.resize((190 * S, int(190 * S * cov.height / cov.width)), Image.LANCZOS)
    paste_center(cv, with_shadow(cov, angle=4), 630 * S, 150 * S)
    return save(rounded(cv), "aplus_1_banner", w, h)

# --- Module 2: features with large sample art (970 x 600) ----------------------
def features():
    w, h = 970, 600
    cv = background(w, h, 2)
    d = ImageDraw.Draw(cv)
    (p1, _), (p2, _) = BOOK["feature_pages"]
    paste_center(cv, art_card(p1, 285 * S, angle=-4), 175 * S, 190 * S)
    paste_center(cv, art_card(p2, 285 * S, angle=3), 300 * S, 415 * S)
    items = BOOK["features"]
    # one heading size for all four, set by the longest heading; same for the sub-lines
    hf, _ = fit(d, max((i[1] for i in items), key=len), ST["title_font"], 36, 395)
    sf = min((fit(d, i[2], BODY, 25, 395) for i in items), key=lambda r: r[1])[0]
    y = 78 * S
    for kind, head, sub in items:
        icon(d, kind, 500 * S, y + 28 * S, 34 * S)
        d.text((548 * S, y - 6 * S), head, font=hf, fill=INK)
        d.text((548 * S, y + 42 * S), sub, font=sf, fill=SUB)
        y += 122 * S
    return save(rounded(cv), "aplus_2_features", w, h)

# --- Module 3: single-sided pages explainer (970 x 600) ------------------------
def single_sided():
    w, h = 970, 600
    cv = background(w, h, 3)
    d = ImageDraw.Draw(cv)
    cov = Image.open(COVER).convert("RGB")
    cw = 290 * S
    cov = cov.resize((cw, int(cw * cov.height / cov.width)), Image.LANCZOS)
    cx, cy = 215 * S, 290 * S
    paste_center(cv, with_shadow(cov), cx, cy)
    # dimension arrows: 8.5 in across the bottom, 11 in up the left side
    left, right = cx - cw // 2, cx + cw // 2
    top, bot = cy - cov.height // 2, cy + cov.height // 2
    fa = font(BODY, 28)
    yb = bot + 24 * S
    d.line([(left, yb), (right, yb)], fill=INK, width=4 * S)
    for x, s in ((left, 1), (right, -1)):
        d.polygon([(x, yb), (x + s * 16 * S, yb - 8 * S), (x + s * 16 * S, yb + 8 * S)], fill=INK)
    centred(d, "8.5 in", cx, yb + 6 * S, fa, INK)
    xl = left - 28 * S
    d.line([(xl, top), (xl, bot)], fill=INK, width=4 * S)
    for y0, s in ((top, 1), (bot, -1)):
        d.polygon([(xl, y0), (xl - 8 * S, y0 + s * 16 * S), (xl + 8 * S, y0 + s * 16 * S)], fill=INK)
    lab = Image.new("RGBA", (140 * S, 50 * S), (0, 0, 0, 0))
    ImageDraw.Draw(lab).text((0, 0), "11 in", font=fa, fill=INK + (255,))
    lab = lab.rotate(90, expand=True)
    cv.paste(lab, (xl - 52 * S, cy - 36 * S), lab)
    # page with big art in front, blank back sheet behind it
    blank = Image.new("RGB", (250 * S, int(250 * S * 11 / 8.5)), (255, 255, 255))
    paste_center(cv, with_shadow(blank, angle=7, border=True), 775 * S, 300 * S)
    paste_center(cv, sheet(BOOK["single_sided_page"][0], 250 * S, angle=-3), 680 * S, 290 * S)
    bubble_text(cv, "Single-sided pages", 680 * S, 16 * S, 42)
    fb, _ = fit(d, "Slip card underneath for markers.", BODY, 27, 440)
    centred(d, "Every design has a blank back.", 690 * S, 506 * S, fb, INK)
    centred(d, "Slip card underneath for markers.", 690 * S, 542 * S, fb, INK)
    return save(rounded(cv), "aplus_3_single_sided", w, h)

# --- Module 4: sample art grid (970 x 600) -------------------------------------
def grid():
    w, h = 970, 600
    cv = background(w, h, 4)
    d = ImageDraw.Draw(cv)
    _, gpx = fit(d, BOOK["grid_title"], ST["title_font"], 48, 880)
    bubble_text(cv, BOOK["grid_title"], w * S // 2, 12 * S, gpx)
    cpx = 238 * S
    for i, (n, _) in enumerate(BOOK["grid_pages"]):
        col, row = i % 3, i // 3
        cx = (w / 2 + (col - 1) * 290) * S
        cy = (210 + row * 255) * S
        paste_center(cv, art_card(n, cpx, angle=(-2, 1.5, -1, 2, -1.5, 1)[i]), cx, cy)
    return save(rounded(cv), "aplus_4_sample_grid", w, h)

# --- Upload guide: the module table, filled in for this book -------------------
def write_guide(files):
    """Copy the upload images into KDP_FINAL_UPLOAD and write the copy-paste guide.
    The module table is also printed so the agent can show it in its reply (pipeline rule 11)."""
    dest = os.path.join(UPLOAD, "03_A_PLUS_CONTENT")
    os.makedirs(dest, exist_ok=True)
    for old in os.listdir(dest):  # drop images from earlier runs (e.g. 970 px files)
        if old.lower().endswith(".jpg") and old not in files:
            os.remove(os.path.join(dest, old))
    for f in files:
        shutil.copyfile(os.path.join(OUT, f), os.path.join(dest, f))
    feat = " and ".join(a for _, a in BOOK["feature_pages"])
    grid_names = ", ".join(a for _, a in BOOK["grid_pages"])
    rows = [
        ("1", "Standard Image & Light Text Overlay (970 x 300 minimum)", files[0],
         "%s coloring book by %s, cover and %s page" % (BOOK["title"], BOOK["author"], BOOK["banner_page"][1]),
         BOOK["title"]),
        ("2", "Standard Image Header With Text (970 x 600 minimum)", files[1],
         "%s coloring pages with the book's features" % (feat[:1].upper() + feat[1:]), "What's inside"),
        ("3", "Standard Image Header With Text (970 x 600 minimum)", files[2],
         "8.5 by 11 inch book with single-sided coloring pages", "Single-sided pages"),
        ("4", "Standard Image Header With Text (970 x 600 minimum)", files[3],
         "Six sample pages: %s" % grid_names, BOOK["grid_title"]),
    ]
    table = ["| # | Module | Image | Alt text |", "|---|---|---|---|"] + \
            ["| %s | %s | `%s` | %s |" % (n, mod, f, alt) for n, mod, f, alt, _ in rows]
    find = (BOOK["isbn"] or "the paperback ISBN (KDP > Bookshelf)") + \
           (" or ASIN " + BOOK["asin"] if BOOK["asin"] else "")
    L = ["=" * 80, "AMAZON A+ CONTENT UPLOAD GUIDE (READY TO COPY & PASTE)",
         "Book Title: " + BOOK["title"], "=" * 80, "",
         "Images to upload: the 03_A_PLUS_CONTENT folder inside KDP_FINAL_UPLOAD.",
         "They are 2x Amazon's minimum size (1940 x 600 and 1940 x 1200), so they stay sharp in",
         "KDP's preview and on high-resolution screens. Don't upload the 970 px files in aplus\\.",
         "",
         "BEFORE YOU START: KDP doesn't publish module sizes. The sizes below are minimums from",
         "third-party guides. If KDP rejects a larger file, use the 970 px version from aplus\\.",
         "",
         "MODULE TABLE",
         ""] + table + [
         "",
         "STEPS",
         "1. KDP > Marketing (top menu) > A+ Content card.",
         "2. Choose the marketplace (start with Amazon.com) > Manage A+ Content.",
         "3. Start creating A+ content. Name: \"%s A+\" (readers don't see it). Language: English." % BOOK["title"],
         "4. Add the four modules in table order. Upload the image and paste the alt text.",
         "   Leave text fields empty (the images carry their text). If KDP insists on a",
         "   headline, use the one listed.",
         ""]
    for n, mod, f, alt, head in rows:
        L += ["   MODULE %s: %s" % (n, mod),
              "     Image:    " + f,
              "     Alt text: " + alt,
              "     Headline (only if required): " + head, ""]
    L += ["5. Next: Apply ASINs > search " + find + " > add the paperback.",
          "6. Review & submit. Approved content appears within about eight business days.",
          "7. Repeat for Amazon.com.au and every other store you sell in (A+ is set per",
          "   marketplace). Copy the content across if KDP offers to.",
          "",
          "If Amazon rejects an image, the likely cause is the inside-page samples. Note the",
          "rejection message and rebuild that module."]
    path = os.path.join(UPLOAD, "03_A_PLUS_CONTENT_GUIDE.txt")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")
    print("guide ->", path)
    print("\n".join(table))

if __name__ == "__main__":
    write_guide([banner(), features(), single_sided(), grid()])
