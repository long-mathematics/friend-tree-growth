#!/usr/bin/env python3
"""Sharper certified supersolution from the unchanged motif certificate."""
import argparse
from decimal import Decimal, localcontext
from fractions import Fraction as Q
import json
from pathlib import Path

from resolvent_supersolution import MotifSupersolution, NU, ETA, M, J
from core_clock_kernel import CoreState, one_core_ring

EPSILON = Q(24776800469, 1485071445500000)
NU_DAGGER = NU - EPSILON
GROUPED_UPPER = Q(8424600447, 5000000000)
CRITICAL_WEIGHT = Q(2970142891, 5000000000)
BETA = Q(2832242711, 5000000000)
TAU = Q(5294970481, 100000000000000)
ZETA = Q(199752266575452391, 1200500000000000000000000000)
assert NU_DAGGER == Q(841268197075281, 1485071445500000)
assert CRITICAL_WEIGHT == ETA / EPSILON


class ContinuationSupersolution(MotifSupersolution):
    @staticmethod
    def denominator(s):
        s = Q(s)
        if s <= NU_DAGGER:
            raise ValueError(f'This construction is proved only for s>{NU_DAGGER}.')
        return ETA + (M if s >= NU else CRITICAL_WEIGHT) * (s - NU)

    def one_step_interval(self, state, s, max_added):
        s = Q(s)
        nonpromotion, promotion, missing = one_core_ring(state, s, max_added)
        lower = Q(state.k) / (state.k + s)
        for transitions in (nonpromotion, promotion):
            lower += sum((mass * self.u0(next_state, s)
                          for next_state, mass in transitions.items()), Q())
        future_bound = GROUPED_UPPER * (state.k + 1) / self.denominator(s)
        upper = min(self.u0(state, s), lower + missing * future_bound)
        if upper < lower:
            raise AssertionError('Supersolution/kernel interval inconsistency.')
        return lower, upper, missing


class CorrectedSupersolution(MotifSupersolution):
    """Primary improved seed from chi + TAU*C, proved for every s>=BETA."""
    @staticmethod
    def denominator(s):
        s = Q(s)
        if s < BETA:
            raise ValueError(f'This interface supports the proved range s>={BETA}.')
        return ZETA + (M + TAU) * (s - BETA)

    def corrected_chi(self, state):
        return self.chi(state) + TAU * state.k

    def u0(self, state, s):
        return self.corrected_chi(state) / self.denominator(s)

    def one_step_interval(self, state, s, max_added):
        s = Q(s)
        nonpromotion, promotion, missing = one_core_ring(state, s, max_added)
        lower = Q(state.k) / (state.k + s)
        for transitions in (nonpromotion, promotion):
            lower += sum((mass * self.u0(next_state, s)
                          for next_state, mass in transitions.items()), Q())
        future_bound = (GROUPED_UPPER + TAU) * (state.k + 1) / self.denominator(s)
        upper = min(self.u0(state, s), lower + missing * future_bound)
        if upper < lower:
            raise AssertionError('Supersolution/kernel interval inconsistency.')
        return lower, upper, missing


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--certificate', type=Path, required=True)
    ap.add_argument('--s', default='56645/100000')
    ap.add_argument('--max-added', type=int, default=8)
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    s = Q(args.s)
    state = CoreState((), (1,), (1,))
    with CorrectedSupersolution(args.certificate) as model:
        lo, hi, missing = model.one_step_interval(state, s, args.max_added)
        u0 = model.u0(state, s)
        residual = s * u0 - model.generator_u0(state, s) - state.k
        assert residual >= 0
        report = dict(proved_range=f's>={BETA}', beta=str(BETA), tau=str(TAU), zeta=str(ZETA), s=str(s),
                      denominator=str(model.denominator(s)),
                      u0_newborn=str(u0), generator_residual=str(residual),
                      ordinary_arrival_increment_bound=str((J + TAU) / model.denominator(s)),
                      one_step_interval=[str(lo), str(hi)],
                      omitted_discounted_ring_mass=str(missing))
        with localcontext() as context:
            context.prec = 40
            report['beta_decimal'] = str(Decimal(BETA.numerator) / Decimal(BETA.denominator))
    if args.output:
        args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
