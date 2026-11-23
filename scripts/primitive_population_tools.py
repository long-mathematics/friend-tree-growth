#!/usr/bin/env python3
"""Exact population-only coefficients and reduced arithmetic for the inert tree.

Null root-stub rings are summed exactly. N counts real births after the
initial two real vertices, not core rings. The default finite audit does
not calculate a successful critical certificate or new digits of mu.

Examples:
  python3 scripts/primitive_population_tools.py --check
  python3 scripts/primitive_population_tools.py --generation 2 --s 1/2 --max-births 5
  python3 scripts/primitive_population_tools.py --generation 2 --max-births 3 --polynomial

Files are written only with --output. Every inequality is decided with
integers or Fraction, including the rational enclosures of algebraic roots.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction as F
from functools import lru_cache
import json
from math import factorial, gcd, lcm
from pathlib import Path

from core_clock_kernel import CoreState
from inert_growth_kernel import (
    INERT_INITIAL, canonical_state, core_depths, ordered_event_prefix,
    core_ring_tail,
)
from check_critical_root_forms import (
    poly_add, poly_multiply, poly_scale, poly_value,
    interpolate_at_positive_integers, outward_decimal,
)
from decimal import ROUND_CEILING, ROUND_FLOOR


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


@lru_cache(maxsize=None)
def proper_channels(state: CoreState):
    """Canonical outcomes, exact proper rates, and new-core depths."""
    degrees = state.degrees()
    adjacency = state.neighbors()
    depths = core_depths(state)
    channels = defaultdict(F)
    for target in range(state.k):
        rate = state.leaves[target] + sum(
            (F(1, degrees[source]) for source in adjacency[target]), F(0))
        if rate:
            channels[(canonical_state(state.add_leaf(target)), 0)] += rate
        if state.leaves[target]:
            channels[(canonical_state(state.promote(target)), depths[target] + 1)] += (
                F(state.leaves[target], degrees[target]))
    population = state.k + sum(state.leaves)
    proper_rate = F(population) - F(1, degrees[0])
    require(sum(channels.values(), F(0)) == proper_rate, "proper-rate normalization")
    return tuple((new, depth, rate) for (new, depth), rate in channels.items())


@lru_cache(maxsize=None)
def population_coefficients(discount: F, births: int):
    """All generation rewards through N proper births, with nulls eliminated."""
    discount = F(discount)
    if discount < 0 or births < 0:
        raise ValueError("Require s>=0 and N>=0.")
    current = {INERT_INITIAL: F(1)}
    rewards = [F(0)] * (births + 1)
    layers = [1]
    for population in range(2, births + 2):
        following = defaultdict(F)
        for old, mass in current.items():
            denominator = discount + population - F(1, old.degrees()[0])
            for new, depth, rate in proper_channels(old):
                weight = mass * rate / denominator
                following[new] += weight
                if depth:
                    rewards[depth] += weight
        current = dict(following)
        layers.append(len(current))
    return tuple(rewards), tuple(layers)


def lower(discount: F, generation: int, births: int) -> F:
    discount = F(discount)
    if discount < 0 or generation < 1 or births < 0:
        raise ValueError("Require s>=0, m>=1 and N>=0.")
    if generation > births:
        return F(0)
    return population_coefficients(discount, births)[0][generation]


def backward_lower(discount: F, generation: int, births: int) -> F:
    """Independent direct source/neighbor recursion, solving its null self-loop."""
    discount = F(discount)
    if discount < 0 or generation < 1 or births < 0:
        raise ValueError("Require s>=0, m>=1 and N>=0.")
    if generation > births:
        return F(0)
    @lru_cache(maxsize=None)
    def visit(state: CoreState, remaining: int) -> F:
        if remaining == 0:
            return F(0)
        population = state.k + sum(state.leaves)
        denominator = population + discount
        degrees, adjacency, depths = state.degrees(), state.neighbors(), core_depths(state)
        answer = F(0)
        for target, leaf_count in enumerate(state.leaves):
            if leaf_count:
                answer += leaf_count / denominator * visit(
                    canonical_state(state.add_leaf(target)), remaining - 1)
        for source, degree in enumerate(degrees):
            for target in adjacency[source]:
                answer += F(1, degree) / denominator * visit(
                    canonical_state(state.add_leaf(target)), remaining - 1)
            if state.leaves[source]:
                answer += F(state.leaves[source], degree) / denominator * (
                    int(depths[source] + 1 == generation)
                    + visit(canonical_state(state.promote(source)), remaining - 1))
        null_weight = F(1, degrees[0]) / denominator
        return answer / (1 - null_weight)
    return visit(INERT_INITIAL, births)


def pole_pairs(generation: int, births: int) -> tuple[tuple[int, int], ...]:
    if not 1 <= generation <= births:
        raise ValueError("Require 1<=m<=N.")
    if generation == 1:
        return tuple((n, d) for n in range(2, births + 2) for d in range(2, n + 1)
                     if not (births >= 2 and n == births + 1 and d == 2))
    cap = births - generation + 2
    return tuple((n, d) for n in range(2, births + 2)
                 for d in range(2, min(n, cap) + 1))


def pole_denominator(generation: int, births: int) -> list[int]:
    polynomial = [1]
    for n, d in pole_pairs(generation, births):
        polynomial = poly_multiply(polynomial, [d * n - 1, d])
    return [int(value) for value in polynomial]


def primitive_form(generation: int, births: int):
    denominator = pole_denominator(generation, births)
    degree = len(denominator) - 1
    values = [poly_value(denominator, s) * lower(F(s), generation, births)
              for s in range(1, degree - generation + 2)]
    rational_numerator = interpolate_at_positive_integers(values)
    kappa = lcm(*(value.denominator for value in rational_numerator))
    numerator = [int(value * kappa) for value in rational_numerator]
    signed = poly_add(poly_scale(poly_multiply(denominator, [36, 12]), kappa),
                      poly_scale(numerator, -1))
    signed = [int(value) for value in signed]
    content = gcd(*signed)
    primitive = [value // content for value in signed]
    return denominator, kappa, numerator, content, primitive


def omitted_mass(discount: F, generation: int, births: int) -> F:
    extra_leaves = births + 1 - generation
    if not 1 <= generation <= births:
        raise ValueError("Require 1<=m<=N.")
    answer = F(1)
    for n in range(2, extra_leaves + 2):
        answer *= F(n * (n - 1)) / (n * (discount + n) - 1)
    degree = extra_leaves + 2
    answer *= F(degree - 1) / (degree * (discount + degree) - 1)
    for step in range(1, generation):
        answer *= F(degree, 2) / (degree * (discount + degree + step) - 1)
    return answer


def universal_omitted_mass(discount: F, births: int) -> F:
    answer = F(1, 2**(births + 1))
    for n in range(2, births + 3):
        answer /= discount + n
    return answer


def primitive_value_lower(births: int) -> F:
    """The uniform U_N bound for N>=3 and m<=N-1."""
    answer = F(3, 2) / (12 * 2**(births + 1))
    for n in range(3, births + 2):
        answer *= F(2 * n - 1, 2)**2
    for n in range(2, births + 3):
        answer /= 1 + n
    return answer


def root_upper(value: F, degree: int, bits: int = 60) -> F:
    """Dyadic upper bound for a positive rational nth root; integer decisions."""
    value = F(value)
    if value < 0 or degree < 1 or bits < 1:
        raise ValueError("Require x>=0, degree>=1 and bits>=1.")
    if value == 0:
        return F(0)
    scale = 2**bits
    numerator = value.numerator * scale**degree
    denominator = value.denominator
    exponent = max(0, numerator.bit_length() - denominator.bit_length() + 1)
    low, high = 0, 1 << ((exponent + degree - 1) // degree)
    while low + 1 < high:
        middle = (low + high) // 2
        if middle**degree * denominator >= numerator:
            high = middle
        else:
            low = middle
    return F(high, scale)


def potential_second_moment(discount: F, generation: int) -> F:
    s = F(discount)
    return s**(-2 * generation) * sum((s / 2)**j for j in range(generation + 1))


def population_tail_bound(discount: F, generation: int, births: int,
                          dyadic_time: int, bits: int = 60) -> F:
    """Rational upper error for L*, using t=k*log(2) and Cauchy--Schwarz.

The only irrational quantities are rounded upwards by exact integer-root
comparisons, and log(2)<1 bounds the incomplete-gamma polynomial.
"""
    s = F(discount)
    if s <= 0 or generation < 1 or births < 1 or dyadic_time < 1:
        raise ValueError("Require s>0, m>=1, N>=1 and k>=1.")
    k = dyadic_time
    survival = F(1, 2**k)
    exponential = root_upper(F(1, 2**(k * s.numerator)), s.denominator, bits)
    time_tail = s**(-generation) * exponential * sum(
        ((s * k)**j / factorial(j) for j in range(generation)), F(0))
    fast_probability = (1 - survival)**births * (1 + births * survival)
    early_tail = root_upper(potential_second_moment(s, generation) * fast_probability, 2, bits)
    return min(s**(-generation), time_tail + early_tail)


def run_checks(max_births: int = 5):
    counts = Counter()
    def check(condition: bool, category: str):
        require(condition, category)
        counts[category] += 1

    def check_value_error(function, *args):
        try:
            function(*args)
        except ValueError:
            check(True, "invalid_coefficient_inputs_rejected")
        else:
            check(False, "invalid_coefficient_inputs_rejected")

    # A float call must not seed an inexact entry shared with an equal Fraction key.
    population_coefficients.cache_clear()
    float_rewards, _ = population_coefficients(0.5, 1)
    rational_rewards, _ = population_coefficients(F(1, 2), 1)
    for rewards in (float_rewards, rational_rewards):
        check(all(isinstance(value, F) for value in rewards)
              and rewards == (F(0), F(1, 4)), "discount_normalization_keeps_exact_results")
    for discount, births in ((F(-1), 0), (F(0), -1)):
        check_value_error(population_coefficients, discount, births)
    for coefficient in (lower, backward_lower):
        value = coefficient(0.5, 1, 1)
        check(isinstance(value, F) and value == F(1, 4),
              "discount_normalization_keeps_exact_results")
        for args in ((F(-1), 1, 0), (F(-1), 1, 1), (F(0), 0, 0),
                     (F(0), -1, 1), (F(0), 1, -1)):
            check_value_error(coefficient, *args)
        for generation, births in ((1, 0), (4, 3)):
            value = coefficient(F(0), generation, births)
            check(isinstance(value, F) and value == 0,
                  "empty_or_unreachable_generation_is_exact_zero")
    examples = []
    discounts = (F(0), F(1, 2), F(2, 3), F(113, 200), F(3, 2))
    for births in range(1, max_births + 1):
        for generation in range(1, births + 1):
            B, kappa, Q, content, primitive = primitive_form(generation, births)
            degree = len(B) - 1
            K = 1
            for n in range(2, births + 2):
                K *= lcm(*range(1, n + 1))
            check(K % kappa == 0, "minimal_integer_clearer_divides_source_clearer")
            check(all(c >= 0 for c in Q), "reduced_numerator_nonnegative")
            check(gcd(content, kappa) == 1, "content_coprime_to_kappa")
            check((12 * B[-1]) % content == 0, "content_divides_twelve_leading_denominator")
            check(gcd(*primitive) == 1, "primitive_integer_content")
            check(len(primitive) - 1 == degree + 1, "primitive_degree")
            expected_degree = (1 if births == 1 else births*(births+1)//2-1) if generation == 1 else (
                births*(births+1)-generation*(generation-1))//2
            check(degree == expected_degree, "exact_pole_degree")
            derivative = [j * B[j] for j in range(1, len(B))]
            for n, d in pole_pairs(generation, births):
                root = -F(d*n-1, d)
                residue = poly_value(Q, root) / (kappa * poly_value(derivative, root))
                check(residue * (-1)**(n-2) > 0, "simple_pole_residue_sign")
                check(poly_value(primitive, root) != 0, "no_polynomial_gcd_remains")
            for s in discounts:
                value = lower(s, generation, births)
                check(value == backward_lower(s, generation, births), "forward_vs_individual_choice_recursion")
                check(poly_value(Q, s) == kappa * poly_value(B, s) * value, "reduced_rational_identity")
                check(poly_value(primitive, s) * content ==
                      kappa * poly_value(B, s) * (12*(s+3)-value), "primitive_signed_identity")
                check(lower(s, generation, births+1)-value >= omitted_mass(s,generation,births),
                      "omitted_path_present_at_next_population")
                check(omitted_mass(s,generation,births) >= universal_omitted_mass(s,births),
                      "universal_omitted_path_bound")
                if s > 0:
                    rings = generation + 2
                    old = ordered_event_prefix(s,generation,rings,births)
                    check(old <= value <= old+core_ring_tail(s,generation,rings),
                          "null_resummation_vs_finite_ring_prefix")
            if generation == births:
                expected = poly_add(poly_multiply(B,[36,12]),[-1])
                check(kappa == content == 1 and Q == [1] and primitive == expected,
                      "minimal_chain_diagonal")
            if births <= 3:
                examples.append({"m":generation,"N":births,"pole_pairs":pole_pairs(generation,births),
                                 "B":[str(x) for x in B],"kappa":kappa,"Q":[str(x) for x in Q],
                                 "content":content,"primitive_P":[str(x) for x in primitive]})
    check(primitive_value_lower(10) == F(3454132356675,2199023255552)>1,
          "all_large_budget_lower_bound_above_one")
    for n in range(3,30):
        check(primitive_value_lower(n+1)/primitive_value_lower(n)==F(2*n+3,2)**2/(2*(n+4))>1,
              "primitive_lower_bound_increasing")
    for s in (F(1,2),F(2,3),F(113,200),F(3,2)):
        for m in range(1,6):
            check(potential_second_moment(s,m)==s**(-2*m)+potential_second_moment(s,m-1)/(2*s),
                  "potential_second_moment_recursion")
        for degree in (2,s.denominator):
            for x in (F(1,3),F(1,32),F(7,3)):
                bound=root_upper(x,degree,20)
                check(bound**degree >= x and (bound-F(1,2**20))**degree < x,
                      "exact_nth_root_rounding")
        for m in range(1,4):
            bound=population_tail_bound(s,m,3,2)
            check(lower(s,m,7)-lower(s,m,3)<=bound,"population_error_vs_larger_finite_cutoff")
    s=F(113,200); threshold=12*(s+3); product=F(1); total=F(0)
    for n in range(1,489):
        product*=F(n+1)/(n+1+s); previous=total; total+=product
        check(total==((n+2)*product-2)/(1-s),"proper_birth_Yule_envelope_closed_form")
    check(previous<threshold<total,"necessary_population_budget_488")
    return {"status":"PASS","total_checks":sum(counts.values()),"checks":dict(sorted(counts.items())),
            "max_births":max_births,"polynomial_examples":examples,
            "states_through_default_cutoff":population_coefficients(F(1),max_births)[1],
            "necessary_population_budget":{"at_discount":str(s),"threshold":str(threshold),"N_min":488,
                "U_487_lower":outward_decimal(previous,ROUND_FLOOR),
                "U_487_upper":outward_decimal(previous,ROUND_CEILING),
                "U_488_lower":outward_decimal(total,ROUND_FLOOR),
                "U_488_upper":outward_decimal(total,ROUND_CEILING)},
            "scope":"Finite arithmetic audit for population-only full-kernel coefficients and primitive pole/numerator formulas. No new mu bracket or irrationality proof."}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="run the exact finite audit (the default)")
    parser.add_argument("--max-births",type=int,default=5)
    parser.add_argument("--generation", type=int, help="compute one coefficient instead of the default audit")
    parser.add_argument("--s", default="1/2", help="positive rational discount")
    parser.add_argument("--dyadic-time", type=int, default=2, help="use t=k*log(2) in the outer error")
    parser.add_argument("--bits", type=int, default=60, help="dyadic precision of algebraic upper enclosures")
    parser.add_argument("--polynomial", action="store_true", help="include the exact reduced polynomial data")
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    if args.max_births<1: parser.error("--max-births must be positive")
    if args.check or args.generation is None:
        report=run_checks(args.max_births)
    else:
        if not 1 <= args.generation <= args.max_births:
            parser.error("Require 1<=generation<=max-births.")
        discount=F(args.s)
        if discount<=0 or args.dyadic_time<1 or args.bits<1:
            parser.error("Require s>0, dyadic-time>=1 and bits>=1.")
        value=lower(discount,args.generation,args.max_births)
        error=population_tail_bound(discount,args.generation,args.max_births,
                                    args.dyadic_time,args.bits)
        upper=min(discount**(-args.generation),value+error)
        report={"status":"COMPUTED","discount":str(discount),
                "generation":args.generation,"proper_birth_budget":args.max_births,
                "lower":str(value),"upper":str(upper),"error":str(upper-value),
                "tail_time":"%d*log(2)" % args.dyadic_time,
                "states_per_population":population_coefficients(discount,args.max_births)[1],
                "certifies_s_less_than_mu":value>12*(discount+3),
                "scope":"One full inert-generation coefficient enclosure, not an outer approximation of the generation pressure."}
        if args.polynomial:
            B,kappa,Q,content,primitive=primitive_form(args.generation,args.max_births)
            report["polynomial"]={"coefficient_order":"constant term first",
                                  "pole_pairs":pole_pairs(args.generation,args.max_births),
                                  "B":B,"kappa":kappa,"Q":Q,"content":content,
                                  "primitive_P":primitive}
    serialized=json.dumps(report,indent=2)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(serialized)
    print(serialized,end="")


if __name__=="__main__":
    main()
