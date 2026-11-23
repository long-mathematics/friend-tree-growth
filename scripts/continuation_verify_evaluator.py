#!/usr/bin/env python3
"""Exact finite checks of the constant-corrected supersolution.

The unmodified motif reader has independent full-tree and boundary-limit
comparisons in verify_supersolution_evaluator.py. These additional checks
exercise the corrected potential, its new endpoint s=BETA and its kernel.
"""
import argparse
from fractions import Fraction as Q
import json
from pathlib import Path

from continuation_supersolution import CorrectedSupersolution, BETA, TAU, ZETA, NU, J
from core_clock_kernel import CoreState


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--certificate', type=Path, required=True)
    ap.add_argument('--output', type=Path, default=Path('continuation_evaluator_checks.json'))
    args = ap.parse_args()
    states = [CoreState((), (n,), (1,)) for n in [1, 2, 22, 23, 24, 799, 800, 801]]
    states.extend(CoreState(((0, 1),), (a, b), (1, 0))
                  for a, b in [(0, 1), (1, 1), (24, 1), (1, 24)])
    states.extend([CoreState(((0, 1), (1, 2)), (0, 0, 1), (1, 0, 0)),
                   CoreState(((0, 1), (1, 2)), (1, 1, 1), (1, 0, 0))])
    for n in [5, 6, 8, 9, 23, 24]:
        states.append(CoreState(tuple((0, j) for j in range(1, n + 1)),
                                (0,) + (1,) * n, (1,) + (0,) * n))
    discounts = [BETA, BETA + Q(1, 10**7), NU]
    drifts = leaf_jumps = promotion_jumps = intervals = 0
    with CorrectedSupersolution(args.certificate) as model:
        for state in states:
            for s in discounts:
                assert s * model.u0(state, s) - model.generator_u0(state, s) >= state.k
                drifts += 1
            for v, leaves in enumerate(state.leaves):
                assert abs(model.corrected_chi(state.add_leaf(v)) - model.corrected_chi(state)) <= J + TAU
                leaf_jumps += 1
                if leaves:
                    assert abs(model.corrected_chi(state.promote(v)) - model.corrected_chi(state)) <= J + TAU
                    promotion_jumps += 1
            if state.k <= 3:
                lo, hi, _ = model.one_step_interval(state, BETA, 2)
                lo2, hi2, _ = model.one_step_interval(state, BETA, 3)
                assert lo <= lo2 <= hi2 <= hi
                intervals += 1
    result = dict(status='PASS', beta=str(BETA), tau=str(TAU), zeta=str(ZETA),
                  states=len(states), tested_discounts=[str(s) for s in discounts],
                  exact_generator_checks=drifts, corrected_leaf_jump_checks=leaf_jumps,
                  corrected_promotion_jump_checks=promotion_jumps,
                  nested_kernel_intervals=intervals)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
