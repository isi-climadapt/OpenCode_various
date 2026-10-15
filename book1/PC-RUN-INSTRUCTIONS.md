# PC run instructions: regenerate art at print resolution

Instructions for a Claude Code session running on the Windows PC where the OpenArt CLI is installed and signed in. Cloud sessions can't use the OpenArt sign-in, so this work has to run on the PC.

## Why this is needed

The published books (Aussie Cuties, and Great Barrier Reef Ocean Friends) print soft for three reasons:

- OpenArt nano-banana-2 art came out at 1024 px. The cover hero crop `book1/kangaroo_frame_cropped.png` is 931 px. Both were enlarged about 2.2x to fill the page, which prints at about 130-140 DPI. KDP needs 300.
- `UnsharpMask` drew light halos around every outline.
- Pillow saved both PDFs as quality-75 JPEG.

Branch `claude/brave-bardeen-oj84gz` already fixes the code (see "Print resolution rules" in `book1/PIPELINE.md`):

- `book1/openart_cli.py` requests `--resolution 2K` for interior pages and `4K` for the cover hero. It falls back to the default size with a warning if the CLI rejects the option. The OpenArt executable is found through the `OPENART_EXE` env var, then PATH, then `C:\Users\ibian\AppData\Local\Programs\openart\bin\openart.exe`.
- `book1/create_kdp_package.py` refuses to build if any art prints below 270 DPI. `--allow-lowres` overrides it for drafts only.

## Before you start

Check each of these on the PC. Stop and report anything missing.

- `git`, Python 3 (`py`) and Pillow 9.1 or later: `py -c "import PIL; print(PIL.__version__)"`
- The OpenArt CLI: `openart version`. If it's missing, install it in PowerShell with `irm https://raw.githubusercontent.com/OpenArt-AI/cli/main/install.ps1 | iex`, then run `openart login`. The login opens a browser, so the user has to do it.
- Signed in: `openart account`

## Steps

1. Run `git fetch origin`, then `git checkout claude/brave-bardeen-oj84gz`. Work from the `book1` folder.
2. Run `openart model form nano-banana-2 text2image`. Confirm the resolution option is named `--resolution` and accepts `2K` and `4K`. If the name or values differ, update `openart_cli.py` to match.
3. Run `openart model cost --model nano-banana-2`. Report the credit cost for 50 pages at 2K plus 3 cover heroes at 4K. **Wait for the user's OK before generating anything.**
4. Move the existing `raw2\*.png` files into `raw2_1k\`. Don't delete them. `batch_generate.py` skips any image that already exists, so they have to be moved first.
5. Run `py batch_generate.py`. Check that every new `raw2` file is about 2048 px and passes the script's QA. Regenerate any flagged pages.
6. Run `py cover_build.py --regen --only C` to generate the kangaroo and joey hero at 4K. Make a new `kangaroo_frame_cropped.png` from it, at least 2150 px wide and framed the same way as the current crop. Show the user the old and new crops side by side, and replace the file only after they approve.
7. Run `py create_kdp_package.py` without `--allow-lowres`. It must build with no low-resolution warnings.
8. Check the output:
   - `KDP_FINAL_UPLOAD\01_MANUSCRIPT_INTERIOR_108P.pdf` has 108 pages at 8.5 × 11 inches.
   - `KDP_FINAL_UPLOAD\02_COVER_WRAP_PRINT_READY.pdf` shows no light halos around outlines at 400% zoom.
   - Show the user `KDP_FINAL_UPLOAD\COVER_PREVIEW.png`.
9. Commit the new art and the rebuilt `KDP_FINAL_UPLOAD` files to `claude/brave-bardeen-oj84gz` and push. Don't open a pull request unless the user asks.

## Done when

- `create_kdp_package.py` builds with no low-resolution warnings.
- Everything in `KDP_FINAL_UPLOAD` comes from 2K/4K art.
- The user has approved the new cover crop.

## After that

Ocean Friends isn't in this repo. Ask the user where its files are, then repeat steps 4-8 for it.
