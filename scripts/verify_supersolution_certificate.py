#!/usr/bin/env python3
"""Reproduce the strict reserve and bounded-jump constants of the supersolution.

Requires gcc, OpenMP, GMP development headers, and the pinned public repository.
No network access or floating-point arithmetic is used in verification.  The
existing builder uses floating-point proposals; its output is checked by the
unchanged exact inequalities plus an exact minimum-slack recorder.
"""
import argparse
from decimal import Decimal, localcontext
from fractions import Fraction as Q
import hashlib
import json
import os
from pathlib import Path
import re
import struct
import subprocess
import difflib

from resolvent_supersolution import MotifSupersolution
from core_clock_kernel import CoreState

PINNED = {
    'cert_format.h': '7522710ab05fe79c6306711476a78f395476c66c720b10c0215d35fc2b48f701',
    'cert_build.c': 'beda03931551b6da514fd6f14218ec769ef73c982b2f483fa683fa0a3902b8c2',
    'cert_verify_gmp.c': '0bea8e43d1b01f84ec39326b9b7d5d2a8f40f64a9bd9ad6e156ae52d6c011af0',
}


def sha256(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def instrument(source):
    helper = '''static mpq_t local_min_vertex_slack;
static int local_slack_initialized=0;
static void record_vertex_slack(const mpq_t rhs,const mpq_t lhs) {
    mpq_t d; mpq_init(d); mpq_sub(d,rhs,lhs);
    if (!local_slack_initialized) {mpq_init(local_min_vertex_slack);mpq_set(local_min_vertex_slack,d);local_slack_initialized=1;}
    else if(mpq_cmp(d,local_min_vertex_slack)<0)mpq_set(local_min_vertex_slack,d);
    mpq_clear(d);
}

'''
    pos = source.index('/* Exact rational eval_g')
    source = source[:pos] + helper + source[pos:]
    start = source.index('/* ===== CHECK 1:')
    end = source.index('/* Precompute exact integer dLf_g_q', start)
    section = source[start:end]
    assert section.count('f_checks++;') == 5
    section = section.replace('f_checks++;',
                              'f_checks++; record_vertex_slack(rhs,lhs);')
    section += ('gmp_printf("EXACT_MIN_VERTEX_SLACK=%Qd\\n",'
                'local_min_vertex_slack); fflush(stdout);\n')
    return source[:start] + section + source[end:]


def maxima(path):
    with path.open('rb') as stream:
        header = struct.unpack('<Qiiiiqqiiiiiiiiii9ii', stream.read(120))
        assert header[0] == 0x494E564433563031
        assert header[1:4] == (1, 1133, 2000)
        assert header[5] == 10**10
        assert header[7:15] == (800, 150, 24, 12, 16, 8, 12, 6)
        scale = header[5]
        stream.seek(8 * (5 * 572 + 3 * 572 * 9), 1)
        answer = {}
        for name, count in [('F', 241904), ('G', 601**2),
                            ('V', 555 * 84 * 290),
                            ('H', 75 * 290 * 291 // 2)]:
            maximum = 0
            for offset in range(0, count, 100000):
                length = min(100000, count - offset)
                values = struct.unpack('<' + 'q' * length, stream.read(8 * length))
                maximum = max(maximum, max(values), -min(values))
            answer[name] = Q(maximum, scale)
        assert stream.read(1) == b''
    return answer


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', type=Path, required=True,
                    help='Checkout of uzay-eth/friend-tree-exponent at the pinned revision')
    ap.add_argument('--output', type=Path,
                    default=Path('supersolution_certificate_work'))
    ap.add_argument('--reuse-binary', action='store_true',
                    help='Reuse existing upper_5665.bin, but rerun the full exact verifier')
    args = ap.parse_args()
    source_dir = args.repo.resolve() / 'verify/motif-bracket'
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    for name, expected in PINNED.items():
        actual = sha256(source_dir / name)
        if actual != expected:
            raise SystemExit(f'Pinned source mismatch: {name}: {actual}')
    original = (source_dir / 'cert_verify_gmp.c').read_text()
    copied = instrument(original)
    verifier_source = out / 'verify_with_slack.c'
    verifier_source.write_text(copied)
    (out / 'verification_patch.diff').write_text(''.join(difflib.unified_diff(
        original.splitlines(True), copied.splitlines(True),
        fromfile='cert_verify_gmp.c', tofile='verify_with_slack.c')))
    binary = out / 'upper_5665.bin'
    env = os.environ.copy()
    env['OMP_NUM_THREADS'] = '4'
    if not args.reuse_binary:
        subprocess.run(['gcc', '-O3', '-Wall', '-Wextra', '-fopenmp',
                        str(source_dir / 'cert_build.c'), '-lm',
                        '-o', str(out / 'cert_build')], check=True)
        with (out / 'build.log').open('w') as log:
            subprocess.run([str(out / 'cert_build'), '1', '1133', '2000', str(binary)],
                           stdout=log, stderr=subprocess.STDOUT, env=env, check=True)
    subprocess.run(['gcc', '-O3', '-Wall', '-Wextra', '-fopenmp',
                    '-I' + str(source_dir), str(verifier_source), '-lgmp',
                    '-o', str(out / 'verify_with_slack')], check=True)
    log_path = out / 'verification_with_slack.log'
    with log_path.open('w') as log:
        subprocess.run([str(out / 'verify_with_slack'), str(binary)], stdout=log,
                       stderr=subprocess.STDOUT, env=env, check=True)
    log = log_path.read_text()
    assert '17329108 exact GMP inequality checks, 0 failures => VERIFIED OK' in log
    assert '37 tested, fails: 0' in log
    eta = Q(re.search(r'EXACT_MIN_VERTEX_SLACK=(\d+/\d+)', log).group(1))
    m = Q(re.search(r'min W\(u\)=(\d+/\d+)', log).group(1))
    assert eta > 0 and m > 0
    values = maxima(binary)
    F, G, V, H = (values[name] for name in ['F', 'G', 'V', 'H'])
    A = F + G + V + 15 * H
    J = 3 * F + 49 * G + 403 * V + 45 * H
    nu = Q(1133, 2000)
    nu_star = nu - eta / A
    assert nu_star == Q(5855965132053781, 10337140174500000)
    with MotifSupersolution(binary) as model:
        f1 = model.vertex((800, 1, 0))
        f2 = model.vertex((800, 2, 0))
        fnb = model.vertex((1, 0, 1))
        g_inf_nb = model.entry('g', model.inf * 601 + model.inner[1, 0, 1])
        parent_bud_limit = f2 - f1 + fnb + g_inf_nb
        chi_newborn = model.chi(CoreState((), (1,), (1,)))
        assert f1 == Q(261553463, 156250000)
        assert parent_bud_limit == Q(9479299189, 10000000000)
        assert chi_newborn == Q(4739578599, 5000000000)
    report = {name: str(value) for name, value in values.items()}
    report.update(c0=str(m), c1=str(A), J=str(J), eta=str(eta),
                  nu=str(nu), nu_star=str(nu_star), status='PASS',
                  original_exact_inequalities=17329108, original_tree_checks=37,
                  measured_vertex_rows=484138,
                  binary_sha256=sha256(binary),
                  parent_f1=str(f1), parent_f2=str(f2), f_newborn=str(fnb),
                  g_inf_newborn=str(g_inf_nb),
                  parent_bud_limit=str(parent_bud_limit),
                  chi_newborn=str(chi_newborn), boundary_remainder='0',
                  instrumented_source_sha256=sha256(verifier_source),
                  original_source_hashes=PINNED,
                  scope='Finite certificate and algebra; the jump-count proof is in the note.')
    with localcontext() as context:
        context.prec = 60
        report['nu_star_decimal'] = str(Decimal(nu_star.numerator) / Decimal(nu_star.denominator))
    (out / 'supersolution_certificate_verification.json').write_text(
        json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
