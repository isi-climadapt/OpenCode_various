# -*- coding: utf-8 -*-
# Book 6: Yummy Cuties full cover wrap builder (KDP paperback specs, locked formula).
# Copied from book5/create_cover_wrap5.py (rule 15); back panel settings changed only.
# 108-page B&W white-paper spine: 108 * 0.002252 = 0.2432in -> 73px @300dpi
# Total: 5248 x 3375 px @ 300 DPI. Usage: py create_cover_wrap6.py

import os, sys, time
from PIL import Image, ImageDraw, ImageFont
from PIL import JpegImagePlugin  # noqa: F401, registers JPEG handler needed by PDF save

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")
FONT_SNIGLET = os.path.join(FONTS, "Sniglet-ExtraBold.ttf")
FONT_BALOO = os.path.join(FONTS, "Baloo2.ttf")

CW, CH = 5248, 3375
BG = (246, 237, 225)
DARK = (35, 25, 20)
BLEED = 38

def save(img, path):
    for a in range(4):
        try:
            img.save(path, dpi=(300, 300)); return
        except OSError:
            time.sleep(2 * (a + 1))
    raise OSError(path)

def build():
    wrap = Image.new("RGB", (CW, CH), BG)

    # FRONT (right side): typeset cover_option_B at true size inside the trim.
    # Stretching it into the bleed resampled the whole front unevenly (1.5% x 2.3%);
    # the bleed takes the wrap background, which matches the front's cream.
    front = Image.open(os.path.join(HERE, "cover_option_B.png")).convert("RGB")
    wrap.paste(front, (CW - BLEED - front.width, BLEED))

    d = ImageDraw.Draw(wrap)

    # SPINE (clean tone, no text: 73px too narrow for reliable print text)
    sx1 = BLEED + 2550
    sx2 = sx1 + 73
    d.rectangle([sx1, 0, sx2, CH], fill=(240, 228, 214))
    d.line([(sx1, 0), (sx1, CH)], fill=(210, 195, 180), width=3)
    d.line([(sx2, 0), (sx2, CH)], fill=(210, 195, 180), width=3)

    # BACK cover (left side): built to read in Amazon's 600 x 776 back image (F13),
    # barcode zone where KDP prints it (F12)
    sys.path.append(os.path.join(os.path.dirname(HERE), "scripts"))
    from back600 import draw_back
    smallest = draw_back(
        wrap,
        title="COLOR THE YUMMY CUTIES!",
        # close-up crops (path, zoom, centre x, centre y) where the character sits off-centre
        cards=[
            (os.path.join(HERE, "raw2", "page_02.png"), 0.72, 0.45, 0.42),
            (os.path.join(HERE, "raw2", "page_05.png"), 0.72, 0.5, 0.45),
            (os.path.join(HERE, "raw2", "page_25.png"), 0.72, 0.55, 0.4),
            (os.path.join(HERE, "raw2", "page_38.png"), 0.72, 0.45, 0.45),
        ],
        bullets=["50 big & bold designs", "A fun fact on every page", "Single-sided pages"],
        footer=["Made with love in Australia", "GUMLEAF KIDS PRESS"],
        fonts=dict(title=FONT_SNIGLET, body=FONT_BALOO),
        colors=dict(ink=DARK, title=(45, 30, 20), card=(40, 25, 15), accent=(176, 42, 92), footer=(70, 55, 45)),
    )
    print("back cover: smallest text %d px (%.0f px in Amazon's 600 px image)" % (smallest, smallest * 600 / 2550))

    return wrap

if __name__ == "__main__":
    wrap = build()
    out_dir = os.path.join(HERE, "kdp_package")
    up_dir = os.path.join(HERE, "KDP_FINAL_UPLOAD")
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(up_dir, exist_ok=True)
    png_path = os.path.join(out_dir, "YUMMY_CUTIES_COVER_WRAP.png")
    pdf_path = os.path.join(out_dir, "YUMMY_CUTIES_COVER_WRAP.pdf")
    save(wrap, png_path)
    # Pillow's default here is quality-75 JPEG; 100 with no chroma subsampling keeps outlines clean
    wrap.save(pdf_path, resolution=300.0, quality=100, subsampling=0)
    prev = wrap.resize((1500, int(1500 * wrap.height / wrap.width)), Image.LANCZOS)
    save(prev, os.path.join(HERE, "cover_wrap_preview.png"))
    from back600 import save_back_preview
    save_back_preview(wrap, os.path.join(HERE, "back_cover_600px_preview.png"))
    import shutil
    shutil.copyfile(pdf_path, os.path.join(up_dir, "02_COVER_WRAP_PRINT_READY.pdf"))
    shutil.copyfile(os.path.join(HERE, "cover_wrap_preview.png"), os.path.join(up_dir, "COVER_PREVIEW.png"))
    print("wrap PDF: %.2f MB" % (os.path.getsize(pdf_path) / (1024 * 1024)))
    print("done")

