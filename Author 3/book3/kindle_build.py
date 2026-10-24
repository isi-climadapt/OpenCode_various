# -*- coding: utf-8 -*-
# Author 3 Book 3 - Who Shook My Tree? Kindle fixed-layout edition (copied from book2, rule 15).
# Input: typeset\p01..p32.png (run `py typeset.py` first), 2588 x 2625 px with bleed.
# Crops each page to the 2550 x 2550 trim box (odd pages x 0..2550, even pages x 38..2588; y 38..2588),
# then writes to KDP_FINAL_UPLOAD\04_KINDLE\:
#   pages\who-shook-0001..0032.jpg   -> import into Kindle Create (Comics, Left-to-Right, Facing Pages on)
#   04_KINDLE_COVER.jpg               -> the ebook cover upload (front cover, trim only)
#   Who_Shook_My_Tree_FIXED_LAYOUT.epub -> fallback: direct upload to KDP as a fixed-layout EPUB
# Page size is a delivery-fee trade-off: KDP charges US$0.15/MB on 70% royalty sales, so pages are
# 1600 px at JPEG quality 80 (about 10 MB for 32 pages). Raise PAGE_PX/QUALITY only with the fee in mind.
# Usage: py kindle_build.py

import io, os, re, uuid, zipfile
from datetime import date
from PIL import Image

import typeset

HERE = os.path.dirname(os.path.abspath(__file__))
TYPESET = os.path.join(HERE, "typeset")
OUT = os.path.join(HERE, "KDP_FINAL_UPLOAD", "04_KINDLE")
PAGES_OUT = os.path.join(OUT, "pages")

TITLE = "Who Shook My Tree?"
AUTHOR = "Hattie Moss"
PUBLISHER = "Saltbush Story House"
TRIM, BLEED = 2550, 38
PAGE_PX, QUALITY = 1600, 80
COVER_QUALITY = 90

ALT = {
    "p01": "Title page: Who Shook My Tree? by Hattie Moss. Banjo the sugar glider peeks out of his hollow in a gum tree, fur on end, a raindrop on his nose.",
    "p02": "For everyone who has ever hidden under the covers when the thunder booms. Copyright 2026 Hattie Moss. Published by Saltbush Story House.",
    "p30": "True Facts from the Bush, part one: lightning and thunder, counting from the flash to the boom, storm safety, superb lyrebirds and green tree frogs.",
    "p31": "True Facts from the Bush, part two: the smell of rain, koalas, wombats and sugar gliders.",
    "p32": "About the author, with Banjo curled up asleep in his hollow and a little green tree frog on the rim.",
}

def crop_trim(n):
    im = Image.open(os.path.join(TYPESET, f"p{n:02d}.png")).convert("RGB")
    x0 = 0 if n % 2 else BLEED            # odd pages: bleed on the right; even pages: bleed on the left
    return im.crop((x0, BLEED, x0 + TRIM, BLEED + TRIM))

def alt_text(pid):
    if pid in ALT:
        return ALT[pid]
    paras = [p for blk in typeset.SPEC[pid]["blocks"] for p in blk["paras"]]
    text = " ".join(typeset.smart(p[2:] if p.startswith("!!") else p).replace("*", "") for p in paras)
    return re.sub(r"\s+", " ", text).strip()

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def front_cover():
    # cover_option_A.png (user's pick) is the front panel with bleed on the right, top and bottom
    im = Image.open(os.path.join(HERE, "cover_option_A.png")).convert("RGB")
    return im.crop((0, BLEED, TRIM, BLEED + TRIM))

def jpeg_bytes(im, q):
    b = io.BytesIO()
    im.save(b, "JPEG", quality=q, optimize=True, dpi=(300, 300))
    return b.getvalue()

def page_xhtml(n, alt):
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en-US" lang="en-US">
<head>
<meta charset="UTF-8"/>
<title>{esc(TITLE)} page {n}</title>
<meta name="viewport" content="width={PAGE_PX}, height={PAGE_PX}"/>
<link rel="stylesheet" type="text/css" href="../css/fxl.css"/>
</head>
<body>
<div class="page"><img src="../images/page-{n:04d}.jpg" alt="{esc(alt)}"/></div>
</body>
</html>
"""

def build_epub(pages, cover_jpg, path):
    book_id = "urn:uuid:" + str(uuid.uuid5(uuid.NAMESPACE_URL, "saltbush/who-shook-my-tree/kindle"))
    modified = date.today().isoformat() + "T00:00:00Z"
    manifest, spine = [], []
    for n, _alt, _jpg in pages:
        manifest.append(f'<item id="p{n:04d}" href="text/page-{n:04d}.xhtml" media-type="application/xhtml+xml"/>')
        manifest.append(f'<item id="img{n:04d}" href="images/page-{n:04d}.jpg" media-type="image/jpeg"/>')
        side = "right" if n % 2 else "left"       # matches the print book: page 1 is a right-hand page
        spine.append(f'<itemref idref="p{n:04d}" properties="page-spread-{side}"/>')
    opf = f"""<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid" xml:lang="en-US"
         prefix="rendition: http://www.idpf.org/vocab/rendition/#">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:identifier id="bookid">{book_id}</dc:identifier>
<dc:title>{esc(TITLE)}</dc:title>
<dc:creator id="author">{AUTHOR}</dc:creator>
<meta refines="#author" property="role" scheme="marc:relators">aut</meta>
<dc:publisher>{PUBLISHER}</dc:publisher>
<dc:language>en-US</dc:language>
<dc:rights>Copyright 2026 Hattie Moss. All rights reserved.</dc:rights>
<meta property="dcterms:modified">{modified}</meta>
<meta property="rendition:layout">pre-paginated</meta>
<meta property="rendition:orientation">auto</meta>
<meta property="rendition:spread">landscape</meta>
<meta name="cover" content="cover-image"/>
<meta name="fixed-layout" content="true"/>
<meta name="original-resolution" content="{PAGE_PX}x{PAGE_PX}"/>
<meta name="book-type" content="children"/>
<meta name="orientation-lock" content="none"/>
<meta name="primary-writing-mode" content="horizontal-lr"/>
<meta name="region-mag" content="false"/>
</metadata>
<manifest>
<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
<item id="css" href="css/fxl.css" media-type="text/css"/>
<item id="cover-image" href="images/cover.jpg" media-type="image/jpeg" properties="cover-image"/>
{chr(10).join(manifest)}
</manifest>
<spine page-progression-direction="ltr">
{chr(10).join(spine)}
</spine>
</package>
"""
    nav = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en-US" lang="en-US">
<head><meta charset="UTF-8"/><title>Contents</title></head>
<body>
<nav epub:type="toc" id="toc"><h1>Contents</h1><ol>
<li><a href="text/page-0001.xhtml">{esc(TITLE)}</a></li>
<li><a href="text/page-0003.xhtml">The Story</a></li>
<li><a href="text/page-0030.xhtml">True Facts from the Bush</a></li>
<li><a href="text/page-0032.xhtml">About the Author</a></li>
</ol></nav>
<nav epub:type="landmarks" hidden=""><ol>
<li><a epub:type="bodymatter" href="text/page-0003.xhtml">Start of story</a></li>
</ol></nav>
</body>
</html>
"""
    css = ("@page { margin: 0; }\n"
           f"html, body {{ margin: 0; padding: 0; width: {PAGE_PX}px; height: {PAGE_PX}px; }}\n"
           f".page {{ position: absolute; top: 0; left: 0; width: {PAGE_PX}px; height: {PAGE_PX}px; }}\n"
           f".page img {{ display: block; width: {PAGE_PX}px; height: {PAGE_PX}px; }}\n")
    container = """<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
<rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles>
</container>
"""
    with zipfile.ZipFile(path, "w") as z:
        z.writestr(zipfile.ZipInfo("mimetype"), "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        z.writestr("META-INF/container.xml", container, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/content.opf", opf, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/nav.xhtml", nav, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/css/fxl.css", css, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/images/cover.jpg", cover_jpg, compress_type=zipfile.ZIP_STORED)
        for n, alt, jpg in pages:
            z.writestr(f"OEBPS/text/page-{n:04d}.xhtml", page_xhtml(n, alt), compress_type=zipfile.ZIP_DEFLATED)
            z.writestr(f"OEBPS/images/page-{n:04d}.jpg", jpg, compress_type=zipfile.ZIP_STORED)

def main():
    os.makedirs(PAGES_OUT, exist_ok=True)
    pages = []
    for n in range(1, 33):
        im = crop_trim(n).resize((PAGE_PX, PAGE_PX), Image.LANCZOS)
        jpg = jpeg_bytes(im, QUALITY)
        with open(os.path.join(PAGES_OUT, f"who-shook-{n:04d}.jpg"), "wb") as f:
            f.write(jpg)
        pages.append((n, alt_text(f"p{n:02d}"), jpg))
    cover_jpg = jpeg_bytes(front_cover(), COVER_QUALITY)
    with open(os.path.join(OUT, "04_KINDLE_COVER.jpg"), "wb") as f:
        f.write(cover_jpg)
    epub = os.path.join(OUT, "Who_Shook_My_Tree_FIXED_LAYOUT.epub")
    build_epub(pages, jpeg_bytes(front_cover().resize((PAGE_PX, PAGE_PX), Image.LANCZOS), QUALITY), epub)

    page_mb = sum(len(j) for _, _, j in pages) / 1048576
    print(f"pages: 32 x {PAGE_PX}px q{QUALITY} = {page_mb:.1f} MB "
          f"(largest {max(len(j) for _, _, j in pages) / 1048576:.2f} MB)")
    print(f"cover: {TRIM}x{TRIM} = {len(cover_jpg) / 1048576:.1f} MB")
    print(f"epub:  {os.path.getsize(epub) / 1048576:.1f} MB, "
          f"est. US delivery fee ${os.path.getsize(epub) / 1048576 * 0.15:.2f}")

if __name__ == "__main__":
    main()
