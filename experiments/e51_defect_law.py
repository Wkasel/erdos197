"""Defect-law states: State(X) = complete-4X MINUS class {v ≡ 2 mod 2^m} of
block (2X,4X], with extras above allowed anywhere ≤ horizon (free).
Chain: verify State(X) -> State(4X) (joint, exact semantics, prefix ordering).
Law: m(X) = log2(X)/... use m such that the class size = |block|/2^{m-1}...
From data: at scale 64 (block (32,64], size 32): withheld class ≡2 mod 8: 4 = 32/8 values.
At 256 (block (128,256], 128): ≡2 mod 16: 8 = 128/16. So modulus = block-size/8·... 
block (2^k-1..2^k]: modulus 2^{k-3}?? 64-block: k=6: mod 8 = 2^3 = 2^{k-3} ✓; 256: k=8: mod 16 ✓ = 2^{k-4}?? 2^{8-4}=16 ✓ but 2^{6-3}=8 ✓ — k-3 vs k-4 inconsistent: 64: mod 8 = 2^{6-3}; 256: 16 = 2^{8-4}: hmm. Use: withheld count = 4, 8: = 2^{k/2}?? k=6: 4 ✓ wait 2^3=8✗. counts: 4 at k=6, 8 at k=8: count = 2^{(k-2)/2}·... 4=2^2 at k=6, 8=2^3 at k=8: count = 2^{k/2-1} ✓✓ modulus = blocksize/count = 2^{k-1}/2^{k/2-1} = 2^{k/2}: k=6: 8 ✓ k=8: 16 ✓ LAW: modulus m_k = 2^{k/2}, class ≡ 2 mod m_k.
Args: X (seed), depth
"""
import sys, time, json
from pysat.solvers import Cadical195

def block(v):
    k = (v - 1).bit_length()
    if 2 ** k < v: k += 1
    return k

def sa(hi):
    return [v for v in range(2, hi + 1) if block(v) % 2 == 0]

def defect_class(comp):
    """withheld set for completeness-level comp: class ≡2 mod 2^{k/2} of block
    (comp/2, comp], k = log2(comp)."""
    k = comp.bit_length() - 1
    m = 2 ** (k // 2)
    return set(v for v in range(comp // 2 + 1, comp + 1) if v % m == 2)

def ladder_law(X, d, max_rounds=10000):
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
        comp = 4 ** i * X * 4   # level-i target completeness = next-scale-minus-defect
        D = defect_class(comp)
        for v in V:
            if v <= comp:
                if v in D:
                    cl.append([-P[i][v]])   # LAW: defect class withheld
                else:
                    cl.append([P[i][v]])
            if i + 1 < d:
                cl.append([-P[i][v], P[i + 1][v]])
    for i in range(d - 1):
        for u in V:
            for w in V:
                if u == w: continue
                cl.append([-P[i][u], P[i][w], -P[i + 1][w], before(u, w)])
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
    print(f"LAW X={X} d={d} H={H}: n={n} clauses={len(cl)}", flush=True)
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
            return order

if __name__ == "__main__":
    X, d = int(sys.argv[1]), int(sys.argv[2])
    t0 = time.time()
    r = ladder_law(X, d)
    tag = 'UNSAT (law wrong or too rigid)' if r is False else 'SAT'
    print(f"LAW-LADDER X={X} d={d}: {tag} ({time.time()-t0:.0f}s)", flush=True)
