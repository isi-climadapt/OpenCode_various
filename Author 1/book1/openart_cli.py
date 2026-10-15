# -*- coding: utf-8 -*-
# Thin wrapper around the OpenArt CLI shared by batch_generate.py and cover_build.py.
# Asks nano-banana-2 for 2K/4K output so art arrives at print size. The model's
# default 1K output has to be enlarged ~2x to fill a page, and enlarged art prints soft.
#
# Check the option names your CLI build accepts with:
#   openart model form nano-banana-2 text2image
# and the credit cost per resolution with:
#   openart model cost --model nano-banana-2

import os, shutil, subprocess

EXE = (os.environ.get("OPENART_EXE") or shutil.which("openart")
       or r"C:\Users\ibian\AppData\Local\Programs\openart\bin\openart.exe")
MODEL = "nano-banana-2"


def generate_image(prompt, out_path, resolution="2K", timeout=600):
    """Generate one image. Returns (ok, message)."""
    base = [EXE, "generate", "image", prompt, "--model", MODEL, "-o", out_path, "--quiet", "--yes"]
    r = subprocess.run(base + ["--resolution", resolution], capture_output=True, text=True, timeout=timeout)
    if r.returncode == 0:
        return True, "ok (%s)" % resolution
    # No retry at the default size: 1K art fails the 270 DPI preflight in
    # create_kdp_package.py, so a fallback only spends credits on unusable pages.
    # CLI v0.1.1 rejects --resolution for images (github.com/OpenArt-AI/cli/issues/2).
    return False, "FAIL " + (r.stderr or r.stdout)[-200:]
