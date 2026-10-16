# -*- coding: utf-8 -*-
# F11 — VECTOR LINE-ART UPSCALER (pixelation + halo cure, pipeline-wide)
# 1024px native -> potracer vector trace -> render at target size.
# Edges are mathematically smooth at ANY resolution: no upscale softness,
# no UnsharpMask halos, pure black/white output -> print-crisp at 300 DPI.
#
# API notes (potracer 0.0.4): Bitmap accepts a PIL grayscale image DIRECTLY.
# Holes vs solids via winding orientation (signed/shoelace area sign).
#
# Usage: py vectorize_line_art.py <src.png> <out.png> [target_w] [target_h]
import sys
import numpy as np
from PIL import Image, ImageOps, ImageDraw
import potrace


def _flatten(curve, scale):
    pts = [(curve.start_point.x * scale, curve.start_point.y * scale)]
    for s in curve:
        end = s.end_point
        if s.is_corner:
            pts += [(s.c.x * scale, s.c.y * scale), (end.x * scale, end.y * scale)]
        else:
            c1, c2 = s.c1, s.c2
            for i in range(1, 13):
                t = i / 12.0; mt = 1 - t
                x = mt**3 * pts[-1][0] + 3 * mt**2 * t * c1.x * scale + 3 * mt * t**2 * c2.x * scale + t**3 * end.x * scale
                y = mt**3 * pts[-1][1] + 3 * mt**2 * t * c1.y * scale + 3 * mt * t**2 * c2.y * scale + t**3 * end.y * scale
                pts.append((x, y))
    return pts


def _signed_area(pts):
    x = np.array([p[0] for p in pts]); y = np.array([p[1] for p in pts])
    return 0.5 * (np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))


def vectorize_line_art(src_path, out_path=None, target_w=2230, target_h=2520, dpi=300):
    """Vector-trace a grayscale line-art page and render at (target_w, target_h)."""
    img = Image.open(src_path).convert("L")
    img = ImageOps.autocontrast(img, cutoff=1)
    # Enlarge 4x before tracing. Potrace only sees black/white pixels, so at 1024 px
    # small shapes (eye highlights, cheeks) trace as diamonds and lumpy ovals. The
    # Lanczos enlargement turns the anti-aliased edges into sub-pixel shape detail.
    # Page 42 agreement: 98.0% -> 99.4%. Costs about 15 s per page instead of 2 s.
    PRE = 4
    img = img.resize((img.width * PRE, img.height * PRE), Image.LANCZOS)

    path = potrace.Bitmap(img).trace(turdsize=8 * PRE * PRE)

    scale = min(target_w / img.width, target_h / img.height)
    W = max(1, int(round(img.width * scale)))
    H2 = max(1, int(round(img.height * scale)))

    # Even-odd fill: every traced outline flips ink inside it. Potrace outlines never
    # cross, so this draws any nesting depth correctly (face inside head inside sun).
    # The old solids-then-holes order painted holes white over the shapes nested in
    # them, which erased eyes, mouths and spines.
    ink = np.zeros((H2, W), dtype=bool)
    for curve in path:
        pts = _flatten(curve, scale)
        if abs(_signed_area(pts)) < 12:  # speckle
            continue
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        x0, y0 = max(0, int(min(xs))), max(0, int(min(ys)))
        x1, y1 = min(W, int(max(xs)) + 2), min(H2, int(max(ys)) + 2)
        if x1 <= x0 or y1 <= y0:
            continue
        m = Image.new("1", (x1 - x0, y1 - y0), 0)
        ImageDraw.Draw(m).polygon([(x - x0, y - y0) for x, y in pts], fill=1)
        ink[y0:y1, x0:x1] ^= np.asarray(m, dtype=bool)
    canvas = Image.fromarray(np.where(ink, 0, 255).astype("uint8"), "L")

    if out_path:
        import time
        for attempt in range(3):
            try:
                canvas.save(out_path, dpi=(dpi, dpi))
                break
            except OSError:
                time.sleep(2 * (attempt + 1))
    return canvas


if __name__ == "__main__":
    src, out = sys.argv[1], sys.argv[2]
    tw = int(sys.argv[3]) if len(sys.argv) > 3 else 2230
    th = int(sys.argv[4]) if len(sys.argv) > 4 else 2520
    c = vectorize_line_art(src, out, tw, th)
    print("out:", c.size)
