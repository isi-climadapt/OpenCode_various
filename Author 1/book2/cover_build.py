# -*- coding: utf-8 -*-
# Book 2 — Front cover options builder (Coco Wyo bestseller formula, locked):
# cream bg + double rounded border + Sniglet bubble title + Pacifico author +
# coloured kawaii hero (UnsharpMask) + Baloo subtitle + "50 BIG & EASY DESIGNS".
# Usage: py cover_build.py            (assembles any existing cover_hero_[ABC].png)
#        py cover_build.py --panel    (3-up choice panel)

import os, sys, time
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")
FONT_SNIGLET = os.path.join(FONTS, "Sniglet-ExtraBold.ttf")
FONT_BALOO = os.path.join(FONTS, "Baloo2.ttf")
FONT_PACIFICO = os.path.join(FONTS, "Pacifico-Regular.ttf")

W, H = 2550, 3300
BG = (246, 237, 225)
DARK = (35, 25, 20)
SUB = (80, 60, 50)
TAG = (110, 90, 80)
IMPRINT = (150, 130, 120)

def save(img, path):
    for a in range(4):
        try:
            img.save(path, dpi=(300, 300)); return
        except OSError:
            time.sleep(2 * (a + 1))
    raise OSError(path)

def build_front(hero_tag):
    hero_path = os.path.join(HERE, "cover_hero_%s.png" % hero_tag)
    out_path = os.path.join(HERE, "cover_option_%s.png" % hero_tag)
    canvas = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(canvas)

    # border: double rounded frame
    d.rounded_rectangle((90, 90, W - 90, H - 90), radius=110, outline=DARK, width=16)
    d.rounded_rectangle((130, 130, W - 130, H - 130), radius=85, outline=DARK, width=5)

    # author (Pacifico script, top)
    f_auth = ImageFont.truetype(FONT_PACIFICO, 100)
    abb = d.textbbox((0, 0), "Matilda Hayes", font=f_auth)
    d.text(((W - (abb[2] - abb[0])) // 2 - abb[0], 175), "Matilda Hayes", fill=(70, 50, 40), font=f_auth)

    # kicker
    f_kick = ImageFont.truetype(FONT_BALOO, 88)
    kick = "GREAT BARRIER REEF"
    kbb = d.textbbox((0, 0), kick, font=f_kick)
    d.text(((W - (kbb[2] - kbb[0])) // 2 - kbb[0], 390), kick, fill=SUB, font=f_kick)

    # bubble title, two lines — drawn on an RGBA overlay with a MANUAL outline.
    # (Pillow's stroke_width synthesis proved unreliable/nondeterministic in this
    #  environment — fills silently dropped, leaving solid blobs. Manual offset
    #  copies + plain fill are deterministic.)
    f_title = ImageFont.truetype(FONT_SNIGLET, 235)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    for text, y in [("OCEAN", 525), ("FRIENDS", 780)]:
        bb = od.textbbox((0, 0), text, font=f_title)
        tx = (W - (bb[2] - bb[0])) // 2 - bb[0]
        od.text((tx + 5, y + 8), text, font=f_title, fill=DARK + (255,))  # shadow
        for dx in (-6, 0, 6):
            for dy in (-6, 0, 6):
                if dx or dy:
                    od.text((tx + dx, y + dy), text, font=f_title, fill=DARK + (255,))
        od.text((tx, y), text, font=f_title, fill=(255, 255, 255, 255))
    canvas.paste(ov, (0, 0), ov)

    # subtitle
    f_sub = ImageFont.truetype(FONT_BALOO, 75)
    sub = "A CUTE & COMFY COLOURING BOOK"
    sbb = d.textbbox((0, 0), sub, font=f_sub)
    d.text(((W - (sbb[2] - sbb[0])) // 2 - sbb[0], 1130), sub, fill=SUB, font=f_sub)

    # hero: aspect-preserving fit into 1650px box, centred, sharpened for print
    hero = Image.open(hero_path).convert("RGB")
    scale = min(1650 / hero.width, 1650 / hero.height)
    hero = hero.resize((int(hero.width * scale), int(hero.height * scale)), Image.LANCZOS)
    hero = hero.filter(ImageFilter.UnsharpMask(radius=2.0, percent=220, threshold=1))
    hx = (W - hero.width) // 2
    hy = 1245 + (1650 - hero.height) // 2
    canvas.paste(hero, (hx, hy))

    # bottom tag + imprint (both must clear the inner border line at y=3170)
    f_tag = ImageFont.truetype(FONT_BALOO, 68)
    tag = "50 BIG & EASY DESIGNS"
    tbb = d.textbbox((0, 0), tag, font=f_tag)
    d.text(((W - (tbb[2] - tbb[0])) // 2 - tbb[0], 2950), tag, fill=TAG, font=f_tag)

    f_pub = ImageFont.truetype(FONT_BALOO, 45)
    pub = "GUMLEAF KIDS PRESS"
    pbb = d.textbbox((0, 0), pub, font=f_pub)
    d.text(((W - (pbb[2] - pbb[0])) // 2 - pbb[0], 3080), pub, fill=IMPRINT, font=f_pub)

    save(canvas, out_path)
    return out_path

def panel(paths):
    tw = 620
    th = int(tw * H / W)
    p = Image.new("RGB", (tw * len(paths) + 40 * (len(paths) + 1), th + 80), (255, 255, 255))
    x = 40
    for path in paths:
        im = Image.open(path).resize((tw, th), Image.LANCZOS)
        p.paste(im, (x, 40))
        x += tw + 40
    out = os.path.join(HERE, "cover_options_panel.png")
    save(p, out)
    return out

if __name__ == "__main__":
    built = [build_front(t) for t in "ABC"]
    for b in built:
        print("built", b)
    print("panel:", panel(built))
