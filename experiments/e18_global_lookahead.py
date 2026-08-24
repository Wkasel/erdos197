"""Global incremental solve of team A's sequence with 2-level lookahead.

Level tops: X_J = 4^J (A-block tops). At step J: solve jointly for a
doom-free prefix covering S_A∩[1,X_J] using values ≤ X_{J+1}, WITH the
requirement that it extends to cover S_A∩[1,X_{J+1}] using values ≤ X_{J+2}
(lookahead); commit only the level-J part. Previous committed order fixed.

Exact semantics: one global order on chosen values; completions of
monotone-placed pairs must be pre-placed if they lie in S_A (any scale;
completions beyond the current value horizon Y are in S_A iff block even —
handled exactly). Sparse order variables: only for pairs that co-occur in
some constraint, plus lazy transitivity on the constraint graph.
"""
import sys, time
import numpy as np
from pysat.solvers import Cadical195

def block(v):
    k = (v - 1).bit_length()
    if 2 ** k < v: k += 1
    return k

def in_sa(v):
    return v >= 2 and block(v) % 2 == 0

def sa(lo, hi):
    return [v for v in range(max(2, lo + 1), hi + 1) if in_sa(v)]

class Inc:
    def __init__(self):
        self.committed = []  # fixed order

    def solve_level(self, X, Y, Xnext=None, Ynext=None):
        """mandatory ≤ X, allowed ≤ Y; if lookahead: joint solve mandatory
        ≤ Xnext allowed ≤ Ynext, commit only ≤ X-mandatory part order prefix."""
        horizon = Ynext if Ynext else Y
        pool = [v for v in sa(0, horizon) if v not in set(self.committed)]
        V = self.committed + pool
        idx = {v: i for i, v in enumerate(V)}
        n = len(V)
        var = 0
        p = {}
        for v in V:
            var += 1
            p[v] = var
        t = {}
        def before(u, w):
            nonlocal var
            a, b = idx[u], idx[w]
            key = (a, b) if a < b else (b, a)
            if key not in t:
                var += 1
                t[key] = var
            lit = t[key]
            return lit if a < b else -lit
        cl = []
        # committed: placed & ordered & before all new placed
        for v in self.committed:
            cl.append([p[v]])
        for i in range(len(self.committed)):
            for j in range(i + 1, len(self.committed)):
                cl.append([before(self.committed[i], self.committed[j])])
        for v in self.committed:
            for w in pool:
                cl.append([-p[w], before(v, w)])
        # mandatory
        mand = X if not Xnext else Xnext
        for v in pool:
            if v <= mand:
                cl.append([p[v]])
        Vset = set(V)
        # pair constraints (both directions), sparse
        for ii in range(n):
            a = V[ii]
            for jj in range(n):
                b = V[jj]
                if b <= a: continue
                # increasing pair (a then b): completion c = 2b - a
                c = 2 * b - a
                if c in Vset:
                    cl.append([-p[a], -p[b], -before(a, b), p[c]])
                    cl.append([-p[a], -p[b], -before(a, b), before(c, b)])
                elif c <= horizon and in_sa(c):
                    cl.append([-p[a], -p[b], -before(a, b)])
                # c beyond horizon: block(c)=block(b)+1 odd => free, or same
                # block: c<=2*top ok... c=2b-a with b<=horizon: c<=2*horizon:
                elif c > horizon and in_sa(c):
                    cl.append([-p[a], -p[b], -before(a, b)])
                # decreasing pair (b then a): completion d = 2a - b < a
                d = 2 * a - b
                if d >= 1:
                    if d in Vset:
                        cl.append([-p[a], -p[b], -before(b, a), p[d]])
                        cl.append([-p[a], -p[b], -before(b, a), before(d, a)])
                    elif in_sa(d):
                        cl.append([-p[a], -p[b], -before(b, a)])
        s = Cadical195(bootstrap_with=cl)
        rounds = 0
        while True:
            rounds += 1
            if rounds > 500:
                raise RuntimeError("rounds")
            if not s.solve():
                return False
            model = s.get_model()
            mset = set(l for l in model if l > 0)
            placed = [v for v in V if p[v] in mset]
            def bef(u, w):
                l = before(u, w)
                return (l in mset) if l > 0 else (-l not in mset)
            k = len(placed)
            wins = {}
            for v in placed: wins[v] = 0
            for i2 in range(k):
                for j2 in range(i2 + 1, k):
                    u, w = placed[i2], placed[j2]
                    if bef(u, w): wins[u] += 1
                    else: wins[w] += 1
            order = sorted(placed, key=lambda v: -wins[v])
            added = 0
            for i2 in range(k):
                for j2 in range(i2 + 1, k):
                    u, w = order[i2], order[j2]
                    if not bef(u, w):
                        for x in order:
                            if x != u and x != w and bef(u, x) and bef(x, w):
                                s.add_clause([-before(u, x), -before(x, w), before(u, w)])
                                added += 1
                                break
                        if added > 20000: break
                if added > 20000: break
            if not added:
                return order

if __name__ == "__main__":
    inc = Inc()
    levels = [(16, 64, 64, 256), (64, 256, 256, 1024), (256, 1024, 1024, 4096)]
    for (X, Y, Xn, Yn) in levels:
        t0 = time.time()
        r = inc.solve_level(X, Y, Xn, Yn)
        dt = time.time() - t0
        if r is False:
            print(f"level X={X} (lookahead {Xn}): UNSAT ({dt:.1f}s)", flush=True)
            break
        # commit only the prefix up to the point where all ≤X placed
        seen = set()
        need = set(v for v in sa(0, X))
        cut = 0
        for i, v in enumerate(r):
            seen.add(v)
            if need <= seen:
                cut = i + 1
                break
        inc.committed = r[:cut]
        print(f"level X={X}: ok ({dt:.1f}s), committed {cut} values "
              f"(max {max(inc.committed)})", flush=True)
    print("final committed prefix:", inc.committed[:80], flush=True)
