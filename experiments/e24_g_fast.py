"""g_X(L) with persistent solver + assumption-based binary search."""
import sys, time
sys.path.insert(0, 'experiments')
from pysat.solvers import Cadical195
from pysat.card import ITotalizer

def block(v):
    k = (v - 1).bit_length()
    if 2 ** k < v: k += 1
    return k

def sa(hi):
    return [v for v in range(2, hi + 1) if block(v) % 2 == 0]

def g(X, L, verbose=False):
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
    s = Cadical195(bootstrap_with=cl)
    small = [v for v in V if v <= L]
    tid = top
    tots = []
    for v in small:
        lits = [before(u, v) for u in V if u != v]
        tot = ITotalizer(lits=lits, ubound=len(lits), top_id=tid)
        tid = tot.top_id
        for c in tot.cnf.clauses:
            s.add_clause(c)
        tots.append(tot)

    def solve_bound(k):
        assum = []
        for tot in tots:
            if k < len(tot.rhs):
                assum.append(-tot.rhs[k])
        rounds = 0
        while True:
            rounds += 1
            if rounds > 2000:
                return None
            if not s.solve(assumptions=assum):
                return False
            model = set(l for l in s.get_model() if l > 0)
            def bef(u, w):
                l = before(u, w)
                return (l in model) if l > 0 else (-l not in model)
            wins = {v: 0 for v in V}
            for i in range(n):
                for j in range(i + 1, n):
                    u, w = V[i], V[j]
                    if bef(u, w): wins[u] += 1
                    else: wins[w] += 1
            order = sorted(V, key=lambda v: -wins[v])
            added = 0
            for i in range(n):
                for j in range(i + 1, n):
                    u, w = order[i], order[j]
                    if not bef(u, w):
                        for x in order:
                            if x != u and x != w and bef(u, x) and bef(x, w):
                                s.add_clause([-before(u, x), -before(x, w),
                                              before(u, w)])
                                added += 1
                                break
                        if added > 15000: break
                if added > 15000: break
            if not added:
                return True

    lo, hi = len(small) - 1, n - 1
    best = None
    while lo <= hi:
        mid = (lo + hi) // 2
        r = solve_bound(mid)
        if verbose:
            print(f"  bound {mid}: {r}", flush=True)
        if r is True:
            best = mid; hi = mid - 1
        elif r is False:
            lo = mid + 1
        else:
            lo = mid + 1
    return best

if __name__ == "__main__":
    L = int(sys.argv[1]) if len(sys.argv) > 1 else 64
    for X in [64, 256, 1024]:
        if X < L: continue
        t0 = time.time()
        r = g(X, L)
        print(f"g_{X}({L}) = {r}  (|small|={len(sa(L))}, n={len(sa(X))})  ({time.time()-t0:.0f}s)", flush=True)
