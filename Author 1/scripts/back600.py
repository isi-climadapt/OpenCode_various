# -*- coding: utf-8 -*-
# Back cover built to read in Amazon's back-cover image (pipeline F13).
# Amazon stores the paperback back-cover image at only 600 x 776 px (the front gets
# 1000 x 1293; checked on B0HN12CCQP, Oct 2026), so our 2550 px back is shrunk 4.25x.
# Text set at 42-62 px ended up 9-14 px tall there and read as blur. This layout keeps
# every word at 80 px or more (about 19 px+ at 600), in dark ink, and lets four big art
# cards carry the rest. The barcode zone sits where KDP prints it (F12).
#
# Usage (inside a wrap builder, after the front and spine are drawn):
#     from back600 import draw_back
#     draw_back(wrap, title=..., cards=[4 raw2 paths], bullets=[3 short lines],
#               footer=[1-2 short lines], fonts=dict(title=..., body=...), colors=dict(...))

import os, sys
from PIL import Image, ImageDraw, ImageFont

BLEED, TRIM_W, TRIM_H = 38, 2550, 3300        # px at 300 DPI
BARCODE_W, BARCODE_H, BARCODE_GAP, BARCODE_PAD = 600, 360, 75, 45   # KDP: 2 x 1.2 in, 0.25 in in
SAFE = 150                                     # text margin from the back trim
CARD, CARD_GAP, CARD_Y = 900, 70, 400          # 2 x 2 art cards
CARD_ZOOM = 0.72   # cards show the central 72% of the page: a whole busy page turns to mush at 600 px
TITLE_PX, BULLET_PX, FOOTER_PX = 150, 92, 80
PREVIEW_W, PREVIEW_H = 600, 776                # Amazon's stored back-cover size


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
        try:  # variable fonts (Baloo 2, Fredoka) default to their thinnest weight
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


def _closeup(card):
    """Crop a page to a close-up of its main character and return the temp file path.
    card is a path, or (path, zoom, cx, cy) with the centre as fractions of the page."""
    import tempfile
    path, zoom, fx, fy = (card, CARD_ZOOM, 0.5, 0.5) if isinstance(card, str) else card
    im = Image.open(path).convert("L")
    cw, ch = int(im.width * zoom), int(im.height * zoom)
    x = min(max(0, int(im.width * fx - cw / 2)), im.width - cw)
    y = min(max(0, int(im.height * fy - ch / 2)), im.height - ch)
    out = os.path.join(tempfile.gettempdir(), "back600_card_%d.png" % abs(hash(card)))
    im.crop((x, y, x + cw, y + ch)).save(out)
    return out


def draw_back(wrap, title, cards, bullets, footer, fonts, colors, card_boost=0.0075):
    """Draw the back panel onto wrap (left of the spine). Returns the smallest text size used."""
    d = ImageDraw.Draw(wrap)
    x0, y0 = BLEED, BLEED
    ink, title_ink = colors["ink"], colors.get("title", colors["ink"])
    smallest = []

    # title: one line, as big as fits
    f, px = _fit(d, title, fonts["title"], TITLE_PX, TRIM_W - 2 * SAFE)
    w = d.textlength(title, font=f)
    d.text((x0 + (TRIM_W - w) / 2, y0 + 170), title, fill=title_ink, font=f)
    smallest.append(px)

    # four big art cards (they read at any size)
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from thumb import art_thumb
    left = x0 + (TRIM_W - (2 * CARD + CARD_GAP)) // 2
    for i, card in enumerate(cards[:4]):
        cx = left + (i % 2) * (CARD + CARD_GAP)
        cy = y0 + CARD_Y + (i // 2) * (CARD + CARD_GAP)
        d.rounded_rectangle([cx, cy, cx + CARD, cy + CARD], radius=44,
                            fill=(255, 255, 255), outline=colors["card"], width=12)
        art = art_thumb(_closeup(card), CARD - 110, boost=card_boost)
        wrap.paste(art.convert("RGB"), (cx + (CARD - art.width) // 2, cy + (CARD - art.height) // 2))

    # three short bullets, left column, clear of the barcode zone
    bar = barcode_area()
    text_right = bar[0] - BARCODE_PAD - 40
    by = y0 + CARD_Y + 2 * CARD + CARD_GAP + 90
    for line in bullets[:3]:
        f, px = _fit(d, line, fonts["body"], BULLET_PX, text_right - (x0 + SAFE) - 70, b"SemiBold")
        d.ellipse([x0 + SAFE, by + px * 0.42, x0 + SAFE + 30, by + px * 0.42 + 30], fill=colors.get("accent", ink))
        d.text((x0 + SAFE + 70, by), line, fill=ink, font=f)
        smallest.append(px)
        by += int(BULLET_PX * 1.35)

    # footer lines (imprint), same column
    fy = max(by + 30, bar[1] - BARCODE_PAD + 40)
    for line in footer[:2]:
        f, px = _fit(d, line, fonts.get("footer", fonts["body"]), FOOTER_PX, text_right - (x0 + SAFE), b"SemiBold")
        d.text((x0 + SAFE, fy), line, fill=colors.get("footer", ink), font=f)
        smallest.append(px)
        fy += int(FOOTER_PX * 1.3)
    if fy > y0 + TRIM_H - 60:
        raise SystemExit("BACK COVER: footer runs past the safe zone (y %d)" % fy)

    # KDP barcode zone (F12): solid white over KDP's printed area plus 0.15 in all round
    d.rounded_rectangle([bar[0] - BARCODE_PAD, bar[1] - BARCODE_PAD, bar[2] + BARCODE_PAD, bar[3] + BARCODE_PAD],
                        radius=24, fill=(255, 255, 255))
    check_barcode(wrap)
    return min(smallest)


def save_back_preview(wrap, path):
    """Save the back panel the way Amazon stores it (600 x 776), for the legibility check."""
    back = wrap.crop((BLEED, BLEED, BLEED + TRIM_W, BLEED + TRIM_H))
    back.resize((PREVIEW_W, PREVIEW_H), Image.LANCZOS).save(path)
    return path
