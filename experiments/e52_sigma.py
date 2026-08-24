"""Sigma(X): the order-independent extension system from notes/16.
V = (9X, 16X]; S1 absorption, S2 zone descents, S3 forced ascents."""
import sys, time, json
import numpy as np
from pysat.solvers import Cadical195

def sigma(X, max_rounds=100000):
    V = list(range(9 * X + 1, 16 * X + 1))
    Vs = set(V)
    idx = {v: i for i, v in enumerate(V)}
    n = len(V)
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
    # S1 increasing: pair (a<b) placed increasing => c=2b-a (<=16X, in V) before b
    #    (c in (16X,...] free; c<=9X impossible since c>b>9X)
    # S1 decreasing: pair (b ≺ a with b>a i.e. placed-first larger): c=2a-b in V => c ≺ a
    for a in V:
        for b in V:
            if b <= a: continue
            c = 2 * b - a
            if c <= 16 * X and c in Vs:
                cl.append([-before(a, b), before(c, b)])
            d2 = 2 * a - b
            if d2 in Vs:
                cl.append([-before(b, a), before(d2, a)])
    # S2: y < z with 2y - z in (9X/4, 4X]: z ≺ y
    for y in V:
        for z in V:
            if z <= y: continue
            x = 2 * y - z
            if 9 * X < 4 * x <= 16 * X and x <= 4 * X and 4 * x > 9 * X:
                # x in (9X/4, 4X]
                cl.append([before(z, y)])
    # S3: u < w with 2u - w in (2X, 9X/4] or (8X, 9X]: u ≺ w
    for u in V:
        for w in V:
            if w <= u: continue
            c = 2 * u - w
            if (2 * X < c and 4 * c <= 9 * X) or (8 * X < c <= 9 * X):
                cl.append([before(u, w)])
    print(f"X={X}: n={n} clauses={len(cl)}", flush=True)
    s = Cadical195(bootstrap_with=cl)
    t0 = time.time()
    rounds = 0
    while True:
        rounds += 1
        if rounds > max_rounds:
            raise RuntimeError("rounds")
        if not s.solve():
            return False
        model = s.get_model()
        posb = np.zeros(top + 1, dtype=bool)
        for l in model:
            if 0 < l <= top: posb[l] = True
        B = np.zeros((n, n), dtype=bool)
        for (i, j), var in t.items():
            if posb[var]: B[i, j] = True
            else: B[j, i] = True
        wins = B.sum(axis=1)
        order = np.argsort(-wins, kind='stable')
        R = B[np.ix_(order, order)]
        iu = np.triu_indices(n, 1)
        bad_idx = np.nonzero(~R[iu])[0]
        if len(bad_idx) == 0:
            return [V[i] for i in order]
        added = 0
        for bi in bad_idx[:40000]:
            a_, b_ = iu[0][bi], iu[1][bi]
            i, j = int(order[a_]), int(order[b_])
            ks = np.nonzero(B[i] & B[:, j])[0]
            if len(ks):
                k = int(ks[0])
                s.add_clause([-before(V[i], V[k]), -before(V[k], V[j]),
                              before(V[i], V[j])])
                added += 1
                if added > 30000: break
        if rounds % 50 == 0:
            print(f"  round {rounds}: {len(bad_idx)} ({time.time()-t0:.0f}s)", flush=True)

if __name__ == "__main__":
    for X in [4, 8, 16, 32, 64]:
        t0 = time.time()
        r = sigma(X)
        tag = 'UNSAT  <-- scheme dead at ALL scales (halving)' if r is False else 'SAT'
        print(f"SIGMA({X}): {tag} ({time.time()-t0:.0f}s)", flush=True)
        if r is not False:
            json.dump(r, open(f'data/sigma{X}.json', 'w'))
        else:
            break
