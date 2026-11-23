#!/usr/bin/env python3
"""Construct and audit signed integer polynomials for full critical certificates.

The exact positive lower sum L_{m,R,N}(s) uses all core-clock rings,
including null stub choices, and a separate real-birth budget. The proved
clearer D=M_N^R*product((s+j)^R,j=2..N+2) makes Q=D*L an integer polynomial
of degree at most R*(N+1). This program recovers Q by exact interpolation
and forms P=12*(s+3)*D-Q. Additional rational evaluations are checked
against the independently ordered individual-clock recursion.

Examples:
  python3 scripts/check_critical_root_forms.py --check
  python3 scripts/check_critical_root_forms.py --generation 2 --core-rings 3 --max-births 4 --isolate-root
  python3 scripts/check_critical_root_forms.py --check --output build/verification/critical_root_form_checks.json

All decisions use exact integers or Fraction. The small default checks
produce only the zero lower-root convention, not a new estimate of mu.
No file is written unless --output is supplied. Neither finite checks nor
the polynomial construction prove irrationality or transcendence.
"""

from __future__ import annotations

import argparse
from collections import Counter
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR, localcontext
from fractions import Fraction as F
from functools import lru_cache
import hashlib
import json
from math import factorial, lcm
from pathlib import Path

from inert_growth_kernel import inert_coefficient, ordered_event_prefix


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def trim(coefficients: list[F] | list[int]) -> list:
    result = list(coefficients)
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


def poly_add(left: list, right: list) -> list:
    result = [F(0)] * max(len(left), len(right))
    for index, coefficient in enumerate(left):
        result[index] += coefficient
    for index, coefficient in enumerate(right):
        result[index] += coefficient
    return trim(result)


def poly_scale(coefficients: list, scalar: F | int) -> list:
    return trim([scalar * coefficient for coefficient in coefficients])


def poly_multiply(left: list, right: list) -> list:
    result = [F(0)] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] += a * b
    return trim(result)


def poly_value(coefficients: list | tuple, value: F | int) -> F:
    result = F(0)
    for coefficient in reversed(coefficients):
        result = result * value + coefficient
    return result


def poly_degree(coefficients: list | tuple) -> int:
    return -1 if all(coefficient == 0 for coefficient in coefficients) else len(coefficients) - 1


@lru_cache(maxsize=None)
def finite_lower(s: F, generation: int, rings: int, births: int) -> F:
    return inert_coefficient(s, generation, rings, births).lower


@lru_cache(maxsize=None)
def ordered_lower(s: F, generation: int, rings: int, births: int) -> F:
    return ordered_event_prefix(s, generation, rings, births)


def denominator_polynomial(rings: int, births: int) -> tuple[int, list[int]]:
    if rings < 1 or births < 0:
        raise ValueError("Require R>=1 and N>=0.")
    integer_clearer = lcm(*range(1, births + 3))
    polynomial = [F(integer_clearer**rings)]
    for shift in range(2, births + 3):
        for _ in range(rings):
            polynomial = poly_multiply(polynomial, [shift, 1])
    require(all(value.denominator == 1 for value in polynomial), "D integrality")
    return integer_clearer, [int(value) for value in polynomial]


def interpolate_at_positive_integers(values: list[F]) -> list[F]:
    """Newton forward interpolation on the nodes 1,...,len(values)."""
    differences = list(values)
    basis = [F(1)]
    polynomial = [F(0)]
    for order in range(len(values)):
        polynomial = poly_add(polynomial, poly_scale(basis, differences[0] / factorial(order)))
        differences = [differences[j + 1] - differences[j] for j in range(len(differences) - 1)]
        basis = poly_multiply(basis, [-(order + 1), 1])
    return trim(polynomial)


def construct_polynomials(generation: int, rings: int, births: int) -> dict[str, object]:
    if generation < 1 or rings < 1 or births < 0:
        raise ValueError("Require m>=1, R>=1, N>=0.")
    integer_clearer, denominator = denominator_polynomial(rings, births)
    degree_bound = rings * (births + 1)
    values = [
        poly_value(denominator, s) * finite_lower(F(s), generation, rings, births)
        for s in range(1, degree_bound + 2)
    ]
    numerator = interpolate_at_positive_integers(values)
    require(all(coefficient.denominator == 1 for coefficient in numerator), "Q coefficient integrality")
    require(all(coefficient >= 0 for coefficient in numerator), "Q coefficient positivity")
    numerator_int = [int(coefficient) for coefficient in numerator]
    signed = poly_add(poly_multiply(denominator, [36, 12]), poly_scale(numerator_int, -1))
    require(all(coefficient.denominator == 1 for coefficient in signed), "P coefficient integrality")
    return {
        "generation": generation, "core_rings": rings, "max_births": births,
        "degree_bound_Q": degree_bound, "integer_clearer": integer_clearer,
        "D": denominator, "Q": numerator_int, "P": [int(coefficient) for coefficient in signed],
    }


def omitted_history_mass(s: F, generation: int, rings: int) -> F:
    answer = F(1) / (2 * (s + 2))**rings
    for j in range(generation):
        answer /= 2 * (s + j + 2)
    return answer


def isolate_positive_root(polynomial: list[int], bits: int = 40) -> dict[str, object]:
    """Isolate the unique positive threshold root, using its proved monotonicity.

    The caller supplies one of the certificate polynomials, whose sign is
    the sign of the strictly increasing residual because D is positive.
    The convention is zero when P(0)>=0. A positive root lies below 1.
    """
    if bits < 1:
        raise ValueError("The isolation precision must be positive.")
    if poly_value(polynomial, 0) >= 0:
        return {"kind": "zero_convention", "value": "0",
                "reason": "There is no positive threshold root because L(0)<=36."}
    require(poly_value(polynomial, 1) > 0, "positive root must be bracketed below 1")
    lower, upper = F(0), F(1)
    for _ in range(bits):
        middle = (lower + upper) / 2
        value = poly_value(polynomial, middle)
        if value == 0:
            return {"kind": "exact_positive_root", "value": str(middle)}
        if value < 0:
            lower = middle
        else:
            upper = middle
    return {"kind": "strict_rational_bracket", "lower": str(lower),
            "upper": str(upper), "width": str(upper - lower), "bits": bits}


def integer_coefficient_report(data: dict[str, object], include_root: bool, bits: int) -> dict[str, object]:
    result = {
        "status": "COMPUTED",
        "parameters": {name: data[name] for name in ("generation", "core_rings", "max_births")},
        "coefficient_order": "constant term first",
        "integer_clearer": str(data["integer_clearer"]),
        "D_coefficients": [str(value) for value in data["D"]],
        "Q_coefficients": [str(value) for value in data["Q"]],
        "P_coefficients": [str(value) for value in data["P"]],
        "degree_P": poly_degree(data["P"]),
        "height_P": str(max(abs(value) for value in data["P"])),
        "degree_bound_P": int(data["degree_bound_Q"]) + 1,
        "height_bound_P": str(49 * poly_value(data["D"], 1)),
        "scope": "A finite full-kernel threshold polynomial; its nonvanishing at mu requires the written omitted-history proof.",
    }
    if include_root:
        result["positive_root"] = isolate_positive_root(data["P"], bits)
    return result


def outward_decimal(value: F, rounding: str, places: int = 18) -> str:
    with localcontext() as context:
        context.prec = places + 30
        context.rounding = rounding
        decimal = Decimal(value.numerator) / Decimal(value.denominator)
        return format(decimal.quantize(Decimal(1).scaleb(-places)), "f")


def potential_ring_values(s: F, rings: int) -> tuple[F, F]:
    product, total = F(1), F(0)
    for j in range(1, rings + 1):
        product *= F(j) / (j + s)
        total += product
    return product, total


def run_checks() -> dict[str, object]:
    counts: Counter[str] = Counter()

    def check(condition: bool, category: str) -> None:
        require(condition, category)
        counts[category] += 1

    discounts = (F(1, 2), F(2, 3), F(113, 200), F(3, 2))
    a, b = F(113, 200), F(2832242711, 5000000000)
    records = []
    examples = []
    for rings in range(1, 4):
        for births in range(5):
            for generation in range(1, 4):
                data = construct_polynomials(generation, rings, births)
                denominator, numerator, signed = data["D"], data["Q"], data["P"]
                degree = rings * (births + 1)
                for coefficient in numerator:
                    check(isinstance(coefficient, int) and coefficient >= 0, "Q_integral_nonnegative_coefficients")
                check(poly_degree(numerator) <= degree, "Q_degree_bound")
                check(poly_degree(signed) <= degree + 1, "P_degree_bound")
                check(poly_value(numerator, 1) <= poly_value(denominator, 1), "Q_at_one_bound")
                check(max(abs(value) for value in signed) <= 49 * poly_value(denominator, 1), "P_height_bound")
                expected_D_one = data["integer_clearer"]**rings * (factorial(births + 3) // 2)**rings
                check(poly_value(denominator, 1) == expected_D_one, "D_at_one_factorial_identity")
                zero_lower = ordered_lower(F(0), generation, rings, births)
                check(poly_value(numerator, 0) == poly_value(denominator, 0) * zero_lower, "independent_zero_discount_extension")
                check(zero_lower <= rings, "finite_ring_reward_bound_at_zero")
                root = isolate_positive_root(signed)
                check(root["kind"] == "zero_convention", "small_budget_zero_root_convention")

                for s in discounts:
                    burst = finite_lower(s, generation, rings, births)
                    ordered = ordered_lower(s, generation, rings, births)
                    check(burst == ordered, "burst_BFS_vs_ordered_events")
                    check(poly_value(numerator, s) == poly_value(denominator, s) * ordered,
                          "interpolation_at_new_rational_points")
                    check(poly_value(signed, s) == poly_value(denominator, s) * (12 * (s + 3) - ordered),
                          "signed_residual_at_new_rational_points")
                    enlarged = finite_lower(s, generation, rings + generation, max(births, generation))
                    omitted = omitted_history_mass(s, generation, rings)
                    check(enlarged - burst >= omitted, "explicit_omitted_history_in_larger_budget")
                    _, ring_envelope = potential_ring_values(s, rings)
                    check(burst <= ring_envelope, "potential_core_ring_envelope")

                coefficient_bytes = json.dumps(signed, separators=(",", ":")).encode()
                records.append({
                    "m": generation, "R": rings, "N": births,
                    "D_degree": degree, "Q_degree": poly_degree(numerator),
                    "P_degree": poly_degree(signed),
                    "P_height": str(max(abs(value) for value in signed)),
                    "P_coefficient_sha256": hashlib.sha256(coefficient_bytes).hexdigest(),
                    "analytic_nonvanishing_lower_bound_from_proof": str(
                        poly_value(denominator, a) * omitted_history_mass(b, generation, rings)),
                    "positive_root": root,
                })
                if (generation, rings, births) in ((1, 1, 1), (1, 2, 2), (2, 2, 2), (3, 3, 3)):
                    examples.append(integer_coefficient_report(data, True, 40))

    for h in range(1, 5):
        _, denominator = denominator_polynomial(h, h)
        for generation in range(1, h + 1):
            for s in discounts:
                check(poly_value(denominator, s) * omitted_history_mass(s, generation, h) > F(3, 2)**h,
                      "literal_diagonal_form_lower_growth")

    for s in (F(1, 2), F(113, 200), F(1), F(3, 2)):
        for rings in range(21):
            product, total = potential_ring_values(s, rings)
            if s == 1:
                closed = sum((F(1, j) for j in range(2, rings + 2)), F(0))
            else:
                closed = ((rings + 1) * product - 1) / (1 - s)
            check(total == closed, "potential_ring_closed_form")
    threshold = 12 * (a + 3)
    product_before, before = potential_ring_values(a, 1221)
    product_after = product_before * F(1222) / (1222 + a)
    after = before + product_after
    check(before < threshold < after, "minimum_ring_threshold_crossing")
    check(before == (1222 * product_before - 1) / (1 - a), "large_ring_closed_form_before")
    check(after == (1223 * product_after - 1) / (1 - a), "large_ring_closed_form_after")
    for value in (before, after):
        check(F(outward_decimal(value, ROUND_FLOOR)) <= value,
              "outward_display_lower_bounds")
        check(value <= F(outward_decimal(value, ROUND_CEILING)),
              "outward_display_upper_bounds")

    # These known integer polynomials exercise the positive-root isolation
    # branch, which cannot occur at the small friend-tree budgets above.
    exact = isolate_positive_root([-1, 2], 20)
    check(exact == {"kind": "exact_positive_root", "value": "1/2"}, "root_isolator_known_exact_root")
    rational = isolate_positive_root([-1, 3], 20)
    check(F(rational["lower"]) < F(1, 3) < F(rational["upper"]), "root_isolator_known_rational_root")
    algebraic = isolate_positive_root([-1, 0, 2], 20)
    lo, hi = F(algebraic["lower"]), F(algebraic["upper"])
    check(lo * lo < F(1, 2) < hi * hi, "root_isolator_known_algebraic_root")
    check(hi - lo == F(1, 2**20), "root_isolator_exact_width")

    return {
        "status": "PASS",
        "arithmetic": "Exact Python integers and fractions.Fraction for every decision; Decimal only for outward display bounds.",
        "scope": "Finite full-environment certificate polynomials, independent ordered-event evaluations, explicit omitted histories, and potential-ring cost bounds.",
        "configuration": {"generations": [1, 2, 3], "core_ring_budgets": [1, 2, 3],
                          "real_birth_budgets": [0, 1, 2, 3, 4], "polynomial_cases": len(records),
                          "fresh_rational_discounts": [str(s) for s in discounts]},
        "checks": dict(sorted(counts.items())), "total_checks": sum(counts.values()),
        "coefficient_order": "constant term first",
        "cases": records, "sample_polynomials": examples,
        "minimum_ring_budget_diagnostic": {
            "test_discount": str(a), "threshold": str(threshold),
            "S_1221_lower_decimal": outward_decimal(before, ROUND_FLOOR),
            "S_1221_upper_decimal": outward_decimal(before, ROUND_CEILING),
            "S_1222_lower_decimal": outward_decimal(after, ROUND_FLOOR),
            "S_1222_upper_decimal": outward_decimal(after, ROUND_CEILING),
            "necessary_core_ring_budget_for_root_in_current_enclosure": 1222,
            "meaning": "The universal potential-ring envelope lies below the required threshold through R=1221. This is a necessary cost condition, not a sufficient certificate or a new estimate of mu.",
        },
        "not_proved_by_this_program": [
            "The full critical pressure characterization and the infinite-model noncancellation theorem require their written proofs.",
            "Interpolation uses the proved degree bound; extra finite evaluations do not establish the general polynomial theorem.",
            "The default small budgets have no positive lower threshold root and yield no new bound for mu.",
            "No rapid root-convergence rate, efficient arbitrary-precision solver, irrationality, or transcendence assertion is established.",
            "The literal polynomial growth diagnostic is not a claim about optimal or primitive denominator clearers.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="run the default exact finite checks (also the default without budgets)")
    parser.add_argument("--generation", type=int)
    parser.add_argument("--core-rings", type=int)
    parser.add_argument("--max-births", type=int)
    parser.add_argument("--isolate-root", action="store_true", help="also isolate the polynomial's positive threshold root, or report the zero convention")
    parser.add_argument("--root-bits", type=int, default=40)
    parser.add_argument("--output", type=Path, help="optional destination for the complete JSON report")
    args = parser.parse_args()
    budgets = (args.generation, args.core_rings, args.max_births)
    if args.check and any(value is not None for value in budgets):
        parser.error("Use --check or supply the three polynomial budgets, not both.")
    if any(value is not None for value in budgets) and not all(value is not None for value in budgets):
        parser.error("Polynomial construction requires --generation, --core-rings, and --max-births together.")
    if args.root_bits < 1:
        parser.error("--root-bits must be positive.")
    if all(value is None for value in budgets):
        if args.isolate_root:
            parser.error("--isolate-root requires explicit polynomial budgets.")
        report = run_checks()
    else:
        try:
            data = construct_polynomials(*budgets)
        except ValueError as error:
            parser.error(str(error))
        report = integer_coefficient_report(data, args.isolate_root, args.root_bits)
    serialized = json.dumps(report, indent=2) + "\n"
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized, encoding="utf-8")
    print(serialized, end="")


if __name__ == "__main__":
    main()
