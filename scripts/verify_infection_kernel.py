#!/usr/bin/env python3
"""Exact rational certificate for the old-core disagreement reproduction bound.

No floating point is used in any assertion.  Decimal strings in the report
are for readability only.  The pure birth process starts at 1 and jumps
n -> n+1 at rate n+5/2.  Its discounted occupation weight at s=11/20 is
w_1=20/81 and w_{n+1}/w_n=(20n+50)/(20n+81).
"""

from fractions import Fraction as F
import json


def certificate():
    s = F(11, 20)
    bound = F(19, 20)
    truncation = 16
    weights = [F(20, 81)]
    for n in range(1, truncation):
        weights.append(weights[-1] * F(20 * n + 50, 20 * n + 81))

    finite = []
    for d in range(2, 64):
        harmonic_partial = sum(
            (w / (d + n) for n, w in enumerate(weights, start=1)),
            F(0),
        )
        upper = F(d - 1, d) * (1 / s - d * harmonic_partial)
        assert upper < bound, (d, upper)
        finite.append((d, upper))

    # For d >= 64, m_d(s) <= 4 sqrt(7/(2d)) <= sqrt(7/8).
    # Squaring is legitimate because both sides are positive.
    assert F(7, 8) < F(15, 16) ** 2
    assert F(15, 16) < bound
    absorption = 40 / (s ** 2 * 133)
    assert absorption == F(16000, 16093) < 1

    maximum_degree, maximum = max(finite, key=lambda pair: pair[1])
    return {
        "status": "PASS",
        "discount": str(s),
        "birth_offset": "5/2",
        "uniform_reproduction_bound": str(bound),
        "finite_degrees_checked": [2, 63],
        "terms_per_degree": truncation,
        "maximum_finite_upper_degree": maximum_degree,
        "maximum_finite_upper_exact": str(maximum),
        "maximum_finite_upper_decimal": format(float(maximum), ".16f"),
        "large_degree_threshold": 64,
        "large_degree_squared_bound": "7/8 < (15/16)^2",
        "all_finite_checks_exact": True,
        "universal_absorption_cutoff_M": 132,
        "absorption_coefficient_at_cutoff": str(absorption),
    }


if __name__ == "__main__":
    print(json.dumps(certificate(), indent=2))
