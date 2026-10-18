# -*- coding: utf-8 -*-
# Contact sheet of the 50 art pages, rendered from the finished interior PDF (what prints).
# Usage: py make_contact_sheet.py
import os
import fitz  # PyMuPDF
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
pdf = fitz.open(os.path.join(HERE, "KDP_FINAL_UPLOAD", "01_MANUSCRIPT_INTERIOR_108P.pdf"))
assert pdf.page_count == 108, pdf.page_count
font = ImageFont.truetype(os.path.join(HERE, "fonts", "Fredoka.ttf"), 30)
tw, th, cols = 340, 440, 10
sheet = Image.new("RGB", (cols * (tw + 12) + 12, 5 * (th + 50) + 12), "white")
d = ImageDraw.Draw(sheet)
for n in range(50):
    pg = pdf[4 + n * 2]  # art pages are PDF pages 5, 7, ... 103
    pix = pg.get_pixmap(dpi=40)
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples).resize((tw, th), Image.LANCZOS)
    x, y = 12 + (n % cols) * (tw + 12), 12 + (n // cols) * (th + 50)
    sheet.paste(im, (x, y))
    d.rectangle([x - 1, y - 1, x + tw, y + th], outline=(170, 170, 170))
    d.text((x, y + th + 6), "%d" % (n + 1), fill=(200, 0, 0), font=font)
sheet.save(os.path.join(HERE, "contact_sheet.png"))
small = sheet.resize((sheet.width // 2, sheet.height // 2), Image.LANCZOS)
small.save(os.path.join(HERE, "contact_sheet_small.png"))
print("contact sheet:", sheet.size)
