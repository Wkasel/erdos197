"""Restriction-semantics chaining: solve pure-complete-X, then pure-4X with
the old values' RELATIVE order fixed (new values interleave freely)."""
import sys, time
sys.path.insert(0, 'experiments')
from pysat.solvers import Cadical195

def block(v):
    k = (v - 1).bit_length()
    if 2 ** k < v: k += 1
    return k

def sa(hi):
    return [v for v in range(2, hi + 1) if block(v) % 2 == 0]

def solve_pure(X, fixed_order=None, max_rounds=2000):
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
    if fixed_order:
        for i in range(len(fixed_order)):
            for j in range(i + 1, len(fixed_order)):
                cl.append([before(fixed_order[i], fixed_order[j])])
    s = Cadical195(bootstrap_with=cl)
    rounds = 0
    while True:
        rounds += 1
        if rounds > max_rounds:
            raise RuntimeError("rounds")
        if not s.solve():
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
                            s.add_clause([-before(u, x), -before(x, w), before(u, w)])
                            added += 1
                            break
                    if added > 15000: break
            if added > 15000: break
        if not added:
            return order

if __name__ == "__main__":
    order = None
    for X in [16, 64, 256, 1024]:
        t0 = time.time()
        r = solve_pure(X, order)
        dt = time.time() - t0
        if r is False:
            print(f"X={X} (restriction-chained): UNSAT ({dt:.1f}s)", flush=True)
            break
        print(f"X={X}: SAT ({dt:.1f}s)", flush=True)
        if X <= 64:
            print("   order:", r, flush=True)
        order = r
    if r is not False:
        import json
        json.dump(r, open('data/chain1024.json', 'w'))
        print("saved chain1024.json", flush=True)
