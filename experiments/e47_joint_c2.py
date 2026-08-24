"""Joint viability with c=2 overhang: State2(X) = complete-X + f1·(2X,4X] +
f2·(8X,16X]; joint with its extension State2(4X) (values ≤ 64X)."""
import sys, time, json
import numpy as np
from pysat.solvers import Cadical195
from pysat.card import CardEnc, EncType

def block(v):
    k = (v - 1).bit_length()
    if 2 ** k < v: k += 1
    return k

def sa(hi):
    return [v for v in range(2, hi + 1) if block(v) % 2 == 0]

def joint2(X, f1=(7,8), f2=(1,8), max_rounds=8000):
    V = sa(64 * X)
    Vs = set(V)
    idx = {v: i for i, v in enumerate(V)}
    n = len(V)
    var = 0
    p1, p2 = {}, {}
    for v in V:
        var += 1; p1[v] = var
    for v in V:
        var += 1; p2[v] = var
    t = {}
    for i in range(n):
        for j in range(i + 1, n):
            var += 1
            t[(i, j)] = var
    def before(u, w):
        i, j = idx[u], idx[w]
        return t[(i, j)] if i < j else -t[(j, i)]
    cl = []
    A1 = [v for v in V if 2*X < v <= 4*X]      # state overhang-1
    A2 = [v for v in V if 8*X < v <= 16*X]     # state overhang-2
    B1 = [v for v in V if 8*X < v <= 16*X]     # ext overhang-1 (=A2 range)
    B2 = [v for v in V if 32*X < v <= 64*X]    # ext overhang-2
    for v in V:
        cl.append([-p1[v], p2[v]])
        if v <= X: cl.append([p1[v]])
        if v <= 4 * X: cl.append([p2[v]])
        if v > 16 * X: cl.append([-p1[v]])
        if v > 64 * X: cl.append([-p2[v]])
    for a in V:
        for b in V:
            if b <= a: continue
            c = 2 * b - a
            if c in Vs:
                cl.append([-p2[a], -p2[b], -before(a, b), p2[c]])
                cl.append([-p2[a], -p2[b], -before(a, b), before(c, b)])
                cl.append([-p1[a], -p1[b], -before(a, b), p1[c]])
            d2 = 2 * a - b
            if d2 >= 1 and d2 in Vs:
                cl.append([-p2[a], -p2[b], -before(b, a), p2[d2]])
                cl.append([-p2[a], -p2[b], -before(b, a), before(d2, a)])
                cl.append([-p1[a], -p1[b], -before(b, a), p1[d2]])
    for u in V:
        for w in V:
            if u == w: continue
            cl.append([-p1[u], p1[w], -p2[w], before(u, w)])
    for (bl, pp, fr) in [(A1, p1, f1), (A2, p1, f2), (B1, p2, f1), (B2, p2, f2)]:
        lits = [pp[v] for v in bl]
        want = len(bl) * fr[0] // fr[1]
        eq = CardEnc.equals(lits=lits, bound=want, top_id=var + 1, encoding=EncType.seqcounter)
        var = eq.nv
        cl.extend(eq.clauses)
    print(f"X={X} f1={f1} f2={f2}: n={n} clauses={len(cl)}", flush=True)
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
        ms = set(l for l in model if l > 0)
        placed2 = [v for v in V if p2[v] in ms]
        def bef(u, w):
            l = before(u, w)
            return (l in ms) if l > 0 else (-l not in ms)
        k = len(placed2)
        wins = {v: 0 for v in placed2}
        for i in range(k):
            for j in range(i + 1, k):
                u, w = placed2[i], placed2[j]
                if bef(u, w): wins[u] += 1
                else: wins[w] += 1
        order = sorted(placed2, key=lambda v: -wins[v])
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
            state1 = [v for v in order if p1[v] in ms]
            return state1, order

if __name__ == "__main__":
    f1 = (int(sys.argv[1]), int(sys.argv[2]))
    f2 = (int(sys.argv[3]), int(sys.argv[4]))
    t0 = time.time()
    r = joint2(16, f1, f2)
    tag = 'UNSAT' if r is False else 'SAT'
    print(f"JOINT-c2 State2(16)+ext f1={f1} f2={f2}: {tag} ({time.time()-t0:.0f}s)", flush=True)
    if r is not False:
        json.dump(r[0], open(f'data/viable2_state16_{f1[0]}{f1[1]}_{f2[0]}{f2[1]}.json', 'w'))
