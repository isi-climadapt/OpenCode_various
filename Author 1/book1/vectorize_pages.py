# -*- coding: utf-8 -*-
# F11: vector-trace the 1K OpenArt line art into print-resolution pages.
# The OpenArt CLI only returns 1024 px images (github.com/OpenArt-AI/cli/issues/2),
# and enlarged 1K art prints soft. Tracing gives smooth outlines at any size.
# Reads raw2_1k/page_XX.png, writes raw2/page_XX.png at 4300 px (600 DPI in the 2150 px art box).
#
# Usage: py vectorize_pages.py [page_01 page_02 ...]

import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "scripts"))
from vectorize_line_art import vectorize_line_art

SRC = os.path.join(HERE, "raw2_1k")
DST = os.path.join(HERE, "raw2")
SIZE = 4300

def main():
    os.makedirs(DST, exist_ok=True)
    keys = sys.argv[1:] or ["page_%02d" % i for i in range(1, 51)]
    for key in keys:
        out = vectorize_line_art(os.path.join(SRC, key + ".png"), os.path.join(DST, key + ".png"), SIZE, SIZE)
        print(key, "traced", out.size, flush=True)

if __name__ == "__main__":
    main()
