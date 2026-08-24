"""Odd-odd chain game with fast transitivity repair (numpy)."""
import sys, time
import numpy as np
from pysat.solvers import Cadical195

def solve_order(V, clauses_fn, fixed_pairs=None, max_rounds=3000):
    idx = {v: i for i, v in enumerate(V)}
    n = len(V)
    tvar = {}
    c = 0
    for i in range(n):
        for j in range(i+1, n):
            c += 1
            tvar[(i, j)] = c
    def before(u, v):
        i, j = idx[u], idx[v]
        return tvar[(i, j)] if i < j else -tvar[(j, i)]
    cl = clauses_fn(before)
    if fixed_pairs:
        for (u, v) in fixed_pairs:
            cl.append([before(u, v)])
    s = Cadical195(bootstrap_with=cl)
    for _ in range(max_rounds):
        if not s.solve():
            return False
        model = s.get_model()
        pos = np.zeros(c+1, dtype=bool)
        for l in model:
            if l > 0: pos[l] = True
        # build boolean matrix B[i,j] = i before j
        B = np.zeros((n, n), dtype=bool)
        for (i, j), var in tvar.items():
            if pos[var]: B[i, j] = True
            else: B[j, i] = True
        wins = B.sum(axis=1)
        order = np.argsort(-wins, kind='stable')
        # check violations against sorted order
        added = 0
        R = B[np.ix_(order, order)]
        viol = np.argwhere(~R & ~np.eye(n, dtype=bool)[...])
        # viol rows a<b where order[a] not before order[b]
        for a, b in viol:
            if a >= b: continue
            i, j = order[a], order[b]
            # find witness k: i before k and k before j
            ks = np.nonzero(B[i] & B[:, j])[0]
            if len(ks):
                k = ks[0]
                u, w, x = V[i], V[k], V[j]
                s.add_clause([-before(u, w), -before(w, x), before(u, x)])
                added += 1
                if added > 20000: break
        if not added:
            return [V[i] for i in order]
    raise RuntimeError("rounds exhausted")

def odd_game(M, lower_order=None):
    X = [v for v in range(M//4+1, M//2+1) if v % 2 == 1]
    Y = [v for v in range(M+1, 2*M+1) if v % 2 == 1]
    V = X + Y
    def mk(before):
        cl = []
        for part in (X, Y):
            ps = set(part)
            for y in part:
                d = 2
                while y + d <= max(part):
                    a, cc = y - d, y + d
                    if a in ps and cc in ps:
                        cl.append([-before(a, y), -before(y, cc)])
                        cl.append([-before(cc, y), -before(y, a)])
                    d += 2
        Ys = set(Y)
        for x in X:
            for y in Y:
                z = 2*y - x
                if z in Ys:
                    cl.append([-before(x, y), before(z, y)])
        return cl
    fixed = []
    if lower_order:
        for i in range(len(lower_order)):
            for j in range(i+1, len(lower_order)):
                fixed.append((lower_order[i], lower_order[j]))
    return solve_order(V, mk, fixed)

if __name__ == "__main__":
    M = 16
    lower = None
    for link in range(5):
        t0 = time.time()
        r = odd_game(M, lower)
        dt = time.time() - t0
        if r is False:
            print(f"link {link} M={M}: UNSAT ({dt:.1f}s)", flush=True)
            break
        upper = [v for v in r if v > M]
        print(f"link {link} M={M}: SAT ({dt:.1f}s) |upper|={len(upper)}", flush=True)
        if M <= 64:
            print("   upper:", upper, flush=True)
        lower = upper
        M *= 4
