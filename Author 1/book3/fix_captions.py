# -*- coding: utf-8 -*-
# Book 3 — caption coherence fixes (F9 audit pass)
import json, io, os

HERE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(HERE, "captions.json")

FIXES = {
    "page_02": "A kangaroo's strong tail helps it balance, even while stirring potions!",
    "page_06": "Cockatoos can copy the words you say, even \"boo\"!",
    "page_07": "Quokkas are called 'the world's happiest animals'. Even pumpkin carvers!",
    "page_21": "Gum trees can grow taller than a 10-storey building. Perfect ghost treehouses!",
    "page_23": "Halloween began as 'All Hallows' Eve'. That's over 1,000 years of ghosts!",
    "page_28": "Kangaroo pouches face forward, perfect for carrying extra lollies!",
    "page_30": "Kookaburras are the world's biggest kingfishers, even witchy ones!",
    "page_31": "Dingoes arrived in Australia more than 4,000 years ago. That's mummy-old!",
    "page_39": "Even ghost bakers know: the biggest cupcake ever weighed as much as a fridge!",
    "page_45": "A kangaroo can hop over 9 metres, faster than any ghost train!",
    "page_48": "Australia grows blue-grey Jarrahdale pumpkins, perfect for wombat carvers!",
}

with io.open(PATH, encoding="utf-8") as f:
    caps = json.load(f)
caps.update(FIXES)
with io.open(PATH, "w", encoding="utf-8") as f:
    json.dump(caps, f, indent=1, ensure_ascii=False)
print("captions updated:", len(caps))
