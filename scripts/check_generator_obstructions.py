#!/usr/bin/env python3
"""Exact finite audit for generator pole examples and a Hankel obstruction.

This finite program does not prove the all-orders star-pole theorem or
classify the arithmetic nature of the original exponent.
"""
import argparse
from fractions import Fraction as Q
from functools import lru_cache
import json
from pathlib import Path
from full_tree_recurrence import (attachment_transitions, canonical_tree,
                                  observables, star)


@lru_cache(maxsize=None)
def power(order, code):
    values = observables(code)
    if order == 0:
        return Q(values.cores)
    return values.population * (
        sum((p * power(order - 1, child)
             for child, p in attachment_transitions(code)), Q(0))
        - power(order - 1, code))


def determinant(rows):
    a = [list(row) for row in rows]
    result = Q(1)
    for col in range(len(a)):
        pivot = next((j for j in range(col, len(a)) if a[j][col]), None)
        if pivot is None:
            return Q(0)
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
            result = -result
        diagonal = a[col][col]
        result *= diagonal
        for row in range(col + 1, len(a)):
            factor = a[row][col] / diagonal
            for j in range(col + 1, len(a)):
                a[row][j] -= factor * a[col][j]
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true',
                        help='run the exact audit (also the default)')
    parser.add_argument('--output', type=Path,
                        help='optional destination for the JSON report')
    args = parser.parse_args()
    checks = 0
    for d in range(2, 11):
        tree = star(d + 1)
        assert power(2, tree) == Q(1, 2) - Q(1, d)
        assert power(3, tree) == Q(d**3 + 11*d*d + d + 6, 6*d*d*(d+1))
        checks += 2
    edge = canonical_tree(((1,), (0,)))
    expected = [Q(2), Q(-2), Q(4), Q(-19, 3), Q(133, 12),
                Q(-8189, 432), Q(70753, 2160)]
    derivatives = [power(r, edge) for r in range(1, 8)]
    assert derivatives == expected
    checks += 7
    moments = [x / 2 for x in derivatives]
    hankel = determinant([[moments[i+j] for j in range(4)] for i in range(4)])
    assert hankel == Q(-43427, 3732480)
    checks += 1
    q = [-437, 19, 969, 468]
    norm = sum((q[i]*q[j]*moments[i+j] for i in range(4) for j in range(4)), Q(0))
    assert norm == Q(-564551, 40)
    checks += 1
    partial_star_contribution = 48 * power(2, star(6))
    assert partial_star_contribution == Q(72, 5)
    assert derivatives[5].denominator % 5 != 0
    checks += 2
    report = {
        'status': 'PASS', 'exact_checks': checks,
        'edge_generator_derivatives': [str(x) for x in derivatives],
        'hankel_determinant_4': str(hankel),
        'negative_square_polynomial_ascending': q,
        'negative_square_value': str(norm),
        'cancellation_example': {
            'four_birth_star_prefix_contribution_to_c6': str(partial_star_contribution),
            'complete_c6': str(derivatives[5]),
            'cancelled_prime': 5,
        },
        'scope': 'Finite exact checks. The all-orders pole theorem is analytic; no irrationality or transcendence assertion follows.'
    }
    serialized = json.dumps(report, indent=2) + '\n'
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized, encoding='utf-8')
    print(serialized, end='')


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run without -O or PYTHONOPTIMIZE.')
    main()
