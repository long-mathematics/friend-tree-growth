#!/usr/bin/env python3
"""Exact finite audits supporting the critical-boundary argument.

Enumerate rooted one-stub inert states using the existing proper-birth
helpers. Check the eligible-core counting lemma and, at every possible
newborn tag, check finite cut profiles by direct graph traversal and an
independent nonbacktracking-walk probability calculation. All arithmetic
decisions use integers or Fraction.

These checks do not prove the infinite disagreement coupling, guardian
minorization, critical divergence, eigenfunction existence, or irrationality.
Those statements, where asserted, require the manuscript proofs.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as F
import json
from pathlib import Path

from core_clock_kernel import CoreState
from inert_growth_kernel import INERT_INITIAL
from primitive_population_tools import proper_channels


S0 = F(11, 20)
INFECTION_BOUND = F(19, 20)


def rooted_paths(adjacency: tuple[tuple[int, ...], ...], tag: int):
    """Unique full-core paths, without using the proposed cut profile."""
    paths = {tag: (tag,)}
    pending = [tag]
    for vertex in pending:
        for neighbor in adjacency[vertex]:
            if neighbor not in paths:
                paths[neighbor] = paths[vertex] + (neighbor,)
                pending.append(neighbor)
    return paths


def cut_profile(state: CoreState, tag: int, radius: int, threshold: int):
    """First high-degree/depth cuts, retaining all degree labels via stubs.

    Each recorded cut is (retained target, removed neighbor, reason).
    High degree takes precedence when both stopping conditions hold.
    """
    adjacency, degrees = state.neighbors(), state.degrees()
    retained = {tag}
    pending = [(tag, -1, 0)]
    cuts = []
    for vertex, parent, depth in pending:
        for neighbor in adjacency[vertex]:
            if neighbor == parent:
                continue
            if degrees[neighbor] >= threshold:
                cuts.append((vertex, neighbor, "degree"))
            elif depth + 1 >= radius:
                cuts.append((vertex, neighbor, "depth"))
            else:
                retained.add(neighbor)
                pending.append((neighbor, vertex, depth + 1))
    vertices = tuple(sorted(retained))
    indices = {old: new for new, old in enumerate(vertices)}
    edges = tuple(sorted((indices[u], indices[v]) for u, v in state.edges
                         if u in retained and v in retained))
    leaves = tuple(state.leaves[v] for v in vertices)
    stubs = tuple(state.stubs[v] + sum(w not in retained for w in adjacency[v])
                  for v in vertices)
    return CoreState(edges, leaves, stubs), vertices, tuple(cuts)


def direct_walk_frontier(state: CoreState, tag: int, cut_edges):
    """Split probability at each forward edge/stub; stop at cuts or dead ends.

    This local traversal does not use path-product formulas. It includes
    original-stub and dead-end terminal mass as a check on conservation.
    """
    adjacency = state.neighbors()
    frontier = {}
    terminal_mass = F(0)
    reached = set()
    pending = [(tag, -1, F(1))]
    for vertex, parent, mass in pending:
        reached.add(vertex)
        forward = [w for w in adjacency[vertex] if w != parent]
        choices = len(forward) + state.stubs[vertex]
        if choices == 0:
            terminal_mass += mass
            continue
        share = mass / choices
        terminal_mass += state.stubs[vertex] * share
        for neighbor in forward:
            edge = vertex, neighbor
            if edge in cut_edges:
                frontier[edge] = share
                terminal_mass += share
            else:
                pending.append((neighbor, vertex, share))
    return frontier, terminal_mass, reached


def run_checks(maximum_population: int):
    if maximum_population < 2:
        raise ValueError("Maximum real population must be at least two.")
    checks = Counter()

    def check(condition, category):
        if not condition:
            raise AssertionError(category)
        checks[category] += 1

    q = INFECTION_BOUND
    check(2 * 19**16 < 20**16, "rational_sixteen_step_discount")
    check(q**160 < F(1, 1024), "rational_depth_discount")
    prefactor = 2 / (S0**2 * (1 - q))
    kappa = prefactor * (F(1, 1024) + q**160 / 2)
    coarse_kappa = prefactor * F(3, 2048)
    check(coarse_kappa == F(375, 1936), "exact_relative_error_constant")
    check(kappa <= coarse_kappa, "relative_error_constant_upper_bound")
    check(coarse_kappa < F(1, 4), "relative_error_absorption_margin")

    states = {INERT_INITIAL}
    rows = []
    total_tags = total_profiles = 0
    smallest_eligible_fraction = None
    largest_frontier_mass = F(0)
    largest_error_ratio = F(0)
    omitted_target_denominator_witness = None

    for population in range(2, maximum_population + 1):
        tags_this_population = profiles_this_population = 0
        for state in sorted(states, key=lambda y: (y.edges, y.leaves, y.stubs)):
            adjacency = state.neighbors()
            core_degrees = state.core_degrees()
            degrees = state.degrees()
            k = state.k
            check(k + sum(state.leaves) == population,
                  "enumerated_real_population")
            check(state.stubs == (1,) + (0,) * (k - 1),
                  "enumerated_single_root_stub")
            check(sum(core_degrees) == 2 * k - 1,
                  "one_stub_core_degree_sum")

            # Direct graph classification for the old-core counting lemma.
            degree_one = {v for v, c in enumerate(core_degrees) if c == 1}
            high = {v for v, c in enumerate(core_degrees) if c >= 3}
            bare_two = {v for v, c in enumerate(core_degrees)
                        if c == 2 and state.leaves[v] == 0}
            isolated = {v for v in bare_two
                        if not any(w in bare_two for w in adjacency[v])}
            eligible = {v for v in range(k)
                        if (core_degrees[v] <= 2 and state.leaves[v] >= 1)
                        or (v in bare_two and any(w in bare_two for w in adjacency[v]))}
            check(all(state.leaves[v] >= 1 for v in degree_one),
                  "degree_one_cores_have_leaves")
            check(len(high) <= len(degree_one) - 1,
                  "high_core_degree_count")
            check(all(not any(w in isolated for w in adjacency[v]) for v in isolated),
                  "isolated_bare_twos_are_independent")
            incident_edges = {edge for edge in state.edges
                              if edge[0] in isolated or edge[1] in isolated}
            check(len(incident_edges) == sum(len(adjacency[v]) for v in isolated),
                  "isolated_incident_edges_are_distinct")
            check(2 * len(isolated) - 1 <= len(incident_edges) <= k - 1,
                  "isolated_bare_two_edge_bound")
            check(2 * len(isolated) <= k, "isolated_bare_two_count")
            check(len(eligible) == k - len(high) - len(isolated),
                  "eligible_core_partition")
            check(len(eligible) >= len(degree_one),
                  "eligible_include_degree_one_cores")
            check(4 * len(eligible) >= k, "eligible_core_quarter_bound")
            fraction = F(len(eligible), k)
            if smallest_eligible_fraction is None or fraction < smallest_eligible_fraction:
                smallest_eligible_fraction = fraction

            newborn_tags = [v for v in range(k)
                            if state.leaves[v] == 1 and core_degrees[v] == 1]
            for tag in newborn_tags:
                tags_this_population += 1
                paths = rooted_paths(adjacency, tag)
                check(len(paths) == k, "newborn_rooted_paths_cover_core")
                # These ranges cover every distinct cut configuration at this
                # population, including one beyond each possible threshold.
                for radius in range(1, k + 2):
                    for threshold in range(3, population + 2):
                        profiles_this_population += 1
                        profile, vertices, cuts = cut_profile(state, tag, radius, threshold)
                        retained = set(vertices)
                        cut_edges = {(v, w) for v, w, _reason in cuts}
                        check(len(cut_edges) == len(cuts), "distinct_cut_edges")
                        check(sum(profile.stubs) >= 1, "cut_profile_has_inert_stub")
                        check(profile.degrees() == tuple(degrees[v] for v in vertices),
                              "cut_profile_preserves_full_degrees")
                        check(profile.core_degrees() == tuple(core_degrees[v] for v in vertices),
                              "cut_profile_preserves_core_and_stub_degrees")
                        check(profile.leaves == tuple(state.leaves[v] for v in vertices),
                              "cut_profile_preserves_leaf_counts")
                        profile_tag = vertices.index(tag)
                        check(profile.leaves[profile_tag] == 1
                              and profile.core_degrees()[profile_tag] == 1,
                              "cut_profile_keeps_newborn_tag")
                        check(all(degrees[v] < threshold and len(paths[v]) - 1 < radius
                                  for v in vertices), "retained_vertices_below_cut_limits")
                        direct_frontier, terminal_mass, reached = direct_walk_frontier(
                            state, tag, cut_edges)
                        check(reached == retained, "direct_walk_visits_exact_retained_profile")
                        check(terminal_mass == 1, "direct_walk_terminal_mass_one")
                        check(set(direct_frontier) == cut_edges,
                              "direct_walk_finds_exact_cut_frontier")

                        cut_paths = [paths[w] for _v, w, _reason in cuts]
                        check(all(not (len(first) < len(second)
                                      and second[:len(first)] == first)
                                  for first in cut_paths for second in cut_paths),
                              "cut_paths_are_prefix_free")
                        path_mass = weighted_error = omitted_denominator_mass = F(0)
                        degree_error = depth_error = F(0)
                        for vertex, outside, reason in cuts:
                            path = paths[vertex]
                            depth = len(path) - 1
                            check(paths[outside] == path + (outside,),
                                  "cut_orientation_follows_newborn_path")
                            probability = F(1)
                            for internal in path[1:]:
                                check(core_degrees[internal] >= 2,
                                      "forward_path_denominator_positive")
                                probability /= core_degrees[internal] - 1
                            check(probability == direct_frontier[vertex, outside],
                                  "path_product_matches_direct_walk")
                            path_mass += probability
                            # Omit the retained target's factor only to record
                            # a finite witness that this incorrect formula can
                            # make the total frontier mass exceed one.
                            wrong_probability = F(1)
                            for internal in path[1:-1]:
                                wrong_probability /= core_degrees[internal] - 1
                            omitted_denominator_mass += wrong_probability
                            term = q**depth * probability / degrees[outside]
                            weighted_error += term
                            if reason == "degree":
                                check(degrees[outside] >= threshold,
                                      "high_degree_cut_rate_condition")
                                check(term <= probability / threshold,
                                      "high_degree_weighted_rate_bound")
                                degree_error += term
                            else:
                                check(depth == radius - 1 and degrees[outside] < threshold,
                                      "depth_cut_rate_condition")
                                check(term <= q**(radius - 1) * probability / 2,
                                      "depth_weighted_rate_bound")
                                depth_error += term
                        check(path_mass <= 1, "prefix_frontier_mass_bound")
                        check(path_mass == sum(direct_frontier.values(), F(0)),
                              "prefix_sum_matches_direct_walk")
                        check(degree_error <= F(1, threshold),
                              "summed_high_degree_cut_bound")
                        check(depth_error <= q**(radius - 1) / 2,
                              "summed_depth_cut_bound")
                        error_bound = F(1, threshold) + q**(radius - 1) / 2
                        check(weighted_error <= error_bound,
                              "combined_weighted_cut_error_bound")
                        largest_frontier_mass = max(largest_frontier_mass, path_mass)
                        largest_error_ratio = max(largest_error_ratio,
                                                  weighted_error / error_bound)
                        if omitted_denominator_mass > 1 and omitted_target_denominator_witness is None:
                            omitted_target_denominator_witness = {
                                "real_population": population,
                                "edges": [list(edge) for edge in state.edges],
                                "leaves": list(state.leaves), "stubs": list(state.stubs),
                                "tag": tag, "radius": radius, "degree_threshold": threshold,
                                "correct_frontier_mass": str(path_mass),
                                "mass_if_retained_target_factor_is_omitted": str(omitted_denominator_mass),
                            }

        total_tags += tags_this_population
        total_profiles += profiles_this_population
        rows.append({"real_population": population, "rooted_one_stub_states": len(states),
                     "newborn_tag_choices": tags_this_population,
                     "cut_profiles_checked": profiles_this_population})
        if population < maximum_population:
            following = set()
            for state in states:
                for child, _depth, rate in proper_channels(state):
                    check(rate > 0, "enumeration_positive_proper_channel")
                    check(child.k + sum(child.leaves) == population + 1,
                          "enumeration_one_real_vertex_per_birth")
                    following.add(child)
            states = following

    if maximum_population >= 6:
        check(omitted_target_denominator_witness is not None,
              "nontrivial_retained_target_denominator_witness")

    return {
        "status": "PASS", "exact_checks": sum(checks.values()),
        "arithmetic": "integers and fractions.Fraction; no floating-point decisions",
        "maximum_real_population": maximum_population,
        "checks": dict(sorted(checks.items())),
        "population_rows": rows,
        "rooted_one_stub_states_checked": sum(row["rooted_one_stub_states"] for row in rows),
        "newborn_tag_choices_checked": total_tags,
        "cut_profiles_checked": total_profiles,
        "minimum_eligible_core_fraction_in_finite_sample": str(smallest_eligible_fraction),
        "largest_prefix_frontier_mass": str(largest_frontier_mass),
        "largest_weighted_error_to_bound_ratio": str(largest_error_ratio),
        "relative_error_certificate": {
            "s0": str(S0), "infection_mass_bound": str(q),
            "radius": 161, "degree_threshold": 1024,
            "kappa_exact": str(kappa), "kappa_upper": str(coarse_kappa),
            "absorption_threshold": "1/4",
        },
        "retained_target_denominator_witness": omitted_target_denominator_witness,
        "scope": "Finite one-stub core counting, cut-profile degree preservation, "
                 "prefix-free path probabilities, weighted cut inequalities, and an exact "
                 "rational absorption constant. This does not prove the infinite coupling, "
                 "guardian construction, critical boundary theorem, or irrationality.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="run the exact audit (also the default)")
    parser.add_argument("--maximum-population", type=int, default=9)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.maximum_population < 2:
        parser.error("--maximum-population must be at least 2")
    report = run_checks(args.maximum_population)
    serialized = json.dumps(report, indent=2) + "\n"
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized, encoding="utf-8")
    print(serialized, end="")


if __name__ == "__main__":
    main()
