#!/usr/bin/env python3
"""Fail closed unless SHA256SUMS covers every stable release file exactly."""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "SHA256SUMS"
SKIP_DIR_NAMES = {".git", "__pycache__"}
SKIP_PREFIXES = {("manuscript", "build"), ("verification", "generated")}
SKIP_SUFFIXES = (
    ".pyc", ".aux", ".log", ".out", ".toc", ".bbl", ".blg",
    ".fls", ".fdb_latexmk", ".synctex.gz",
)
HEX64 = re.compile(r"[0-9a-f]{64}")


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


def claimed_hashes() -> dict[str, str]:
    claimed: dict[str, str] = {}
    for number, line in enumerate(MANIFEST.read_text(encoding="utf-8").splitlines(), 1):
        if "  " not in line:
            raise RuntimeError(f"malformed manifest line {number}")
        expected, name = line.split("  ", 1)
        posix = PurePosixPath(name)
        if (
            not HEX64.fullmatch(expected)
            or not name
            or "\\" in name
            or posix.is_absolute()
            or any(part in {"", ".", ".."} for part in posix.parts)
        ):
            raise RuntimeError(f"malformed manifest line {number}")
        if name in claimed:
            raise RuntimeError(f"duplicate manifest path: {name}")
        resolved = (ROOT / Path(*posix.parts)).resolve()
        if ROOT.resolve() not in resolved.parents:
            raise RuntimeError(f"manifest path escapes archive: {name}")
        claimed[name] = expected
    return claimed


def main() -> int:
    try:
        claimed = claimed_hashes()
        actual = stable_files()
        names = {path.relative_to(ROOT).as_posix() for path in actual}
        if set(claimed) != names:
            raise RuntimeError(
                f"coverage mismatch: missing={sorted(names-set(claimed))}, "
                f"extra={sorted(set(claimed)-names)}"
            )
        for path in actual:
            name = path.relative_to(ROOT).as_posix()
            if digest(path) != claimed[name]:
                raise RuntimeError(f"hash mismatch: {name}")
        print(f"VERIFIED_SHA256SUMS files={len(actual)}")
        return 0
    except (OSError, RuntimeError) as error:
        print(f"HASH_VERIFICATION_FAILED: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
