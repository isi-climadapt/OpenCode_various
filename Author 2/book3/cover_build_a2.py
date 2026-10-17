# -*- coding: utf-8 -*-
# Author 2 Book 3 (Robot Wonders): Front cover options builder (Lane A Premium Educational House):
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

STYLE = ("thick clean smooth dark outlines, colored in soft bright marker colors, plain white "
         "background, kawaii cute style, chunky rounded shapes, centred composition, professional "
         "kids coloring book cover art. No text, no words, no letters, no watermark.")

HERO_PROMPTS = {
    "A": ("Children's coloring book cover illustration: one adorable smiling friendly robot with a "
          "round head, antennas and a happy face waving in the middle, with a cute Mars rover, a robot "
          "dog and a small drone around it among gears and sparkles, " + STYLE),
    "B": ("Children's coloring book cover illustration: a cheerful group of cute robots waving "
          "together: a humanoid robot, a robot vacuum, a robot dog and a six-wheeled rover, with "
          "stars, gears and sparkles around them, " + STYLE),
    "C": ("Children's coloring book cover illustration: one cute smiling six-wheeled Mars rover "
          "with a camera head and a happy face exploring rocky hills, with a little helicopter "
          "flying above and stars around, " + STYLE),
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

    # bold color-block frame: thick blue outer + yellow inner accents
    d.rounded_rectangle((90, 90, W - 90, H - 90), radius=60, outline=BLUE, width=26)
    d.rounded_rectangle((150, 150, W - 150, H - 150), radius=35, outline=YELLOW, width=10)

    # publisher wordmark (top)
    f_pub = ImageFont.truetype(FONT_FREDO, 62)
    pub = "WATTLE WONDERS PUBLISHING"
    pbb = d.textbbox((0, 0), pub, font=f_pub)
    d.text(((W - (pbb[2] - pbb[0])) // 2 - pbb[0], 200), pub, fill=(90, 130, 60), font=f_pub)

    # title: LILITA solid, two lines
    f_title = ImageFont.truetype(FONT_LILITA, 250)
    for text, y in [("ROBOT", 560), ("WONDERS", 820)]:
        bb = d.textbbox((0, 0), text, font=f_title)
        d.text(((W - (bb[2] - bb[0])) // 2 - bb[0], y), text, fill=DARK, font=f_title)

    # age badge pill (yellow with blue stroke)
    f_age = ImageFont.truetype(FONT_LILITA, 95)
    age = "AGES 3-8  |  FUN FACTS ON EVERY PAGE"
    abb = d.textbbox((0, 0), age, font=f_age)
    bx0 = (W - (abb[2] - abb[0])) // 2 - 60
    by0 = 1150
    d.rounded_rectangle([bx0, by0, bx0 + (abb[2] - abb[0]) + 120, by0 + 170], radius=60,
                        fill=YELLOW, outline=BLUE, width=8)
    d.text((bx0 + 60 - abb[0], by0 + 30), age, fill=DARK, font=f_age)

    # hero: aspect-preserving fit into 1600px box, centred. No sharpening: on enlarged
    # art it only draws light halos round the outlines. Needs a 2K hero to print 270+ DPI.
    hero = Image.open(hero_path).convert("RGB")
    scale = min(1600 / hero.width, 1600 / hero.height)
    if 300.0 / scale < 270:
        print("WARNING: %s prints at %d DPI (needs 270+); regenerate at 2K" % (os.path.basename(hero_path), 300.0 / scale))
    hero = hero.resize((int(hero.width * scale), int(hero.height * scale)), Image.LANCZOS)
    hx = (W - hero.width) // 2
    hy = 1400 + (1600 - hero.height) // 2
    # AI backgrounds come back off-white (~253); lift near-white to pure white so the
    # hero has no faint square against the white cover
    hero = hero.point(lambda v: 255 if v > 244 else v)
    canvas.paste(hero, (hx, hy))

    # bottom tag
    f_tag = ImageFont.truetype(FONT_FREDO, 60)
    tag = "50 BIG & BOLD ROBOT DESIGNS"
    tbb = d.textbbox((0, 0), tag, font=f_tag)
    # 3090 sat on the yellow inner frame (y 3140-3150); 3045 clears it
    d.text(((W - (tbb[2] - tbb[0])) // 2 - tbb[0], 3045), tag, fill=BLUE, font=f_tag)

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
