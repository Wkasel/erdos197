"""e140: SS5 probes — where (2,2,2) enters, and the two reduction cores.

Part H  The halved parity core H(m): single team, single order on
        W1 = [3m-7, 4m], W2 = [4m+1, 6m+7(+1)], block order W1 < W2,
        no monotone 3-AP.  notes/55 SS5 proves: the complementary
        parity coloring of CI(M) is feasible iff H_even(M/2) and
        H_odd(M/2) are both SAT.  The e135 lock therefore predicts
        UNSAT here; verify directly at m = 16, 24, 32, 40.

Part B  Bound-profile frontier on CORE'(48): decomposed encoding
        (e136) at bounds (2,1,1), (1,2,1), (1,1,2), (2,2,1),
        (2,1,2), (1,2,2) — which coordinates of (2,2,2) are
        load-bearing.  SAT witnesses: dump per-team block profiles.

Part F  Double-fan gadget FG(M; X): AP-free order of P2-core
        [4M+1, 6M+15] + the unguarded fan units z < y (z = 2y - x
        in core) for each x in X.  The (1,1,1) escape realizes a
        single fan; test X = {4M}, {4M,4M-1}, {4M,4M-2},
        {4M-1,4M-3} at M = 48 to isolate what a SECOND band value
        buys (the conjectured role of the middle 2 in (2,2,2)).

Run: .venv/bin/python experiments/e140_bounds_probes.py
Log: data/e140_probes.log
"""
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from e136_u_decomp_check import solve_decomposed

from pysat.solvers import Cadical195


def order_theory(vals, unit_pairs, block_split=None):
    """SAT check: linear order on vals, AP-free (in-set APs), plus
    units (u, w) meaning u < w, plus optional block order (all of
    block A before all of block B).  Returns verdict, secs."""
    V = sorted(vals)
    n = len(V)
    idx = {v: i for i, v in enumerate(V)}
    off = {}
    top = 0
    for i in range(n):
        for j in range(i + 1, n):
            top += 1
            off[(i, j)] = top

    def lit(u, w):
        i, j = idx[u], idx[w]
        return off[(i, j)] if i < j else -off[(j, i)]

    Vs = set(V)
    cls = []
    for b in V:
        for d in range(1, min(b - V[0], V[-1] - b) + 1):
            a, c = b - d, b + d
            if a in Vs and c in Vs:
                cls.append([-lit(a, b), -lit(b, c)])
                cls.append([lit(a, b), lit(b, c)])
    for (u, w) in unit_pairs:
        cls.append([lit(u, w)])
    if block_split is not None:
        A, B = block_split
        for u in A:
            for w in B:
                cls.append([lit(u, w)])
    for i in range(n):
        for j in range(i + 1, n):
            xij = off[(i, j)]
            for k in range(j + 1, n):
                cls.append([-xij, -off[(j, k)], off[(i, k)]])
                cls.append([xij, off[(j, k)], -off[(i, k)]])
    t0 = time.time()
    with Cadical195(bootstrap_with=cls) as s:
        ok = s.solve()
    return ('SAT' if ok else 'UNSAT'), round(time.time() - t0, 1)


def partH():
    print('== part H: halved parity core H(m) ==', flush=True)
    for m in (16, 24, 32, 40):
        for tag, w2hi in (('even', 6 * m + 7), ('odd', 6 * m + 8)):
            W1 = list(range(3 * m - 7, 4 * m + 1))
            W2 = list(range(4 * m + 1, w2hi + 1))
            v, el = order_theory(W1 + W2, [], block_split=(W1, W2))
            print(f'  H_{tag}({m}) |W1|={len(W1)} |W2|={len(W2)}: '
                  f'{v} [{el}s]', flush=True)


def partB():
    print('== part B: bound-profile frontier on CORE\'(48) ==', flush=True)
    M = 48
    for bounds in ((2, 1, 1), (1, 2, 1), (1, 1, 2),
                   (2, 2, 1), (2, 1, 2), (1, 2, 2)):
        v, el, info = solve_decomposed(M, bounds)
        line = f'  bounds {bounds}: {v} [{el}s]'
        if v == 'SAT':
            profs = {}
            for team in 'AB':
                col = info[team]
                profs[team] = [len([x for x in col if x <= 2 * M]),
                               len([x for x in col if 2 * M < x <= 4 * M]),
                               len([x for x in col if x > 4 * M])]
            line += f'  profiles A{profs["A"]} B{profs["B"]}'
            small = min(('A', 'B'), key=lambda t: len(info[t]))
            line += f'  minority {small}: {sorted(info[small])[:60]}'
        print(line, flush=True)


def fan_units(M, x):
    """Fan of x in P2-core: units (z, y) = z placed before y, for
    y, z = 2y - x both in the core."""
    lo, hi = 4 * M + 1, 6 * M + 15
    out = []
    for y in range(lo, hi + 1):
        z = 2 * y - x
        if z != y and lo <= z <= hi:
            out.append((z, y))
    return out


def partF():
    print('== part F: double-fan gadget on P2-core, M=48 ==', flush=True)
    M = 48
    core = list(range(4 * M + 1, 6 * M + 16))
    for X in ((4 * M,), (4 * M, 4 * M - 1), (4 * M, 4 * M - 2),
              (4 * M - 1, 4 * M - 3)):
        units = []
        for x in X:
            units += fan_units(M, x)
        v, el = order_theory(core, units)
        print(f'  FG(48; X={X}) units={len(units)}: {v} [{el}s]',
              flush=True)


def main():
    partH()
    partB()
    partF()
    print('e140: DONE', flush=True)


if __name__ == '__main__':
    main()
