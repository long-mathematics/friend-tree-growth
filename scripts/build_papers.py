#!/usr/bin/env python3
"""Build the two research drafts with a standard LaTeX installation.

Only the Python standard library is needed. Install a TeX distribution with
amsmath, amsthm, mathtools, lmodern, microtype, booktabs, and hyperref.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PAPERS = {
    "original": "friend_tree_growth",
    "local": "local_redirection_irrationality",
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paper", choices=["all", *PAPERS], default="all")
    parser.add_argument("--engine", default="pdflatex")
    parser.add_argument("--format", type=Path, help="optional format for pdftex")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "build" / "papers")
    args = parser.parse_args()
    engine = shutil.which(args.engine)
    if engine is None:
        parser.error(f"LaTeX engine not found: {args.engine}")
    build_dir = args.output_dir.resolve()
    build_dir.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    # Reproducible PDF timestamps for this dated research draft. The caller can
    # override the epoch for a later revision without modifying the build tool.
    env.setdefault("SOURCE_DATE_EPOCH", "1795392000")  # 2026-11-23 00:00 UTC
    env.setdefault("FORCE_SOURCE_DATE", "1")
    selected = PAPERS.values() if args.paper == "all" else [PAPERS[args.paper]]
    reports = []
    for name in selected:
        source = ROOT / f"{name}.tex"
        if not source.is_file():
            raise SystemExit(f"Missing manuscript: {source}")
        command = [engine]
        if args.format is not None:
            command.append(f"-fmt={args.format.resolve()}")
        command += [
            "-interaction=nonstopmode", "-halt-on-error", "-file-line-error",
            f"-output-directory={build_dir}", source.name,
        ]
        for pass_number in range(1, 4):
            result = subprocess.run(
                command, cwd=ROOT, env=env, text=True,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            )
            (build_dir / f"{name}.pass-{pass_number}.txt").write_text(result.stdout)
            if result.returncode:
                print(result.stdout[-8000:])
                raise SystemExit(f"{name}: LaTeX failed on pass {pass_number}")
        log = (build_dir / f"{name}.log").read_text(errors="replace")
        forbidden = [
            "Overfull", "undefined references", "undefined citations",
            "There were undefined", "multiply defined", "Rerun to get",
        ]
        defects = [line for line in log.splitlines()
                   if any(marker in line for marker in forbidden)]
        if defects:
            raise SystemExit(name + ": unresolved build diagnostics:\n" + "\n".join(defects))
        built_pdf = build_dir / f"{name}.pdf"
        delivered_pdf = ROOT / built_pdf.name
        shutil.copyfile(built_pdf, delivered_pdf)
        pages = re.search(r"Output written on .*?\((\d+) pages?", log, re.S)
        report = {
            "source": source.name,
            "pdf": delivered_pdf.name,
            "pages": int(pages.group(1)) if pages else None,
            "bytes": delivered_pdf.stat().st_size,
            "sha256": hashlib.sha256(delivered_pdf.read_bytes()).hexdigest(),
            "passes": 3,
            "unresolved_references": False,
            "overfull_boxes": False,
        }
        reports.append(report)
        print(json.dumps(report, sort_keys=True))
    (build_dir / "build_report.json").write_text(json.dumps(reports, indent=2) + "\n")


if __name__ == "__main__":
    main()
