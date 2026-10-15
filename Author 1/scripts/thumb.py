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
