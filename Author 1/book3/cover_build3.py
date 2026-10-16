# -*- coding: utf-8 -*-
# Book 3 — Front cover options builder (Coco Wyo formula + F9-safe typeset).
# Title rendered via MANUAL outline on RGBA overlay (stroke_width synthesis unreliable).
# Usage: py cover_build3.py            (assembles existing cover_hero_[ABC].png)
#        py cover_build3.py --gen      (generate heroes via OpenArt first)
#        py cover_build3.py --panel    (3-up choice panel)

import os, sys, subprocess, time
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")
FONT_SNIGLET = os.path.join(FONTS, "Sniglet-ExtraBold.ttf")
FONT_BALOO = os.path.join(FONTS, "Baloo2.ttf")
FONT_PACIFICO = os.path.join(FONTS, "Pacifico-Regular.ttf")
EXE = r"C:\Users\ibian\AppData\Local\Programs\openart\bin\openart.exe"
MODEL = "nano-banana-2"

W, H = 2550, 3300
MIN_DPI = 270
BG = (246, 237, 225)
DARK = (35, 25, 20)
SUB = (80, 60, 50)
TAG = (110, 90, 80)
IMPRINT = (150, 130, 120)

STYLE = ("thick clean smooth dark outlines, coloured in soft bright marker colours, warm cream "
         "beige background, kawaii cute style, chunky rounded shapes, centred composition, "
         "professional kids colouring book cover art. No text, no words, no letters, no watermark.")

HERO_PROMPTS = {
    "A": ("Children's colouring book cover illustration: one adorable smiling koala wearing a round "
          "white ghost costume waving hello beside a happy kangaroo in a witch hat stirring a small "
          "cauldron, pumpkins, cute bats and a crescent moon around them, " + STYLE),
    "B": ("Children's colouring book cover illustration: one adorable smiling wombat wearing a "
          "vampire cape and a happy platypus pirate with a tricorn hat holding a candy basket, "
          "pumpkins, spooky trees, bats and stars around them, " + STYLE),
    "C": ("Children's colouring book cover illustration: one cute dingo werewolf howling happily "
          "at a big friendly full moon beside a smiling black cat, pumpkins, gravestones with "
          "rounded tops, bats and clouds around them, " + STYLE),
}


def save(img, path):
    for a in range(4):
        try:
            img.save(path, dpi=(300, 300)); return
        except OSError:
            time.sleep(2 * (a + 1))
    raise OSError(path)


def gen_hero(tag):
    path = os.path.join(HERE, "cover_hero_%s.png" % tag)
    if os.path.exists(path) and os.path.getsize(path) > 10000 and "--regen" not in sys.argv:
        return path, "cached"
    r = subprocess.run([EXE, "generate", "image", HERO_PROMPTS[tag], "--model", MODEL,
                        "-o", path, "--quiet", "--yes"], capture_output=True, text=True, timeout=300)
    return path, "ok" if r.returncode == 0 else "FAIL " + (r.stderr or r.stdout)[-120:]


def build_front(hero_tag):
    hero_path = os.path.join(HERE, "cover_hero_%s.png" % hero_tag)
    out_path = os.path.join(HERE, "cover_option_%s.png" % hero_tag)

    canvas = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(canvas)

    d.rounded_rectangle((90, 90, W - 90, H - 90), radius=110, outline=DARK, width=16)
    d.rounded_rectangle((130, 130, W - 130, H - 130), radius=85, outline=DARK, width=5)

    f_auth = ImageFont.truetype(FONT_PACIFICO, 100)
    abb = d.textbbox((0, 0), "Matilda Hayes", font=f_auth)
    d.text(((W - (abb[2] - abb[0])) // 2 - abb[0], 175), "Matilda Hayes", fill=(70, 50, 40), font=f_auth)

    # bubble title, two lines — MANUAL outline on RGBA overlay (F2/F5-safe, deterministic)
    f_title = ImageFont.truetype(FONT_SNIGLET, 225)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    for text, y in [("AUSSIE", 470), ("CUTIES", 720)]:
        bb = od.textbbox((0, 0), text, font=f_title)
        tx = (W - (bb[2] - bb[0])) // 2 - bb[0]
        od.text((tx + 5, y + 8), text, font=f_title, fill=DARK + (255,))
        for dx in (-6, 0, 6):
            for dy in (-6, 0, 6):
                if dx or dy:
                    od.text((tx + dx, y + dy), text, font=f_title, fill=DARK + (255,))
        od.text((tx, y), text, font=f_title, fill=(255, 255, 255, 255))
    canvas.paste(ov, (0, 0), ov)
    d = ImageDraw.Draw(canvas)

    # banner
    f_banner = ImageFont.truetype(FONT_SNIGLET, 120)
    ban = "AT HALLOWEEN"
    bbb = d.textbbox((0, 0), ban, font=f_banner)
    d.text(((W - (bbb[2] - bbb[0])) // 2 - bbb[0], 1010), ban, fill=(200, 90, 30), font=f_banner)

    # subtitle
    f_sub = ImageFont.truetype(FONT_BALOO, 72)
    sub = "A CUTE & SPOOKY COLOURING BOOK"
    sbb = d.textbbox((0, 0), sub, font=f_sub)
    d.text(((W - (sbb[2] - sbb[0])) // 2 - sbb[0], 1190), sub, fill=SUB, font=f_sub)

    # hero: aspect-preserving fit into 1620px box, centred. No sharpening: on
    # enlarged art it only draws light halos round the outlines.
    hero = Image.open(hero_path).convert("RGB")
    scale = min(1620 / hero.width, 1620 / hero.height)
    dpi = 300.0 / scale
    if dpi < MIN_DPI:
        print("WARNING: %s prints at %d DPI (needs %d+); regenerate at 2K" % (os.path.basename(hero_path), dpi, MIN_DPI))
    hero = hero.resize((int(hero.width * scale), int(hero.height * scale)), Image.LANCZOS)
    hx = (W - hero.width) // 2
    hy = 1300 + (1620 - hero.height) // 2
    canvas.paste(hero, (hx, hy))

    # bottom tag + imprint (clear of inner border at y=3170)
    f_tag = ImageFont.truetype(FONT_BALOO, 68)
    tag = "50 BIG & EASY DESIGNS"
    tbb = d.textbbox((0, 0), tag, font=f_tag)
    d.text(((W - (tbb[2] - tbb[0])) // 2 - tbb[0], 2960), tag, fill=TAG, font=f_tag)

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
    if "--gen" in sys.argv or not any(os.path.exists(os.path.join(HERE, "cover_hero_%s.png" % t)) for t in "ABC"):
        for t in "ABC":
            p, status = gen_hero(t)
            print("hero", t, status, flush=True)
    built = [build_front(t) for t in "ABC"]
    for b in built:
        print("built", b)
    print("panel:", panel(built))
