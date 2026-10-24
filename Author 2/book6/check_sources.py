# -*- coding: utf-8 -*-
# Book 6 (from book5): extra source checks the batch audit misses (run after every generation).
#   EDGE  ink within 8 px of any source edge (left/right too; the canvas audit only sees top/bottom)
#   GREY  grey paper background (photo-of-a-page renders): >15% of pixels mid-grey
# Usage: py check_sources.py [page_NN ...]
import os, sys
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
keys = sys.argv[1:] or ["page_%02d" % i for i in range(1, 51)]
bad = 0
for k in keys:
    g = np.asarray(Image.open(os.path.join(HERE, "raw2", k + ".png")).convert("L"))
    ink = g < 128
    m = 8
    e = {"T": ink[:m].sum(), "B": ink[-m:].sum(), "L": ink[:, :m].sum(), "R": ink[:, -m:].sum()}
    flags = ["EDGE %s %d" % (s, v) for s, v in e.items() if v > 20]
    grey = ((g > 150) & (g < 240)).mean()
    if grey > 0.15:
        flags.append("GREY %.0f%%" % (grey * 100))
    if flags:
        bad += 1
        print(k, ", ".join(flags))
print("source check: %d/%d clean" % (len(keys) - bad, len(keys)))
