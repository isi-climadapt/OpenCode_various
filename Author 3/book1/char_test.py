# -*- coding: utf-8 -*-
# Author 3 Book 1 - Who Peeled My Tree? Character consistency test via OpenArt CLI.
# Phase 1 (sheets): Banjo + Olive model sheet on each candidate model (text2image).
# Phase 2 (pages): 3 story pages per model, image2image with the chosen sheet as reference.
# Usage: py char_test.py sheets
#        py char_test.py pages <reference.png>
# Outputs go to char_test\ ; existing files >10KB are skipped (cache).

import os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "char_test")
EXE = r"C:\Users\ibian\AppData\Local\Programs\openart\bin\openart.exe"
MODELS = {"nbpro": "nano-banana-pro", "ideo": "ideogram-4-5", "sd45": "byte-plus-seedream-4-5"}

STYLE = ("Children's picture book illustration. Soft gouache and colored-pencil look with visible "
         "paper grain, rounded chunky character shapes, gentle line work, no heavy outlines. "
         "Palette of eucalyptus greens, warm ochre and terracotta bark, twilight violet and dusky "
         "blue, moonlight silver. Warm, funny, expressive. No words, letters, numbers, signs or "
         "text anywhere in the image.")

BANJO = ("Banjo, a small round sugar glider: soft blue-gray fur, cream belly and cheeks, one black "
         "stripe running from between his eyes over his head and down his back, huge glossy black "
         "eyes, small pink nose, round ears lined with pink, a cream-edged gliding membrane between "
         "his front and back paws, long fluffy gray tail with a black tip, no clothes")
OLIVE = ("Olive, a chunky round koala: silver-gray fur, white chest, big fluffy white-edged ears, "
         "large black leathery nose, sleepy half-closed eyes, no clothes")

SHEET = ("Character model sheet on a plain white background for a picture book. Left half: " + BANJO +
         ", shown three times: standing front view, side view, and gliding with the membrane spread "
         "wide. Right half: " + OLIVE + ", shown twice: sitting hugging a branch asleep, and sitting "
         "awake looking calm. Same character design in every pose, evenly lit, full bodies visible. "
         + STYLE)

PAGES = {
    "p05_glide": ("Square page. " + BANJO + ", mid-glide toward the viewer against a violet dusk "
                  "sky over the Australian bush, membrane spread wide, joyful open mouth. The top "
                  "left third of the image is open sky, empty, for text. " + STYLE),
    "p08_olive": ("Square page. At night in a tall gum tree, " + OLIVE + ", asleep hugging a high "
                  "fork of the tree. " + BANJO + ", bouncing on the branch beside her, waving a "
                  "long curl of peeled bark, eyes wide and alarmed. Moonlit sky. The top third of "
                  "the image is open sky, empty, for text. " + STYLE),
    "p21_low": ("Square page. Moonlit night. The trunk of a gum tree almost bare of old bark, smooth "
                "new bark showing in cream, pink, gray-green and orange patches, heaps of curled old "
                "bark at its base. " + BANJO + ", very small, sitting on the bark pile with his head "
                "in his paws, sad. Cool blue palette. The top third is calm dark sky, empty, for "
                "text. " + STYLE),
}

def run(model, prompt, path, refs=()):
    if os.path.exists(path) and os.path.getsize(path) > 10000:
        return path, "cached"
    cmd = [EXE, "generate", "image", prompt, "--model", model, "-o", path, "--quiet", "--yes"]
    for r in refs:
        cmd += ["--image", r]
    for attempt in range(2):  # F7: one retry on failure
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        if p.returncode == 0:
            return path, "ok"
    return path, "FAIL: " + (p.stderr or p.stdout)[-300:]

def main():
    os.makedirs(OUT, exist_ok=True)
    jobs = []
    if sys.argv[1] == "sheets":
        for key, model in MODELS.items():
            jobs.append((model, SHEET, os.path.join(OUT, f"sheet_{key}.png"), ()))
    elif sys.argv[1] == "pages":
        ref = os.path.abspath(sys.argv[2])
        for key, model in MODELS.items():
            for page, prompt in PAGES.items():
                full = ("Use the attached character sheet as the exact design for the characters. "
                        + prompt)
                jobs.append((model, full, os.path.join(OUT, f"{page}_{key}.png"), (ref,)))
    with ThreadPoolExecutor(max_workers=6) as ex:
        for path, status in ex.map(lambda j: run(*j), jobs):
            print(os.path.basename(path), status)

if __name__ == "__main__":
    main()
