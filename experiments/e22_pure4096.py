"""Decide pure-complete-4096 (n=2730). Numpy-accelerated lazy transitivity."""
import sys, time
import numpy as np
sys.path.insert(0, 'experiments')
from pysat.solvers import Cadical195

def block(v):
    k = (v - 1).bit_length()
    if 2 ** k < v: k += 1
    return k

def sa(hi):
    return [v for v in range(2, hi + 1) if block(v) % 2 == 0]

def solve_pure(X, max_rounds=4000):
    V = sa(X)
    idx = {v: i for i, v in enumerate(V)}
    n = len(V)
    print(f"n={n}", flush=True)
    top = 0
    t = {}
    for i in range(n):
        for j in range(i + 1, n):
            top += 1
            t[(i, j)] = top
    def before(u, w):
        i, j = idx[u], idx[w]
        return t[(i, j)] if i < j else -t[(j, i)]
    cl = []
    Vs = set(V)
    for y in V:
        d = 1
        while y + d <= X:
            a, c = y - d, y + d
            if a in Vs and c in Vs:
                cl.append([-before(a, y), -before(y, c)])
                cl.append([-before(c, y), -before(y, a)])
            d += 1
    for a in V:
        for b in V:
            if b <= a: continue
            c = 2 * b - a
            if c in Vs:
                cl.append([-before(a, b), before(c, b)])
            d2 = 2 * a - b
            if d2 >= 1 and d2 in Vs:
                cl.append([-before(b, a), before(d2, a)])
    print(f"clauses={len(cl)}", flush=True)
    s = Cadical195(bootstrap_with=cl)
    rounds = 0
    t0 = time.time()
    while True:
        rounds += 1
        if rounds > max_rounds:
            raise RuntimeError("rounds")
        if not s.solve():
            return False
        model = s.get_model()
        pos = np.zeros(top + 1, dtype=bool)
        for l in model:
            if 0 < l <= top:
                pos[l] = True
        B = np.zeros((n, n), dtype=bool)
        for (i, j), var in t.items():
            if pos[var]:
                B[i, j] = True
            else:
                B[j, i] = True
        wins = B.sum(axis=1)
        order = np.argsort(-wins, kind='stable')
        R = B[np.ix_(order, order)]
        iu = np.triu_indices(n, 1)
        badmask = ~R[iu]
        bad_idx = np.nonzero(badmask)[0]
        if len(bad_idx) == 0:
            return [V[i] for i in order]
        added = 0
        for bi in bad_idx[:30000]:
            a_, b_ = iu[0][bi], iu[1][bi]
            i, j = order[a_], order[b_]
            ks = np.nonzero(B[i] & B[:, j])[0]
            if len(ks):
                k = int(ks[0])
                u, w, x = V[i], V[k], V[j]
                s.add_clause([-before(u, w), -before(w, x), before(u, x)])
                added += 1
                if added > 20000:
                    break
        if rounds % 20 == 0:
            print(f"round {rounds}: {len(bad_idx)} viol, {time.time()-t0:.0f}s", flush=True)

if __name__ == "__main__":
    t0 = time.time()
    r = solve_pure(4096)
    dt = time.time() - t0
    if r is False:
        print(f"PURE-4096: UNSAT ({dt:.0f}s)  <-- DYADIC PARTITION DEAD", flush=True)
    else:
        print(f"PURE-4096: SAT ({dt:.0f}s)", flush=True)
        import json
        json.dump(r, open('data/pure4096.json', 'w'))
