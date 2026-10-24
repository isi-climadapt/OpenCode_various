# -*- coding: utf-8 -*-
# Author 3 Book 3 - Who Shook My Tree? Typeset (copied from book2\typeset.py, rule 15) the 32 interior pages onto the page art.
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
    "p03": dict(blocks=[B(0.06, 0.30, 0.40, [
        "Way up high in the hills, there is a gum tree.",
        "It is summer in the hills. The night is hot, and the air is sticky and still."])]),
    "p04": dict(blocks=[B(0.10, 0.07, 0.80, [
        "Banjo is a sugar glider. He sleeps all day and plays all night.",
        "Tonight, Banjo has a plan: his BIGGEST glide ever, right across the gully."], align="c")]),
    "p05": dict(vig=(1.0, 0.5, 0.5), blocks=[B(0.10, 0.10, 0.80, [
        "He fluffs his fur.", "He wiggles his toes.", 'He counts. "One. Two. Thr..."'], align="c")]),
    "p06": dict(blocks=[B(0.06, 0.10, 0.44, ["!!BOOM!"], align="c", px=150)]),
    "p07": dict(blocks=[B(0.40, 0.12, 0.54, [
        "The whole tree SHAKES.", "A big white light FLASHES across the bush.",
        "And then everything goes drip. Drip. DRIP."], align="c", panel=True)]),
    "p08": dict(blocks=[B(0.10, 0.06, 0.80, [
        "Banjo scrambles up to Olive.",
        '"Olive! OLIVE! Did you feel that?"',
        'Olive is hugging the trunk, eyes shut. "Mmm. It\'s a storm, Banjo."'], align="c", panel=True)]),
    "p09": dict(vig=(0.52, 0.5, 0.53), blocks=[
        B(0.08, 0.06, 0.84, ['"Storms don\'t SHAKE trees," says Banjo. "SOMEBODY shook my tree. '
                             'And I\'m going to find out who."'], align="c"),
        B(0.08, 0.82, 0.84, ['"Mmm," says Olive, and hugs her tree a little tighter.'], align="c")]),
    "p10": dict(blocks=[B(0.08, 0.06, 0.84, [
        "Down at the bottom of the tree, something RUMBLES.",
        "It's Wombat!",
        '"Wombat! Did you shake my tree?"'], align="c", panel=True)]),
    "p11": dict(blocks=[B(0.10, 0.05, 0.80, [
        "!!RUMBLE,", "goes Wombat's tummy.",
        '"I missed my dinner," says Wombat. "My tummy goes RUMBLE. It doesn\'t go BOOM."',
        '"Sorry, Wombat."'], align="c", panel=True)]),
    "p12": dict(blocks=[B(0.08, 0.06, 0.84, [
        "!!FLASH!", "For a moment, the whole bush turns white.",
        "Up on a branch, Cockatoo spreads her big white wings.",
        '"AH-HA! YOU did the FLASH!"'], align="c", panel=True)]),
    "p13": dict(vig=(0.62, 0.5, None), blocks=[B(0.08, 0.06, 0.84, [
        "!!SQUAWK!", '"I was STRETCHING," says Cockatoo.',
        "She folds her wings. And the sky goes FLASH all by itself.",
        '"Sorry, Cockatoo."'], align="c")]),
    "p14": dict(blocks=[B(0.08, 0.06, 0.84, [
        "THUMP. THUMP. THUMP. Somebody is banging on the bark.",
        '"Possum! Stop thumping my tree!"'], align="c", panel=True)]),
    "p15": dict(vig=(0.66, 0.5, None), blocks=[B(0.08, 0.06, 0.84, [
        '"I\'m not thumping," says Possum, from deep in a hollow. "I\'m SHAKING. That BOOM is scary!"',
        "Knock, knock, knock, go his knees.",
        '"Sorry, Possum."'], align="c")]),
    "p16": dict(blocks=[B(0.08, 0.06, 0.84, [
        "Then the rain comes. Big, fat, splashy drops.",
        "Banjo's fur is wet. His tail is wet. Even his EARS are wet."], align="c", panel=True)]),
    "p17": dict(blocks=[B(0.06, 0.07, 0.44, [
        '"This is serious," says Banjo. "Somebody shook my tree AND made it RAIN on me."'],
        panel=True)]),
    "p18": dict(blocks=[B(0.08, 0.06, 0.84, [
        "Then, from a low branch, comes a voice.",
        "!!BOOM!",
        "It's a bird with a long, swirly tail.",
        '"BOOM! BOOM!" "GOTCHA!" shouts Banjo.'], align="c")]),
    "p19": dict(vig=(0.62, 0.5, None), blocks=[B(0.08, 0.05, 0.84, [
        '"I\'m Lyrebird," he says. "I copy sounds."',
        '"SQUAWK!" Just like Cockatoo. "RUMBLE!" Just like Wombat\'s tummy.',
        '"And I copied BOOM from the SKY."',
        "BOOM, goes the sky. Lyrebird's beak is shut."], align="c")]),
    "p20": dict(blocks=[B(0.07, 0.10, 0.46, [
        "Everybody is hiding. The bush is dark and wet and LOUD."], panel=True)]),
    "p21": dict(blocks=[B(0.50, 0.07, 0.44, [
        '"Somebody is shaking my tree," whispers Banjo. "And I can\'t find out who. '
        'And I\'m a little bit SCARED."'], panel=True)]),
    "p22": dict(blocks=[B(0.06, 0.05, 0.88, [
        "This time, Olive opens BOTH eyes. She climbs down and wraps Banjo in a big, fluffy hug.",
        '"Nobody shook your tree," she says. "It\'s a thunderstorm. The flash is lightning. '
        'The BOOM is thunder. And the wind shakes every tree."'], panel=True)]),
    "p23": dict(vig=(0.56, 0.5, None), blocks=[B(0.07, 0.05, 0.86, [
        '"Here\'s a trick," says Olive. "When you see a flash, count until the BOOM."',
        'FLASH! "One gum tree, two gum tree..." BOOM!',
        'FLASH! "One gum tree, two gum tree, three, four, five..." boom.',
        '"Bigger numbers mean the storm is going away."'], align="c")]),
    "p24": dict(blocks=[B(0.10, 0.06, 0.80, [
        "Banjo says sorry to Wombat, Cockatoo, Possum and Lyrebird.",
        "Then everybody squeezes into Wombat's burrow, safe and dry."], align="c", panel=True)]),
    "p25": dict(vig=(0.64, 0.5, None), feather=0.14, blocks=[B(0.10, 0.06, 0.80, [
        "Wombat counts on his toes.", "Cockatoo counts on her feathers.",
        "Possum counts with his eyes shut tight.",
        "And Lyrebird counts in Olive's voice."], align="c")]),
    "p26": dict(blocks=[B(0.06, 0.06, 0.88, [
        "Slowly, the storm rumbles away over the hills. The moon comes out. In every puddle, frogs "
        "begin to sing.",
        'Banjo climbs to the top of his tree. "One. Two. THREE!"'], align="c", panel=True)]),
    "p27": dict(blocks=[B(0.08, 0.05, 0.84, [
        "It's the BIGGEST, swooshiest, sparkliest glide EVER, right across the gully!",
        "!!WHEEE!"], align="c", panel=True)]),
    "p28": dict(blocks=[B(0.06, 0.06, 0.88, [
        "At sunrise, Banjo heads home to bed.",
        '"Good night, trunk. Good night, branches. Good night, my big, beautiful, SHAKY tree."'],
        align="c", panel=True)]),
    "p29": dict(vig=(0.62, 0.5, None), blocks=[B(0.08, 0.05, 0.84, [
        "RRRUMBLE! The whole tree SHAKES.",
        '"Not AGAIN!" cries Banjo.',
        "But it isn't a storm. It's Olive, snoring.",
        '"RRRUMBLE," says Lyrebird. And he giggles.'], align="c")]),
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
        # no one-word last line: pull a word down from the line above (Book 3 addition)
        if not shout and len(cur) == 1 and len(lines) >= 2 and lines[-2] != "gap" \
                and len(lines[-2]) >= 3 and lines[-2] is not cur:
            prev = lines[-2]
            moved = prev.pop()
            words = [(moved[0], moved[1])] + [(w, f) for w, f, _ in cur]
            cur[:] = []
            x = 0
            for w, f in words:
                cur.append((w, f, x + (space if cur else 0)))
                x = cur[-1][2] + f.getlength(w)
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
    # 90th percentile, not the median: Book 3 p25's vignettes touch the image edge, and the
    # median then read as dark and washed the whole page out. Gain capped at 255/225.
    bg = [sorted(c[i] for c in band)[int(len(band) * 0.9)] for i in range(3)]
    lut = []
    for i in range(3):
        k = 255.0 / max(bg[i], 225)
        lut += [min(255, int(v * k + 0.5)) for v in range(256)]
    img = img.point(lut)
    # soft white key (Book 3): pixels whose darkest channel is above 215 fade to pure white by
    # 245, so paper grain disappears where vignettes run off the art's edge (p25, facts spots)
    import numpy as np
    a = np.asarray(img).astype(np.float32)
    t = np.clip((a.min(axis=2, keepdims=True) - 215.0) / 30.0, 0, 1)
    return Image.fromarray((a * (1 - t) + 255.0 * t).astype("uint8"), "RGB")

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
            feather_paste(canvas, art, (ox + int(cx * TRIM) - side // 2, top),
                          edge=spec.get("feather", 0.07))
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
    d.text((cx, oy + int(TRIM * 0.15)), "Who Shook", font=chewy(230), fill=DARK, anchor="ms")
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
    d.text((cx, oy + int(TRIM * 0.36)), "For everyone who has ever hidden", font=italic(76), fill=DARK, anchor="ms")
    d.text((cx, oy + int(TRIM * 0.40)), "under the covers when the thunder booms.", font=italic(76), fill=DARK, anchor="ms")
    small = font("Nunito[wght].ttf", 40, "Regular")
    lines = ["Who Shook My Tree?",
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
    ("Lightning", "is a giant spark of electricity in a storm cloud. It heats the air so fast that "
     "the air bursts with a BOOM. That BOOM is thunder."),
    ("Flash, then boom.", "Light travels much faster than sound, so you see lightning before you "
     "hear thunder. Count the seconds in between: every 5 seconds means the storm is about 1 mile away."),
    ("When thunder roars, go indoors.", "The safest place to watch a storm is from inside."),
    ("Superb lyrebirds", "copy the songs and calls of more than 20 kinds of birds, so well that it's "
     "hard to tell them apart. At night they sleep up in the trees."),
    ("Green tree frogs", "call loudly after rain: \u201ccrawk, crawk, crawk.\u201d"),
    ("The smell of rain", "has a name: petrichor. Two Australian scientists named it in 1964."),
    ("Koalas", "hug tree trunks on hot days, because the trunk is cooler than the air."),
    ("Wombats", "dig long burrows under the ground, where they stay safe and dry."),
    ("Sugar gliders", "sleep in tree hollows lined with leaves, often curled up together in a group."),
]
CREAM = (250, 244, 228)

def spot(pid, box_frac):
    """Crop a spot illustration from a vignette page (box in fractions of the 2048 art)."""
    art = whiten(Image.open(os.path.join(PAGES_DIR, pid + ".png")).convert("RGB"))
    W = art.width
    return art.crop(tuple(int(v * W) for v in box_frac))

def facts_pages():
    """Pages 30 (left) and 31 (right): white pages, heading, facts, spot art cropped from the story
    vignettes (p23 Banjo and Olive, p25 wombat/cockatoo/possum/lyrebird), edges feathered into white."""
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
    # left page (even): heading + Banjo spot, then the first five facts
    c = pages["p30"]; ox, oy = BLEED, BLEED
    d = ImageDraw.Draw(c)
    d.text((ox + SAFE + 10, oy + 380), "True Facts", font=head, fill=(176, 92, 52), anchor="ls")
    d.text((ox + SAFE + 10, oy + 560), "from the Bush", font=head, fill=(176, 92, 52), anchor="ls")
    sp = spot("p23", (0.15, 0.10, 0.90, 0.95)); sp.thumbnail((640, 640), Image.LANCZOS)
    feather_paste(c, sp, (ox + TRIM - SAFE - sp.width, oy + 90))
    end = facts_text(c, ox, oy, FACTS[:5], 860, SAFE + 10, TRIM - 2 * SAFE - 20)
    if end > TRIM - SAFE:
        print(f"  WARNING p30: facts run to y {end}, past the safe zone")
    # right page (odd): remaining facts, then four spots along the bottom
    c = pages["p31"]; ox, oy = 0, BLEED
    end = facts_text(c, ox, oy, FACTS[5:], SAFE + 90, SAFE + 10, TRIM - 2 * SAFE - 20)
    size = 500                                   # 2 x 2 grid of spots under the facts
    gx = ox + (TRIM - 2 * size - 60) // 2
    gy = oy + TRIM - SAFE - 2 * size - 40
    if end > gy - oy - 30:
        print(f"  WARNING p31: facts (to y {end}) collide with the spot art grid")
    for i, (pid, box) in enumerate(spots_right):
        sp = spot(pid, box); sp.thumbnail((size, size), Image.LANCZOS)
        feather_paste(c, sp, (gx + (i % 2) * (size + 60), gy + (i // 2) * (size + 40)), edge=0.22)
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
        "More Banjo and Olive stories: *Who Peeled My Tree?* and *Who Frosted My Tree?*"], align="c", px=64)
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
