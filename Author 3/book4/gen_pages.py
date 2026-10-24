# -*- coding: utf-8 -*-
# Author 3 Book 4 - Who Took My Pouch? Page art via OpenArt CLI, hybrid pipeline
# (copied from book3\gen_pages.py, rule 15; scenes from BOOK4-PLAN.md):
#   1. draft:  nano-banana-pro (1024 px) with the character sheet(s) as references
#   2. refine: ideogram-4-5 image2image with [draft, sheets] as references -> 2048 px
# char_test\sheet_hero.png (Clover, Hugo) on every page; char_test\sheet_extra.png (Mom, the baby,
# Pelican) and Book 1's cast sheet (wombat, possum, echidna) where the page needs them.
# Ideogram takes up to 5 references, so draft + 3 sheets fits.
# ≤6 workers, F7 retry. About 84 credits per page (40 + 44).
# Usage: py gen_pages.py check                 # print every prompt, no CLI calls, no credits
#        py gen_pages.py batch p01 p03 ...    # draft + refine these pages
#        py gen_pages.py refine p05 ...       # refine only (draft already in drafts\)
#        py gen_pages.py batch all
# Cached: files >10KB are skipped; delete a file to regenerate it.

import os, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
DRAFTS = os.path.join(HERE, "drafts")     # nano-banana-pro 1024 px
PAGES_DIR = os.path.join(HERE, "pages")   # ideogram 2048 px finals
SHEET = os.path.join(HERE, "char_test", "sheet_hero.png")
EXTRA = os.path.join(HERE, "char_test", "sheet_extra.png")
CAST = os.path.join(HERE, "..", "book1", "char_test", "sheet_cast.png")
NEW = EXTRA
REFS = {"x": EXTRA, "c": CAST}
EXE = r"C:\Users\ibian\AppData\Local\Programs\openart\bin\openart.exe"
DRAFT_MODEL, REFINE_MODEL = "nano-banana-pro", "ideogram-4-5"

# The house look in daylight: golden grass, warm red earth, eucalyptus sage greens, soft blue sky.
STYLE = ("Children's picture book illustration. Soft gouache and colored-pencil look with visible "
         "paper grain, rounded chunky character shapes, gentle line work, no heavy outlines. "
         "Sunny Australian grassland palette of golden grass, warm red-ochre earth, eucalyptus sage "
         "greens and soft clear blue sky, with cream and pink gum-tree bark. Warm, funny, "
         "expressive. No words, letters, numbers, signs or text anywhere in the image.")
FULL = "Full-bleed square painting that runs to every edge, no white border, no frame."
VIG = ("Vignette on a plain white background: the painting has soft edges that fade into white, "
       "no frame, no border line, no box.")

CLOVER = ("Clover the young kangaroo joey (small, warm caramel-fawn fur, cream belly and cheeks, "
          "very big upright pink-lined ears, huge glossy dark brown eyes, small black nose, one "
          "little tuft of fur on top of her head, long narrow feet, long thick tail)")
HUGO = ("Hugo the quokka (small chunky round wallaby, brown-gray fur, short rounded ears, wide "
        "happy smile, rosy cheeks, thin tail)")
MOM = ("Clover's mom, a tall adult kangaroo (soft gray-fawn fur, cream belly, gentle kind face, "
       "big ears, a pouch on her tummy)")
WOMBAT = "a mother wombat (brown, round, square-ish nose, small ears, stubby legs)"
PELICAN = ("an Australian pelican (white body, black wing feathers, very long pale pink bill with "
           "a stretchy throat pouch)")
POSSUM = "a mother brushtail possum (gray, bushy black tail, pink nose, big pink ears)"
ECHIDNA = "an echidna (round brown body covered in cream and brown spines, long thin snout)"
# Text space wording from Books 1-3: "open sky, empty" blends into the scene.
SKY = (" is open sky, empty, for text, painted with the same soft texture and gentle gradient as "
       "the rest of the picture and continuous with the scene below: no hard edge, no flat band, "
       "no separate panel.")
TOP = "The top third of the image" + SKY
TOP40 = "The top 40 percent of the image" + SKY
GUM = "a gum tree with smooth cream, pink and ochre bark and sage-green leaves"
DAY = "Sunny morning in the Australian grassland, tall golden grass, scattered gum trees"

# id: (kind, extra reference sheets: "x" = Book 4 extra sheet, "c" = Book 1 cast sheet, scene)
PAGES = {
    "p01": ("vig", "x", f"{MOM} seen from the side, only her tummy, legs and tail. {CLOVER} is "
            "diving head-first into her mom's pouch: only Clover's long back feet and long tail "
            "stick out of the pouch, kicking happily. Small vignette in the middle of the page "
            "with lots of empty white space above and below."),
    "p03": ("full", "x", "Early golden sunrise over wide Australian grassland, tall golden grass, "
            f"red earth, a few gum trees, soft hills far away. In the middle distance, {MOM} "
            f"stands in the grass with {CLOVER}'s head and ears poking out of her pouch, small in "
            "the wide landscape. " + TOP),
    "p04": ("full", "x", f"{DAY}. {MOM} hops across the grass, and {CLOVER} rides in her pouch "
            "with her head, front paws and big ears out, ears flapping in the wind, grinning with "
            "joy. " + TOP),
    "p05": ("vig", "x", "Three small separate vignettes in a row across the middle of the page, "
            f"each showing {CLOVER} in her mom's pouch (only the mom's tummy and pouch shown, gray-"
            "fawn fur): in the first, Clover asleep in the pouch with only her ears and nose "
            "showing; in the second, Clover in the pouch munching a stalk of golden grass; in the "
            "third, Clover in the pouch bouncing, ears flying up. No frames. Lots of empty white "
            "space at the top."),
    "p06": ("full", "x", f"{DAY}. {CLOVER} bounces backward off her mom's tummy, the pouch shut "
            "tight, little dizzy stars and swirls around Clover's head, ears flopping, a surprised "
            f"funny face. Only the lower half of {MOM} is shown on the right side of the picture. "
            "To the left, a wide soft blue sky fills the upper part of the picture, open and "
            "empty for text, one continuous painted sky with no hard edges or bands."),
    "p07": ("full", "x", f"{DAY}. {MOM} stands under {GUM}, bending her head down to lick inside "
            "the top of her own pouch, busy cleaning it, eyes closed calmly. "
            f"{CLOVER} stands in front of her with her mouth open in shock, paws up. To the "
            "right, the sky fills the upper part of the picture, open and empty for text, one "
            "continuous painted sky with no hard edges or bands."),
    "p08": ("full", "", f"{DAY}. {HUGO} sits calmly in the grass at the foot of {GUM}, smiling "
            f"his wide happy smile. {CLOVER} bounds up to him, paws out, big ears straight up, "
            "eyes wide and alarmed. " + TOP),
    "p09": ("vig", "", f"{CLOVER} standing in a determined detective pose, chin up, paws on "
            f"hips, big ears straight up. Beside her {HUGO} sits calmly nibbling a green leaf, "
            "smiling. A few tufts of golden grass under them. White space at the top and bottom."),
    "p10": ("full", "c", f"{DAY}. A fallen gum log in the grass with a burrow dug under it, a "
            f"spray of red earth flying. {WOMBAT} backs out of the burrow. {CLOVER} stands on "
            "top of the log pointing an accusing paw at the wombat. " + TOP),
    # test 24 Oct: the pouch read as a front pouch. v2 (with the Book 1 cast sheet) filled the
    # scene with extra animals: v3 uses no cast sheet and names the only two animals
    "p11": ("full", "", "Only two animals in this picture: one wombat and Clover. No other "
            f"animals, no birds, no quokka. {DAY}. A brown, round mother wombat stands on all "
            "four short legs in side view, her head on the left, looking back over her shoulder "
            "and smiling. Under her belly, right between her back legs, a tiny baby wombat pokes "
            "its head out of her pouch, which opens toward her tail; the baby looks backward and "
            f"waves one little paw. {CLOVER} stands on the right looking sorry, ears drooping. "
            + TOP),
    "p12": ("full", "x", f"A sunny waterhole in the Australian bush, blue water, reeds and red "
            f"earth banks. {PELICAN} stands at the water's edge with its throat pouch hugely "
            f"full and bulging. {CLOVER} leaps onto the bank pointing at it in triumph. " + TOP),
    "p13": ("vig", "x", f"{PELICAN} with its long beak open, a small silver fish leaping out of "
            f"its throat pouch with a splash of water drops. {CLOVER} beside it, startled, ears "
            "back, getting splashed. White space at the top."),
    "p14": ("full", "c", f"{DAY}. {POSSUM} sits on a low branch of {GUM}, with a big round "
            "lump hidden under her bushy tail on her back, wriggling. "
            f"{CLOVER} stands at the foot of the tree looking up suspiciously, pointing. " + TOP),
    "p15": ("vig", "c", f"{POSSUM} on a short branch with a fuzzy little baby possum riding on "
            "her back, hugging her fur and grinning. "
            f"{CLOVER} below on the grass, giggling with her paws over her mouth. "
            "White space at the top."),
    "p16": ("full", "", f"Hot midday sun over golden grassland, heat shimmer, red earth. {CLOVER} "
            "trudges along alone, tired, ears drooping, feet dragging, little puffs of dust. "
            + TOP),
    "p17": ("full", "", "Only one animal in this picture: Clover. "
            f"{DAY}. The trunk of {GUM} rises from the bottom edge to the top edge on the right. "
            f"In its shade, {CLOVER} tries to curl up in a lumpy tussock of grass to nap, "
            "uncomfortable and grumpy, legs and tail sticking out. To the left of the trunk, the "
            "soft blue sky fills the upper part of the picture, open and empty for text, one "
            "continuous painted sky with no hard edges or bands."),
    "p18": ("full", "c", f"{DAY}, late afternoon light. {ECHIDNA} waddles proudly through the "
            f"grass. {CLOVER} leaps toward it mid-hop, pointing, shouting in triumph. " + TOP),
    "p19": ("vig", "c", f"{ECHIDNA} sitting up proudly, patting its round tummy with one paw. "
            f"{CLOVER} beside it, staring, her big ears shooting straight up with a new idea. "
            "White space at the top."),
    "p20": ("full", "", "Sunset over Australian grassland: pink and orange sky, the golden grass "
            "turning pink, long shadows, gum trees in silhouette, a few far-off kangaroos and "
            "birds heading home in the distance, very small. No characters up close. " + TOP),
    "p21": ("full", "", "Only one animal in this picture: Clover. Dusk in the grassland, pink and "
            "violet sky. A low round rock sits in the lower right of the picture. "
            f"{CLOVER}, very small, sits alone on the rock, hugging her own long tail, sad and "
            "lonely, ears drooping. Above her, the dusky sky fills the upper part of the picture, "
            "open and empty for text, one continuous painted sky with a soft gradient, no hard "
            "edges, no flat bands."),
    "p22": ("full", "", f"Dusk in the grassland, pink and violet sky. {HUGO} sits beside {CLOVER} "
            "on a low rock, one arm around her, smiling his biggest kind smile; Clover looks up "
            "at him, a little hopeful. " + TOP40),
    "p23": ("vig", "x", f"Close-up: {CLOVER} peeking into the open top of her mom's pouch (only "
            "the mom's gray-fawn tummy and pouch shown), her face full of wonder, a warm glow "
            "from inside. Inside the pouch, a tiny pink baby kangaroo no bigger than a jellybean, "
            "curled up asleep, cute and simple. White space at the top."),
    "p24": ("full", "x", f"Dusk, soft pink and gold light in the grassland. {MOM} hugs {CLOVER} "
            "with both arms, a big warm hug, Clover's eyes closed happily. A little way off, "
            f"{HUGO} watches, smiling. " + TOP),
    "p25": ("vig", "x", "Four small separate vignettes, one in each corner of the page, each a "
            f"sunny grassland scene: top left, {CLOVER} hopping high over a little bush; top "
            f"right, Clover racing {HUGO} through the grass; bottom left, Clover napping "
            "curled up at her mom's feet (only the mom's legs and tail shown); bottom right, "
            "Clover with her head inside her mom's pouch drinking, only Clover's back half, tail "
            "and feet showing. No frames. Empty white space in the middle."),
    "p26": ("full", "xc", f"{DAY}. {MOM} stands in the grass with a little bulge in her pouch. "
            f"{CLOVER} stands guard in front of her, chest puffed out proudly. Visitors gather "
            f"around: {WOMBAT}, {PELICAN}, {POSSUM} and {ECHIDNA}, all smiling. " + TOP),
    "p27": ("full", "x", f"Golden morning in the grassland. {MOM} stands in the grass; a tiny "
            "baby kangaroo's head with two little ears and big dark eyes peeks out of her pouch. "
            f"{CLOVER} stands on tiptoe nose to nose with the baby, smiling proudly. " + TOP),
    "p28": ("full", "x", "Night in the Australian grassland, deep indigo sky full of stars, a "
            f"silver moon. {MOM} lies resting in the grass. {CLOVER} is curled up asleep against "
            "her mom's legs, cozy. Just the baby's tiny ears poke out of the pouch. " + TOP),
    "p29": ("vig", "x", f"Morning. {MOM} with the baby kangaroo poking its head out of her "
            "pouch, the baby holding the pouch rim with both tiny paws, looking cheeky and "
            f"bossy. {CLOVER} in front, laughing with her paws on her tummy. {HUGO} beside her, "
            "smiling. White space at the top."),
    "p32": ("vig", "", f"{CLOVER} curled up asleep in a cozy nest of golden grass, tail wrapped "
            "around her, small and peaceful. Small vignette in the middle of the page."),
}

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

def sheets(pid):
    return [SHEET] + [REFS[k] for k in PAGES[pid][1]]

def draft_job(pid):
    kind, _, scene = PAGES[pid]
    # "appears once" added after Book 1 p26 showed Banjo 4 times and Olive twice
    lead = ("Use the attached character sheet(s) as the exact design for every character, not as a "
            "layout: each character appears only once in the picture. Square page. ")
    return (DRAFT_MODEL, lead + scene + " " + (FULL if kind == "full" else VIG) + " " + STYLE,
            os.path.join(DRAFTS, pid + ".png"), sheets(pid))

def refine_job(pid):
    kind, _, scene = PAGES[pid]
    refs = [os.path.join(DRAFTS, pid + ".png")] + sheets(pid)
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

def check():
    for ref in (SHEET, EXTRA, CAST):
        print(("ok      " if os.path.exists(ref) else "MISSING ") + os.path.normpath(ref))
    for pid in PAGES:
        model, prompt, path, refs = draft_job(pid)
        print(f"{pid} {PAGES[pid][0]:4} refs={PAGES[pid][1] or '-':3} {len(prompt):4} chars: {PAGES[pid][2][:60]}")
    print(f"{len(PAGES)} pages, about {len(PAGES) * 84} credits before retries")

def main():
    cmd, ids = sys.argv[1], sys.argv[2:]
    if cmd == "check":
        check()
        return
    os.makedirs(DRAFTS, exist_ok=True)
    os.makedirs(PAGES_DIR, exist_ok=True)
    if ids == ["all"]:
        ids = list(PAGES)
    if cmd == "batch":
        run_all([draft_job(p) for p in ids])
    run_all([refine_job(p) for p in ids if os.path.exists(os.path.join(DRAFTS, p + ".png"))])

if __name__ == "__main__":
    main()
