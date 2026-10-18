# -*- coding: utf-8 -*-
# Author 3 Book 1 - Who Peeled My Tree? Page art via OpenArt CLI, hybrid pipeline
# (locked after the character test, see BOOK1-PLAN.md):
#   1. draft:  nano-banana-pro (1024 px) with the character sheet(s) as references
#   2. refine: ideogram-4-5 image2image with [draft, sheet] as references -> 2048 px
# Engine = char_test.py (cache + F7 retry), ≤6 workers.
# Usage: py gen_pages.py cast                 # supporting cast sheet
#        py gen_pages.py batch p01 p03 ...    # draft + refine these pages
#        py gen_pages.py refine p05 ...       # refine only (draft already in drafts\)
#        py gen_pages.py batch all
# Cached: files >10KB are skipped; delete a file to regenerate it.

import os, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
DRAFTS = os.path.join(HERE, "drafts")     # nano-banana-pro 1024 px
PAGES_DIR = os.path.join(HERE, "pages")   # ideogram 2048 px finals
SHEET = os.path.join(HERE, "char_test", "sheet_nbpro.png")
CAST = os.path.join(HERE, "char_test", "sheet_cast.png")
EXE = r"C:\Users\ibian\AppData\Local\Programs\openart\bin\openart.exe"
DRAFT_MODEL, REFINE_MODEL = "nano-banana-pro", "ideogram-4-5"

STYLE = ("Children's picture book illustration. Soft gouache and colored-pencil look with visible "
         "paper grain, rounded chunky character shapes, gentle line work, no heavy outlines. "
         "Palette of eucalyptus greens, warm ochre and terracotta bark, twilight violet and dusky "
         "blue, moonlight silver. Warm, funny, expressive. No words, letters, numbers, signs or "
         "text anywhere in the image.")
FULL = "Full-bleed square painting that runs to every edge, no white border, no frame."
VIG = ("Vignette on a plain white background: the painting has soft edges that fade into white, "
       "no frame, no border line, no box.")

BANJO = ("Banjo the sugar glider (small and round, soft blue-gray fur, cream belly and cheeks, one "
         "black stripe from between his eyes over his head and down his back, huge glossy black "
         "eyes, small pink nose, round pink-lined ears, cream-edged gliding membrane between front "
         "and back paws, long fluffy gray tail with a black tip)")
OLIVE = ("Olive the koala (chunky and round, silver-gray fur, white chest, big fluffy white-edged "
         "ears, large black leathery nose)")
COCKY = "a sulphur-crested cockatoo (white, yellow crest)"
POSSUM = "a common brushtail possum (gray, bushy black tail, pink nose, big ears)"
ECHIDNA = "a short-beaked echidna (brown body, cream-yellow spines, long thin snout)"
WOMBAT = "a common wombat (brown, round, square-ish nose, small ears, stubby legs)"
KOOKA = "a laughing kookaburra (brown and cream, big beak)"
# Text space wording: "calm, plain area" made nano-banana-pro paint a flat band with a hard edge
# (batch 1, p03/p04/p10/p11). "Open sky, empty" (p05/p08/p21) blends into the scene.
SKY = (" is open sky, empty, for text, painted with the same soft texture and gentle gradient as "
       "the rest of the picture and continuous with the scene below: no hard edge, no flat band, "
       "no separate panel.")
TOP = "The top third of the image" + SKY
TOP40 = "The top 40 percent of the image" + SKY

# id: (kind, uses_cast_sheet, scene)
PAGES = {
    "p01": ("vig", False, f"{BANJO} peeking out of a round hollow in a short piece of gum-tree trunk, "
            "only his eyes, ears, nose and front paws showing over the rim, curious. One long curl of "
            "peeled bark hangs beside the hollow. Small vignette in the middle of the page with lots "
            "of empty white space above and below."),
    "p03": ("full", False, "A tall, smooth gum tree in the Australian bush at sunset, seen from far "
            "away so the whole tree fits. Halfway up the trunk is a round hollow with a tiny sugar "
            "glider peeking out. Peach and violet sky, small gum trees and grass in the distance. " + TOP),
    "p04": ("full", False, f"Dusk. A smooth gum-tree trunk rises from the bottom edge to the top edge "
            f"of the picture on the right side. Low on the trunk, {BANJO} sits at the mouth of his "
            "round hollow, stretching his arms up and yawning, just waking up. To the left of the "
            "trunk, a wide violet and peach sky with soft clouds fills the upper part of the picture, "
            "open and empty for text, with no hard edges or bands. A few eucalyptus leaves."),
    "p05": ("full", False, f"{BANJO} mid-glide toward the viewer against a violet dusk sky over the "
            "Australian bush, membrane spread wide, joyful open mouth. The top left third of the "
            "image is open sky, empty, for text."),
    "p06": ("full", False, f"Night, close view of a smooth gum-tree trunk. {BANJO} clinging to the "
            "trunk with all four paws, nose to nose with a long curl of bark peeling away from the "
            "trunk, surprised. Moonlight. " + TOP),
    "p07": ("vig", False, f"Close-up of {BANJO} holding a long curl of peeled bark in both paws, eyes "
            "enormous, fur standing on end in shock, mouth open. Lots of white space at the top."),
    "p08": ("full", False, f"At night in a tall gum tree, {OLIVE} asleep hugging a high fork of the "
            f"tree. {BANJO} bouncing on the branch beside her, waving a long curl of peeled bark, "
            "eyes wide and alarmed. Moonlit sky. " + TOP),
    "p09": ("vig", False, f"{OLIVE} sitting on a short branch with one eye half open and the other "
            f"closed, unbothered. Beside her {BANJO} stands in a determined pose, chin up, paws on "
            "hips, holding a curl of bark. White space at the top and bottom."),
    "p10": ("full", True, f"Night in a gum tree. {BANJO} tiptoeing along a moonlit branch toward "
            f"{COCKY} asleep with its head tucked under its wing. Banjo holds a paw to his lips. " + TOP),
    "p11": ("full", True, f"Night. {COCKY} wide awake and cross on its branch, yellow crest blasting "
            f"straight up, wings out, beak open in a loud squawk. {BANJO} shrinking back nervously "
            "on the same branch, ears flat. " + TOP),
    "p12": ("full", False, "Night. The smooth trunk of a gum tree with several long ribbons of old "
            "bark hanging off it and blowing in the wind, a pile of curled bark on the ground at the "
            f"base. {BANJO}, small, at the base staring up at it. Moonlight. " + TOP),
    "p13": ("vig", False, f"Three small separate vignettes of {BANJO} down the left half of the page: "
            "at the top, measuring a strip of bark longer than he is; in the middle, peering through "
            "a big dewdrop on a eucalyptus leaf like a magnifying glass; at the bottom, a serious "
            "thinking face with a paw on his chin. No frames. The right half of the page is empty white."),
    "p14": ("full", True, f"Night. Inside a cozy tree hollow lined with leaves and feathers, {POSSUM} "
            f"curled up in its soft nest. {BANJO} at the opening of the hollow pointing an accusing "
            "paw at the nest. Warm, cozy light. The top third of the image is the dark wooden "
            "inside wall of the hollow, empty, for text, painted with the same soft texture as the "
            "rest and continuous with it: no hard edge, no flat band, no separate panel."),
    "p15": ("vig", True, f"{POSSUM} holding up a single stripy sock with a puzzled face, a few leaves "
            f"and feathers around it. {BANJO} looking at the sock, confused. White space at the top."),
    "p16": ("full", True, f"Night. A gum-tree trunk rises from the bottom edge to the top edge of the "
            f"picture on the right. At its base, {ECHIDNA} snuffling at the roots with its long nose. "
            f"{BANJO} leaping down from the trunk toward it in a dramatic pose, arms out. To the left "
            "of the trunk, moonlit night sky over the bush fills the upper part of the picture, open "
            "and empty for text, one continuous painted sky with no hard edges or bands."),
    "p17": ("full", True, f"Night at the foot of a gum tree. {ECHIDNA} pointing its long snout "
            f"straight up the trunk, a little tongue out with one ant on it. {BANJO} beside it "
            "following its gaze upward, puzzled. " + TOP),
    "p18": ("full", True, f"Night in the bush. A gum-tree trunk on the left rises from the bottom edge "
            "to the top edge of the picture, with one low branch reaching right. "
            f"{BANJO} hangs upside down by his back paws from that low branch, face to face with "
            f"{WOMBAT} trundling past below. Above the branch, moonlit night sky fills the upper part "
            "of the picture, open and empty for text, one continuous painted sky with no hard edges "
            "or bands."),
    "p19": ("vig", True, "An imagined scene: a wobbly tower of three wombats standing on each other's "
            "backs, the top one reaching for a strip of bark on a tree trunk, all three looking "
            f"grumpy and unhappy. {WOMBAT} is the design for all three. A small {BANJO} in the lower "
            "corner imagining it. No speech bubble outline. White space at the top."),
    "p20": ("full", False, "Moonlit night, cool blue palette. A gum-tree trunk almost bare of old "
            "bark, smooth new bark showing in cream, pink, gray-green and orange patches, big heaps "
            "of curled old bark at its base. No animals. " + TOP),
    "p21": ("full", False, "Moonlit night. A gum-tree trunk almost bare of old bark, smooth new bark "
            "in cream, pink, gray-green and orange patches, heaps of curled old bark at its base. "
            f"{BANJO}, very small, sitting on the bark pile with his head in his paws, sad. Cool blue "
            "palette. " + TOP),
    "p22": ("full", False, f"Moonlit night. {OLIVE}, awake with both eyes open, sitting beside "
            f"{BANJO} on a branch, both looking at the gum trunk with patchy cream, pink and green "
            "new bark. Olive calm and kind, Banjo listening with wide eyes. " + TOP40),
    "p23": ("vig", False, f"{BANJO} hugging a smooth section of gum-tree trunk with patchy cream, "
            "pink and green bark, his cheek pressed against it, eyes closed, smiling peacefully. "
            "White space at the top."),
    "p24": ("full", True, f"Night at the foot of a gum tree with patchy new bark. {BANJO} standing in "
            f"front of {COCKY}, {POSSUM}, {ECHIDNA} and {WOMBAT}, all gathered together; Banjo "
            "apologizing shyly with his paws together, the others smiling. Heaps of curled old bark "
            "around. " + TOP),
    "p25": ("vig", True, "Four small separate vignettes, one in each corner of the page: top left, "
            f"{COCKY} happily chewing a strip of bark; top right, {POSSUM} snuggled in a curl of "
            f"bark like a blanket; bottom left, {ECHIDNA} nosing under a pile of bark finding "
            f"beetles; bottom right, {WOMBAT} at the entrance of its burrow with a big flat piece of "
            "bark as a doormat. No frames. Empty white space in the middle."),
    "p26": ("full", False, f"Night. {BANJO} at the top of a tall gum-tree trunk with smooth patchy "
            f"cream, pink and green new bark, crouched and grinning, ready to slide down. {OLIVE} on "
            "a branch nearby watching with a small smile. " + TOP),
    "p27": ("full", False, f"{BANJO} sliding down a smooth, patchy, spotty gum-tree trunk at top "
            "speed, ears blown back, laughing, tail streaming behind, painted speed lines. "
            "Moonlight. " + TOP),
    "p28": ("full", True, f"Dawn in the bush, pink and gold sky. {KOOKA} on a branch laughing with "
            f"its beak wide open. {BANJO} yawning as he climbs into his round hollow in the patchy "
            "gum trunk. " + TOP),
    "p29": ("vig", False, f"{BANJO} staring in surprise at a little tuft of his own fluffy gray fur "
            f"floating in the air in front of him, mouth open. In a lower corner, {OLIVE} asleep "
            "hugging a branch. White space at the top."),
    "p32": ("vig", False, f"{BANJO} curled up asleep in his round tree hollow, tail wrapped around "
            "him, small and cozy. Small vignette in the middle of the page."),
}

CAST_PROMPT = ("Supporting character model sheet on a plain white background for the same picture "
               "book, in exactly the same art style as the attached reference sheet. Five animals, "
               f"each shown once, full body, friendly and expressive: {COCKY}; {POSSUM}; {ECHIDNA}; "
               f"{WOMBAT}; {KOOKA}. Evenly lit, no overlap. " + STYLE)

def run(model, prompt, path, refs=()):
    if os.path.exists(path) and os.path.getsize(path) > 10000:
        return path, "cached"
    cmd = [EXE, "generate", "image", prompt, "--model", model, "-o", path, "--quiet", "--yes"]
    for r in refs:
        cmd += ["--image", r]
    for attempt in range(3):  # F7: retry; reference uploads time out now and then, so pause first
        if attempt:
            time.sleep(20)
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
        if p.returncode == 0:
            return path, "ok"
    return path, "FAIL: " + (p.stderr or p.stdout)[-300:]

def draft_job(pid):
    kind, cast, scene = PAGES[pid]
    refs = [SHEET] + ([CAST] if cast else [])
    # "appears once" added after p26 showed Banjo 4 times and Olive twice, copying the sheet layout
    lead = ("Use the attached character sheet(s) as the exact design for every character, not as a "
            "layout: each character appears only once in the picture. Square page. ")
    return (DRAFT_MODEL, lead + scene + " " + (FULL if kind == "full" else VIG) + " " + STYLE,
            os.path.join(DRAFTS, pid + ".png"), refs)

def refine_job(pid):
    kind, cast, scene = PAGES[pid]
    refs = [os.path.join(DRAFTS, pid + ".png"), SHEET] + ([CAST] if cast else [])
    lead = ("Repaint the first image at high detail, keeping its exact composition, poses and facial "
            "expressions. Keep every character exactly like the character sheet(s) in the other "
            "attached images, each character appearing only once. The scene: ")
    keep = (" Extend the painting to every edge. " + FULL) if kind == "full" else (
        " Keep the plain white background around the vignette. " + VIG)
    return (REFINE_MODEL, lead + scene + keep + " " + STYLE, os.path.join(PAGES_DIR, pid + ".png"), refs)

def run_all(jobs):
    with ThreadPoolExecutor(max_workers=6) as ex:
        for path, status in ex.map(lambda j: run(*j), jobs):
            print(os.path.basename(os.path.dirname(path)) + "/" + os.path.basename(path), status)

def main():
    os.makedirs(DRAFTS, exist_ok=True)
    os.makedirs(PAGES_DIR, exist_ok=True)
    cmd, ids = sys.argv[1], sys.argv[2:]
    if ids == ["all"]:
        ids = list(PAGES)
    if cmd == "cast":
        run_all([(DRAFT_MODEL, CAST_PROMPT, CAST, [SHEET])])
        return
    if cmd == "batch":
        run_all([draft_job(p) for p in ids])
    run_all([refine_job(p) for p in ids if os.path.exists(os.path.join(DRAFTS, p + ".png"))])

if __name__ == "__main__":
    main()
