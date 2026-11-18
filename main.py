#!/usr/bin/env python3
"""make.fun entry: news-image-20261118 (Manja lane).

Writes one image — a one-page summary of the world's news of Wednesday
18 November 2026 — to /output/entry.png.

The image is baked into this repository (assets/entry.png), rendered by
render.py from the news data in data/news.json. This program copies it to
the output path and verifies it meets the bounty limits (PNG, at most
1024x1024, at most 1 MiB). Pure standard library: no network, no
randomness, no timestamps — running it twice writes identical bytes.
"""
import hashlib
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "assets", "entry.png")
DST = "/output/entry.png"
MAX_BYTES = 1 * 1024 * 1024
MAX_DIM = 1024


def png_dimensions(path):
    """Read width/height from a PNG IHDR chunk (pure stdlib)."""
    with open(path, "rb") as f:
        head = f.read(33)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file")
    if head[12:16] != b"IHDR":
        raise ValueError("missing IHDR chunk")
    w, h = struct.unpack(">II", head[16:24])
    return w, h


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    if not os.path.isfile(SRC):
        print(f"missing baked image: {SRC}", file=sys.stderr)
        return 1
    w, h = png_dimensions(SRC)
    if w > MAX_DIM or h > MAX_DIM:
        print(f"image too large: {w}x{h} (max {MAX_DIM}x{MAX_DIM})",
              file=sys.stderr)
        return 1
    size = os.path.getsize(SRC)
    if size > MAX_BYTES:
        print(f"image too big: {size} bytes (max {MAX_BYTES})",
              file=sys.stderr)
        return 1
    os.makedirs(os.path.dirname(DST), exist_ok=True)
    shutil.copyfile(SRC, DST)
    if sha256(SRC) != sha256(DST):
        print("copy verification failed", file=sys.stderr)
        return 1
    print(f"wrote {DST} ({w}x{h}, {size} bytes, sha256 {sha256(DST)[:16]}...)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
