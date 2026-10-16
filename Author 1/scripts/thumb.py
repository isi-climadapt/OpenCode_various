# -*- coding: utf-8 -*-
# Crisp line-art thumbnail renderer for cover wraps (high-quality back-cover samples).
# Downscale + re-binarize keeps lines pure black/white at ANY size — no grey mush,
# both in print and in Amazon's low-res gallery derivatives.
from PIL import Image, ImageOps


def crisp_thumb(path, box_w, box_h, threshold=128):
    """Aspect-preserving fit of a line-art page into (box_w, box_h), re-binarized."""
    img = Image.open(path).convert("L")
    img = ImageOps.autocontrast(img, cutoff=1)
    scale = min(box_w / img.width, box_h / img.height)
    img = img.resize((max(1, int(img.width * scale)), max(1, int(img.height * scale))), Image.LANCZOS)
    img = img.point(lambda p: 0 if p < threshold else 255)
    return img


def art_thumb(path_1k, box, boost=0.0075):
    """Back-cover sample: the page's art only (no caption), traced from the 1K line art at
    2x the box size, cropped to the ink, lines thickened, reduced to fit box x box.
    Amazon's back-cover image is ~1000 px wide, so thin lines and page captions go soft
    there; thicker lines and bigger art survive it and still print cleanly."""
    import os, sys
    from PIL import ImageFilter
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from vectorize_line_art import vectorize_line_art
    big = vectorize_line_art(path_1k, None, box * 2, box * 2)
    ink = ImageOps.invert(big).getbbox()
    if ink:
        pad = int(box * 2 * 0.02)
        big = big.crop((max(0, ink[0] - pad), max(0, ink[1] - pad),
                        min(big.width, ink[2] + pad), min(big.height, ink[3] + pad)))
    k = max(3, int(box * 2 * boost) | 1)  # odd MinFilter size grows every black line
    big = big.filter(ImageFilter.MinFilter(k))
    scale = box / max(big.size)
    return big.resize((max(1, int(big.width * scale)), max(1, int(big.height * scale))), Image.LANCZOS)
