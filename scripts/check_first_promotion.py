#!/usr/bin/env python3
"""Exact finite checks for the inert newborn's first-promotion transform.

All pass/fail decisions use integers or fractions.Fraction.  Decimal output
is rounded outwards.  Floating point occurs only in explicitly labelled
denominator-growth diagnostics; those diagnostics do not prove asymptotics.

Run with no arguments (or --check) to write a JSON report in build/verification/.
Use --output PATH to choose a different report destination.
This verifies finite identities and inequalities, not their infinite-tail
proofs, nor any irrationality or transcendence assertion.
"""

from __future__ import annotations

import argparse
from collections import Counter
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR, localcontext
from fractions import Fraction
from math import isqrt, log
from pathlib import Path
import json


Q = Fraction
ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "build" / "verification" / "first_promotion_checks.json"


def require(condition: bool, description: str) -> None:
    if not condition:
        raise AssertionError(description)


def weights(s: Q, n_max: int) -> list[Q]:
    result = [Q(1)]
    for j in range(1, n_max + 1):
        result.append(result[-1] * j * j / (j * j + (s + 2) * j + s))
    return result


def null_eliminated_channels(s: Q, j: int) -> tuple[Q, Q]:
    """Sum arbitrarily many discounted null rings in the original CTMC."""
    leaf_rate = Q(j)
    promotion_rate = Q(j, j + 1)
    null_rate = Q(1, j + 1)
    total_rate = leaf_rate + promotion_rate + null_rate
    leaf_once = leaf_rate / (s + total_rate)
    promotion_once = promotion_rate / (s + total_rate)
    null_once = null_rate / (s + total_rate)
    return leaf_once / (1 - null_once), promotion_once / (1 - null_once)


def killed_backward_transform(s: Q, last_state: int) -> Q:
    """Original backward equations, killing at the next leaf birth."""
    continuation = Q(0)
    for j in range(last_state, 0, -1):
        leaf_rate = Q(j)
        promotion_rate = Q(j, j + 1)
        null_rate = Q(1, j + 1)
        total_rate = leaf_rate + promotion_rate + null_rate
        continuation = (promotion_rate + leaf_rate * continuation) / (
            s + total_rate - null_rate
        )
    return continuation


def reduction_constants(s: Q) -> tuple[Q, Q, Q]:
    return (
        1 / (s + 1),
        (s * s + 3 * s + 4) / ((s + 1) * (s + 2)),
        s * s / ((s + 1) * (s + 2)),
    )


def tail_constants(s: Q, start: int) -> tuple[Q, Q, Q, Q, Q]:
    a = s + 4
    b = 2 * s + 3
    k = s + 3
    c_minus = k - b / a
    c_plus = k - b * start / (a * start + b)
    return a, b, k, c_minus, c_plus


def accelerated_interval(s: Q, w: list[Q], start: int) -> tuple[Q, Q, Q]:
    """Use the stated analytic tail theorem; check its width exactly."""
    a, b, k, c_minus, c_plus = tail_constants(s, start)
    u_start = w[start] / (start * start)
    head = sum((w[n] / (n * n) for n in range(1, start)), Q(0))
    lower_tail = u_start * (start + c_minus) / k
    upper_tail = u_start * (start + c_plus) / k
    width = u_start * b * b / (k * a * (a * start + b))
    require(upper_tail - lower_tail == width, "accelerated tail width")
    _, _, c = reduction_constants(s)
    constant = Q(2) / ((s + 1) * (s + 2))
    return constant + c * (head + lower_tail), constant + c * (head + upper_tail), c * width


def ctmc_interval(s: Q, w: list[Q], last_state: int) -> tuple[Q, Q]:
    """Use first-promotion hazard bounds after reaching last_state + 1."""
    head = killed_backward_transform(s, last_state)
    discounted_arrival = (last_state + 1) * w[last_state]
    current_hazard = Q(last_state + 1, last_state + 2)
    return (
        head + discounted_arrival * current_hazard / (s + current_hazard),
        head + discounted_arrival / (s + 1),
    )


def outward_decimal(x: Q, rounding: str, places: int = 30) -> str:
    with localcontext() as ctx:
        ctx.prec = places + 20
        ctx.rounding = rounding
        value = Decimal(x.numerator) / Decimal(x.denominator)
        return format(value.quantize(Decimal(1).scaleb(-places)), "f")


def primes_up_to(bound: int) -> list[int]:
    sieve = bytearray(b"\x01") * (bound + 1)
    sieve[0:2] = b"\x00\x00"
    for p in range(2, isqrt(bound) + 1):
        if sieve[p]:
            sieve[p * p : bound + 1 : p] = b"\x00" * ((bound - p * p) // p + 1)
    return [p for p in range(2, bound + 1) if sieve[p]]


def valuation(value: int, prime: int) -> int:
    require(value > 0, "valuation requires a positive integer")
    exponent = 0
    while value % prime == 0:
        value //= prime
        exponent += 1
    return exponent


def factorial_valuation(n: int, prime: int) -> int:
    total = 0
    while n:
        n //= prime
        total += n
    return total


def square_discriminant(s: Q) -> dict[str, object]:
    p, q = s.numerator, s.denominator
    delta = p * p + 4 * q * q
    root = isqrt(delta)
    report: dict[str, object] = {
        "s": str(s), "integer_discriminant": delta, "is_square": root * root == delta
    }
    if root * root == delta:
        radical = Q(root, q)
        a = (s + 2 + radical) / 2
        b = (s + 2 - radical) / 2
        require(a + b == s + 2 and a * b == s, "rational quadratic factors")
        report.update({"sqrt_s_squared_plus_4": str(radical), "a": str(a), "b": str(b)})
    return report


def run_checks(max_n: int, prime_bound: int) -> dict[str, object]:
    cases = {
        "zero": Q(0),
        "small_positive": Q(1, 20),
        "quarter": Q(1, 4),
        "half": Q(1, 2),
        "rational_candidate": Q(13, 23),
        "original_lower_endpoint": Q(113, 200),
        "original_upper_endpoint": Q(2832242711, 5000000000),
        "three_quarters": Q(3, 4),
        "one": Q(1),
        "split_three_halves": Q(3, 2),
        "split_inside_original_interval": Q(2603, 4602),
        "two": Q(2),
        "three": Q(3),
        "seven_halves": Q(7, 2),
    }
    diagnostic_n = [50, 100, 250, 500, 1000]
    tail_starts = [1, 2, 3, 5, 10, 20, 51]
    w_limit = max(max_n + 1, max(diagnostic_n), max(tail_starts) + max_n + 1)
    count: Counter[str] = Counter()
    ps = primes_up_to(prime_bound)
    output_cases: dict[str, object] = {}

    for name, s in cases.items():
        w = weights(s, w_limit)
        a, b, c = reduction_constants(s)
        discounted_arrival = Q(1)
        partial = Q(0)
        weighted_partial = Q(0)
        raw_integer_product = 1
        factorial = 1
        p, q = s.numerator, s.denominator

        for j in range(1, max_n + 1):
            leaf, promotion = null_eliminated_channels(s, j)
            proper_rate = Q(j) + Q(j, j + 1)
            require(leaf == Q(j) / (s + proper_rate), f"leaf elimination {name}, {j}")
            require(promotion == Q(j, j + 1) / (s + proper_rate), f"promotion elimination {name}, {j}")
            require(discounted_arrival * promotion == w[j], f"promotion mass {name}, {j}")
            discounted_arrival *= leaf
            require(discounted_arrival == (j + 1) * w[j], f"arrival mass {name}, {j}")
            count["null_elimination_and_ctmc_mass_identities"] += 4

            factorial *= j
            raw_integer_product *= q * j * j + (p + 2 * q) * j + p
            require(w[j] == Q(q**j * factorial * factorial, raw_integer_product), f"integer product {name}, {j}")
            count["integer_product_identities"] += 1

            n = j - 1
            require(
                w[n] * (a * n + b) - w[n + 1] * (a * (n + 1) + b)
                == w[n] - c * w[n + 1] / ((n + 1) ** 2),
                f"telescoping difference {name}, {n}",
            )
            partial += w[j]
            weighted_partial += w[j] / (j * j)
            boundary = w[j] * (a * j + b - 1)
            require(
                partial == Q(2) / ((s + 1) * (s + 2)) + c * weighted_partial - boundary,
                f"finite boundary identity {name}, {j}",
            )
            count["reduction_and_boundary_identities"] += 2
            require(partial == killed_backward_transform(s, j), f"backward CTMC transform {name}, {j}")
            count["independent_backward_ctmc_identities"] += 1
            if s == 0:
                require(w[j] == Q(2, (j + 1) * (j + 2)), f"zero-discount mass {j}")
                require(partial == 1 - Q(2, j + 2), f"zero-discount partial sum {j}")
                count["zero_discount_identities"] += 2

        for start in tail_starts:
            aa, bb, k, c_minus, c_plus = tail_constants(s, start)
            for n in range(start, start + max_n + 1):
                u = w[n] / (n * n)
                next_u = w[n + 1] / ((n + 1) ** 2)
                denominator = n * n + aa * n + bb
                require(next_u / u == Q(n * n) / denominator, f"u recurrence {name}, {n}")
                residual_minus = u * (n + c_minus) / k - next_u * (n + 1 + c_minus) / k - u
                residual_plus = u * (n + c_plus) / k - next_u * (n + 1 + c_plus) / k - u
                require(residual_minus == -u * bb * bb / (k * aa * denominator), f"lower residual identity {name}, {n}")
                require(residual_plus == u * bb * bb * (n - start) / (k * (aa * start + bb) * denominator), f"upper residual identity {name}, {n}")
                require(residual_minus < 0 and residual_plus >= 0, f"tail signs {name}, {n}")
                require((residual_plus == 0) == (n == start), f"strict upper residual {name}, {n}")
                count["tail_recurrence_residual_and_sign_checks"] += 5
            lower, upper, width = accelerated_interval(s, w, start)
            require(upper - lower == width and width >= 0, f"transform width {name}, {start}")
            require((width == 0) == (s == 0), f"strict transform width {name}, {start}")
            count["accelerated_interval_width_checks"] += 2

        delta = p * p + 4 * q * q
        inert_primes = []
        split_primes = []
        for ell in ps:
            if (2 * q * delta) % ell == 0:
                continue
            symbol = pow(delta % ell, (ell - 1) // 2, ell)
            require(symbol in (1, ell - 1), "good-prime Legendre symbol")
            if symbol == ell - 1:
                inert_primes.append(ell)
            else:
                split_primes.append(ell)
            for n in range(1, max_n + 1):
                numerator_valuation = valuation(w[n].numerator, ell)
                expected = 2 * factorial_valuation(n, ell) if symbol == ell - 1 else 0
                require(numerator_valuation == expected, f"prime valuation {name}, {ell}, {n}")
                count["good_prime_numerator_valuation_checks"] += 1

        lower, upper, width = accelerated_interval(s, w, 51)
        broad_lower, broad_upper = ctmc_interval(s, w, max_n)
        require(lower <= broad_upper and broad_lower <= upper, f"independent intervals overlap {name}")
        count["independent_interval_overlap_checks"] += 1
        if s == 0:
            require(lower == upper == broad_lower == broad_upper == 1, "exact zero-discount transform")
            count["zero_discount_transform_checks"] += 1

        diagnostic = []
        for n in diagnostic_n:
            diagnostic.append({
                "n": n,
                "denominator_bits": w[n].denominator.bit_length(),
                "log_denominator_over_n_log_n": log(w[n].denominator) / (n * log(n)),
            })
        output_cases[name] = {
            "s": str(s),
            "discriminant": square_discriminant(s),
            "w_1": str(w[1]),
            "w_max_n": str(w[max_n]),
            "partial_transform_max_n": str(partial),
            "accelerated_transform_interval": {
                "tail_starts_at": 51,
                "lower": str(lower), "upper": str(upper), "width": str(width),
                "lower_decimal_outward": outward_decimal(lower, ROUND_FLOOR),
                "upper_decimal_outward": outward_decimal(upper, ROUND_CEILING),
                "certification": "Exact endpoints conditional only on the stated analytic tail and boundary-limit proofs; finite residual identities checked here.",
            },
            "independent_ctmc_hazard_interval": {
                "kill_after_leaf_state": max_n,
                "lower": str(broad_lower), "upper": str(broad_upper),
                "overlaps_accelerated_interval": True,
            },
            "good_inert_primes_checked": inert_primes,
            "good_split_primes_checked": split_primes,
            "floating_denominator_diagnostics_not_proofs": diagnostic,
        }

    conic = Q(2603, 4602)
    require(Q(113, 200) < conic < Q(2832242711, 5000000000), "split example inside original bracket")
    require(conic == Q(78 * 78 - 59 * 59, 78 * 59), "rational conic parametrization")
    require(square_discriminant(conic)["is_square"] is True, "split example discriminant")
    require(square_discriminant(Q(1281, 2260))["is_square"] is False, "rejected conic example")
    count["rational_conic_checks"] += 4
    return {
        "status": "PASS",
        "arithmetic": "Python standard library: exact integers and fractions.Fraction for every decision",
        "scope": "Finite checks for the original inert newborn first-promotion packet, its reduction, tail residuals, and good-prime valuation identities.",
        "configuration": {"max_n_exact_checks": max_n, "prime_bound": prime_bound, "cases": len(cases)},
        "checks": dict(sorted(count.items())),
        "total_checks": sum(count.values()),
        "formulae": {
            "w_n": "product(j^2/[j^2+(s+2)j+s], j=1..n); w_0=1",
            "first_promotion_transform": "L(s)=sum(w_n,n>=1)",
            "finite_reduction": "sum(w_n,n=1..N)=2/[(s+1)(s+2)]+s^2/[(s+1)(s+2)]*sum(w_n/n^2,n=1..N)-w_N*(N/(s+1)+2/[(s+1)(s+2)])",
            "accelerated_tail": "u_M*(M+c_minus)/k < sum(u_n,n>=M) < u_M*(M+c_plus(M))/k, u_n=w_n/n^2, k=s+3, A=s+4, B=2s+3, c_minus=k-B/A, c_plus(M)=k-B*M/(A*M+B)",
        },
        "rejected_square_discriminant_example": square_discriminant(Q(1281, 2260)),
        "cases": output_cases,
        "not_proved_by_this_program": [
            "The infinite telescoping boundary limit and infinite-tail inequalities require their written analytic proofs.",
            "Prime-density arguments and denominator asymptotics require their written number-theoretic proofs.",
            "Floating denominator diagnostics cannot establish any asymptotic estimate.",
            "The first-promotion packet alone does not characterize the original growth exponent.",
            "No irrationality or transcendence claim is established for the first-promotion transform or the original exponent.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="run the full finite check suite (also the default)")
    parser.add_argument("--max-n", type=int, default=80)
    parser.add_argument("--prime-bound", type=int, default=251)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    if args.max_n < 1:
        parser.error("--max-n must be positive")
    if args.prime_bound < 3:
        parser.error("--prime-bound must be at least 3")
    report = run_checks(args.max_n, args.prime_bound)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    examples = {
        name: {
            "s": case["s"],
            "lower": case["accelerated_transform_interval"]["lower_decimal_outward"],
            "upper": case["accelerated_transform_interval"]["upper_decimal_outward"],
        }
        for name, case in report["cases"].items()
        if name in ("rational_candidate", "original_lower_endpoint", "original_upper_endpoint", "split_inside_original_interval")
    }
    print(json.dumps({"status": report["status"], "total_checks": report["total_checks"], "checks": report["checks"], "examples": examples, "output": str(args.output)}, indent=2))


if __name__ == "__main__":
    main()
