# Final production driver: Gemini N1 + dilation + assembly
# Generates via Gemini 2.5-flash-image API, upscales, thickens, and assembles.
import sys, os, json, urllib.request, base64, time, subprocess, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import batch_generate as B

HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR_RAW = os.path.join(HERE, "gemini_raw")
OUTDIR_FINAL = os.path.join(HERE, "final_art")
API = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent"

def gen(scene_key, key):
    prompt = B.load_prompts()[scene_key] + " " + B.SUFFIX
    body = json.dumps({'contents': [{'parts': [{'text': prompt}]}],
                       'generationConfig': {'responseModalities': ['IMAGE'], 'imageConfig': {'aspectRatio': '3:4'}}}).encode()
    req = urllib.request.Request(API, data=body, method="POST",
        headers={'x-goog-api-key': key, 'Content-Type': 'application/json'})
    r = urllib.request.urlopen(req, timeout=240)
    d = json.loads(r.read())
    raw = base64.b64decode(d['candidates'][0]['content']['parts'][0]['inlineData']['data'])
    p = os.path.join(OUTDIR_RAW, scene_key + ".png")
    open(p, "wb").write(raw)
    return p

def process(src, key, caption):
    from PIL import Image, ImageFilter, ImageOps, ImageFont, ImageDraw
    img = Image.open(src).convert("L")
    img = ImageOps.autocontrast(img, cutoff=1)
    big = img.resize((2550, 3300), Image.LANCZOS)
    sharp = big.point(lambda p: 0 if p < 120 else 255)
    thick = sharp.filter(ImageFilter.MinFilter(9))
    bbox = thick.point(lambda p: 255 - p).getbbox()
    ink_cx = (bbox[0] + bbox[2]) / 2 if bbox else thick.width / 2
    ink_cy = (bbox[1] + bbox[3]) / 2 if bbox else thick.height / 2
    x_p = int((B.CANVAS_W - thick.width) / 2 + (B.CANVAS_W/2) - ink_cx)
    y_p = int(150 + (2830 - 150 - thick.height) / 2 + (2680/2) - ink_cy)
    x_p = max(90, min(x_p, B.CANVAS_W - thick.width - 90))
    y_p = max(150, min(y_p, 2830 - thick.height + 120))
    canvas = Image.new("L", (B.CANVAS_W, B.CANVAS_H), 255)
    canvas.paste(thick, (x_p, y_p))
    d = ImageDraw.Draw(canvas)
    size = 115
    font = ImageFont.truetype(B.FONT, size)
    while size > 55 and d.textbbox((0, 0), caption, font=font)[2] > B.CANVAS_W - 300:
        size -= 5; font = ImageFont.truetype(B.FONT, size)
    bbox = d.textbbox((0, 0), caption, font=font)
    d.text(((B.CANVAS_W-bbox[2]+bbox[0])//2, 2880), caption, fill=0, font=font)
    m = re.match(r"page_(\d+)", key)
    number = str(int(m.group(1)) * 2 - 1)
    numf = ImageFont.truetype(B.FONT, 62)
    nb = d.textbbox((0, 0), number, font=numf)
    d.text((B.CANVAS_W - 130 - (nb[2] - nb[0]), 3010), number, fill=120, font=numf)
    return canvas

def main():
    os.makedirs(OUTDIR_RAW, exist_ok=True); os.makedirs(OUTDIR_FINAL, exist_ok=True)
    key = open(os.path.join(HERE, 'recraft', 'key.tmp')).read().strip() # Gemini key in old place for now
    for t in ('page_01', 'page_09', 'page_41'):
        try:
            print("generating", t, "...")
            src = gen(t, key)
            print("assembling", t, "...")
            cv = process(src, t, B.caption_for(t))
            cv.save(os.path.join(OUTDIR_FINAL, '%s_final.png' % t), dpi=(300,300))
            print(t, "done")
        except Exception as e:
            print(t, "ERROR", e)

if __name__ == "__main__":
    main()
