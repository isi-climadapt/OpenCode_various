# -*- coding: utf-8 -*-
# Back cover built to read in Amazon's small back-cover image (pipeline F13), Author 3 version.
# Copied from Author 2\scripts\back600.py (commit 7b5eaa7) and adapted for square, full-color
# picture books: 8.5 x 8.5 in trim (2550 px back), color art cards cropped from the page art
# (the coloring-book version turns cards to grayscale line art), and a dark twilight back with
# cream ink to match the front's sky. Amazon shrinks the back about 4.25x (600 px wide), so every
# word stays at 80 px or more (about 19 px+ at 600) and four big art cards carry the rest. No blurb
# or bio: the description, A+ and Author Central carry them. Barcode zone where KDP prints it (F12).
#
# Usage (inside a wrap builder, after the front and spine are drawn):
#     from back600 import draw_back, save_back_preview
#     draw_back(wrap, title=..., cards=[4 page paths or (path, zoom, cx, cy)], bullets=[3 short],
#               footer=[1-2 short lines], fonts=dict(title=..., body=...), colors=dict(...))

import os
from PIL import Image, ImageDraw, ImageFont

BLEED, TRIM_W, TRIM_H = 38, 2550, 2550         # px at 300 DPI (8.5 x 8.5 in)
BARCODE_W, BARCODE_H, BARCODE_GAP, BARCODE_PAD = 600, 360, 75, 45   # KDP: 2 x 1.2 in, 0.25 in in
SAFE = 150                                     # text margin from the back trim
CARD, CARD_GAP, CARD_Y = 700, 50, 360          # 2 x 2 art cards
CARD_ZOOM = 0.72   # cards show the central 72% of a page so the character reads at 600 px
TITLE_PX, BULLET_PX, FOOTER_PX = 150, 92, 80
PREVIEW_W = 600                                # Amazon's stored back-cover width


def barcode_area():
    """(x0, y0, x1, y1) of KDP's printed barcode on the wrap: 0.25 in from the spine fold
    and the bottom trim of the back cover."""
    spine_x, bottom_y = BLEED + TRIM_W, BLEED + TRIM_H
    return (spine_x - BARCODE_GAP - BARCODE_W, bottom_y - BARCODE_GAP - BARCODE_H,
            spine_x - BARCODE_GAP, bottom_y - BARCODE_GAP)


def check_barcode(wrap):
    """Fail the build unless KDP's barcode area (plus 0.1 in) is solid white."""
    x0, y0, x1, y1 = barcode_area()
    m = 30
    lo = wrap.crop((x0 - m, y0 - m, x1 + m, y1 + m)).convert("L").getextrema()[0]
    if lo < 250:
        raise SystemExit("BARCODE CHECK FAILED: KDP's barcode area is not solid white (darkest %d)" % lo)
    print("barcode check: KDP area is solid white")


def _font(font_path, px, weight=None):
    f = ImageFont.truetype(font_path, px)
    if weight:
        try:  # variable fonts (Nunito) default to their thinnest weight
            f.set_variation_by_name(weight)
        except (OSError, ValueError):
            pass  # static font: use as is
    return f


def _fit(d, text, font_path, px, max_w, weight=None):
    f = _font(font_path, px, weight)
    while d.textlength(text, font=f) > max_w and px > 40:
        px -= 4
        f = _font(font_path, px, weight)
    return f, px


def _closeup(card, size):
    """Crop a page to a close-up of its main character, in color, at size x size.
    card is a path, or (path, zoom, cx, cy) with the centre as fractions of the page."""
    path, zoom, fx, fy = (card, CARD_ZOOM, 0.5, 0.5) if isinstance(card, str) else card
    im = Image.open(path).convert("RGB")
    cw, ch = int(im.width * zoom), int(im.height * zoom)
    x = min(max(0, int(im.width * fx - cw / 2)), im.width - cw)
    y = min(max(0, int(im.height * fy - ch / 2)), im.height - ch)
    return im.crop((x, y, x + cw, y + ch)).resize((size, size), Image.LANCZOS)


def draw_back(wrap, title, cards, bullets, footer, fonts, colors):
    """Draw the back panel onto wrap (left of the spine). Returns the smallest text size used."""
    d = ImageDraw.Draw(wrap)
    x0, y0 = BLEED, BLEED
    ink, title_ink = colors["ink"], colors.get("title", colors["ink"])
    smallest = []

    # title: one line, as big as fits
    f, px = _fit(d, title, fonts["title"], TITLE_PX, TRIM_W - 2 * SAFE)
    w = d.textlength(title, font=f)
    d.text((x0 + (TRIM_W - w) / 2, y0 + 150), title, fill=title_ink, font=f)
    smallest.append(px)

    # four big color art cards with rounded corners and a cream frame
    left = x0 + (TRIM_W - (2 * CARD + CARD_GAP)) // 2
    for i, card in enumerate(cards[:4]):
        cx = left + (i % 2) * (CARD + CARD_GAP)
        cy = y0 + CARD_Y + (i // 2) * (CARD + CARD_GAP)
        art = _closeup(card, CARD)
        mask = Image.new("L", (CARD, CARD), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, CARD - 1, CARD - 1], radius=44, fill=255)
        wrap.paste(art, (cx, cy), mask)
        d.rounded_rectangle([cx, cy, cx + CARD, cy + CARD], radius=44, outline=colors["card"], width=12)

    # three short bullets, left column, clear of the barcode zone
    bar = barcode_area()
    text_right = bar[0] - BARCODE_PAD - 40
    by = y0 + CARD_Y + 2 * CARD + CARD_GAP + 70
    for line in bullets[:3]:
        f, px = _fit(d, line, fonts["body"], BULLET_PX, text_right - (x0 + SAFE) - 70, "SemiBold")
        d.ellipse([x0 + SAFE, by + px * 0.42, x0 + SAFE + 30, by + px * 0.42 + 30], fill=colors.get("accent", ink))
        d.text((x0 + SAFE + 70, by), line, fill=ink, font=f)
        smallest.append(px)
        by += int(BULLET_PX * 1.3)

    # footer lines (series and imprint), same column
    fy = by + 20
    for line in footer[:2]:
        f, px = _fit(d, line, fonts.get("footer", fonts["body"]), FOOTER_PX, text_right - (x0 + SAFE), "SemiBold")
        d.text((x0 + SAFE, fy), line, fill=colors.get("footer", ink), font=f)
        smallest.append(px)
        fy += int(FOOTER_PX * 1.25)
    if fy > y0 + TRIM_H - 40:
        raise SystemExit("BACK COVER: footer runs past the trim (y %d)" % fy)

    # KDP barcode zone (F12): solid white over KDP's printed area plus 0.15 in all round
    d.rounded_rectangle([bar[0] - BARCODE_PAD, bar[1] - BARCODE_PAD, bar[2] + BARCODE_PAD, bar[3] + BARCODE_PAD],
                        radius=24, fill=(255, 255, 255))
    check_barcode(wrap)
    return min(smallest)


def save_back_preview(wrap, path):
    """Save the back panel the way Amazon stores it (600 px wide), for the legibility check."""
    back = wrap.crop((BLEED, BLEED, BLEED + TRIM_W, BLEED + TRIM_H))
    back.resize((PREVIEW_W, PREVIEW_W * TRIM_H // TRIM_W), Image.LANCZOS).save(path)
    return path
