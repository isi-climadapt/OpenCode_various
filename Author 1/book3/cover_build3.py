# -*- coding: utf-8 -*-
# Book 3 — Front cover options builder (Coco Wyo formula + F9-safe typeset).
# Thumbnail-first layout: solid dark one-line title, art cropped to fill the middle,
# purple "COLOURING BOOK / FOR KIDS AGES 3-8" band.
# Usage: py cover_build3.py            (assembles existing cover_hero_[ABC].png)
#        py cover_build3.py --gen      (generate heroes via OpenArt first)
#        py cover_build3.py --panel    (3-up choice panel)

import os, sys, subprocess, time
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")
FONT_SNIGLET = os.path.join(FONTS, "Sniglet-ExtraBold.ttf")
FONT_BALOO = os.path.join(FONTS, "Baloo2.ttf")
FONT_PACIFICO = os.path.join(FONTS, "Pacifico-Regular.ttf")
FONT_LILITA = os.path.join(FONTS, "LilitaOne-Regular.ttf")
EXE = r"C:\Users\ibian\AppData\Local\Programs\openart\bin\openart.exe"
MODEL = "nano-banana-2"

W, H = 2550, 3300
MIN_DPI = 270
BG = (246, 237, 225)
DARK = (35, 25, 20)
SUB = (80, 60, 50)
TAG = (110, 90, 80)
IMPRINT = (150, 130, 120)
HALLOWEEN = (196, 82, 18)
BAND = (72, 40, 104)
BAND_TEXT = (255, 196, 70)
HERO_Y, HERO_W, HERO_H = 765, 2200, 1850   # hero box (between title and band)
BAND_Y = 2630

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


def hero_crop(hero):
    """Crop the hero to its drawn content (plus a small margin) so the art, not its
    empty cream border, fills the cover."""
    import numpy as np
    a = np.asarray(hero).astype(int)
    ink = np.abs(a - a[5, 5]).sum(2) > 40
    rows, cols = ink.sum(1), ink.sum(0)
    y0, y1 = np.argmax(rows > 20), len(rows) - np.argmax(rows[::-1] > 20)
    x0, x1 = np.argmax(cols > 20), len(cols) - np.argmax(cols[::-1] > 20)
    m = hero.width // 75
    return hero.crop((max(0, x0 - m), max(0, y0 - m), min(hero.width, x1 + m), min(hero.height, y1 + m)))


def match_background(hero):
    """Shift the hero's own cream (and only colours close to it) to the cover's BG,
    so the hero doesn't show as a lighter box. Art colours further away are untouched."""
    import numpy as np
    a = np.asarray(hero).astype(float)
    src = np.median(np.concatenate([a[:8].reshape(-1, 3), a[-8:].reshape(-1, 3)]), axis=0)
    w = np.clip(1 - np.abs(a - src).sum(2) / 45.0, 0, 1)[..., None]
    a = a + w * (np.array(BG, float) - src)
    return Image.fromarray(np.clip(a.round(), 0, 255).astype("uint8"), "RGB")


def centred(d, text, font, y, fill):
    bb = d.textbbox((0, 0), text, font=font)
    d.text(((W - (bb[2] - bb[0])) // 2 - bb[0], y), text, fill=fill, font=font)


def build_front(hero_tag):
    hero_path = os.path.join(HERE, "cover_hero_%s.png" % hero_tag)
    out_path = os.path.join(HERE, "cover_option_%s.png" % hero_tag)

    canvas = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(canvas)

    d.rounded_rectangle((90, 90, W - 90, H - 90), radius=110, outline=DARK, width=16)
    d.rounded_rectangle((130, 130, W - 130, H - 130), radius=85, outline=DARK, width=5)

    centred(d, "Matilda Hayes", ImageFont.truetype(FONT_PACIFICO, 85), 165, (70, 50, 40))

    # Title in solid dark type on one line. The old white-with-outline title
    # vanished into the cream background at search-result size.
    f_title = ImageFont.truetype(FONT_SNIGLET, 268)
    centred(d, "AUSSIE CUTIES", f_title, 290, DARK)
    centred(d, "AT HALLOWEEN", ImageFont.truetype(FONT_SNIGLET, 160), 585, HALLOWEEN)

    # hero: cropped to its content and fitted to the box between title and band.
    # No sharpening: on enlarged art it only draws light halos round the outlines.
    # Edges are feathered into the cover cream so the hero's own (slightly lighter)
    # cream doesn't show as a box.
    hero = match_background(hero_crop(Image.open(hero_path).convert("RGB")))
    scale = min(HERO_W / hero.width, HERO_H / hero.height)
    dpi = 300.0 / scale
    if dpi < MIN_DPI:
        print("WARNING: %s prints at %d DPI (needs %d+); regenerate at 2K" % (os.path.basename(hero_path), dpi, MIN_DPI))
    hero = hero.resize((int(hero.width * scale), int(hero.height * scale)), Image.LANCZOS)
    mask = Image.new("L", hero.size, 0)
    ImageDraw.Draw(mask).rectangle((30, 30, hero.width - 31, hero.height - 31), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(14))
    canvas.paste(hero, ((W - hero.width) // 2, HERO_Y + (HERO_H - hero.height) // 2), mask)

    # "colouring book for kids" band, big enough to read at search-result size
    d.rounded_rectangle((175, BAND_Y, W - 175, BAND_Y + 360), radius=60, fill=BAND)
    centred(d, "COLOURING BOOK", ImageFont.truetype(FONT_SNIGLET, 182), BAND_Y + 8, (255, 255, 255))
    centred(d, "FOR KIDS AGES 3-8", ImageFont.truetype(FONT_LILITA, 128), BAND_Y + 212, BAND_TEXT)

    # bottom tag + imprint (clear of inner border at y=3170)
    centred(d, "50 BIG & EASY DESIGNS", ImageFont.truetype(FONT_BALOO, 62), 3010, TAG)
    centred(d, "GUMLEAF KIDS PRESS", ImageFont.truetype(FONT_BALOO, 42), 3090, IMPRINT)

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
