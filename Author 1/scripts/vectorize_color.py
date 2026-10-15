# -*- coding: utf-8 -*-
# F11b v3 — COLOUR cover-art vectorizer (winding-aware layers, ink-on-top):
#   1) quantize -> unique palette; bg = most common colour
#   2) fill layers (non-bg, non-near-black), largest first, each traced with
#      winding-aware hole handling + auto polarity check (F11a logic)
#   3) ink layer = near-black clusters (max(RGB) < 60), traced as ONE mask, pasted LAST
# Usage: py vectorize_color.py <src.png> <out.png> <target_w> <target_h> [colors]
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import potrace


def _flatten(curve):
    pts = [(curve.start_point.x, curve.start_point.y)]
    for s in curve:
        end = s.end_point
        if s.is_corner:
            pts += [(s.c.x, s.c.y), (end.x, end.y)]
        else:
            c1, c2 = s.c1, s.c2
            for i in range(1, 13):
                t = i / 12.0; mt = 1 - t
                x = mt**3 * pts[-1][0] + 3 * mt**2 * t * c1.x + 3 * mt * t**2 * c2.x + t**3 * end.x
                y = mt**3 * pts[-1][1] + 3 * mt**2 * t * c1.y + 3 * mt * t**2 * c2.y + t**3 * end.y
                pts.append((x, y))
    return pts


def _signed_area(pts):
    x = np.array([p[0] for p in pts]); y = np.array([p[1] for p in pts])
    return 0.5 * (np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))


def render_region_mask(region_bool, out_size, scale):
    """Trace a boolean region -> L mask (region=255, background=0), winding-aware
    holes + automatic polarity fallback (empirical, like F11a)."""
    h, w = region_bool.shape
    mimg = Image.fromarray(((~region_bool) * 255).astype("uint8"), "L")
    path = potrace.Bitmap(mimg).trace(turdsize=10)
    solids, holes = [], []
    for curve in path:
        pts = [(x * scale, y * scale) for x, y in _flatten(curve)]
        a = _signed_area(pts)
        if abs(a) < 30:
            continue
        (holes if a < 0 else solids).append(pts)
    W, H = out_size

    def build(solid_list, hole_list):
        cv = Image.new("L", (W, H), 0)
        dr = ImageDraw.Draw(cv)
        for pts in solid_list:
            dr.polygon(pts, fill=255)
        for pts in hole_list:
            dr.polygon(pts, fill=0)
        return cv

    m = build(solids, holes)
    if np.asarray(m.resize((W // 4, H // 4))).mean() < np.asarray(
            Image.fromarray((region_bool * 255).astype("uint8")).resize((W // 4, H // 4))).astype(float).mean() * 0.35 / 255:
        m = build(holes, solids)  # winding inverted for this layer
    return m


def vectorize_color_art(src_path, out_path, target_w, target_h, colors=24, dpi=300):
    img = Image.open(src_path).convert("RGB").resize((target_w, target_h), Image.LANCZOS)
    img = img.filter(ImageFilter.SMOOTH_MORE)

    q = img.quantize(colors=colors, method=Image.Quantize.MEDIANCUT).convert("RGB")
    npq = np.asarray(q).astype(int)

    flat = npq.reshape(-1, 3)
    uniqs, counts = np.unique(flat, axis=0, return_counts=True)
    bg = tuple(int(v) for v in uniqs[counts.argmax()])

    canvas = Image.new("RGB", (target_w, target_h), bg)

    ink_colour = (35, 25, 20)

    def paste_colour(colour, mask):
        fill = Image.new("RGB", (target_w, target_h), colour)
        canvas.paste(fill, (0, 0), mask)

    # fills: skip bg and near-black clusters; near-black = cluster whose max channel < 60
    fills = []
    for u, cnt in zip(uniqs, counts):
        u = tuple(int(v) for v in u)
        if cnt < 200 or u == bg or max(u) < 60:
            continue
        fills.append((cnt, u))
    fills.sort(key=lambda e: -e[0])

    for cnt, u in fills:
        region = (npq == np.array(u).reshape(1, 1, 3)).all(axis=2)
        mask = render_region_mask(region, (target_w, target_h), 1.0)
        paste_colour(u, mask)

    # ink layer LAST
    dark = (npq.max(axis=2) < 60)
    if dark.any():
        mask = render_region_mask(dark, (target_w, target_h), 1.0)
        paste_colour(ink_colour, mask)

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
    tw, th = int(sys.argv[3]), int(sys.argv[4])
    n = int(sys.argv[5]) if len(sys.argv) > 5 else 24
    c = vectorize_color_art(src, out, tw, th, n)
    print("out:", c.size)
