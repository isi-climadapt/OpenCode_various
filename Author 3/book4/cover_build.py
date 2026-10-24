# -*- coding: utf-8 -*-
# Author 3 Book 4 - Who Took My Pouch? front cover options builder.
# Copied from book3\cover_build.py (rule 15; newest Author 3 cover): full-bleed painting, solid
# one-line title on a soft band, "Ages 3-5" badge bottom-left (rule 16), author along the bottom.
# Same band, type and badge as the Banjo books so Hattie Moss reads as one look; golden grassland
# palette and a sky-blue band for the new Clover and Hugo series.
# Hero art: hybrid pipeline from gen_pages.py (nano-banana-pro draft, ideogram-4-5 refine to 2048 px).
# Usage: py cover_build.py --gen        (draft heroes A/B/C via nano-banana-pro, then build options)
#        py cover_build.py --refine A   (refine hero A to 2048 px with ideogram, rebuild)
#        py cover_build.py              (build options from whatever heroes exist)

import os, sys, subprocess, time
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")
EXE = r"C:\Users\ibian\AppData\Local\Programs\openart\bin\openart.exe"
SHEET = os.path.join(HERE, "char_test", "sheet_hero.png")       # Clover, Hugo
EXTRA = os.path.join(HERE, "char_test", "sheet_extra.png")      # Mom, the baby, Pelican
CAST = os.path.join(HERE, "..", "book1", "char_test", "sheet_cast.png")   # wombat, possum, echidna

# front panel incl. bleed: trim 2550 x 2550, bleed on the outer (right), top and bottom edges
TRIM, BLEED = 2550, 38
W, H = TRIM + BLEED, TRIM + 2 * BLEED - 1      # 2588 x 2625
NIGHT = (34, 72, 120)        # band colour: deep sky blue (Banjo books use twilight indigo)
TITLE = (255, 222, 120)
CREAM = (255, 249, 236)
BADGE = (214, 98, 52)
MIN_DPI = 230   # full-bleed 8.75 in from 2048 px art = 234 DPI (CLI is capped at 2K; see BOOK1-PLAN)

STYLE = ("Children's picture book cover illustration. Soft gouache and colored-pencil look with "
         "visible paper grain, rounded chunky character shapes, gentle line work. Sunny Australian "
         "grassland palette of golden grass, warm red-ochre earth, eucalyptus sage greens and a "
         "clear blue sky, with cream and pink gum-tree bark. Friendly and funny. Full-bleed square "
         "painting to every edge, no border, no frame. No words, letters, numbers or text anywhere.")
SKY = ("The top quarter of the picture is open clear blue sky, empty, for the title, painted "
       "with the same soft texture and continuous with the scene: no hard edge, no flat band.")
CLOVER = ("Clover the young kangaroo joey (warm caramel-fawn fur, cream belly and cheeks, very big "
          "upright pink-lined ears, huge glossy dark brown eyes, small black nose, one tuft of fur "
          "on top of her head, long feet, long thick tail)")
HUGO = "Hugo the quokka (small round brown-gray wallaby, wide happy smile, rosy cheeks)"
MOM = "Clover's mom, a tall gray-fawn kangaroo with a kind face and a pouch on her tummy"

# Round 1 (24 Oct): the user picked layout A but didn't want Clover looking mad. Round 2 keeps
# A's layout (Clover big in front, Mom with the baby peeking out behind, Hugo at the side) with a
# friendly Clover. Round 1 drafts are in rejects\cover_round1.
BEHIND = (f"Behind her, {MOM} stands with a tiny baby kangaroo's head and little ears peeking out "
          f"of her pouch. {HUGO} sits in the grass at the side, smiling. Gum trees and red earth. ")
HERO_PROMPTS = {
    "A": (f"{CLOVER}, large in the picture, standing in tall golden grass, looking back over her "
          "shoulder at the baby with a big surprised, curious face: eyebrows up, mouth in a small "
          "round 'oh', ears straight up, one paw lifted. Sweet and funny, not angry. " + BEHIND + SKY),
    "B": (f"{CLOVER}, large in the picture, standing in tall golden grass facing the viewer with "
          "a puzzled, comic face: head tilted, one ear flopped sideways, paws spread wide as if "
          "asking 'where did it go?', a small smile. Friendly, not angry. " + BEHIND + SKY),
    "C": (f"{CLOVER}, large in the picture, standing in tall golden grass facing the viewer with "
          "a big happy grin and bright eyes, one paw pointing back over her shoulder at the baby "
          "peeking out of the pouch. Cheerful and warm. " + BEHIND + SKY),
}
REFS = {"A": [SHEET, EXTRA], "B": [SHEET, EXTRA], "C": [SHEET, EXTRA]}

def save(img, path):
    for a in range(4):
        try:
            img.save(path, dpi=(300, 300)); return
        except OSError:
            time.sleep(2 * (a + 1))
    raise OSError(path)

def run(model, prompt, path, refs):
    cmd = [EXE, "generate", "image", prompt, "--model", model, "-o", path, "--quiet", "--yes"]
    for r in refs:
        cmd += ["--image", r]
    for a in range(3):
        if a:
            time.sleep(20)
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
        if p.returncode == 0:
            return "ok"
    return "FAIL " + (p.stderr or p.stdout)[-200:]

def gen_draft(tag):
    path = os.path.join(HERE, f"cover_hero_{tag}_draft.png")
    if os.path.exists(path) and os.path.getsize(path) > 10000:
        return path, "cached"
    lead = ("Use the attached character sheets as the exact design for every character, not as a "
            "layout: each character appears only once. Square picture book cover. ")
    return path, run("nano-banana-pro", lead + HERO_PROMPTS[tag] + " " + STYLE, path, REFS[tag])

def refine(tag):
    draft = os.path.join(HERE, f"cover_hero_{tag}_draft.png")
    path = os.path.join(HERE, f"cover_hero_{tag}.png")
    lead = ("Repaint the first image at high detail, keeping its exact composition, poses and facial "
            "expressions. Keep every character exactly like the character sheets in the other "
            "attached images, each appearing only once. The scene: ")
    return path, run("ideogram-4-5", lead + HERO_PROMPTS[tag] + " " + STYLE, path, [draft] + REFS[tag])

def font(name, px, weight=None):
    f = ImageFont.truetype(os.path.join(FONTS, name), px)
    if weight:
        f.set_variation_by_name(weight)
    return f

def centred(d, text, fnt, cx, y, fill, **kw):
    d.text((cx, y), text, font=fnt, fill=fill, anchor="ms", **kw)

def build_front(tag):
    hero_path = os.path.join(HERE, f"cover_hero_{tag}.png")
    if not os.path.exists(hero_path):
        hero_path = os.path.join(HERE, f"cover_hero_{tag}_draft.png")   # layout preview only
    hero = Image.open(hero_path).convert("RGB")
    dpi = hero.width / (H / 300.0)
    note = "" if dpi >= MIN_DPI else "  (draft resolution, preview only)"
    print(f"{os.path.basename(hero_path)}: {hero.width} px -> {dpi:.0f} DPI full bleed{note}")
    canvas = hero.resize((H, H), Image.LANCZOS).crop(((H - W) // 2, 0, (H - W) // 2 + W, H))
    cx = TRIM // 2                                   # trim box starts at x 0 (spine side)

    # sky band behind the title, fading into the painted sky (no hard edge)
    band_h = 640
    shade = Image.new("RGB", (W, band_h), NIGHT)
    mask = Image.linear_gradient("L").resize((W, band_h)).point(lambda v: int((255 - v) * 0.86))
    canvas.paste(shade, (0, 0), mask)
    d = ImageDraw.Draw(canvas)

    # title: solid colour, one line, as large as fits inside the safe width
    title, size = "Who Took My Pouch?", 300
    f_t = font("Chewy-Regular.ttf", size)
    while d.textlength(title, font=f_t) > TRIM - 2 * 150 - 40:
        size -= 4
        f_t = font("Chewy-Regular.ttf", size)
    centred(d, title, f_t, cx, BLEED + 150 + int(size * 0.80), TITLE,
            stroke_width=6, stroke_fill=(30, 26, 66))

    # author name along the bottom, light with a soft dark glow for any background
    f_a = font("Nunito[wght].ttf", 120, "ExtraBold")
    glow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    ImageDraw.Draw(glow).text((cx, BLEED + TRIM - 175), "Hattie Moss", font=f_a,
                              fill=(20, 18, 50, 230), anchor="ms")
    glow = glow.filter(ImageFilter.GaussianBlur(18))
    canvas.paste(glow, (0, 0), glow)
    d = ImageDraw.Draw(canvas)
    centred(d, "Hattie Moss", f_a, cx, BLEED + TRIM - 175, CREAM)

    # age badge (replaces the coloring-book band): round, bottom-left corner inside the safe zone,
    # clear of the characters (Book 3 note: top-right covered characters in the drafts)
    r = 165
    bx, by = 150 + r, BLEED + TRIM - 150 - r
    d.ellipse((bx - r, by - r, bx + r, by + r), fill=BADGE, outline=CREAM, width=12)
    centred(d, "AGES", font("Nunito[wght].ttf", 70, "Black"), bx, by - 10, CREAM)
    centred(d, "3-5", font("Chewy-Regular.ttf", 130), bx, by + 108, CREAM)

    out = os.path.join(HERE, f"cover_option_{tag}.png")
    save(canvas, out)
    return out

def panel(paths):
    tw = 700
    p = Image.new("RGB", (tw * len(paths) + 40 * (len(paths) + 1), tw + 80 + 240), "white")
    for i, path in enumerate(paths):
        im = Image.open(path).resize((tw, int(tw * H / W)), Image.LANCZOS)
        p.paste(im, (40 + i * (tw + 40), 40))
        thumb = Image.open(path).resize((160, int(160 * H / W)), Image.LANCZOS)   # search-result size
        p.paste(thumb, (40 + i * (tw + 40), tw + 100))
    out = os.path.join(HERE, "cover_options_panel.png")
    save(p, out)
    return out

if __name__ == "__main__":
    if "--gen" in sys.argv:
        for t in "ABC":
            print("draft", t, gen_draft(t)[1], flush=True)
    if "--refine" in sys.argv:
        t = sys.argv[sys.argv.index("--refine") + 1]
        print("refine", t, refine(t)[1], flush=True)
    built = [build_front(t) for t in "ABC"
             if os.path.exists(os.path.join(HERE, f"cover_hero_{t}_draft.png"))]
    print("panel:", panel(built))
