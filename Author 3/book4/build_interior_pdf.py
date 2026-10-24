# -*- coding: utf-8 -*-
# Author 3 Book 3 - assemble typeset\p01..p32.png into the KDP interior PDF.
# Page size 8.625 x 8.75 in (8.5 x 8.5 trim + bleed), 300 DPI, JPEG quality 97 with no chroma
# subsampling so the typeset text stays crisp. Then verifies page count and page size with PyMuPDF.
# Usage: py build_interior_pdf.py

import io, os
import img2pdf, fitz
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "typeset")
OUT_DIR = os.path.join(HERE, "KDP_FINAL_UPLOAD")
OUT = os.path.join(OUT_DIR, "01_MANUSCRIPT_INTERIOR_32P.pdf")
PAGE_IN = (8.625, 8.75)

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    jpgs = []
    for n in range(1, 33):
        im = Image.open(os.path.join(SRC, f"p{n:02d}.png")).convert("RGB")
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=97, subsampling=0, dpi=(300, 300))
        jpgs.append(buf.getvalue())
    layout = img2pdf.get_layout_fun((img2pdf.in_to_pt(PAGE_IN[0]), img2pdf.in_to_pt(PAGE_IN[1])))
    with open(OUT, "wb") as f:
        f.write(img2pdf.convert(jpgs, layout_fun=layout))
    doc = fitz.open(OUT)
    sizes = {(round(p.rect.width / 72, 3), round(p.rect.height / 72, 3)) for p in doc}
    print(OUT)
    print(f"pages: {doc.page_count}  page size (in): {sizes}  file: {os.path.getsize(OUT) / 1e6:.1f} MB")
    assert doc.page_count == 32 and sizes == {PAGE_IN}, "page count or size wrong"

if __name__ == "__main__":
    main()
