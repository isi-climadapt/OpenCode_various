# -*- coding: utf-8 -*-
# Author 3 Book 2 - Who Frosted My Tree? Page art via OpenArt CLI, hybrid pipeline
# (copied from book1\gen_pages.py, rule 15; scenes from BOOK2-PLAN.md):
#   1. draft:  nano-banana-pro (1024 px) with the character sheet(s) as references
#   2. refine: ideogram-4-5 image2image with [draft, sheet] as references -> 2048 px
# Same cast as Book 1, so the Book 1 sheets are the references (no new character test).
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
SHEETS = os.path.join(HERE, "..", "book1", "char_test")
SHEET = os.path.join(SHEETS, "sheet_nbpro.png")
CAST = os.path.join(SHEETS, "sheet_cast.png")
EXE = r"C:\Users\ibian\AppData\Local\Programs\openart\bin\openart.exe"
DRAFT_MODEL, REFINE_MODEL = "nano-banana-pro", "ideogram-4-5"

# Book 1's look gone wintry: snow white and cream, twilight violet and dusky blue, moonlight
# silver, the gum tree's warm ochre and pink bark as the color accent. Night snow glows blue and
# violet, never flat gray.
STYLE = ("Children's picture book illustration. Soft gouache and colored-pencil look with visible "
         "paper grain, rounded chunky character shapes, gentle line work, no heavy outlines. "
         "Winter palette of soft snow white and cream, twilight violet and dusky blue, moonlight "
         "silver, with warm ochre and pink gum-tree bark and eucalyptus greens as accents. Snow at "
         "night glows blue and violet, never flat gray. Warm, funny, expressive. No words, "
         "letters, numbers, signs or text anywhere in the image.")
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
# Text space wording: "calm, plain area" made nano-banana-pro paint a flat band with a hard edge
# (Book 1 batch 1). "Open sky, empty" blends into the scene.
SKY = (" is open sky, empty, for text, painted with the same soft texture and gentle gradient as "
       "the rest of the picture and continuous with the scene below: no hard edge, no flat band, "
       "no separate panel.")
TOP = "The top third of the image" + SKY
TOP40 = "The top 40 percent of the image" + SKY
SNOWTREE = "a gum tree with smooth bark in cream, pink and ochre, every branch thick with snow"

# id: (kind, uses_cast_sheet, scene)
PAGES = {
    "p01": ("vig", False, f"{BANJO} peeking out of a round hollow in a short piece of gum-tree trunk, "
            "only his eyes, ears, nose and front paws showing over the rim, curious. A little cap of "
            "snow sits on the rim of the hollow above his ears. Small vignette in the middle of the "
            "page with lots of empty white space above and below."),
    "p03": ("full", False, "Winter dusk in the hills of the Australian bush. A tall gum tree seen "
            "from far away so the whole tree fits, a round hollow halfway up its trunk. Bare, "
            "rolling hills behind, heavy violet and blue clouds rolling in, a cold wind bending the "
            "grass. No snow on the ground yet. No animals anywhere in this picture: no sugar "
            "gliders, no koalas, the hollow is empty and dark. " + TOP),
    "p04": ("full", False, f"Cold winter dusk. A smooth gum-tree trunk rises from the bottom edge to "
            f"the top edge of the picture on the right side. Low on the trunk, {BANJO} sits in the "
            "mouth of his round hollow, wrapping his long fluffy tail around his nose and "
            "shivering, curled into a tight fluffy ball. To the left of the trunk, a wide dusky blue "
            "and violet sky with heavy clouds fills the upper part of the picture, open and empty "
            "for text, with no hard edges or bands."),
    "p05": ("vig", False, f"Three small separate vignettes in a row across the middle of the page, "
            f"the same {BANJO} curled up asleep in a round tree hollow in each: in the first, a "
            "small crescent moon above the hollow; in the second, a small sun above it; in the "
            "third, a small moon above it and the first tiny snowflakes falling. No frames. Lots of "
            "empty white space at the top."),
    # batch 2: TOP gave a flat sky band; trunk-edge-to-edge layout instead
    "p06": ("full", False, "Pale violet early evening. A thick gum-tree trunk covered in fresh "
            "white snow rises from the bottom edge to the top edge of the picture on the right "
            f"two-thirds. Low on the trunk, {BANJO}'s head pokes out of a round hollow whose rim "
            "is piled with snow, eyes enormous, mouth open in shock. To the left of the trunk, a "
            "pale violet sky with a few falling snowflakes fills the upper part of the picture, "
            "open and empty for text, one continuous painted sky with no hard edges or bands."),
    # batch 1: TOP gave a flat sky band with a hard edge; the Book 1 p04 layout (trunk edge to
    # edge, sky beside it) fixed the same fault there
    "p07": ("full", False, f"Evening. The trunk of {SNOWTREE} rises from the bottom edge to the top "
            "edge of the picture on the left side, one thick snowy branch reaching right across "
            f"the lower half. {BANJO} stands on that branch holding up a pawful of snow toward the "
            "viewer like evidence, outraged. Snowy hills far below. To the right of the trunk, a "
            "pale violet evening sky fills the upper part of the picture, open and empty for text, "
            "one continuous painted sky with no hard edges or bands."),
    "p08": ("full", False, f"Evening, high in {SNOWTREE}. In the top fork, {OLIVE} asleep hugging "
            "the branch, completely covered in a thick layer of snow except one fluffy ear and her "
            f"big black nose. {BANJO} bouncing on the branch beside her, paws out, eyes wide and "
            "alarmed. " + TOP),
    "p09": ("vig", False, f"{OLIVE} sitting on a short snowy branch with one eye half open and the "
            "other closed, unbothered, a round cap of snow on her head like a hat. Beside her "
            f"{BANJO} stands in a determined pose, chin up, paws on hips. White space at the top "
            "and bottom."),
    "p10": ("full", True, f"Evening in {SNOWTREE}. {COCKY} perched on a snowy branch, so white it "
            f"almost disappears into the snow, only its yellow crest, dark eye and black beak "
            f"showing clearly. {BANJO} tiptoeing along the branch toward it, holding a paw to his "
            "lips. " + TOP),
    "p11": ("full", True, f"{COCKY} on a snowy branch, puffed up and cross, beak open in a loud "
            "squawk, its yellow crest flopping sideways in the cold. "
            f"{BANJO} on the same branch, peering closely at its feathers and counting on his "
            "toes, confused. " + TOP),
    "p12": ("full", False, "Dusk in the snowy bush, big soft snowflakes falling everywhere. "
            f"{BANJO} stands in the snow holding out one paw, a single big star-shaped snowflake "
            "resting on it, and stares at it in wonder. " + TOP),
    # batch 2: copied the sheet layout (four Banjos, two koalas); now told it is not a sheet
    "p13": ("vig", False, "This is a story page, not a character sheet: no koala, no other "
            f"animals, no standing poses. Three small separate vignettes of {BANJO} down the left "
            "half of the page, each a little snowy scene: "
            "at the top, staring at his own wet empty paw, puzzled; in the middle, bending low to "
            "follow a line of tiny footprints in the snow; at the bottom, a serious thinking face "
            "with a paw on his chin and a blob of snow on his nose. No frames. The right half of the "
            "page is empty white."),
    "p14": ("full", True, f"Evening in the snowy bush. {POSSUM} sitting up in the snow, its whole "
            "face covered in white snow like a big white beard, blinking. Behind it, a "
            f"possum-shaped dent in a snowbank. {BANJO} pointing an accusing paw at it, "
            "triumphant. " + TOP),
    "p15": ("vig", True, "A snowbank with three possum-face-shaped holes in a row, as if someone "
            f"fell into it face first three times. {POSSUM} beside the snowbank, shaking snow off "
            f"its ears, embarrassed. {BANJO} looking at the holes, eyebrows raised. White space at "
            "the top."),
    "p16": ("full", True, f"Evening in the snowy bush. {WOMBAT} pushing a big round snowball almost "
            "as tall as itself across the snow with its head and front paws, a long rolled track "
            f"behind it. {BANJO} on a low snowy branch staring at it, amazed. " + TOP),
    # batch 2: added a koala, possum, cockatoo, kookaburra and the (missing) echidna; cast sheet
    # dropped and the animals limited to two
    "p17": ("full", False, "Only two animals in this picture: Banjo and the hidden wombat. No "
            "koala, no possum, no birds, no echidna. Evening in the snowy bush. A gum-tree trunk on the left rises from the "
            "bottom edge to the top edge of the picture, with one low branch reaching right. "
            f"{BANJO} hangs upside down by his back paws from that low branch. Below, a giant "
            "snowball as big as a small hill rolls across the snow, and only the four stubby feet "
            "of a wombat show beneath it, pushing. Above the branch, a dusky violet sky fills the "
            "upper part of the picture, open and empty for text, one continuous painted sky with "
            "no hard edges or bands."),
    "p18": ("full", False, "Evening at the foot of a snowy gum tree. A fallen log under thick snow, "
            "with a small hollow at one end where an animal usually sleeps, now empty and filled "
            f"with snow. {BANJO} peering into the empty hollow, worried. No other animals. " + TOP),
    "p19": ("vig", False, f"{BANJO} shouting up at the sky with both paws in the air, very "
            "dramatic, snowflakes bouncing off the top of his head. White space at the top and "
            "bottom."),
    "p20": ("full", False, "Moonlit night in the snowy bush, everything still and quiet, blue-white "
            "and silver under the moon. A tall gum tree with snowy branches stands on the right "
            "side, snowy hills behind. No animals. " + TOP),
    "p21": ("full", False, "Moonlit night in the snowy bush, blue-white and silver. At the foot of "
            f"the gum tree, a snow-covered fallen log. {BANJO}, very small, sits in the snow beside "
            "the log with his tail wrapped round his feet, sad and lonely. Near the log, a small "
            "round mound of snow with the tips of a few cream-yellow spines just poking through, "
            "easy to miss. " + TOP),
    "p22": ("full", False, f"Moonlit night at the foot of the snowy gum tree. {OLIVE}, awake with "
            f"both eyes open and snow on her head, sitting in the snow beside {BANJO}. Olive calm "
            "and kind, explaining; Banjo listening with wide eyes. Snowflakes drifting down. "
            + TOP40),
    "p23": ("vig", True, "A cutaway view of a snowbank beside a fallen log: above the line of the "
            f"snow, {BANJO}'s face pressed against the snow, eyes wide. Below, inside a cozy hollow "
            f"under the snow, {ECHIDNA} curled up fast asleep with its eyes shut, a tiny puff of "
            "breath mist at its snout. White space at the top."),
    "p24": ("full", True, f"Evening under the snowy gum tree. {BANJO} standing in the snow in front "
            f"of {COCKY}, {POSSUM} and {WOMBAT}, all gathered together; Banjo apologizing shyly with "
            "his paws together, the others smiling. Snowflakes drifting down. " + TOP),
    "p25": ("vig", True, "Four small separate vignettes, one in each corner of the page: top left, "
            f"{COCKY} lying on its back in the snow flapping its wings to make a bird-shaped snow "
            f"angel; top right, {POSSUM} proudly standing beside a lopsided snow sculpture of a "
            "possum; bottom left, a giant snowball with a gum-nut nose and two eucalyptus-leaf eyes, "
            f"{WOMBAT} beside it; bottom right, a small round snowy mound with a single gum leaf on "
            "top like a pillow and the tips of a few cream-yellow spines peeking out. No frames. "
            "Empty white space in the middle."),
    "p26": ("full", False, f"Snowy evening. {BANJO} crouched on the end of a high snowy branch of "
            f"the gum tree, grinning, ready to leap. {OLIVE} sits lower in the tree with snow on her "
            "head, watching with a small smile. Big soft snowflakes falling. " + TOP),
    "p27": ("full", False, f"{BANJO} mid-glide through falling snowflakes, membrane spread wide, "
            "tongue out catching a snowflake, laughing with joy, snowy hills and gum trees far "
            "below. Twilight violet sky full of big soft flakes. " + TOP),
    "p28": ("full", False, "A pink and gold winter dawn over snowy hills in the Australian bush. "
            f"{BANJO} yawning as he climbs into his round hollow in the snowy gum trunk, sleepy. "
            + TOP),
    "p29": ("vig", False, f"A round white snow-koala on a snowy branch: {OLIVE} completely buried "
            "under a big lump of snow that has just fallen on her, only her black nose and one "
            f"fluffy ear showing. {BANJO} peeking out of his hollow just above, mouth open in "
            "surprise. White space at the top."),
    "p32": ("vig", False, f"{BANJO} curled up asleep in his round tree hollow, tail wrapped around "
            "him, a little cap of snow on the rim of the hollow, small and cozy. Small vignette in "
            "the middle of the page."),
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

def draft_job(pid):
    kind, cast, scene = PAGES[pid]
    refs = [SHEET] + ([CAST] if cast else [])
    # "appears once" added after Book 1 p26 showed Banjo 4 times and Olive twice
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

def check():
    for ref in (SHEET, CAST):
        print(("ok      " if os.path.exists(ref) else "MISSING ") + os.path.normpath(ref))
    for pid in PAGES:
        model, prompt, path, refs = draft_job(pid)
        print(f"{pid} {PAGES[pid][0]:4} cast={PAGES[pid][1]!s:5} {len(prompt):4} chars: {PAGES[pid][2][:70]}")
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
