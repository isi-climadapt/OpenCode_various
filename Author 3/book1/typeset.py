# -*- coding: utf-8 -*-
# Author 3 Book 1 - Who Peeled My Tree? Typeset the 32 interior pages onto the page art.
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
    "p03": dict(blocks=[B(0.07, 0.765, 0.86, [
        "Way up high in the Australian bush, there is a gum tree.",
        "Way up high in the gum tree, there is a hollow.",
        "And in the hollow lives Banjo."], align="c", panel=True)]),
    "p04": dict(blocks=[B(0.07, 0.07, 0.31, [
        "Banjo is a sugar glider. He sleeps all day and plays all night.",
        "Every evening, he says good morning to his tree.",
        '"Good morning, trunk! Good morning, branches! Good morning, my big, smooth, beautiful tree!"'], panel=True)]),
    "p05": dict(blocks=[B(0.10, 0.07, 0.50, ["!!WHEEE!"])]),
    "p06": dict(blocks=[B(0.42, 0.06, 0.50, [
        "Banjo lands on the trunk with a soft *pat.*", "Then he sees it."])]),
    "p07": dict(vig=(0.78, 0.5, None), blocks=[B(0.10, 0.06, 0.80, [
        "!!HEY!", "Somebody has been PEELING my tree!"], align="c")]),
    "p08": dict(blocks=[B(0.12, 0.06, 0.76, [
        "Banjo scrambles up to the top branch.",
        '"Olive! OLIVE! Wake up!"',
        'Olive opens one eye. "Mmm?"',
        '"Somebody peeled my tree!"'], align="c", panel=True)]),
    "p09": dict(vig=(0.58, 0.5, 0.50), blocks=[
        B(0.10, 0.06, 0.80, ['"Gum trees do that, Banjo," says Olive.',
                             "And she closes her eye again."], align="c"),
        B(0.10, 0.80, 0.80, ['"Trees don\'t peel THEMSELVES," says Banjo. '
                             '"I\'m going to find out who did this."'], align="c")]),
    "p10": dict(blocks=[B(0.08, 0.06, 0.84, [
        "Cockatoo chews everything. Sticks. Seeds. Fence posts. Window frames.",
        '"Cockatoo! Did you chew my tree?"'], align="c", panel=True)]),
    "p11": dict(blocks=[B(0.08, 0.06, 0.84, [
        "!!SQUAWK!",
        '"It\'s the middle of the NIGHT! I do my chewing in the daytime, like a sensible bird."',
        '"Oh," says Banjo. "Sorry, Cockatoo."'], align="c", panel=True)]),
    "p12": dict(blocks=[B(0.08, 0.06, 0.84, [
        "The next night, there is MORE peeling.",
        "Long strips. Curly strips. Strips that go *flap, flap, flap* in the wind."], align="c")]),
    "p13": dict(vig=(1.0, 0.5, 0.5), blocks=[B(0.55, 0.38, 0.38, [
        '"This is serious," says Banjo.', '"This needs a detective."'])]),
    "p14": dict(blocks=[B(0.08, 0.06, 0.84, [
        "Possum has the softest bed in the whole bush. Suspiciously soft.",
        '"Possum! Is that MY bark in your bed?"'], align="c")]),
    "p15": dict(vig=(0.74, 0.5, None), blocks=[B(0.08, 0.06, 0.84, [
        "Possum pulls out leaves. Then feathers. Then one stripy sock.",
        '"I don\'t know where the sock came from," says Possum.',
        "No bark at all."], align="c")]),
    "p16": dict(blocks=[B(0.06, 0.34, 0.38, [
        "At the bottom of the tree, something is scratching.",
        "*Scritch. Scratch. Scritch.*", '"AH-HA! Caught you!"'], panel=True)]),
    "p17": dict(blocks=[B(0.50, 0.06, 0.44, [
        '"I\'m looking for ants," says Echidna. "Ants live down here, in the dirt."',
        "She points her long nose up, up, up.",
        '"Your peeling is way up THERE."'], panel=True)]),
    "p18": dict(blocks=[B(0.40, 0.06, 0.53, [
        "Then Wombat comes trundling by.",
        '"Wombat! Did you peel my tree?"',
        '"Wombats don\'t climb trees," says Wombat.'], panel=True)]),
    "p19": dict(vig=(0.72, 0.5, None), blocks=[B(0.10, 0.06, 0.80, [
        '"Not even if you stand on each other?"', '"ESPECIALLY not then."'], align="c")]),
    "p20": dict(blocks=[B(0.07, 0.06, 0.38, [
        "By the third night, the old bark is nearly all gone.",
        "Banjo's tree is patchy and blotchy and spotty all over."], panel=True)]),
    "p21": dict(blocks=[B(0.62, 0.08, 0.30, ['"My tree is ruined," whispers Banjo.'], panel=True)]),
    "p22": dict(blocks=[B(0.08, 0.06, 0.84, [
        "This time, Olive opens BOTH eyes.",
        '"Banjo," she says. "Nobody peeled your tree. Your tree peeled itself."',
        '"Trees can DO that?"',
        '"Gum trees can. When they grow bigger, the old bark gets too small. So they let it go."'],
        panel=True)]),
    "p23": dict(vig=(0.56, 0.5, None), blocks=[B(0.08, 0.06, 0.84, [
        '"Like when I got too big for my baby hollow?"',
        '"Just like that."',
        "Banjo touches the new bark.",
        "It is smooth. It is cool. It smells like peppermint and rain.",
        '"Oh," says Banjo. "It\'s NEW."'], align="c")]),
    "p24": dict(blocks=[B(0.48, 0.06, 0.46, [
        "Banjo says sorry to Cockatoo, Possum, Echidna and Wombat.",
        "And the old bark? Everybody finds a use for it."], panel=True)]),
    "p25": dict(vig=(0.72, 0.5, None), blocks=[B(0.10, 0.06, 0.80, [
        "Cockatoo gets something to chew.", "Possum gets a new blanket.",
        "Echidna finds beetles hiding underneath.", "Wombat gets a doormat."],
        align="c")]),
    "p26": dict(blocks=[B(0.52, 0.06, 0.40, ["But Banjo finds the best use of all."], panel=True)]),
    "p27": dict(blocks=[B(0.46, 0.06, 0.48, [
        "The new bark makes the smoothest, slipperiest, ZOOMIEST slide in the whole bush!",
        "!!WHEEE!"], align="c", panel=True)]),
    "p28": dict(blocks=[B(0.06, 0.06, 0.56, [
        "At sunrise, Kookaburra starts to laugh, and Banjo heads home to bed.",
        '"Good night, trunk. Good night, branches. Good night, my big, beautiful, SPOTTY tree."'],
        panel=True)]),
    "p29": dict(vig=(0.70, 0.5, None), blocks=[B(0.08, 0.06, 0.84, [
        "Banjo gives himself a good scratch. A tuft of fluffy fur floats away.",
        '"OLIVE! Somebody is peeling ME!"',
        '"Zzz," says Olive. "Gliders do that too."'], align="c")]),
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
    d.text((cx, oy + int(TRIM * 0.15)), "Who Peeled", font=chewy(230), fill=DARK, anchor="ms")
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
    d.text((cx, oy + int(TRIM * 0.36)), "For everyone who has ever", font=italic(76), fill=DARK, anchor="ms")
    d.text((cx, oy + int(TRIM * 0.40)), "outgrown something.", font=italic(76), fill=DARK, anchor="ms")
    small = font("Nunito[wght].ttf", 40, "Regular")
    lines = ["Who Peeled My Tree?",
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
    ("Why do gum trees peel?", "Many gum trees (eucalyptus) shed their old outer bark as the trunk grows "
     "wider. The new bark underneath can be cream, pink, green, orange or gray. Peeling may also help "
     "the tree get rid of moss, lichen and bugs."),
    ("Scribbly gums", "have squiggly lines on their bark. The squiggles are tunnels made by tiny moth "
     "caterpillars."),
    ("Sugar gliders", "sleep all day and come out at night. A sugar glider weighs about as much as a "
     "small apple. A stretchy flap of skin between its front and back legs lets it glide up to 150 feet "
     "(45 meters). Sugar gliders live in tree hollows in family groups and eat tree sap, nectar and insects."),
    ("Koalas", "sleep up to 20 hours a day and eat mostly eucalyptus leaves."),
    ("Cockatoos", "chew wood to keep their beaks in shape."),
    ("Echidnas", "catch ants and termites with a long, sticky tongue."),
    ("Brushtail possums", "sleep in tree hollows, and sometimes in people's roofs."),
    ("Wombats", "make poop shaped like cubes."),
    ("Furry animals shed too.", "Like most furry animals, sugar gliders lose old fur as new fur grows."),
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
    # left page (even): heading + Banjo spot, then the first three facts
    c = pages["p30"]; ox, oy = BLEED, BLEED
    d = ImageDraw.Draw(c)
    d.text((ox + SAFE + 10, oy + 380), "True Facts", font=head, fill=(176, 92, 52), anchor="ls")
    d.text((ox + SAFE + 10, oy + 560), "from the Bush", font=head, fill=(176, 92, 52), anchor="ls")
    sp = spot("p23", (0.15, 0.10, 0.90, 0.95)); sp.thumbnail((640, 640), Image.LANCZOS)
    feather_paste(c, sp, (ox + TRIM - SAFE - sp.width, oy + 90))
    end = facts_text(c, ox, oy, FACTS[:3], 860, SAFE + 10, TRIM - 2 * SAFE - 20)
    if end > TRIM - SAFE:
        print(f"  WARNING p30: facts run to y {end}, past the safe zone")
    # right page (odd): remaining facts, then four spots along the bottom
    c = pages["p31"]; ox, oy = 0, BLEED
    end = facts_text(c, ox, oy, FACTS[3:], SAFE + 90, SAFE + 10, TRIM - 2 * SAFE - 20)
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
        "Look out for more Banjo and Olive stories."], align="c", px=64)
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
