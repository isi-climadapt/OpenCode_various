# -*- coding: utf-8 -*-
# Author 3 Book 3 - Who Shook My Tree? Page art via OpenArt CLI, hybrid pipeline
# (copied from book2\gen_pages.py, rule 15; scenes from BOOK3-PLAN.md):
#   1. draft:  nano-banana-pro (1024 px) with the character sheet(s) as references
#   2. refine: ideogram-4-5 image2image with [draft, sheets] as references -> 2048 px
# Book 1 sheets for Banjo, Olive and the suspects; char_test\sheet_new.png (Book 3 character test)
# for Lyrebird and the green tree frogs. Ideogram takes up to 5 references, so draft + 3 sheets fits.
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
NEW = os.path.join(HERE, "char_test", "sheet_new.png")
REFS = {"c": CAST, "n": NEW}
EXE = r"C:\Users\ibian\AppData\Local\Programs\openart\bin\openart.exe"
DRAFT_MODEL, REFINE_MODEL = "nano-banana-pro", "ideogram-4-5"

# Book 1's look on a stormy summer night: deep indigo, storm violet and slate blue, warm ochre and
# pink gum bark and rain-washed eucalyptus greens as accents. Lightning is a soft glow far away
# inside the clouds, never touching a tree or an animal.
STYLE = ("Children's picture book illustration. Soft gouache and colored-pencil look with visible "
         "paper grain, rounded chunky character shapes, gentle line work, no heavy outlines. "
         "Stormy summer night palette of deep indigo, storm violet and slate blue, with warm ochre "
         "and pink gum-tree bark and rain-washed eucalyptus greens as accents. Any lightning is only "
         "a soft lilac-white glow inside distant clouds, never a bolt striking a tree or an animal. "
         "Any rain is soft slanted streaks. Friendly, not frightening. Warm, funny, expressive. No "
         "words, letters, numbers, signs or text anywhere in the image.")
# Test page p26 (24 Oct) painted rain after the storm: the style line used to ask for rain on
# every page. Pages after the storm now say so outright.
AFTER = "The storm is over: no rain at all, no falling raindrops."
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
WOMBAT = "a common wombat (brown, round, square-ish nose, small ears, stubby legs)"
LYRE = ("a male superb lyrebird (soft brown-gray body, slim neck, small head, dark eye, long legs, "
        "a very long tail of two broad outer feathers striped brown and cream in a lyre shape, "
        "filled with fine silvery lace plumes)")
FROG = ("Australian green tree frogs (plump, bright leaf-green back, white belly, big golden eyes, "
        "round sticky toe pads, wide smiley mouth)")
# Text space wording: "calm, plain area" made nano-banana-pro paint a flat band with a hard edge
# (Book 1 batch 1). "Open sky, empty" blends into the scene.
SKY = (" is open sky, empty, for text, painted with the same soft texture and gentle gradient as "
       "the rest of the picture and continuous with the scene below: no hard edge, no flat band, "
       "no separate panel.")
TOP = "The top third of the image" + SKY
TOP40 = "The top 40 percent of the image" + SKY
TREE = "a gum tree with smooth bark in cream, pink and ochre and dark eucalyptus leaves"
NIGHT = "Stormy summer night in the Australian bush, wind in the leaves"

# id: (kind, extra reference sheets: "c" = Book 1 cast sheet, "n" = Book 3 new sheet, scene)
PAGES = {
    "p01": ("vig", "", f"{BANJO} peeking out of a round hollow in a short piece of gum-tree trunk, "
            "only his eyes, ears, nose and front paws showing over the rim, every hair of his fur "
            "standing on end, startled. One fat raindrop drips off the rim of the hollow onto his "
            "nose. Small vignette in the middle of the page with lots of empty white space above "
            "and below."),
    # batch 1: rain was already falling; the storm hasn't arrived yet
    # redo 1: flat sky band with a hard edge above the treetop; trunk-edge-to-edge layout instead
    "p03": ("full", "", "No rain yet: dry, hot, still air, no raindrops anywhere. Hot, still summer "
            f"dusk in the hills of the Australian bush, golden and violet light. {TREE} stands on the "
            "right, its trunk rising from the bottom edge to the top edge of the picture, a round "
            "hollow halfway up the trunk, its leafy branches reaching left. Golden grassy hills roll "
            "away to the left; far off over the hills, tall storm clouds are building, with a faint "
            "glow inside them. No animals anywhere in this picture: no sugar gliders, no koalas, the "
            "hollow is empty and dark. To the left of the trunk, a wide golden-violet dusk sky fills "
            "the upper part of the picture, open and empty for text, one continuous painted sky with "
            "a soft gradient, no hard edges, no flat bands, no horizontal line across the sky."),
    "p04": ("full", "", f"Summer evening. The top branch of {TREE}. {BANJO} stands at the end of "
            "the branch stretching his gliding membrane wide, looking out across a deep gully to a "
            "far gum tree on the other side. Dark violet clouds gather far behind the hills. "
            + TOP),
    # batch 1: rainy backgrounds before the storm
    "p05": ("vig", "", "No rain yet: dry, no raindrops, no storm clouds. " f"Three small separate vignettes in a row across the middle of the page, "
            f"the same {BANJO} on a short branch in each: in the first, fluffing up his fur; in the "
            "second, wiggling his toes; in the third, crouched low, ready to leap. No frames. Lots "
            "of empty white space at the top."),
    # trunk-edge-to-edge layout (Book 2 p06/p07 fix for flat sky bands)
    "p06": ("full", "", f"{NIGHT}. The top of {TREE} sways hard in a strong gust, leaves flying "
            f"off in the wind. {BANJO} clings to the top branch with all four paws, every hair "
            "standing on end, eyes enormous, mouth open in shock. A soft lilac glow inside far-off "
            "clouds over the hills. To the left of the tree, a wide dark violet sky fills the upper "
            "part of the picture, open and empty for text, one continuous painted sky with no hard "
            "edges or bands."),
    # batch 1: added an awake Olive (she is asleep on p08)
    "p07": ("full", "", "Only one animal in this picture: Banjo. No koala, no other animals. "
            f"{NIGHT}. For a moment the whole bush is lit pale lilac-white by distant "
            "lightning glowing inside the clouds far away. The first big round raindrops are "
            f"falling. The trunk of {TREE} rises from the bottom edge to the top edge on the left; "
            f"on a branch reaching right, {BANJO} looks up as a big raindrop lands on his head. To "
            "the right of the trunk, the sky fills the upper part of the picture, open and empty "
            "for text, one continuous painted sky with no hard edges or bands."),
    "p08": ("full", "", f"{NIGHT}, high in {TREE}. {OLIVE} asleep with her eyes shut, hugging the "
            f"trunk with her arms and legs. {BANJO} bouncing on the branch beside her, paws out, "
            "eyes wide and alarmed, the wind tugging both their fur. " + TOP),
    "p09": ("vig", "", f"{OLIVE} with her eyes shut, hugging a short piece of gum-tree trunk a "
            f"little tighter, cozy and calm. Beside her {BANJO} stands in a determined pose, chin "
            "up, paws on hips, his damp fur sticking up in tufts. White space at the top and "
            "bottom."),
    "p10": ("full", "c", f"{NIGHT}, at the foot of {TREE}. {WOMBAT} stands beside the trunk "
            f"looking up. {BANJO} clings head-down to the trunk just above it, pointing an "
            "accusing paw at the wombat. " + TOP),
    "p11": ("full", "c", f"{NIGHT}, at the foot of {TREE}. {WOMBAT} patting its round tummy with "
            f"one paw, embarrassed, smiling sheepishly. {BANJO} sits on a low branch above, "
            "looking sorry. " + TOP),
    # batch 1: added an echidna, a wombat and a kookaburra from the cast sheet, and a lightning bolt
    "p12": ("full", "c", "Only two animals in this picture: the cockatoo and Banjo. No echidna, no "
            "wombat, no kookaburra, no possum, no koala. No lightning bolt. "
            f"{NIGHT}. {COCKY} on a branch of {TREE} with its big white wings spread "
            "wide, glowing white for a moment in a soft flash of distant light from the clouds. "
            f"{BANJO} on the same branch pointing at it in triumph. " + TOP),
    "p13": ("vig", "c", f"{COCKY} on a short branch with its wings folded tight and its yellow "
            "crest up, cross, while behind it a small cloud glows with a soft flash. "
            f"{BANJO} beside it looking from the cockatoo up to the glowing cloud, mouth open. "
            "White space at the top."),
    # batch 1: flat sky band with a hard edge; trunk-edge-to-edge layout instead (Book 2 fix)
    "p14": ("full", "c", "Only two animals in this picture: the possum, of which only the tail "
            f"shows, and Banjo. {NIGHT}. The trunk of {TREE} rises from the bottom edge to the top "
            "edge of the picture on the left side, with a round hollow low on it; out of the hollow "
            f"sticks the bushy black tail of {POSSUM}, thumping against the bark. {BANJO} stands on "
            "a branch reaching right from the trunk, paws on hips, frowning. To the right of the "
            "trunk, the dark violet sky fills the upper part of the picture, open and empty for "
            "text, one continuous painted sky with no hard edges or bands."),
    "p15": ("vig", "c", f"{POSSUM} huddled inside a round hollow in a short piece of gum-tree "
            "trunk, only its big frightened eyes, big ears and trembling knees showing, knees "
            "knocking together. White space at the top."),
    "p16": ("full", "", f"{NIGHT}, heavy soft rain pouring down in slanted streaks. {BANJO} sits "
            f"on a branch of {TREE}, completely soaked, fur flat and dripping, water running off "
            "his ears and the tip of his nose, looking grumpy. " + TOP),
    # batch 1: added a grumpy Olive on the ground
    "p17": ("full", "", "Only one animal in this picture: Banjo. No koala, no other animals. "
            f"{NIGHT}, rain falling. The trunk of {TREE} rises from the bottom edge to "
            f"the top edge on the right. On a branch beside it, {BANJO} wrings out his long fluffy "
            "tail with both paws like a towel, water splashing out, a serious detective frown. To "
            "the left of the trunk, the dark violet sky fills the upper part of the picture, open "
            "and empty for text, one continuous painted sky with no hard edges or bands."),
    "p18": ("full", "n", f"{NIGHT}, light rain. {LYRE} stands on a low branch of {TREE}, beak "
            "wide open as if calling out loudly, its lace tail spread proudly behind it. "
            f"{BANJO} leaps along the branch toward it, pointing, shouting in triumph. " + TOP),
    "p19": ("vig", "n", f"{LYRE} on a short branch with its beak shut tight and its eyes looking "
            "sideways, innocent, while a small cloud above it glows with a soft flash. "
            f"{BANJO} beside it staring at its closed beak. White space at the top."),
    # batch 1: the trunk ended in a flat cut top like a stump
    "p20": ("full", "", f"{NIGHT}, rain falling, trees swaying, a far lilac glow inside the "
            f"clouds over the hills. {TREE} stands tall on the right side with its whole rounded crown "
            "of leaves, no cut or broken top. Everything dark, wet and windy. No animals. " + TOP),
    # batch 1: flat sky band with a hard edge across the top (seen at typesetting)
    "p21": ("full", "", "Only one animal in this picture: Banjo. No lightning bolt. "
            f"{NIGHT}, rain falling. The trunk of {TREE} rises from the bottom edge to the top edge "
            "of the picture on the left side, one long branch reaching right across the lower half. "
            f"{BANJO}, very small, sits near the end of that branch on the right side of the "
            "picture, wrapped in his own tail, wet, scared and lonely. Above the branch, the dark "
            "violet stormy sky fills the upper part of the picture, open and empty for text, one "
            "continuous painted sky with a soft gradient, no hard edges, no flat bands, no "
            "horizontal line across the sky."),
    "p22": ("full", "", f"{NIGHT}, rain falling. On a branch of {TREE}, {OLIVE}, awake with both "
            f"eyes open, hugs {BANJO} in her fluffy arms, calm and kind; Banjo peeks out of the "
            "hug, still a little scared. " + TOP40),
    "p23": ("vig", "", f"{OLIVE} and {BANJO} sitting side by side on a short branch, both counting "
            "on their paws, Banjo concentrating hard, looking at a tiny far-off cloud on the "
            "horizon with a small soft glow in it. White space at the top."),
    "p24": ("full", "cn", f"{NIGHT}, rain falling. At the foot of {TREE}, the round mouth of a "
            f"burrow in the earth. {WOMBAT} stands at the entrance waving everyone in. {BANJO}, "
            f"{COCKY}, {POSSUM} and {LYRE} crowd toward the burrow; Banjo says sorry with his paws "
            "together. " + TOP),
    "p25": ("vig", "cn", "Four small separate vignettes, one in each corner of the page, each a "
            "cozy earthy burrow scene with soft warm light: top left, "
            f"{WOMBAT} counting on its toes; top right, {COCKY} counting on its wing feathers; "
            f"bottom left, {POSSUM} with its eyes squeezed shut; bottom right, {LYRE} with its beak "
            "open, calling. No frames. Empty white space in the middle."),
    # test page 24 Oct: rain kept falling and Banjo sat on a low branch with a faint stripe
    "p26": ("full", "n", f"{AFTER} The rain-washed Australian bush under a bright full moon, the "
            "last clouds drifting away over the hills. Puddles on the ground hold the moon. Two "
            f"{FROG} sing at a puddle's edge in the lower left. High up on the right, on the very top "
            f"branch of {TREE}, {BANJO} crouches grinning, ready to leap, his black head stripe and "
            "cream-edged gliding membrane clearly visible. " + TOP),
    "p27": ("full", "", f"{AFTER} {BANJO} mid-glide across a moonlit gully, membrane spread wide, laughing "
            "with joy, sparkling raindrops shaking off his fur. Below, the wet bush and a puddle "
            "reflecting the moon. Clear moonlit sky after the storm. " + TOP),
    "p28": ("full", "", f"{AFTER} A pink and gold summer dawn over rain-washed hills in the Australian "
            f"bush, raindrops sparkling on the leaves. {BANJO} yawning as he climbs into his round "
            f"hollow in the trunk of {TREE}, sleepy. " + TOP),
    "p29": ("vig", "n", f"{AFTER} {OLIVE} fast asleep hugging a short branch with her mouth wide open in "
            "a giant snore, the branch bouncing. Just above, "
            f"{BANJO} peeks out of a round hollow, startled. On a nearby twig, {LYRE} with its beak "
            "open, grinning. White space at the top."),
    "p32": ("vig", "n", f"{AFTER} {BANJO} curled up asleep in his round tree hollow, tail wrapped around "
            "him, small and cozy. One small Australian green tree frog (plump, bright green, golden "
            "eyes) sits on the rim of the hollow. Small vignette in the middle of the page."),
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
    for ref in (SHEET, CAST, NEW):
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
