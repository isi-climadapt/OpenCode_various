# -*- coding: utf-8 -*-
# STAGE 7 (A+ Content), Author 3 Book 2 (Who Frosted My Tree?). Copied from book1\aplus_build.py
# (rule 15), which was copied from the latest A+ builder,
# Author 1\book4\aplus_build.py (commit 90f22ed), and adapted for a full-color story book:
#   - art cards show the real typeset story pages (trimmed), not traced line art
#   - module 3 "single-sided pages" (a coloring-book feature) becomes "Meet the cast"
#   - author3 style: Chewy titles in warm yellow with a night-blue outline, Nunito body text,
#     twilight lavender panels with stars
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
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ---- per-book settings -------------------------------------------------------
BOOK = {
    "upload_dir": "KDP_FINAL_UPLOAD",
    "cover": "cover_option_C.png",
    "title": "Who Frosted My Tree?",
    "author": "Hattie Moss",
    "kicker": "A FUNNY AUSTRALIAN WINTER MYSTERY",
    "tagline": "Starring Banjo the sugar glider",
    "isbn": "",
    "asin": "",
    "banner_page": (27, "Banjo gliding through the snow"),
    "feature_pages": [(11, "the cross cockatoo"), (14, "Possum's snowy face")],
    "features": [("star", "A funny snow-day mystery", "Silly suspects and a missing friend"),
                 ("heart", "A cozy winter read-aloud", "For snowy nights at home and at school"),
                 ("bulb", "True facts about hibernation", "Real animals that sleep through winter"),
                 ("book", "Made for ages 3 to 5", "Short lines and big shouted words")],
    # cast: (label, source image, crop box in fractions); same sheets as Book 1
    "cast": [("Banjo", "../book1/char_test/sheet_nbpro.png", (0.04, 0.03, 0.44, 0.395)),
             ("Olive", "../book1/char_test/sheet_nbpro.png", (0.57, 0.53, 0.95, 0.95)),
             ("Cockatoo", "../book1/char_test/sheet_cast.png", (0.04, 0.02, 0.36, 0.47)),
             ("Possum", "../book1/char_test/sheet_cast.png", (0.50, 0.06, 0.95, 0.44)),
             ("Wombat", "../book1/char_test/sheet_cast.png", (0.04, 0.64, 0.42, 0.95)),
             ("Echidna", "../book1/char_test/sheet_cast.png", (0.30, 0.38, 0.70, 0.67))],
    "cast_heading": "THE SUSPECTS AND A FRIEND",
    "cast_line": "Who frosted the tree? Read it to find out.",
    "grid_title": "A snow day in the bush",
    "grid_pages": [(6, "Banjo waking up to snow"), (8, "Olive under the snow"), (12, "the first snowflake"),
                   (16, "Wombat's snowball"), (21, "Banjo's lonely night"), (27, "Banjo's snowy glide")],
    "sky": (226, 220, 245),       # twilight lavender, from the cover sky
    "sky_light": (240, 236, 252),
}
# -----------------------------------------------------------------------------

ST = {"title_fill": (255, 222, 120), "title_line": (38, 34, 86),
      "ink": (38, 34, 86), "sub": (84, 78, 128)}

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")
OUT = os.path.join(HERE, "aplus")
UPLOAD = os.path.normpath(os.path.join(HERE, BOOK["upload_dir"]))
TYPESET = os.path.join(HERE, "typeset")
COVER = os.path.join(HERE, BOOK["cover"])
TRIM, BLEED = 2550, 38

S = 2  # draw scale
SKY, SKY_LIGHT = BOOK["sky"], BOOK["sky_light"]
INK, SUB = ST["ink"], ST["sub"]

def font(kind, px):
    if kind == "title":
        return ImageFont.truetype(os.path.join(FONTS, "Chewy-Regular.ttf"), int(px * S))
    f = ImageFont.truetype(os.path.join(FONTS, "Nunito[wght].ttf"), int(px * S))
    f.set_variation_by_name("ExtraBold" if kind == "head" else "Bold")
    return f

def page_image(n, px):
    """Typeset story page n, cropped to the trim box, px square."""
    im = Image.open(os.path.join(TYPESET, "p%02d.png" % n)).convert("RGB")
    ox = 0 if n % 2 else BLEED
    return im.crop((ox, BLEED, ox + TRIM, BLEED + TRIM)).resize((px, px), Image.LANCZOS)

def with_shadow(img, angle=0, radius=10, offset=(6, 10)):
    img = img.convert("RGBA")
    pad = radius * 3 * S
    cv = Image.new("RGBA", (img.width + 2 * pad, img.height + 2 * pad), (0, 0, 0, 0))
    sh = Image.new("RGBA", img.size, (20, 18, 60, 90))
    cv.paste(sh, (pad + offset[0] * S, pad + offset[1] * S), img.split()[3])
    cv = cv.filter(ImageFilter.GaussianBlur(radius * S))
    cv.paste(img, (pad, pad), img)
    return cv.rotate(angle, resample=Image.BICUBIC, expand=True)

def paste_center(canvas, rgba, cx, cy):
    canvas.paste(rgba, (int(cx - rgba.width / 2), int(cy - rgba.height / 2)), rgba)

def background(w, h, seed):
    """Twilight panel with soft bands, small stars and sparkles."""
    W, H = w * S, h * S
    bg = Image.new("RGB", (W, H), SKY)
    d = ImageDraw.Draw(bg)
    rnd = random.Random(seed)
    for k in range(3):
        y = int(H * (0.25 + 0.3 * k)) + rnd.randint(-20, 20) * S
        pts = [(x, y + int(18 * S * math.sin(x / (90.0 * S) + k))) for x in range(0, W + 10, 10)]
        d.line(pts, fill=SKY_LIGHT, width=10 * S)
    for _ in range(int(w / 40)):
        r = rnd.randint(3, 7) * S
        x, y = rnd.randint(0, W), rnd.randint(0, H)
        d.ellipse([x - r // 2, y - r // 2, x + r // 2, y + r // 2], fill=(255, 255, 255))
    for _ in range(int(w / 90)):
        x, y, r = rnd.randint(0, W), rnd.randint(0, H), rnd.randint(6, 12) * S
        d.polygon([(x, y - r), (x + r / 4, y - r / 4), (x + r, y), (x + r / 4, y + r / 4),
                   (x, y + r), (x - r / 4, y + r / 4), (x - r, y), (x - r / 4, y - r / 4)], fill=(255, 250, 225))
    return bg

def rounded(canvas, radius=26):
    m = Image.new("L", canvas.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, canvas.width - 1, canvas.height - 1], radius=radius * S, fill=255)
    out = Image.new("RGB", canvas.size, (255, 255, 255))
    out.paste(canvas, (0, 0), m)
    return out

def title_text(canvas, text, cx, y, px):
    """Cover-style title: Chewy, warm yellow, night-blue outline and drop shadow."""
    f = font("title", px)
    ov = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    bb = od.textbbox((0, 0), text, font=f)
    tx = int(cx - (bb[2] - bb[0]) / 2 - bb[0])
    o = max(2, int(px * S / 40))
    od.text((tx + o, y + 2 * o), text, font=f, fill=INK + (255,))
    for dx in (-o, 0, o):
        for dy in (-o, 0, o):
            if dx or dy:
                od.text((tx + dx, y + dy), text, font=f, fill=ST["title_line"] + (255,))
    od.text((tx, y), text, font=f, fill=ST["title_fill"] + (255,))
    canvas.paste(ov, (0, 0), ov)
    return bb[3] - bb[1]

def fit(d, text, kind, px, max_w):
    while px > 10:
        f = font(kind, px)
        bb = d.textbbox((0, 0), text, font=f)
        if bb[2] - bb[0] <= max_w * S:
            return f, px
        px -= 1
    return font(kind, px), px

def centred(d, text, cx, y, f, fill):
    bb = d.textbbox((0, 0), text, font=f)
    d.text((int(cx - (bb[2] - bb[0]) / 2 - bb[0]), y), text, font=f, fill=fill)

def icon(d, kind, cx, cy, r):
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
    elif kind == "book":
        d.polygon([(cx, cy - k * 0.5), (cx - k, cy - k * 0.8), (cx - k, cy + k * 0.6), (cx, cy + k * 0.9)],
                  fill=(150, 200, 235), outline=INK)
        d.polygon([(cx, cy - k * 0.5), (cx + k, cy - k * 0.8), (cx + k, cy + k * 0.6), (cx, cy + k * 0.9)],
                  fill=(150, 200, 235), outline=INK)

def save(img, name, w, h):
    """Write the 2x upload file and a minimum-size fallback. Returns the upload file name."""
    os.makedirs(OUT, exist_ok=True)
    big = os.path.join(OUT, "%s_%dx%d.jpg" % (name, w * S, h * S))
    img.save(big, quality=92, subsampling=0)
    img.resize((w, h), Image.LANCZOS).save(os.path.join(OUT, "%s_%dx%d.jpg" % (name, w, h)), quality=92, subsampling=0)
    print(name, img.size, "%.0f KB" % (os.path.getsize(big) / 1024))
    return os.path.basename(big)

def page_card(n, px, angle=0):
    """A story page as a rounded card with a cream edge and soft shadow."""
    pg = page_image(n, px)
    card = Image.new("RGBA", (px, px), (0, 0, 0, 0))
    m = Image.new("L", (px, px), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, px - 1, px - 1], radius=int(px * 0.05), fill=255)
    card.paste(pg, (0, 0), m)
    ImageDraw.Draw(card).rounded_rectangle([0, 0, px - 1, px - 1], radius=int(px * 0.05),
                                           outline=(255, 249, 236, 255), width=max(3, int(px * 0.02)))
    return with_shadow(card, angle=angle)

def character(src, box, px):
    """Character crop from a model sheet, its white background made transparent."""
    im = Image.open(os.path.join(HERE, src)).convert("RGB")
    W, H = im.size
    im = im.crop((int(box[0] * W), int(box[1] * H), int(box[2] * W), int(box[3] * H)))
    a = np.asarray(im).astype(int)
    from scipy import ndimage
    # background = near-white paper connected to the crop border (a white belly or chest
    # inside the outline stays opaque); a global threshold made those see-through
    paper = a.min(2) > 225
    lab, _ = ndimage.label(paper)
    edge = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    fg = ~np.isin(lab, list(edge))
    # keep the character only: drop fragments of neighbouring figures cut by the crop box
    lab, n = ndimage.label(ndimage.binary_closing(fg, iterations=3))
    if n > 1:
        sizes = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))
        fg &= np.isin(lab, [i + 1 for i, s in enumerate(sizes) if s >= 0.08 * sizes.max()])
    alpha = (fg * 255).astype("uint8")
    rgba = im.convert("RGBA")
    rgba.putalpha(Image.fromarray(alpha).filter(ImageFilter.GaussianBlur(1.5)))
    bb = rgba.getbbox()
    rgba = rgba.crop(bb)
    k = px / max(rgba.size)
    return rgba.resize((int(rgba.width * k), int(rgba.height * k)), Image.LANCZOS)

# --- Module 1: brand banner with book mockup (970 x 300) -----------------------
def banner():
    w, h = 970, 300
    cv = background(w, h, 1)
    d = ImageDraw.Draw(cv)
    centred(d, BOOK["author"], 265 * S, 22 * S, font("head", 30), SUB)
    fk, _ = fit(d, BOOK["kicker"], "body", 22, 470)
    centred(d, BOOK["kicker"], 265 * S, 72 * S, fk, INK)
    _, tpx = fit(d, BOOK["title"], "title", 66, 500)
    title_text(cv, BOOK["title"], 265 * S, 112 * S, tpx)
    centred(d, BOOK["tagline"], 265 * S, 222 * S, font("body", 26), SUB)
    paste_center(cv, page_card(BOOK["banner_page"][0], 220 * S, angle=-5), 820 * S, 150 * S)
    cov = Image.open(COVER).convert("RGB")
    cov = cov.resize((215 * S, int(215 * S * cov.height / cov.width)), Image.LANCZOS)
    paste_center(cv, with_shadow(cov, angle=4), 630 * S, 150 * S)
    return save(rounded(cv), "aplus_1_banner", w, h)

# --- Module 2: features with large sample pages (970 x 600) --------------------
def features():
    w, h = 970, 600
    cv = background(w, h, 2)
    d = ImageDraw.Draw(cv)
    (p1, _), (p2, _) = BOOK["feature_pages"]
    paste_center(cv, page_card(p1, 285 * S, angle=-4), 175 * S, 190 * S)
    paste_center(cv, page_card(p2, 285 * S, angle=3), 300 * S, 415 * S)
    items = BOOK["features"]
    hf, _ = fit(d, max((i[1] for i in items), key=len), "title", 36, 395)
    sf = min((fit(d, i[2], "body", 24, 395) for i in items), key=lambda r: r[1])[0]
    y = 78 * S
    for kind, head, sub in items:
        icon(d, kind, 500 * S, y + 28 * S, 34 * S)
        d.text((548 * S, y - 6 * S), head, font=hf, fill=INK)
        d.text((548 * S, y + 42 * S), sub, font=sf, fill=SUB)
        y += 122 * S
    return save(rounded(cv), "aplus_2_features", w, h)

# --- Module 3: meet the cast (970 x 600), replaces the coloring "single-sided" module ---
def cast():
    w, h = 970, 600
    cv = background(w, h, 3)
    d = ImageDraw.Draw(cv)
    title_text(cv, "Meet the cast", w * S // 2, 14 * S, 50)
    hero = BOOK["cast"][:2]
    rest = BOOK["cast"][2:]
    # Banjo and Olive large on the left; suspects in a 2 x 2 grid on the right
    for i, (label, src, box) in enumerate(hero):
        cx, cy = (150 + i * 230) * S, 300 * S
        ch = character(src, box, 230 * S)
        paste_center(cv, with_shadow(ch, radius=6, offset=(3, 6)), cx, cy)
        centred(d, label, cx, (cy + 128 * S), font("title", 40), INK)
    centred(d, BOOK["cast_heading"], 760 * S, 92 * S, font("head", 22), SUB)
    for i, (label, src, box) in enumerate(rest):
        cx, cy = (680 + (i % 2) * 165) * S, (205 + (i // 2) * 190) * S
        ch = character(src, box, 130 * S)
        paste_center(cv, with_shadow(ch, radius=5, offset=(2, 5)), cx, cy)
        centred(d, label, cx, cy + 74 * S, font("head", 24), INK)
    fb, _ = fit(d, BOOK["cast_line"], "body", 24, 420)
    centred(d, BOOK["cast_line"], 265 * S, 552 * S, fb, INK)
    return save(rounded(cv), "aplus_3_cast", w, h)

# --- Module 4: sample page grid (970 x 600) ------------------------------------
def grid():
    w, h = 970, 600
    cv = background(w, h, 4)
    d = ImageDraw.Draw(cv)
    _, gpx = fit(d, BOOK["grid_title"], "title", 48, 880)
    title_text(cv, BOOK["grid_title"], w * S // 2, 12 * S, gpx)
    cpx = 238 * S
    for i, (n, _) in enumerate(BOOK["grid_pages"]):
        col, row = i % 3, i // 3
        cx = (w / 2 + (col - 1) * 290) * S
        cy = (210 + row * 255) * S
        paste_center(cv, page_card(n, cpx, angle=(-2, 1.5, -1, 2, -1.5, 1)[i]), cx, cy)
    return save(rounded(cv), "aplus_4_sample_grid", w, h)

# --- Upload guide: the module table, filled in for this book -------------------
def write_guide(files):
    dest = os.path.join(UPLOAD, "03_A_PLUS_CONTENT")
    os.makedirs(dest, exist_ok=True)
    for old in os.listdir(dest):
        if old.lower().endswith(".jpg") and old not in files:
            os.remove(os.path.join(dest, old))
    for f in files:
        shutil.copyfile(os.path.join(OUT, f), os.path.join(dest, f))
    feat = " and ".join(a for _, a in BOOK["feature_pages"])
    grid_names = ", ".join(a for _, a in BOOK["grid_pages"])
    cast_names = ", ".join(c[0] for c in BOOK["cast"])
    rows = [
        ("1", "Standard Image & Light Text Overlay (970 x 300 minimum)", files[0],
         "%s picture book by %s, cover and a page of %s" % (BOOK["title"], BOOK["author"], BOOK["banner_page"][1]),
         BOOK["title"]),
        ("2", "Standard Image Header With Text (970 x 600 minimum)", files[1],
         "Story pages with %s, and the book's features" % feat, "What's inside"),
        ("3", "Standard Image Header With Text (970 x 600 minimum)", files[2],
         "The characters: %s" % cast_names, "Meet the cast"),
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
    L += ["5. Next: Apply ASINs > search " + find + " > add the paperback (and the Kindle",
          "   edition once it exists).",
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
    write_guide([banner(), features(), cast(), grid()])
