# -*- coding: utf-8 -*-
# F9 â€” Caption <-> Image Coherence Audit (pipeline rule, applies to EVERY book)
# Verifies each page's caption shares content with its image: the caption must
# match the scene's hero/friend ANIMALS or scene object words (stem match).
# Usage:  py scripts/caption_coherence.py <book_folder>
# Exit 0 = all coherent, exit 1 = flagged pages (regen/rewrite captions).
import json, os, re, sys

STOP = set("""a an the and or of with in on at to for from into over under three two four five
his her its their this that very little big cute friendly happy simple one whole whole page
scene wearing surrounded while even your you they them she he it""".split())

CLOSING = {"page_50"}  # intentional closing-greeting pages (no scene fact required)


def content_words(text):
    return [w for w in re.findall(r"[a-z][a-z'-]+", text.lower())
            if len(w) > 2 and w not in STOP]


def load(book):
    scenes = {}
    with open(os.path.join(book, "PAGE-GENERATION-PROMPTS.md"), encoding="utf-8") as f:
        for line in f:
            m = re.match(r"\|\s*(page_\d+)\s*\|\s*([^|]+)\|\s*(.+?)\s*\|", line)
            if m and not m.group(3).startswith("Fun-fact"):
                scenes[m.group(1)] = (m.group(2).strip(), m.group(3).strip())
    with open(os.path.join(book, "captions.json"), encoding="utf-8") as f:
        caps = json.load(f)
    return scenes, caps


def _norm(w):
    return w[:-1] if w.endswith("s") else w


def matches(caption, title, scene):
    cap_words = {_norm(w) for w in content_words(caption)}
    ref_words = {_norm(w) for w in content_words(title)}
    ref_words |= {_norm(w) for w in content_words(scene)}
    for cw in cap_words:
        key = cw[:4] if len(cw) >= 4 else cw
        for sw in ref_words:
            skey = sw[:4] if len(sw) >= 4 else sw
            if key == skey:
                return True
    return False


def check(book):
    scenes, caps = load(book)
    fails = []
    for k in sorted(scenes):
        if k in CLOSING:
            continue
        if k not in caps:
            fails.append((k, scenes[k][0], "<<MISSING CAPTION>>"))
            continue
        title, scene = scenes[k]
        if not matches(caps[k], title, scene):
            fails.append((k, title, caps[k]))
    return fails, len(scenes)


if __name__ == "__main__":
    book = sys.argv[1] if len(sys.argv) > 1 else \
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fails, total = check(book)
    for k, t, c in fails:
        print("F9 FLAG %s [%s]: %s" % (k, t, c))
    print("F9 coherence: %d/%d captions match their images" % (total - len(fails), total))
    sys.exit(1 if fails else 0)

