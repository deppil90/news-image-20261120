#!/usr/bin/env python3
"""Entry point for the news-image-20261120 competition.

Copies the pre-drawn entry.png (which sits next to this file) into the
directory named by MAKEFUN_OUTPUT_DIR, as entry.png. Deterministic:
same input bytes, same output bytes, every run. Standard library only,
no network access, no clock reads.
"""

import hashlib
import os
import shutil
import sys

SOURCE_NAME = "entry.png"
TARGET_NAME = "entry.png"
CHUNK = 65536
MAX_BYTES = 1048576


def fail(message):
    print("main.py: " + message, file=sys.stderr)
    return 1


def locate_source():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, SOURCE_NAME)


def resolve_target():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        return None
    return os.path.join(out_dir, TARGET_NAME)


def copy_and_digest(source, target):
    """Copy source to target atomically and return (sha256, byte count).

    Bytes go to a scratch file first and are moved into place only once
    fully written, so an interrupted run never leaves a partial entry.png.
    The digest is re-checked after the move.
    """
    scratch = target + ".tmp"
    digest = hashlib.sha256()
    total = 0
    with open(source, "rb") as src, open(scratch, "wb") as dst:
        while True:
            block = src.read(CHUNK)
            if not block:
                break
            total += len(block)
            if total > MAX_BYTES:
                os.unlink(scratch)
                return None, total
            digest.update(block)
            dst.write(block)
    os.replace(scratch, target)
    check = hashlib.sha256()
    with open(target, "rb") as handle:
        while True:
            block = handle.read(CHUNK)
            if not block:
                break
            check.update(block)
    if check.hexdigest() != digest.hexdigest():
        return None, total
    return digest.hexdigest(), total


def main():
    source = locate_source()
    if not os.path.isfile(source):
        return fail("source image not found: " + source)
    target = resolve_target()
    if target is None:
        return fail("MAKEFUN_OUTPUT_DIR is not set")
    os.makedirs(os.path.dirname(target), exist_ok=True)
    digest, total = copy_and_digest(source, target)
    if digest is None:
        return fail("source image exceeds the 1 MiB limit")
    print("wrote {} ({} bytes, sha256 {})".format(target, total, digest))
    return 0


if __name__ == "__main__":
    sys.exit(main())
