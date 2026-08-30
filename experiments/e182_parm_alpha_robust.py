#!/usr/bin/env python3
"""e182: independent verification of the e155c alpha-robustness kill
(notes/77 SS4.5, Theorem P-ARM''').

Fresh encoder, deliberately different from e155/e155c: FULL-SCALE
coordinates (no halving), Glucose42 (not Cadical195), direct clause
building.  For scale M and parity class c: points = class-c band
values [3M-15, 4M] minus a removed set; constraints = transitivity +
AP-midpoint pairs for in-class APs + alpha units z < y for every A2
AP (x, y, z) with x = 2y - z in [2M-30, 2M] and y, z in the point
set.  Checks, for each maximal clique Q of the e155b SAT-alive graph
(lifted to full scale) and for random sub-cliques:

    system minus Q         UNSAT?   (the Case-S kill)
    system minus Q' (Q'⊂Q) UNSAT?   (a-fortiori sanity, sampled)

Run: .venv/bin/python experiments/e182_parm_alpha_robust.py m [m ...]
Log: data/e182_alpha_robust.log (append) + .json
"""
import itertools
import json
import os
import random
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
DATA = os.path.join(HERE, '..', 'data')
from pysat.solvers import Glucose42

LOG = []


def log(*a):
    s = ' '.join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def alpha_unsat(M, parity, removed):
    pts = [v for v in range(3 * M - 15, 4 * M + 1)
           if v % 2 == parity and v not in removed]
    ps = set(pts)
    var = {}

    def o(u, v):
        if (u, v) not in var:
            var[(u, v)] = len(var) + 1
        return var[(u, v)]

    def lit(u, v):
        return o(u, v) if u < v else -o(v, u)

    cls = []
    n = len(pts)
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                cls.append([-lit(pts[i], pts[j]), -lit(pts[j], pts[k]),
                            lit(pts[i], pts[k])])
                cls.append([lit(pts[i], pts[j]), lit(pts[j], pts[k]),
                            -lit(pts[i], pts[k])])
    for a in pts:
        d = 2
        while a + 2 * d <= 4 * M:
            if a + d in ps and a + 2 * d in ps:
                cls.append([-lit(a, a + d), -lit(a + d, a + 2 * d)])
                cls.append([lit(a, a + d), lit(a + d, a + 2 * d)])
            d += 2
    n_units = 0
    for y in pts:
        for z in pts:
            if z <= y:
                continue
            x = 2 * y - z
            if 2 * M - 30 <= x <= 2 * M:
                cls.append([lit(z, y)])
                n_units += 1
    with Glucose42(bootstrap_with=cls) as s:
        return not s.solve(), n_units


def maximal_cliques(edges):
    verts = sorted(set(x for p in edges for x in p))
    adj = {v: set() for v in verts}
    for (a, b) in edges:
        adj[a].add(b)
        adj[b].add(a)
    out = []

    def bk(r, p, x):
        if not p and not x:
            out.append(sorted(r))
            return
        pivot = max(p | x, key=lambda u: len(adj[u]), default=None)
        for v in list(p - (adj[pivot] if pivot else set())):
            bk(r | {v}, p & adj[v], x & adj[v])
            p.discard(v)
            x.add(v)
    bk(set(), set(verts), set())
    return out


def main():
    random.seed(182)
    with open(os.path.join(DATA, 'e155_parm_hyp.json')) as f:
        res = json.load(f)
    summary = {}
    for marg in sys.argv[1:]:
        m = int(marg)
        M = 2 * m
        for parity, wname in ((1, 'W2o'), (0, 'W2e')):
            t0 = time.time()
            off = 1 if parity == 1 else 0
            sat_alive = [tuple(p) for p in
                         res[str(m)]['B'][wname]['sat_alive']]
            cliqs = maximal_cliques(sat_alive)
            n_sat = 0
            checked = 0
            for Q in cliqs:
                rem = tuple(2 * q - off for q in Q)
                uns, nu = alpha_unsat(M, parity, rem)
                checked += 1
                if not uns:
                    n_sat += 1
                    log(f'  !! e182 m={m} {wname}: SAT after removing '
                        f'clique {Q}')
                # sampled sub-clique (a-fortiori sanity)
                if len(Q) >= 2 and random.random() < 0.3:
                    k = random.randrange(1, len(Q))
                    sub = tuple(sorted(random.sample(Q, k)))
                    rem2 = tuple(2 * q - off for q in sub)
                    uns2, _ = alpha_unsat(M, parity, rem2)
                    checked += 1
                    if not uns2:
                        n_sat += 1
                        log(f'  !! e182 m={m} {wname}: SAT after '
                            f'removing SUB-clique {sub}')
            log(f'e182 m={m} {"odd" if parity else "even"} class: '
                f'{len(cliqs)} maximal cliques + sampled sub-cliques '
                f'({checked} solves, fresh Glucose42 full-scale '
                f'encoder): SAT verdicts (MUST be 0): {n_sat} '
                f'[{time.time()-t0:.0f}s]')
            summary[f'{m}_{wname}'] = {'cliques': len(cliqs),
                                       'solves': checked,
                                       'n_sat': n_sat}
    with open(os.path.join(DATA, 'e182_alpha_robust.json'), 'w') as f:
        json.dump(summary, f)
    with open(os.path.join(DATA, 'e182_alpha_robust.log'), 'a') as f:
        f.write('\n'.join(LOG) + '\n')
    log('e182: DONE')


if __name__ == '__main__':
    main()
