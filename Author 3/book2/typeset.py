# -*- coding: utf-8 -*-
# Author 3 Book 2 - Who Frosted My Tree? Typeset the 32 interior pages onto the page art.
# KDP: 8.5 x 8.5 in trim, bleed -> page 8.625 x 8.75 in at 300 DPI = 2588 x 2625 px.
# Odd pages are right-hand pages: gutter on the left, bleed on the right. Even pages: mirror.
# Text is laid out in trim-box fractions and must stay 0.5 in (150 px) inside the trim on all sides.
# Markup in paragraphs: "!!" prefix = big shout line (Chewy); *word* = italic; ALLCAPS words = Chewy.
# Usage: py typeset.py            -> typeset\pXX.png (all pages)
#        py typeset.py p04 p22    -> only these pages

import os, re, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PAGES_DIR = os.path.join(HERE, "pages")
OUT = os.path.join(HERE, "typeset")
FONTS = os.path.join(HERE, "fonts")

DPI = 300
TRIM = 2550                      # 8.5 in
BLEED = 38                       # 0.125 in (37.5 px, rounded up)
PAGE_W, PAGE_H = TRIM + BLEED, TRIM + 2 * BLEED   # 2588 x 2626 -> trimmed to 2625 below
PAGE_H = 2625
SAFE = 150                       # 0.5 in inside the trim

BODY_PX = 80                     # uniform body size on every story page (about 19 pt)
SHOUT_SCALE, INLINE_SCALE = 2.0, 1.22
DARK, LIGHT = (34, 36, 66), (255, 249, 236)
PANEL = (253, 248, 236)

def font(name, px, weight=None):
    f = ImageFont.truetype(os.path.join(FONTS, name), px)
    if weight:
        f.set_variation_by_name(weight)
    return f

def body(px=BODY_PX):   return font("Nunito[wght].ttf", px, "Bold")
def italic(px=BODY_PX): return font("Nunito-Italic[wght].ttf", px, "Bold Italic")
def chewy(px):          return ImageFont.truetype(os.path.join(FONTS, "Chewy-Regular.ttf"), px)

def smart(s):
    s = re.sub(r'(^|[\s(])"', "\\1\u201c", s)
    s = s.replace('"', "\u201d")
    return s.replace("'", "\u2019")

# ---------------------------------------------------------------- page specs
# block: x, y, w in trim fractions; align "l"/"c"; panel = soft cream box behind the text
def B(x, y, w, paras, align="l", panel=False, color=None, px=BODY_PX):
    return dict(x=x, y=y, w=w, paras=paras, align=align, panel=panel, color=color, px=px)

# vignette pages: art whitened to pure white, then scaled and placed (cx, cy = centre in trim fractions)
SPEC = {
    "p03": dict(blocks=[B(0.06, 0.17, 0.36, [
        "Way up high in the hills, there is a gum tree.",
        "It is winter in the hills. The nights are long, and the wind is cold."])]),
    "p04": dict(blocks=[B(0.07, 0.07, 0.34, [
        "Banjo is a sugar glider. He sleeps all day and plays all night.",
        "But tonight is SO cold that Banjo curls into a tight, fluffy ball."])]),
    "p05": dict(vig=(1.0, 0.5, 0.5), blocks=[B(0.10, 0.10, 0.80, [
        "He sleeps all night.", "And all day.", "And all night AGAIN."], align="c")]),
    "p06": dict(blocks=[B(0.06, 0.08, 0.27, [
        "When Banjo finally pokes his nose out, he can't believe his eyes."])]),
    "p07": dict(blocks=[B(0.40, 0.06, 0.54, [
        "!!HEY!", "Somebody has FROSTED my tree!", "Like a CAKE!"], align="c")]),
    "p08": dict(blocks=[B(0.20, 0.06, 0.76, [
        "Banjo scrambles up to the top branch.",
        '"Olive! OLIVE! Wake up!"',
        "There is a big white lump where Olive should be.",
        'The lump opens one eye. "Mmm?"'], align="c", panel=True)]),
    "p09": dict(vig=(0.48, 0.5, 0.52), blocks=[
        B(0.08, 0.06, 0.84, ['"It\'s snow, Banjo," says Olive.',
                             '"Snow doesn\'t happen HERE," says Banjo.',
                             '"Not often," says Olive. And she closes her eye again.'], align="c"),
        B(0.08, 0.79, 0.84, ['"Then somebody DID this," says Banjo. '
                             '"And I\'m going to find out who."'], align="c")]),
    "p10": dict(blocks=[B(0.08, 0.06, 0.84, [
        "Cockatoo is white. White feathers. White tail. White EVERYTHING.",
        "Very suspicious.",
        '"Cockatoo! Is all this white stuff YOURS?"'], align="c", panel=True)]),
    "p11": dict(blocks=[B(0.10, 0.05, 0.80, [
        "!!SQUAWK!",
        '"My feathers are ON me! All of them! Count them if you like!"',
        "Banjo counts to eleven and gives up.",
        '"Sorry, Cockatoo."'], align="c", panel=True)]),
    "p12": dict(blocks=[B(0.08, 0.06, 0.84, [
        "More white is falling from the sky.",
        "Banjo catches a piece.",
        "It sparkles. It tickles. And then it's GONE."], align="c")]),
    "p13": dict(vig=(1.0, 0.5, 0.5), blocks=[B(0.55, 0.38, 0.38, [
        '"Disappearing frosting," says Banjo.',
        '"This is serious. This needs a detective."'])]),
    "p14": dict(blocks=[B(0.08, 0.06, 0.84, [
        "Possum's face is white. All of it.",
        '"AH-HA! Caught you white-handed!"'], align="c", panel=True)]),
    "p15": dict(vig=(0.74, 0.5, None), blocks=[B(0.08, 0.06, 0.84, [
        '"I fell in it," says Possum. "Face first."',
        '"Once?"',
        '"Twice," says Possum. "Maybe three times."'], align="c")]),
    "p16": dict(blocks=[B(0.42, 0.06, 0.52, [
        "Then Wombat comes trundling by, pushing a giant white ball.",
        '"Wombat! What is THAT?"'], panel=True)]),
    "p17": dict(blocks=[B(0.46, 0.06, 0.48, [
        '"I went for a walk," says Wombat, "and it followed me."',
        "The ball gets bigger. And BIGGER.",
        '"I can\'t stop," says Wombat.'])]),
    "p18": dict(blocks=[B(0.44, 0.06, 0.50, [
        "Banjo knows who will help. Echidna lives by the old log.",
        "But the log is covered in snow.",
        "And Echidna is GONE."], panel=True)]),
    "p19": dict(vig=(0.72, 0.5, None), blocks=[B(0.10, 0.06, 0.80, [
        '"Somebody took Echidna!" cries Banjo.',
        '"Somebody frosted my tree AND took my friend!"'], align="c")]),
    "p20": dict(blocks=[B(0.07, 0.10, 0.46, [
        "The bush is white and quiet.",
        "No crunch. No chirp. No Echidna."], panel=True)]),
    "p21": dict(blocks=[B(0.50, 0.07, 0.44, [
        '"My tree is frosted," whispers Banjo. "My friend is missing. And my toes are FROZEN."'],
        panel=True)]),
    "p22": dict(blocks=[B(0.06, 0.05, 0.88, [
        "This time, Olive opens BOTH eyes. She climbs all the way down.",
        '"Banjo," she says. "Nobody frosted your tree. When the clouds get very, very cold, '
        'the rain turns into snow."',
        '"And Echidna?"'], panel=True)]),
    "p23": dict(vig=(0.60, 0.5, None), blocks=[B(0.07, 0.05, 0.86, [
        "Olive points to a small spiky bump in the snow. Under the bump, something is snoring.",
        '"Echidna is hibernating," says Olive. "She\'s sleeping through the cold. '
        'She\'ll wake up when it\'s warm again."',
        '"She\'s not missing," says Banjo. "She\'s just VERY asleep."'], align="c")]),
    "p24": dict(blocks=[B(0.34, 0.06, 0.58, [
        "Banjo says sorry to Cockatoo, Possum and Wombat.",
        "And the snow? Everybody finds a use for it."], panel=True)]),
    "p25": dict(vig=(0.72, 0.5, None), blocks=[B(0.10, 0.06, 0.80, [
        "Cockatoo makes snow angels.", "Possum makes a snow possum.",
        "Wombat's ball gets a gum-nut nose.",
        "And Echidna gets the coziest blanket in the bush."], align="c")]),
    "p26": dict(blocks=[B(0.50, 0.06, 0.42, ["But Banjo finds the best thing of all."], panel=True)]),
    "p27": dict(blocks=[B(0.08, 0.05, 0.84, [
        "Gliding through the snowflakes is the swooshiest, sparkliest, FROSTIEST glide in the whole bush!",
        "!!WHEEE!"], align="c", panel=True)]),
    "p28": dict(blocks=[B(0.06, 0.06, 0.39, [
        "At sunrise, Banjo heads home to bed.",
        '"Good night, trunk. Good night, branches. Good night, my big, beautiful, FROSTED tree."'])]),
    "p29": dict(vig=(0.62, 0.5, None), blocks=[B(0.08, 0.05, 0.84, [
        "A lump of snow slides off a branch. FLUMP! Right on top of Olive.",
        '"OLIVE! Somebody frosted YOU!"',
        '"Zzz," says Olive. "Wake me up in spring."'], align="c")]),
}

# ---------------------------------------------------------------- rich text layout
def tokens(para, px):
    """Split a paragraph into (word, font) runs. Returns (runs, is_shout)."""
    if para.startswith("!!"):
        return [(w, chewy(int(px * SHOUT_SCALE))) for w in smart(para[2:]).split()], True
    runs, ital = [], False
    for w in smart(para).split():
        start, end = w.startswith("*"), w.endswith("*") or w.endswith("*.") or w.endswith("*,")
        clean = w.replace("*", "")
        if start:
            ital = True
        core = re.sub(r"[^A-Za-z]", "", clean)
        if len(core) >= 2 and core.isupper():
            f = chewy(int(px * INLINE_SCALE))
        else:
            f = italic(px) if ital else body(px)
        runs.append((clean, f))
        if end:
            ital = False
    return runs, False

def layout(block, trim_w):
    """Return list of lines; each line = (width, ascent, descent, [(word, font, x)])."""
    px = block["px"]
    maxw = int(block["w"] * trim_w)
    space = body(px).getlength(" ")
    lines = []
    for i, para in enumerate(block["paras"]):
        runs, shout = tokens(para, px)
        cur, x = [], 0
        for word, f in runs:
            wl = f.getlength(word)
            if cur and x + space + wl > maxw:
                lines.append(cur)
                cur, x = [], 0
            cur.append((word, f, x + (space if cur else 0)))
            x = cur[-1][2] + wl
        lines.append(cur)
        if i < len(block["paras"]) - 1:
            lines.append("gap")
    out = []
    for ln in lines:
        if ln == "gap":
            out.append((0, int(px * 0.32), 0, []))
            continue
        asc = max(f.getmetrics()[0] for _, f, _ in ln)
        desc = max(f.getmetrics()[1] for _, f, _ in ln)
        w = ln[-1][2] + ln[-1][1].getlength(ln[-1][0])
        out.append((w, asc, desc, ln))
    return out

def region_luma(img, box):
    crop = img.crop(box).convert("L").resize((32, 32))
    px = list(crop.get_flattened_data())
    return sum(px) / len(px) / 255.0

def draw_block(canvas, block, ox, oy, page_id):
    lines = layout(block, TRIM)
    lead = 1.12
    total_h = sum(int((a + d) * lead) for _, a, d, _ in lines)
    maxw = int(block["w"] * TRIM)
    bx, by = ox + int(block["x"] * TRIM), oy + int(block["y"] * TRIM)
    widest = max(w for w, _, _, _ in lines)
    # safe-zone check (trim-relative)
    x0 = bx - ox + ((maxw - widest) // 2 if block["align"] == "c" else 0)
    if x0 < SAFE or x0 + widest > TRIM - SAFE or by - oy < SAFE * 0.8 or by - oy + total_h > TRIM - SAFE:
        print(f"  WARNING {page_id}: text outside the 0.5 in safe zone "
              f"(x {x0}-{x0 + widest}, y {by - oy}-{by - oy + total_h})")
    if block["panel"]:
        pad = 50
        if block["align"] == "c":
            px0 = bx + (maxw - widest) // 2 - pad
        else:
            px0 = bx - pad
        rect = (px0, by - pad, px0 + widest + 2 * pad, by + total_h + pad)
        mask = Image.new("L", canvas.size, 0)
        ImageDraw.Draw(mask).rounded_rectangle(rect, radius=60, fill=232)
        mask = mask.filter(ImageFilter.GaussianBlur(14))
        canvas.paste(Image.new("RGB", canvas.size, PANEL), (0, 0), mask)
        color = DARK
    else:
        luma = region_luma(canvas, (bx, by, bx + maxw, by + total_h))
        color = block["color"] or (DARK if luma > 0.55 else LIGHT)
    # soft shadow behind light text for legibility on paintings
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    d, ds = ImageDraw.Draw(layer), ImageDraw.Draw(shadow)
    y = by
    for w, a, dsc, ln in lines:
        base = y + a
        xoff = bx + ((maxw - w) // 2 if block["align"] == "c" else 0)
        for word, f, x in ln:
            d.text((xoff + x, base), word, font=f, fill=color + (255,), anchor="ls")
            if color == LIGHT:
                ds.text((xoff + x + 3, base + 4), word, font=f, fill=(20, 18, 40, 200), anchor="ls")
        y += int((a + dsc) * lead)
    if color == LIGHT:
        canvas.paste(shadow.filter(ImageFilter.GaussianBlur(6)), (0, 0), shadow.filter(ImageFilter.GaussianBlur(6)))
    canvas.paste(layer, (0, 0), layer)

# ---------------------------------------------------------------- art placement
def whiten(img):
    """Scale channels so the vignette's off-white paper becomes pure white."""
    w, h = img.size
    band = [img.getpixel((x, y)) for x in range(0, w, 16) for y in (4, h - 5)] + \
           [img.getpixel((x, y)) for y in range(0, h, 16) for x in (4, w - 5)]
    bg = [sorted(c[i] for c in band)[len(band) // 2] for i in range(3)]
    lut = []
    for i in range(3):
        k = 255.0 / max(bg[i], 1)
        lut += [min(255, int(v * k + 0.5)) for v in range(256)]
    return img.point(lut)

def feather_paste(canvas, art, xy, edge=0.07):
    """Paste a whitened vignette with its outer edge faded to transparent, so no box edge shows
    where the painted paper texture meets the white page."""
    import numpy as np
    w, h = art.size
    e = max(1, int(min(w, h) * edge))
    xs = np.minimum(np.arange(w), np.arange(w)[::-1]) / e
    ys = np.minimum(np.arange(h), np.arange(h)[::-1]) / e
    a = np.clip(np.minimum.outer(ys, xs), 0, 1)
    a = a * a * (3 - 2 * a)                       # smoothstep
    canvas.paste(art, xy, Image.fromarray((a * 255).astype("uint8"), "L"))

def page_canvas(pid):
    n = int(pid[1:])
    ox = 0 if n % 2 else BLEED            # trim box x offset (even pages carry bleed on the left)
    oy = BLEED
    canvas = Image.new("RGB", (PAGE_W, PAGE_H), "white")
    art_path = os.path.join(PAGES_DIR, pid + ".png")
    spec = SPEC.get(pid, {})
    if os.path.exists(art_path):
        art = Image.open(art_path).convert("RGB")
        if "vig" in spec:
            scale, cx, cy = spec["vig"]   # cy=None: sit the art on the bottom safe line
            art = whiten(art)
            side = int(TRIM * scale)
            art = art.resize((side, side), Image.LANCZOS)
            top = oy + (TRIM - side - 60 if cy is None else int(cy * TRIM) - side // 2)
            feather_paste(canvas, art, (ox + int(cx * TRIM) - side // 2, top))
        else:
            side = PAGE_H                  # cover the whole bleed page
            art = art.resize((side, side), Image.LANCZOS)
            canvas.paste(art, ((PAGE_W - side) // 2, 0))
    return canvas, ox, oy

# ---------------------------------------------------------------- special pages
def title_page():
    canvas, ox, oy = page_canvas("p01")
    canvas = Image.new("RGB", (PAGE_W, PAGE_H), "white")
    art = whiten(Image.open(os.path.join(PAGES_DIR, "p01.png")).convert("RGB"))
    side = int(TRIM * 0.56)
    art = art.resize((side, side), Image.LANCZOS)
    feather_paste(canvas, art, (ox + (TRIM - side) // 2, oy + int(TRIM * 0.30)))
    d = ImageDraw.Draw(canvas)
    cx = ox + TRIM // 2
    d.text((cx, oy + int(TRIM * 0.15)), "Who Frosted", font=chewy(230), fill=DARK, anchor="ms")
    d.text((cx, oy + int(TRIM * 0.255)), "My Tree?", font=chewy(230), fill=DARK, anchor="ms")
    d.text((cx, oy + int(TRIM * 0.92)), "Hattie Moss", font=body(96), fill=DARK, anchor="ms")
    d.text((cx, oy + int(TRIM * 0.96)), "Saltbush Story House", font=font("Nunito[wght].ttf", 52, "SemiBold"),
           fill=(110, 112, 130), anchor="ms")
    return canvas

def copyright_page():
    canvas = Image.new("RGB", (PAGE_W, PAGE_H), "white")
    ox, oy = BLEED, BLEED
    d = ImageDraw.Draw(canvas)
    cx = ox + TRIM // 2
    d.text((cx, oy + int(TRIM * 0.36)), "For everyone who has waited", font=italic(76), fill=DARK, anchor="ms")
    d.text((cx, oy + int(TRIM * 0.40)), "all year for the first snow.", font=italic(76), fill=DARK, anchor="ms")
    small = font("Nunito[wght].ttf", 40, "Regular")
    lines = ["Who Frosted My Tree?",
             "Text and illustrations copyright \u00a9 2026 Hattie Moss.",
             "All rights reserved. No part of this book may be reproduced in any form",
             "without written permission from the publisher, except for brief quotations in reviews.",
             "Published by Saltbush Story House.",
             "First edition, 2026."]
    y = oy + int(TRIM * 0.74)
    for ln in lines:
        d.text((ox + SAFE + 20, y), ln, font=small, fill=(70, 72, 90), anchor="ls")
        y += 60
    return canvas

FACTS = [
    ("Australia gets snow.", "Snow falls every winter in the Australian Alps, and now and then on "
     "hills and high plains further down."),
    ("Snow gums", "are gum trees that grow high in the snowy mountains. Their bark peels into stripes "
     "of white, gray, green, orange and red."),
    ("Snowflakes", "form when water freezes high in cold clouds. Most snowflakes have six sides."),
    ("Echidnas hibernate.", "In the coldest places, an echidna can sleep through winter for months. "
     "Its body cools right down and its heart beats very slowly."),
    ("Mountain pygmy possums", "hibernate under the snow in the Australian Alps for up to seven months."),
    ("Sugar gliders", "curl up together in their tree hollows to keep warm. On very cold nights they "
     "can drop into a deep sleep called torpor, and save energy."),
    ("Koalas", "have thick, woolly fur that keeps out cold and rain."),
    ("Wombats", "stay warm in deep burrows under the ground."),
    ("Cockatoos", "fluff up their feathers to trap warm air."),
]
CREAM = (250, 244, 228)

def spot(pid, box_frac):
    """Crop a spot illustration from a vignette page (box in fractions of the 2048 art)."""
    art = whiten(Image.open(os.path.join(PAGES_DIR, pid + ".png")).convert("RGB"))
    W = art.width
    return art.crop(tuple(int(v * W) for v in box_frac))

def facts_pages():
    """Pages 30 (left) and 31 (right): white pages, heading, facts, spot art cropped from the story
    vignettes (p23 Banjo, p25 cockatoo/possum/echidna/wombat), edges feathered into white."""
    pages = {pid: Image.new("RGB", (PAGE_W, PAGE_H), "white") for pid in ("p30", "p31")}
    spots_right = [("p25", (0.0, 0.0, 0.5, 0.5)), ("p25", (0.5, 0.0, 1.0, 0.5)),
                   ("p25", (0.0, 0.5, 0.5, 1.0)), ("p25", (0.5, 0.5, 1.0, 1.0))]
    head = chewy(170)
    bold, reg = body(70), font("Nunito[wght].ttf", 70, "Regular")
    def facts_text(canvas, ox, oy, items, y0, x0, w):
        d = ImageDraw.Draw(canvas)
        y = oy + y0
        sp = reg.getlength(" ")
        for title, text in items:
            words = [(t, bold) for t in title.split()] + [(t, reg) for t in text.split()]
            line, x, rows = [], 0, []
            for word, f in words:
                wl = f.getlength(word)
                if line and x + sp + wl > w:
                    rows.append(line); line, x = [], 0
                line.append((word, f, x + (sp if line else 0))); x = line[-1][2] + wl
            rows.append(line)
            for row in rows:
                for word, f, xx in row:
                    d.text((ox + x0 + xx, y), word, font=f, fill=DARK, anchor="ls")
                y += 96
            y += 48
        return y - oy
    # left page (even): heading + Banjo spot, then the first four facts
    c = pages["p30"]; ox, oy = BLEED, BLEED
    d = ImageDraw.Draw(c)
    d.text((ox + SAFE + 10, oy + 380), "True Facts", font=head, fill=(176, 92, 52), anchor="ls")
    d.text((ox + SAFE + 10, oy + 560), "from the Bush", font=head, fill=(176, 92, 52), anchor="ls")
    sp = spot("p23", (0.15, 0.10, 0.90, 0.95)); sp.thumbnail((640, 640), Image.LANCZOS)
    feather_paste(c, sp, (ox + TRIM - SAFE - sp.width, oy + 90))
    end = facts_text(c, ox, oy, FACTS[:4], 860, SAFE + 10, TRIM - 2 * SAFE - 20)
    if end > TRIM - SAFE:
        print(f"  WARNING p30: facts run to y {end}, past the safe zone")
    # right page (odd): remaining facts, then four spots along the bottom
    c = pages["p31"]; ox, oy = 0, BLEED
    end = facts_text(c, ox, oy, FACTS[4:], SAFE + 90, SAFE + 10, TRIM - 2 * SAFE - 20)
    size = 500                                   # 2 x 2 grid of spots under the facts
    gx = ox + (TRIM - 2 * size - 60) // 2
    gy = oy + TRIM - SAFE - 2 * size - 40
    if end > gy - oy - 30:
        print(f"  WARNING p31: facts (to y {end}) collide with the spot art grid")
    for i, (pid, box) in enumerate(spots_right):
        sp = spot(pid, box); sp.thumbnail((size, size), Image.LANCZOS)
        feather_paste(c, sp, (gx + (i % 2) * (size + 60), gy + (i // 2) * (size + 40)), edge=0.05)
    return pages

def about_page():
    canvas, ox, oy = page_canvas("p32")
    canvas = Image.new("RGB", (PAGE_W, PAGE_H), "white")
    art = whiten(Image.open(os.path.join(PAGES_DIR, "p32.png")).convert("RGB"))
    side = int(TRIM * 0.40)
    art = art.resize((side, side), Image.LANCZOS)
    feather_paste(canvas, art, (ox + (TRIM - side) // 2, oy + int(TRIM * 0.12)))
    blk = B(0.16, 0.60, 0.68, [
        "Hattie Moss writes funny picture books about Australian animals. She thinks gum trees are "
        "the best trees and sugar gliders are the best gliders.",
        "Look out for more Banjo and Olive stories, starting with *Who Peeled My Tree?*"], align="c", px=64)
    draw_block(canvas, blk, ox, oy, "p32")
    d = ImageDraw.Draw(canvas)
    d.text((ox + TRIM // 2, oy + int(TRIM * 0.55)), "About the Author", font=chewy(110), fill=DARK, anchor="ms")
    d.text((ox + TRIM // 2, oy + TRIM - SAFE), "Saltbush Story House",
           font=font("Nunito[wght].ttf", 52, "SemiBold"), fill=(110, 112, 130), anchor="ms")
    return canvas

# ---------------------------------------------------------------- main
def build(pid):
    if pid == "p01":
        return title_page()
    if pid == "p02":
        return copyright_page()
    if pid == "p32":
        return about_page()
    canvas, ox, oy = page_canvas(pid)
    for blk in SPEC[pid]["blocks"]:
        draw_block(canvas, blk, ox, oy, pid)
    return canvas

def main():
    os.makedirs(OUT, exist_ok=True)
    want = sys.argv[1:] or [f"p{n:02d}" for n in range(1, 33)]
    facts = None
    for pid in want:
        if pid in ("p30", "p31"):
            facts = facts or facts_pages()
            img = facts[pid]
        else:
            img = build(pid)
        img.save(os.path.join(OUT, pid + ".png"), dpi=(DPI, DPI))
        print(pid, img.size)

if __name__ == "__main__":
    main()
