"""Flexible-reservoir states: State'(X) = complete-X + (block (2X,4X] minus a
FREE reservoir of exactly |block|/8 values). Chain with restriction semantics.
"""
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

def solve_flex(X, fixed_order=None, fixed_placed=None, max_rounds=4000):
    """values: S_A∩[1,4X]; placed-vars for block (2X,4X] (complete-X mandatory);
    cardinality: exactly 7/8 of the new block placed; doom: completions of
    monotone-placed pairs must be placed-before if in S_A∩[1,8X] (beyond 4X:
    (4X,8X] odd: free; so doom targets = S_A∩[1,4X] = our value set + none)."""
    V = sa(4 * X)
    Vs = set(V)
    newblock = [v for v in V if v > 2 * X]
    idx = {v: i for i, v in enumerate(V)}
    n = len(V)
    var = 0
    p = {}
    for v in V:
        var += 1
        p[v] = var
    t = {}
    for i in range(n):
        for j in range(i + 1, n):
            var += 1
            t[(i, j)] = var
    def before(u, w):
        i, j = idx[u], idx[w]
        return t[(i, j)] if i < j else -t[(j, i)]
    cl = []
    for v in V:
        if v <= 2 * X:
            cl.append([p[v]])
    for a in V:
        for b in V:
            if b <= a: continue
            c = 2 * b - a
            if c in Vs:
                cl.append([-p[a], -p[b], -before(a, b), p[c]])
                cl.append([-p[a], -p[b], -before(a, b), before(c, b)])
            d2 = 2 * a - b
            if d2 >= 1 and d2 in Vs:
                cl.append([-p[a], -p[b], -before(b, a), p[d2]])
                cl.append([-p[a], -p[b], -before(b, a), before(d2, a)])
    # cardinality: placed new = 7/8 of block
    want = len(newblock) * 7 // 8
    lits = [p[v] for v in newblock]
    eq = CardEnc.equals(lits=lits, bound=want, top_id=var + 1, encoding=EncType.seqcounter)
    var = eq.nv
    cl.extend(eq.clauses)
    if fixed_order:
        fo = [v for v in fixed_order]
        for i in range(len(fo)):
            cl.append([p[fo[i]]])
            for j in range(i + 1, len(fo)):
                cl.append([before(fo[i], fo[j])])
    if fixed_placed is not None:
        # values NOT in fixed_placed but ≤ old horizon must have been unplaced:
        for v in fixed_placed['unplaced']:
            pass  # they're now allowed to be placed (they're ≤ 2X: mandatory ✓)
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
        ms = set(l for l in model if l > 0)
        placed = [v for v in V if p[v] in ms]
        pset = set(placed)
        def bef(u, w):
            l = before(u, w)
            return (l in ms) if l > 0 else (-l not in ms)
        wins = {v: 0 for v in placed}
        np_ = len(placed)
        for i in range(np_):
            for j in range(i + 1, np_):
                u, w = placed[i], placed[j]
                if bef(u, w): wins[u] += 1
                else: wins[w] += 1
        order = sorted(placed, key=lambda v: -wins[v])
        added = 0
        for i in range(np_):
            for j in range(i + 1, np_):
                u, w = order[i], order[j]
                if not bef(u, w):
                    for x in order:
                        if x != u and x != w and bef(u, x) and bef(x, w):
                            s.add_clause([-before(u, x), -before(x, w), before(u, w)])
                            added += 1
                            break
                    if added > 25000: break
            if added > 25000: break
        if not added:
            return order

if __name__ == "__main__":
    t0 = time.time()
    s64 = solve_flex(64)
    print(f"FlexState(64): {'SAT' if s64 else 'UNSAT'} ({time.time()-t0:.0f}s)", flush=True)
    if not s64: sys.exit()
    json.dump(s64, open('data/flexstate64.json', 'w'))
    t0 = time.time()
    s256 = solve_flex(256, fixed_order=s64)
    print(f"Flex 64->256: {'SAT' if s256 else 'UNSAT'} ({time.time()-t0:.0f}s)", flush=True)
    if s256:
        json.dump(s256, open('data/flexstate256.json', 'w'))
        t0 = time.time()
        s1024 = solve_flex(1024, fixed_order=s256)
        print(f"Flex 256->1024: {'SAT' if s1024 else 'UNSAT'} ({time.time()-t0:.0f}s)", flush=True)
        if s1024:
            json.dump(s1024, open('data/flexstate1024.json', 'w'))
