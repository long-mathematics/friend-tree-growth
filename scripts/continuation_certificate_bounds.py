#!/usr/bin/env python3
"""Strengthen the inherited verified motif certificate without altering it.

Rechecks only its 484138 exact vertex rows, computes correlated grouped
upper weights, and compares each row reserve with its matching upper weight.
All arithmetic controlling the result is exact. The unchanged edge/vertical/
cherry inequalities are inherited from the full pinned certificate check.
"""
import argparse
from array import array
from decimal import Decimal, localcontext
from fractions import Fraction as Q
import hashlib
import json
from math import ceil
from pathlib import Path
import struct
import sys

from resolvent_supersolution import MotifSupersolution, NU, ETA, M, J


def read_array(stream, offset, count):
    stream.seek(offset)
    values = array('q')
    values.fromfile(stream, count)
    if sys.byteorder != 'little':
        values.byteswap()
    return values


class GroupedUpper:
    def __init__(self, model):
        self.model = model
        c = model
        self.scale = c.scale
        self.f = read_array(c.file, c.offset['f'], 241904)
        self.g = read_array(c.file, c.offset['g'], 601**2)
        hv = read_array(c.file, c.offset['hV'], 555 * 84 * 290)
        hc = read_array(c.file, c.offset['hC'], 75 * 290 * 291 // 2)
        chs, pars = list(c.chs), list(c.pars)
        self.incoming = [0] * c.ng
        for iw, w in enumerate(chs):
            bound = max(0, max(self.g[p * c.ng + w] for p in pars))
            for triple, ui in c.hu.items():
                p = c.inner[triple]
                best_vertical = max(hv[(pi * 84 + ui) * 290 + iw] for pi in range(555))
                bound = max(bound, self.g[p * c.ng + w] + best_vertical)
            self.incoming[w] = bound
        width = 290 * 291 // 2
        self.cherries = [max(0, max(hc[i * width:(i + 1) * width])) for i in range(75)]
        del hv, hc

    def f_integer(self, l, k, h):
        if k > 150:
            return self.f[241902 if h else 241903]
        return self.f[(0 if h else 151 * 801) + 801 * k + min(l, 800)]

    def incoming_at(self, k, degree):
        c = self.model
        r0, r1 = self.incoming[c.inf], self.incoming[c.t1 + min(k, 13)]
        return Q(r0) if degree is None else r0 + Q(24, degree) * (r1 - r0)

    def bound(self, l, k, h, tail_degree='actual'):
        c = self.model
        degree = l + k + h
        result = Q(self.f_integer(l, k, h))
        if h:
            if tail_degree == 'actual' and degree < 24:
                result += self.incoming[c.inner[l, k, h]]
            else:
                result += self.incoming_at(k, degree if tail_degree == 'actual' else tail_degree)
        ci = c.cu.get((l, k, h))
        if ci is not None:
            result += (k * (k - 1) // 2) * self.cherries[ci]
        return result / self.scale

    def vertex(self, l, k, h):
        return Q(self.f_integer(l, k, h), self.scale)

    def edge_newborn(self, l, k, h):
        c = self.model
        w = c.inner[1, 0, 1]
        d = l + k + h
        if d < 24:
            return Q(self.g[c.inner[l, k, h] * 601 + w], self.scale)
        p1 = c.t1 + (0 if h else 14) + min(k, 13)
        return Q((d - 24) * self.g[c.inf * 601 + w] + 24 * self.g[p1 * 601 + w], d * self.scale)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--certificate', type=Path, required=True)
    ap.add_argument('--output', type=Path, default=Path('continuation_certificate_bounds.json'))
    ap.add_argument('--perturb-core', action='store_true',
                    help='Find and exactly verify a positive constant per-core correction.')
    ap.add_argument('--verify-beta', help='Exact rational target; use with --verify-correction to skip discovery.')
    ap.add_argument('--verify-correction', help='Exact rational per-core correction to verify.')
    args = ap.parse_args()
    if (args.verify_beta or args.verify_correction) and not args.perturb_core:
        ap.error('--verify-beta/--verify-correction require --perturb-core')
    with MotifSupersolution(args.certificate) as c:
        grouped = GroupedUpper(c)
        c.file.seek(0)
        header = struct.unpack('<Qiiiiqqiiiiiiiiii9ii', c.file.read(120))
        sr = header[6]
        rpar = read_array(c.file, 120, 572)
        rch = read_array(c.file, 120 + 8 * 572, 572)
        fnb = grouped.vertex(1, 0, 1)
        gnb_inf = Q(grouped.g[c.inf * 601 + c.inner[1, 0, 1]], c.scale)
        count = 0
        minimum_slack = minimum_ratio = maximum_weight = None
        best_ratio_state = best_weight_state = best_slack_state = None
        category_reports = {}
        saved_rows = [] if args.perturb_core else None
        def record(slack, weight, state):
            nonlocal count, minimum_slack, minimum_ratio, maximum_weight
            nonlocal best_ratio_state, best_weight_state, best_slack_state
            count += 1
            assert slack >= 0 and weight > 0
            if saved_rows is not None:
                if state[0] == 'VSTAR':
                    birth = Q(state[2])
                elif state[0] == 'Ltail':
                    birth = Q(801, 801 + state[1] + state[2]) if state[3] == 0 else Q(1)
                else:
                    birth = Q(state[1], state[1] + state[2] + state[3])
                saved_rows.append((slack, weight, birth, state))
            ratio = slack / weight
            if minimum_slack is None or slack < minimum_slack:
                minimum_slack, best_slack_state = slack, state
            if minimum_ratio is None or ratio < minimum_ratio:
                minimum_ratio, best_ratio_state = ratio, state
            if maximum_weight is None or weight > maximum_weight:
                maximum_weight, best_weight_state = weight, state
            category = category_reports.setdefault(state[0], {'count': 0})
            category['count'] += 1
            for label, value in [('minimum_slack', slack), ('minimum_ratio', ratio), ('maximum_weight', weight)]:
                take = (label not in category or
                        (value > category[label] if label == 'maximum_weight' else value < category[label]))
                if take:
                    category[label] = value
                    category[label + '_state'] = state
                    if label == 'minimum_ratio':
                        category['ratio_row_slack'] = slack
                        category['ratio_row_weight'] = weight
        for h in (0, 1):
            fu = grouped.vertex(0, 151, h)
            for bi, b in enumerate((Q(0), Q(1))):
                for gi, gnb in enumerate((gnb_inf, grouped.edge_newborn(0, 151, h))):
                    weight = grouped.bound(0, 151, h, tail_degree=None if gi == 0 else 151 + h)
                    record(NU * fu - b * (fnb + gnb), weight, ['VSTAR', h, bi, gi])
        for h in (0, 1):
            for k in range(151):
                for l in range(801):
                    d = l + k + h
                    if d < 2:
                        continue
                    fu = grouped.vertex(l, k, h)
                    rhs = NU * fu
                    weight = grouped.bound(l, k, h)
                    if l == 800:
                        b = Q(l, d)
                        bud = b * (grouped.vertex(l - 1, k + 1, h) - fu + fnb + grouped.edge_newborn(l - 1, k + 1, h))
                        record(rhs - bud, weight, ['L800', l, k, h])
                        for bi, b in enumerate((Q(801, 801 + k + h), Q(1))):
                            for gi, gnb in enumerate((gnb_inf, grouped.edge_newborn(800, k + 1, h))):
                                bud = b * (grouped.vertex(800, k + 1, h) - fu + fnb + gnb)
                                tail_weight = grouped.bound(l, k, h, tail_degree=None if gi == 0 else 801 + k + h)
                                record(rhs - bud, tail_weight, ['Ltail', k, h, bi, gi])
                    else:
                        up = grouped.vertex(l + 1, k, h) - fu
                        bud = (Q(l, d) * (grouped.vertex(l - 1, k + 1, h) - fu + fnb + grouped.edge_newborn(l - 1, k + 1, h))) if l else Q()
                        if d < 24:
                            ui = c.inner[l, k, h]
                            rate = l + Q(h * rpar[ui] + k * rch[ui], sr)
                            record(rhs - rate * up - bud, weight, ['inner', l, k, h])
                        else:
                            for ri, rate in enumerate((Q(l), l + Q(h + k, 2))):
                                record(rhs - rate * up - bud, weight, ['outer', l, k, h, ri])
        assert count == 484138
        assert minimum_slack == ETA
        assert maximum_weight == Q(8424600447, 5000000000)
        uniform_bound = NU - ETA / maximum_weight
        typed_bound = NU - minimum_ratio
        report = {
            'status': 'PASS', 'vertex_rows_rechecked': count,
            'minimum_vertex_slack': str(minimum_slack), 'minimum_slack_state': best_slack_state,
            'grouped_upper_A': str(maximum_weight), 'maximum_weight_state': best_weight_state,
            'uniform_reserve_bound': str(uniform_bound),
            'typed_reserve_epsilon': str(minimum_ratio), 'minimum_ratio_state': best_ratio_state,
            'typed_reserve_bound': str(typed_bound),
            'binary_sha256': hashlib.sha256(c.data).hexdigest(),
            'incoming_INF_integer': grouped.incoming[c.inf],
            'incoming_T1_13_integer': grouped.incoming[c.t1 + 13],
            'row_categories': {name: {key: str(value) if isinstance(value, Q) else value
                                     for key, value in row.items()}
                               for name, row in category_reports.items()},
            'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'scope': 'New exact vertex-row/weight comparisons; other motif inequalities inherited from the unchanged fully verified certificate.'
        }
        if saved_rows is not None:
            discovery_rows = (None if args.verify_beta else
                              [(float(d), float(q), float(b)) for d, q, b, _ in saved_rows])
            def feasible_float(beta):
                lower, upper = 0.0, float('inf')
                for delta, weight, birth in discovery_rows:
                    spare = delta - (float(NU) - beta) * weight
                    coefficient = beta - birth
                    if coefficient > 0:
                        lower = max(lower, -spare / coefficient)
                    elif coefficient < 0:
                        upper = min(upper, -spare / coefficient)
                    elif spare < 0:
                        return False
                return lower <= upper
            hi = None
            if args.verify_beta or args.verify_correction:
                assert args.verify_beta and args.verify_correction
                beta = Q(args.verify_beta)
            else:
                lo, hi = 0.5, float(NU)
                assert not feasible_float(lo) and feasible_float(hi)
                for _ in range(45):
                    middle = (lo + hi) / 2
                    if feasible_float(middle):
                        hi = middle
                    else:
                        lo = middle
                # Floating point only proposes a rational target; every decisive
                # inequality below is recomputed with exact Fraction arithmetic.
                beta = Q(ceil(hi * 10**10) + 1, 10**10)
            lower, upper = Q(), None
            lower_state = upper_state = None
            for delta, weight, birth, state in saved_rows:
                spare = delta - (NU - beta) * weight
                coefficient = beta - birth
                if coefficient > 0:
                    endpoint = -spare / coefficient
                    if endpoint > lower:
                        lower, lower_state = endpoint, [delta, weight, birth, state]
                elif coefficient < 0:
                    endpoint = -spare / coefficient
                    if upper is None or endpoint < upper:
                        upper, upper_state = endpoint, [delta, weight, birth, state]
                else:
                    assert spare >= 0
            assert upper is not None and Q() <= lower <= upper
            middle = (lower + upper) / 2
            correction = Q(args.verify_correction) if args.verify_correction else Q(round(middle * 10**14), 10**14)
            if args.verify_correction:
                assert lower <= correction <= upper
            elif not lower <= correction <= upper:
                correction = middle
            minimum_perturbed_margin = None
            minimum_perturbed_state = None
            minimum_perturbed_slack = minimum_perturbed_ratio = None
            minimum_perturbed_slack_state = minimum_perturbed_ratio_state = None
            adjusted_categories = {}
            for delta, weight, birth, state in saved_rows:
                margin = delta - (NU - beta) * weight + correction * (beta - birth)
                assert margin >= 0
                if minimum_perturbed_margin is None or margin < minimum_perturbed_margin:
                    minimum_perturbed_margin, minimum_perturbed_state = margin, state
                adjusted_slack = delta + correction * (NU - birth)
                adjusted_ratio = adjusted_slack / (weight + correction)
                if minimum_perturbed_slack is None or adjusted_slack < minimum_perturbed_slack:
                    minimum_perturbed_slack, minimum_perturbed_slack_state = adjusted_slack, state
                if minimum_perturbed_ratio is None or adjusted_ratio < minimum_perturbed_ratio:
                    minimum_perturbed_ratio, minimum_perturbed_ratio_state = adjusted_ratio, state
                category = adjusted_categories.setdefault(state[0], {'count': 0})
                category['count'] += 1
                for label, value in [('minimum_margin_at_beta', margin),
                                     ('minimum_adjusted_slack', adjusted_slack),
                                     ('minimum_adjusted_ratio', adjusted_ratio)]:
                    if label not in category or value < category[label]:
                        category[label] = value
                        category[label + '_state'] = state
                        if label == 'minimum_margin_at_beta':
                            category['margin_row_original_delta'] = delta
                            category['margin_row_original_weight'] = weight
                            category['margin_row_birth_fraction'] = birth
            def row_report(row):
                return {'delta': str(row[0]), 'weight': str(row[1]), 'birth': str(row[2]), 'state': row[3]}
            report['constant_core_correction'] = {
                'verified_beta': str(beta), 'correction_t': str(correction),
                'feasible_t_interval': [str(lower), str(upper)],
                'lower_constraint': row_report(lower_state),
                'upper_constraint': row_report(upper_state),
                'minimum_exact_margin': str(minimum_perturbed_margin),
                'minimum_margin_state': minimum_perturbed_state,
                'minimum_adjusted_vertex_slack': str(minimum_perturbed_slack),
                'minimum_adjusted_slack_state': minimum_perturbed_slack_state,
                'minimum_adjusted_ratio': str(minimum_perturbed_ratio),
                'minimum_adjusted_ratio_state': minimum_perturbed_ratio_state,
                'sharpened_beta': str(NU - minimum_perturbed_ratio),
                'row_categories': {name: {key: str(value) if isinstance(value, Q) else value
                                         for key, value in row.items()}
                                   for name, row in adjusted_categories.items()},
                'exact_rows_verified': len(saved_rows),
                'discovery_beta_approximation': hi,
            }
        with localcontext() as context:
            context.prec = 60
            for name, value in [('uniform_reserve_bound_decimal', uniform_bound), ('typed_reserve_bound_decimal', typed_bound), ('typed_epsilon_decimal', minimum_ratio)]:
                report[name] = str(Decimal(value.numerator) / Decimal(value.denominator))
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
