"""Joint 2-level viability: solve State(X) AND its extension State(4X) as one
instance (values ≤ 16X), then commit the State(X) part only.
State(X) = complete-X + 7/8 of block (2X,4X] (free reservoir choice).
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

def joint(X, fixed_order=None, max_rounds=6000):
    """values ≤ 16X; State(X)-part = complete-2X?? precisely:
    placed-set P1 = S_A∩[1,X] ∪ 7/8·(2X,4X]  (the state)
    placed-set P2 = S_A∩[1,4X] ∪ 7/8·(8X,16X]  (its extension; P1 ⊆ P2)
    one global order; doom w.r.t. full team membership ≤ 16X (completions
    ≤ 32X land in (16X,32X] odd → free).
    Encode: p1[v], p2[v] with p1→p2; complete parts mandatory; cardinalities."""
    V = sa(16 * X)
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
    b1 = [v for v in V if 2 * X < v <= 4 * X]
    b2 = [v for v in V if 8 * X < v <= 16 * X]
    for v in V:
        cl.append([-p1[v], p2[v]])
        if v <= X:
            cl.append([p1[v]])
        elif v <= 2 * X:
            cl.append([-p1[v]])   # (X,2X] odd-block: not in S_A anyway (sa() excludes) — no-op safeguard
        if v <= 4 * X:
            cl.append([p2[v]])
        if 4 * X < v <= 8 * X:
            cl.append([-p2[v]])   # odd block safeguard
    # only new-block values optional in P1
    for v in V:
        if v > 4 * X:
            cl.append([-p1[v]])
    # doom constraints on P2 (the full final prefix); P1-order = restriction ✓
    for a in V:
        for b in V:
            if b <= a: continue
            c = 2 * b - a
            if c in Vs:
                cl.append([-p2[a], -p2[b], -before(a, b), p2[c]])
                cl.append([-p2[a], -p2[b], -before(a, b), before(c, b)])
            d2 = 2 * a - b
            if d2 >= 1 and d2 in Vs:
                cl.append([-p2[a], -p2[b], -before(b, a), p2[d2]])
                cl.append([-p2[a], -p2[b], -before(b, a), before(d2, a)])
    # ALSO: P1 must itself be doom-free (its unplaced-completions must not be
    # in team-P1-future... P1 is a prefix of P2 in time? The state = a prefix:
    # require: for pairs both in P1: completion in team ⇒ IN P1 and before:
    for a in V:
        for b in V:
            if b <= a: continue
            c = 2 * b - a
            if c in Vs:
                cl.append([-p1[a], -p1[b], -before(a, b), p1[c]])
            d2 = 2 * a - b
            if d2 >= 1 and d2 in Vs:
                cl.append([-p1[a], -p1[b], -before(b, a), p1[d2]])
    # P1-values precede P2-only values?? NO — restriction semantics: the state
    # is the TIME-prefix: require all P1 values before all (P2 minus P1) values:
    for u in V:
        for w in V:
            if u == w: continue
            # p1[u] ∧ ¬p1[w] ∧ p2[w] → before(u,w)
            if u < w:
                cl.append([-p1[u], p1[w], -p2[w], before(u, w)])
            else:
                cl.append([-p1[u], p1[w], -p2[w], before(u, w)])
    # cardinalities: |P1 ∩ b1| = 7/8|b1|; |P2 ∩ b2| = 7/8|b2|
    for (bl, pp, frac) in [(b1, p1, 7), (b2, p2, 7)]:
        lits = [pp[v] for v in bl]
        want = len(bl) * frac // 8
        eq = CardEnc.equals(lits=lits, bound=want, top_id=var + 1, encoding=EncType.seqcounter)
        var = eq.nv
        cl.extend(eq.clauses)
    if fixed_order:
        for i in range(len(fixed_order)):
            cl.append([p1[fixed_order[i]]])
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
                    if added > 25000: break
            if added > 25000: break
        if not added:
            state1 = [v for v in order if p1[v] in ms]
            return state1, order

if __name__ == "__main__":
    t0 = time.time()
    r = joint(64)
    if r is False:
        print(f"JOINT State(64)+ext: UNSAT ({time.time()-t0:.0f}s)  <-- level-1 viability fails", flush=True)
    else:
        s1, full = r
        print(f"JOINT State(64)+ext: SAT ({time.time()-t0:.0f}s) |state|={len(s1)}", flush=True)
        json.dump(s1, open('data/viable_state64.json', 'w'))
        json.dump(full, open('data/viable_full256.json', 'w'))
