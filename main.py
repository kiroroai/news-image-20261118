#!/usr/bin/env python3
"""Entry program for make.fun competition news-image-20261118.

Copies the pre-rendered poster entry.png (built by build_poster.py)
byte-for-byte into the output directory, as /output/entry.png or
$MAKEFUN_OUTPUT_DIR/entry.png. Standard library only.

The copy is verified: the output must be byte-identical to the source
and within the competition limits (at most 1 MiB, at most 1024x1024 px).
"""

import hashlib
import os
import shutil
import sys

MAX_BYTES = 1048576
MAX_DIM = 1024


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def png_dimensions(path):
    """Read width/height from a PNG header (no decoder needed)."""
    with open(path, "rb") as f:
        header = f.read(33)
    if header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("entry.png is not a PNG file")
    width = int.from_bytes(header[16:20], "big")
    height = int.from_bytes(header[20:24], "big")
    return width, height


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        print("error: entry.png not found next to main.py", file=sys.stderr)
        return 1
    if os.path.getsize(src) > MAX_BYTES:
        print("error: entry.png exceeds 1 MiB", file=sys.stderr)
        return 1
    width, height = png_dimensions(src)
    if width > MAX_DIM or height > MAX_DIM:
        print("error: entry.png exceeds 1024x1024 px", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    if sha256(dst) != sha256(src):
        print("error: output differs from source", file=sys.stderr)
        return 1
    print("wrote %s (%dx%d, %d bytes)" % (dst, width, height,
                                          os.path.getsize(dst)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
