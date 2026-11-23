#!/usr/bin/env python3
"""Certified rational coefficients of the inert-parent friend-tree process.

Compute a positive finite approximation to A_m^infinity(s), the expected
discounted number of future generation-m core births from a newborn tag
with one leaf and an inert parent. A root clock choosing the inert parent
is a NULL event: it still counts toward the core-ring budget.

Leaf-clock waiting is integrated exactly by the beta/Pólya burst law in
core_clock_kernel.py. The two finite budgets are:
  * core_rings: all core clock rings, including null/nonpromotion rings;
  * max_births: real vertex arrivals after the initial two real vertices.

The error combines a universal potential-genealogy ring tail with an
explicit reward bound for each history discarded at the birth budget.
Every coefficient and error bound uses fractions.Fraction. No finite
matrix eigenvalue or effective outer-generation convergence is assumed.

Examples:
    python3 inert_growth_kernel.py --check
    python3 inert_growth_kernel.py --s 1/2 --generation 2 --core-rings 3 --max-births 4
    python3 inert_growth_kernel.py --s 1 --generation 1 --core-rings 6 --max-births 8
    python3 inert_growth_kernel.py --s 1/2 --search --max-stage 3

The uniform inert minorization proved in the companion argument implies
that lower > 12*(s+3) certifies s < mu. This program reports that test;
the default small computation is only a demonstration, not a new bound.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction as F
from functools import lru_cache

from core_clock_kernel import CoreState, one_core_ring


INERT_INITIAL = CoreState((), (1,), (1,))


@lru_cache(maxsize=None)
def core_depths(state: CoreState) -> tuple[int, ...]:
    """Genealogical depths, with the original tag at vertex zero."""
    adjacency = state.neighbors()
    depths = [-1] * state.k
    depths[0] = 0
    pending = [0]
    for vertex in pending:
        for neighbor in adjacency[vertex]:
            if depths[neighbor] < 0:
                depths[neighbor] = depths[vertex] + 1
                pending.append(neighbor)
    return tuple(depths)


@lru_cache(maxsize=None)
def canonical_state(state: CoreState) -> CoreState:
    """Root-preserving isomorphism reduction; leaf labels are irrelevant."""
    adjacency = state.neighbors()

    def encode(vertex: int, parent: int):
        children = [encode(j, vertex) for j in adjacency[vertex] if j != parent]
        return state.leaves[vertex], state.stubs[vertex], tuple(sorted(children))

    leaves, stubs, edges = [], [], []

    def decode(node, parent: int | None) -> None:
        vertex = len(leaves)
        leaves.append(node[0])
        stubs.append(node[1])
        if parent is not None:
            edges.append((parent, vertex))
        for child in node[2]:
            decode(child, vertex)

    decode(encode(0, -1), None)
    return CoreState(tuple(edges), tuple(leaves), tuple(stubs))


def potential_profile(core_rings: int, max_degree: int) -> tuple[F, ...]:
    """Coefficients through max_degree of prod_{i=1}^R (1+z/i)."""
    if core_rings < 0 or max_degree < 0:
        raise ValueError("Budgets and polynomial degree must be nonnegative.")
    coefficients = [F(1)] + [F()] * max_degree
    for population in range(1, core_rings + 1):
        for degree in range(min(population, max_degree), 0, -1):
            coefficients[degree] += coefficients[degree - 1] / population
    return tuple(coefficients)


def core_ring_tail(s: F, generation: int, core_rings: int) -> F:
    """Universal discounted reward after R actual core-clock rings."""
    if s <= 0 or generation < 1 or core_rings < 0:
        raise ValueError("Require s>0, generation>=1, and core_rings>=0.")
    clock_transform = F(1)
    for population in range(1, core_rings + 1):
        clock_transform *= F(population) / (population + s)
    profile = potential_profile(core_rings, generation - 1)
    return clock_transform * sum(
        (coefficient / s ** (generation - depth)
         for depth, coefficient in enumerate(profile)), F()
    )


@lru_cache(maxsize=None)
def future_generation_bound(state: CoreState, s: F, generation: int) -> F:
    """Future generation-m reward from each currently existing core.

Each existing node starts only its NEW future branches, so descendants
of already existing children are not counted twice.
"""
    return sum((F(1) / s ** (generation - depth)
                for depth in core_depths(state) if depth < generation), F())


@dataclass(frozen=True)
class InertCoefficientApproximation:
    s: F
    generation: int
    core_rings: int
    max_births: int
    lower: F
    birth_error: F
    ring_error: F
    states_per_layer: tuple[int, ...]

    @property
    def raw_error(self) -> F:
        return self.birth_error + self.ring_error

    @property
    def upper(self) -> F:
        return min(self.lower + self.raw_error, F(1) / self.s ** self.generation)

    @property
    def error(self) -> F:
        return self.upper - self.lower

    @property
    def certificate_threshold(self) -> F:
        return 12 * (self.s + 3)

    @property
    def certifies_s_less_than_mu(self) -> bool:
        return self.lower > self.certificate_threshold


def inert_coefficient(s: F, generation: int, core_rings: int,
                      max_births: int) -> InertCoefficientApproximation:
    """Exact burst BFS and a rigorous upper error for A_m^infinity(s)."""
    if s <= 0 or generation < 1 or core_rings < 0 or max_births < 0:
        raise ValueError("Require s>0, generation>=1, and nonnegative budgets.")
    population_limit = 2 + max_births
    current = {INERT_INITIAL: F(1)}
    layers = [1]
    lower, birth_error = F(), F()
    largest_new_core_reward = max(F(1) / s ** j for j in range(generation))

    for _ in range(core_rings):
        following: dict[CoreState, F] = defaultdict(F)
        for old, history_weight in current.items():
            population = old.k + sum(old.leaves)
            max_added = population_limit - population
            if max_added < 0:
                raise AssertionError("Retained state exceeded its birth budget.")
            failures, promotions, omitted_ring_mass = one_core_ring(old, s, max_added)

            # Before the omitted forced core ring, only leaves are added.
            # Its graph/depth profile is unchanged. The ring can add at
            # most one new core or one immediate target-generation reward.
            birth_error += history_weight * omitted_ring_mass * (
                future_generation_bound(old, s, generation) + largest_new_core_reward
            )

            for new, transition_weight in failures.items():
                weight = history_weight * transition_weight
                if new.k + sum(new.leaves) > population_limit:
                    birth_error += weight * future_generation_bound(new, s, generation)
                else:
                    following[canonical_state(new)] += weight

            for new, transition_weight in promotions.items():
                weight = history_weight * transition_weight
                # one_core_ring appends the newly promoted core last.
                reward = F(int(core_depths(new)[old.k] == generation))
                if new.k + sum(new.leaves) > population_limit:
                    birth_error += weight * (
                        reward + future_generation_bound(new, s, generation)
                    )
                else:
                    lower += weight * reward
                    following[canonical_state(new)] += weight

        current = dict(following)
        layers.append(len(current))

    result = InertCoefficientApproximation(
        s, generation, core_rings, max_births, lower, birth_error,
        core_ring_tail(s, generation, core_rings), tuple(layers)
    )
    if result.lower > F(1) / s ** generation or result.error < 0:
        raise AssertionError("Lower approximation exceeded the potential-genealogy bound.")
    return result


def ordered_event_prefix(s: F, generation: int, core_rings: int,
                         max_births: int) -> F:
    """Independent audit by ordered leaf/core clock events, without beta bursts.

The next individual clock attempt has total rate n, including silent
stub choices. A leaf event uses one birth; a core event uses one ring
and, unless silent, one birth. Thus the recursion is finite.
"""
    @lru_cache(maxsize=None)
    def visit(state: CoreState, rings_left: int, births_left: int) -> F:
        if rings_left == 0:
            return F()
        population = state.k + sum(state.leaves)
        denominator = population + s
        answer = F()
        depths, degrees = core_depths(state), state.degrees()
        if births_left:
            for target, leaf_count in enumerate(state.leaves):
                if leaf_count:
                    answer += F(leaf_count) / denominator * visit(
                        state.add_leaf(target), rings_left, births_left - 1
                    )
        for source, degree in enumerate(degrees):
            if births_left:
                for target in state.neighbors()[source]:
                    answer += F(1, degree) / denominator * visit(
                        state.add_leaf(target), rings_left - 1, births_left - 1
                    )
                if state.leaves[source]:
                    reward = F(int(depths[source] + 1 == generation))
                    answer += F(state.leaves[source], degree) / denominator * (
                        reward + visit(state.promote(source), rings_left - 1, births_left - 1)
                    )
            if state.stubs[source]:
                answer += F(state.stubs[source], degree) / denominator * visit(
                    state, rings_left - 1, births_left
                )
        return answer

    return visit(INERT_INITIAL, core_rings, max_births)


def run_checks() -> dict[str, object]:
    comparisons = 0
    discounts = (F(1, 2), F(1), F(2, 3))
    for s in discounts:
        for generation in (1, 2, 3):
            for rings in range(4):
                for births in range(5):
                    estimate = inert_coefficient(s, generation, rings, births)
                    ordered = ordered_event_prefix(s, generation, rings, births)
                    assert estimate.lower == ordered
                    comparisons += 1
            previous_tail = F(1) / s ** generation
            for rings in range(21):
                tail = core_ring_tail(s, generation, rings)
                assert F() <= tail <= previous_tail
                if rings < generation:
                    assert tail == F(1) / s ** generation
                previous_tail = tail

    for rings in range(21):
        assert core_ring_tail(F(1), 1, rings) == F(1, rings + 1)
        harmonic = sum((F(1, i) for i in range(1, rings + 1)), F())
        assert core_ring_tail(F(1), 2, rings) == (1 + harmonic) / (rings + 1)

    for births in range(7):
        first = inert_coefficient(F(1), 1, 1, births)
        expected = sum((F(2, (m + 1) ** 2 * (m + 2))
                        for m in range(1, births + 1)), F())
        assert first.lower == expected

    for s in discounts:
        null_or_bud = F(1) / (2 * (s + 2))
        for rings in range(21):
            one_birth = inert_coefficient(s, 1, rings, 1)
            assert one_birth.lower == (1 - null_or_bud ** rings) / (2 * s + 3)

    for generation in (1, 2):
        larger = inert_coefficient(F(1, 2), generation, 4, 6)
        for rings in range(4):
            for births in range(5):
                smaller = inert_coefficient(F(1, 2), generation, rings, births)
                assert smaller.lower <= larger.lower <= smaller.upper

    return {
        "status": "PASS",
        "ordered_event_comparisons": comparisons,
        "checks": [
            "burst BFS versus individual-clock recursion",
            "null rings counted without consuming a real birth",
            "potential generation-profile and exact ring-tail identities",
            "one-ring scalar partial sums",
            "one-birth null-chain identity for every tested ring budget",
            "nested positive approximations and certified intervals",
        ],
        "scope": "Finite identities and tail bounds; no new numerical exponent bracket.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--search", action="store_true",
                        help="Enumerate scalar lower tests; potentially very expensive.")
    parser.add_argument("--max-stage", type=int, default=0,
                        help="Search limit; zero means unbounded, with no termination for s>=mu.")
    parser.add_argument("--s", default="1/2")
    parser.add_argument("--generation", type=int, default=2)
    parser.add_argument("--core-rings", type=int, default=3)
    parser.add_argument("--max-births", type=int, default=4)
    args = parser.parse_args()
    if args.check:
        print(json.dumps(run_checks(), indent=2))
        return
    if args.search:
        s = F(args.s)
        if s <= 0 or args.max_stage < 0:
            parser.error("Search requires s>0 and max-stage>=0.")
        stage = 1
        while args.max_stage == 0 or stage <= args.max_stage:
            for generation in range(1, stage + 1):
                result = inert_coefficient(s, generation, stage, stage)
                if result.certifies_s_less_than_mu:
                    print(json.dumps({
                        "status": "CERTIFIED_S_LESS_THAN_MU",
                        "discount_s": str(s),
                        "generation": generation,
                        "core_ring_budget_including_nulls": stage,
                        "real_birth_budget": stage,
                        "lower": str(result.lower),
                        "strict_threshold": str(result.certificate_threshold),
                    }, indent=2))
                    return
            print(json.dumps({"completed_stage": stage, "certificate_found": False}), flush=True)
            stage += 1
        print(json.dumps({
            "status": "NO_CERTIFICATE_WITHIN_FINITE_BUDGET",
            "meaning": "No conclusion about the sign of s-mu.",
        }, indent=2))
        return
    result = inert_coefficient(F(args.s), args.generation, args.core_rings, args.max_births)
    report = {
        "discount_s": str(result.s),
        "generation": result.generation,
        "core_ring_budget_including_nulls": result.core_rings,
        "real_birth_budget": result.max_births,
        "lower": str(result.lower),
        "upper": str(result.upper),
        "lower_decimal": float(result.lower),
        "upper_decimal": float(result.upper),
        "birth_budget_error": str(result.birth_error),
        "core_ring_error": str(result.ring_error),
        "states_per_layer": result.states_per_layer,
        "lower_certificate_threshold": str(result.certificate_threshold),
        "certifies_s_less_than_mu": result.certifies_s_less_than_mu,
    }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
