#!/usr/bin/env python3
"""Exact finite audit of the signed harmonic/product martingale.

This checker uses the repository's exact tree enumerators, but forms
the product polynomials, the signed harmonic sums, and the free-tree birth
operator independently. It checks entire rational polynomials, not samples
of the parameter. Passing is a finite audit, not an irrationality proof.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction as F
from math import comb
from pathlib import Path
import json
import sys


def clean(p):
    p = list(p)
    while len(p) > 1 and not p[-1]:
        p.pop()
    return tuple(p)


def add(p, q):
    r = [F()] * max(len(p), len(q))
    for i, a in enumerate(p):
        r[i] += a
    for i, a in enumerate(q):
        r[i] += a
    return clean(r)


def scale(p, x):
    return clean(a * x for a in p)


def linear(p, x):
    return add(p, (F(),) + scale(p, x))


def value(p, x):
    y = F()
    for a in reversed(p):
        y = y * x + a
    return y


def degrees_product(degrees, signs):
    p = (F(1),)
    for d, sign in zip(degrees, signs):
        for j in range(1, d):
            p = linear(p, F(sign, j))
    return p


def harmonic_observables(degrees, signs):
    j = sum((sign * sum((F(1, k) for k in range(1, d)), F())
             for d, sign in zip(degrees, signs)), F())
    s2 = sum((sum((F(1, k * k) for k in range(1, d)), F())
              for d in degrees), F())
    c = sum(d >= 2 for d in degrees)
    return j, s2, c


def bipartition(adjacency):
    signs = [0] * len(adjacency)
    signs[0] = 1
    pending = [0]
    for u in pending:
        for v in adjacency[u]:
            if not signs[v]:
                signs[v] = -signs[u]
                pending.append(v)
            assert signs[v] == -signs[u]
    assert all(signs)
    return tuple(signs)


def append_leaf(adjacency, target):
    n = len(adjacency)
    rows = [list(row) for row in adjacency]
    rows[target].append(n)
    rows.append([target])
    return tuple(tuple(row) for row in rows)


def integer_product(degrees, signs, k):
    result = 1
    parity = 0
    for d, sign in zip(degrees, signs):
        if sign == 1:
            result *= comb(k + d - 1, d - 1)
        else:
            result *= comb(k - 1, d - 1) if d <= k else 0
            parity += d - 1
    return (-1) ** parity * result


def run(repo, maximum):
    sys.path.insert(0, str(repo / "scripts"))
    from full_tree_recurrence import (
        adjacency_from_code, attachment_transitions, canonical_tree, star,
    )
    from inert_growth_kernel import INERT_INITIAL, core_depths
    from primitive_population_tools import proper_channels

    checks = Counter()

    def check(condition, name):
        if not condition:
            raise AssertionError(name)
        checks[name] += 1

    def audit_state(degrees, signs):
        p = degrees_product(degrees, signs)
        j, s2, c = harmonic_observables(degrees, signs)
        check((p[1] if len(p) > 1 else 0) == j,
              "first_product_coefficient")
        check((p[2] if len(p) > 2 else 0) == (j * j - s2) / 2,
              "second_product_coefficient")
        # Exact rational upper bound 5/3 > zeta(2), adequate as a finite audit.
        # The analytic proof in the accompanying note uses zeta(2) itself.
        check(c <= s2 <= F(5, 3) * c, "quadratic_variation_core_comparison")
        for k in (1, 2, 3, 4):
            check(value(p, k) == integer_product(degrees, signs, k),
                  "integer_binomial_specialization")
        return p, j, s2, c

    free_rows = []
    free_dist = {canonical_tree(((1,), (0,))): F(1)}
    for n in range(2, maximum + 1):
        expectation = (F(),)
        j2_mean = s2_mean = core_mean = F()
        for code, mass in free_dist.items():
            adjacency = adjacency_from_code(code)
            degrees = tuple(map(len, adjacency))
            signs = bipartition(adjacency)
            p, j, s2, c = audit_state(degrees, signs)
            # The free initial edge is symmetric under interchanging colors.
            # Conditional on an uncolored tree, the two colorings have equal
            # law; average them before using the uncolored distribution.
            even_p = tuple(a if i % 2 == 0 else F() for i, a in enumerate(p))
            expectation = add(expectation, scale(even_p, mass))
            j2_mean += mass * j * j
            s2_mean += mass * s2
            core_mean += mass * c
            generator = (F(),)
            j_drift = quadratic_drift = F()
            total_rate = F()
            for target, neighbors in enumerate(adjacency):
                rate = sum((F(1, degrees[source]) for source in neighbors), F())
                child = append_leaf(adjacency, target)
                child_degrees = tuple(map(len, child))
                child_signs = signs + (-signs[target],)
                child_p = degrees_product(child_degrees, child_signs)
                child_j, child_s2, _ = harmonic_observables(child_degrees, child_signs)
                check(child_p == linear(p, F(signs[target], degrees[target])),
                      "free_birth_product_ratio")
                check(child_s2 - s2 == (child_j - j) ** 2,
                      "pathwise_quadratic_variation_increment")
                generator = add(generator, scale(add(child_p, scale(p, -1)), rate))
                j_drift += rate * (child_j - j)
                quadratic_drift += rate * (child_j**2 - child_s2 - j*j + s2)
                total_rate += rate
            check(generator == (F(),), "free_polynomial_generator_zero")
            check(j_drift == 0 and quadratic_drift == 0,
                  "free_harmonic_and_quadratic_generator_zero")
            check(total_rate == n, "free_rate_normalization")
            check(sum((F(signs[w], degrees[w]) *
                       sum((F(1, degrees[u]) for u in adjacency[w]), F())
                       for w in range(n)), F()) == 0,
                  "free_doob_rate_correction_zero")
        check(expectation == (F(1),), "free_expected_product_polynomial_one")
        check(j2_mean == s2_mean, "free_exact_variance_identity")
        if n >= 3:
            check(free_dist.get(star(n), F()) == F(2, n - 1),
                  "free_two_color_star_probability")
        free_rows.append({"population": n, "states": len(free_dist),
                          "mean_cores": str(core_mean), "mean_J_squared": str(j2_mean)})
        if n < maximum:
            following = defaultdict(F)
            for code, mass in free_dist.items():
                for child, probability in attachment_transitions(code):
                    following[child] += mass * probability
            free_dist = dict(following)

    inert_rows = []
    inert_dist = {INERT_INITIAL: F(1)}
    for n in range(2, maximum + 1):
        expectation = (F(),)
        j_mean = j2_mean = s2_mean = core_mean = star_probability = F()
        for state, mass in inert_dist.items():
            degrees = state.degrees()
            signs = tuple((-1) ** depth for depth in core_depths(state))
            p, j, s2, c = audit_state(degrees, signs)
            expectation = add(expectation, scale(p, mass))
            j_mean += mass * j
            j2_mean += mass * j * j
            s2_mean += mass * s2
            core_mean += mass * c
            if state.k == 1:
                star_probability += mass
                check(value(p, 1) == n, "inert_star_product_value")
            else:
                check(value(p, 1) == 0, "inert_nonstar_product_zero")
            generator = (F(),)
            j_drift = quadratic_drift = F()
            total_rate = F()
            for child, _depth, rate in proper_channels(state):
                child_degrees = child.degrees()
                child_signs = tuple((-1) ** depth for depth in core_depths(child))
                child_p = degrees_product(child_degrees, child_signs)
                child_j, child_s2, _ = harmonic_observables(child_degrees, child_signs)
                generator = add(generator, scale(add(child_p, scale(p, -1)), rate))
                j_drift += rate * (child_j - j)
                quadratic_drift += rate * (child_j**2 - child_s2 - j*j + s2)
                total_rate += rate
            check(generator == (F(),), "inert_polynomial_generator_zero")
            check(j_drift == 0 and quadratic_drift == 0,
                  "inert_harmonic_and_quadratic_generator_zero")
            check(total_rate == n - F(1, degrees[0]), "inert_proper_rate_normalization")
        check(expectation == (F(1), F(1)), "inert_expected_product_one_plus_z")
        check(j_mean == 1, "inert_harmonic_mean_one")
        check(j2_mean == s2_mean, "inert_exact_variance_identity")
        check(star_probability == F(2, n), "inert_root_star_probability")
        inert_rows.append({"population": n, "states": len(inert_dist),
                           "mean_cores": str(core_mean), "mean_J_squared": str(j2_mean)})
        if n < maximum:
            following = defaultdict(F)
            for state, mass in inert_dist.items():
                rate = n - F(1, state.degrees()[0])
                for child, _depth, channel_rate in proper_channels(state):
                    following[child] += mass * channel_rate / rate
            inert_dist = dict(following)

    return {"status": "PASS", "exact_checks": sum(checks.values()), "arithmetic": "exact Fraction polynomial arithmetic",
            "maximum_population": maximum, "checks": dict(sorted(checks.items())),
            "free": free_rows, "inert": inert_rows,
            "scope": "Finite checks of the proved identities; no irrationality assertion."}


def main():
    if not __debug__:
        raise SystemExit("Run exact checks without -O or PYTHONOPTIMIZE.")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="run the exact audit (the default)")
    parser.add_argument("--repo", type=Path,
                        default=Path(__file__).resolve().parents[1])
    parser.add_argument("--maximum-population", type=int, default=10)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.maximum_population < 2:
        parser.error("--maximum-population must be at least 2")
    report = run(args.repo.resolve(), args.maximum_population)
    encoded = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded)
    print(encoded)


if __name__ == "__main__":
    main()
