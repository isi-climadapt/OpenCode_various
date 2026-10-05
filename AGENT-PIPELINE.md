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
| **Branding** | Verified clean on Bing + Amazon AU | Pen name **Matilda Hayes** / Imprint **Gumleaf Kids Press** |
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

### Hard Rules (never break)

1. **OpenArt CLI / nano-banana-2 for ALL generation** (interiors + covers) — never Gemini, never Recraft
2. **All lettering typeset programmatically** (Baloo 2 / Sniglet / Pacifico) — never AI-generated text
3. **API keys live in Windows user env vars only** — never in files, never in git
4. Fixed-position layout, art box ≤2150×2150, all margins ≥0.53"
5. One book = one folder (`book1`, `book2`...) with identical structure
6. Full F1–F8 audit suite must pass + human contact-sheet review before any PDF export
7. Cover follows the Coco Wyo formula (researched live bestseller pattern)

---

## THE FINAL AGENT PIPELINE (v2.0)

```
┌────────────────────────────────────────────────────────────────────┐
│  STAGE 1: TREND SCOUT AGENT (research)                             │
│  • Scan Amazon .au/.com bestsellers for kids colouring            │
│  • Check seasonal calendar (publish 6–8 weeks pre-peak)          │
│  • Output: ranked shortlist of 5–8 concepts with demand evidence   │
└──────────────────────────┬─────────────────────────────────────────┘
                           ▼
┌────────────────────────────────────────────────────────────────────┐
│  STAGE 2: NICHE VALIDATOR AGENT (research)                        │
│  • Live SERP census (titles, prices, reviews, page counts)        │
│  • BSR band check: winning = ≤250 reviews & BSR ≤30K              │
│  • Price floor check: niche must support A$13.99+                 │
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
│  • UnsharpMask(radius=2.0) on hero for 300 DPI print sharpness     │
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
│  • Pricing: .au floor A$13.99, anchor A$16.99 (A$4.91/sale)        │
│  • Output: KDP_FINAL_UPLOAD/ folder (manuscript + cover + guide)   │
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

### Book 2 Candidates (from Stage 1 research, ranked)

1. **Aussie Cuties at Christmas** — Q4 window (publish by ~Oct 20 for Nov–Dec peak); reuse 80% of pipeline
2. **Great Barrier Reef Ocean Friends** — ocean theme evergreen
3. **Outback Australian Adventures** — desert/dingo/camel scenes

### Cost & Time per Book (validated on Book 1)

| Item | Value |
|---|---|
| OpenArt credits | ~3,000 (50 pages + regens + covers) |
| Calendar time | 1–2 days (pipeline is fully scripted) |
| Human checkpoints | 2 (contact-sheet approval, cover choice) |
| Unit economics (.au) | A$16.99 − A$5.28 print = **A$4.91/sale** |
| Break-even | ~600 sales (vs. Starter credit cost) |
