#!/usr/bin/env python3
"""Certified rational enclosures for modified VAN exponents.

This checks finite root brackets using Fraction arithmetic.  The CMJ bridge
and the irrationality theorem are mathematical proofs in the accompanying
note, not consequences of the numerical checks.  Standard library only.
"""
from fractions import Fraction as Q
from math import factorial, gcd, lcm
from decimal import Decimal, localcontext
from pathlib import Path
import argparse
import json


def exp_minus_one_bounds(n=80):
    if n % 2:
        raise ValueError("n must be even")
    upper = sum((Q((-1) ** j, factorial(j)) for j in range(n + 1)), Q(0))
    return upper - Q(1, factorial(n + 1)), upper


def F_bounds(s, n=80):
    """Bounds integral_0^1 x^s exp(x-1) dx for rational s in [0,1]."""
    if not 0 <= s <= 1:
        raise ValueError("this tail estimate uses s in [0,1]")
    lower_e, upper_e = exp_minus_one_bounds(n)
    partial = sum((Q(1, factorial(j)) / (s + j + 1)
                   for j in range(n + 1)), Q(0))
    tail = Q(2, (n + 2) * factorial(n + 1))
    return lower_e * partial, upper_e * partial + tail


def m_of_F(s, omega, f):
    return (s + omega) * (1 - f) / (s * (s + omega - omega * f))


def m_bounds(s, omega, n=80):
    lo, hi = F_bounds(s, n)
    # m is strictly decreasing in F at fixed positive s and omega >= 0.
    return m_of_F(s, omega, hi), m_of_F(s, omega, lo)


def decimal(q, precision=45):
    with localcontext() as ctx:
        ctx.prec = precision
        return str(Decimal(q.numerator) / Decimal(q.denominator))


def bracket(omega, steps=90):
    lo, hi = Q(0), Q(1)
    terms = 80
    for _ in range(steps):
        mid = (lo + hi) / 2
        while True:
            lower, upper = m_bounds(mid, omega, terms)
            if lower > 1:
                lo = mid
                break
            if upper < 1:
                hi = mid
                break
            terms *= 2
    lower_left, _ = m_bounds(lo, omega, terms)
    _, upper_right = m_bounds(hi, omega, terms)
    assert lower_left > 1 and upper_right < 1
    return {"omega": str(omega), "left": str(lo), "right": str(hi),
            "left_decimal": decimal(lo), "right_decimal": decimal(hi),
            "width": str(hi-lo), "series_terms": terms+1,
            "certified_m_left_lower_minus_one": str(lower_left-1),
            "certified_one_minus_m_right_upper": str(1-upper_right)}


def coefficient_denominator_checks():
    checks = 0
    for p in range(1, 10):
        for q in range(1, 10):
            if gcd(p, q) != 1:
                continue
            a = Q(1)
            common = 1
            for n in range(1, 21):
                a *= Q(q*n, p+q*n)
                common = lcm(common, a.denominator)
                proposed = lcm(*range(1, p+q*n+1))
                assert proposed % common == 0
                assert 0 < a <= 1
                checks += 1
    return checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("van_root_checks.json"))
    args = parser.parse_args()
    report = {"status": "PASS", "arithmetic": "Python fractions.Fraction",
              "scope": "Certified finite root brackets and coefficient checks; not a numerical proof of irrationality.",
              "models": {name: bracket(Q(omega)) for name, omega in
                         [("PAN", 0), ("DAN", 1), ("VAN_2", 2)]},
              "finite_E_coefficient_checks": coefficient_denominator_checks()}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({"status": report["status"],
                      "brackets": {name: [r["left_decimal"], r["right_decimal"]]
                                   for name, r in report["models"].items()},
                      "finite_E_coefficient_checks": report["finite_E_coefficient_checks"],
                      "output": str(args.output)}, indent=2))


if __name__ == "__main__":
    main()
