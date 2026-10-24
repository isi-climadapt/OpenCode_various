# -*- coding: utf-8 -*-
# Author 3 Book 3 - Who Shook My Tree? Character test for the two new animals via OpenArt CLI
# (adapted from book1\char_test.py, the only Author 3 character test).
# Phase 1 (this script): a model sheet for Lyrebird and the green tree frogs on nano-banana-pro,
#   with Book 1's cast sheet as the style reference so they match the existing cast. Two takes.
# Phase 2: two real story pages with gen_pages.py (p18 Lyrebird, p26 frogs) once a take is copied
#   to char_test\sheet_new.png. Those pages count toward the 29 if approved.
# Usage: py char_test.py sheets        # about 40 credits per take
# Outputs go to char_test\ ; existing files >10KB are skipped (cache).

import os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "char_test")
CAST = os.path.join(HERE, "..", "book1", "char_test", "sheet_cast.png")
EXE = r"C:\Users\ibian\AppData\Local\Programs\openart\bin\openart.exe"
MODEL = "nano-banana-pro"

STYLE = ("Children's picture book illustration. Soft gouache and colored-pencil look with visible "
         "paper grain, rounded chunky character shapes, gentle line work, no heavy outlines. "
         "Warm, funny, expressive. No words, letters, numbers, signs or text anywhere in the image.")

LYRE = ("Lyrebird, a male superb lyrebird: soft brown-gray body, slim neck, small rounded head, "
        "dark friendly eye, long gray legs, and a very long tail made of two broad outer feathers "
        "striped brown and cream that curve into a lyre shape, filled with fine silvery lace plumes. "
        "Friendly, a little proud, a show-off, no clothes")
FROG = ("an Australian green tree frog: plump and round, bright leaf-green back, white belly, big "
        "golden eyes, round sticky toe pads, wide smiley mouth, no clothes")

SHEET = ("Character model sheet on a plain white background for a picture book, painted in exactly "
         "the same style as the attached reference sheet of Australian animals: the same gouache "
         "and colored-pencil texture, the same soft line work, the same round friendly eyes with a "
         "white highlight, the same proportions and level of detail. This sheet shows only two new "
         "animals, not the animals in the reference. Left two-thirds: " + LYRE + ", shown twice: "
         "standing in side view with the long tail trailing behind, and with the tail fanned up "
         "over his back in a proud display, beak open as if singing. Right third: " + FROG +
         ", shown three times: sitting, singing with its throat puffed out, and clinging to a twig. "
         "Same character design in every pose, evenly lit, full bodies visible, no cockatoo, no "
         "possum, no echidna, no wombat, no kookaburra. " + STYLE)

def run(prompt, path, refs):
    if os.path.exists(path) and os.path.getsize(path) > 10000:
        return path, "cached"
    cmd = [EXE, "generate", "image", prompt, "--model", MODEL, "-o", path, "--quiet", "--yes"]
    for r in refs:
        cmd += ["--image", r]
    for attempt in range(2):  # F7: one retry on failure
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        if p.returncode == 0:
            return path, "ok"
    return path, "FAIL: " + (p.stderr or p.stdout)[-300:]

def main():
    os.makedirs(OUT, exist_ok=True)
    if sys.argv[1] == "sheets":
        jobs = [(SHEET, os.path.join(OUT, f"sheet_new_{k}.png"), (CAST,)) for k in ("a", "b")]
        with ThreadPoolExecutor(max_workers=2) as ex:
            for path, status in ex.map(lambda j: run(*j), jobs):
                print(os.path.basename(path), status)

if __name__ == "__main__":
    main()
