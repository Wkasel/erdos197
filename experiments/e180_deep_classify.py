#!/usr/bin/env python3
"""e180: GAP-FG-deep cross-scale audit (notes/77 SS2) — scale-generic
version of e154_deep_classify (which was hard-coded to M=48).

For each scale M: load the closure-ALIVE (q,p) pairs from the e146
catalogue (alive = grid minus fg patterns), build ONE incremental
CaDiCaL195 instance with the pair-independent base theory (linear
order on O = [1, N], N = 2M+15; full transitivity; AP-freeness for
every 3-AP inside O), then classify each alive pair SAT/UNSAT with its
fan units as assumptions.

Uniform claims under audit (exact at 48, notes/59 SSC.1):
  (RES-LAW)  every SAT escape has p - q ≡ 0 (mod 8);
  (DEEP-LAW) the UNSAT stalls are EXACTLY the pairs with both
             attackers in E1 (q, p ∈ [M, M+15]) and 8 ∤ (p−q);
  (CLOSE-LAW) distance ≤ 15 escapes are exactly gap-8 pairs in E1×E1.

Run: .venv/bin/python experiments/e180_deep_classify.py M [M ...]
Output: data/e180_deep_M{M}.json, data/e180_deep.log (append).
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


def run(M):
    t0 = time.time()
    N = 2 * M + 15
    log(f'== e180 deep classification, M={M} (N={N}) ==')
    with open(os.path.join(DATA, f'e146_catalogue_M{M}.json')) as f:
        cat = json.load(f)
    dead = set()
    for pat in cat:
        src = pat.get('src', '')
        if src.startswith('fg('):
            qq, pp = src[3:-1].split(',')
            dead.add((int(qq), int(pp)))
    alive = [(q, p) for q in range(0, M + 15)
             for p in range(q + 1, M + 16) if (q, p) not in dead]
    log(f'closure-alive pairs: {len(alive)}')

    var = {}

    def o(u, v):
        assert u < v
        if (u, v) not in var:
            var[(u, v)] = len(var) + 1
        return var[(u, v)]

    def lit(u, v):
        """literal: u placed before v (any u != v)."""
        return o(u, v) if u < v else -o(v, u)

    cls = []
    # transitivity on all ordered triples
    for u in range(1, N + 1):
        for v in range(u + 1, N + 1):
            for w in range(v + 1, N + 1):
                a, b, c = o(u, v), o(v, w), o(u, w)
                cls.append([-a, -b, c])
                cls.append([a, b, -c])
    # AP-freeness
    n_ap = 0
    for a in range(1, N + 1):
        for d in range(1, (N - a) // 2 + 1):
            b, c = a + d, a + 2 * d
            cls.append([-o(a, b), -o(b, c)])
            cls.append([o(a, b), o(b, c)])
            n_ap += 1
    log(f'base theory: {len(var)} vars, {len(cls)} clauses ({n_ap} APs) '
        f'[{time.time()-t0:.0f}s]')
    solver = Cadical195(bootstrap_with=cls)

    res = {}
    for (q, p) in sorted(alive):
        assume = []
        for r in (p, q):
            a = 1
            while 2 * a + r <= N:
                assume.append(lit(2 * a + r, a))
                a += 1
        t1 = time.time()
        sat = solver.solve(assumptions=assume)
        res[(q, p)] = (sat, round(time.time() - t1, 2))
    R = sorted(qp for qp, (s, _) in res.items() if s)
    D = sorted(qp for qp, (s, _) in res.items() if not s)
    log(f'R(M) SAT escapes: {len(R)};  D(M) UNSAT stalls: {len(D)} '
        f'[total {time.time()-t0:.0f}s]')

    # ---- law audits ----
    e1 = lambda q, p: (M <= q <= M + 15) and (M <= p <= M + 15)
    bad_res = [(q, p) for (q, p) in R if (p - q) % 8 != 0]
    log(f'(RES-LAW) SAT escapes with 8 not| gap (MUST be 0): '
        f'{len(bad_res)} {bad_res or ""}')
    pred_D = sorted((q, p) for (q, p) in res
                    if e1(q, p) and (p - q) % 8 != 0)
    exact = pred_D == D
    log(f'(DEEP-LAW) D(M) == E1xE1 non-mod-8 alive pairs: {exact}')
    if not exact:
        log(f'   D minus pred: {sorted(set(D)-set(pred_D))[:20]}')
        log(f'   pred minus D: {sorted(set(pred_D)-set(D))[:20]}')
    close_esc = [(q, p) for (q, p) in R if p - q <= 15]
    bad_close = [(q, p) for (q, p) in close_esc
                 if not (e1(q, p) and p - q == 8)]
    log(f'(CLOSE-LAW) distance<=15 escapes: {len(close_esc)}; '
        f'violators (not gap-8 E1xE1, MUST be 0): {len(bad_close)} '
        f'{bad_close or ""}')
    gaps_R = sorted(set(p - q for (q, p) in R))
    log(f'R gaps realized: {gaps_R}')
    qmin_R = min((q for q, p in R), default=None)
    log(f'R q-range: {qmin_R}..{max((q for q,p in R), default=None)}')
    slow = sorted(res.items(), key=lambda kv: -kv[1][1])[:3]
    log(f'slowest solves: {[(qp, t) for qp, (s, t) in slow]}')
    out = {'M': M, 'alive': len(alive),
           'R': R, 'D': D,
           'res_law_ok': not bad_res, 'deep_law_ok': exact,
           'close_law_ok': not bad_close,
           'close_escapes': close_esc}
    with open(os.path.join(DATA, f'e180_deep_M{M}.json'), 'w') as f:
        json.dump(out, f)
    solver.delete()
    return out


def main():
    Ms = [int(a) for a in sys.argv[1:]] or [64]
    for M in Ms:
        run(M)
    with open(os.path.join(DATA, 'e180_deep.log'), 'a') as f:
        f.write('\n'.join(LOG) + '\n')
    log('e180: DONE')


if __name__ == '__main__':
    main()
