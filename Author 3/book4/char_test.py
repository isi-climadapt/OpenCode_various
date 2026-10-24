# -*- coding: utf-8 -*-
# Author 3 Book 4 - Who Took My Pouch? Character test for the new series cast via OpenArt CLI
# (copied from book3\char_test.py, rule 15).
# Phase 1 (this script): two model sheets on nano-banana-pro, with Book 1's cast sheet as the
#   style reference so the new cast matches the house look. Two takes each.
#   hero:  Clover the joey (3 poses) and Hugo the quokka (2 poses)
#   extra: Mom kangaroo (2 poses, one with the new baby peeking out) and the pelican
# Phase 2: two real story pages with gen_pages.py (p08 Clover and Hugo, p12 pelican) once takes
#   are copied to char_test\sheet_hero.png and char_test\sheet_extra.png. Those pages count
#   toward the 29 if they pass.
# Usage: py char_test.py sheets        # about 40 credits per take, 4 takes
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

CLOVER = ("Clover, a small young kangaroo joey, a girl: soft warm caramel-fawn fur, cream belly, "
          "cheeks and inner arms, very big upright ears lined with pink, huge glossy dark brown "
          "eyes with a white highlight, small black nose, one little tuft of fur sticking up on top "
          "of her head, short front paws, long narrow back feet, a long thick tail, no clothes")
HUGO = ("Hugo, a quokka, a boy: a small chunky round wallaby with short coarse brown-gray fur, "
        "short rounded ears, small dark eyes, small black nose, a wide happy closed-mouth smile "
        "and round rosy cheeks, short thin tail, no clothes")
MOM = ("Mom, a tall adult kangaroo: soft gray-fawn fur, cream belly, a gentle kind face, big "
       "ears, a pouch on her tummy, a long strong tail, no clothes")
PELICAN = ("an Australian pelican: big white body, black wing feathers, a very long pale pink bill "
           "with a stretchy throat pouch under it, round friendly eye, short gray legs")

LEAD = ("Character model sheet on a plain white background for a picture book, painted in exactly "
        "the same style as the attached reference sheet of Australian animals: the same gouache "
        "and colored-pencil texture, the same soft line work, the same round friendly eyes with a "
        "white highlight, the same proportions and level of detail. This sheet shows only new "
        "animals, not the animals in the reference. ")
SHEETS = {
    "hero": LEAD + "Left half: " + CLOVER + ", shown three times: standing front view smiling, "
            "side view mid-hop with both feet off the ground, and sitting with her arms crossed "
            "looking cross. Right half: " + HUGO + ", shown twice: sitting front view smiling, and "
            "standing side view nibbling a green leaf. Same character design in every pose, evenly "
            "lit, full bodies visible, no other animals. " + STYLE,
    "extra": LEAD + "Left two-thirds: " + MOM + ", shown twice: standing in side view with her "
             "pouch closed, and standing front view with the head of a tiny baby kangaroo (short "
             "fawn fuzz, tiny ears, big dark eyes) peeking out of her pouch. Right third: " +
             PELICAN + ", standing, shown once. Same character design in every pose, evenly lit, "
             "full bodies visible, no other animals. " + STYLE,
}

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
        jobs = [(SHEETS[s], os.path.join(OUT, f"sheet_{s}_{k}.png"), (CAST,))
                for s in SHEETS for k in ("a", "b")]
        with ThreadPoolExecutor(max_workers=4) as ex:
            for path, status in ex.map(lambda j: run(*j), jobs):
                print(os.path.basename(path), status)

if __name__ == "__main__":
    main()
