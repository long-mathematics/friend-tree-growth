#!/usr/bin/env python3
"""Exact helpers for a future friend-tree root solver.

The Yule cutoff bound is fully implemented. The trisection driver is an
adapter for complete strict-comparison certificate streams; this file does
not implement the full friend-tree upper-certificate search.
"""

from __future__ import annotations

from collections.abc import Callable, Iterator
from dataclasses import dataclass
from fractions import Fraction
import json
from math import comb
from typing import Literal


Q = Fraction


def generation_tail_bound(upper: Q, discount: Q, terms: int,
                          comparison: Q = Q(2)) -> Q:
    """Bound sum_{m>terms} A_m(discount), provided upper >= mu is certified.

    This routine does not certify its supplied upper bound and does not
    evaluate the coefficients or the pressure. The chord bound for
    comparison**(-alpha) makes its output entirely rational.
    """
    b, s, endpoint = Q(upper), Q(discount), Q(comparison)
    if not 0 < b < s <= endpoint or endpoint <= 1 or terms < 0:
        raise ValueError("Require 0<b<s<=S, S>1, and terms>=0.")
    alpha = (s - b) / (endpoint - b)
    ratio = 1 - alpha * (1 - 1 / endpoint)
    return 12 * (b + 3) * ratio**(terms + 1) / (1 - ratio)


def generation_cutoff(upper: Q, discount: Q, tolerance: Q,
                      comparison: Q = Q(2)) -> int:
    """Smallest truncation index meeting the rational generation majorant."""
    if tolerance <= 0:
        raise ValueError("The tolerance must be positive.")
    if generation_tail_bound(upper, discount, 0, comparison) <= tolerance:
        return 0
    lower, upper_index = 0, 1
    while generation_tail_bound(upper, discount, upper_index, comparison) > tolerance:
        lower, upper_index = upper_index, 2 * upper_index
    while upper_index - lower > 1:
        middle = (lower + upper_index) // 2
        if generation_tail_bound(upper, discount, middle, comparison) <= tolerance:
            upper_index = middle
        else:
            lower = middle
    return upper_index


def full_tree_generating_tail(cutoff: int, argument: Q) -> Q:
    """Bound the full-tree scalar G(z) tail using a_n <= n-2."""
    z = Q(argument)
    if cutoff < 2 or not 0 < z < 1:
        raise ValueError("Require cutoff>=2 and 0<z<1.")
    m = cutoff - 1
    return z**m * (m * (m + 1) / (1 - z)
                   + (2 * m + 1) * z / (1 - z)**2
                   + z * (1 + z) / (1 - z)**3)


def yule_tail_mean(founders: int, cutoff: int, survival: Q) -> Q:
    """E[Y_n(t); Y_n(t)>N], where survival = exp(-t).

    Evaluating at a rational lower bound for exp(-T) instead supplies a
    rigorous rational upper bound for the tail at T.
    """
    if founders < 1 or cutoff < founders or not 0 < survival <= 1:
        raise ValueError("Require n>=1, N>=n, and 0<p<=1.")
    p = Q(survival)
    q = 1 - p
    return founders / p * sum(
        (Q(comb(cutoff + 1, j)) * p**j * q**(cutoff + 1 - j)
         for j in range(founders + 1)), Q(0)
    )


def yule_population_cutoff(founders: int, survival: Q, tolerance: Q) -> int:
    """Smallest N>=n for which the exact tail bound is <= tolerance."""
    if tolerance <= 0:
        raise ValueError("The tolerance must be positive.")
    if yule_tail_mean(founders, founders, survival) <= tolerance:
        return founders
    lower = founders
    upper = max(founders + 1, 2 * founders)
    while yule_tail_mean(founders, upper, survival) > tolerance:
        lower, upper = upper, 2 * upper
    while upper - lower > 1:
        middle = (lower + upper) // 2
        if yule_tail_mean(founders, middle, survival) <= tolerance:
            upper = middle
        else:
            lower = middle
    return upper


@dataclass(frozen=True)
class StrictComparison:
    test: Q
    relation: Literal["below", "above"]
    evidence: str


@dataclass(frozen=True)
class Bracket:
    lower: Q
    upper: Q
    depth: int
    evidence: str


ComparisonStream = Callable[[Q], Iterator[StrictComparison | None]]


def trisection_round(previous: Bracket, steps: ComparisonStream) -> Bracket:
    """One equality-safe round, assuming sound complete strict streams.

    Each next(stream) must finish in finite time. At a point different from
    the unknown root, the stream eventually returns a sound strict
    comparison. At equality it may yield None forever. The two streams
    are advanced alternately, so one necessarily supplies a certificate.
    """
    a, b = previous.lower, previous.upper
    if not a < b:
        raise ValueError("The initial bracket must have positive width.")
    points = ((2 * a + b) / 3, (a + 2 * b) / 3)
    streams = [iter(steps(point)) for point in points]
    active = [True, True]
    while any(active):
        for i, point in enumerate(points):
            if not active[i]:
                continue
            try:
                certificate = next(streams[i])
            except StopIteration:
                active[i] = False
                continue
            if certificate is None:
                continue
            if certificate.test != point:
                raise ValueError("Certificate test point does not match its stream.")
            if certificate.relation == "below":
                return Bracket(point, b, previous.depth + 1, certificate.evidence)
            if certificate.relation == "above":
                return Bracket(a, point, previous.depth + 1, certificate.evidence)
            raise ValueError("Certificate relation must be 'below' or 'above'.")
    raise RuntimeError("Both strict-comparison streams ended without a certificate.")


def check() -> dict[str, object]:
    count = 0
    for n in range(1, 9):
        for p in (Q(1, 4), Q(1, 2), Q(3, 4), Q(1)):
            # Independent initial condition and tail-difference recurrence
            # from the negative-binomial point probabilities.
            assert yule_tail_mean(n, n, p) == n / p - n * p**n
            count += 1
            for cutoff in range(n, n + 30):
                mass = Q(comb(cutoff, n - 1)) * p**n * (1 - p)**(cutoff + 1 - n)
                assert (yule_tail_mean(n, cutoff, p)
                        - yule_tail_mean(n, cutoff + 1, p)) == (cutoff + 1) * mass
                count += 1
            for tolerance in (Q(1, 10), Q(1, 1000)):
                cutoff = yule_population_cutoff(n, p, tolerance)
                assert yule_tail_mean(n, cutoff, p) <= tolerance
                if cutoff > n:
                    assert yule_tail_mean(n, cutoff - 1, p) > tolerance
                count += 1

    rounds = 24
    examples = []
    for root in (Q(1, 3), Q(2, 3), Q(1, 7), Q(13, 23), Q(8, 9)):
        def steps(test: Q) -> Iterator[StrictComparison | None]:
            # The equality stream never decides. Deliberately nonuniform
            # delays exercise fair interleaving rather than an equality test
            # in the root driver itself.
            if test == root:
                while True:
                    yield None
            for _ in range((test.numerator + test.denominator) % 5):
                yield None
            relation = "below" if test < root else "above"
            yield StrictComparison(test, relation, "exact rational demonstration")

        bracket = Bracket(Q(0), Q(1), 0, "initial strict demonstration bracket")
        for depth in range(1, rounds + 1):
            previous = bracket
            bracket = trisection_round(bracket, steps)
            assert bracket.lower < root < bracket.upper
            assert previous.lower <= bracket.lower < bracket.upper <= previous.upper
            assert bracket.upper - bracket.lower <= Q(2, 3) ** depth
            assert (bracket.lower * 3**depth).denominator == 1
            assert (bracket.upper * 3**depth).denominator == 1
            count += 5
        examples.append({"root": str(root), "rounds": rounds,
                         "lower": str(bracket.lower), "upper": str(bracket.upper)})

    # Independent exact tests of the geometric interior-series tail.
    for z in (Q(1, 4), Q(1, 2), Q(3, 4)):
        for cutoff in range(2, 22):
            head = sum((m * (m + 1) * z**m for m in range(cutoff - 1)), Q(0))
            assert full_tree_generating_tail(cutoff, z) == 2 * z / (1 - z)**3 - head
            count += 1

    # The irrational exponential comparison is equivalent here to a
    # finite rational-power inequality, so no floating point is used.
    for endpoint in (Q(3, 2), Q(2), Q(3)):
        for alpha in (Q(1, 5), Q(1, 3), Q(1, 2), Q(2, 3), Q(1)):
            ratio = 1 - alpha * (1 - 1 / endpoint)
            assert ratio**alpha.denominator * endpoint**alpha.numerator >= 1
            count += 1

    # Exact pressure contraction constants after canceling log(2).
    assert Q(200, 287) / Q(400, 63) == Q(9, 82)
    assert 1 - Q(9, 82) == Q(73, 82)
    count += 2
    certified_upper = Q(2832242711, 5000000000)
    discount = Q(3, 5)
    tolerance = Q(1, 10**10)
    truncation = generation_cutoff(certified_upper, discount, tolerance)
    assert generation_tail_bound(certified_upper, discount, truncation) <= tolerance
    assert generation_tail_bound(certified_upper, discount, truncation - 1) > tolerance
    count += 2
    return {"status": "PASS", "exact_checks": count,
            "scope": "Exact Yule and scalar-series tails, rational generation majorants, and generic equality-safe root-driver checks; not a friend-tree root calculation or pressure evaluation.",
            "trisection_examples": examples,
            "example_yule_cutoff": yule_population_cutoff(3, Q(1, 8), Q(1, 10**12)),
            "generation_tail_example": {
                "certified_mu_upper_bound": str(certified_upper),
                "discount": str(discount), "tolerance": str(tolerance),
                "generation_terms_required_by_majorant": truncation,
                "scope": "Truncation bound only; the generation coefficients have not been computed in this example.",
            }}


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run the exact checks without -O or PYTHONOPTIMIZE.")
    print(json.dumps(check(), indent=2))
