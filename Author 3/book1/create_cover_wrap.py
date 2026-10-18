# -*- coding: utf-8 -*-
# Author 3 Book 1 - Who Peeled My Tree? full cover wrap (KDP paperback, premium color, 8.5 x 8.5).
# Based on the latest wrap builder, Author 1\book4\create_cover_wrap4.py (commit 90f22ed):
# front pasted at true size inside its trim, plain spine, twilight back. The back is built with
# ..\scripts\back600.py (pipeline F13, ported 18 Oct 2026 as in book2): Amazon stores the back
# image at only 600 px wide, so the old blurb, sample cards and 42 px bio blurred. Now: one-line
# title, four close-up color art cards, three short bullets, two footer lines, every word 80 px or
# more, KDP barcode zone and check (F12). JPEG quality 100 with no chroma subsampling in the PDF.
# Spine: 32 pages x 0.002347 in (premium color, KDP Paperback Submission Guidelines) = 0.0751 in
# = 22.5 px -> 23 px. No spine text (KDP allows spine text from 79 pages).
# Wrap: 0.125 + 8.5 + 0.0751 + 8.5 + 0.125 = 17.325 in x 8.75 in -> 5198 x 2625 px at 300 DPI.
# Usage: py create_cover_wrap.py

import os, shutil, sys, time
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from PIL import JpegImagePlugin  # noqa: F401, registers JPEG handler needed by PDF save

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
from back600 import draw_back, check_barcode, save_back_preview  # noqa: E402
FONTS = os.path.join(HERE, "fonts")
TRIM, BLEED, SPINE = 2550, 38, 22   # 22.5 px exact; 22 keeps the wrap at 5198 px = 17.327 in vs 17.325
CW, CH = BLEED + TRIM + SPINE + TRIM + BLEED, 2625
SAFE = 150                                    # 0.5 in inside each trim edge
NIGHT = (38, 34, 86)
NIGHT2 = (58, 52, 118)
TITLE = (255, 222, 120)
CREAM = (255, 249, 236)
SOFT = (226, 220, 245)

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

    # BACK (left): built to read at Amazon's 600 px back image (F13)
    P = lambda pid: os.path.join(HERE, "pages", pid + ".png")
    smallest = draw_back(
        wrap,
        title="Somebody is peeling Banjo's tree!".replace("'", "’"),
        cards=[(P("p06"), 0.62, 0.58, 0.48),    # Banjo nose to nose with the peeling bark
               (P("p11"), 0.70, 0.50, 0.58),    # the cross cockatoo
               (P("p14"), 0.66, 0.52, 0.60),    # Possum's soft bed
               (P("p18"), 0.70, 0.50, 0.62)],   # Wombat and upside-down Banjo
        bullets=["A funny read-aloud mystery",
                 "Real Australian bush animals",
                 "True bush facts at the back"],
        footer=["Banjo and Olive, Book 1",
                "Saltbush Story House"],
        fonts=dict(title=os.path.join(FONTS, "Chewy-Regular.ttf"),
                   body=os.path.join(FONTS, "Nunito[wght].ttf")),
        colors=dict(ink=CREAM, title=TITLE, card=CREAM, accent=TITLE, footer=SOFT))
    print(f"back: smallest text {smallest} px (about {smallest * 600 / 2550:.0f} px at Amazon's 600 px)")
    d = ImageDraw.Draw(wrap)

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
    save_back_preview(wrap, os.path.join(HERE, "back_cover_600px_preview.png"))
    print(f"wrap {CW} x {CH} px = {CW / 300:.3f} x {CH / 300:.3f} in; PDF {os.path.getsize(pdf_path) / 1e6:.1f} MB")
