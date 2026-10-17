# GUMLEAF KIDS PRESS — Master Agent Pipeline v2.0 (FINAL)

> The complete, locked, battle-tested pipeline for producing a bestselling kids' colouring book
> from trend research to KDP upload — using **OpenArt** as the single generation engine.
> Built from the full production of Book 1: *Aussie Cuties* (Oct 2026).

---

## THE CONVERSATION RETROSPECTIVE — What We Learned

### Timeline of Book 1: "Aussie Cuties"

| Phase | What Happened | Key Decision |
|---|---|---|
| **Research** | 4 parallel research agents studied KDP strategy, niches, production, marketing; 500-book market analysis | Bold & Easy + kids crossover identified as the growth edge; A$13.99 = 60% royalty floor on .au |
| **Branding** | Verified clean on Bing + Amazon AU | Pen name **Matilda Hayes** / Imprint **Gumleaf Kids Press** — ✅ **ALREADY LOCKED, never re-verify** (see publishing/00-brand-identity.md) |
| **Validation** | Live SERP census on .au + .com: zero incumbents >16 reviews in niche; "Bold & Easy" unoccupied on .com | GO verdict; differentiate on spec transparency, 108pp, back-matter, series |
| **Tool Trials** | OpenArt (Nano Banana 2) vs Recraft (SVG) vs Gemini direct (N1/N2) bake-off | **OpenArt CLI wins**: best scene coherence, ~50 credits/page, commercial rights via subscription. Gemini direct cheaper per-call (~4¢) but output weaker + throttled; Recraft vectors gorgeous but 96 credits/gen + weaker scenes. **LOCKED: OpenArt for everything.** |
| **Generation** | 50 pages via OpenArt; multiple failure modes found & fixed | Locked prompt suffix (rich-but-simple, white margins, no frames, no text in art) |
| **Assembly** | Several layout bugs: art/caption overlap, stretch distortion, clipped captions | **LOCKED: fixed-position layout, art ≤2150px, auto-fit captions, page numbers bottom-right** |
| **Cover** | First attempts too plain; researched Coco Wyo bestsellers live (12,388 reviews) | **LOCKED: Coco Wyo formula** — coloured kawaii hero + Sniglet bubble title + Pacifico author script + cream background + rounded frame |
| **Title** | "Australian Animals Colouring Book" → "Aussie Friends" → user asked for catchy | **LOCKED: "Aussie Cuties: A cute and comfy colouring book, perfect for animal lovers"** (rhyme formula like *Spooky Cutie*) |
| **KDP QA** | Previewer flagged pages 37/67/95/108 margins; bio box overflow; blurry hero | Margins widened to >0.53", bio box rewrapped, UnsharpMask sharpening — **0 pages flagged** |
| **Publish** | Upload guide written, pricing set | A$16.99 (A$4.91/sale) .au; $9.99 US; £7.99 UK |

### The 8 Failure Modes (F1–F8) — baked into every future run

| ID | Failure | Audit | Fix (locked in scripts) |
|---|---|---|---|
| F1 | Colour fill sneaks into art | RGB saturation scan | binarize strip; regen if ugly |
| F2 | AI draws a frame/border box | line-span scan in edge bands | regen with "no frame, white margin" phrases |
| F3 | Art touches raw edges ("in a box") | outer-12px ink count | margin phrase in every prompt |
| F4 | Non-square source stretched | aspect check | **aspect-preserving fit ONLY** (`min` scale) |
| F5 | Caption clipped | textbbox width check | auto-shrink font loop |
| F6 | Art/caption overlap | gap-band ink scan | **fixed y-paste, art ≤2150px, caption at 2860** |
| F7 | API throttling (parallel) | exit + stderr | ≤6 workers, retry failed |
| F8 | OneDrive file lock on save | OSError | retry ×3 with sleep |
| F9 | Caption doesn't match the image (wrong animal/scene) | `Author 1\scripts\caption_coherence.py` — stem-matches every caption against its page's scene text | rewrite caption to name what is actually in the scene; audit runs after EVERY typeset, must pass before contact sheet / PDF export |
| F10 | Cover text overflows the safe zone (KDP previewer flags it) | back-cover title ink extends past x 150..2476 of the back panel | auto-shrink title font until width ≤ 2230px (baked into all create_cover_wrap scripts); always verify title ink extents after wrap build |
| F11 | Print looks soft (Oct 2026: Aussie Cuties + Ocean Friends) | any art below 270 DPI at print size; halos round outlines; JPEG-75 PDFs | interiors vector-traced (`scripts\vectorize_line_art.py`, even-odd fill) and exported 600 DPI 1-bit lossless; cover hero ≥2K, never sharpened; cover PDF JPEG quality 100. Full rules: `Author 1\book1\PIPELINE.md` → "Print resolution rules" |

### Hard Rules (never break)

0. **Author folder structure:** every pen name gets a top-level folder (`Author 1\`, `Author 2\`...) containing its own `publishing\` (brand identity, research, validations), `book1\`, `book2\`..., `scripts\` and upload folders. Author 1 = **Matilda Hayes / Gumleaf Kids Press** (verified brand). Author 2 = new pen name + different branding style, brand lock required before production (rule 0's verification applies new)
0a. **Brand is FIXED FOREVER per author:** Matilda Hayes (author) / Gumleaf Kids Press (imprint) — already locked & verified clean; no re-verification, no renaming, no second pen name for the kids line (adult lines get their own, TBD)
1. **OpenArt CLI for ALL generation** — never Gemini, never Recraft. Interiors: nano-banana-2 (the CLI only returns 1K, so pages are vector-traced, F11). Cover hero: draft with nano-banana-2, then Ideogram 4.5 image2image from the CLI with the draft as reference, for 2K output (~44 credits); show the user old vs new before replacing
2. **All lettering typeset programmatically** (Baloo 2 / Sniglet / Pacifico) — never AI-generated text
3. **API keys live in Windows user env vars only** — never in files, never in git
4. Fixed-position layout, art box ≤2150×2150, all margins ≥0.53"
5. One book = one folder (`book1`, `book2`...) with identical structure
6. Full F1–F8 audit suite must pass + human contact-sheet review before any PDF export
7. Cover follows the Coco Wyo formula (researched live bestseller pattern)
8. Trend research = **100-book analysis only**, latest + most-sold bestsellers, weighted to Amazon.com (primary market) with .com.au as secondary (no broad scrapes)
9. **F9 caption↔image coherence must pass** before any contact-sheet review or PDF export — every caption must describe what is actually in its image (`scripts/caption_coherence.py`, runs automatically after every batch typeset)
10. **Uniform caption typography**: fixed font size across all pages of a book (80px @300DPI), word-wrap to max 2 lines — never per-page shrinking
11. **Every book ships with A+ Content (Stage 7).** Run `aplus_build.py` after the final interior + cover exist. It must produce the 4 module images AND `KDP_FINAL_UPLOAD\03_A_PLUS_CONTENT_GUIDE.txt` — the step-by-step guide with, for each module, the KDP module to pick, the image file, the alt text and a fallback headline, filled in for this book. Show the user the 4 drafts before anything goes to KDP. **Upload the 2x files** (1940 × 600 / 1940 × 1200): Amazon's 970 px sizes are minimums, and a 970 px file looks pixelated in KDP's preview and on high-resolution screens. **Every A+ hand-off ends with this table in the reply**, one per book (the script prints it, and it's at the top of the guide):

    | # | Module | Image | Alt text |
    |---|---|---|---|
    | 1 | Standard Image & Light Text Overlay (970 x 300 minimum) | `aplus_1_banner_1940x600.jpg` | … |
    | 2 | Standard Image Header With Text (970 x 600 minimum) | `aplus_2_features_1940x1200.jpg` | … |
    | 3 | Standard Image Header With Text (970 x 600 minimum) | `aplus_3_single_sided_1940x1200.jpg` | … |
    | 4 | Standard Image Header With Text (970 x 600 minimum) | `aplus_4_sample_grid_1940x1200.jpg` | … |
12. **No em dashes (—) anywhere in a book** (user rule, Oct 2026): not in captions, interior pages, covers, descriptions, A+ panels, copy-paste guides or alt text. Use a full stop, comma or colon instead. Check before every build: `grep -rn "—"` over the book folder must return nothing.
13. **The US is the primary market** (user decision, Oct 2026): Amazon.com is the KDP primary marketplace, US $9.99 is the lead price, research weights .com, and **all customer-facing text uses US spelling** ("coloring", "color", "favorite", "cozy", "check off"): title, subtitle, description, keywords, interior pages, back cover, A+ panels and alt text. Pen names, imprints and the Australian voice and facts stay. Books published before this decision keep their spelling unless the user asks.

---

## THE FINAL AGENT PIPELINE (v2.0)

```
┌────────────────────────────────────────────────────────────────────┐
│  STAGE 1: TREND SCOUT AGENT (research — 100-book analysis)         │
│  Sample: 100 books ONLY — the LATEST + MOST-SOLD:                  │
│  • 50 from Amazon.com.au bestseller lists (kids colouring/         │
│    activity categories) + "Most Sold" / Movers & Shakers           │
│  • 50 from Amazon.com bestseller lists (same categories)          │
│  Priority: recency (new releases) + sales velocity (BSR) over      │
│  breadth — no broad 500-book scrape                                │
│  • Check seasonal calendar (publish 6–8 weeks pre-peak)           │
│  • Output: ranked shortlist of 5–8 concepts with demand evidence    │
└──────────────────────────┬─────────────────────────────────────────┘
                           ▼
┌────────────────────────────────────────────────────────────────────┐
│  STAGE 2: NICHE VALIDATOR AGENT (research)                        │
│  • Live SERP census (titles, prices, reviews, page counts)        │
│  • BSR band check: winning = ≤250 reviews & BSR ≤30K              │
│  • Price check: niche must support US $9.99 (A$13.99+ on .au)     │
│  • Title collision check (exact-match search)                     │
│  • Output: GO / GO-WITH-CHANGES + locked title & keywords         │
└──────────────────────────┬─────────────────────────────────────────┘
                           ▼
┌────────────────────────────────────────────────────────────────────┐
│  STAGE 3: ASSET PRODUCER AGENT (OpenArt generation)               │
│  Tool: openart.exe generate image --model nano-banana-2            │
│  • 50 scene prompts + LOCKED suffix (rich-but-simple 6–8 habitat  │
│    elements, thick black outlines, white margins, no frames,     │
│    no text in art, nothing in bottom 6%)                          │
│  • ≤6 parallel workers (F7), cached (reruns skip done pages)      │
│  • QA gauntlet: F1 colour scan, F2 frame scan, F3 edge-touch      │
│  • Output: 50 clean B&W sources in raw2/                           │
└──────────────────────────┬─────────────────────────────────────────┘
                           ▼
┌────────────────────────────────────────────────────────────────────┐
│  STAGE 4: ASSEMBLER AGENT (interior PDF)                          │
│  • Fixed layout: art ≤2150px @ y=200, caption @2860 auto-fit,     │
│    page number bottom-right @3010                                 │
│  • 108 pages: title, copyright, belongs-to, tips+pledge,          │
│    50 art + 50 blank backs, checklist, certificate, thank-you      │
│  • Margins ≥0.53" everywhere (KDP previewer-proof)                 │
│  • Output: 01_MANUSCRIPT_INTERIOR_108P.pdf                         │
└──────────────────────────┬─────────────────────────────────────────┘
                           ▼
┌────────────────────────────────────────────────────────────────────┐
│  STAGE 5: COVER AGENT (OpenArt hero + typeset assembly)           │
│  Hero: openart.exe → coloured kawaii scene, no text               │
│  Formula (Coco Wyo bestseller pattern):                            │
│  • Cream bg + double rounded border                               │
│  • Sniglet bubble title (white fill, dark stroke, drop shadow)    │
│  • Pacifico author script top, hero centred, Baloo subtitle       │
│  • Hero ≥2K (prints ≥270 DPI), NEVER sharpened (halos, F11)        │
│  • Full wrap: 0.125" bleed + spine (pages×0.002252") + back cover │
│    with blurb, 4 sample thumbs, bio box (≤42px font, 4 lines),     │
│    KDP barcode zone 2×1.2" bottom-right                            │
│  • Output: 02_COVER_WRAP_PRINT_READY.pdf                           │
└──────────────────────────┬─────────────────────────────────────────┘
                           ▼
┌────────────────────────────────────────────────────────────────────┐
│  STAGE 6: KDP PACKAGER AGENT (metadata + upload)                  │
│  • Copy-paste guide: title, subtitle (catchy rhyme formula),       │
│    plain-text description (no raw HTML), 7 keywords, 3 categories   │
│  • NEVER check "low-content" box                                  │
│  • AI disclosure: Yes → images "some with extensive editing" →     │
│    "OpenArt, Nano Banana 2"; text = No                            │
│  • Pricing: US $9.99 primary; A$16.99 .au; £7.99 UK                │
│  • Output: KDP_FINAL_UPLOAD/ folder (manuscript + cover + guide)   │
└──────────────────────────┬─────────────────────────────────────────┘
                           ▼
┌────────────────────────────────────────────────────────────────────┐
│  STAGE 7: A+ CONTENT AGENT (Amazon product page)                  │
│  Tool: aplus_build.py (edit only the BOOK settings block)          │
│  Pattern: #1 Oceans & Seas bestseller (Coco Wyo "Ocean Scene")     │
│  • Module 1: brand banner + book mockup        1940 x 600 (2x)     │
│  • Module 2: features + 2 sample pages         1940 x 1200 (2x)    │
│  • Module 3: single-sided pages explainer      1940 x 1200 (2x)    │
│  • Module 4: 6-page sample grid                1940 x 1200 (2x)    │
│    (2x Amazon's 970 px minimum; 970 px looks pixelated in KDP)     │
│  • Sample pages rendered from the print PDF (shows the real book)  │
│  • Human checkpoint: user approves the 4 drafts                    │
│  • Output: KDP_FINAL_UPLOAD/03_A_PLUS_CONTENT/ (4 images) +        │
│    03_A_PLUS_CONTENT_GUIDE.txt — steps + per-module table:         │
│    module to pick | image | alt text | fallback headline,          │
│    ISBN/ASIN to apply it to, repeat per marketplace                │
│  • Reply to the user ends with the # | Module | Image | Alt text    │
│    table for each book (rule 11)                                   │
└────────────────────────────────────────────────────────────────────┘
```

### Per-Book Reusable Asset Checklist

Copy these from `book1/` for each new book:

| Asset | File | Reuse |
|---|---|---|
| Fonts | `fonts/` (Baloo2, Sniglet-ExtraBold, Pacifico) | copy as-is |
| Generator | `batch_generate.py` | swap prompts table + captions.json |
| Assembler | `create_kdp_package.py` | swap title strings + checklist names |
| Prompts | `PAGE-GENERATION-PROMPTS.md` template | 50 new scenes |
| Facts | `captions.json` | 50 new one-liners |
| Upload guide | `KDP_FINAL_UPLOAD/00_COPY_PASTE_INTO_KDP.txt` | new title/keywords |
| Page tracer | `vectorize_pages.py` + `..\scripts\vectorize_line_art.py` | copy as-is |
| A+ Content | `aplus_build.py` (from `Author 1\book2\`) | edit the `BOOK` block: titles, sample pages + animal names, features, panel colour, ISBN/ASIN |

### Book 2 Candidates (from Stage 1 research, ranked)

1. **Aussie Cuties at Christmas** — Q4 window (publish by ~Oct 20 for Nov–Dec peak); reuse 80% of pipeline
2. **Great Barrier Reef Ocean Friends** — ocean theme evergreen
3. **Outback Australian Adventures** — desert/dingo/camel scenes

### Cost & Time per Book (validated on Book 1)

| Item | Value |
|---|---|
| OpenArt credits | ~3,000 (50 pages + regens + covers) |
| Calendar time | 1–2 days (pipeline is fully scripted) |
| Human checkpoints | 3 (contact-sheet approval, cover choice, A+ drafts) |
| Unit economics (.au) | A$16.99 − A$5.28 print = **A$4.91/sale** |
| Break-even | ~600 sales (vs. Starter credit cost) |
