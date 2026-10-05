# -*- coding: utf-8 -*-
# CANONICAL COVER PIPELINE v1.0 (locked process — always OpenArt, never Gemini)
# Design formula copied from Amazon bestseller covers (Coco Wyo / FairyWren pattern):
#   one adorable fully-coloured hero scene + chunky rounded typeset title + soft background + border
# Heroes generated via OpenArt CLI (nano-banana-2). All lettering typeset in Baloo 2 (never AI text).
#
# Usage: py cover_build.py [--only A|B|C]

import os, sys, subprocess
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
CONCEPTS = os.path.join(HERE, "cover_concepts")
EXE = r"C:\Users\ibian\AppData\Local\Programs\openart\bin\openart.exe"
MODEL = "nano-banana-2"
FONT = os.path.join(HERE, "fonts", "Baloo2.ttf")
W, H = 2550, 3300

# Hero scenes (colour, bestseller formula) — regenerate per book
HERO_PROMPTS = {
    "A": ("Children's colouring book cover illustration: one adorable smiling quokka holding a bunch "
          "of cheerful balloons on a sunny sandy beach with turquoise sea and a happy smiling sun, "
          "bright happy colours, kawaii cute style, chunky rounded shapes, clean simple composition, "
          "centred, professional kids book cover art. No text, no words, no letters, no watermark."),
    "B": ("Children's colouring book cover illustration: one adorable sleepy koala hugging a soft "
          "eucalyptus branch with round leaves, tiny stars and a crescent moon, soft dreamy pastel "
          "greens and blues, kawaii cute style, chunky rounded shapes, centred composition, "
          "professional kids book cover art. No text, no words, no letters, no watermark."),
    "C": ("Children's colouring book cover illustration: a sweet mother kangaroo with a smiling "
          "joey peeking out of her pouch in the Australian outback, warm orange sunset sky, red "
          "earth and two round bushes, kawaii cute style, chunky rounded shapes, centred "
          "composition, professional kids book cover art. No text, no words, no letters, no watermark."),
}

PALETTES = {
    "A": {"bg": (255, 250, 235), "title": (139, 90, 43), "sub": (60, 130, 90),  "border": (255, 200, 80)},
    "B": {"bg": (240, 248, 240), "title": (46, 110, 70),  "sub": (70, 100, 140), "border": (170, 215, 170)},
    "C": {"bg": (255, 244, 230), "title": (200, 90, 30),  "sub": (120, 70, 30),  "border": (250, 180, 120)},
}

def gen_hero(tag):
    path = os.path.join(CONCEPTS, "hero_%s.png" % tag)
    if os.path.exists(path) and os.path.getsize(path) > 10000 and "--regen" not in sys.argv:
        return path, "cached"
    r = subprocess.run([EXE, "generate", "image", HERO_PROMPTS[tag], "--model", MODEL,
                        "-o", path, "--quiet", "--yes"], capture_output=True, text=True, timeout=300)
    return path, "ok" if r.returncode == 0 else "FAIL " + (r.stderr or r.stdout)[-120:]

def assemble(tag):
    p = PALETTES[tag]
    canvas = Image.new("RGB", (W, H), p["bg"])
    d = ImageDraw.Draw(canvas)
    # playful double border frame (bestseller pattern)
    d.rounded_rectangle((70, 70, W-70, H-70), radius=90, outline=p["border"], width=22)
    d.rounded_rectangle((120, 120, W-120, H-120), radius=70, outline=p["border"], width=10)
    # coloured hero scene (OpenArt)
    hero = Image.open(os.path.join(CONCEPTS, "hero_%s.png" % tag)).convert("RGB")
    hero.thumbnail((1950, 1950), Image.LANCZOS)
    canvas.paste(hero, ((W - hero.width)//2, 720))
    # typeset title — two big lines (Baloo 2, never AI lettering)
    tf = ImageFont.truetype(FONT, 300)
    for line, y in (("Aussie", 220), ("Animals", 430)):
        bb = d.textbbox((0, 0), line, font=tf)
        d.text(((W-(bb[2]-bb[0]))//2 - bb[0], y), line, fill=p["title"], font=tf)
    # subtitle
    sf = ImageFont.truetype(FONT, 130)
    sub = "A Bold & Easy Colouring Book for Kids"
    bb = d.textbbox((0, 0), sub, font=sf)
    d.text(((W-(bb[2]-bb[0]))//2 - bb[0], 2750), sub, fill=p["sub"], font=sf)
    # age badge line
    af = ImageFont.truetype(FONT, 100)
    age = "Ages 3-8  |  50 Big & Bold Designs with Fun Facts"
    bb = d.textbbox((0, 0), age, font=af)
    d.text(((W-(bb[2]-bb[0]))//2 - bb[0], 2930), age, fill=p["sub"], font=af)
    # author + imprint
    bf = ImageFont.truetype(FONT, 95)
    auth = "Matilda Hayes  |  Gumleaf Kids Press"
    bb = d.textbbox((0, 0), auth, font=bf)
    d.text(((W-(bb[2]-bb[0]))//2 - bb[0], 3080), auth, fill=(120, 120, 120), font=bf)
    out = os.path.join(HERE, "cover_proposal_%s.png" % tag)
    canvas.save(out, dpi=(300, 300))
    canvas.resize((600, 776), Image.LANCZOS).save(os.path.join(HERE, "cover_small_%s.png" % tag))
    return out

def main():
    os.makedirs(CONCEPTS, exist_ok=True)
    tags = ["A", "B", "C"]
    if "--only" in sys.argv:
        tags = [t for t in sys.argv[sys.argv.index("--only")+1:] if t in "ABC"]
    for t in tags:
        path, status = gen_hero(t)
        print("hero", t, status, flush=True)
        if os.path.exists(path) and os.path.getsize(path) > 10000:
            print("cover", t, "->", assemble(t), flush=True)
        else:
            print("cover", t, "SKIPPED (no hero)", flush=True)
    if len(tags) == 3:
        panel = Image.new("RGB", (1900, 800), "white")
        for k, t in enumerate(("A", "B", "C")):
            panel.paste(Image.open(os.path.join(HERE, "cover_small_%s.png" % t)), (30 + k*630, 10))
        panel.save(os.path.join(HERE, "cover_proposals_panel.png"))
        print("panel -> cover_proposals_panel.png", flush=True)

if __name__ == "__main__":
    main()
