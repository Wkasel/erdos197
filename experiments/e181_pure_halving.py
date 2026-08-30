#!/usr/bin/env python3
"""e181: Lemma PURE audit (notes/77 SS3.1) — the class-c subsystem of a
same-parity double fan IS the halved double fan, at the SAT level.

Claim (Lemma PURE + converse, notes/77): for a same-parity attacker
pair (q, p) (q ≡ p mod 2, parity e) on window O = [1, N]:

    "dead via a PURE pattern" (some UNSAT S-restricted block-2 theory
    with support inside the class {s ≡ p mod 2})
        ⟺
    the class-c subsystem (order on O ∩ class, in-class APs, fan units
    with in-class midpoints) is UNSAT
        ⟺
    the halved double fan ThFG(q^, p^; N^) is UNSAT, where for p, q
    even: q^ = q/2, p^ = p/2, N^ = floor(N/2) (class = evens, s = 2s^);
    for p, q odd: q^ = (q-1)/2, p^ = (p-1)/2, N^ = ceil(N/2)
    (class = odds, s = 2s^-1).

This script verifies the SECOND equivalence machine-independently:
for every same-parity pair at scale M it solves BOTH theories with a
fresh direct encoding (CaDiCaL; order vars + transitivity + APs +
units) and asserts equal verdicts.  The first equivalence is the
restriction/monotonicity argument (hand, notes/77 SS3.1); the halving
bijection is the hand isomorphism.  A mismatch here would break the
bookkeeping of the isomorphism (window ends / parity of unit sources).

Run: .venv/bin/python experiments/e181_pure_halving.py M [M ...]
Output: data/e181_pure_M{M}.json, data/e181_pure.log (append).
"""
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
DATA = os.path.join(HERE, '..', 'data')
from pysat.solvers import Cadical195

LOG = []


def log(*a):
    s = ' '.join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def solve_theory(points, aps, units):
    """Order theory on `points`: transitivity, AP-midpoint constraints
    for each (a,b,c) in aps, and unit facts (u,v) = u before v.
    Returns True iff SAT."""
    idx = {v: i for i, v in enumerate(points)}
    var = {}

    def o(u, v):
        if (u, v) not in var:
            var[(u, v)] = len(var) + 1
        return var[(u, v)]

    def lit(u, v):
        return o(u, v) if idx[u] < idx[v] else -o(v, u)

    cls = []
    n = len(points)
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                u, v, w = points[i], points[j], points[k]
                a, b, c = o(u, v), o(v, w), o(u, w)
                cls.append([-a, -b, c])
                cls.append([a, b, -c])
    for (a, b, c) in aps:
        cls.append([-lit(a, b), -lit(b, c)])
        cls.append([lit(a, b), lit(b, c)])
    for (u, v) in units:
        cls.append([lit(u, v)])
    with Cadical195(bootstrap_with=cls) as s:
        return s.solve()


def class_subsystem_sat(N, p, q, e):
    """Class-c subsystem at full scale: points = class-e offsets of
    [1,N]; in-class APs; fan units with in-class midpoints."""
    pts = [s for s in range(1, N + 1) if s % 2 == e]
    ptset = set(pts)
    aps = []
    for a in pts:
        d = 2
        while a + 2 * d <= N:
            if (a + d) in ptset:
                aps.append((a, a + d, a + 2 * d))
            d += 2
    units = []
    for r in (p, q):
        for a in pts:
            if 2 * a + r <= N:
                units.append((2 * a + r, a))
                assert (2 * a + r) % 2 == e
    return solve_theory(pts, aps, units)


def halved_fan_sat(Nh, ph, qh):
    """Halved double fan: window [1, Nh], attackers (qh, ph)."""
    pts = list(range(1, Nh + 1))
    aps = []
    for a in pts:
        d = 1
        while a + 2 * d <= Nh:
            aps.append((a, a + d, a + 2 * d))
            d += 1
    units = []
    for r in (ph, qh):
        a = 1
        while 2 * a + r <= Nh:
            units.append((2 * a + r, a))
            a += 1
    return solve_theory(pts, aps, units)


def run(M):
    t0 = time.time()
    N = 2 * M + 15
    log(f'== e181 Lemma PURE bijection audit, M={M} (N={N}) ==')
    n_pairs = n_dead_half = 0
    mism = []
    for q in range(0, M + 15):
        for p in range(q + 2, M + 16, 2):     # same parity
            e = p % 2
            if e == 0:
                ph, qh, Nh = p // 2, q // 2, N // 2
            else:
                ph, qh, Nh = (p - 1) // 2, (q - 1) // 2, (N + 1) // 2
            if qh == ph:
                continue                       # degenerate (q^=p^)
            s1 = class_subsystem_sat(N, p, q, e)
            s2 = halved_fan_sat(Nh, ph, qh)
            n_pairs += 1
            if not s2:
                n_dead_half += 1
            if s1 != s2:
                mism.append((q, p, s1, s2))
    log(f'same-parity pairs audited: {n_pairs}; halved-dead: '
        f'{n_dead_half}; MISMATCHES (must be 0): {len(mism)} '
        f'{mism[:10] if mism else ""}  [{time.time()-t0:.0f}s]')
    out = {'M': M, 'pairs': n_pairs, 'halved_dead': n_dead_half,
           'mismatches': mism}
    with open(os.path.join(DATA, f'e181_pure_M{M}.json'), 'w') as f:
        json.dump(out, f)
    return out


def main():
    Ms = [int(a) for a in sys.argv[1:]] or [48]
    for M in Ms:
        run(M)
    with open(os.path.join(DATA, 'e181_pure.log'), 'a') as f:
        f.write('\n'.join(LOG) + '\n')
    log('e181: DONE')


if __name__ == '__main__':
    main()
