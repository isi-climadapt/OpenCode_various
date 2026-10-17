# -*- coding: utf-8 -*-
# Author 2 Book 3: Full cover wrap builder: Robot Wonders (KDP paperback specs).
# 108-page B&W white-paper spine: 108 * 0.002252 = 0.2432in -> 73px @300dpi
# Total: 0.125 bleed + 8.5 back + 0.2432 spine + 8.5 front + 0.125 bleed = 17.4932in x 11.25in
# = 5248 x 3375 px @ 300 DPI. Usage: py create_cover_wrap_a2.py

import os, sys, time
from PIL import Image, ImageDraw, ImageFont
from PIL import JpegImagePlugin  # noqa: F401: registers JPEG handler needed by PDF save

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")
FONT_LILITA = os.path.join(FONTS, "LilitaOne-Regular.ttf")
FONT_FREDO = os.path.join(FONTS, "Fredoka.ttf")

CW, CH = 5248, 3375
BG = (255, 255, 255)
DARK = (30, 30, 35)
BLEED = 38
BLUE = (35, 90, 160)
YELLOW = (255, 200, 40)


def save(img, path):
    for a in range(4):
        try:
            img.save(path, dpi=(300, 300)); return
        except OSError:
            time.sleep(2 * (a + 1))
    raise OSError(path)


def build():
    wrap = Image.new("RGB", (CW, CH), BG)

    # FRONT (right side): typeset cover option C at true size inside the trim.
    # Stretching it into the bleed resampled the whole front unevenly (1.5% x 2.3%);
    # the front's bleed is filled with its own edge color instead.
    front = Image.open(os.path.join(HERE, "cover_option_C.png")).convert("RGB")
    fx = CW - BLEED - front.width
    ImageDraw.Draw(wrap).rectangle([fx, 0, CW, CH], fill=front.getpixel((2, 2)))
    wrap.paste(front, (fx, BLEED))

    d = ImageDraw.Draw(wrap)

    # SPINE (clean tone, no text: 73px too narrow for reliable print text)
    sx1 = BLEED + 2550
    sx2 = sx1 + 73
    d.rectangle([sx1, 0, sx2, CH], fill=(240, 235, 225))
    d.line([(sx1, 0), (sx1, CH)], fill=(200, 195, 190), width=3)
    d.line([(sx2, 0), (sx2, CH)], fill=(200, 195, 190), width=3)

    # BACK cover (left side): auto-shrink title into safe zone (max 2230px, rule F10)
    bk_t = "MEET THE ROBOTS!"
    size = 130
    f_bktitle = ImageFont.truetype(FONT_LILITA, size)
    bb = d.textbbox((0, 0), bk_t, font=f_bktitle)
    while bb[2] - bb[0] > 2230 and size > 60:
        size -= 5
        f_bktitle = ImageFont.truetype(FONT_LILITA, size)
        bb = d.textbbox((0, 0), bk_t, font=f_bktitle)
    d.text((BLEED + (2550 - (bb[2] - bb[0])) // 2 - bb[0], 240), bk_t, fill=BLUE, font=f_bktitle)

    f_blurb = ImageFont.truetype(FONT_FREDO, 62)
    blurb_lines = [
        "Power up! Meet a Mars rover, a stair-climbing robot",
        "dog, a backflipping robot and Aussie stars like the",
        "driverless mine trucks and the robot that protects the",
        "Great Barrier Reef. 50 big, bold, easy designs for young",
        "inventors, with a real fact on every single page.",
    ]
    y_b = 480
    for line in blurb_lines:
        bb = d.textbbox((0, 0), line, font=f_blurb)
        d.text((BLEED + (2550 - (bb[2] - bb[0])) // 2 - bb[0], y_b), line, fill=(60, 65, 75), font=f_blurb)
        y_b += 82

    # 4 sample interior previews (crisp binarized thumbs)
    sys.path.append(os.path.join(os.path.dirname(HERE), "scripts"))
    from thumb import art_thumb
    samples = ["page_01", "page_08", "page_20", "page_34"]  # Mars rover, robot dog, humanoid, drone
    thumb_w = thumb_h = 520  # square art cards, no captions: Amazon's back image is ~1000 px wide
    thumb_y = 990
    for idx, s_key in enumerate(samples):
        s_path = os.path.join(HERE, "raw2", "%s.png" % s_key)  # 1K line art
        if os.path.exists(s_path):
            thumb = art_thumb(s_path, thumb_w - 40)
            tx = BLEED + 160 + idx * (thumb_w + 50)
            d.rounded_rectangle([tx - 10, thumb_y - 10, tx + thumb_w + 10, thumb_y + thumb_h + 10],
                                radius=30, fill=(255, 255, 255), outline=(30, 30, 35), width=8)
            wrap.paste(thumb.convert("RGB"), (tx + (thumb_w - thumb.width) // 2, thumb_y + (thumb_h - thumb.height) // 2))

    bullets = [
        ("•  50 BIG & BOLD DESIGNS", "Extra-thick lines, easy for crayons, markers, & little hands"),
        ("•  FUN FACTS ON EVERY PAGE", "Real robot secrets, from Mars helicopters to robot penguins!"),
        ("•  SINGLE-SIDED PAGES", "No bleed-through! Great for cutting out and displaying artwork"),
        ("•  LEARN & COLOR", "Real robots and friendly helpers for curious kids 3-8"),
    ]
    f_bhead = ImageFont.truetype(FONT_FREDO, 58)
    f_bdesc = ImageFont.truetype(FONT_FREDO, 50)
    y_bull = 1800
    for head, desc in bullets:
        d.text((BLEED + 220, y_bull), head, fill=(30, 30, 35), font=f_bhead)
        d.text((BLEED + 220, y_bull + 65), desc, fill=(95, 100, 110), font=f_bdesc)
        y_bull += 160

    # Bio box (locked author bio: Wattle Wonders voice)
    d.rounded_rectangle([BLEED + 160, 2540, BLEED + 1660, 3020], radius=35, fill=(255, 255, 255), outline=(40, 45, 55), width=6)
    f_bio_title = ImageFont.truetype(FONT_LILITA, 56)
    d.text((BLEED + 220, 2585), "ABOUT FLORA WATT", fill=BLUE, font=f_bio_title)
    f_bio = ImageFont.truetype(FONT_FREDO, 42)
    bio_lines = [
        "Flora Watt is an Australian author and illustrator who believes",
        "learning and coloring belong together. Her books turn big,",
        "exciting topics into friendly, bold designs that young artists",
        "can finish and feel proud of. Made with love in Australia.",
    ]
    yb = 2680
    for line in bio_lines:
        d.text((BLEED + 220, yb), line, fill=(70, 75, 85), font=f_bio)
        yb += 64

    # KDP barcode zone (bottom-right of back cover)
    bc_x = BLEED + 2550 - 680 - 60
    bc_y = CH - 38 - 420 - 60
    d.rounded_rectangle([bc_x, bc_y, bc_x + 680, bc_y + 420], radius=20, fill=(255, 255, 255), outline=(210, 205, 200), width=3)
    f_bc = ImageFont.truetype(FONT_FREDO, 38)
    d.text((bc_x + 130, bc_y + 180), "[ KDP BARCODE AREA ]", fill=(180, 175, 170), font=f_bc)

    f_bimp = ImageFont.truetype(FONT_FREDO, 46)
    d.text((BLEED + 220, 3160), "WATTLE WONDERS PUBLISHING  •  MELBOURNE, AUSTRALIA", fill=(140, 135, 130), font=f_bimp)

    return wrap


if __name__ == "__main__":
    wrap = build()
    out_dir = os.path.join(HERE, "kdp_package")
    up_dir = os.path.join(HERE, "KDP_FINAL_UPLOAD")
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(up_dir, exist_ok=True)
    png_path = os.path.join(out_dir, "ROBOT_WONDERS_COVER_WRAP.png")
    pdf_path = os.path.join(out_dir, "ROBOT_WONDERS_COVER_WRAP.pdf")
    save(wrap, png_path)
    # Pillow's default here is quality-75 JPEG; 100 with no chroma subsampling keeps outlines clean
    wrap.save(pdf_path, resolution=300.0, quality=100, subsampling=0)
    prev = wrap.resize((1500, int(1500 * wrap.height / wrap.width)), Image.LANCZOS)
    save(prev, os.path.join(HERE, "cover_wrap_preview.png"))
    import shutil
    shutil.copyfile(pdf_path, os.path.join(up_dir, "02_COVER_WRAP_PRINT_READY.pdf"))
    shutil.copyfile(os.path.join(HERE, "cover_wrap_preview.png"), os.path.join(up_dir, "COVER_PREVIEW.png"))
    print("wrap PDF: %.2f MB" % (os.path.getsize(pdf_path) / (1024 * 1024)))
    print("done")
