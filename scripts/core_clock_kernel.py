#!/usr/bin/env python3
"""Exact core-clock kernels for the original random friend tree.

All retained weights and missing-mass bounds use fractions.Fraction.
Between core-clock rings, the leaf counts are independent Yule processes.
This module integrates those waiting events exactly, then sums a finite
number of nonpromotion core rings. It does not approximate the exponent
by a finite-matrix eigenvalue or claim an outer-generation error bound.

Examples:
    python3 core_clock_kernel.py --check
    python3 core_clock_kernel.py --s 1/2 --core-rings 4 --max-added 5
    python3 core_clock_kernel.py --s 1/2 --core-rings 1 --relative-base 2

The default initial state is an edge core with one leaf at each endpoint.
An inert boundary stub counts in a vertex's degree, receives outgoing
core-clock choices silently, and sends no incoming events. Stubs are used
for the controlled environment approximations in the companion note.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction as F
from math import comb, factorial
from typing import Iterator


def rising(x: int | F, n: int) -> F:
    value = F(1)
    for j in range(n):
        value *= x + j
    return value


@dataclass(frozen=True)
class CoreState:
    """A labelled active core tree, leaf counts, and inert boundary counts."""

    edges: tuple[tuple[int, int], ...]
    leaves: tuple[int, ...]
    stubs: tuple[int, ...] = ()

    def __post_init__(self) -> None:
        k = len(self.leaves)
        if not self.stubs:
            object.__setattr__(self, "stubs", (0,) * k)
        if k < 1 or len(self.stubs) != k:
            raise ValueError("Need at least one core vertex and matching stubs.")
        if any(v < 0 for v in self.leaves + self.stubs):
            raise ValueError("Counts must be nonnegative.")
        if len(self.edges) != k - 1 or len(set(self.edges)) != k - 1:
            raise ValueError("Active core must have k-1 distinct edges.")
        if any(not 0 <= i < j < k for i, j in self.edges):
            raise ValueError("Edges must satisfy 0 <= i < j < k.")
        adj = self.neighbors()
        seen, pending = {0}, [0]
        while pending:
            for j in adj[pending.pop()]:
                if j not in seen:
                    seen.add(j)
                    pending.append(j)
        if len(seen) != k or any(d < 2 for d in self.degrees()):
            raise ValueError("Need a connected core and full degrees at least 2.")

    @property
    def k(self) -> int:
        return len(self.leaves)

    def neighbors(self) -> tuple[tuple[int, ...], ...]:
        adj: list[list[int]] = [[] for _ in self.leaves]
        for i, j in self.edges:
            adj[i].append(j)
            adj[j].append(i)
        return tuple(tuple(row) for row in adj)

    def core_degrees(self) -> tuple[int, ...]:
        return tuple(len(row) + b for row, b in zip(self.neighbors(), self.stubs))

    def degrees(self) -> tuple[int, ...]:
        return tuple(l + c for l, c in zip(self.leaves, self.core_degrees()))

    def promotion_rate(self) -> F:
        return sum((F(l, d) for l, d in zip(self.leaves, self.degrees())), F())

    def with_leaves(self, leaves: tuple[int, ...]) -> CoreState:
        return CoreState(self.edges, leaves, self.stubs)

    def add_leaf(self, target: int) -> CoreState:
        leaves = list(self.leaves)
        leaves[target] += 1
        return self.with_leaves(tuple(leaves))

    def promote(self, parent: int) -> CoreState:
        if self.leaves[parent] == 0:
            raise ValueError("Cannot promote a nonexistent leaf.")
        leaves = list(self.leaves)
        leaves[parent] -= 1
        leaves.append(1)
        return CoreState(self.edges + ((parent, self.k),), tuple(leaves), self.stubs + (0,))


def allocations(leaves: tuple[int, ...], extra: int) -> Iterator[tuple[int, ...]]:
    """Added leaves; initially zero Yule families remain zero."""
    current = [0] * len(leaves)
    active = [i for i, l in enumerate(leaves) if l]

    def visit(position: int, remaining: int) -> Iterator[tuple[int, ...]]:
        if position == len(active):
            if remaining == 0:
                yield tuple(current)
            return
        i = active[position]
        for count in range(remaining + 1):
            current[i] = count
            yield from visit(position + 1, remaining - count)
        current[i] = 0

    yield from visit(0, extra)


def burst_weight(leaves: tuple[int, ...], added: tuple[int, ...], alpha: F) -> F:
    """Resolvent weight for one specified core-clock index.

    Product binomial coefficients times Beta(alpha+sum(leaves), sum(added)+1).
    The sum over all added vectors is 1/alpha, not one.
    """
    if len(leaves) != len(added) or any(m < 0 for m in added):
        raise ValueError("Invalid added-leaf vector.")
    coefficient = 1
    for l, m in zip(leaves, added):
        if l == 0:
            if m:
                return F()
        else:
            coefficient *= comb(l + m - 1, m)
    j = sum(added)
    return F(coefficient * factorial(j)) / rising(alpha + sum(leaves), j + 1)


def burst_tail(leaf_total: int, alpha: F, first_omitted_extra: int) -> F:
    """Normalized Exp(alpha)-time Yule tail for added count >= cutoff."""
    if first_omitted_extra < 0:
        raise ValueError("Cutoff must be nonnegative.")
    return rising(leaf_total, first_omitted_extra) / rising(alpha + leaf_total, first_omitted_extra)


def one_core_ring(state: CoreState, s: F, max_added: int):
    """Retained nonpromotion/promotion measures and exact omitted ring mass."""
    if s < 0 or max_added < 0:
        raise ValueError("Need nonnegative s and max_added.")
    alpha = state.k + s
    failures: dict[CoreState, F] = defaultdict(F)
    successes: dict[CoreState, F] = defaultdict(F)
    neighbors = state.neighbors()
    for extra in range(max_added + 1):
        for added in allocations(state.leaves, extra):
            weight = burst_weight(state.leaves, added, alpha)
            middle = state.with_leaves(tuple(l + m for l, m in zip(state.leaves, added)))
            for source, degree in enumerate(middle.degrees()):
                if middle.leaves[source]:
                    successes[middle.promote(source)] += weight * F(middle.leaves[source], degree)
                for target in neighbors[source]:
                    failures[middle.add_leaf(target)] += weight / degree
                if middle.stubs[source]:
                    failures[middle] += weight * F(middle.stubs[source], degree)
    omitted = F(state.k) / alpha * burst_tail(sum(state.leaves), alpha, max_added + 1)
    return dict(failures), dict(successes), omitted


@dataclass
class PromotionApproximation:
    output: dict[CoreState, F]
    lost_burst_mass: F
    unfinished_mass: F
    remaining_state_count: int

    @property
    def mass(self) -> F:
        return sum(self.output.values(), F())

    @property
    def error(self) -> F:
        return self.lost_burst_mass + self.unfinished_mass


def first_promotion(state: CoreState, s: F, core_rings: int,
                    max_added: int = 5, relative_base: int | None = None) -> PromotionApproximation:
    """Positive finite approximation; error bounds missing kernel mass.

    If relative_base=p is provided, A=p**denominator(s) and every burst
    retains total leaf count < ceil(A*(current_total+k+s)). This implements
    the uniform rational truncation theorem. Otherwise max_added is fixed;
    the reported adaptive error is still a rigorous rational mass bound.
    """
    if core_rings < 1 or s < 0 or (relative_base is not None and relative_base < 2):
        raise ValueError("Invalid discount or truncation parameters.")
    current = {state: F(1)}
    output: dict[CoreState, F] = defaultdict(F)
    lost = F()
    for _ in range(core_rings):
        following: dict[CoreState, F] = defaultdict(F)
        for old, probability in current.items():
            cutoff = max_added
            if relative_base is not None:
                boundary = relative_base ** s.denominator * (sum(old.leaves) + old.k + s)
                n = -(-boundary.numerator // boundary.denominator)
                cutoff = n - sum(old.leaves) - 1
            failures, successes, omitted = one_core_ring(old, s, cutoff)
            lost += probability * omitted
            for new, weight in failures.items():
                following[new] += probability * weight
            for new, weight in successes.items():
                output[new] += probability * weight
        current = dict(following)
    return PromotionApproximation(dict(output), lost, sum(current.values(), F()), len(current))


def relative_error_bound(state: CoreState, s: F, core_rings: int, base: int) -> F:
    b0 = state.promotion_rate()
    if s + b0 <= 0 or base < 2:
        raise ValueError("Need s+b0>0 and base>=2.")
    q0 = (state.k - b0) / (state.k + s)
    exponent = state.k * s.denominator + s.numerator
    return q0 ** core_rings + F(state.k, base ** exponent) / (s + b0)


Profile = tuple[int, int, tuple]


def project_environment(state: CoreState, tag: int, radius: int, degree_cut: int) -> Profile:
    """Canonical finite initial profile with inert edges at both cutoffs.

    Each node is (leaf_count, inert_stub_count, sorted_child_profiles).
    The distinguished tag becomes the root. Require a newborn tag.
    """
    if radius < 1 or degree_cut < 3:
        raise ValueError("Require radius>=1 and degree_cut>=3.")
    if state.leaves[tag] != 1 or state.core_degrees()[tag] != 1:
        raise ValueError("The projection is defined here for newborn tags.")
    adj, degrees = state.neighbors(), state.degrees()

    def descend(i: int, parent: int, depth: int) -> Profile:
        stubs = state.stubs[i]
        children = []
        for j in adj[i]:
            if j == parent:
                continue
            if depth + 1 >= radius or degrees[j] >= degree_cut:
                stubs += 1
            else:
                children.append(descend(j, i, depth + 1))
        return state.leaves[i], stubs, tuple(sorted(children))

    return descend(tag, -1, 0)


def materialize_profile(profile: Profile) -> CoreState:
    leaves, stubs, edges = [], [], []

    def descend(node: Profile, parent: int | None) -> None:
        index = len(leaves)
        leaves.append(node[0])
        stubs.append(node[1])
        if parent is not None:
            edges.append((parent, index))
        for child in node[2]:
            descend(child, index)

    descend(profile, None)
    return CoreState(tuple(edges), tuple(leaves), tuple(stubs))


def tagged_profile_row(state: CoreState, s: F, radius: int, degree_cut: int,
                       max_population: int) -> tuple[dict[Profile, F], F]:
    """Approximate a row of the finite profile transfer matrix.

    The tag is vertex zero. Every future child of that tag is rewarded,
    with its state projected immediately after its birth. All intervening
    evolution is retained through the given active-population cutoff.
    Silent events at inert stubs are summed by the holding-time denominator.
    Returns a positive rational row and a rational upper bound on missing
    row mass. This computes selected rows, not all finite profile types.
    """
    n0 = state.k + sum(state.leaves)
    if s <= 0 or max_population < n0:
        raise ValueError("Require s>0 and max_population>=initial population.")
    current = {state: F(1)}
    row: dict[Profile, F] = defaultdict(F)
    for population in range(n0, max_population):
        following: dict[CoreState, F] = defaultdict(F)
        for old, probability in current.items():
            degrees, neighbors = old.degrees(), old.neighbors()
            silent = sum((F(b, d) for b, d in zip(old.stubs, degrees)), F())
            denominator = population - silent + s
            for target in range(old.k):
                gain = old.leaves[target] + sum((F(1, degrees[j]) for j in neighbors[target]), F())
                if gain:
                    following[old.add_leaf(target)] += probability * gain / denominator
                if old.leaves[target]:
                    new = old.promote(target)
                    weight = probability * F(old.leaves[target], degrees[target]) / denominator
                    following[new] += weight
                    if target == 0:
                        profile = project_environment(new, old.k, radius, degree_cut)
                        row[profile] += weight
        current = dict(following)
    tail = F(1) / s
    for population in range(n0, max_population):
        tail *= F(population) / (population + s)
    return dict(row), tail


def explicit_leaf_paths(leaves: tuple[int, ...], alpha: F, extra: int):
    """Independent micro-event recursion up to the first core ring."""
    rows = {leaves: F(1)}
    for _ in range(extra):
        following: dict[tuple[int, ...], F] = defaultdict(F)
        for counts, weight in rows.items():
            for i, count in enumerate(counts):
                if count:
                    new = list(counts)
                    new[i] += 1
                    following[tuple(new)] += weight * count / (sum(counts) + alpha)
        rows = dict(following)
    return {counts: weight / (sum(counts) + alpha) for counts, weight in rows.items()}


def expanded_tree(state: CoreState) -> list[set[int]]:
    if any(state.stubs):
        raise ValueError("Expanded-tree audit only applies without stubs.")
    adjacency = [set(row) for row in state.neighbors()]
    for i, leaves in enumerate(state.leaves):
        for _ in range(leaves):
            j = len(adjacency)
            adjacency.append({i})
            adjacency[i].add(j)
    return adjacency


def full_tree_promotion_rate(adjacency: list[set[int]]) -> F:
    return sum((F(sum(len(adjacency[j]) == 1 for j in row), len(row))
                for row in adjacency if len(row) >= 2), F())


def full_tree_generator_b(state: CoreState) -> F:
    """Enumerate every source/neighbor choice in the original full tree."""
    adjacency = expanded_tree(state)
    before = full_tree_promotion_rate(adjacency)
    value = F()
    for row in adjacency:
        for target in row:
            after = [set(neighbors) for neighbors in adjacency]
            after[target].add(len(after))
            after.append({target})
            value += (full_tree_promotion_rate(after) - before) / len(row)
    return value


def run_checks() -> dict[str, object]:
    checked = 0
    for leaves in [(2,), (1, 1), (1, 0, 2), (2, 1, 1)]:
        for s in [F(), F(1, 2), F(7, 5)]:
            alpha = len(leaves) + s
            total = F()
            for extra in range(5):
                direct = explicit_leaf_paths(leaves, alpha, extra)
                for counts, value in direct.items():
                    added = tuple(n - l for n, l in zip(counts, leaves))
                    assert value == burst_weight(leaves, added, alpha)
                    checked += 1
                subtotal = sum(direct.values(), F())
                assert subtotal == rising(sum(leaves), extra) / rising(alpha + sum(leaves), extra + 1)
                total += subtotal
            assert total + burst_tail(sum(leaves), alpha, 5) / alpha == 1 / alpha
    edge = CoreState(((0, 1),), (1, 1))
    star = CoreState((), (2,))
    inert = CoreState((), (1,), (1,))
    for state in (edge, star, inert):
        for s in (F(), F(1, 2), F(2)):
            failures, successes, tail = one_core_ring(state, s, 4)
            assert sum(failures.values(), F()) + sum(successes.values(), F()) + tail == F(state.k) / (state.k + s)
    for n in range(2, 9):
        assert burst_weight((2,), (n - 2,), F(1)) == F(2, n * (n + 1))
    small = first_promotion(edge, F(1, 2), 2, 2)
    large = first_promotion(edge, F(1, 2), 3, 3)
    assert small.mass <= large.mass <= small.mass + small.error
    undiscounted = first_promotion(edge, F(), 3, 3)
    assert undiscounted.mass + undiscounted.error == 1
    relative = first_promotion(edge, F(1, 2), 1, relative_base=2)
    assert relative.error <= relative_error_bound(edge, F(1, 2), 1, 2)
    path = ((0, 1), (1, 2), (2, 3), (3, 4))
    first = CoreState(path, (1, 0, 1, 0, 1))
    second = CoreState(path, (1, 1, 0, 0, 1))
    assert Counter(zip(first.leaves, first.core_degrees())) == Counter(zip(second.leaves, second.core_degrees()))
    assert first.promotion_rate() == second.promotion_rate() == F(4, 3)
    assert full_tree_generator_b(first) == F(13, 9)
    assert full_tree_generator_b(second) == F(53, 36)
    for radius in (1, 2, 3):
        for cutoff in (3, 4, 6):
            profile = project_environment(edge, 0, radius, cutoff)
            assert project_environment(materialize_profile(profile), 0, radius, cutoff) == profile
    assert project_environment(edge, 0, 1, 3) == (1, 1, ())
    profile_row, row_tail = tagged_profile_row(star, F(1, 2), 2, 5, 5)
    assert sum(profile_row.values(), F()) == F(4, 9)
    assert row_tail == F(32, 21)
    stub_row, stub_tail = tagged_profile_row(inert, F(1), 1, 3, 3)
    assert stub_row == {(1, 1, ()): F(1, 5)}
    assert stub_tail == F(2, 3)
    return {"status": "PASS", "exact_burst_entry_comparisons": checked,
            "checks": ["ordered leaf histories", "Pólya allocation and exact tail",
                       "core-ring mass conservation including inert stubs", "star law",
                       "positive promotion truncations", "rational error bound",
                       "non-lumpability from original full-tree generator",
                       "finite-profile projection idempotence",
                       "tagged transfer rows including inert holding times"],
            "scope": "Finite identities and bounds; no numerical exponent certificate."}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--s", default="1/2")
    parser.add_argument("--core-rings", type=int, default=4)
    parser.add_argument("--max-added", type=int, default=5)
    parser.add_argument("--relative-base", type=int)
    args = parser.parse_args()
    if args.check:
        print(json.dumps(run_checks(), indent=2))
        return
    state = CoreState(((0, 1),), (1, 1))
    s = F(args.s)
    result = first_promotion(state, s, args.core_rings, args.max_added, args.relative_base)
    report = {"s": str(s), "core_rings": args.core_rings,
              "retained_output_states": len(result.output),
              "retained_discounted_mass": str(result.mass),
              "retained_mass_decimal": float(result.mass),
              "certified_missing_mass_bound": str(result.error),
              "missing_mass_bound_decimal": float(result.error),
              "unfinished_states": result.remaining_state_count}
    if args.relative_base:
        report["uniform_relative_cutoff_bound"] = str(relative_error_bound(state, s, args.core_rings, args.relative_base))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
