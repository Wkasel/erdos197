#!/usr/bin/env python3
"""e154: GAP-FG-deep — complete SAT/UNSAT classification of the 165
closure-alive (q,p) pairs at M=48.

Base theory (pair-independent): linear order on O = [1, N], N = 2M+15
(order vars o(u,v) for u < v numeric, "u placed before v"), full
transitivity, AP-freeness for every 3-AP inside O.  Per pair (q,p):
fan units as ASSUMPTIONS (literal forcing (2a+r) before a).
One incremental CaDiCaL195 instance, sequential solves (one solver
query at a time).

Output: the exact resonance set R(48) (SAT escapes) and the exact deep
set D(48) (UNSAT but closure-stalled), cross-referenced with the e142b
phase-split kills.
"""
import json, time
from itertools import combinations
from pysat.solvers import Cadical195
from e152_mc_schema import closure_verdict

def main():
    M = 48
    N = 2*M + 15
    t0 = time.time()
    var = {}
    def o(u, v):
        """literal: u placed before v (u < v numeric)."""
        assert u < v
        if (u, v) not in var:
            var[(u, v)] = len(var) + 1
        return var[(u, v)]
    def lit(u, v):
        """literal for 'u placed before v' for any u != v."""
        return o(u, v) if u < v else -o(v, u)

    cls = []
    # transitivity on all triples u < v < w
    for u, v, w in combinations(range(1, N + 1), 3):
        cls.append([-o(u, v), -o(v, w), o(u, w)])
        cls.append([o(u, v), o(v, w), -o(u, w)])
    # AP-freeness
    nap = 0
    for a in range(1, N + 1):
        for b in range(a + 1, N + 1):
            c = 2*b - a
            if c <= N:
                cls.append([-o(a, b), -o(b, c)])
                cls.append([o(a, b), o(b, c)])
                nap += 1
    print(f'base: {len(var)} vars, {len(cls)} clauses, {nap} APs '
          f'[{time.time()-t0:.1f}s]', flush=True)

    log = []
    def p_(*a):
        s = ' '.join(str(x) for x in a); print(s, flush=True); log.append(s)

    # closure-alive pairs
    alive = []
    for q in range(0, M + 15):
        for p in range(q + 1, M + 16):
            ref, _ = closure_verdict(M, p, q)
            if not ref:
                alive.append((q, p))
    p_(f'closure-alive pairs: {len(alive)}')

    with Cadical195(bootstrap_with=cls) as S:
        sat_set, unsat_set = [], []
        for (q, p) in alive:
            assume = []
            for r in (p, q):
                a = 1
                while 2*a + r <= N:
                    assume.append(lit(2*a + r, a))
                    a += 1
            res = S.solve(assumptions=assume)
            (sat_set if res else unsat_set).append((q, p))
        p_(f'SAT (true resonance escapes): {len(sat_set)}')
        p_('R(48) =', sat_set)
        p_(f'UNSAT (deep, split-needed): {len(unsat_set)}')
        p_('D(48) =', unsat_set)

    # anatomy
    from collections import Counter
    p_('R gaps:', dict(sorted(Counter(pp - qq for qq, pp in sat_set).items())))
    p_('R q-values:', dict(sorted(Counter(qq for qq, pp in sat_set).items())))
    p_('D gaps:', dict(sorted(Counter(pp - qq for qq, pp in unsat_set).items())))
    p_('D min q:', min((qq for qq, pp in unsat_set), default=None),
       ' D max q:', max((qq for qq, pp in unsat_set), default=None))
    p_(f'total {time.time()-t0:.1f}s')
    with open('data/e154_deep_classify.json', 'w') as f:
        json.dump({'M': M, 'R': sat_set, 'D': unsat_set}, f)
    with open('data/e154_deep_classify.log', 'w') as f:
        f.write('\n'.join(log) + '\n')

if __name__ == '__main__':
    main()
