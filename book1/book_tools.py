# Book asset toolkit: shared functions for generation + assembly
import re, os
from PIL import Image, ImageOps, ImageDraw, ImageFont

W, H = 2550, 3300
ART_W = 2400
CANVAS_W, CANVAS_H = 2550, 3300
HERE = os.path.dirname(os.path.abspath(__file__))
PROMPTS_MD = os.path.join(HERE, "PAGE-GENERATION-PROMPTS.md")
CAPTIONS = os.path.join(HERE, "captions.json")
FONT = os.path.join(HERE, "fonts", "Baloo2.ttf")

SUFFIX = ("Bold and easy coloring book page for kids ages 3-8. A rich but simple scene around the "
          "animal with 6 to 8 easy elements suitable for its habitat (trees, clouds, stars, waves, "
          "rocks, flowers, smaller animal friends, bubbles, sun, grass or sand), each element drawn "
          "as one big simple closed shape. Very thick, clean, smooth black outlines (heavy, "
          "marker-friendly). Plain white background, no frame or border around the image edge. "
          "Only simple closed shapes with large open areas to colour. The main animal stays the "
          "largest thing on the page, portrait composition. Cute, friendly, happy faces with large "
          "simple eyes. No shading, no grey, no colour fill, no texture, no crosshatching. "
          "No words, letters, numbers or text anywhere in the image. Nothing in the bottom 6 "
          "percent of the page.")

def load_prompts():
    scenes = {}
    with open(PROMPTS_MD, encoding="utf-8") as f:
        for line in f:
            mm = re.match(r"\|\s*(page_\d+)\s*\|\s*[^|]+\|\s*(.+?)\s*\|", line)
            if mm and not mm.group(2).startswith("Fun-fact"):
                scenes[mm.group(1)] = mm.group(2)
    return scenes

def caption_for(key):
    import json
    with open(CAPTIONS, encoding="utf-8") as f:
        return json.load(f).get(key, "")
