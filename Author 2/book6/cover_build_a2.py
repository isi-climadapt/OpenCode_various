# -*- coding: utf-8 -*-
# Author 2 Book 6 (Stomp Wonders): Front cover options builder (Lane A Premium Educational House):
# white/bright bg + Lilita One solid wordmark + age badge + colored kawaii hero +
# WATTLE WONDERS wordmark. No blob-prone stroke synthesis anywhere.
# Usage: py cover_build_a2.py [--gen] [--panel]

import os, sys, subprocess, time
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")
FONT_LILITA = os.path.join(FONTS, "LilitaOne-Regular.ttf")
FONT_FREDO = os.path.join(FONTS, "Fredoka.ttf")
FONT_PACIFICO = os.path.join(FONTS, "Pacifico-Regular.ttf")
EXE = r"C:\Users\ibian\AppData\Local\Programs\openart\bin\openart.exe"
MODEL = "nano-banana-2"

W, H = 2550, 3300
BG = (255, 255, 255)
DARK = (30, 30, 35)
BLUE = (35, 90, 160)
YELLOW = (255, 200, 40)

TITLE_LINES = ('STOMP', 'WONDERS')
BAND = 'DINOSAUR COLORING BOOK'
TAG = '50 BIG & BOLD DESIGNS  |  FUN FACTS ON EVERY PAGE'

STYLE = ("thick clean smooth dark outlines, colored in soft bright marker colors, plain white "
         "background, kawaii cute style, chunky rounded shapes, centred composition, professional "
         "kids coloring book cover art. No text, no words, no letters, no numbers, no signs, "
         "no writing anywhere, no border, no frame, no watermark.")

HERO_PROMPTS = {
    "A": ("Children's coloring book cover illustration: one adorable smiling T. rex with a big head, "
          "a happy closed-mouth smile and tiny waving arms in the middle, with a cute triceratops, a "
          "stegosaurus and a little long-neck dinosaur around it among ferns, palm-like trees, a small "
          "volcano and sparkles, no sharp teeth showing, " + STYLE),
    "B": ("Children's coloring book cover illustration: a cheerful group of cute dinosaurs with happy "
          "closed-mouth smiles standing together on a grassy hill: a T. rex, a triceratops, a "
          "stegosaurus, a long-neck brachiosaurus and a little pterodactyl flying above, with ferns, a "
          "smiling sun and sparkles, no sharp teeth showing, " + STYLE),
    "C": ("Children's coloring book cover illustration: one big cute baby T. rex with a happy "
          "closed-mouth smile stomping forward with one foot lifted, a little dust puff under its "
          "foot, with a baby triceratops and a baby stegosaurus peeking around it among ferns, palm "
          "leaves, stars and sparkles, no sharp teeth showing, " + STYLE),
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


def fit_font(d, text, path, px, max_w):
    """Largest font size <= px whose text fits max_w."""
    while px > 40:
        f = ImageFont.truetype(path, px)
        bb = d.textbbox((0, 0), text, font=f)
        if bb[2] - bb[0] <= max_w:
            return f, bb
        px -= 4
    return f, bb


def centre_text(d, text, f, bb, y, fill):
    d.text(((W - (bb[2] - bb[0])) // 2 - bb[0], y - bb[1]), text, fill=fill, font=f)


def build_front(hero_tag):
    # Laid out to read at Amazon search size (~160-220 px tall): dark title, a solid
    # band saying what the book is, and the art filling the lower half.
    hero_path = os.path.join(HERE, "cover_hero_%s.png" % hero_tag)
    out_path = os.path.join(HERE, "cover_option_%s.png" % hero_tag)

    canvas = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(canvas)

    # bold color-block frame: thick blue outer + yellow inner accents
    d.rounded_rectangle((90, 90, W - 90, H - 90), radius=60, outline=BLUE, width=26)
    d.rounded_rectangle((150, 150, W - 150, H - 150), radius=35, outline=YELLOW, width=10)

    # publisher wordmark (top)
    f_pub = ImageFont.truetype(FONT_FREDO, 56)
    pub = "WATTLE WONDERS PUBLISHING"
    pbb = d.textbbox((0, 0), pub, font=f_pub)
    centre_text(d, pub, f_pub, pbb, 200, (90, 130, 60))

    # title: LILITA solid, two lines (must match the KDP title field)
    for text, y in [(TITLE_LINES[0], 300), (TITLE_LINES[1], 540)]:
        f, bb = fit_font(d, text, FONT_LILITA, 270, W - 420)
        centre_text(d, text, f, bb, y, DARK)

    # what-it-is band: solid blue, white subject line + yellow age line
    d.rounded_rectangle((200, 810, W - 200, 1190), radius=40, fill=BLUE)
    f, bb = fit_font(d, BAND, FONT_LILITA, 190, W - 480)
    centre_text(d, BAND, f, bb, 845, (255, 255, 255))
    f, bb = fit_font(d, "FOR KIDS AGES 4-8", FONT_LILITA, 130, W - 480)
    centre_text(d, "FOR KIDS AGES 4-8", f, bb, 1045, YELLOW)

    # hero: cropped to its drawing, then aspect-preserving fit into the 2130 x 1700 box.
    # No sharpening: on enlarged art it only draws light halos round the outlines.
    # Needs a 2K hero to print 270+ DPI.
    hero = Image.open(hero_path).convert("RGB")
    # AI backgrounds come back off-white (~253); lift near-white to pure white so the
    # hero has no faint square against the white cover
    hero = hero.point(lambda v: 255 if v > 244 else v)
    ink = hero.convert("L").point(lambda v: 255 if v < 250 else 0).getbbox()
    if ink:
        pad = 24
        hero = hero.crop((max(ink[0] - pad, 0), max(ink[1] - pad, 0),
                          min(ink[2] + pad, hero.width), min(ink[3] + pad, hero.height)))
    box_w, box_h, box_y = 2130, 1700, 1250
    scale = min(box_w / hero.width, box_h / hero.height)
    if 300.0 / scale < 270:
        print("WARNING: %s prints at %d DPI (needs 270+); regenerate at 2K" % (os.path.basename(hero_path), 300.0 / scale))
    hero = hero.resize((int(hero.width * scale), int(hero.height * scale)), Image.LANCZOS)
    canvas.paste(hero, ((W - hero.width) // 2, box_y + (box_h - hero.height) // 2))

    # bottom tag, clear of the yellow inner frame (y 3140-3150)
    f, bb = fit_font(d, TAG, FONT_LILITA, 76, W - 480)
    centre_text(d, TAG, f, bb, 3010, BLUE)

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
