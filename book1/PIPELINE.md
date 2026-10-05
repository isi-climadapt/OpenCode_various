# CANONICAL PRODUCTION PIPELINE v1.0 — "The Golden Path"

> This is THE locked, approved pipeline that produced the final `raw\` set for Book 1 (verified Oct 2026).
> All future books (Books 2, 3, ...) MUST use this exact approach. Do not deviate without a logged reason.

## Pipeline stages (in order)

```
[PROMPTS] PAGE-GENERATION-PROMPTS.md  ──┐
[FACTS]   captions.json                ──┼──>  batch_generate.py  ──>  raw2\ (native art)  ──>  raw\ (print pages)
[DRIVER]  batch_generate.py            ──┘         (OpenArt CLI)         (cache layer)        (2550x3300 final)
```

1. **Generate:** OpenArt CLI (`openart.exe generate image --model nano-banana-2 -o raw2\<page>.png`), 6 parallel workers max (Starter throttles above). Caching: existing raw2 files >10KB are skipped.
2. **Post-process per page** (all in `pad_and_caption`):
   - Grayscale → `autocontrast(cutoff=1)`
   - **Aspect-preserving fit into 2400×2400** (`min(2400/w, 2400/h)` scale — NEVER blind-square-stretch)
   - Binarize: `p < 110 → black, else white`
   - **FIXED paste at y=150, horizontally centred** on 2550×3300 canvas ← this is the anti-overlap guarantee: art bottom ≤ 2550, caption zone starts 2880
3. **Typeset:**
   - Caption: Baloo 2, baseline 115px, auto-shrink −5px steps until it fits 2250px width, centred at y=2880, pure black
   - Page number: Baloo 2, 62px, grey(120), **bottom-right corner** (right inset 130px, y=3010), formula `N*2-1`
4. **QA:** greys scan on art zone; failures regenerate; frame/edge-touch/colour audits per PRODUCTION-STANDARD.md §6b
5. **Contact sheet** rebuild for human sign-off before any PDF assembly

## Layout constants (LOCKED — overlap-proof by construction)

| Constant | Value | Why |
|---|---|---|
| Canvas | 2550×3300 (8.5×11 @ 300 DPI) | KDP trim |
| Art fit box | 2400×2400 max, aspect-preserving | no distortion |
| Art paste | x=(2550−w)/2, **y=150 FIXED** | art bottom ≤2550 |
| Caption baseline | y=2880, centred | 330px clear gap from art |
| Page number | bottom-right, x inset 130, y=3010 | approved corner style |
| Margins | all content ≥0.375" print-safe | KDP no-bleed spec |

## Prompt formula (LOCKED)

`scene text (from prompt table) + SUFFIX` where SUFFIX mandates:
- Rich-but-simple: 6–8 habitat elements, each one big closed shape
- **"generous plain white margin on every side; no element touches the image edges"**
- **"no frame or border around the image edge"**
- Very thick marker-friendly pure-black outlines; no grey/colour/texture
- No text/letters anywhere in art (all lettering typeset programmatically)
- Nothing in bottom 6% of page (caption strip)

## Known failure modes → mandatory audits (from Book 1 production)

| ID | Failure | Audit | Fix |
|---|---|---|---|
| F1 | Colour fill sneaks in | RGB saturation scan | binarize strip; regen if ugly |
| F2 | Drawn frame/border box | 65%+ line-span scan in edge bands | regen with margin phrase |
| F3 | Art touching raw edges | outer-12px ink count | regen with margin phrase |
| F4 | Stretch distortion | raw2 non-square + blind stretch | aspect-preserving fit ONLY |
| F5 | Caption clipped | textbbox wider than 2250 | auto-shrink font (in driver) |
| F6 | Caption/art overlap | ink scan of gap band 2600–2860 | **fixed y=150 paste — never ink-bbox centering** |
| F7 | Parallel throttle | CLI exit + stderr msg | ≤6 workers, retry failed |
| F8 | OneDrive file lock | OSError on save | retry ×3 with 1.5s sleep |

## Hard rules (never break)

1. Text/numbers are ALWAYS typeset programmatically (Baloo 2) — never AI-generated lettering
2. `raw2\` = native sources (keep); `raw\` = final print pages (assemble target)
3. Secrets (API keys) live in Windows user env vars ONLY — never in files, never in git (see .gitignore)
4. Run full audit suite before the contact sheet goes for human review
5. One book = one folder (book1, book2...) with identical file structure

## Run commands

```powershell
# full run (skips cached pages)
py batch_generate.py

# selected pages only
py batch_generate.py --only page_01 page_09

# after any regen, full-book audit + contact sheet
py -c "from PIL import Image; ..."   # per PRODUCTION-STANDARD.md §6b scripts
```

## Tool stack (as approved)

- **Interiors:** OpenArt CLI / nano-banana-2 (~50 credits/page; Plus plan for commercial rights)
- **Covers: OpenArt CLI / nano-banana-2 — ALWAYS (locked rule; never Gemini for covers)**
- **Vector specialist:** Recraft (SVG titles/logos, vectorize, crisp_upscale)
- **Rasterizer:** resvg (installed via resvg-cli wheel)
- **Fonts:** Baloo 2 (SIL OFL) at `book1\fonts\Baloo2.ttf`

## Cover pipeline (LOCKED — copy of Amazon bestseller formula)

Script: `py cover_build.py [--regen] [--only A|B|C]` (per-book copy)

1. **Hero via OpenArt** (`nano-banana-2`), coloured illustration prompt: "Children's colouring book cover illustration: [hero scene]. Bright/soft colours, kawaii cute style, chunky rounded shapes, centred, professional kids book cover art. No text, no words, no letters, no watermark."
2. **Assembly (always typeset, never AI lettering):**
   - Soft solid background + playful double rounded border frame
   - Title: Baloo 2, 300px, two lines, centred top
   - Hero: coloured OpenArt scene, ≤1950px, centred at y=720
   - Subtitle: "A Bold & Easy Colouring Book for Kids" (130px)
   - Badge line: "Ages 3-8 | 50 Big & Bold Designs with Fun Facts" (100px)
   - Author/imprint: "Matilda Hayes | Gumleaf Kids Press" (95px, grey)
3. Design source: Amazon bestseller pattern research (Coco Wyo 8.7K reviews / FairyWren 1.5K reviews formula: one adorable coloured hero + chunky rounded title + clean soft background)
