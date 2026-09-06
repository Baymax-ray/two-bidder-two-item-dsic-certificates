#!/usr/bin/env python3
"""Create the root SHA-256 manifest for stable release files."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "SHA256SUMS"
SKIP_DIR_NAMES = {".git", "__pycache__"}
SKIP_PREFIXES = {("manuscript", "build"), ("verification", "generated")}
SKIP_SUFFIXES = (
    ".pyc", ".aux", ".log", ".out", ".toc", ".bbl", ".blg",
    ".fls", ".fdb_latexmk", ".synctex.gz",
)


def skipped(relative: Path) -> bool:
    if any(part in SKIP_DIR_NAMES for part in relative.parts):
        return True
    if any(relative.parts[: len(prefix)] == prefix for prefix in SKIP_PREFIXES):
        return True
    return relative.name.lower().endswith(SKIP_SUFFIXES)


def stable_files() -> list[Path]:
    files = []
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT)
        if skipped(relative) or not path.is_file() or path == MANIFEST:
            continue
        if path.is_symlink():
            raise RuntimeError(f"symbolic link not supported: {relative.as_posix()}")
        files.append(path)
    return sorted(files, key=lambda path: path.relative_to(ROOT).as_posix())


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            value.update(block)
    return value.hexdigest()


def main() -> None:
    lines = [
        f"{digest(path)}  {path.relative_to(ROOT).as_posix()}"
        for path in stable_files()
    ]
    MANIFEST.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"WROTE_SHA256SUMS files={len(lines)}")


if __name__ == "__main__":
    main()
