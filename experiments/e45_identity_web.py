"""HS identity web for S_A: for every ray a, a+d, ..., a+(2t+4)d fully inside
S_A (t odd), the chaotic-order identity f(a)≺f(a+d) ⟺ f(a+sd)≺f(a+td) holds
(s even < t odd; per HS Lemmas 2.4/2.5, needing ~run up to a+2(t+2)d).
Add all such biconditionals to the pure-complete system and decide.
"""
import sys, time
import numpy as np
from pysat.solvers import Cadical195

def block(v):
    k = (v - 1).bit_length()
    if 2 ** k < v: k += 1
    return k

def sa(hi):
    return [v for v in range(2, hi + 1) if block(v) % 2 == 0]

def solve(X, with_web=True, max_rounds=100000):
    V = sa(X)
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
    for y in V:
        d = 1
        while y + d <= X:
            x, z = y - d, y + d
            if x in Vs and z in Vs:
                cl.append([-before(x, y), -before(y, z)])
                cl.append([-before(z, y), -before(y, x)])
            d += 1
    web = 0
    if with_web:
        # identities: need run a + i*d in S_A for i = 0..2(t+2); then for
        # s even in [0, t): f(a)<f(a+d) <-> f(a+s d)<f(a+t d)
        for d in range(1, X // 6 + 1):
            for a in V:
                # longest run from a with difference d
                L = 0
                while a + (L + 1) * d <= X and (a + (L + 1) * d) in Vs:
                    L += 1
                # t odd with 2(t+2) <= L
                tmax = L // 2 - 2
                for tt in range(3, tmax + 1, 2):
                    for ss in range(0, tt, 2):
                        u1, w1 = a, a + d
                        u2, w2 = a + ss * d, a + tt * d
                        if u2 == w2: continue
                        l1 = before(u1, w1)
                        l2 = before(u2, w2)
                        cl.append([-l1, l2])
                        cl.append([l1, -l2])
                        web += 1
    print(f"X={X} n={n} web-identities={web} clauses={len(cl)}", flush=True)
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
    for X in [64, 256, 1024]:
        t0 = time.time()
        r = solve(X, with_web=True)
        print(f"identity-web pure-{X}: {'SAT' if r else 'UNSAT'} ({time.time()-t0:.0f}s)", flush=True)
        if r is False:
            break
