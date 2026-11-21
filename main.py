#!/usr/bin/env python3
"""Entry program for the news-image-20261121 competition.

The picture itself ships in this repository as entry.png (drawn by
make_image.py). This program's whole job is to place that file in the
output directory, byte for byte, so the two grader runs agree exactly.
It uses only the Python standard library and touches no network.
"""

import os
import shutil
import sys
from pathlib import Path

REPO_DIR = Path(__file__).resolve().parent
IMAGE = REPO_DIR / "entry.png"
MAX_BYTES = 1_048_576  # the gate's 1 MiB cap


def output_dir() -> Path:
    """Where the grader wants the image: $MAKEFUN_OUTPUT_DIR or /output."""
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def main() -> int:
    if not IMAGE.is_file():
        print(f"entry image not found: {IMAGE}", file=sys.stderr)
        return 1
    target_dir = output_dir()
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / "entry.png"
    shutil.copyfile(IMAGE, target)
    written = target.stat().st_size
    if written > MAX_BYTES:
        print(f"entry image over the size cap: {written} bytes",
              file=sys.stderr)
        return 1
    print(f"wrote {target} ({written} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
