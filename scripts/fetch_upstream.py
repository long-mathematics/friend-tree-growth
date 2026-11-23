#!/usr/bin/env python3
"""Fetch the five immutable upstream inputs after checking SHA-256 digests.

No credentials are required. Files are written only below the selected cache
directory. A pre-existing file with a different digest is rejected rather than
silently overwritten. The complete upstream license is among the inputs.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "verification" / "upstream_manifest.json"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def prepare_source(directory: Path, *, download: bool = True) -> dict:
    manifest = json.loads(MANIFEST_PATH.read_text())
    for name, expected in manifest["files"].items():
        destination = directory / name
        if not destination.exists():
            if not download:
                raise FileNotFoundError(f"Missing pinned source: {destination}")
            url = ("https://raw.githubusercontent.com/uzay-eth/friend-tree-exponent/"
                   + manifest["commit"] + "/" + name)
            request = Request(url, headers={"User-Agent": "friend-tree-growth-verifier"})
            with urlopen(request, timeout=60) as response:
                content = response.read()
            actual = hashlib.sha256(content).hexdigest()
            if actual != expected:
                raise ValueError(f"Download digest mismatch for {name}: {actual}")
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(content)
        actual = digest(destination)
        if actual != expected:
            raise ValueError(f"Pinned source digest mismatch for {name}: {actual}")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path,
                        default=ROOT / ".cache" / "upstream")
    parser.add_argument("--offline", action="store_true",
                        help="Require every source file to be present already.")
    args = parser.parse_args()
    manifest = prepare_source(args.directory, download=not args.offline)
    print(json.dumps({"status": "PASS", "commit": manifest["commit"],
                      "sha256_verified_files": len(manifest["files"]),
                      "directory": str(args.directory)}, indent=2))


if __name__ == "__main__":
    main()
