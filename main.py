#!/usr/bin/env python3
"""Place the entry image at $MAKEFUN_OUTPUT_DIR/entry.png.

The poster itself (entry.png) was drawn for Friday, 20 November 2026
by draw.py in this repository. This program only copies the finished
image to the output directory, so the graded run is byte-for-byte
deterministic. Standard library only; no network, no clock.
"""

import hashlib
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    # Copy through a temp file and rename, so a failed run never
    # leaves a half-written image behind.
    tmp = out_dir / ".entry.png.tmp"
    shutil.copyfile(SOURCE, tmp)
    os.replace(tmp, target)
    if _sha256(target) != _sha256(SOURCE):
        raise SystemExit("output differs from entry.png")
    print(f"Wrote {target} ({target.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
