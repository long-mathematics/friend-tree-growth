#!/usr/bin/env python3
"""Reproduce the corrected original-model motif certificate from pinned inputs.

The upstream builder proposes a binary using floating-point arithmetic; all
decisive certificate inequalities and the correction are checked exactly.
This runner never calls the optional floating-point correction search.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
import platform
from pathlib import Path
import shutil
import subprocess
import sys

from fetch_upstream import ROOT, digest, prepare_source

SCRIPTS = ROOT / "scripts"
BETA = "2832242711/5000000000"
TAU = "5294970481/100000000000000"
ZETA = "199752266575452391/1200500000000000000000000000"


def run(script: str, arguments: list[str], log: Path) -> None:
    try:
        with log.open("w") as stream:
            subprocess.run([sys.executable, str(SCRIPTS / script), *arguments],
                           stdout=stream, stderr=subprocess.STDOUT, check=True)
    except subprocess.CalledProcessError:
        print(f"FAIL {script}; diagnostic log: {log}", file=sys.stderr, flush=True)
        print(log.read_text(errors="replace")[-12000:], file=sys.stderr, flush=True)
        raise
    print(f"PASS {script}", flush=True)


def main() -> None:
    if not __debug__:
        raise SystemExit("Run the exact checkers without -O or PYTHONOPTIMIZE.")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", type=Path, default=ROOT / ".cache" / "upstream")
    parser.add_argument("--work-dir", type=Path, default=ROOT / ".cache" / "motif-certificate")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "build" / "verification")
    parser.add_argument("--offline", action="store_true",
                        help="Use previously downloaded, hash-verified sources.")
    parser.add_argument("--reuse-binary", action="store_true",
                        help="Reuse the pinned binary but rerun every exact check.")
    args = parser.parse_args()
    args.source_dir = args.source_dir.resolve()
    args.work_dir = args.work_dir.resolve()
    args.output_dir = args.output_dir.resolve()
    args.work_dir.mkdir(parents=True, exist_ok=True)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    manifest = prepare_source(args.source_dir, download=not args.offline)
    print("PASS pinned source hashes", flush=True)
    original_args = ["--repo", str(args.source_dir), "--output", str(args.work_dir)]
    if args.reuse_binary:
        binary = args.work_dir / "upper_5665.bin"
        if digest(binary) != manifest["certificate"]["sha256"]:
            raise ValueError("The reused certificate does not match the pinned binary.")
        original_args.append("--reuse-binary")
    diagnostics = [
        ("verification_with_slack.log", "original_certificate_verification.log"),
        ("verification_patch.diff", "verification_patch.diff"),
    ]
    if not args.reuse_binary:
        diagnostics.append(("build.log", "certificate_build.log"))
    for name, _ in diagnostics:
        (args.work_dir / name).unlink(missing_ok=True)
    try:
        run("verify_supersolution_certificate.py", original_args,
            args.output_dir / "original_certificate_runner.log")
    finally:
        # Preserve the child process diagnostics even if it fails before the
        # final JSON report, so CI artifacts show the underlying cause.
        for name, destination in diagnostics:
            source = args.work_dir / name
            if source.exists() and source != args.output_dir / destination:
                shutil.copyfile(source, args.output_dir / destination)
    binary = args.work_dir / "upper_5665.bin"
    if digest(binary) != manifest["certificate"]["sha256"]:
        raise ValueError("The rebuilt certificate differs from the pinned binary.")
    shutil.copyfile(args.work_dir / "supersolution_certificate_verification.json",
                    args.output_dir / "original_certificate_verification.json")
    correction_path = args.output_dir / "corrected_certificate_checks.json"
    run("continuation_certificate_bounds.py", [
        "--certificate", str(binary), "--perturb-core", "--verify-beta", BETA,
        "--verify-correction", TAU, "--output", str(correction_path)],
        args.output_dir / "corrected_certificate_runner.log")
    correction = json.loads(correction_path.read_text())
    result = correction["constant_core_correction"]
    if not (correction["status"] == "PASS" and result["verified_beta"] == BETA
            and result["correction_t"] == TAU and result["minimum_exact_margin"] == ZETA
            and result["exact_rows_verified"] == 484138):
        raise ValueError("Corrected certificate did not reproduce the stated constants.")
    for script, name, extra in [
        ("verify_supersolution_evaluator.py", "supersolution_evaluator_checks.json",
         ["--repo", str(args.source_dir)]),
        ("continuation_verify_evaluator.py", "corrected_evaluator_checks.json", []),
    ]:
        run(script, ["--certificate", str(binary), "--output", str(args.output_dir / name), *extra],
            args.output_dir / (name.removesuffix(".json") + ".log"))
    sources = ["verify_supersolution_certificate.py", "continuation_certificate_bounds.py",
               "verify_supersolution_evaluator.py", "continuation_verify_evaluator.py",
               "resolvent_supersolution.py", "continuation_supersolution.py",
               "core_clock_kernel.py", "fetch_upstream.py", "verify_bound.py"]
    gain = Fraction(1133, 2000) - Fraction(BETA)
    metadata = {
        "status": "PASS", "python": platform.python_version(),
        "upstream_commit": manifest["commit"], "reused_binary": args.reuse_binary,
        "binary_sha256": digest(binary), "beta": BETA, "tau": TAU, "zeta": ZETA,
        "improvement_over_1133_2000": str(gain),
        "original_exact_GMP_inequalities": 17329108, "modified_vertex_rows": 484138,
        "source_sha256": {name: hashlib.sha256((SCRIPTS / name).read_bytes()).hexdigest()
                          for name in sources},
        "scope": "Full rerun of the upstream exact checker with instrumentation that "
                 "only records vertex slack, followed by the exact corrected-row check. "
                 "This is not a second independent implementation of the full certificate. "
                 "The all-degree tail argument and drift-to-growth implication are analytic.",
    }
    (args.output_dir / "bound_verification_run.json").write_text(json.dumps(metadata, indent=2) + "\n")
    print(f"VERIFIED mu <= {BETA} = 0.5664485422", flush=True)


if __name__ == "__main__":
    main()
