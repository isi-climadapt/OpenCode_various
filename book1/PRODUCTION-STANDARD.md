# Book 1 — Production Standard (interior art) — magnet spec v1.0

> Governs EVERY page sent to the assembler. If an image violates any "MUST", it gets regenerated.
> Trim: 8.5 × 11 in paperback, black & white interior, no-bleed build (all 108 pages single-sided symmetric).

---

## 1. Canvas & resolution

| Item | Spec | Why |
|---|---|---|
| Final page size | **2550 × 3300 px** exactly | 8.5×11 in @ 300 DPI |
| Working resolution in AI tool | ≥ 2048 px on the long side (e.g. Midjourney 1456×2048, DALL·E 1024×1792, Ideogram/FLUX 1024×1024→pad) | native detail for upscaler |
| Upscale path | Upscayl (free) "4x" or Topaz Gigapixel → then **pad/crop to 2550×3300 on white** | never stretch; lock aspect |
| Minimum DPE (effective) | 300 DPI at print size | KDP reject threshold is 72, we stay way above |
| Colour mode | 8-bit grayscale or RGB (both fine) — **no alpha channel needed** | final PDF converts anyway |
| Final step per image | Levels: push blacks to 0, whites to 255 (pure black on pure white, NO greys survive) | grey = muddy print + 1-star reviews |

### Canvas zoning (no-bleed build)
```
┌──────────────────────────────┐  0 ──┐
│  TOP SAFE MARGIN  0.5" = 150px│      │ art may enter
│  (title/ Accreditation zone)  │      │
├──────────────────────────────┤ 150  │
│                              │      │
│        ART ZONE              │      │ hero animal lives here
│   hero fills 55–70% height   │      │
│                              │      │
├──────────────────────────────┤ 2835 │ caption strip start
│  CAPTION STRIP 0.6" = 180px  │      │ EMPTY in art
│  (fun-fact text typeset here)│      │
├──────────────────────────────┤ 3010 │
│  BOTTOM MARGIN 0.87"=260px   │      │
└──────────────────────────────┘ 3300 ┘
   left/right: keep art inside
   x = 150 … 2400 (0.5" side margins)
```

## 2. Line weights (the heart of "bold & easy")

| Stroke role | Thickness @300 DPI | In points (÷4.17) | Share of art |
|---|---|---|---|
| **Main outline** (body silhouettes, head, big props) | **10–14 px** | 2.4–3.4 pt | everything structural |
| **Secondary outline** (inner ear, shell segments, wing edges) | **7–9 px** | 1.7–2.2 pt | ~20% of lines |
| **Detail accent** (smiles, spots, tiny stars) | **6–8 px** minimum | 1.4–1.9 pt | oldest kids see it |
| FORBIDDEN | anything < 6 px, hairlines, crosshatch, stippling, dotted fills | — | 0% |

Practical test: **at 20% zoom (thumbnail), every shape must read.** At 100% zoom, lines look chunky (almost comic-book).

Line style:
- Round caps and round joins everywhere
- Perfectly closed contours (no visible gaps where a colour could "escape" a region)
- No half-transparent strokes; pure #000000 on pure #FFFFFF

## 3. Composition rules per page

1. **Hero size:** animal occupies **55–70% of page height** (Coco Wyo benchmark). Nothing tiny.
2. **Cuteness lock:** head-to-body ratio ≈ 1:1.3; eyes large and simple (dot + arc for closed/happy); max 2 carefully-placed face lines.
3. **Open space ≥ 60% of the page** — big blank colourable regions, not line-stuffed.
4. **Background accents (max 3):** grass tufts, leaves, water waves, clouds, stars — each one = single closed shape, no texture strokes within.
5. **One scene, one message:** hero + optional 1 small friend (baby joey, butterfly, tiny fish). Never a crowd.
6. **Caption strip must be EMPTY** in the artwork — no floor shadow, no ground scribbles inside the bottom 180px; the typesetter adds the fun fact there.
7. **No landscape/portrait mixing** — all portrait.
8. **No text/letters/numbers/watermarks/signatures anywhere.** If the AI writes anything, reject.
9. **No shading/gray/hatching/colour fill.** Interiors of shapes stay WHITE so kids colour them.
10. Scene coherence: animal on the ground/branch/water — feet/wheels actually touch the ground line where applicable.

## 4. Age-band calibration (ages 3–8)

| Zone | Rule |
|---|---|
| Complexity ceiling | ≤ 12 distinct closed regions per page (a 3-y/o can finish one page in 10–15 min) |
| Smallest colourable region | ≥ 1.0 cm² at print (≈ 118 × 118 px)- e.g. eyes must be ≥ 60px wide circles, not pinheads |
| Edge-to-edge consistency | All 50 pages must sit within ±15% of the same "crowdedness" — flip test |
| Difficult-per-page spread | Pages 1–8 super simple (10 or fewer regions) → 9–50 gradually add prop count, never new line styles |

## 5. File handling

| Item | Spec |
|---|---|
| Filename | `page_01.png` … `page_50.png` (two digits, zero-padded, matching the 50-scene table) |
| Format | PNG (PNG-24 fine); no interlacing; no embedded colour profile required |
| Placeholder location | `book1\raw\` — overwrite the old script-generated art |
| Keep originals | save the AI-native resolution file too in `book1\raw\native\` (for later re-upscales) |
| Jpeg? | Never for line art (ringing artifacts produce grey halos). PNG only. |

## 6. QA scorecard (run every page; ≥ 9/10 to pass)

1. Outline thickness in 10–14px band at final size? (2)
2. All shapes closed, no gaps? (1)
3. Pure black/white only — zero greys? (1)
4. Hero ≥ 55% page height? (1)
5. ≥ 60% open white space? (1)
6. Nothing in caption strip / margins respected? (1)
7. Face symmetry fine & cute (not uncanny/AI artifact)? (1)
8. No accidental text or watermark? (1)
9. Recognizable Aussie animal at thumbnail size? (1)
10. Print-contrast crisp after levels cleanup? (1)

Retry policy: max 2 regenerations per failing page; if it still fails on attempt 3 → simplify the scene prompt (drop background accents) and retry once more.

## 7. Optional polish pipeline (recommended before handoff)

1. Batch: convert to grayscale → Image > Adjustments > Levels (0, 128, 235 → 0/255 endpoints)
2. Spot-erase any AI stray dots (clone stamp on white)
3.pad to 2550×3300 white canvas, centred, preserving aspect (no crop of hero)
4. Save PNG → drop in `book1\raw\`

## 8. Typo/font spec for the assembler (info for Agent 4)

- Caption font: rounded, friendly, dyslexia-lean: **Baloo 2** (SIL Open Font License) or Quicksand Semi-Bold
- Caption size: ~30 pt (≈125 px @300 dpi) centred inside the caption strip; single line, max ~45 characters (already in prompt pack)
- Page numbers: 14 pt, bottom-centre inside the 0.5" bottom strip, skipping picture pages? — NO: numbers go on the caption strip left corner (0.25" from bottom), colour-scheme black.
- Title/copyright pages: same family, larger weights.

## 9. KDP compliance refs (final checklist before upload)

- [ ] All 50 art pages single-sided (blank backs built by assembler)
- [ ] 108pp total (front/back matter per the idea-bank build sheet)
- [ ] No-bleed build: all content ≥ 0.375" from edges; gutter 0.375" (safe: page count < 151)
- [ ] Fonts embedded in PDF; PDF exported "press-quality", no transparency flattening artifacts
- [ ] Every generated asset declared as AI-generated in the KDP questionnaire (honest)
- [ ] Author: Matilda Hayes · Imprint: Gumleaf Kids Press · Series: Gumleaf Aussie Friends
