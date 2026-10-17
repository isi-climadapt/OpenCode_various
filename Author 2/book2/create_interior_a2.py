# -*- coding: utf-8 -*-
# Author 2 Book 2: KDP Interior Packager: Minibeast Wonders (Wattle Wonders Publishing)
# 108 pages @ 300 DPI, 8.5x11in B&W, no-bleed, margins >= 0.53in.
# House look: Lilita One titles (solid poster caps), Fredoka prose/captions,
# uniform caption rule (fixed 80px, max 2 lines), bigger art box 2230x2520.
# Usage: py create_interior_a2.py

import os, sys, json, time, shutil
from PIL import Image, ImageDraw, ImageFont, ImageOps
from PIL import JpegImagePlugin  # noqa: F401 — registers JPEG handler needed by PDF save

ROOT = os.path.dirname(os.path.abspath(__file__))
FONTS_DIR = os.path.join(ROOT, "fonts")
RAW2_DIR = os.path.join(ROOT, "raw2")
CAPTIONS_FILE = os.path.join(ROOT, "captions.json")
OUTPUT_DIR = os.path.join(ROOT, "kdp_package")
FINAL_UPLOAD_DIR = os.path.join(ROOT, "KDP_FINAL_UPLOAD")
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(FINAL_UPLOAD_DIR, exist_ok=True)

FONT_LILITA = os.path.join(FONTS_DIR, "LilitaOne-Regular.ttf")
FONT_FREDO = os.path.join(FONTS_DIR, "Fredoka.ttf")
FONT_SNIGLET = os.path.join(FONTS_DIR, "Sniglet-ExtraBold.ttf")
FONT_PACIFICO = os.path.join(FONTS_DIR, "Pacifico-Regular.ttf")

W, H = 2550, 3300

TITLE = "Minibeast Wonders"

HERO_CROP = os.path.join(ROOT, "ladybird_cropped.png")
HERO_BOX = (360, 380, 700, 650)  # ladybird body + leaf in raw2/page_01.png (1024 px); outlines touching it are kept whole

with open(CAPTIONS_FILE, encoding="utf-8") as f:
    CAPTIONS = json.load(f)


def save_png(img, path):
    for attempt in range(4):  # F8 OneDrive lock retry
        try:
            img.save(path, dpi=(300, 300))
            return
        except OSError:
            time.sleep(2 * (attempt + 1))
    raise OSError("could not save %s" % path)


def make_hero_crop():
    """Crop the ladybird from raw2/page_01.png as the interior hero icon (cached)."""
    if os.path.exists(HERO_CROP) and os.path.getsize(HERO_CROP) > 10000:
        return
    src = Image.open(os.path.join(RAW2_DIR, "page_01.png")).convert("L")
    src = ImageOps.autocontrast(src, cutoff=1)
    import numpy as np
    from scipy import ndimage
    # Keep only the ladybird and its leaf, found on the whole page so nothing is cut
    # off: the ink outlines touching the box centre, plus everything they enclose
    # (spots, face, the little bugs on the leaf). Neighbouring leaves and grass drop out.
    ink = np.asarray(src) < 120
    lab, _ = ndimage.label(ink, structure=np.ones((3, 3)))
    x0, y0, x1, y1 = HERO_BOX
    centre = lab[y0:y1, x0:x1]
    ids = [i for i in np.unique(centre) if i and (centre == i).sum() > 2000]
    shape = ndimage.binary_fill_holes(np.isin(lab, ids))
    crop = Image.fromarray(np.where(shape & ink, 0, 255).astype("uint8"), "L")
    bb = ImageOps.invert(crop).getbbox()
    crop = crop.crop(bb) if bb else crop
    save_png(crop, HERO_CROP)


def draw_star(draw, x, y, size, fill=(180, 160, 150)):
    pts = [
        (x, y - size), (x + size * 0.25, y - size * 0.25),
        (x + size, y), (x + size * 0.25, y + size * 0.25),
        (x, y + size), (x - size * 0.25, y + size * 0.25),
        (x - size, y), (x - size * 0.25, y - size * 0.25),
    ]
    draw.polygon(pts, fill=fill)


def make_blank_page():
    return Image.new("L", (W, H), 255)


def draw_uniform_caption(d, caption_text):
    """Hard rule 10: fixed 80px caption font (Fredoka), word-wrap max 2 lines."""
    size = 80
    font = ImageFont.truetype(FONT_FREDO, size)
    max_w = W - 300

    def wrap(fnt):
        out, line = [], ""
        for wd in caption_text.split(" "):
            test = (line + " " + wd).strip()
            if d.textbbox((0, 0), test, font=fnt)[2] > max_w and line:
                out.append(line)
                line = wd
            else:
                line = test
        if line:
            out.append(line)
        return out

    lines = wrap(font)
    while len(lines) > 2 and size > 55:
        size -= 5
        font = ImageFont.truetype(FONT_FREDO, size)
        lines = wrap(font)
    lines = lines[:2]
    if len(lines) == 1:
        bb = d.textbbox((0, 0), lines[0], font=font)
        d.text(((W - (bb[2] - bb[0])) // 2 - bb[0], 2880), lines[0], fill=0, font=font)
    else:
        for i, ln in enumerate(lines):
            bb = d.textbbox((0, 0), ln, font=font)
            d.text(((W - (bb[2] - bb[0])) // 2 - bb[0], 2840 + i * 92), ln, fill=0, font=font)


def make_title_page():
    page = Image.new("L", (W, H), 255)
    d = ImageDraw.Draw(page)

    d.rounded_rectangle((160, 160, W - 160, H - 160), radius=40, outline=0, width=20)
    d.rounded_rectangle((200, 200, W - 200, H - 200), radius=25, outline=0, width=6)

    f_kicker = ImageFont.truetype(FONT_FREDO, 75)
    kick = "LET'S EXPLORE!"
    bb = d.textbbox((0, 0), kick, font=f_kicker)
    d.text(((W - (bb[2] - bb[0])) // 2 - bb[0], 400), kick, fill=60, font=f_kicker)

    f_title = ImageFont.truetype(FONT_LILITA, 250)
    for text, y in [("MINIBEAST", 540), ("WONDERS", 800)]:
        bb = d.textbbox((0, 0), text, font=f_title)
        tw = bb[2] - bb[0]
        d.text(((W - tw) // 2 - bb[0], y), text, fill=0, font=f_title)

    f_tag = ImageFont.truetype(FONT_FREDO, 68)
    tag = "50 Big & Bold Designs with Fun Facts"
    bb = d.textbbox((0, 0), tag, font=f_tag)
    d.text(((W - (bb[2] - bb[0])) // 2 - bb[0], 1160), tag, fill=80, font=f_tag)

    icon = Image.open(HERO_CROP).convert("L")
    icon = icon.point(lambda p: 0 if p < 120 else 255)
    icon.thumbnail((1200, 1050), Image.LANCZOS)
    page.paste(icon, ((W - icon.width) // 2, 1360))

    f_by = ImageFont.truetype(FONT_FREDO, 55)
    d.text(((W - 140) // 2, 2620), "Created by", fill=100, font=f_by)
    f_auth = ImageFont.truetype(FONT_PACIFICO, 110)
    bb = d.textbbox((0, 0), "Flora Watt", font=f_auth)
    d.text(((W - (bb[2] - bb[0])) // 2 - bb[0], 2700), "Flora Watt", fill=0, font=f_auth)

    f_imp = ImageFont.truetype(FONT_FREDO, 50)
    bb = d.textbbox((0, 0), "WATTLE WONDERS PUBLISHING", font=f_imp)
    d.text(((W - (bb[2] - bb[0])) // 2 - bb[0], 2930), "WATTLE WONDERS PUBLISHING", fill=100, font=f_imp)

    return page


def make_copyright_page():
    page = Image.new("L", (W, H), 255)
    d = ImageDraw.Draw(page)
    f_reg = ImageFont.truetype(FONT_FREDO, 46)
    f_bold = ImageFont.truetype(FONT_FREDO, 54)

    lines = [
        (TITLE, f_bold),
        ("First Edition: November 2026", f_reg),
        ("", f_reg),
        ("Published by Wattle Wonders Publishing", f_bold),
        ("Melbourne, Australia", f_reg),
        ("", f_reg),
        ("Created by Flora Watt", f_bold),
        ("Copyright © 2026 Wattle Wonders Publishing", f_reg),
        ("All rights reserved.", f_reg),
        ("", f_reg),
        ("No part of this publication may be reproduced, distributed, or", f_reg),
        ("transmitted in any form or by any means, including photocopying,", f_reg),
        ("recording, or other electronic or mechanical methods, without", f_reg),
        ("the prior written permission of the publisher.", f_reg),
        ("", f_reg),
        ("Illustrations created with AI assistance and extensively edited and", f_reg),
        ("curated by human artists for maximum quality and child enjoyment.", f_reg),
        ("", f_reg),
        ("Designed and printed for young explorers everywhere.", f_reg),
        ("Made with love in Australia.", f_reg),
    ]

    y = 1200
    for text, font in lines:
        if text:
            d.text((300, y), text, fill=40, font=font)
        y += 65
    return page


def make_belongs_to_page():
    page = Image.new("L", (W, H), 255)
    d = ImageDraw.Draw(page)

    d.rounded_rectangle((160, 160, W - 160, H - 160), radius=40, outline=0, width=16)

    f_title = ImageFont.truetype(FONT_LILITA, 125)
    text = "THIS BOOK BELONGS TO:"
    bb = d.textbbox((0, 0), text, font=f_title)
    d.text(((W - (bb[2] - bb[0])) // 2 - bb[0], 650), text, fill=0, font=f_title)

    d.line([(350, 1000), (W - 350, 1000)], fill=0, width=10)
    d.line([(350, 1200), (W - 350, 1200)], fill=0, width=10)

    f_name = ImageFont.truetype(FONT_FREDO, 60)
    d.text(((W - 400) // 2, 1050), "ARTIST NAME", fill=140, font=f_name)

    icon = Image.open(HERO_CROP).convert("L")
    icon = icon.point(lambda p: 0 if p < 120 else 255)
    icon.thumbnail((1100, 850), Image.LANCZOS)
    page.paste(icon, ((W - icon.width) // 2, 1450))

    f_msg = ImageFont.truetype(FONT_FREDO, 65)
    msg = "Get ready to colour 50 minibeast wonders!"
    bb = d.textbbox((0, 0), msg, font=f_msg)
    d.text(((W - (bb[2] - bb[0])) // 2 - bb[0], 2800), msg, fill=50, font=f_msg)

    return page


def make_tips_page():
    page = Image.new("L", (W, H), 255)
    d = ImageDraw.Draw(page)

    d.rounded_rectangle((160, 160, W - 160, H - 160), radius=40, outline=0, width=16)
    d.rounded_rectangle((200, 200, W - 200, H - 200), radius=25, outline=0, width=5)

    f_title = ImageFont.truetype(FONT_LILITA, 135)
    t = "TOP COLOURING TIPS!"
    bb = d.textbbox((0, 0), t, font=f_title)
    d.text(((W - (bb[2] - bb[0])) // 2 - bb[0], 230), t, fill=0, font=f_title)

    tips = [
        ("1. Put a Blank Sheet Behind Your Page", "When using juicy markers, place a scrap sheet behind your drawing to keep the next page perfectly clean!"),
        ("2. Start Light, Then Go Dark", "Colour lighter shades first, then layer darker tones on top for amazing depth and pop."),
        ("3. Mix Your Art Tools", "Try combining crayons, coloured pencils, and markers together on the same minibeast for fun textures."),
        ("4. There Are No Mistakes In Art!", "Make your minibeasts any colour you want. Purple ladybirds and rainbow snails are awesome!"),
    ]
    f_head = ImageFont.truetype(FONT_FREDO, 60)
    f_desc = ImageFont.truetype(FONT_FREDO, 48)

    y = 430
    for head, desc in tips:
        d.text((220, y), head, fill=0, font=f_head)
        y += 72
        words = desc.split(" ")
        line = ""
        for w in words:
            test = line + (" " if line else "") + w
            bb = d.textbbox((0, 0), test, font=f_desc)
            if bb[2] - bb[0] > 2050:
                d.text((260, y), line, fill=60, font=f_desc)
                y += 62
                line = w
            else:
                line = test
        if line:
            d.text((260, y), line, fill=60, font=f_desc)
            y += 80
        y += 20

    d.line([(220, y + 10), (W - 220, y + 10)], fill=180, width=4)

    y_test = y + 60
    f_test_title = ImageFont.truetype(FONT_LILITA, 105)
    tt = "MY COLOUR TEST PALETTE"
    bb = d.textbbox((0, 0), tt, font=f_test_title)
    d.text(((W - (bb[2] - bb[0])) // 2 - bb[0], y_test), tt, fill=0, font=f_test_title)

    f_test_sub = ImageFont.truetype(FONT_FREDO, 48)
    tsub = "Test your pencils, markers, and crayons here before colouring your minibeasts!"
    bb = d.textbbox((0, 0), tsub, font=f_test_sub)
    d.text(((W - (bb[2] - bb[0])) // 2 - bb[0], y_test + 120), tsub, fill=90, font=f_test_sub)

    f_num = ImageFont.truetype(FONT_FREDO, 44)
    radius = 125
    y_circles = y_test + 360

    for i in range(5):
        cx = 360 + i * 455
        d.ellipse([cx - radius, y_circles - radius, cx + radius, y_circles + radius], outline=0, width=7)
        lbl = "Colour %d" % (i + 1)
        lbb = d.textbbox((0, 0), lbl, font=f_num)
        d.text((cx - (lbb[2] - lbb[0]) // 2 - lbb[0], y_circles + radius + 20), lbl, fill=100, font=f_num)

    d.line([(220, y_circles + radius + 110), (W - 220, y_circles + radius + 110)], fill=180, width=4)

    y_bottom = y_circles + radius + 160

    icon = Image.open(HERO_CROP).convert("L")
    icon = icon.point(lambda p: 0 if p < 120 else 255)
    icon.thumbnail((880, 660), Image.LANCZOS)
    page.paste(icon, (240, y_bottom + 60))

    box_x = 1180
    d.rounded_rectangle([box_x, y_bottom, W - 240, y_bottom + 820], radius=30, outline=0, width=6)

    f_pl_title = ImageFont.truetype(FONT_LILITA, 62)
    d.text((box_x + 60, y_bottom + 60), "MY EXPLORER PLEDGE:", fill=0, font=f_pl_title)

    f_pl_text = ImageFont.truetype(FONT_FREDO, 50)
    d.text((box_x + 60, y_bottom + 180), '"I promise to have fun,', fill=40, font=f_pl_text)
    d.text((box_x + 60, y_bottom + 250), 'make this book my own,', fill=40, font=f_pl_text)
    d.text((box_x + 60, y_bottom + 320), 'and be proud of every', fill=40, font=f_pl_text)
    d.text((box_x + 60, y_bottom + 390), 'drawing I colour!"', fill=40, font=f_pl_text)

    d.line([(box_x + 60, y_bottom + 600), (W - 300, y_bottom + 600)], fill=0, width=5)
    f_sig_lbl = ImageFont.truetype(FONT_FREDO, 44)
    d.text((box_x + 60, y_bottom + 625), "ARTIST SIGNATURE", fill=120, font=f_sig_lbl)

    f_pnum = ImageFont.truetype(FONT_FREDO, 55)
    d.text((W - 180, 3110), "4", fill=120, font=f_pnum)

    return page


def make_art_page(i):
    key = "page_%02d" % i
    raw2_path = os.path.join(RAW2_DIR, "%s.png" % key)
    caption_text = CAPTIONS.get(key, "")
    page_num = str(i * 2 + 3)

    # F11: vector-trace the native art -> crisp at 300 DPI (no upscale softness/halos)
    # BIGGER art box: 2230 x 2520 (0.53" side margins at 2230)
    sys.path.append(os.path.join(os.path.dirname(ROOT), "scripts"))
    from vectorize_line_art import vectorize_line_art
    # Trace at 2x and reduce with Lanczos: the anti-aliased edges survive to the
    # 600 DPI threshold in to_print_bw instead of 1/300 in stair-steps.
    img = vectorize_line_art(raw2_path, None, target_w=2230 * 2, target_h=2520 * 2)
    img = img.resize((img.width // 2, img.height // 2), Image.LANCZOS)

    page = Image.new("L", (W, H), 255)
    x_p = (W - img.width) // 2
    y_p = 170
    page.paste(img, (x_p, y_p))

    d = ImageDraw.Draw(page)
    draw_uniform_caption(d, caption_text)

    f_num = ImageFont.truetype(FONT_FREDO, 60)
    nb = d.textbbox((0, 0), page_num, font=f_num)
    d.text((W - 200 - (nb[2] - nb[0]), 3010), page_num, fill=120, font=f_num)

    return page


def make_checklist_page():
    page = Image.new("L", (W, H), 255)
    d = ImageDraw.Draw(page)

    d.rounded_rectangle((160, 160, W - 160, H - 160), radius=40, outline=0, width=14)

    f_title = ImageFont.truetype(FONT_LILITA, 100)
    text = "MY MINIBEAST WONDERS CHECKLIST"
    bb = d.textbbox((0, 0), text, font=f_title)
    d.text(((W - (bb[2] - bb[0])) // 2 - bb[0], 280), text, fill=0, font=f_title)

    f_sub = ImageFont.truetype(FONT_FREDO, 50)
    sub = "Tick each box as you finish colouring each minibeast!"
    bb = d.textbbox((0, 0), sub, font=f_sub)
    d.text(((W - (bb[2] - bb[0])) // 2 - bb[0], 410), sub, fill=90, font=f_sub)

    names = [
        "1. Ladybird lunch", "2. Ladybird spots", "3. Honeybee flowers", "4. Honeybee dance",
        "5. Queen bee", "6. Butterfly feet", "7. Caterpillar grows", "8. Chrysalis",
        "9. Ulysses butterfly", "10. Gum moth caterpillar", "11. Strong ant", "12. Ant nest",
        "13. Bull ant", "14. Dragonfly", "15. Firefly", "16. Glow-worms",
        "17. Christmas beetle", "18. Rainbow stag beetle", "19. Dung beetle", "20. Jewel beetle",
        "21. Weevil", "22. Grasshopper", "23. Cricket song", "24. Katydid",
        "25. Green grocer cicada", "26. Praying mantis", "27. Stick insect", "28. Snail house",
        "29. Snail trail", "30. Earthworm", "31. Giant earthworm", "32. Spider legs",
        "33. Spider silk", "34. Huntsman", "35. Peacock spider", "36. Blue-banded bee",
        "37. Stingless bee", "38. Leaf-cutter bee", "39. Moth", "40. Bogong moth",
        "41. Termite mound", "42. Centipede", "43. Millipede", "44. Slater",
        "45. Water strider", "46. Mud dauber wasp", "47. Burrowing cockroach", "48. Lacewing",
        "49. Six legs", "50. Garden party",
    ]

    f_item = ImageFont.truetype(FONT_FREDO, 46)
    y_start = 510
    for idx, name in enumerate(names):
        col = idx // 25
        row = idx % 25
        x = 260 if col == 0 else 1340
        y = y_start + row * 95
        d.rectangle([x, y + 6, x + 38, y + 44], outline=0, width=5)
        d.text((x + 60, y), name, fill=30, font=f_item)

    d.text((W - 220, 3010), "105", fill=120, font=ImageFont.truetype(FONT_FREDO, 60))
    return page


def make_certificate_page():
    page = Image.new("L", (W, H), 255)
    d = ImageDraw.Draw(page)

    d.rounded_rectangle((160, 160, W - 160, H - 160), radius=55, outline=0, width=22)
    d.rounded_rectangle((200, 200, W - 200, H - 200), radius=40, outline=0, width=8)

    f_top = ImageFont.truetype(FONT_FREDO, 70)
    t = "OFFICIAL CERTIFICATE"
    bb = d.textbbox((0, 0), t, font=f_top)
    d.text(((W - (bb[2] - bb[0])) // 2 - bb[0], 400), t, fill=60, font=f_top)

    f_award = ImageFont.truetype(FONT_LILITA, 155)
    award = "MINIBEAST ARTIST AWARD"
    bb = d.textbbox((0, 0), award, font=f_award)
    size = 155
    while bb[2] - bb[0] > 2050 and size > 80:  # shrink to fit (was an endless loop)
        size -= 5
        f_award = ImageFont.truetype(FONT_LILITA, size)
        bb = d.textbbox((0, 0), award, font=f_award)
    d.text(((W - (bb[2] - bb[0])) // 2 - bb[0], 550), award, fill=0, font=f_award)

    f_p = ImageFont.truetype(FONT_FREDO, 65)
    p1 = "This certifies that"
    bb = d.textbbox((0, 0), p1, font=f_p)
    d.text(((W - (bb[2] - bb[0])) // 2 - bb[0], 900), p1, fill=60, font=f_p)

    d.line([(400, 1250), (W - 400, 1250)], fill=0, width=8)
    f_lbl = ImageFont.truetype(FONT_FREDO, 50)
    d.text(((W - 350) // 2, 1280), "NAME OF ARTIST", fill=130, font=f_lbl)

    line1, line2 = "has successfully coloured all 50 minibeast", "wonders in this book!"
    for line, yy in ((line1, 1500), (line2, 1580)):
        bb2 = d.textbbox((0, 0), line, font=f_p)
        d.text(((W - (bb2[2] - bb2[0])) // 2 - bb2[0], yy), line, fill=40, font=f_p)

    draw_star(d, W // 2, 1950, 160, fill=0)
    draw_star(d, W // 2, 1950, 110, fill=255)
    f_star = ImageFont.truetype(FONT_LILITA, 60)
    stxt = u"\u2605 50 \u2605"
    d.text((W // 2 - 80, 1910), stxt, fill=0, font=f_star)

    d.line([(350, 2600), (950, 2600)], fill=0, width=6)
    d.line([(W - 950, 2600), (W - 350, 2600)], fill=0, width=6)

    f_sig = ImageFont.truetype(FONT_PACIFICO, 75)
    d.text((450, 2480), "Flora Watt", fill=0, font=f_sig)

    f_siglbl = ImageFont.truetype(FONT_FREDO, 50)
    d.text((540, 2630), "AUTHOR", fill=100, font=f_siglbl)
    d.text((W - 760, 2630), "DATE", fill=100, font=f_siglbl)

    d.text((W - 220, 3010), "107", fill=120, font=ImageFont.truetype(FONT_FREDO, 60))
    return page


def make_thank_you_page():
    page = Image.new("L", (W, H), 255)
    d = ImageDraw.Draw(page)

    d.rounded_rectangle((160, 160, W - 160, H - 160), radius=40, outline=0, width=14)

    f_title = ImageFont.truetype(FONT_LILITA, 125)
    t = "THANK YOU!"
    bb = d.textbbox((0, 0), t, font=f_title)
    d.text(((W - (bb[2] - bb[0])) // 2 - bb[0], 350), t, fill=0, font=f_title)

    f_msg = ImageFont.truetype(FONT_FREDO, 62)
    msg = [
        "Thank you for colouring with Wattle Wonders Publishing!",
        "We hope you loved your trip through the garden",
        "with Flora Watt.",
        "",
        "If you loved this book, please consider leaving a kind",
        "review on Amazon. It helps independent Australian",
        "bookmakers create more adventures for kids!",
        "",
        "IN THE WATTLE WONDERS SERIES:",
        u"\u2022 Space Wonders: Book 1",
        u"\u2022 Minibeast Wonders: Book 2",
        u"\u2022 Robot Wonders: Book 3",
    ]
    y = 650
    for line in msg:
        if line:
            bb = d.textbbox((0, 0), line, font=f_msg)
            d.text(((W - (bb[2] - bb[0])) // 2 - bb[0], y), line, fill=30 if not line.startswith(u"\u2022") else 0, font=f_msg)
        y += 95

    f_imp = ImageFont.truetype(FONT_FREDO, 56)
    imp = "WATTLE WONDERS PUBLISHING  •  MELBOURNE, AUSTRALIA"
    bb = d.textbbox((0, 0), imp, font=f_imp)
    d.text(((W - (bb[2] - bb[0])) // 2 - bb[0], 2850), imp, fill=100, font=f_imp)

    d.text((W - 220, 3010), "108", fill=120, font=ImageFont.truetype(FONT_FREDO, 60))
    return page


def to_print_bw(page, line_art):
    """2x Lanczos to 600 DPI, then 1-bit (same as Author 1). Line art is thresholded for
    clean edges. On text pages dark greys go solid black and only lighter greys (95+)
    are dithered, so they still print lighter."""
    big = page.resize((W * 2, H * 2), Image.LANCZOS)
    if line_art:
        return big.point(lambda p: 0 if p < 128 else 255).convert("1", dither=Image.Dither.NONE)
    return big.point(lambda p: 0 if p < 95 else (255 if p > 235 else p)).convert("1")


def main():
    make_hero_crop()
    print("=== STEP 1: GENERATING 108 INTERIOR PAGES ===")
    # (builder, is_line_art) in page order. Each page is built, converted to 600 DPI
    # 1-bit and written straight to disk: 108 pages at 600 DPI won't fit in memory.
    plan = [(make_title_page, False), (make_copyright_page, False),       # pages 1-4
            (make_belongs_to_page, False), (make_tips_page, False)]
    for i in range(1, 51):                                                  # pages 5-104
        plan += [(lambda i=i: make_art_page(i), True), (make_blank_page, True)]
    plan += [(make_checklist_page, False), (make_blank_page, True),         # pages 105-108
             (make_certificate_page, False), (make_thank_you_page, False)]
    assert len(plan) == 108, "Page count must be exactly 108!"

    interior_pdf_path = os.path.join(OUTPUT_DIR, "MINIBEAST_WONDERS_INTERIOR_108P.pdf")
    upload_interior_path = os.path.join(FINAL_UPLOAD_DIR, "01_MANUSCRIPT_INTERIOR_108P.pdf")
    print("Exporting Interior PDF (600 DPI 1-bit, lossless img2pdf) to:", interior_pdf_path)
    import img2pdf
    page_png_dir = os.path.join(OUTPUT_DIR, "pages_png")
    os.makedirs(page_png_dir, exist_ok=True)
    png_paths = []
    for idx, (builder, line_art) in enumerate(plan, start=1):
        pp = os.path.join(page_png_dir, "pp_%03d.png" % idx)
        bw = to_print_bw(builder(), line_art)
        for attempt in range(4):  # F8 OneDrive lock retry
            try:
                bw.save(pp, dpi=(600, 600)); break
            except OSError:
                time.sleep(2 * (attempt + 1))
        png_paths.append(pp)
        if idx % 20 == 0:
            print("  ...%d / 108 pages built" % idx)
    for attempt in range(4):
        try:
            with open(interior_pdf_path, "wb") as fh:
                fh.write(img2pdf.convert(png_paths))
            break
        except OSError:
            time.sleep(2 * (attempt + 1))
    shutil.rmtree(page_png_dir, ignore_errors=True)
    shutil.copyfile(interior_pdf_path, upload_interior_path)
    print("Interior PDF export complete! Size: %.2f MB" % (os.path.getsize(interior_pdf_path) / (1024 * 1024)))
    print("Upload copy at:", upload_interior_path)


if __name__ == "__main__":
    main()
