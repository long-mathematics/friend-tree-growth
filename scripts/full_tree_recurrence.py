#!/usr/bin/env python3
"""Exact finite coefficients and drift identities for the original free tree.

Start from one edge, with no inert stub. Trees are merged by an unlabelled
canonical code: the minimum, over all roots, of their nested rooted tuples.
Every attachment target is still counted, including targets with the same
canonical outcome. Thus all transition multiplicities are retained.

The program computes a_n=E C_n and b_n=E Lambda(T_n), where C is the number
of nonleaves and Lambda=sum_{leaf w} sum_{u~w} 1/d(u). It checks
n*(a_{n+1}-a_n)=b_n and a per-state Lambda drift identity. The latter
involves further observables K and J and does not close a scalar recurrence.

Examples:
  python3 scripts/full_tree_recurrence.py --check
  python3 scripts/full_tree_recurrence.py --max-population 9
  python3 scripts/full_tree_recurrence.py --check --output build/verification/full_tree_recurrence_checks.json

This is an exploratory exact coefficient calculator, not a solver for mu.
All arithmetic decisions are exact. Files are written only with --output.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction as F
from functools import lru_cache
import json
from pathlib import Path


TreeCode = tuple["TreeCode", ...]
Adjacency = tuple[tuple[int, ...], ...]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


@lru_cache(maxsize=None)
def canonical_tree(adjacency: Adjacency) -> TreeCode:
    """Minimum rooted nested-tuple encoding over every possible root."""
    if not adjacency:
        raise ValueError("A tree must contain a vertex.")

    def encode(vertex: int, parent: int) -> TreeCode:
        return tuple(sorted(encode(neighbor, vertex)
                            for neighbor in adjacency[vertex] if neighbor != parent))

    return min(encode(root, -1) for root in range(len(adjacency)))


@lru_cache(maxsize=None)
def adjacency_from_code(code: TreeCode) -> Adjacency:
    neighbors: list[list[int]] = []

    def add(subtree: TreeCode, parent: int | None) -> None:
        vertex = len(neighbors)
        neighbors.append([])
        if parent is not None:
            neighbors[vertex].append(parent)
            neighbors[parent].append(vertex)
        for child in subtree:
            add(child, vertex)

    add(code, None)
    return tuple(tuple(sorted(row)) for row in neighbors)


def code_text(code: TreeCode) -> str:
    return "(" + "".join(code_text(child) for child in code) + ")"


@lru_cache(maxsize=None)
def attach_leaf(code: TreeCode, target: int) -> TreeCode:
    adjacency = adjacency_from_code(code)
    new_vertex = len(adjacency)
    rows = [list(row) for row in adjacency]
    rows[target].append(new_vertex)
    rows.append([target])
    return canonical_tree(tuple(tuple(row) for row in rows))


@dataclass(frozen=True)
class Observables:
    population: int
    cores: int
    lam: F
    k: F
    j: F
    h: tuple[F, ...]
    leaf_neighbors: tuple[int, ...]


@lru_cache(maxsize=None)
def observables(code: TreeCode) -> Observables:
    adjacency = adjacency_from_code(code)
    degrees = tuple(len(row) for row in adjacency)
    if len(adjacency) < 2:
        raise ValueError("The free friend-tree process starts with at least an edge.")
    h = tuple(sum((F(1, degrees[source]) for source in row), F(0))
              for row in adjacency)
    leaves = tuple(sum(degrees[neighbor] == 1 for neighbor in row) for row in adjacency)
    cores = sum(degree >= 2 for degree in degrees)
    lam = sum((h[vertex] for vertex, degree in enumerate(degrees) if degree == 1), F(0))
    k = sum((F(leaves[vertex], degree**2)
             for vertex, degree in enumerate(degrees) if degree >= 2), F(0))
    j = sum((h[vertex] * F(degree - leaves[vertex], degree * (degree + 1))
             for vertex, degree in enumerate(degrees) if degree >= 2), F(0))
    return Observables(len(adjacency), cores, lam, k, j, h, leaves)


@lru_cache(maxsize=None)
def attachment_transitions(code: TreeCode) -> tuple[tuple[TreeCode, F], ...]:
    """Aggregate h_T(w)/n, retaining every target-vertex multiplicity."""
    values = observables(code)
    transitions: dict[TreeCode, F] = defaultdict(F)
    for target, rate in enumerate(values.h):
        transitions[attach_leaf(code, target)] += rate / values.population
    return tuple(sorted(transitions.items()))


def two_stage_transitions(code: TreeCode) -> dict[TreeCode, F]:
    """Independent direct source/neighbor choices, without using h_T."""
    adjacency = adjacency_from_code(code)
    n = len(adjacency)
    transitions: dict[TreeCode, F] = defaultdict(F)
    for neighbors in adjacency:
        choice = F(1, n * len(neighbors))
        for target in neighbors:
            transitions[attach_leaf(code, target)] += choice
    return dict(transitions)


def double_star(first_leaves: int, second_leaves: int) -> TreeCode:
    if first_leaves < 1 or second_leaves < 1:
        raise ValueError("Both double-star core vertices must have leaves.")
    neighbors: list[list[int]] = [[1], [0]]
    for parent, count in ((0, first_leaves), (1, second_leaves)):
        for _ in range(count):
            vertex = len(neighbors)
            neighbors[parent].append(vertex)
            neighbors.append([parent])
    return canonical_tree(tuple(tuple(row) for row in neighbors))


def star(population: int) -> TreeCode:
    return canonical_tree((tuple(range(1, population)),
                           *(tuple([0]) for _ in range(population - 1))))


def compute(max_population: int, audit: bool) -> dict[str, object]:
    if max_population < 3:
        raise ValueError("--max-population must be at least 3.")
    counts: Counter[str] = Counter()

    def check(condition: bool, category: str) -> None:
        require(condition, category)
        counts[category] += 1

    edge = canonical_tree(((1,), (0,)))
    distribution: dict[TreeCode, F] = {edge: F(1)}
    rows = []
    moments: dict[int, tuple[F, F, F, F]] = {}
    initial_distributions: dict[int, dict[TreeCode, F]] = {}
    per_state_audits = 0

    for n in range(2, max_population + 1):
        mass = sum(distribution.values(), F(0))
        require(mass == 1, "tree distribution must have total mass one")
        if audit:
            check(all(weight > 0 for weight in distribution.values()), "positive_tree_weights")
            counts["distribution_normalization"] += 1
        a_n = sum((weight * observables(code).cores for code, weight in distribution.items()), F(0))
        b_n = sum((weight * observables(code).lam for code, weight in distribution.items()), F(0))
        k_n = sum((weight * observables(code).k for code, weight in distribution.items()), F(0))
        j_n = sum((weight * observables(code).j for code, weight in distribution.items()), F(0))
        moments[n] = a_n, b_n, k_n, j_n
        rows.append({"population": n, "unlabelled_tree_states": len(distribution),
                     "a_n_expected_cores": str(a_n), "b_n_expected_Lambda": str(b_n),
                     "expected_K": str(k_n), "expected_J": str(j_n)})
        if n <= 5:
            initial_distributions[n] = dict(distribution)

        following: dict[TreeCode, F] = defaultdict(F)
        for code, weight in distribution.items():
            values = observables(code)
            if n < max_population or audit:
                transitions = dict(attachment_transitions(code))
            if audit:
                direct = two_stage_transitions(code)
                check(sum(values.h, F(0)) == n, "attachment_rate_normalization")
                check(sum(transitions.values(), F(0)) == 1, "aggregated_transition_normalization")
                check(sum(direct.values(), F(0)) == 1, "direct_transition_normalization")
                check(transitions == direct, "aggregated_vs_two_stage_transitions")
                check(all(observables(new).population == n + 1 for new in transitions),
                      "one_vertex_per_transition")
                core_drift = sum((probability * (observables(new).cores - values.cores)
                                  for new, probability in direct.items()), F(0))
                check(n * core_drift == values.lam, "per_state_core_drift")
                if n >= 3:
                    adjacency = adjacency_from_code(code)
                    leaf_formula = sum((F(values.leaf_neighbors[v], len(neighbors))
                                        for v, neighbors in enumerate(adjacency)
                                        if len(neighbors) >= 2), F(0))
                    check(values.lam == leaf_formula, "Lambda_leaf_neighbor_identity")
                    lam_drift = sum((probability * (observables(new).lam - values.lam)
                                     for new, probability in direct.items()), F(0))
                    check(n * lam_drift == values.lam / 2 - values.k + values.j,
                          "per_state_Lambda_drift")
                else:
                    edge_lam_drift = sum(
                        (probability * (observables(new).lam - values.lam)
                         for new, probability in direct.items()), F(0))
                    check(n * edge_lam_drift == -2, "edge_Lambda_drift_exception")
                per_state_audits += 1
            if n < max_population:
                for new, probability in transitions.items():
                    following[new] += weight * probability
        if n < max_population:
            distribution = dict(following)

    if audit:
        for n in range(2, max_population):
            a_n, b_n, k_n, j_n = moments[n]
            a_next, b_next, _, _ = moments[n + 1]
            check(n * (a_next - a_n) == b_n, "expected_core_recurrence")
            if n >= 3:
                check(n * (b_next - b_n) == b_n / 2 - k_n + j_n,
                      "expected_Lambda_recurrence")
        for n, expected in ((2, F(0)), (3, F(1)), (4, F(4, 3)),
                            (5, F(19, 12)), (6, F(647, 360))):
            if n <= max_population:
                check(moments[n][0] == expected, "hand_computed_initial_core_means")
        check(observables(edge).lam == 2, "edge_Lambda_exception")
        if max_population >= 4:
            check(initial_distributions[4][star(4)] == F(2, 3), "four_vertex_star_probability")
        if max_population >= 5:
            check(initial_distributions[5][star(5)] == F(1, 2), "five_vertex_star_probability")

    witness = []
    for allocation in ((3, 1), (2, 2)):
        code = double_star(*allocation)
        values = observables(code)
        witness.append({"leaf_allocation": list(allocation), "canonical_tree_code": code_text(code),
                        "population": values.population, "core_count": values.cores,
                        "Lambda": str(values.lam),
                        "conditional_expected_core_increment": str(values.lam / values.population)})
    if audit:
        check(witness[0]["population"] == witness[1]["population"] == 6,
              "double_star_same_population")
        check(witness[0]["core_count"] == witness[1]["core_count"] == 2,
              "double_star_same_core_count")
        check(witness[0]["Lambda"] == "5/4" and witness[1]["Lambda"] == "4/3",
              "double_star_distinct_core_drift")

    final_distribution = [
        {"canonical_tree_code": code_text(code), "probability": str(weight),
         "core_count": observables(code).cores, "Lambda": str(observables(code).lam)}
        for code, weight in sorted(distribution.items())
    ]
    return {
        "status": "PASS" if audit else "COMPUTED",
        "model": "Original free friend tree grown from an edge, with no inert stub.",
        "arithmetic": "Python standard-library integers and fractions.Fraction; no floating-point decisions.",
        "configuration": {"initial_population": 2, "max_population": max_population,
                          "canonicalization": "minimum nested rooted tuple over all roots; target multiplicities retained"},
        "identities": {
            "h_T(w)": "sum(1/d_T(u), u adjacent to w)",
            "attachment_probability": "h_T(w)/n",
            "Lambda(T)": "sum(h_T(w), w a leaf); Lambda(edge)=2",
            "K(T)": "sum(ell_T(w)/d_T(w)^2, w a nonleaf)",
            "J(T)": "sum(h_T(w)*(d_T(w)-ell_T(w))/(d_T(w)*(d_T(w)+1)), w a nonleaf)",
            "core_recurrence": "n*(a_(n+1)-a_n)=b_n for n>=2",
            "Lambda_drift": "n*E[Lambda(T_(n+1))-Lambda(T_n) | T_n=T]=Lambda(T)/2-K(T)+J(T) for n>=3",
        },
        "checks": dict(sorted(counts.items())), "total_checks": sum(counts.values()),
        "per_state_drift_audits": per_state_audits,
        "coefficients": rows,
        "nonclosure_witness": {
            "trees": witness,
            "conclusion": "Population and core count alone do not determine the next core-growth drift. This does not prove the absence of every scalar recurrence for the averaged sequence.",
        },
        "final_population_distribution": final_distribution,
        "scope": "Exploratory exact finite coefficient calculator and drift audit, not an efficient solver for mu or a closed finite scalar recurrence.",
        "not_proved_by_this_program": [
            "No finite recurrence closure, scalar differential equation, or hypergeometric formula for mu is established.",
            "Finite coefficients and state-wise identities do not establish an asymptotic error bound for recovering mu.",
            "No irrationality or transcendence assertion follows from these finite computations.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="audit independent transitions, per-state drifts, and expectation recurrences")
    parser.add_argument("--max-population", type=int, default=10)
    parser.add_argument("--output", type=Path, help="optional destination for the complete JSON report")
    args = parser.parse_args()
    if args.max_population < 3:
        parser.error("--max-population must be at least 3.")
    report = compute(args.max_population, args.check)
    serialized = json.dumps(report, indent=2) + "\n"
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized, encoding="utf-8")
    print(serialized, end="")


if __name__ == "__main__":
    main()
