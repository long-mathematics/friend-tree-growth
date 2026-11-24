#!/usr/bin/env python3
"""Exact whole-polynomial checks of original friend-tree insertion identities.

Polynomial dictionaries are over Q[x,z], not parameter samples. The proof for
arbitrary trees is in sections/transcendence/product_martingale_insertions.tex; this finite audit does
not prove a scalar closure or an arithmetic classification of the exponent.

The repository root defaults to the parent of the scripts directory.
"""
from collections import Counter, defaultdict
from fractions import Fraction as Q
from pathlib import Path
import argparse
import json
import sys


def add(*polys):
    out = defaultdict(Q)
    for poly in polys:
        for monomial, coefficient in poly.items():
            out[monomial] += coefficient
    return {m: c for m, c in out.items() if c}


def scale(poly, scalar):
    return {m: scalar * c for m, c in poly.items() if scalar * c}


def multiply(first, second):
    out = defaultdict(Q)
    for (x, z), a in first.items():
        for (xx, zz), b in second.items():
            out[x + xx, z + zz] += a * b
    return {m: c for m, c in out.items() if c}


def shift_x(poly, exponent):
    return {(x + exponent, z): c for (x, z), c in poly.items()}


def parity(poly, degree_parity):
    return {m: c for m, c in poly.items() if m[1] % 2 == degree_parity}


def evaluate(poly, x, z):
    return sum((c * x ** i * z ** j for (i, j), c in poly.items()), Q(0))


def product(degrees, signs):
    out = {(0, 0): Q(1)}
    for degree, sign in zip(degrees, signs):
        for j in range(1, degree):
            out = multiply(out, {(0, 0): Q(1), (0, 1): Q(sign, j)})
    return out


def signs_of(adjacency):
    signs = [None] * len(adjacency)
    signs[0] = 1
    pending = [0]
    while pending:
        vertex = pending.pop()
        for neighbor in adjacency[vertex]:
            if signs[neighbor] is None:
                signs[neighbor] = -signs[vertex]
                pending.append(neighbor)
    return signs


def main():
    if not __debug__:
        raise SystemExit("Run exact checks without -O or PYTHONOPTIMIZE.")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo-root', type=Path,
                        default=Path(__file__).resolve().parents[1])
    parser.add_argument('--max-population', type=int, default=9)
    parser.add_argument('--check', action='store_true',
                        help='run the exact audit (also the default)')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.max_population < 3:
        parser.error('--max-population must be at least 3')
    sys.path.insert(0, str(args.repo_root / 'scripts'))
    from full_tree_recurrence import (adjacency_from_code, attachment_transitions,
                                      canonical_tree)

    checks = Counter()

    def check(condition, category):
        if not condition:
            raise AssertionError(category)
        checks[category] += 1

    edge = canonical_tree(((1,), (0,)))
    distribution = {edge: Q(1)}
    rows = []
    previous = None
    x_minus_one = {(1, 0): Q(1), (0, 0): Q(-1)}
    for n in range(2, args.max_population + 1):
        totals = {name: {} for name in ('a', 'd', 'q', 'rhs_a', 'rhs_d', 'rhs_q')}
        check(sum(distribution.values(), Q(0)) == 1, 'distribution_normalization')
        for code, mass in distribution.items():
            adjacency = adjacency_from_code(code)
            degrees = [len(row) for row in adjacency]
            signs = signs_of(adjacency)
            rates = [sum((Q(1, degrees[u]) for u in row), Q(0))
                     for row in adjacency]
            cores = sum(d >= 2 for d in degrees)
            color_difference = sum(signs)
            lam = sum((rate for rate, d in zip(rates, degrees) if d == 1), Q(0))
            lam_signed = sum((sign * rate for sign, rate, d in zip(signs, rates, degrees)
                              if d == 1), Q(0))
            edge_weight = sum((Q(1, degrees[u] * degrees[v])
                               for u, neighbors in enumerate(adjacency)
                               for v in neighbors if u < v), Q(0))
            p = product(degrees, signs)
            core_poly = scale(p, Q(cores))
            color_poly = scale(p, Q(color_difference))
            fugacity_poly = shift_x(p, cores)
            leaf_poly = {(0, 0): lam, (0, 1): lam_signed}
            rhs_a = multiply(p, leaf_poly)
            rhs_d = multiply(p, {(0, 0): Q(color_difference), (0, 1): -2 * edge_weight})
            rhs_q = multiply(multiply(x_minus_one, fugacity_poly), leaf_poly)
            lp, lcore, lcolor, lfugacity = {}, {}, {}, {}
            for vertex, rate in enumerate(rates):
                child_degrees = degrees[:] + [1]
                child_degrees[vertex] += 1
                child_signs = signs[:] + [-signs[vertex]]
                child_cores = cores + (degrees[vertex] == 1)
                child_color_difference = color_difference - signs[vertex]
                child_p = product(child_degrees, child_signs)
                check(child_p == multiply(p, {(0, 0): Q(1),
                                              (0, 1): Q(signs[vertex], degrees[vertex])}),
                      'entire_polynomial_birth_identity')
                lp = add(lp, scale(add(child_p, scale(p, Q(-1))), rate))
                lcore = add(lcore, scale(add(scale(child_p, Q(child_cores)),
                                             scale(core_poly, Q(-1))), rate))
                lcolor = add(lcolor, scale(add(scale(child_p, Q(child_color_difference)),
                                               scale(color_poly, Q(-1))), rate))
                lfugacity = add(lfugacity,
                                scale(add(shift_x(child_p, child_cores),
                                          scale(fugacity_poly, Q(-1))), rate))
            check(lp == {}, 'entire_polynomial_product_harmonicity')
            check(lcore == rhs_a, 'entire_polynomial_core_insertion')
            check(lcolor == rhs_d, 'entire_polynomial_color_insertion')
            check(lfugacity == rhs_q, 'entire_bivariate_fugacity_insertion')

            # Conditional on an uncolored tree, its two colorings have equal
            # probability, by swapping the two initial edge labels. For scalar
            # observables keep the even part in z; D changes sign too, so the
            # D-inserted observables use the odd part instead.
            for name, poly, sign_parity in (
                    ('a', core_poly, 0), ('d', color_poly, 1), ('q', fugacity_poly, 0),
                    ('rhs_a', rhs_a, 0), ('rhs_d', rhs_d, 1), ('rhs_q', rhs_q, 0)):
                totals[name] = add(totals[name], scale(parity(poly, sign_parity), mass))

        if previous is not None:
            for name in ('a', 'd', 'q'):
                check(scale(add(totals[name], scale(previous[name], Q(-1))), Q(n-1))
                      == previous['rhs_' + name],
                      'entire_polynomial_population_' + name)
        if n >= 3:
            check(evaluate(totals['a'], Q(1), Q(1)) == 1,
                  'core_insertion_at_star_boundary')
            check(evaluate(totals['d'], Q(1), Q(1)) == 2-n,
                  'color_insertion_at_star_boundary')
        rows.append({'population': n, 'unlabelled_trees': len(distribution),
                     'a_n_coefficients_in_z': {
                         str(z): str(c) for (x, z), c in sorted(totals['a'].items())}})
        previous = totals
        if n < args.max_population:
            following = defaultdict(Q)
            for code, mass in distribution.items():
                for child, probability in attachment_transitions(code):
                    following[child] += mass * probability
            distribution = dict(following)

    report = {
        'status': 'PASS', 'exact_checks': sum(checks.values()),
        'checks_by_category': dict(checks), 'population_rows': rows,
        'scope': 'Finite exact identities over Q[x,z] for the original free friend tree. '
                 'No scalar closure, irrationality, or all-complex-time integrability is asserted.'
    }
    serialized = json.dumps(report, indent=2) + '\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized, encoding='utf-8')
    print(serialized, end='')


if __name__ == '__main__':
    main()
