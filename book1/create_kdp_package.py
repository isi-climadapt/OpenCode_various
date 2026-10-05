# -*- coding: utf-8 -*-
# Complete KDP Production Packager for Aussie Animals (Book 1)
# Generates:
#   1. AUSSIE_ANIMALS_INTERIOR_108P.pdf (108 pages @ 300 DPI, 8.5x11 in, B&W)
#   2. AUSSIE_ANIMALS_COVER_WRAP.pdf (17.493 x 11.25 in @ 300 DPI, full-wrap paperback)
#   3. High-res preview PNGs for visual inspection

import os, sys, re, json
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter, JpegImagePlugin

ROOT = os.path.dirname(os.path.abspath(__file__))
FONTS_DIR = os.path.join(ROOT, "fonts")
RAW2_DIR = os.path.join(ROOT, "raw2")
CAPTIONS_FILE = os.path.join(ROOT, "captions.json")
OUTPUT_DIR = os.path.join(ROOT, "kdp_package")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Fonts
FONT_SNIGLET = os.path.join(FONTS_DIR, "Sniglet-ExtraBold.ttf")
FONT_BALOO = os.path.join(FONTS_DIR, "Baloo2.ttf")
FONT_PACIFICO = os.path.join(FONTS_DIR, "Pacifico-Regular.ttf")

# Canvas specs (8.5 x 11 in @ 300 DPI)
W, H = 2550, 3300

with open(CAPTIONS_FILE, encoding="utf-8") as f:
    CAPTIONS = json.load(f)

# Helper: Draw stars / sparkles
def draw_star(draw, x, y, size, fill=(180, 160, 150)):
    pts = [
        (x, y - size), (x + size*0.25, y - size*0.25),
        (x + size, y), (x + size*0.25, y + size*0.25),
        (x, y + size), (x - size*0.25, y + size*0.25),
        (x - size, y), (x - size*0.25, y - size*0.25)
    ]
    draw.polygon(pts, fill=fill)

# ==============================================================================
# INTERIOR PAGES BUILDER
# ==============================================================================

def make_blank_page():
    return Image.new("L", (W, H), 255)

def make_title_page():
    page = Image.new("L", (W, H), 255)
    d = ImageDraw.Draw(page)
    
    # Border (0.53in margin safe)
    d.rounded_rectangle((160, 160, W-160, H-160), radius=60, outline=0, width=12)
    d.rounded_rectangle((185, 185, W-185, H-185), radius=45, outline=0, width=4)
    
    # Title
    f_title = ImageFont.truetype(FONT_SNIGLET, 210)
    for text, y in [("AUSSIE", 450), ("CUTIES", 680)]:
        bb = d.textbbox((0, 0), text, font=f_title, stroke_width=16)
        tw = bb[2] - bb[0]
        d.text(((W - tw) // 2 - bb[0], y), text, fill=255, stroke_width=16, stroke_fill=0, font=f_title)
        
    # Subtitle
    f_sub = ImageFont.truetype(FONT_BALOO, 80)
    sub = "A CUTE & COMFY COLOURING BOOK"
    bb = d.textbbox((0, 0), sub, font=f_sub)
    d.text(((W - (bb[2]-bb[0])) // 2 - bb[0], 980), sub, fill=0, font=f_sub)
    
    # Tagline
    f_tag = ImageFont.truetype(FONT_BALOO, 65)
    tag = "50 Big & Easy Designs with Fun Facts"
    bb = d.textbbox((0, 0), tag, font=f_tag)
    d.text(((W - (bb[2]-bb[0])) // 2 - bb[0], 1100), tag, fill=80, font=f_tag)
    
    # Hero icon from kangaroo page
    icon = Image.open(os.path.join(ROOT, "kangaroo_frame_cropped.png")).convert("L")
    icon = icon.point(lambda p: 0 if p < 120 else 255)
    icon.thumbnail((1200, 1200), Image.LANCZOS)
    page.paste(icon, ((W - icon.width) // 2, 1300))
    
    # Author
    f_by = ImageFont.truetype(FONT_BALOO, 55)
    d.text(((W - 140) // 2, 2680), "Created by", fill=100, font=f_by)
    f_auth = ImageFont.truetype(FONT_PACIFICO, 110)
    bb = d.textbbox((0, 0), "Matilda Hayes", font=f_auth)
    d.text(((W - (bb[2]-bb[0])) // 2 - bb[0], 2760), "Matilda Hayes", fill=0, font=f_auth)
    
    # Imprint
    f_imp = ImageFont.truetype(FONT_BALOO, 50)
    bb = d.textbbox((0, 0), "GUMLEAF KIDS PRESS", font=f_imp)
    d.text(((W - (bb[2]-bb[0])) // 2 - bb[0], 2980), "GUMLEAF KIDS PRESS", fill=100, font=f_imp)
    
    return page

def make_copyright_page():
    page = Image.new("L", (W, H), 255)
    d = ImageDraw.Draw(page)
    f_reg = ImageFont.truetype(FONT_BALOO, 46)
    f_bold = ImageFont.truetype(FONT_BALOO, 54)
    
    lines = [
        ("Aussie Cuties: A cute and comfy colouring book, perfect for animal lovers", f_bold),
        ("First Edition — October 2026", f_reg),
        ("", f_reg),
        ("Published by Gumleaf Kids Press", f_bold),
        ("Melbourne, Australia", f_reg),
        ("", f_reg),
        ("Created by Matilda Hayes", f_bold),
        ("Copyright © 2026 Gumleaf Kids Press", f_reg),
        ("All rights reserved.", f_reg),
        ("", f_reg),
        ("No part of this publication may be reproduced, distributed, or", f_reg),
        ("transmitted in any form or by any means, including photocopying,", f_reg),
        ("recording, or other electronic or mechanical methods, without", f_reg),
        ("the prior written permission of the publisher.", f_reg),
        ("", f_reg),
        ("Illustrations created with AI assistance and extensively edited and", f_reg),
        ("curated by human artists for maximum quality and child enjoyment.", f_reg),
        ("", f_reg),
        ("Designed and printed for young artists everywhere.", f_reg),
        ("Made with love in Australia.", f_reg),
    ]
    
    y = 1200
    for text, font in lines:
        if text:
            d.text((300, y), text, fill=40, font=font)
        y += 65
    return page

def make_belongs_to_page():
    page = Image.new("L", (W, H), 255)
    d = ImageDraw.Draw(page)
    
    # Decorative border (0.53in margin safe)
    d.rounded_rectangle((160, 160, W-160, H-160), radius=50, outline=0, width=10)
    
    f_title = ImageFont.truetype(FONT_SNIGLET, 120)
    text = "THIS BOOK BELONGS TO:"
    bb = d.textbbox((0, 0), text, font=f_title)
    d.text(((W - (bb[2]-bb[0])) // 2 - bb[0], 650), text, fill=0, font=f_title)
    
    # Large dotted line for child's name
    d.line([(350, 1000), (W-350, 1000)], fill=0, width=10)
    d.line([(350, 1200), (W-350, 1200)], fill=0, width=10)
    
    f_name = ImageFont.truetype(FONT_BALOO, 60)
    d.text(((W - 400) // 2, 1050), "ARTIST NAME", fill=140, font=f_name)
    
    # Kangaroo + joey icon
    icon = Image.open(os.path.join(ROOT, "kangaroo_frame_cropped.png")).convert("L")
    icon = icon.point(lambda p: 0 if p < 120 else 255)
    icon.thumbnail((1100, 1100), Image.LANCZOS)
    page.paste(icon, ((W - icon.width) // 2, 1450))
    
    f_msg = ImageFont.truetype(FONT_BALOO, 65)
    msg = "Get ready to colour 50 amazing Australian animals!"
    bb = d.textbbox((0, 0), msg, font=f_msg)
    d.text(((W - (bb[2]-bb[0])) // 2 - bb[0], 2800), msg, fill=50, font=f_msg)
    
    return page

def make_tips_page():
    page = Image.new("L", (W, H), 255)
    d = ImageDraw.Draw(page)
    
    # Double border (0.53in margin safe)
    d.rounded_rectangle((160, 160, W-160, H-160), radius=50, outline=0, width=10)
    d.rounded_rectangle((185, 185, W-185, H-185), radius=40, outline=0, width=4)
    
    # Title
    f_title = ImageFont.truetype(FONT_SNIGLET, 130)
    t = "TOP COLOURING TIPS!"
    bb = d.textbbox((0, 0), t, font=f_title)
    d.text(((W - (bb[2]-bb[0])) // 2 - bb[0], 230), t, fill=0, font=f_title)
    
    tips = [
        ("1. Put a Blank Sheet Behind Your Page", "When using juicy markers, place a scrap sheet behind your drawing to keep the next page perfectly clean!"),
        ("2. Start Light, Then Go Dark", "Colour lighter shades first, then layer darker tones on top for amazing depth and pop."),
        ("3. Mix Your Art Tools", "Try combining crayons, coloured pencils, and markers together on the same animal for fun textures."),
        ("4. There Are No Mistakes In Art!", "Make your Australian animals any colour you want — purple koalas and rainbow kangaroos are awesome!")
    ]
    f_head = ImageFont.truetype(FONT_BALOO, 60)
    f_desc = ImageFont.truetype(FONT_BALOO, 48)
    
    y = 430
    for head, desc in tips:
        d.text((220, y), head, fill=0, font=f_head)
        y += 72
        words = desc.split(" ")
        line = ""
        for w in words:
            test = line + (" " if line else "") + w
            bb = d.textbbox((0, 0), test, font=f_desc)
            if bb[2] - bb[0] > 2050:
                d.text((260, y), line, fill=60, font=f_desc)
                y += 62
                line = w
            else:
                line = test
        if line:
            d.text((260, y), line, fill=60, font=f_desc)
            y += 80
        y += 20
        
    d.line([(220, y + 10), (W - 220, y + 10)], fill=180, width=4)
    
    # Section 2: Colour Test Palette (Big, generous swatches)
    y_test = y + 60
    f_test_title = ImageFont.truetype(FONT_SNIGLET, 105)
    tt = "MY COLOUR TEST PALETTE"
    bb = d.textbbox((0, 0), tt, font=f_test_title)
    d.text(((W - (bb[2]-bb[0])) // 2 - bb[0], y_test), tt, fill=0, font=f_test_title)
    
    f_test_sub = ImageFont.truetype(FONT_BALOO, 48)
    tsub = "Test your pencils, markers, and crayons here before colouring your animals!"
    bb = d.textbbox((0, 0), tsub, font=f_test_sub)
    d.text(((W - (bb[2]-bb[0])) // 2 - bb[0], y_test + 120), tsub, fill=90, font=f_test_sub)
    
    f_num = ImageFont.truetype(FONT_BALOO, 44)
    radius = 125
    y_circles = y_test + 360
    
    for i in range(5):
        cx = 360 + i * 455
        d.ellipse([cx - radius, y_circles - radius, cx + radius, y_circles + radius], outline=0, width=7)
        lbl = f"Colour {i+1}"
        lbb = d.textbbox((0, 0), lbl, font=f_num)
        d.text((cx - (lbb[2]-lbb[0])//2 - lbb[0], y_circles + radius + 20), lbl, fill=100, font=f_num)
        
    d.line([(220, y_circles + radius + 110), (W - 220, y_circles + radius + 110)], fill=180, width=4)
    
    # Section 3: Bottom Mascot + Artist Pledge (Filling down to y=2980)
    y_bottom = y_circles + radius + 160
    
    # Mascot Kangaroo
    icon = Image.open(os.path.join(ROOT, "kangaroo_frame_cropped.png")).convert("L")
    icon = icon.point(lambda p: 0 if p < 120 else 255)
    icon.thumbnail((880, 880), Image.LANCZOS)
    page.paste(icon, (240, y_bottom))
    
    # Pledge box on right
    box_x = 1180
    d.rounded_rectangle([box_x, y_bottom, W - 240, y_bottom + 880], radius=35, outline=0, width=6)
    
    f_pl_title = ImageFont.truetype(FONT_SNIGLET, 62)
    d.text((box_x + 60, y_bottom + 60), "MY ARTIST PLEDGE:", fill=0, font=f_pl_title)
    
    f_pl_text = ImageFont.truetype(FONT_BALOO, 50)
    d.text((box_x + 60, y_bottom + 180), '"I promise to have fun,', fill=40, font=f_pl_text)
    d.text((box_x + 60, y_bottom + 250), 'make this book my own,', fill=40, font=f_pl_text)
    d.text((box_x + 60, y_bottom + 320), 'and be proud of every', fill=40, font=f_pl_text)
    d.text((box_x + 60, y_bottom + 390), 'drawing I colour!"', fill=40, font=f_pl_text)
    
    d.line([(box_x + 60, y_bottom + 650), (W - 300, y_bottom + 650)], fill=0, width=5)
    f_sig_lbl = ImageFont.truetype(FONT_BALOO, 44)
    d.text((box_x + 60, y_bottom + 675), "ARTIST SIGNATURE", fill=120, font=f_sig_lbl)
    
    # Page number
    f_pnum = ImageFont.truetype(FONT_BALOO, 55)
    d.text((W - 180, 3110), "4", fill=120, font=f_pnum)
    
    return page

def make_art_page(i):
    key = "page_%02d" % i
    raw2_path = os.path.join(RAW2_DIR, "%s.png" % key)
    caption_text = CAPTIONS.get(key, "")
    page_num = str(i * 2 + 3) # Starts at page 5
    
    img = Image.open(raw2_path).convert("L")
    img = ImageOps.autocontrast(img, cutoff=1)
    
    # Fit into 2150x2150 (generous 0.66" margins - eliminates ALL KDP margin errors)
    scale = min(2150 / img.width, 2150 / img.height)
    img = img.resize((int(img.width * scale), int(img.height * scale)), Image.LANCZOS)
    img = img.point(lambda p: 0 if p < 110 else 255)
    
    # Canvas
    page = Image.new("L", (W, H), 255)
    x_p = (W - img.width) // 2
    y_p = 200 # Fixed y position: generous top margin and safe distance from caption
    page.paste(img, (x_p, y_p))
    
    d = ImageDraw.Draw(page)
    
    # Auto-fit caption (safe within 2150 width)
    size = 110
    f_cap = ImageFont.truetype(FONT_BALOO, size)
    while size > 50 and d.textbbox((0, 0), caption_text, font=f_cap)[2] > 2150:
        size -= 5
        f_cap = ImageFont.truetype(FONT_BALOO, size)
    bb = d.textbbox((0, 0), caption_text, font=f_cap)
    d.text(((W - (bb[2]-bb[0])) // 2 - bb[0], 2860), caption_text, fill=0, font=f_cap)
    
    # Page number at bottom right (well inside margins)
    f_num = ImageFont.truetype(FONT_BALOO, 60)
    nb = d.textbbox((0, 0), page_num, font=f_num)
    d.text((W - 200 - (nb[2]-nb[0]), 3010), page_num, fill=120, font=f_num)
    
    return page

def make_checklist_page():
    page = Image.new("L", (W, H), 255)
    d = ImageDraw.Draw(page)
    
    # 0.53in margins: eliminates KDP gutter & edge warnings
    d.rounded_rectangle((160, 160, W-160, H-160), radius=50, outline=0, width=8)
    
    f_title = ImageFont.truetype(FONT_SNIGLET, 95)
    text = "MY AUSSIE ART GALLERY CHECKLIST"
    bb = d.textbbox((0, 0), text, font=f_title)
    d.text(((W - (bb[2]-bb[0])) // 2 - bb[0], 280), text, fill=0, font=f_title)
    
    f_sub = ImageFont.truetype(FONT_BALOO, 50)
    sub = "Tick each box as you finish colouring each animal!"
    bb = d.textbbox((0, 0), sub, font=f_sub)
    d.text(((W - (bb[2]-bb[0])) // 2 - bb[0], 410), sub, fill=90, font=f_sub)
    
    # 50 animal names in 2 columns of 25
    animal_names = [
        "1. Koala (Nap)", "2. Koala (Snack)", "3. Kangaroo", "4. Kangaroo & Joey",
        "5. Wallaby", "6. Wombat", "7. Wombat Burrow", "8. Platypus",
        "9. Quokka", "10. Quokka Selfie", "11. Emu", "12. Kookaburra",
        "13. Galah", "14. Cockatoo", "15. Magpie", "16. Lorikeet",
        "17. Cassowary", "18. Brolga", "19. Jabiru Stork", "20. Wedge-Tailed Eagle",
        "21. Pelican", "22. Echidna", "23. Echidna Lunch", "24. Dingo",
        "25. Tasmanian Devil", "26. Frill-Necked Lizard", "27. Blue-Tongue Lizard", "28. Goanna",
        "29. Bilby", "30. Numbat", "31. Quoll", "32. Hopping Mouse",
        "33. Bandicoot", "34. Bettong", "35. Potoroo", "36. Possum",
        "37. Sugar Glider", "38. Camel", "39. Sea Turtle", "40. Dugong",
        "41. Dolphin", "42. Little Penguin", "43. Seahorse", "44. Clownfish",
        "45. Jellyfish", "46. Octopus", "47. Hermit Crab", "48. Baby Whale",
        "49. Tree Frog", "50. Butterfly Garden"
    ]
    
    f_item = ImageFont.truetype(FONT_BALOO, 46)
    y_start = 510
    for idx, name in enumerate(animal_names):
        col = idx // 25
        row = idx % 25
        x = 260 if col == 0 else 1340
        y = y_start + row * 95
        # Checkbox square
        d.rectangle([x, y + 6, x + 38, y + 44], outline=0, width=5)
        d.text((x + 60, y), name, fill=30, font=f_item)
        
    d.text((W - 220, 3010), "105", fill=120, font=ImageFont.truetype(FONT_BALOO, 60))
    return page

def make_certificate_page():
    page = Image.new("L", (W, H), 255)
    d = ImageDraw.Draw(page)
    
    # Certificate fancy double border (0.53in margin safe)
    d.rounded_rectangle((160, 160, W-160, H-160), radius=70, outline=0, width=16)
    d.rounded_rectangle((195, 195, W-195, H-195), radius=55, outline=0, width=6)
    
    f_top = ImageFont.truetype(FONT_BALOO, 70)
    t = "OFFICIAL CERTIFICATE"
    bb = d.textbbox((0, 0), t, font=f_top)
    d.text(((W - (bb[2]-bb[0])) // 2 - bb[0], 400), t, fill=60, font=f_top)
    
    f_award = ImageFont.truetype(FONT_SNIGLET, 150)
    award = "YOUNG ARTIST AWARD"
    bb = d.textbbox((0, 0), award, font=f_award)
    d.text(((W - (bb[2]-bb[0])) // 2 - bb[0], 550), award, fill=0, font=f_award)
    
    f_p = ImageFont.truetype(FONT_BALOO, 65)
    p1 = "This certifies that"
    bb = d.textbbox((0, 0), p1, font=f_p)
    d.text(((W - (bb[2]-bb[0])) // 2 - bb[0], 900), p1, fill=60, font=f_p)
    
    # Name underline
    d.line([(400, 1250), (W-400, 1250)], fill=0, width=8)
    f_lbl = ImageFont.truetype(FONT_BALOO, 50)
    d.text(((W - 350) // 2, 1280), "NAME OF ARTIST", fill=130, font=f_lbl)
    
    p2 = "has successfully coloured all 50 Australian Wildlife pages in this book!"
    bb = d.textbbox((0, 0), p2, font=f_p)
    d.text(((W - (bb[2]-bb[0])) // 2 - bb[0], 1500), p2, fill=40, font=f_p)
    
    # Big star seal in center
    draw_star(d, W // 2, 1950, 160, fill=0)
    draw_star(d, W // 2, 1950, 110, fill=255)
    f_star = ImageFont.truetype(FONT_SNIGLET, 60)
    d.text((W // 2 - 80, 1910), "★ 50 ★", fill=0, font=f_star)
    
    # Signatures
    d.line([(350, 2600), (950, 2600)], fill=0, width=6)
    d.line([(W-950, 2600), (W-350, 2600)], fill=0, width=6)
    
    f_sig = ImageFont.truetype(FONT_PACIFICO, 75)
    d.text((450, 2480), "Matilda Hayes", fill=0, font=f_sig)
    
    f_siglbl = ImageFont.truetype(FONT_BALOO, 50)
    d.text((540, 2630), "AUTHOR", fill=100, font=f_siglbl)
    d.text((W-720, 2630), "DATE", fill=100, font=f_siglbl)
    
    d.text((W - 220, 3010), "107", fill=120, font=ImageFont.truetype(FONT_BALOO, 60))
    return page

def make_thank_you_page():
    page = Image.new("L", (W, H), 255)
    d = ImageDraw.Draw(page)
    
    # 0.53in margin: completely safe from KDP inside gutter & edges
    d.rounded_rectangle((160, 160, W-160, H-160), radius=50, outline=0, width=8)
    
    f_title = ImageFont.truetype(FONT_SNIGLET, 120)
    t = "THANK YOU!"
    bb = d.textbbox((0, 0), t, font=f_title)
    d.text(((W - (bb[2]-bb[0])) // 2 - bb[0], 350), t, fill=0, font=f_title)
    
    f_msg = ImageFont.truetype(FONT_BALOO, 62)
    msg = [
        "Thank you for colouring with Gumleaf Kids Press!",
        "We hope you enjoyed exploring the wild and wonderful",
        "animals of Australia with Matilda Hayes.",
        "",
        "If you loved this book, please consider leaving a kind",
        "review on Amazon — it helps independent Australian",
        "bookmakers create more adventures for kids!",
        "",
        "COMING SOON IN THE GUMLEAF AUSSIE SERIES:",
        "★ Aussie Cuties at Christmas",
        "★ Great Barrier Reef Ocean Friends",
        "★ Outback Australian Adventures"
    ]
    y = 650
    for line in msg:
        if line:
            bb = d.textbbox((0, 0), line, font=f_msg)
            d.text(((W - (bb[2]-bb[0])) // 2 - bb[0], y), line, fill=30 if not line.startswith("★") else 0, font=f_msg)
        y += 95
        
    f_imp = ImageFont.truetype(FONT_BALOO, 56)
    imp = "GUMLEAF KIDS PRESS  •  MELBOURNE, AUSTRALIA"
    bb = d.textbbox((0, 0), imp, font=f_imp)
    d.text(((W - (bb[2]-bb[0])) // 2 - bb[0], 2850), imp, fill=100, font=f_imp)
    
    d.text((W - 220, 3010), "108", fill=120, font=ImageFont.truetype(FONT_BALOO, 60))
    return page

# ==============================================================================
# COVER WRAP BUILDER (KDP Paperback Specs)
# ==============================================================================

def make_full_cover_wrap():
    # KDP formula for 108 pages B&W on white paper:
    # Spine width = 108 * 0.002252 = 0.2432 in
    # Total width = 0.125 (bleed) + 8.5 (back) + 0.2432 (spine) + 8.5 (front) + 0.125 (bleed) = 17.4932 in
    # Total height = 11.25 in (11.0 + 2 * 0.125)
    # At 300 DPI: Width = 5248 px, Height = 3375 px
    
    CW, CH = 5248, 3375
    BG_COLOR = (246, 237, 225) # Warm cream matching front cover
    
    wrap = Image.new("RGB", (CW, CH), BG_COLOR)
    d = ImageDraw.Draw(wrap)
    
    # Coordinate landmarks
    # Bleed = 38 px (0.125 in * 300 DPI = 37.5 px)
    # Back cover width = 2550 px
    # Spine width = 73 px
    # Front cover width = 2550 px
    
    back_x1 = 0
    back_x2 = 38 + 2550
    spine_x1 = back_x2
    spine_x2 = spine_x1 + 73
    front_x1 = spine_x2
    front_x2 = CW
    
    # 1. FRONT COVER (Right side)
    # Rebuild front cover with razor-sharp kangaroo linework (UnsharpMask eliminates all print blur)
    fc_canvas = Image.new("RGB", (W, H), BG_COLOR)
    fc_d = ImageDraw.Draw(fc_canvas)
    
    # Author
    abb = fc_d.textbbox((0, 0), "Matilda Hayes", font=ImageFont.truetype(FONT_PACIFICO, 95))
    fc_d.text(((W - (abb[2]-abb[0])) // 2 - abb[0], 160), "Matilda Hayes", fill=(70, 50, 40), font=ImageFont.truetype(FONT_PACIFICO, 95))
    
    # Title: AUSSIE CUTIES
    f_title = ImageFont.truetype(FONT_SNIGLET, 245)
    tbb = fc_d.textbbox((0, 0), "AUSSIE CUTIES", font=f_title, stroke_width=22)
    tw = tbb[2] - tbb[0]
    tx = (W - tw) // 2 - tbb[0]
    ty = 310
    fc_d.text((tx + 6, ty + 10), "AUSSIE CUTIES", font=f_title, fill=(35, 25, 20), stroke_width=22, stroke_fill=(35, 25, 20))
    fc_d.text((tx, ty), "AUSSIE CUTIES", font=f_title, fill=(255, 255, 255), stroke_width=22, stroke_fill=(35, 25, 20))
    
    # Subtitle
    f_sub = ImageFont.truetype(FONT_BALOO, 75)
    sub = "A CUTE & COMFY COLOURING BOOK"
    sbb = fc_d.textbbox((0, 0), sub, font=f_sub)
    fc_d.text(((W - (sbb[2]-sbb[0])) // 2 - sbb[0], 610), sub, fill=(80, 60, 50), font=f_sub)
    
    # Kangaroo Hero: Resized & sharpened with UnsharpMask for high-res 300 DPI clarity
    k_frame = Image.open(os.path.join(ROOT, "kangaroo_frame_cropped.png")).convert("RGB")
    target_w = 2150
    target_h = int(k_frame.height * (target_w / k_frame.width))
    k_res = k_frame.resize((target_w, target_h), Image.LANCZOS)
    k_res = k_res.filter(ImageFilter.UnsharpMask(radius=2.0, percent=220, threshold=1))
    fc_canvas.paste(k_res, ((W - target_w) // 2, 730))
    
    # Bottom: 50 BIG & EASY DESIGNS (No age groups)
    f_tag = ImageFont.truetype(FONT_BALOO, 68)
    tag = "50 BIG & EASY DESIGNS"
    tagbb = fc_d.textbbox((0, 0), tag, font=f_tag)
    fc_d.text(((W - (tagbb[2]-tagbb[0])) // 2 - tagbb[0], 2980), tag, fill=(110, 90, 80), font=f_tag)
    
    f_pub = ImageFont.truetype(FONT_BALOO, 45)
    pub = "GUMLEAF KIDS PRESS"
    pbb = fc_d.textbbox((0, 0), pub, font=f_pub)
    fc_d.text(((W - (pbb[2]-pbb[0])) // 2 - pbb[0], 3130), pub, fill=(150, 130, 120), font=f_pub)
    
    # Save standalone front cover too
    fc_canvas.save(os.path.join(ROOT, "front_cover_final.png"), dpi=(300, 300))
    
    # Scale to full cover wrap height with bleed
    front_cover_bleed = fc_canvas.resize((2588, 3375), Image.LANCZOS)
    wrap.paste(front_cover_bleed, (front_x1, 0))
    
    # 2. SPINE (Center)
    # Clean warm spine with small vertical line or subtle tone
    d.rectangle([spine_x1, 0, spine_x2, CH], fill=(240, 228, 214))
    d.line([(spine_x1, 0), (spine_x1, CH)], fill=(210, 195, 180), width=3)
    d.line([(spine_x2, 0), (spine_x2, CH)], fill=(210, 195, 180), width=3)
    
    # 3. BACK COVER (Left side)
    # Title at top of back cover
    f_bktitle = ImageFont.truetype(FONT_SNIGLET, 130)
    bk_t = "MEET YOUR AUSSIE CUTIES!"
    bb = d.textbbox((0, 0), bk_t, font=f_bktitle)
    d.text((38 + (2550 - (bb[2]-bb[0])) // 2 - bb[0], 240), bk_t, fill=(45, 30, 20), font=f_bktitle)
    
    # Marketing Blurb
    f_blurb = ImageFont.truetype(FONT_BALOO, 62)
    blurb_lines = [
        "Hop into the wonderful world of Aussie Cuties! From cuddly",
        "koalas asleep in gum trees to bounding kangaroos, cheeky quokkas,",
        "and playful dolphins, this delightful book is packed with 50 big,",
        "bold, and easy designs created specially for young artists."
    ]
    y_b = 480
    for line in blurb_lines:
        bb = d.textbbox((0, 0), line, font=f_blurb)
        d.text((38 + (2550 - (bb[2]-bb[0])) // 2 - bb[0], y_b), line, fill=(70, 50, 40), font=f_blurb)
        y_b += 82
        
    # 4 Sample Interior Previews (Koala, Quokka, Platypus, Dolphin)
    # Shows parents Look-Inside proof
    samples = ["page_01", "page_09", "page_08", "page_41"]
    thumb_w, thumb_h = 470, 610
    thumb_y = 960
    for idx, s_key in enumerate(samples):
        s_path = os.path.join(ROOT, "raw", "%s.png" % s_key)
        if os.path.exists(s_path):
            thumb = Image.open(s_path).convert("RGB")
            thumb.thumbnail((thumb_w - 20, thumb_h - 20), Image.LANCZOS)
            tx = 38 + 140 + idx * (thumb_w + 110)
            # Rounded drop shadow frame
            d.rounded_rectangle([tx - 10, thumb_y - 10, tx + thumb_w + 10, thumb_y + thumb_h + 10], radius=30, fill=(255, 255, 255), outline=(40, 25, 15), width=8)
            wrap.paste(thumb, (tx + (thumb_w - thumb.width) // 2, thumb_y + (thumb_h - thumb.height) // 2))
            
    # Feature Bullet Points
    bullets = [
        ("•  50 BIG & BOLD DESIGNS", "Extra-thick lines, easy for crayons, markers, & little hands"),
        ("•  FUN FACTS ON EVERY PAGE", "Learn amazing secrets about Australia's iconic animals"),
        ("•  SINGLE-SIDED PAGES", "No bleed-through! Great for cutting out and displaying artwork"),
        ("•  PERFECT GIFT IDEA", "Great for quiet afternoons, road trips, birthdays, & creative fun")
    ]
    f_bhead = ImageFont.truetype(FONT_BALOO, 58)
    f_bdesc = ImageFont.truetype(FONT_BALOO, 50)
    y_bull = 1760
    for head, desc in bullets:
        d.text((38 + 220, y_bull), head, fill=(35, 25, 20), font=f_bhead)
        d.text((38 + 220, y_bull + 65), desc, fill=(90, 75, 65), font=f_bdesc)
        y_bull += 160
        
    # Matilda Hayes Bio Box on Back Cover (generous width + safe 4-line wrap)
    d.rounded_rectangle([38 + 160, 2500, 38 + 1660, 2980], radius=35, fill=(255, 255, 255), outline=(60, 40, 30), width=6)
    f_bio_title = ImageFont.truetype(FONT_SNIGLET, 56)
    d.text((38 + 220, 2545), "ABOUT MATILDA HAYES", fill=(45, 30, 20), font=f_bio_title)
    f_bio = ImageFont.truetype(FONT_BALOO, 42)
    bio_lines = [
        "Matilda Hayes is an Australian author who creates cheerful, bold,",
        "and easy colouring books designed to spark imagination and",
        "creativity. She lives under wide sunny skies with two cheeky kids",
        "and a sleepy Australian kelpie named Banjo."
    ]
    yb = 2640
    for line in bio_lines:
        d.text((38 + 220, yb), line, fill=(80, 65, 55), font=f_bio)
        yb += 64
        
    # Barcode reservation area (KDP requirement: 2.0 x 1.2 in = 600 x 360 px at bottom-right of back cover)
    # Leave this area completely empty
    bc_x = 38 + 2550 - 680 - 60
    bc_y = CH - 38 - 420 - 60
    d.rounded_rectangle([bc_x, bc_y, bc_x + 680, bc_y + 420], radius=20, fill=(255, 255, 255), outline=(210, 200, 190), width=3)
    f_bc = ImageFont.truetype(FONT_BALOO, 38)
    d.text((bc_x + 130, bc_y + 180), "[ KDP BARCODE AREA ]", fill=(180, 170, 160), font=f_bc)
    
    # Bottom Imprint on Back Cover
    f_bimp = ImageFont.truetype(FONT_BALOO, 46)
    d.text((38 + 220, 3120), "GUMLEAF KIDS PRESS  •  MELBOURNE, AUSTRALIA", fill=(140, 125, 115), font=f_bimp)
    
    return wrap

# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

def main():
    print("=== STEP 1: GENERATING 108 INTERIOR PAGES ===")
    interior_pages = []
    
    print("Building front matter (pages 1-4)...")
    interior_pages.append(make_title_page())       # Page 1
    interior_pages.append(make_copyright_page())   # Page 2
    interior_pages.append(make_belongs_to_page())  # Page 3
    interior_pages.append(make_tips_page())        # Page 4
    
    print("Building 50 single-sided art pages (pages 5-104)...")
    for i in range(1, 51):
        art_page = make_art_page(i)
        interior_pages.append(art_page)           # Odd page: Art
        interior_pages.append(make_blank_page())   # Even page: Blank back
        if i % 10 == 0:
            print("  ...%d / 50 art pages built" % i)
            
    print("Building back matter (pages 105-108)...")
    interior_pages.append(make_checklist_page())   # Page 105
    interior_pages.append(make_blank_page())       # Page 106
    interior_pages.append(make_certificate_page()) # Page 107
    interior_pages.append(make_thank_you_page())   # Page 108
    
    print("Total interior pages assembled:", len(interior_pages))
    assert len(interior_pages) == 108, "Page count must be exactly 108!"
    
    FINAL_UPLOAD_DIR = os.path.join(os.path.dirname(ROOT), "KDP_FINAL_UPLOAD")
    os.makedirs(FINAL_UPLOAD_DIR, exist_ok=True)
    
    interior_pdf_path = os.path.join(OUTPUT_DIR, "AUSSIE_CUTIES_INTERIOR_108P.pdf")
    upload_interior_path = os.path.join(FINAL_UPLOAD_DIR, "01_MANUSCRIPT_INTERIOR_108P.pdf")
    print("Exporting Interior PDF to:", interior_pdf_path)
    interior_pages[0].save(
        interior_pdf_path,
        save_all=True,
        append_images=interior_pages[1:],
        resolution=300.0,
        optimize=True
    )
    import shutil
    shutil.copyfile(interior_pdf_path, upload_interior_path)
    print("Interior PDF export complete! Size: %.2f MB" % (os.path.getsize(interior_pdf_path) / (1024*1024)))
    
    print("\n=== STEP 2: GENERATING FULL COVER WRAP (KDP SPECS) ===")
    cover_wrap = make_full_cover_wrap()
    cover_png_path = os.path.join(OUTPUT_DIR, "AUSSIE_CUTIES_COVER_WRAP.png")
    cover_pdf_path = os.path.join(OUTPUT_DIR, "AUSSIE_CUTIES_COVER_WRAP.pdf")
    cover_small_path = os.path.join(OUTPUT_DIR, "AUSSIE_CUTIES_COVER_WRAP_PREVIEW.png")
    upload_cover_path = os.path.join(FINAL_UPLOAD_DIR, "02_COVER_WRAP_PRINT_READY.pdf")
    upload_preview_path = os.path.join(FINAL_UPLOAD_DIR, "COVER_PREVIEW.png")
    
    print("Saving cover PNG...")
    import time
    for attempt in range(4):
        try:
            cover_wrap.save(cover_png_path, dpi=(300, 300))
            break
        except OSError:
            time.sleep(2)
            
    print("Saving cover PDF...")
    for attempt in range(4):
        try:
            cover_wrap.save(cover_pdf_path, resolution=300.0)
            shutil.copyfile(cover_pdf_path, upload_cover_path)
            break
        except OSError:
            time.sleep(2)
    print("Saving preview...")
    preview_img = cover_wrap.resize((1500, int(1500 * cover_wrap.height / cover_wrap.width)), Image.LANCZOS)
    for attempt in range(4):
        try:
            preview_img.save(cover_small_path)
            preview_img.save(upload_preview_path)
            break
        except OSError:
            time.sleep(2)
    
    print("Cover Wrap complete! PDF Size: %.2f MB" % (os.path.getsize(cover_pdf_path) / (1024*1024)))
    print("All files ready in:", OUTPUT_DIR)
    print("Upload folder ready in:", FINAL_UPLOAD_DIR)

if __name__ == "__main__":
    main()
