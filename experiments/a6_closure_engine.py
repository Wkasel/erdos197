#!/usr/bin/env python3
"""AUDIT A6, engine 2: an independent refutation engine that uses ONLY
consequences derivable by hand: the midpoint-extremal rules R1-R4 (each an
immediate consequence of AP-freeness plus totality of a linear order),
transitivity, and exhaustive binary case splits.

R1-R4, derived from the paper's condition (i): for an AP a<b<c in (M,2M],
the placements a<b<c and c<b<a are forbidden.  In a total order this yields
    R1: a<b  =>  c<b        R3: c<b  =>  a<b
    R2: b<c  =>  b<a        R4: b<a  =>  b<c
(e.g. R1: if a<b and also b<c we would have a<b<c; totality then forces c<b.)

If every leaf of the split tree closes with a contradiction (some u<v and
v<u both derived), the hypothesis set is refuted -- a finite, replayable
derivation, independent of any SAT solver.

No code copied from the existing experiment suite.
"""

import sys
import time

CLOSED = 'closed'


class State:
    __slots__ = ('after',)

    def __init__(self, n):
        self.after = [0] * n     # after[u] bitmask: u precedes v for v set

    def copy(self):
        s = State.__new__(State)
        s.after = list(self.after)
        return s


def build(M):
    n = M
    vals = list(range(M + 1, 2 * M + 1))
    idx = {v: i for i, v in enumerate(vals)}
    aps = []
    for b in vals:
        dmax = min(b - (M + 1), 2 * M - b)
        for d in range(1, dmax + 1):
            aps.append((idx[b - d], idx[b], idx[b + d]))
    return n, vals, idx, aps


def propagate(st, n, aps):
    """Close under transitivity + R1-R4. Return True iff contradiction."""
    after = st.after
    changed = True
    while changed:
        changed = False
        # transitivity (bitset Floyd-Warshall sweep)
        for u in range(n):
            au = after[u]
            new = au
            m = au
            while m:
                v = (m & -m).bit_length() - 1
                m &= m - 1
                new |= after[v]
            if new != au:
                after[u] = new
                changed = True
        # midpoint rules
        for a, b, c in aps:
            ab = (after[a] >> b) & 1
            ba = (after[b] >> a) & 1
            bc = (after[b] >> c) & 1
            cb = (after[c] >> b) & 1
            if ab and not cb:            # R1
                after[c] |= 1 << b
                changed = True
            if cb and not ab:            # R3
                after[a] |= 1 << b
                changed = True
            if bc and not ba:            # R2
                after[b] |= 1 << a
                changed = True
            if ba and not bc:            # R4
                after[b] |= 1 << c
                changed = True
    for u in range(n):
        m = after[u]
        while m:
            v = (m & -m).bit_length() - 1
            m &= m - 1
            if (after[v] >> u) & 1:
                return True
    return False


def undecided_pair(st, n, aps, priority):
    after = st.after
    for u, v in priority:
        if not ((after[u] >> v) & 1) and not ((after[v] >> u) & 1):
            return (u, v)
    # fallback: most-constrained undecided pair among AP members
    count = {}
    for a, b, c in aps:
        for (x, y) in ((a, b), (b, c), (a, c)):
            if not ((after[x] >> y) & 1) and not ((after[y] >> x) & 1):
                count[(x, y)] = count.get((x, y), 0) + 1
    if not count:
        return None
    return max(count, key=count.get)


def refute(st, n, aps, priority, depth, log, label):
    if propagate(st, n, aps):
        log.append((depth, label, 'contradiction'))
        return True
    pair = undecided_pair(st, n, aps, priority)
    if pair is None:
        log.append((depth, label, 'SATURATED WITHOUT CONTRADICTION'))
        return False
    u, v = pair
    for (x, y) in ((u, v), (v, u)):
        st2 = st.copy()
        st2.after[x] |= 1 << y
        if not refute(st2, n, aps, priority, depth + 1, log,
                      label + f' [{x}<{y}]'):
            return False
    return True


def run(M, seeds_names, expect_refuted=True):
    n, vals, idx, aps = build(M)
    b3, b5, b6 = idx[M + 3], idx[M + 5], idx[M + 6]
    t3, t5, t10 = idx[2 * M - 3], idx[2 * M - 5], idx[2 * M - 10]
    m0 = idx[3 * M // 2]
    seeds = {
        'A1': (t5, b5), 'A2': (t3, b6), 'A3': (t10, b3),
        'b5b3': (b5, b3), 'b3b5': (b3, b5),
        't5t3': (t5, t3), 't3t5': (t3, t5),
    }
    st = State(n)
    for nm in seeds_names:
        u, v = seeds[nm]
        st.after[u] |= 1 << v
    # split priority: the (m0, t5) comparison, then ladder-phase pairs
    priority = [(m0, t5), (idx[M + 2], idx[M + 4]),
                (idx[M + 1], idx[M + 5]), (idx[M + 3], idx[M + 7])]
    log = []
    t0 = time.time()
    ok = refute(st, n, aps, priority, 0, log, 'root')
    dt = time.time() - t0
    verdict = 'REFUTED' if ok else 'not refuted'
    status = 'AGREE' if ok == expect_refuted else '**DISAGREE**'
    print(f'M={M:4d} closure-engine [{"+".join(seeds_names):20s}] -> '
          f'{verdict} ({len(log)} leaves, max depth '
          f'{max((d for d, _, _ in log), default=0)}) {status} {dt:.1f}s')
    for d, lab, res in log:
        print(f'    depth {d}: {lab} -> {res}')
    return ok == expect_refuted


if __name__ == '__main__':
    Ms = [int(a) for a in sys.argv[1:]] or [48]
    all_ok = True
    for M in Ms:
        all_ok &= run(M, ['A1', 'A2', 'A3', 'b5b3'])      # FLIP
        all_ok &= run(M, ['b5b3', 't5t3'])                # transfer lock dir 1
        all_ok &= run(M, ['b3b5', 't3t5'])                # transfer lock dir 2
    print('ALL AGREE' if all_ok else 'DISAGREEMENT — FIVE-ALARM')
