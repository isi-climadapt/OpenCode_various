# -*- coding: utf-8 -*-
# Author 3 Book 1 - contact sheet of finished page art (pages\pXX.png), laid out as book spreads
# so left/right pairs are reviewed together. Usage: py contact_sheet.py [out.png]

import os, re, sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PAGES_DIR = os.path.join(HERE, "pages")
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "contact_sheet.png")
T, PAD, LAB = 520, 24, 44
FONT = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 26)

def main():
    nums = sorted(int(m.group(1)) for f in os.listdir(PAGES_DIR)
                  if (m := re.match(r"p(\d+)\.png$", f)))
    # group into book spreads: page 1 alone, then (2,3), (4,5) ... page 32 alone
    rows, seen = [], set()
    for n in nums:
        if n in seen:
            continue
        pair = (n,) if n == 1 else ((n, n + 1) if n % 2 == 0 else (n - 1, n))
        pair = tuple(p for p in pair if p in nums)
        seen.update(pair)
        rows.append(pair)
    cols = 2  # spreads per row
    grid = [rows[i:i + cols] for i in range(0, len(rows), cols)]
    W = PAD + cols * (2 * T + PAD)
    H = PAD + len(grid) * (T + LAB + PAD)
    sheet = Image.new("RGB", (W, H), "#eeeeee")
    d = ImageDraw.Draw(sheet)
    for r, spreads in enumerate(grid):
        y = PAD + r * (T + LAB + PAD)
        for c, pair in enumerate(spreads):
            x0 = PAD + c * (2 * T + PAD)
            d.text((x0, y + 8), "Pages " + "-".join(str(p) for p in pair), fill="black", font=FONT)
            for p in pair:
                x = x0 + (T if p % 2 else 0)  # odd pages are right-hand pages
                im = Image.open(os.path.join(PAGES_DIR, f"p{p:02d}.png")).convert("RGB")
                im = im.resize((T, T), Image.LANCZOS)
                sheet.paste(im, (x, y + LAB))
                d.text((x + 8, y + LAB + T - 34), f"p{p}", fill="white", font=FONT,
                       stroke_width=3, stroke_fill="black")
    sheet.save(OUT)
    print(OUT, sheet.size, f"{len(nums)} pages")

if __name__ == "__main__":
    main()
