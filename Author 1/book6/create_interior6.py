# -*- coding: utf-8 -*-
# Book 6: KDP Interior Packager, Yummy Cuties (US spelling in all printed text)
# Copied from book5/create_interior5.py (rule 15); only book text and hero changed.
# 108 pages, 8.5x11in, 600 DPI 1-bit lossless, no-bleed, margins >= 0.53in.
# Engine = book2/create_interior.py with:
#   - BIGGER art box 2230x2520 (style upgrade per author)
#   - UNIFORM caption rule: fixed 80px font, word-wrap max 2 lines (hard rule 10)
#   - Sweet treats front/back matter; tracer = local vectorize_line_art.py (4x pre-trace, Author 2 fix)
# Usage: py create_interior5.py

import os, sys, json, time, shutil
from PIL import Image, ImageDraw, ImageFont, ImageOps
from PIL import JpegImagePlugin  # noqa: F401, registers JPEG handler needed by PDF save

ROOT = os.path.dirname(os.path.abspath(__file__))
FONTS_DIR = os.path.join(ROOT, "fonts")
RAW2_DIR = os.path.join(ROOT, "raw2")
CAPTIONS_FILE = os.path.join(ROOT, "captions.json")
OUTPUT_DIR = os.path.join(ROOT, "kdp_package")
FINAL_UPLOAD_DIR = os.path.join(ROOT, "KDP_FINAL_UPLOAD")
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(FINAL_UPLOAD_DIR, exist_ok=True)

FONT_SNIGLET = os.path.join(FONTS_DIR, "Sniglet-ExtraBold.ttf")
FONT_BALOO = os.path.join(FONTS_DIR, "Baloo2.ttf")
FONT_PACIFICO = os.path.join(FONTS_DIR, "Pacifico-Regular.ttf")

W, H = 2550, 3300

TITLE = "Yummy Cuties"
SUBTITLE_LONG = "A cute and cozy coloring book of sweet treats and tasty snacks for kids ages 4-8"

HERO_CROP = os.path.join(ROOT, "hero_cropped.png")
HERO_SRC, HERO_BOX = "page_29", (60, 80, 965, 920)  # puppy and kitten sharing cookies on the picnic blanket

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
    """Crop the hero friends from raw2/HERO_SRC as the interior hero icon (cached)."""
    if os.path.exists(HERO_CROP) and os.path.getsize(HERO_CROP) > 10000:
        return
    src = Image.open(os.path.join(RAW2_DIR, HERO_SRC + ".png")).convert("L")
    src = ImageOps.autocontrast(src, cutoff=1)
    crop = src.crop(HERO_BOX)
    # vector-trace at 2x (F11) so the icon prints as crisply as the art pages
    tmp = HERO_CROP + ".src.png"
    crop.save(tmp)
    sys.path.insert(0, ROOT)
    from vectorize_line_art import vectorize_line_art
    crop = vectorize_line_art(tmp, None, target_w=crop.width * 2, target_h=crop.height * 2)
    os.remove(tmp)
    save_png(crop, HERO_CROP)


def draw_star(draw, x, y, size, fill=(180, 160, 150)):
    pts = [
        (x, y - size), (x + size * 0.25, y - size * 0.25),
        (x + size, y), (x + size * 0.25, y + size * 0.25),
        (x, y + size), (x - size * 0.25, y + size * 0.25),
        (x - size, y), (x - size * 0.25, y - size * 0.25),
    ]
    draw.polygon(pts, fill=fill)


def framed_page_number(d, number):
    """Page number for pages with a rounded frame: right edge at x 2310 and baseline
    above y 3100, inside the inner frame line (x 2390 / y 3140) instead of on it."""
    f = ImageFont.truetype(FONT_BALOO, 60)
    bb = d.textbbox((0, 0), number, font=f)
    d.text((2310 - bb[2], 3020), number, fill=120, font=f)


def make_blank_page():
    return Image.new("L", (W, H), 255)


def draw_uniform_caption(d, caption_text):
    """Hard rule 10: fixed 80px caption font, word-wrap max 2 lines."""
    size = 80
    font = ImageFont.truetype(FONT_BALOO, size)
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
        font = ImageFont.truetype(FONT_BALOO, size)
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

    d.rounded_rectangle((160, 160, W - 160, H - 160), radius=60, outline=0, width=12)
    d.rounded_rectangle((185, 185, W - 185, H - 185), radius=45, outline=0, width=4)

    f_kicker = ImageFont.truetype(FONT_BALOO, 72)
    kick = "MUNCH! CRUNCH! YUM!"
    bb = d.textbbox((0, 0), kick, font=f_kicker)
    d.text(((W - (bb[2] - bb[0])) // 2 - bb[0], 380), kick, fill=80, font=f_kicker)

    f_title = ImageFont.truetype(FONT_SNIGLET, 225)
    for text, y in [("YUMMY", 520), ("CUTIES", 770)]:
        bb = d.textbbox((0, 0), text, font=f_title, stroke_width=16)
        tw = bb[2] - bb[0]
        d.text(((W - tw) // 2 - bb[0], y), text, fill=255, stroke_width=16, stroke_fill=0, font=f_title)

    f_banner = ImageFont.truetype(FONT_SNIGLET, 125)
    ban = "SWEET TREATS"
    bb = d.textbbox((0, 0), ban, font=f_banner)
    d.text(((W - (bb[2] - bb[0])) // 2 - bb[0], 1080), ban, fill=0, font=f_banner)

    f_tag = ImageFont.truetype(FONT_BALOO, 62)
    tag = "50 Big & Cozy Designs with Fun Facts"
    bb = d.textbbox((0, 0), tag, font=f_tag)
    d.text(((W - (bb[2] - bb[0])) // 2 - bb[0], 1290), tag, fill=80, font=f_tag)

    icon = Image.open(HERO_CROP).convert("L")
    icon = icon.point(lambda p: 0 if p < 120 else 255)
    icon.thumbnail((1250, 1000), Image.LANCZOS)
    page.paste(icon, ((W - icon.width) // 2, 1440))

    f_by = ImageFont.truetype(FONT_BALOO, 55)
    d.text(((W - 140) // 2, 2620), "Created by", fill=100, font=f_by)
    f_auth = ImageFont.truetype(FONT_PACIFICO, 110)
    bb = d.textbbox((0, 0), "Matilda Hayes", font=f_auth)
    d.text(((W - (bb[2] - bb[0])) // 2 - bb[0], 2700), "Matilda Hayes", fill=0, font=f_auth)

    f_imp = ImageFont.truetype(FONT_BALOO, 50)
    bb = d.textbbox((0, 0), "GUMLEAF KIDS PRESS", font=f_imp)
    d.text(((W - (bb[2] - bb[0])) // 2 - bb[0], 2930), "GUMLEAF KIDS PRESS", fill=100, font=f_imp)

    return page


def make_copyright_page():
    page = Image.new("L", (W, H), 255)
    d = ImageDraw.Draw(page)
    f_reg = ImageFont.truetype(FONT_BALOO, 46)
    f_bold = ImageFont.truetype(FONT_BALOO, 54)

    lines = [
        (TITLE, f_bold),
        ("First Edition, October 2026", f_reg),
        ("", f_reg),
        ("Published by Gumleaf Kids Press", f_bold),
        ("Melbourne, Australia", f_reg),
        ("", f_reg),
        ("Created by Matilda Hayes", f_bold),
        ("Copyright © 2026 Gumleaf Kids Press", f_reg),
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
        ("Designed and printed for young artists everywhere.", f_reg),
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

    d.rounded_rectangle((160, 160, W - 160, H - 160), radius=50, outline=0, width=10)

    f_title = ImageFont.truetype(FONT_SNIGLET, 120)
    text = "THIS BOOK BELONGS TO:"
    bb = d.textbbox((0, 0), text, font=f_title)
    d.text(((W - (bb[2] - bb[0])) // 2 - bb[0], 650), text, fill=0, font=f_title)

    d.line([(350, 1000), (W - 350, 1000)], fill=0, width=10)
    d.line([(350, 1200), (W - 350, 1200)], fill=0, width=10)

    f_name = ImageFont.truetype(FONT_BALOO, 60)
    d.text(((W - 400) // 2, 1050), "ARTIST NAME", fill=140, font=f_name)

    icon = Image.open(HERO_CROP).convert("L")
    icon = icon.point(lambda p: 0 if p < 120 else 255)
    icon.thumbnail((1100, 850), Image.LANCZOS)
    page.paste(icon, ((W - icon.width) // 2, 1450))

    f_msg = ImageFont.truetype(FONT_BALOO, 65)
    msg = "Get ready to color 50 yummy friends!"
    bb = d.textbbox((0, 0), msg, font=f_msg)
    d.text(((W - (bb[2] - bb[0])) // 2 - bb[0], 2800), msg, fill=50, font=f_msg)

    return page


def make_tips_page():
    page = Image.new("L", (W, H), 255)
    d = ImageDraw.Draw(page)

    d.rounded_rectangle((160, 160, W - 160, H - 160), radius=50, outline=0, width=10)
    d.rounded_rectangle((185, 185, W - 185, H - 185), radius=40, outline=0, width=4)

    f_title = ImageFont.truetype(FONT_SNIGLET, 130)
    t = "TOP COLORING TIPS!"
    bb = d.textbbox((0, 0), t, font=f_title)
    d.text(((W - (bb[2] - bb[0])) // 2 - bb[0], 230), t, fill=0, font=f_title)

    tips = [
        ("1. Put a Blank Sheet Behind Your Page", "When using juicy markers, place a scrap sheet behind your drawing to keep the next page perfectly clean!"),
        ("2. Start Light, Then Go Dark", "Color lighter shades first, then layer darker tones on top for amazing depth and pop."),
        ("3. Mix Your Art Tools", "Try combining crayons, colored pencils, and markers together on the same picture for fun textures."),
        ("4. There Are No Mistakes In Art!", "Make your treats any color you want. Blue pancakes and rainbow cupcakes are awesome!"),
    ]
    f_head = ImageFont.truetype(FONT_BALOO, 60)
    f_desc = ImageFont.truetype(FONT_BALOO, 48)

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
    f_test_title = ImageFont.truetype(FONT_SNIGLET, 105)
    tt = "MY COLOR TEST PALETTE"
    bb = d.textbbox((0, 0), tt, font=f_test_title)
    d.text(((W - (bb[2] - bb[0])) // 2 - bb[0], y_test), tt, fill=0, font=f_test_title)

    f_test_sub = ImageFont.truetype(FONT_BALOO, 48)
    tsub = "Test your pencils, markers, and crayons here before coloring your yummy friends!"
    bb = d.textbbox((0, 0), tsub, font=f_test_sub)
    d.text(((W - (bb[2] - bb[0])) // 2 - bb[0], y_test + 120), tsub, fill=90, font=f_test_sub)

    f_num = ImageFont.truetype(FONT_BALOO, 44)
    radius = 125
    y_circles = y_test + 360

    for i in range(5):
        cx = 360 + i * 455
        d.ellipse([cx - radius, y_circles - radius, cx + radius, y_circles + radius], outline=0, width=7)
        lbl = "Color %d" % (i + 1)
        lbb = d.textbbox((0, 0), lbl, font=f_num)
        d.text((cx - (lbb[2] - lbb[0]) // 2 - lbb[0], y_circles + radius + 20), lbl, fill=100, font=f_num)

    d.line([(220, y_circles + radius + 110), (W - 220, y_circles + radius + 110)], fill=180, width=4)

    y_bottom = y_circles + radius + 160

    icon = Image.open(HERO_CROP).convert("L")
    icon = icon.point(lambda p: 0 if p < 120 else 255)
    icon.thumbnail((880, 660), Image.LANCZOS)
    page.paste(icon, (240, y_bottom + 60))

    box_x = 1180
    d.rounded_rectangle([box_x, y_bottom, W - 240, y_bottom + 820], radius=35, outline=0, width=6)

    f_pl_title = ImageFont.truetype(FONT_SNIGLET, 62)
    d.text((box_x + 60, y_bottom + 60), "MY ARTIST PLEDGE:", fill=0, font=f_pl_title)

    f_pl_text = ImageFont.truetype(FONT_BALOO, 50)
    d.text((box_x + 60, y_bottom + 180), '"I promise to have fun,', fill=40, font=f_pl_text)
    d.text((box_x + 60, y_bottom + 250), 'make this book my own,', fill=40, font=f_pl_text)
    d.text((box_x + 60, y_bottom + 320), 'and be proud of every', fill=40, font=f_pl_text)
    d.text((box_x + 60, y_bottom + 390), 'drawing I color!"', fill=40, font=f_pl_text)

    d.line([(box_x + 60, y_bottom + 600), (W - 300, y_bottom + 600)], fill=0, width=5)
    f_sig_lbl = ImageFont.truetype(FONT_BALOO, 44)
    d.text((box_x + 60, y_bottom + 625), "ARTIST SIGNATURE", fill=120, font=f_sig_lbl)

    f_pnum = ImageFont.truetype(FONT_BALOO, 55)
    framed_page_number(d, "4")

    return page


def make_art_page(i):
    key = "page_%02d" % i
    raw2_path = os.path.join(RAW2_DIR, "%s.png" % key)
    caption_text = CAPTIONS.get(key, "")
    page_num = str(i * 2 + 3)

    # F11: vector-trace the native art -> crisp at print size (no upscale softness/halos).
    # BIGGER art box: 2230 x 2520 (0.53" side margins at 2230). Trace at 2x and reduce
    # with Lanczos: the anti-aliased edges survive to the 600 DPI threshold in
    # to_print_bw instead of 1/300 in stair-steps.
    sys.path.insert(0, ROOT)
    from vectorize_line_art import vectorize_line_art
    img = vectorize_line_art(raw2_path, None, target_w=2230 * 2, target_h=2520 * 2)
    img = img.resize((img.width // 2, img.height // 2), Image.LANCZOS)

    page = Image.new("L", (W, H), 255)
    x_p = (W - img.width) // 2
    y_p = 170
    page.paste(img, (x_p, y_p))

    d = ImageDraw.Draw(page)
    draw_uniform_caption(d, caption_text)

    f_num = ImageFont.truetype(FONT_BALOO, 60)
    nb = d.textbbox((0, 0), page_num, font=f_num)
    d.text((W - 200 - (nb[2] - nb[0]), 3010), page_num, fill=120, font=f_num)

    return page


def make_checklist_page():
    page = Image.new("L", (W, H), 255)
    d = ImageDraw.Draw(page)

    d.rounded_rectangle((160, 160, W - 160, H - 160), radius=50, outline=0, width=8)

    f_title = ImageFont.truetype(FONT_SNIGLET, 95)
    text = "MY YUMMY CUTIES CHECKLIST"
    bb = d.textbbox((0, 0), text, font=f_title)
    d.text(((W - (bb[2] - bb[0])) // 2 - bb[0], 280), text, fill=0, font=f_title)

    f_sub = ImageFont.truetype(FONT_BALOO, 50)
    sub = "Check each box as you finish coloring each yummy page!"
    bb = d.textbbox((0, 0), sub, font=f_sub)
    d.text(((W - (bb[2] - bb[0])) // 2 - bb[0], 410), sub, fill=90, font=f_sub)

    names = [
        "1. Cupcake baker", "2. Pancake stack", "3. Honeycomb bear", "4. Strawberry patch",
        "5. Ice cream cone", "6. Popcorn night", "7. Pizza chef", "8. Banana monkey",
        "9. Watermelon picnic", "10. Carrot pull", "11. Apple orchard", "12. Pineapple sloth",
        "13. Peanut elephant", "14. Cacao tree", "15. Cotton candy fair", "16. Ice pop day",
        "17. Spaghetti slurp", "18. Sushi rolls", "19. Corn field", "20. Blueberry bush",
        "21. Lemonade", "22. Grape vine", "23. Broccoli forest", "24. Potato dig",
        "25. Avocado toast", "26. Tomato garden", "27. Pumpkin patch", "28. Coconut beach",
        "29. Cookie picnic", "30. Donut stack", "31. Pretzel seal", "32. Bread baker",
        "33. Waffle breakfast", "34. Hot cocoa", "35. Milkshake", "36. Big sandwich",
        "37. Cinnamon rolls", "38. Kiwi and kiwi", "39. Tea party", "40. S'mores campfire",
        "41. Birthday cake", "42. Swiss cheese", "43. Maple syrup", "44. Bamboo lunch",
        "45. Orange grove", "46. Apple pie", "47. Egg nest", "48. Mango toucan",
        "49. Cranberry bog", "50. Yummy Cuties feast",
    ]

    f_item = ImageFont.truetype(FONT_BALOO, 46)
    y_start = 510
    for idx, name in enumerate(names):
        col = idx // 25
        row = idx % 25
        x = 260 if col == 0 else 1340
        y = y_start + row * 95
        d.rectangle([x, y + 6, x + 38, y + 44], outline=0, width=5)
        d.text((x + 60, y), name, fill=30, font=f_item)

    framed_page_number(d, "105")
    return page


def make_certificate_page():
    page = Image.new("L", (W, H), 255)
    d = ImageDraw.Draw(page)

    d.rounded_rectangle((160, 160, W - 160, H - 160), radius=70, outline=0, width=16)
    d.rounded_rectangle((195, 195, W - 195, H - 195), radius=55, outline=0, width=6)

    f_top = ImageFont.truetype(FONT_BALOO, 70)
    t = "OFFICIAL CERTIFICATE"
    bb = d.textbbox((0, 0), t, font=f_top)
    d.text(((W - (bb[2] - bb[0])) // 2 - bb[0], 400), t, fill=60, font=f_top)

    award = "YUMMY ARTIST AWARD"
    size = 150  # shrink until the award keeps 100+ px clear of the inner frame (x 195..2355)
    f_award = ImageFont.truetype(FONT_SNIGLET, size)
    while d.textbbox((0, 0), award, font=f_award)[2] - d.textbbox((0, 0), award, font=f_award)[0] > 1960:
        size -= 4
        f_award = ImageFont.truetype(FONT_SNIGLET, size)
    bb = d.textbbox((0, 0), award, font=f_award)
    d.text(((W - (bb[2] - bb[0])) // 2 - bb[0], 550), award, fill=0, font=f_award)

    f_p = ImageFont.truetype(FONT_BALOO, 65)
    p1 = "This certifies that"
    bb = d.textbbox((0, 0), p1, font=f_p)
    d.text(((W - (bb[2] - bb[0])) // 2 - bb[0], 900), p1, fill=60, font=f_p)

    d.line([(400, 1250), (W - 400, 1250)], fill=0, width=8)
    f_lbl = ImageFont.truetype(FONT_BALOO, 50)
    d.text(((W - 350) // 2, 1280), "NAME OF ARTIST", fill=130, font=f_lbl)

    line1, line2 = "has successfully colored all 50 cozy", "Yummy Cuties pages in this book!"
    for line, yy in ((line1, 1500), (line2, 1580)):
        bb2 = d.textbbox((0, 0), line, font=f_p)
        d.text(((W - (bb2[2] - bb2[0])) // 2 - bb2[0], yy), line, fill=40, font=f_p)

    # round badge (the 4-point star's centre was too narrow for the number)
    d.ellipse((W // 2 - 170, 1950 - 170, W // 2 + 170, 1950 + 170), outline=0, width=14)
    d.ellipse((W // 2 - 140, 1950 - 140, W // 2 + 140, 1950 + 140), outline=0, width=5)
    # Sniglet and Baloo 2 have no star glyph (it prints as a box): plain number
    f_star = ImageFont.truetype(FONT_SNIGLET, 130)
    sbb = d.textbbox((0, 0), "50", font=f_star)
    d.text((W // 2 - (sbb[2] - sbb[0]) // 2 - sbb[0], 1950 - (sbb[3] - sbb[1]) // 2 - sbb[1]), "50", fill=0, font=f_star)

    d.line([(350, 2600), (950, 2600)], fill=0, width=6)
    d.line([(W - 950, 2600), (W - 350, 2600)], fill=0, width=6)

    f_sig = ImageFont.truetype(FONT_PACIFICO, 75)
    d.text((450, 2480), "Matilda Hayes", fill=0, font=f_sig)

    f_siglbl = ImageFont.truetype(FONT_BALOO, 50)
    d.text((540, 2630), "AUTHOR", fill=100, font=f_siglbl)
    d.text((W - 720, 2630), "DATE", fill=100, font=f_siglbl)

    framed_page_number(d, "107")
    return page


def make_thank_you_page():
    page = Image.new("L", (W, H), 255)
    d = ImageDraw.Draw(page)

    d.rounded_rectangle((160, 160, W - 160, H - 160), radius=50, outline=0, width=8)

    f_title = ImageFont.truetype(FONT_SNIGLET, 120)
    t = "THANK YOU!"
    bb = d.textbbox((0, 0), t, font=f_title)
    d.text(((W - (bb[2] - bb[0])) // 2 - bb[0], 350), t, fill=0, font=f_title)

    f_msg = ImageFont.truetype(FONT_BALOO, 62)
    msg = [
        "Thank you for coloring with Gumleaf Kids Press!",
        "We hope you loved your tasty treat",
        "adventure with Matilda Hayes.",
        "",
        "If you loved this book, please consider leaving a kind",
        "review on Amazon. It helps independent Australian",
        "bookmakers create more adventures for kids!",
        "",
        "MORE FROM MATILDA HAYES:",
        u"• Aussie Cuties: Out Now!",
        u"• Great Barrier Reef Ocean Friends: Out Now!",
        u"• Aussie Cuties at Halloween: Out Now!",
        u"• Snowy Cuties: Out Now!",
        u"• Pawsome Cuties: Out Now!",
    ]
    y = 650
    for line in msg:
        if line:
            bb = d.textbbox((0, 0), line, font=f_msg)
            d.text(((W - (bb[2] - bb[0])) // 2 - bb[0], y), line, fill=30 if not line.startswith(u"\u2022") else 0, font=f_msg)
        y += 95

    f_imp = ImageFont.truetype(FONT_BALOO, 56)
    imp = "GUMLEAF KIDS PRESS  •  MELBOURNE, AUSTRALIA"
    bb = d.textbbox((0, 0), imp, font=f_imp)
    d.text(((W - (bb[2] - bb[0])) // 2 - bb[0], 2850), imp, fill=100, font=f_imp)

    framed_page_number(d, "108")
    return page


def to_print_bw(page, line_art):
    """2x Lanczos to 600 DPI, then 1-bit (same as book1). Line art is thresholded for
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

    interior_pdf_path = os.path.join(OUTPUT_DIR, "YUMMY_CUTIES_INTERIOR_108P.pdf")
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
