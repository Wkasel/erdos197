#!/usr/bin/env python3
"""a7 audit: cross-scale check of the notes/59 §C resonance/deep laws.

e154_deep_classify parametrized to any M (author ran M = 48 only).
Laws under test at the new scale:
  (1) resonance law: every SAT-escape pair has 8 | (p - q);
  (2) deep law: the UNSAT-stall set is exactly the non-resonant part
      of the E1×E1 corner (both attackers in E1, i.e. q >= M - 16);
  (3) close-pair law: every distance-<=15 escape has both attackers
      in E1 (gap-8 pairs inside E1×E1).
Usage: a7_deep_crossscale.py M
"""
import json, sys, time
from itertools import combinations
sys.path.insert(0, 'experiments')
from pysat.solvers import Cadical195
from e152_mc_schema import closure_verdict

def main():
    M = int(sys.argv[1])
    N = 2*M + 15
    t0 = time.time()
    var = {}
    def o(u, v):
        assert u < v
        if (u, v) not in var:
            var[(u, v)] = len(var) + 1
        return var[(u, v)]
    def lit(u, v):
        return o(u, v) if u < v else -o(v, u)
    cls = []
    for u, v, w in combinations(range(1, N + 1), 3):
        cls.append([-o(u, v), -o(v, w), o(u, w)])
        cls.append([o(u, v), o(v, w), -o(u, w)])
    for a in range(1, N + 1):
        for b in range(a + 1, N + 1):
            c = 2*b - a
            if c <= N:
                cls.append([-o(a, b), -o(b, c)])
                cls.append([o(a, b), o(b, c)])
    print(f'base built [{time.time()-t0:.0f}s]', flush=True)
    alive = [(q, p) for q in range(0, M + 15) for p in range(q + 1, M + 16)
             if not closure_verdict(M, p, q)[0]]
    print(f'closure-alive pairs: {len(alive)} [{time.time()-t0:.0f}s]',
          flush=True)
    sat_set, unsat_set = [], []
    with Cadical195(bootstrap_with=cls) as S:
        for (q, p) in alive:
            assume = []
            for r in (p, q):
                a = 1
                while 2*a + r <= N:
                    assume.append(lit(2*a + r, a))
                    a += 1
            (sat_set if S.solve(assumptions=assume) else unsat_set).append((q, p))
    res_ok = all((p - q) % 8 == 0 for q, p in sat_set)
    e1 = M - 16          # q >= M-16 <=> attacker x2 = 4M-q <= 3M+16? NB:
    # E1 = [3M-15, 3M] <=> offset q in [M, M+15]; but attackers live at
    # 4M-q with q <= M+15, so E1xE1 <=> q >= M (both offsets >= M).
    deep_in_corner = all(q >= M and 8*((p - q) % 8 != 0)
                         for q, p in unsat_set) if unsat_set else True
    deep_exact = all(qq >= M and (pp - qq) % 8 != 0 for qq, pp in unsat_set)
    # exactness other direction: non-resonant E1xE1 alive pairs all in D
    nonres_e1_alive = [(q, p) for (q, p) in alive
                       if q >= M and (p - q) % 8 != 0]
    other_dir = sorted(nonres_e1_alive) == sorted(unsat_set)
    close_escapes = [(q, p) for q, p in sat_set if p - q <= 15]
    close_law = all(q >= M and (p - q) == 8 for q, p in close_escapes)
    print(f'M={M}: alive {len(alive)} -> SAT {len(sat_set)} / UNSAT '
          f'{len(unsat_set)}', flush=True)
    print(f'  resonance law (8 | gap on ALL escapes): '
          f'{"OK" if res_ok else "VIOLATED " + str([x for x in sat_set if (x[1]-x[0])%8][:8])}')
    print(f'  deep law (D = non-resonant E1xE1, q >= M): '
          f'{"OK" if deep_exact and other_dir else "VIOLATED"}'
          f'  (D subset: {deep_exact}, converse: {other_dir})')
    print(f'  close-pair law (dist<=15 escapes = gap-8 E1xE1): '
          f'{"OK" if close_law else "VIOLATED"}  '
          f'({len(close_escapes)} close escapes)')
    print(f'  R gaps: {sorted(set(p-q for q,p in sat_set))}')
    print(f'  D q-range: '
          f'{[min(q for q,_ in unsat_set), max(q for q,_ in unsat_set)] if unsat_set else None}'
          f'  D gaps: {sorted(set(p-q for q,p in unsat_set))}')
    print(f'total {time.time()-t0:.0f}s')
    with open(f'data/e157_audit_deep_M{M}.json', 'w') as f:
        json.dump({'M': M, 'R': sat_set, 'D': unsat_set,
                   'laws': {'resonance': res_ok,
                            'deep_exact': bool(deep_exact and other_dir),
                            'close': bool(close_law)}}, f)

if __name__ == '__main__':
    main()
