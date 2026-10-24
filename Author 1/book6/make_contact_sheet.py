# -*- coding: utf-8 -*-
# Book 4: contact sheet of the 50 assembled pages (raw/) for the human review checkpoint.
# Writes contact_sheet.png (10 x 5 grid, labelled) and contact_sheet_small.png.
# Usage: py make_contact_sheet.py
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
FONT = os.path.join(HERE, "fonts", "Baloo2.ttf")
COLS, ROWS = 10, 5
TW, TH = 400, 518   # thumb keeps the 2550 x 3300 page ratio
LABEL = 44

sheet = Image.new("L", (COLS * TW, ROWS * (TH + LABEL)), 255)
d = ImageDraw.Draw(sheet)
f = ImageFont.truetype(FONT, 34)
for i in range(1, 51):
    p = os.path.join(RAW, "page_%02d.png" % i)
    c, r = (i - 1) % COLS, (i - 1) // COLS
    x, y = c * TW, r * (TH + LABEL)
    if os.path.exists(p):
        im = Image.open(p).convert("L").resize((TW - 8, TH - 8), Image.LANCZOS)
        sheet.paste(im, (x + 4, y + 4))
    d.rectangle((x + 2, y + 2, x + TW - 2, y + TH - 2), outline=170, width=2)
    d.text((x + 12, y + TH + 2), "page %d" % i, fill=0, font=f)
sheet.save(os.path.join(HERE, "contact_sheet.png"))
sheet.resize((sheet.width // 2, sheet.height // 2), Image.LANCZOS).save(
    os.path.join(HERE, "contact_sheet_small.png"))
print("contact sheet:", sheet.size)
