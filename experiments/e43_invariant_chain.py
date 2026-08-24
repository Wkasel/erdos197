"""Invariant-chain test: does the g-witness state-profile chain across scales?

State(X): order on P(X) = S_A∩[1,X] ∪ (block(2X..4X) minus class-1-mod-8),
doom-free, where the missing reservoir is exactly {v in (2X,4X]: v≡1 mod 8}.
Test: from the known State(64) (derived from g256 witness), extend (restriction
semantics: old order preserved, new values interleave) to State(256).
"""
import sys, time, json
import numpy as np
from pysat.solvers import Cadical195

def block(v):
    k = (v - 1).bit_length()
    if 2 ** k < v: k += 1
    return k

def sa(hi):
    return [v for v in range(2, hi + 1) if block(v) % 2 == 0]

def state_values(X):
    """P(X) = S_A∩[1,X] + block (2X,4X] minus (v≡1 mod 8)."""
    vals = sa(X)
    vals += [v for v in range(2 * X + 1, 4 * X + 1) if v % 8 != 1]
    return sorted(vals)

def solve_state(X, fixed_order=None, max_rounds=4000):
    V = state_values(X)
    Vs = set(V)
    team = set(sa(4 * X))  # doom targets: full team membership up to 4X;
    # completions ≤ 8X: (4X,8X] is an odd block: free ✓ exact semantics.
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
    for a in V:
        for b in V:
            if b <= a: continue
            c = 2 * b - a
            if c in Vs:
                cl.append([-before(a, b), before(c, b)])
            elif c in team:
                cl.append([-before(a, b)])   # doomed: completion in team, unplaced
            d2 = 2 * a - b
            if d2 >= 1:
                if d2 in Vs:
                    cl.append([-before(b, a), before(d2, a)])
                elif d2 in team:
                    cl.append([-before(b, a)])
    if fixed_order:
        for i in range(len(fixed_order)):
            for j in range(i + 1, len(fixed_order)):
                cl.append([before(fixed_order[i], fixed_order[j])])
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
    # Stage 1: find State(64) from scratch
    t0 = time.time()
    s64 = solve_state(64)
    print(f"State(64): {'SAT' if s64 else 'UNSAT'} ({time.time()-t0:.0f}s)", flush=True)
    if not s64: sys.exit()
    json.dump(s64, open('data/state64.json', 'w'))
    # Stage 2: extend to State(256) with restriction semantics
    t0 = time.time()
    s256 = solve_state(256, fixed_order=s64)
    print(f"State(64)->State(256): {'SAT' if s256 else 'UNSAT'} ({time.time()-t0:.0f}s)", flush=True)
    if s256:
        json.dump(s256, open('data/state256.json', 'w'))
        # Stage 3
        t0 = time.time()
        s1024 = solve_state(1024, fixed_order=s256)
        print(f"State(256)->State(1024): {'SAT' if s1024 else 'UNSAT'} ({time.time()-t0:.0f}s)", flush=True)
        if s1024:
            json.dump(s1024, open('data/state1024.json', 'w'))
