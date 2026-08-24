"""Robust self-similar pure-X: completions AND their +-2 S-neighbors in the
same block must precede. Robustness absorbs anchor-descent drift in pumping."""
import sys, time, json
import numpy as np
from pysat.solvers import Cadical195

def block(v):
    k = (v - 1).bit_length()
    if 2 ** k < v: k += 1
    return k

def sa(hi):
    return [v for v in range(2, hi + 1) if block(v) % 2 == 0]

def solve(X, radius=2):
    V = sa(X)
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
    Vs = set(V)
    def thick(z, b):
        """z and S-neighbors within radius, same block as z"""
        K = block(z)
        out = []
        for dz in range(-radius, radius + 1):
            zz = z + dz
            if zz in Vs and block(zz) == K:
                out.append(zz)
        return out
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
                for zz in thick(c, b):
                    if zz != b and zz != a:
                        cl.append([-before(a, b), before(zz, b)])
            d2 = 2 * a - b
            if d2 >= 1 and d2 in Vs:
                for zz in thick(d2, a):
                    if zz != a and zz != b:
                        cl.append([-before(b, a), before(zz, a)])
    for u in V:
        if 4 * u > X or 4 * u not in Vs: continue
        for w in V:
            if w <= u or 4 * w > X or 4 * w not in Vs: continue
            cl.append([-before(u, w), before(4 * u, 4 * w)])
            cl.append([before(u, w), -before(4 * u, 4 * w)])
    print(f"n={n} clauses={len(cl)}", flush=True)
    s = Cadical195(bootstrap_with=cl)
    t0 = time.time()
    rounds = 0
    while True:
        rounds += 1
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
        if rounds % 25 == 0:
            print(f"round {rounds}: {len(bad_idx)} viol ({time.time()-t0:.0f}s)", flush=True)

if __name__ == "__main__":
    X = int(sys.argv[1])
    r = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    t0 = time.time()
    res = solve(X, r)
    dt = time.time() - t0
    if res is False:
        print(f"ROBUST(r={r}) selfsim-{X}: UNSAT ({dt:.0f}s)", flush=True)
    else:
        print(f"ROBUST(r={r}) selfsim-{X}: SAT ({dt:.0f}s)", flush=True)
        json.dump(res, open(f"data/robust_selfsim{X}_r{r}.json", "w"))
