# -*- coding: utf-8 -*-
# Author 3 Book 1 - Who Peeled My Tree? full cover wrap (KDP paperback, premium color, 8.5 x 8.5).
# Based on the latest wrap builder, Author 1\book4\create_cover_wrap4.py (commit 90f22ed):
# front pasted at true size inside its trim, back with title, blurb, sample cards, bio box,
# barcode zone, imprint line; JPEG quality 100 with no chroma subsampling in the PDF.
# Spine: 32 pages x 0.002347 in (premium color, KDP Paperback Submission Guidelines) = 0.0751 in
# = 22.5 px -> 23 px. No spine text (KDP allows spine text from 79 pages).
# Wrap: 0.125 + 8.5 + 0.0751 + 8.5 + 0.125 = 17.325 in x 8.75 in -> 5198 x 2625 px at 300 DPI.
# Usage: py create_cover_wrap.py

import os, shutil, time
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from PIL import JpegImagePlugin  # noqa: F401, registers JPEG handler needed by PDF save

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")
TRIM, BLEED, SPINE = 2550, 38, 22   # 22.5 px exact; 22 keeps the wrap at 5198 px = 17.327 in vs 17.325
CW, CH = BLEED + TRIM + SPINE + TRIM + BLEED, 2625
SAFE = 150                                    # 0.5 in inside each trim edge
NIGHT = (38, 34, 86)
NIGHT2 = (58, 52, 118)
TITLE = (255, 222, 120)
CREAM = (255, 249, 236)
SOFT = (226, 220, 245)

# KDP prints the barcode (when "Amazon adds the barcode" is selected) on the BACK cover, bottom
# corner next to the spine: 2 x 1.2 in, 0.25 in from the spine fold and from the bottom trim
# (KDP Barcodes help page; confirmed in the KDP previewer for this book, 18 Oct 2026).
# The cover must be solid white there. BARCODE_PAD of white goes round it so small print shifts
# never put the barcode on artwork. Never place the zone from SAFE: that put it 0.5 in in and
# KDP's barcode landed half on the purple background (Book 1, first upload).
BARCODE_W, BARCODE_H, BARCODE_GAP, BARCODE_PAD = 600, 360, 75, 45   # px at 300 DPI

def barcode_area():
    """(x0, y0, x1, y1) of KDP's printed barcode on the wrap, in px."""
    spine_x, bottom_y = BLEED + TRIM, BLEED + TRIM          # back trim's spine edge and bottom edge
    return (spine_x - BARCODE_GAP - BARCODE_W, bottom_y - BARCODE_GAP - BARCODE_H,
            spine_x - BARCODE_GAP, bottom_y - BARCODE_GAP)

def check_barcode(wrap):
    """Fail the build unless KDP's barcode area (plus 0.1 in) is pure white."""
    x0, y0, x1, y1 = barcode_area()
    m = 30
    region = wrap.crop((x0 - m, y0 - m, x1 + m, y1 + m)).convert("L")
    lo = region.getextrema()[0]
    if lo < 250:
        raise SystemExit(f"BARCODE CHECK FAILED: KDP's barcode area {x0 - m},{y0 - m}-{x1 + m},{y1 + m} "
                         f"is not solid white (darkest value {lo}). Move artwork or text out of it.")
    print("barcode check: KDP area is solid white")

def font(name, px, weight=None):
    f = ImageFont.truetype(os.path.join(FONTS, name), px)
    if weight:
        f.set_variation_by_name(weight)
    return f

def save(img, path):
    for a in range(4):
        try:
            img.save(path, dpi=(300, 300)); return
        except OSError:
            time.sleep(2 * (a + 1))
    raise OSError(path)

def wrap_lines(d, text, fnt, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) > maxw and cur:
            lines.append(cur); cur = w
        else:
            cur = t
    return lines + [cur]

def build():
    # back + spine: twilight gradient so the back matches the front's sky
    grad = Image.linear_gradient("L").resize((CW, CH))
    wrap = Image.composite(Image.new("RGB", (CW, CH), NIGHT2), Image.new("RGB", (CW, CH), NIGHT), grad)

    # FRONT (right): option C at true size; its own bleed covers the right/top/bottom edges
    front = Image.open(os.path.join(HERE, "cover_option_C.png")).convert("RGB")
    fx = BLEED + TRIM + SPINE
    wrap.paste(front, (fx, 0))

    d = ImageDraw.Draw(wrap)
    bx0 = BLEED                                # back trim box x origin
    cx = bx0 + TRIM // 2
    maxw = TRIM - 2 * SAFE - 40

    # back title, auto-shrunk to the safe width
    t, size = "Somebody is peeling Banjo's tree!".replace("'", "’"), 130
    f_t = font("Chewy-Regular.ttf", size)
    while d.textlength(t, font=f_t) > maxw:
        size -= 4
        f_t = font("Chewy-Regular.ttf", size)
    d.text((cx, BLEED + SAFE + 110), t, font=f_t, fill=TITLE, anchor="ms")

    # blurb
    blurb = ("Banjo the sugar glider loves his big, smooth gum tree. So when long strips of bark "
             "start curling off it, he knows just what to do: find the tree peeler! Was it "
             "Cockatoo? Possum? Echidna? Wombat? Olive the koala knows the answer, if only she "
             "could stay awake. A funny bedtime mystery about change, growing up and the wonders "
             "of the Australian bush.").replace("'", "’")
    f_b = font("Nunito[wght].ttf", 58, "Bold")
    y = BLEED + SAFE + 230
    for line in wrap_lines(d, blurb, f_b, maxw):
        d.text((cx, y), line, font=f_b, fill=CREAM, anchor="ms")
        y += 80

    # three sample pages as square cards (from the typeset interior, trimmed)
    cards = ["p11", "p14", "p27"]
    cw_ = 600
    gap = (TRIM - 2 * SAFE - 3 * cw_) // 2
    cy = y + 30
    for i, pid in enumerate(cards):
        n = int(pid[1:])
        im = Image.open(os.path.join(HERE, "typeset", pid + ".png")).convert("RGB")
        ox = 0 if n % 2 else BLEED
        im = im.crop((ox, BLEED, ox + TRIM, BLEED + TRIM)).resize((cw_, cw_), Image.LANCZOS)
        x = bx0 + SAFE + i * (cw_ + gap)
        shadow = Image.new("RGBA", wrap.size, (0, 0, 0, 0))
        ImageDraw.Draw(shadow).rounded_rectangle((x + 10, cy + 14, x + cw_ + 10, cy + cw_ + 14),
                                                 radius=34, fill=(10, 8, 30, 150))
        shadow = shadow.filter(ImageFilter.GaussianBlur(14))
        wrap.paste(shadow, (0, 0), shadow)
        mask = Image.new("L", (cw_, cw_), 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, cw_ - 1, cw_ - 1), radius=34, fill=255)
        wrap.paste(im, (x, cy), mask)
        d = ImageDraw.Draw(wrap)
        d.rounded_rectangle((x, cy, x + cw_, cy + cw_), radius=34, outline=CREAM, width=8)
    y = cy + cw_ + 110

    # bullets
    f_h = font("Nunito[wght].ttf", 54, "ExtraBold")
    for b in ["•  A funny read-aloud mystery with a twist at the end",
              "•  Real Australian animals, plus true bush facts at the back",
              "•  A gentle story about change and growing up"]:
        d.text((bx0 + SAFE + 20, y), b, font=f_h, fill=CREAM, anchor="ls")
        y += 78

    # bio box (in-book bio, locked in publishing\00-brand-identity.md)
    bio_top = BLEED + TRIM - SAFE - 330
    box = (bx0 + SAFE, bio_top, bx0 + SAFE + 1450, BLEED + TRIM - SAFE)
    d.rounded_rectangle(box, radius=34, fill=(255, 255, 255), outline=(60, 54, 110), width=5)
    d.text((box[0] + 50, bio_top + 85), "ABOUT HATTIE MOSS", font=font("Chewy-Regular.ttf", 64),
           fill=NIGHT, anchor="ls")
    f_bio = font("Nunito[wght].ttf", 42, "SemiBold")
    by = bio_top + 155
    for line in wrap_lines(d, "Hattie Moss writes funny picture books about Australian animals. "
                           "She thinks gum trees are the best trees and sugar gliders are the "
                           "best gliders.", f_bio, 1450 - 100):
        d.text((box[0] + 50, by), line, font=f_bio, fill=(70, 66, 100), anchor="ls")
        by += 58

    # KDP barcode zone, where KDP actually prints it (checked in the KDP previewer, 18 Oct 2026):
    # 2 x 1.2 in, 0.25 in from the spine fold and from the bottom trim. The white box covers that
    # area plus 0.15 in all round, so the barcode always lands on solid white. (It was 0.5 in in
    # from the edges before, and KDP's barcode sat half on the purple.)
    bar = barcode_area()
    bc = (bar[0] - BARCODE_PAD, bar[1] - BARCODE_PAD, bar[2] + BARCODE_PAD, bar[3] + BARCODE_PAD)
    d.rectangle(bc, fill=(255, 255, 255))

    # imprint line under the bio box would leave the safe zone; put it above the barcode instead
    d.text(((bc[0] + bc[2]) // 2, bc[1] - 40), "SALTBUSH STORY HOUSE", font=font("Nunito[wght].ttf", 40, "Bold"),
           fill=SOFT, anchor="ms")

    # spine: plain, matched to the front's left edge colour
    edge = front.crop((0, 0, 4, CH)).resize((1, 1)).getpixel((0, 0))
    d.rectangle((BLEED + TRIM, 0, BLEED + TRIM + SPINE, CH), fill=edge)
    return wrap

if __name__ == "__main__":
    wrap = build()
    check_barcode(wrap)
    out_dir = os.path.join(HERE, "kdp_package")
    up_dir = os.path.join(HERE, "KDP_FINAL_UPLOAD")
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(up_dir, exist_ok=True)
    png_path = os.path.join(out_dir, "WHO_PEELED_MY_TREE_COVER_WRAP.png")
    pdf_path = os.path.join(out_dir, "WHO_PEELED_MY_TREE_COVER_WRAP.pdf")
    save(wrap, png_path)
    wrap.save(pdf_path, resolution=300.0, quality=100, subsampling=0)
    prev = wrap.resize((1800, int(1800 * CH / CW)), Image.LANCZOS)
    save(prev, os.path.join(HERE, "cover_wrap_preview.png"))
    shutil.copyfile(pdf_path, os.path.join(up_dir, "02_COVER_WRAP_PRINT_READY.pdf"))
    shutil.copyfile(os.path.join(HERE, "cover_wrap_preview.png"), os.path.join(up_dir, "COVER_PREVIEW.png"))
    print(f"wrap {CW} x {CH} px = {CW / 300:.3f} x {CH / 300:.3f} in; PDF {os.path.getsize(pdf_path) / 1e6:.1f} MB")
