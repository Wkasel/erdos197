"""Erdős #197 — doom-free prefixes for the dyadic team set.

S_A = union of even dyadic blocks (2^(k-1), 2^k], k even  (value 1 -> team B).

Question(X, Y): does there exist Q with S_A∩[1,X] ⊆ Q ⊆ S_A∩[1,Y] and an
arrangement of Q such that
  - no monotone 3-AP within the arrangement, and
  - for every monotone-placed pair, its completion (in the same direction),
    if it lies in S_A∩[1,Y], is in Q and placed BEFORE the later element.
    (Completions > Y are outside S_A when Y is an A-block top: free.)

If S_A is permutable then Question(X, Y) is SAT for every X and some finite
Y (take a genuine prefix). Growing UNSAT walls = evidence of impossibility;
structured SAT solutions = seeds of a construction.
"""
from pysat.solvers import Cadical195
import time
import sys


def sa_values(Y):
    vals = []
    k = 2
    while 2 ** (k - 1) < Y:
        if k % 2 == 0:
            lo, hi = 2 ** (k - 1), min(2 ** k, Y)
            vals.extend(range(lo + 1, hi + 1))
        k += 1
    return vals


class DoomFree:
    def __init__(self, X, Y):
        self.X, self.Y = X, Y
        self.V = sa_values(Y)
        self.Vset = set(self.V)
        self.idx = {v: i for i, v in enumerate(self.V)}
        self.n = len(self.V)
        c = 0
        self.p = {}
        for v in self.V:
            c += 1
            self.p[v] = c
        self.t = {}
        for i in range(self.n):
            for j in range(i + 1, self.n):
                c += 1
                self.t[(i, j)] = c
        self.nv = c
        self.cl = []
        self._build()

    def before(self, u, v):
        i, j = self.idx[u], self.idx[v]
        return self.t[(i, j)] if i < j else -self.t[(j, i)]

    def _build(self):
        add = self.cl.append
        X, Y = self.X, self.Y
        # mandatory prefix
        for v in self.V:
            if v <= X:
                add([self.p[v]])
        # monotone pair dooms/violations: for x<y both placed:
        #  increasing (x before y): c=2y-x in S_A => placed and before y
        #  decreasing (y before x): c=2x-y in S_A => placed and before x
        for a in self.V:
            for b in self.V:
                if b <= a:
                    continue
                # increasing pair (a, b)
                c = 2 * b - a
                if c in self.Vset:
                    # placed(a) & placed(b) & a<b order => placed(c) & c before b
                    add([-self.p[a], -self.p[b], -self.before(a, b), self.p[c]])
                    add([-self.p[a], -self.p[b], -self.before(a, b),
                         self.before(c, b)])
                elif c <= Y:
                    pass  # not in S_A: free
                # else: c > Y: free when Y is an A-block top (assert below)
                # decreasing pair (b placed first, then a): completion 2a-b
                d = 2 * a - b
                if d >= 1 and d in self.Vset:
                    add([-self.p[a], -self.p[b], -self.before(b, a), self.p[d]])
                    add([-self.p[a], -self.p[b], -self.before(b, a),
                         self.before(d, a)])
        # (3-AP violations inside are implied by the pair rules: if x,y,z all
        # placed with x<y<z an AP and x≺y≺z, then rule forces z ≺ y — contradiction
        # emerges via order consistency; but order consistency needs transitivity,
        # which is lazy. Add direct AP clauses for safety.)
        for y in self.V:
            d = 1
            while y + d <= max(self.V):
                x, z = y - d, y + d
                if x in self.Vset and z in self.Vset:
                    add([-self.p[x], -self.p[y], -self.p[z],
                         -self.before(x, y), -self.before(y, z)])
                    add([-self.p[x], -self.p[y], -self.p[z],
                         -self.before(z, y), -self.before(y, x)])
                d += 1

    def solve(self):
        s = Cadical195(bootstrap_with=self.cl)
        while True:
            if not s.solve():
                return False
            model = s.get_model()
            pos = set(l for l in model if l > 0)
            placed = [v for v in self.V if self.p[v] in pos]

            def bef(u, v):
                l = self.before(u, v)
                return (l in pos) if l > 0 else (-l not in pos)

            wins = {v: 0 for v in placed}
            for i, u in enumerate(placed):
                for v in placed[i + 1:]:
                    if bef(u, v):
                        wins[u] += 1
                    else:
                        wins[v] += 1
            order = sorted(placed, key=lambda v: -wins[v])
            bad = 0
            for i in range(len(order)):
                for j in range(i + 1, len(order)):
                    u, v = order[i], order[j]
                    if not bef(u, v):
                        for w in order:
                            if w != u and w != v and bef(u, w) and bef(w, v):
                                cl = [-self.before(u, w), -self.before(w, v),
                                      self.before(u, v)]
                                s.add_clause(cl)
                                bad += 1
                                break
                        if bad > 5000:
                            break
                if bad > 5000:
                    break
            if not bad:
                return order


if __name__ == "__main__":
    for X, Y in [(16, 64), (64, 256), (256, 1024)]:
        t0 = time.time()
        df = DoomFree(X, Y)
        r = df.solve()
        dt = time.time() - t0
        if r is False:
            print(f"X={X} Y={Y} (n={df.n}): UNSAT ({dt:.1f}s)")
        else:
            extra = [v for v in r if v > X]
            print(f"X={X} Y={Y} (n={df.n}): SAT ({dt:.1f}s) |Q|={len(r)} "
                  f"beyond-X used: {len(extra)}")
            print("  order:", r if len(r) < 60 else r[:60])
