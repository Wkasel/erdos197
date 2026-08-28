"""e141: minimal value-support of the double-fan refutation (GAP-FG).

Greedy deletion MUS over P2-core VALUES: keep the double-fan
instance (AP-freeness on surviving values + fans of X restricted to
surviving values) UNSAT while deleting values one at a time
(descending).  The surviving support is the FG core — the input for
the uniform hand schema (which ladders/mirrors carry the fan
contradiction).

Runs: M=48 X=(192,191); M=48 X=(129,130); M=64 X=(256,255).
Anchor-coordinate anatomy printed for each.

Run: .venv/bin/python experiments/e141_fg_mus.py
Log: data/e141_fg_mus.log
"""
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from pysat.solvers import Cadical195


def fg_solve(M, X, support):
    V = sorted(support)
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
        for d in range(1, (V[-1] - V[0]) // 2 + 1):
            a, c = b - d, b + d
            if a in Vs and c in Vs:
                cls.append([-lit(a, b), -lit(b, c)])
                cls.append([lit(a, b), lit(b, c)])
    for x in X:
        for y in V:
            z = 2 * y - x
            if z != y and z in Vs:
                cls.append([lit(z, y)])
    for i in range(n):
        for j in range(i + 1, n):
            xij = off[(i, j)]
            for k in range(j + 1, n):
                cls.append([-xij, -off[(j, k)], off[(i, k)]])
                cls.append([xij, off[(j, k)], -off[(i, k)]])
    with Cadical195(bootstrap_with=cls) as s:
        return s.solve()          # True = SAT


def mus(M, X):
    t0 = time.time()
    support = list(range(4 * M + 1, 6 * M + 16))
    assert not fg_solve(M, X, support), (M, X, 'not UNSAT to start')
    for v in sorted(support, reverse=True):
        trial = [w for w in support if w != v]
        if not fg_solve(M, X, trial):
            support = trial
    el = time.time() - t0
    # anatomy
    sup = sorted(support)
    runs = []
    st = prev = sup[0]
    for v in sup[1:]:
        if v == prev + 1:
            prev = v
            continue
        runs.append((st, prev))
        st = prev = v
    runs.append((st, prev))
    print(f'  M={M} X={X}: |core|={len(sup)} [{el:.0f}s]', flush=True)
    print(f'    runs (absolute): {runs}', flush=True)
    print(f'    runs (offsets from 4M): '
          f'{[(a - 4 * M, b - 4 * M) for (a, b) in runs]}', flush=True)
    print(f'    runs (offsets from 6M): '
          f'{[(a - 6 * M, b - 6 * M) for (a, b) in runs]}', flush=True)
    return sup


def main():
    mus(48, (192, 191))
    mus(48, (129, 130))
    mus(64, (256, 255))
    print('e141: DONE', flush=True)


if __name__ == '__main__':
    main()
