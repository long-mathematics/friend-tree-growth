#!/usr/bin/env python3
"""Independent finite checks of the exact supersolution evaluator.

The original repository's Python evaluator provides the independent comparison.
The infinite jump and drift statements are proved in supersolution_local.tex.
"""
import argparse
from fractions import Fraction as Q
import importlib.util
import json
from pathlib import Path

from resolvent_supersolution import MotifSupersolution, NU, NU_STAR, J, PARENT_LIMIT_WEIGHT
from core_clock_kernel import CoreState


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', type=Path, required=True)
    ap.add_argument('--certificate', type=Path, required=True)
    ap.add_argument('--output', type=Path, default=Path('supersolution_evaluator_checks.json'))
    args = ap.parse_args()
    path = args.repo / 'verify/motif-bracket/verify_python_cross.py'
    spec = importlib.util.spec_from_file_location('independent_certificate_reader', path)
    independent = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(independent)
    ref = independent.PyCert(str(args.certificate))
    states = [CoreState((), (n,), (1,)) for n in [1, 2, 22, 23, 24, 799, 800, 801]]
    states.extend(CoreState(((0, 1),), (a, b), (1, 0))
                  for a, b in [(0, 1), (1, 1), (24, 1), (1, 24)])
    states.extend([CoreState(((0, 1), (1, 2)), (0, 0, 1), (1, 0, 0)),
                   CoreState(((0, 1), (1, 2)), (1, 1, 1), (1, 0, 0))])
    for n in [5, 6, 8, 9, 23, 24]:
        states.append(CoreState(tuple((0, j) for j in range(1, n + 1)),
                                (0,) + (1,) * n, (1,) + (0,) * n))
    comparisons = limit_comparisons = drifts = leaf_jumps = promotion_jumps = intervals = 0
    with MotifSupersolution(args.certificate) as model:
        for state in states:
            parent, children, triples = model.augmented_core(state)
            par = list(parent)
            for i, (leaves, k, h) in enumerate(triples):
                par.extend([i] * leaves)
            phi, cores = ref.eval_phi(par)
            assert phi == model.psi(state) and cores == state.k + 1
            comparisons += 1
            finite_limits = []
            for degree in [801, 1602]:
                par_d = list(parent)
                for i, (leaves, k, h) in enumerate(triples):
                    par_d.extend([i] * (degree - 1 if i == 0 else leaves))
                finite_limits.append(ref.eval_phi(par_d)[0])
            assert (2 * finite_limits[1] - finite_limits[0]
                    - PARENT_LIMIT_WEIGHT == model.chi(state))
            limit_comparisons += 1
            for s in [NU_STAR + Q(1, 10**7), NU, Q(3, 5)]:
                assert s * model.u0(state, s) - model.generator_u0(state, s) >= state.k
                drifts += 1
            for v, leaves in enumerate(state.leaves):
                assert abs(model.chi(state.add_leaf(v)) - model.chi(state)) <= J
                leaf_jumps += 1
                if leaves:
                    assert abs(model.chi(state.promote(v)) - model.chi(state)) <= J
                    promotion_jumps += 1
            if state.k <= 3:
                lo, hi, _ = model.one_step_interval(state, NU, 2)
                lo2, hi2, _ = model.one_step_interval(state, NU, 3)
                assert lo <= lo2 <= hi2 <= hi
                intervals += 1
    result = dict(status='PASS', independent_phi_states=comparisons,
                  independent_boundary_limit_states=limit_comparisons,
                  exact_generator_checks=drifts, leaf_jump_checks=leaf_jumps,
                  promotion_jump_checks=promotion_jumps,
                  nested_kernel_intervals=intervals)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
