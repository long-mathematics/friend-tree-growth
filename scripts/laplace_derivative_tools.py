#!/usr/bin/env python3
"""Exact positive beta-derivative coefficients and their elementary tails.

These enclose fixed derivatives of the full-tree Laplace transform when
fed exact finite a_n=E C_n. They do not enclose mu: the derivative-order
ratio limit has no proved effective error rate.
"""

import argparse
from fractions import Fraction as Q
import json
from pathlib import Path


def homogeneous(values, order):
    """H_0,...,H_order for a finite tuple of positive rational variables."""
    result = [Q(1)] + [Q(0)] * order
    for value in values:
        value = Q(value)
        for m in range(1, order + 1):
            result[m] += value * result[m - 1]
    return tuple(result)


def beta_weight(discount, population):
    s = Q(discount)
    if population < 2 or s <= 0:
        raise ValueError("Require n>=2 and s>0.")
    value = Q(1, 1) / (s + 2)
    for n in range(2, population):
        value *= Q(n) / (s + n + 1)
    return value


def beta_derivative_weights(discount, population, order):
    s = Q(discount)
    if order < 0:
        raise ValueError("The derivative order must be nonnegative.")
    base = beta_weight(s, population)
    values = [1 / (s + j) for j in range(2, population + 1)]
    return tuple(base * value for value in homogeneous(values, order))


def derivative_tail(discount, cutoff, order):
    """Upper bounds on each B_m tail, 0<=m<=order, using a_n<=n-2."""
    s = Q(discount)
    if s <= 1 or cutoff < 2 or order < 0:
        raise ValueError("Require s>1, cutoff>=2, and order>=0.")
    values = [1 / (s + j) for j in range(2, cutoff + 1)]
    first = homogeneous([*values, 1 / (s - 1)], order)
    second = homogeneous([*values, 1 / s, 1 / (s - 1)], order)
    prefactor = cutoff * beta_weight(s, cutoff)
    return tuple(prefactor * ((cutoff - 1) * first[m] / (s - 1)
                             + 2 * second[m] / (s * (s - 1)))
                 for m in range(order + 1))


def enclose_derivatives(coefficients, discount, order):
    """Input exact actual a_2,...,a_N; return intervals for B_0,...,B_order.

    The caller must supply the correct full-tree coefficients. The basic
    size bounds checked here do not verify that mathematical provenance.
    """
    coefficients = tuple(Q(value) for value in coefficients)
    if not coefficients:
        raise ValueError("At least a_2 is required.")
    if any(not 0 <= value <= n - 2
           for n, value in enumerate(coefficients, start=2)):
        raise ValueError("Coefficients violate the required 0<=a_n<=n-2 bound.")
    lower = [Q(0)] * (order + 1)
    for n, coefficient in enumerate(coefficients, start=2):
        row = beta_derivative_weights(discount, n, order)
        for m in range(order + 1):
            lower[m] += coefficient * row[m]
    tail = derivative_tail(discount, len(coefficients) + 1, order)
    return tuple((lower[m], lower[m] + tail[m]) for m in range(order + 1))


def check():
    checks = 0
    order = 8
    discounts = (Q(3, 2), Q(2), Q(5, 2), Q(3), Q(5))
    for s in discounts:
        tail = derivative_tail(s, 2, order)
        for m, value in enumerate(tail):
            assert value == 2 * ((s - 1) ** (-m - 1) - s ** (-m - 1))
            checks += 1
        for n in range(2, 30):
            now = derivative_tail(s, n, order)
            following = derivative_tail(s, n + 1, order)
            point = beta_derivative_weights(s, n + 1, order)
            for m in range(order + 1):
                assert now[m] > following[m] > 0
                assert now[m] - following[m] == (n - 1) * point[m]
                checks += 2
            values = [1 / (s + j) for j in range(2, n + 1)]
            h = homogeneous(values, order)
            for m in range(1, order + 1):
                powers = [sum((x ** k for x in values), Q(0))
                          for k in range(1, m + 1)]
                assert m * h[m] == sum((powers[k - 1] * h[m - k]
                                       for k in range(1, m + 1)), Q(0))
                checks += 1
    initial = (Q(0), Q(1), Q(4, 3), Q(19, 12), Q(647, 360))
    intervals = enclose_derivatives(initial, Q(2), 3)
    assert all(0 < lower < upper for lower, upper in intervals)
    checks += 1
    return {
        "status": "PASS", "exact_checks": checks,
        "scope": "Positive beta-derivative weights and fixed-order tails only; no mu bracket or derivative-order convergence rate.",
        "example": {
            "discount": "2", "population_cutoff": 6,
            "B_m_intervals": [[str(a), str(b)] for a, b in intervals],
        },
    }


def main():
    if not __debug__:
        raise SystemExit("Run exact checks without -O or PYTHONOPTIMIZE.")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="run the exact default checks (also the default)")
    parser.add_argument("--output", type=Path,
                        help="optional destination for the complete JSON report")
    args = parser.parse_args()
    serialized = json.dumps(check(), indent=2) + "\n"
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized, encoding="utf-8")
    print(serialized, end="")


if __name__ == "__main__":
    main()
