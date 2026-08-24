"""Erdős #197 — incremental chaining of doom-free prefixes for S_A
(even dyadic blocks). At each level J (A-block top X_J = 4^J), require:
  prefix P_J: contains S_A∩[1,X_J], contained in S_A∩[1,X_{J+1}],
  doom-free, and EXTENDS P_{J-1} (previous order fixed, append-only).
The reservoir R_J = allowed values not yet placed.
"""
from pysat.solvers import Cadical195
import sys
import time


def sa_values(lo, hi):
    """S_A values in (lo, hi]: even dyadic blocks."""
    vals = []
    k = 2
    while 2 ** (k - 1) < hi:
        if k % 2 == 0:
            a, b = max(2 ** (k - 1), lo), min(2 ** k, hi)
            if b > a:
                vals.extend(range(a + 1, b + 1))
        k += 1
    return vals


def in_sa(v):
    k = v.bit_length()
    return k % 2 == 0 and v > 2 ** (k - 1) or (k % 2 == 0 and v == 2 ** k)


def sa_member(v):
    if v < 2:
        return False
    k = (v - 1).bit_length()  # v in (2^(k-1)... hmm compute block index
    # block of v: smallest k with v <= 2^k and v > 2^(k-1)
    k = (v - 1).bit_length()
    if 2 ** k < v:
        k += 1
    return k % 2 == 0


class Chain:
    def __init__(self):
        self.prefix = []   # fixed placed order so far

    def extend(self, X, Y, timeout_rounds=400):
        """append values to reach mandatory X, allowed up to Y."""
        old = list(self.prefix)
        oldset = set(old)
        new_pool = [v for v in sa_values(0, Y) if v not in oldset]
        V = old + new_pool
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
        cl = []

        def before(u, v):
            i, j = idx[u], idx[v]
            return t[(i, j)] if i < j else -t[(j, i)]

        # fix old prefix: placed, and order as given; old before all new placed
        for v in old:
            cl.append([p[v]])
        for i in range(len(old)):
            for j in range(i + 1, len(old)):
                cl.append([before(old[i], old[j])])
        for v in old:
            for w in new_pool:
                cl.append([-p[w], before(v, w)])
        # mandatory new values
        for v in new_pool:
            if v <= X:
                cl.append([p[v]])
        Vset = set(V)
        # doom/AP pair constraints (same as e8)
        for a in V:
            for b in V:
                if b <= a:
                    continue
                c = 2 * b - a
                if c in Vset:
                    cl.append([-p[a], -p[b], -before(a, b), p[c]])
                    cl.append([-p[a], -p[b], -before(a, b), before(c, b)])
                elif c <= Y and sa_member(c):
                    cl.append([-p[a], -p[b], -before(a, b)])  # doomed: forbid
                d = 2 * a - b
                if d >= 1:
                    if d in Vset:
                        cl.append([-p[a], -p[b], -before(b, a), p[d]])
                        cl.append([-p[a], -p[b], -before(b, a), before(d, a)])
                    elif sa_member(d):
                        cl.append([-p[a], -p[b], -before(b, a)])
        s = Cadical195(bootstrap_with=cl)
        rounds = 0
        while True:
            rounds += 1
            if rounds > timeout_rounds:
                return None
            if not s.solve():
                return False
            model = s.get_model()
            pos = set(l for l in model if l > 0)
            placed = [v for v in V if p[v] in pos]

            def bef(u, v):
                l = before(u, v)
                return (l in pos) if l > 0 else (-l not in pos)

            wins = {v: 0 for v in placed}
            for i, u in enumerate(placed):
                for w in placed[i + 1:]:
                    if bef(u, w):
                        wins[u] += 1
                    else:
                        wins[w] += 1
            order = sorted(placed, key=lambda v: -wins[v])
            bad = 0
            for i in range(len(order)):
                for j in range(i + 1, len(order)):
                    u, w = order[i], order[j]
                    if not bef(u, w):
                        for x in order:
                            if x != u and x != w and bef(u, x) and bef(x, w):
                                s.add_clause([-before(u, x), -before(x, w),
                                              before(u, w)])
                                bad += 1
                                break
                        if bad > 6000:
                            break
                if bad > 6000:
                    break
            if not bad:
                self.prefix = order
                return order


if __name__ == "__main__":
    ch = Chain()
    levels = [(4, 16), (16, 64), (64, 256), (256, 1024), (1024, 4096)]
    for X, Y in levels:
        t0 = time.time()
        r = ch.extend(X, Y)
        dt = time.time() - t0
        if r is False:
            print(f"level X={X}: STUCK (UNSAT) ({dt:.1f}s)")
            break
        if r is None:
            print(f"level X={X}: gave up transitivity ({dt:.1f}s)")
            break
        print(f"level X={X} Y={Y}: extended, |prefix|={len(r)} ({dt:.1f}s)")
        held = [v for v in sa_values(0, Y) if v not in set(r)]
        print(f"   reservoir: {len(held)} values held back: {held[:30]}{'...' if len(held)>30 else ''}")
