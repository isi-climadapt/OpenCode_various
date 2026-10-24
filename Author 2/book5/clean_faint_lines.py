# -*- coding: utf-8 -*-
# Book 5: whiten faint straight frame lines in the outer bands of raw2 sources.
# The batch audit and check_sources only see dark ink; nano-banana-2 sometimes draws a
# light grey panel edge (pages 27, 33) that survives the vector trace as a thin line.
# A row (or column) in the outer 15% counts as a faint line when light-grey pixels
# (110-245) run across more than 30% of it and dark ink (<110) covers under 3%.
# Originals are kept in raw2_orig/. Usage: py clean_faint_lines.py [page_NN ...]
import os, sys, shutil
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
RAW2, ORIG = os.path.join(HERE, "raw2"), os.path.join(HERE, "raw2_orig")
os.makedirs(ORIG, exist_ok=True)
keys = sys.argv[1:] or ["page_%02d" % i for i in range(1, 51)]
for k in keys:
    src = os.path.join(RAW2, k + ".png")
    g = np.asarray(Image.open(src).convert("L")).astype(np.int16)
    h, w = g.shape
    faint = (g >= 110) & (g < 245)
    dark = g < 110
    out = g.copy()
    hit = []
    for axis, n, size in ((0, h, w), (1, w, h)):
        band = int(n * 0.15)
        for i in list(range(band)) + list(range(n - band, n)):
            f = faint[i] if axis == 0 else faint[:, i]
            dk = dark[i] if axis == 0 else dark[:, i]
            if f.sum() > 0.30 * size and dk.sum() < 0.03 * size:
                if axis == 0:
                    out[i][faint[i]] = 255
                else:
                    out[:, i][faint[:, i]] = 255
                hit.append(("row" if axis == 0 else "col") + str(i))
    if hit:
        if not os.path.exists(os.path.join(ORIG, k + ".png")):
            shutil.copyfile(src, os.path.join(ORIG, k + ".png"))
        Image.fromarray(out.clip(0, 255).astype("uint8"), "L").save(src)
        print(k, "cleaned", len(hit), "lines:", hit[0], "...", hit[-1])
print("done")
