#!/usr/bin/env python3
"""Entry program for make.fun competition news-image-20261118.

Copies the pre-rendered poster entry.png (built by build_poster.py)
byte-for-byte into the output directory, as /output/entry.png or
$MAKEFUN_OUTPUT_DIR/entry.png. Standard library only.
"""

import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("wrote", dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
