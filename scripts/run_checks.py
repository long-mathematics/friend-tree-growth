#!/usr/bin/env python3
"""Run the fast exact checks supporting the two manuscripts.

This does not run the full motif certificate, prove an analytic theorem, or
implement the general arbitrary-precision algorithm for the original exponent.
Use verify_bound.py for the full numerical upper-bound verification.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def run_json(script: str, arguments: list[str]) -> dict:
    result = subprocess.run([sys.executable, str(SCRIPTS / script), *arguments],
                            text=True, capture_output=True, check=True)
    report = json.loads(result.stdout)
    if report.get("status") != "PASS":
        raise RuntimeError(f"{script} did not report PASS")
    return report


def main() -> None:
    if not __debug__:
        raise SystemExit("Run the exact checkers without -O or PYTHONOPTIMIZE.")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path,
                        default=ROOT / "build" / "verification")
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    checks = [
        ("core_clock_kernel.py", ["--check"], "core_kernel_checks.json"),
        ("inert_growth_kernel.py", ["--check"], "inert_growth_checks.json"),
        ("verify_infection_kernel.py", [], "infection_kernel_checks.json"),
    ]
    for script, arguments, filename in checks:
        report = run_json(script, arguments)
        (args.output_dir / filename).write_text(json.dumps(report, indent=2) + "\n")
        print(f"PASS {script}", flush=True)
    run_json("check_van_root.py", ["--output", str(args.output_dir / "van_root_checks.json")])
    print("PASS check_van_root.py", flush=True)
    names = [row[0] for row in checks] + ["check_van_root.py"]
    metadata = {
        "status": "PASS",
        "python": platform.python_version(),
        "arithmetic": "Python fractions.Fraction; no floating-point proof decisions",
        "source_sha256": {name: hashlib.sha256((SCRIPTS / name).read_bytes()).hexdigest()
                          for name in names},
        "scope": "Finite kernel identities, bounds, and modified-model root brackets. "
                 "Analytic proofs are in the manuscripts. The general original-model "
                 "computability algorithm is not implemented by these scripts.",
    }
    (args.output_dir / "quick_check_run.json").write_text(json.dumps(metadata, indent=2) + "\n")


if __name__ == "__main__":
    main()
