"""EXACT necessary-condition ladder for S_A permutability.

Depth-d joint at seed X: nested prefixes P_1 ⊆ P_2 ⊆ ... ⊆ P_d, one global
order; P_i ⊇ S_A∩[1, 4^{i-1}X] (complete levels), extras anywhere within the
horizon H = 4^d X; every P_i doom-free w.r.t. team ∩ [1, H] with completions
beyond H free (H = block top ⇒ (H,2H] odd ⇒ exact).
P_i values all placed before P_{i+1}∖P_i values (prefix semantics).
A global solution restricts+truncates to a witness for EVERY (X, d).
=> UNSAT for ANY (X, d) proves S_A is not permutable.
Args: X d
"""
import sys, time, json
from pysat.solvers import Cadical195

def block(v):
    k = (v - 1).bit_length()
    if 2 ** k < v: k += 1
    return k

def sa(hi):
    return [v for v in range(2, hi + 1) if block(v) % 2 == 0]

def ladder(X, d, max_rounds=10000):
    H = (4 ** d) * X
    V = sa(H)
    Vs = set(V)
    idx = {v: i for i, v in enumerate(V)}
    n = len(V)
    var = 0
    P = []
    for i in range(d):
        pi = {}
        for v in V:
            var += 1
            pi[v] = var
        P.append(pi)
    t = {}
    for i in range(n):
        for j in range(i + 1, n):
            var += 1
            t[(i, j)] = var
    def before(u, w):
        i, j = idx[u], idx[w]
        return t[(i, j)] if i < j else -t[(j, i)]
    cl = []
    for i in range(d):
        comp = 4 ** i * X
        for v in V:
            if v <= comp:
                cl.append([P[i][v]])
            if i + 1 < d:
                cl.append([-P[i][v], P[i + 1][v]])
    # prefix time-ordering: P_i values before non-P_i (within P_{i+1}) values
    for i in range(d - 1):
        for u in V:
            for w in V:
                if u == w: continue
                cl.append([-P[i][u], P[i][w], -P[i + 1][w], before(u, w)])
    # doom for each level
    for i in range(d):
        pi = P[i]
        for a in V:
            for b in V:
                if b <= a: continue
                c = 2 * b - a
                if c in Vs:
                    cl.append([-pi[a], -pi[b], -before(a, b), pi[c]])
                    if i == d - 1:
                        cl.append([-pi[a], -pi[b], -before(a, b), before(c, b)])
                d2 = 2 * a - b
                if d2 >= 1 and d2 in Vs:
                    cl.append([-pi[a], -pi[b], -before(b, a), pi[d2]])
                    if i == d - 1:
                        cl.append([-pi[a], -pi[b], -before(b, a), before(d2, a)])
    print(f"X={X} d={d} H={H}: n={n} clauses={len(cl)}", flush=True)
    s = Cadical195(bootstrap_with=cl)
    rounds = 0
    while True:
        rounds += 1
        if rounds > max_rounds:
            raise RuntimeError("rounds")
        if not s.solve():
            return False
        model = s.get_model()
        ms = set(l for l in model if l > 0)
        top_placed = [v for v in V if P[d - 1][v] in ms]
        def bef(u, w):
            l = before(u, w)
            return (l in ms) if l > 0 else (-l not in ms)
        k = len(top_placed)
        wins = {v: 0 for v in top_placed}
        for i in range(k):
            for j in range(i + 1, k):
                u, w = top_placed[i], top_placed[j]
                if bef(u, w): wins[u] += 1
                else: wins[w] += 1
        order = sorted(top_placed, key=lambda v: -wins[v])
        added = 0
        for i in range(k):
            for j in range(i + 1, k):
                u, w = order[i], order[j]
                if not bef(u, w):
                    for x in order:
                        if x != u and x != w and bef(u, x) and bef(x, w):
                            s.add_clause([-before(u, x), -before(x, w), before(u, w)])
                            added += 1
                            break
                    if added > 30000: break
            if added > 30000: break
        if not added:
            return order, [sorted(v for v in V if P[i][v] in ms) for i in range(d)]

if __name__ == "__main__":
    X, d = int(sys.argv[1]), int(sys.argv[2])
    t0 = time.time()
    r = ladder(X, d)
    tag = 'UNSAT  <-- S_A NOT PERMUTABLE (exact necessary condition fails)' if r is False else 'SAT'
    print(f"LADDER X={X} d={d}: {tag} ({time.time()-t0:.0f}s)", flush=True)
    if r is not False:
        json.dump(r[1], open(f'data/ladder_{X}_{d}.json', 'w'))
