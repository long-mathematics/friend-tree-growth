#!/usr/bin/env python3
"""Finite exact checks of a comparison process, not of irrationality.

The analytic proof is in sections/transcendence/bipartite_product_martingale.tex.  The original
friend-tree module is only used to enumerate every free tree through size 9.
"""
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
import json
import sys

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / 'scripts'))
from full_tree_recurrence import adjacency_from_code, attach_leaf, canonical_tree


def signs_of(adj):
    signs = [None] * len(adj)
    signs[0] = 1
    pending = [0]
    while pending:
        v = pending.pop()
        for w in adj[v]:
            if signs[w] is None:
                signs[w] = -signs[v]
                pending.append(w)
    return signs


def product(degrees, signs, z):
    value = Q(1)
    for degree, sign in zip(degrees, signs):
        for j in range(1, degree):
            value *= 1 + Q(sign) * z / j
    return value


def main():
    if not __debug__:
        raise SystemExit("Run exact checks without -O or PYTHONOPTIMIZE.")
    checks = Counter()
    trees = {canonical_tree(((1,), (0,)))}
    rows = []
    for n in range(2, 10):
        rows.append({'population': n, 'trees': len(trees)})
        following = set()
        for code in trees:
            adj = adjacency_from_code(code)
            degrees = [len(row) for row in adj]
            signs = signs_of(adj)
            counts = Counter(signs)
            rates = [Q(counts[-s] * d, n-1) for d, s in zip(degrees, signs)]
            assert all(x > 0 for x in rates)
            assert sum(rates) == n
            checks['positive_normalized_rates'] += 1
            for s in (-1, 1):
                assert sum(rate for rate, sign in zip(rates, signs) if sign == s) == counts[-s]
                checks['exact_color_yule_rate'] += 1
            assert sum(Q(s) * rate / d for s, rate, d in zip(signs, rates, degrees)) == 0
            checks['product_balance'] += 1
            c = sum(d >= 2 for d in degrees)
            if n >= 3:
                promotion = sum(rate for rate, d in zip(rates, degrees) if d == 1)
                assert promotion >= Q(min(counts.values()) * (n-c), n-1)
                checks['promotion_lower_bound'] += 1
            for z in (Q(1), Q(2), Q(-2), Q(13, 23)):
                p = product(degrees, signs, z)
                drift = Q(0)
                for v, rate in enumerate(rates):
                    new_degrees = degrees[:] + [1]
                    new_degrees[v] += 1
                    new_signs = signs[:] + [-signs[v]]
                    drift += rate * (product(new_degrees, new_signs, z) - p)
                assert drift == 0
                checks['direct_product_martingale_drift'] += 1
            if n < 9:
                following.update(attach_leaf(code, v) for v in range(n))
        trees = following
    for n in range(2, 101):
        em = sum((Q(min(k, n-k), n-1) for k in range(1, n)), Q(0))
        assert em >= Q(n, 4)
        checks['uniform_color_minimum_bound'] += 1
    result = {
        'status': 'PASS',
        'exact_checks': sum(checks.values()),
        'checks_by_category': dict(checks),
        'enumerated_trees': rows,
        'scope': 'Comparison process only. Original friend-tree irrationality remains open.'
    }
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
