#!/usr/bin/env python3
"""Exact evaluation of the certificate-based friend-tree supersolution.

Requires the pinned upper_5665.bin generated and verified by
verify_supersolution_certificate.py.  Uses only the standard library plus
the companion core_clock_kernel.py.  The supported range is s>NU_STAR;
this does not assert construction for every s>mu.
"""
import argparse
import hashlib
from fractions import Fraction as Q
from itertools import combinations
import json
import mmap
from pathlib import Path
import struct

from core_clock_kernel import CoreState, one_core_ring

NU = Q(1133, 2000)
ETA = Q(24776800469, 2500000000000000)
M = Q(2989767809, 10000000000)
A = Q(20674280349, 5000000000)
J = Q(338409055893, 5000000000)
PARENT_LIMIT_WEIGHT = Q(261553463, 156250000)
NU_STAR = NU - ETA / A
CERTIFICATE_SHA256 = '3a4aef888a5b567a8ada05f9546f98c979d361da9f9b33ba6e794eb91fb30abe'


class MotifSupersolution:
    """Memory-mapped exact evaluator; no full-array Python-int allocation."""

    def __init__(self, binary):
        self.file = Path(binary).open('rb')
        self.data = mmap.mmap(self.file.fileno(), 0, access=mmap.ACCESS_READ)
        if hashlib.sha256(self.data).hexdigest() != CERTIFICATE_SHA256:
            self.close()
            raise ValueError('Certificate differs from the verified input; recheck its constants before use.')
        header = struct.unpack_from('<Qiiiiqqiiiiiiiiii9ii', self.data, 0)
        if (header[0] != 0x494E564433563031 or header[1:4] != (1, 1133, 2000)
                or header[5] != 10**10
                or header[7:15] != (800, 150, 24, 12, 16, 8, 12, 6)):
            raise ValueError('Expected the pinned 0.5665 upper motif certificate.')
        self.scale = header[5]
        self.inner = {}
        kinds, child_counts, parent_indicators = [], [], []
        for h in (1, 0):
            for d in range(2, 24):
                for k in range(d - h + 1):
                    self.inner[d - h - k, k, h] = len(kinds)
                    kinds.append(0); child_counts.append(k); parent_indicators.append(h)
        self.inf = len(kinds)
        kinds.append(1); child_counts.append(-1); parent_indicators.append(-1)
        self.t1 = len(kinds)
        for h in (1, 0):
            for k in range(14):
                kinds.append(2); child_counts.append(k); parent_indicators.append(h)
        self.ng = len(kinds)
        self.pars = {v: i for i, v in enumerate(
            v for v in range(self.ng) if kinds[v] == 1 or child_counts[v] >= 1)}
        self.chs = {v: i for i, v in enumerate(
            v for v in range(self.ng) if kinds[v] == 1 or parent_indicators[v] == 1)}
        self.hu = {(l, k, 1): i for i, (l, k) in enumerate(
            (l, k) for k in range(1, 9) for l in range(16) if l + k + 1 < 16)}
        self.cu = {(l, k, h): i for i, (l, k, h) in enumerate(
            (l, k, h) for h in (1, 0) for k in range(2, 7)
            for l in range(12) if l + k + h < 12)}
        assert (self.inf, self.ng, len(self.pars), len(self.chs), len(self.hu), len(self.cu)) == (572, 601, 555, 290, 84, 75)
        self.offset = {}
        offset = 120 + 8 * (5 * 572 + 3 * 572 * 9)
        for name, count in [('f', 241904), ('g', 601**2),
                            ('hV', 555 * 84 * 290), ('hC', 75 * 290 * 291 // 2)]:
            self.offset[name] = offset
            offset += 8 * count
        if offset != len(self.data):
            raise ValueError('Unexpected certificate size.')

    def close(self):
        self.data.close()
        self.file.close()

    def __enter__(self):
        return self

    def __exit__(self, *unused):
        self.close()

    def entry(self, name, index):
        return Q(struct.unpack_from('<q', self.data, self.offset[name] + 8 * index)[0], self.scale)

    def endpoint(self, triple):
        l, k, h = triple
        d = l + k + h
        if d < 24:
            return ((self.inner[triple], Q(1)),)
        t = Q(24, d)
        return ((self.inf, 1 - t), (self.t1 + (0 if h else 14) + min(k, 13), t))

    def vertex(self, triple):
        l, k, h = triple
        index = (241902 if h else 241903) if k > 150 else (
            (0 if h else 151 * 801) + 801 * k + min(l, 800))
        return self.entry('f', index)

    def edge(self, p, w):
        return sum((pa * wb * self.entry('g', a * 601 + b)
                    for a, pa in self.endpoint(p) for b, wb in self.endpoint(w)), Q())

    def vertical(self, p, u, w):
        if u not in self.hu:
            return Q()
        middle = self.hu[u]
        return sum((pa * wb * self.entry('hV', (self.pars[a] * 84 + middle) * 290 + self.chs[b])
                    for a, pa in self.endpoint(p) for b, wb in self.endpoint(w)), Q())

    def cherry(self, u, w1, w2):
        if u not in self.cu:
            return Q()
        total = Q()
        for a, wa in self.endpoint(w1):
            for b, wb in self.endpoint(w2):
                i, j = sorted((self.chs[a], self.chs[b]))
                pair = i * 290 - i * (i - 1) // 2 + j - i
                total += wa * wb * self.entry('hC', self.cu[u] * (290 * 291 // 2) + pair)
        return total

    @staticmethod
    def augmented_core(state):
        if state.stubs != (1,) + (0,) * (state.k - 1):
            raise ValueError('Need exactly one inert stub, incident to core 0.')
        adjacency = state.neighbors()
        parent = [-1, 0] + [-2] * (state.k - 1)
        pending, seen = [0], {0}
        while pending:
            u = pending.pop()
            for v in adjacency[u]:
                if v not in seen:
                    seen.add(v); pending.append(v); parent[v + 1] = u + 1
        children = [[] for _ in parent]
        for v in range(1, len(parent)):
            children[parent[v]].append(v)
        leaves = (1,) + state.leaves
        triples = tuple((leaves[v], len(children[v]), int(v != 0)) for v in range(len(parent)))
        return parent, children, triples

    def psi(self, state):
        parent, children, triples = self.augmented_core(state)
        total = sum((self.vertex(triple) for triple in triples), Q())
        for w in range(1, len(parent)):
            p = parent[w]
            total += self.edge(triples[p], triples[w])
            if parent[p] >= 0:
                total += self.vertical(triples[parent[p]], triples[p], triples[w])
        for u, triple in enumerate(triples):
            if triple in self.cu:
                for w1, w2 in combinations(children[u], 2):
                    total += self.cherry(triple, triples[w1], triples[w2])
        return total

    def chi(self, state):
        """Algebraic large-parent limit with the parent's own weight removed.

        This is a function of the finite component; no infinite random tree
        or infinite-degree process is being constructed.
        """
        parent, children, triples = self.augmented_core(state)
        total = sum((self.vertex(triple) for triple in triples[1:]), Q())
        for w in range(1, len(parent)):
            p = parent[w]
            if p == 0:
                total += sum((weight * self.entry('g', self.inf * 601 + endpoint)
                              for endpoint, weight in self.endpoint(triples[w])), Q())
            else:
                total += self.edge(triples[p], triples[w])
                gp = parent[p]
                if gp == 0:
                    middle = self.hu.get(triples[p])
                    if middle is not None:
                        total += sum((weight * self.entry('hV',
                            (self.pars[self.inf] * 84 + middle) * 290 + self.chs[endpoint])
                            for endpoint, weight in self.endpoint(triples[w])), Q())
                elif gp > 0:
                    total += self.vertical(triples[gp], triples[p], triples[w])
        for u in range(1, len(triples)):
            if triples[u] in self.cu:
                for w1, w2 in combinations(children[u], 2):
                    total += self.cherry(triples[u], triples[w1], triples[w2])
        return total

    @staticmethod
    def denominator(s):
        s = Q(s)
        if s <= NU_STAR:
            raise ValueError(f'This construction is proved only for s>{NU_STAR}.')
        return ETA + (M if s >= NU else A) * (s - NU)

    def u0(self, state, s):
        s = Q(s)
        return self.chi(state) / self.denominator(s)

    def generator_u0(self, state, s):
        old = self.u0(state, s)
        degree, adjacency = state.degrees(), state.neighbors()
        drift = Q()
        for u, leaves in enumerate(state.leaves):
            gain = leaves + sum((Q(1, degree[v]) for v in adjacency[u]), Q())
            drift += gain * (self.u0(state.add_leaf(u), s) - old)
            if leaves:
                drift += Q(leaves, degree[u]) * (self.u0(state.promote(u), s) - old)
        return drift

    def one_step_interval(self, state, s, max_added):
        """Certified interval for T_s U0, integrating its holding reward exactly."""
        s = Q(s)
        nonpromotion, promotion, missing = one_core_ring(state, s, max_added)
        lower = Q(state.k) / (state.k + s)
        for transitions in (nonpromotion, promotion):
            lower += sum((mass * self.u0(next_state, s)
                          for next_state, mass in transitions.items()), Q())
        denominator = self.denominator(s)
        future_bound = A * (state.k + 1) / denominator
        upper = min(self.u0(state, s), lower + missing * future_bound)
        if upper < lower:
            raise AssertionError('Supersolution/kernel interval inconsistency.')
        return lower, upper, missing


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--certificate', type=Path, required=True)
    p.add_argument('--s', default='1133/2000')
    p.add_argument('--max-added', type=int, default=5)
    args = p.parse_args()
    s = Q(args.s)
    state = CoreState((), (1,), (1,))
    with MotifSupersolution(args.certificate) as model:
        lo, hi, missing = model.one_step_interval(state, s, args.max_added)
        u0 = model.u0(state, s)
        residual = s * u0 - model.generator_u0(state, s) - state.k
        assert residual >= 0
        report = {'proved_range': f's>{NU_STAR}', 's': str(s),
                  'chi_newborn': str(model.chi(state)), 'u0_newborn': str(u0),
                  'u0_generator_residual': str(residual),
                  'u0_boundary_increment_bound': str(J / model.denominator(s)),
                  'u1_interval': [str(lo), str(hi)],
                  'omitted_discounted_ring_mass': str(missing),
                  'max_added': args.max_added}
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
