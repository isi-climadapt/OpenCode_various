# -*- coding: utf-8 -*-
# Batch-generate 50 book pages via OpenArt CLI (Nano Banana 2), pad to print canvas, QA.
# Usage: py batch_generate.py [--start N]

import os, re, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.abspath(__file__))
PROMPTS_MD = os.path.join(ROOT, "PAGE-GENERATION-PROMPTS.md")
RAW2 = os.path.join(ROOT, "raw2")       # native model output
OUT = os.path.join(ROOT, "raw")         # print-canvas pages
EXE = r"C:\Users\ibian\AppData\Local\Programs\openart\bin\openart.exe"
MODEL = "nano-banana-2"

SUFFIX = ("Bold and easy coloring book page for kids ages 3-8. A rich but simple scene around the "
          "animal with 6 to 8 easy elements suitable for its habitat (trees, clouds, stars, waves, "
          "rocks, flowers, smaller animal friends, bubbles, sun, grass or sand), each element drawn "
          "as one big simple closed shape. Very thick, clean, smooth black outlines (heavy, "
          "marker-friendly). Plain white background, no frame or border around the image edge. "
          "Only simple closed shapes with large open areas to colour. The main animal stays the "
          "largest thing on the page, portrait composition. Cute, friendly, happy faces with large "
          "simple eyes. No shading, no grey, no colour, no fill, no texture, no crosshatching. "
          "No words, letters, numbers or text anywhere in the image. Nothing in the bottom 6 "
          "percent of the page.")

CANVAS_W, CANVAS_H = 2550, 3300
ART_W = 2250  # art upscale target width (0.5in side margins)

def load_prompts():
    scenes = {}
    with open(PROMPTS_MD, encoding="utf-8") as f:
        for line in f:
            m = re.match(r"\|\s*(page_\d+)\s*\|", line)
            if m:
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                if len(cells) >= 3 and not cells[0].startswith("page") or len(cells) >= 3:
                    pass
                mm = re.match(r"\|\s*(page_\d+)\s*\|\s*[^|]+\|\s*(.+?)\s*\|", line)
                if mm and not mm.group(2).startswith("Fun-fact"):
                    scenes[mm.group(1)] = mm.group(2)
    return scenes

def generate(key, scene):
    path = os.path.join(RAW2, key + ".png")
    if os.path.exists(path) and os.path.getsize(path) > 10000:
        return key, "cached"
    prompt = scene + " " + SUFFIX
    r = subprocess.run([EXE, "generate", "image", prompt, "--model", MODEL,
                        "-o", os.path.join(RAW2, key + ".png"), "--quiet", "--yes"],
                       capture_output=True, text=True, timeout=300)
    if r.returncode == 0:
        return key, "ok"
    return key, "FAIL: " + (r.stderr or r.stdout)[-200:]

def pad_and_caption(src, key, caption_text):
    from PIL import Image, ImageOps, ImageDraw, ImageFont
    FONT = os.path.join(ROOT, "fonts", "Baloo2.ttf")
    font = ImageFont.truetype(FONT, 115)
    numf = ImageFont.truetype(FONT, 62)
    img = Image.open(src).convert("L")
    img = ImageOps.autocontrast(img, cutoff=1)
    img = img.point(lambda p: 0 if p < 110 else 255)
    img = img.resize((2400, 2400), Image.LANCZOS)
    canvas = Image.new("L", (CANVAS_W, CANVAS_H), 255)
    canvas.paste(img, (75, 130))
    d = ImageDraw.Draw(canvas)
    bbox = d.textbbox((0, 0), caption_text, font=font)
    d.text(((CANVAS_W-bbox[2]+bbox[0])//2, 2950), caption_text, fill=0, font=font)
    m = re.match(r"page_(\d+)", key)
    number = str(int(m.group(1)) * 2 - 1)
    nb = d.textbbox((0, 0), number, font=numf)
    d.text((CANVAS_W - 130 - (nb[2] - nb[0]), 3060), number, fill=120, font=numf)
    return canvas

def caption_for(key):
    import json
    capfile = os.path.join(ROOT, "captions.json")
    with open(capfile, encoding="utf-8") as f:
        caps = json.load(f)
    return caps.get(key, "")

def qa(canvas_img, key):
    w, h = canvas_img.size
    px = canvas_img.load()
    greys = sum(1 for y in range(0, 2900, 4) for x in range(0, w, 4)
                if 40 < px[x, y] < 215)
    greys /= (w//4)*((2900)//4)
    issues = []
    if greys > 0.004: issues.append("greys %.2f%%" % (greys*100))
    return issues

def main():
    os.makedirs(RAW2, exist_ok=True)
    os.makedirs(OUT, exist_ok=True)
    scenes = load_prompts()
    keys = sorted(scenes.keys())
    if "--only" in sys.argv:
        keys = [k for k in keys if k in sys.argv[sys.argv.index("--only")+1:]]
    from concurrent.futures import ThreadPoolExecutor
    results = {}
    with ThreadPoolExecutor(max_workers=6) as ex:
        for key, status in ex.map(lambda k: generate(k, scenes[k]), keys):
            results[key] = status
            print(key, status, flush=True)
    print("--- post-processing ---")
    report = {}
    for key in keys:
        src = os.path.join(RAW2, key + ".png")
        if not os.path.exists(src):
            report[key] = ["missing source"]
            continue
        try:
            cv = pad_and_caption(src, key, caption_for(key))
            issues = qa(cv, key)
            cv.save(os.path.join(OUT, key + ".png"), dpi=(300, 300))
            report[key] = issues
            print(key, "assembled", issues or "QA-OK", flush=True)
        except Exception as e:
            report[key] = ["process error: %s" % e]
            print(key, "ERROR", e, flush=True)
    fails = {k: v for k, v in report.items() if v}
    print("=== SUMMARY: %d ok, %d flagged ===" % (len(report)-len(fails), len(fails)))
    for k, v in fails.items():
        print("FLAG", k, v)

if __name__ == "__main__":
    main()
