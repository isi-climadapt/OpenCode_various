# -*- coding: utf-8 -*-
# Author 2 Book 4 - Zoom Wonders. Batch-generate 50 pages via OpenArt CLI (Nano Banana 2).
# Style upgrade per author: 10-14 scene elements + art fills bigger area (fit box 2400x2700).
# Engine = book1/batch_generate.py + full locked suffix + F1/F2/F3/F5 audit + F7 retry + F8 save retry.
# Usage: py batch_generate_a2.py [--start N] [--only page_01 page_02 ...]

import os, re, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
PROMPTS_MD = os.path.join(HERE, "PAGE-GENERATION-PROMPTS.md")
RAW2 = os.path.join(HERE, "raw2")       # native model output
OUT = os.path.join(HERE, "raw")         # print-canvas pages
EXE = r"C:\Users\ibian\AppData\Local\Programs\openart\bin\openart.exe"
MODEL = "nano-banana-2"

SUFFIX = ("Bold and easy coloring book page. A rich, detailed but simple scene with 10 to 14 easy "
          "elements arranged to fill the whole page around the main vehicle (things that "
          "belong in the scene's setting, plus a few sparkles), all "
          "part of one connected scene, never a border of separate stickers or icons around the "
          "edge, each element drawn as one big simple closed shape. The composition fills "
          "almost the entire page. Whole scene floats with a plain white margin on every side; no "
          "element touches the image edges. Absolutely no rectangular frame or box line anywhere; "
          "do not draw a border. Very thick, clean, smooth black outlines (heavy, "
          "marker-friendly), pure black on plain white only. Only simple closed shapes with large "
          "open areas to color. The main vehicle stays the largest thing on the page, portrait "
          "composition. Cute, friendly, happy faces with large simple eyes. No shading, no grey, "
          "no color fill, no texture, no crosshatching. "
          "No words, letters, numbers, logos or symbols anywhere in the image. Nothing in the bottom 6 "
          "percent of the page.")

CANVAS_W, CANVAS_H = 2550, 3300
FIT_W, FIT_H = 2400, 2700   # BIGGER art fit box (was 2400x2400)

def load_prompts():
    scenes = {}
    with open(PROMPTS_MD, encoding="utf-8") as f:
        for line in f:
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
                        "-o", path, "--quiet", "--yes"],
                       capture_output=True, text=True, timeout=300)
    if r.returncode == 0:
        return key, "ok"
    return key, "FAIL: " + (r.stderr or r.stdout)[-200:]

def save_with_retry(img, path, tries=3):
    for i in range(tries):
        try:
            img.save(path, dpi=(300, 300))
            return True
        except OSError:
            time.sleep(2 * (i + 1))   # F8 OneDrive lock
    return False

def pad_and_caption(src, key, caption_text):
    from PIL import Image, ImageOps, ImageDraw, ImageFont
    FONT = os.path.join(HERE, "fonts", "Fredoka.ttf")
    numf = ImageFont.truetype(FONT, 62)
    img = Image.open(src).convert("L")
    img = ImageOps.autocontrast(img, cutoff=1)

    # F4: aspect-preserving fit into BIGGER box
    scale = min(FIT_W / img.width, FIT_H / img.height)
    img = img.resize((int(img.width * scale), int(img.height * scale)), Image.LANCZOS)
    img = img.point(lambda p: 0 if p < 110 else 255)

    canvas = Image.new("L", (CANVAS_W, CANVAS_H), 255)
    x_p = (CANVAS_W - img.width) // 2
    y_p = 150
    canvas.paste(img, (x_p, y_p))

    d = ImageDraw.Draw(canvas)

    # F5 v2 (author rule): UNIFORM caption size on every page: fixed 80px font,
    # word-wrap to max 2 lines; only shrinks if even 2 lines cannot fit.
    size = 80
    font = ImageFont.truetype(FONT, size)
    max_w = CANVAS_W - 300

    def wrap_to_lines(fnt):
        out, line = [], ""
        for wd in caption_text.split(" "):
            test = (line + " " + wd).strip()
            if d.textbbox((0, 0), test, font=fnt)[2] > max_w and line:
                out.append(line)
                line = wd
            else:
                line = test
        if line:
            out.append(line)
        return out

    lines = wrap_to_lines(font)
    while len(lines) > 2 and size > 55:
        size -= 5
        font = ImageFont.truetype(FONT, size)
        lines = wrap_to_lines(font)
    lines = lines[:2]

    if len(lines) == 1:
        bb = d.textbbox((0, 0), lines[0], font=font)
        d.text(((CANVAS_W - bb[2] + bb[0]) // 2, 2880), lines[0], fill=0, font=font)
    else:
        for i, ln in enumerate(lines):
            bb = d.textbbox((0, 0), ln, font=font)
            d.text(((CANVAS_W - bb[2] + bb[0]) // 2, 2840 + i * 92), ln, fill=0, font=font)

    m = re.match(r"page_(\d+)", key)
    number = str(int(m.group(1)) * 2 - 1)
    nb = d.textbbox((0, 0), number, font=numf)
    d.text((CANVAS_W - 130 - (nb[2] - nb[0]), 3010), number, fill=120, font=numf)

    return canvas, size

def caption_for(key):
    import json
    capfile = os.path.join(HERE, "captions.json")
    with open(capfile, encoding="utf-8") as f:
        caps = json.load(f)
    return caps.get(key, "")

def audit(src, canvas_img, key, final_caption_px):
    """F1 colour / F2 frame-line / F3 edge-touch / F5 caption-fit audit."""
    from PIL import Image
    issues = []
    # F1 colour fill scan on native source
    rgb = Image.open(src).convert("RGB")
    w, h = rgb.size
    px = rgb.load()
    col = 0; n = 0
    for y in range(0, h, 4):
        for x in range(0, w, 4):
            r, g, b = px[x, y]
            if max(r, g, b) - min(r, g, b) > 30:
                col += 1
            n += 1
    if col / max(n, 1) > 0.002:
        issues.append("F1 colour %.2f%%" % (col / n * 100))
    # F2 frame scan + F3 edge-touch on assembled canvas (art zone y 150..2835)
    g = canvas_img
    gw, gh = g.size
    gp = g.load()
    band = 80
    for y0 in (150, 2835 - band):
        for y in range(y0, y0 + band, 2):
            dark = sum(1 for x in range(0, gw, 2) if gp[x, y] < 128)
            if dark / (gw / 2) > 0.75:
                issues.append("F2 hline y=%d" % y); break
    for x0 in (0, gw - band):
        for x in range(x0, x0 + band, 2):
            dark = sum(1 for y in range(150, 2835, 2) if gp[x, y] < 128)
            if dark / ((2835 - 150) / 2) > 0.75:
                issues.append("F2 vline x=%d" % x); break
    for x0, y0, x1, y1 in ((0, 150, 12, 2835), (gw - 12, 150, gw, 2835),
                           (0, 150, gw, 162), (0, 2823, gw, 2835)):
        ink = sum(1 for y in range(y0, y1, 2) for x in range(x0, x1, 2) if gp[x, y] < 200)
        area = max((x1 - x0) // 2 * (y1 - y0) // 2, 1)
        if ink / area > 0.02:
            issues.append("F3 edge x%d y%d" % (x0, y0)); break
    if final_caption_px < 70:
        issues.append("F5 caption %dpx" % final_caption_px)
    greys = sum(1 for y in range(150, 2835, 4) for x in range(0, gw, 4)
                if 40 < gp[x, y] < 215)
    greys /= (gw // 4) * ((2835 - 150) // 4)
    if greys > 0.004:
        issues.append("greys %.2f%%" % (greys * 100))
    return issues

def main():
    os.makedirs(RAW2, exist_ok=True)
    os.makedirs(OUT, exist_ok=True)
    scenes = load_prompts()
    keys = sorted(scenes.keys())
    if "--only" in sys.argv:
        keys = [k for k in keys if k in sys.argv[sys.argv.index("--only") + 1:]]
    results = {}
    with ThreadPoolExecutor(max_workers=6) as ex:
        for key, status in ex.map(lambda k: generate(k, scenes[k]), keys):
            results[key] = status
            print(key, status, flush=True)
    # F7: serial retry pass for failures
    failed = [k for k, s in results.items() if s.startswith("FAIL")]
    for k in failed:
        time.sleep(3)
        k2, status = generate(k, scenes[k])
        results[k] = status
        print("retry", k, status, flush=True)
    print("--- post-processing ---")
    report = {}
    for key in keys:
        src = os.path.join(RAW2, key + ".png")
        if not os.path.exists(src) or os.path.getsize(src) < 10000:
            report[key] = ["missing source"]
            print(key, "MISSING SOURCE", flush=True)
            continue
        try:
            cv, cap_px = pad_and_caption(src, key, caption_for(key))
            issues = audit(src, cv, key, cap_px)
            ok = save_with_retry(cv, os.path.join(OUT, key + ".png"))
            report[key] = issues if ok else issues + ["F8 save failed"]
            print(key, "assembled", report[key] or "QA-OK", flush=True)
        except Exception as e:
            report[key] = ["process error: %s" % e]
            print(key, "ERROR", e, flush=True)
    fails = {k: v for k, v in report.items() if v}
    print("=== SUMMARY: %d ok, %d flagged ===" % (len(report) - len(fails), len(fails)))
    for k, v in fails.items():
        print("FLAG", k, v)
    # F9: caption <-> image coherence audit (pipeline-wide rule)
    coh = os.path.join(os.path.dirname(HERE), "scripts", "caption_coherence.py")
    if os.path.exists(coh):
        r = subprocess.run([sys.executable, coh, HERE], capture_output=True, text=True)
        print(r.stdout.strip())
        if r.returncode != 0:
            print("F9 COHERENCE FAILED: fix captions.json and re-run post-processing")
    else:
        print("F9 coherence script missing:", coh)

if __name__ == "__main__":
    main()
