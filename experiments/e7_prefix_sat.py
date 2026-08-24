"""Erdős #197 — full-problem prefix SAT.

Encode: assignment a_v (A/B) of each v in [1..N] + one global timeline
(order vars). Constraints:
  * no monochromatic monotone 3-AP (all terms <= N);
  * IOU consistency: for completion values c in (N, 2N): it cannot be that
    team A has an increasingly-placed pair completing to c AND team B does
    too (c must belong to the other team in any infinite extension: both
    claims => contradiction).
A YES-answer to #197 implies SAT for every N. UNSAT for any N resolves
Erdős #197 in the negative, with a certificate.

Lazy transitivity via triangle clauses on demand.
"""
from pysat.solvers import Cadical195
import sys
import time


class PrefixSAT:
    def __init__(self, N):
        self.N = N
        self.var = 0
        self.a = {}      # team var per value: True = A
        self.t = {}      # order var per pair (u<v): True = "u before v"
        for v in range(1, N + 1):
            self.var += 1
            self.a[v] = self.var
        for u in range(1, N + 1):
            for v in range(u + 1, N + 1):
                self.var += 1
                self.t[(u, v)] = self.var
        self.clauses = []
        self.iouA = {}
        self.iouB = {}
        self._build()

    def before(self, u, v):
        if u < v:
            return self.t[(u, v)]
        return -self.t[(v, u)]

    def _build(self):
        N = self.N
        add = self.clauses.append
        # symmetry breaking
        add([self.a[1]])
        # monochromatic monotone 3-APs
        for y in range(2, N + 1):
            for d in range(1, min(y - 1, N - y) + 1):
                x, z = y - d, y + d
                ax, ay, az = self.a[x], self.a[y], self.a[z]
                for (l1, l2) in [(self.before(x, y), self.before(y, z)),
                                 (self.before(z, y), self.before(y, x))]:
                    add([-ax, -ay, -az, -l1, -l2])
                    add([ax, ay, az, -l1, -l2])
        # IOUs for completions beyond N
        for c in range(N + 1, 2 * N):
            pairs = []
            # c = 2y - x  with x < y <= N
            for y in range((c + 2) // 2, N + 1):
                x = 2 * y - c
                if 1 <= x < y:
                    pairs.append((x, y))
            if not pairs:
                continue
            self.var += 1
            iA = self.var
            self.var += 1
            iB = self.var
            self.iouA[c], self.iouB[c] = iA, iB
            for (x, y) in pairs:
                # A-pair increasing => iouA
                add([-self.a[x], -self.a[y], -self.before(x, y), iA])
                add([self.a[x], self.a[y], -self.before(x, y), iB])
            add([-iA, -iB])

    def solve(self, max_rounds=2000, verbose=False):
        s = Cadical195(bootstrap_with=self.clauses)
        N = self.N
        rounds = 0
        while True:
            rounds += 1
            if rounds > max_rounds:
                return None
            if not s.solve():
                return False
            model = s.get_model()
            pos = set(l for l in model if l > 0)

            def bef(u, v):
                return self.before(u, v) in pos if u < v else self.before(u, v) not in pos or True

            def bef2(u, v):
                l = self.before(u, v)
                return (l in pos) if l > 0 else (-l not in pos)

            # topological attempt: count wins
            wins = [0] * (N + 1)
            for u in range(1, N + 1):
                for v in range(u + 1, N + 1):
                    if bef2(u, v):
                        wins[u] += 1
                    else:
                        wins[v] += 1
            order = sorted(range(1, N + 1), key=lambda v: -wins[v])
            # batch: collect violated transitivity triangles
            fixed = 0
            for i in range(N):
                for j in range(i + 1, N):
                    u, v = order[i], order[j]
                    if not bef2(u, v):
                        for w in order:
                            if w != u and w != v and bef2(u, w) and bef2(w, v):
                                c = [-self.before(u, w), -self.before(w, v),
                                     self.before(u, v)]
                                s.add_clause(c)
                                self.clauses.append(c)
                                fixed += 1
                                break
                        if fixed > 8000:
                            break
                if fixed > 8000:
                    break
            if not fixed:
                # consistent: extract solution
                team = {v: (self.a[v] in pos) for v in range(1, N + 1)}
                return order, team


def run(N):
    t0 = time.time()
    ps = PrefixSAT(N)
    r = ps.solve()
    dt = time.time() - t0
    if r is False:
        print(f"N={N}: UNSAT !!! ({dt:.1f}s)  <-- #197 RESOLVED (NO)")
        return False
    if r is None:
        print(f"N={N}: gave up on transitivity rounds ({dt:.1f}s)")
        return None
    order, team = r
    A = sorted(v for v in team if team[v])
    B = sorted(v for v in team if not team[v])
    print(f"N={N}: SAT ({dt:.1f}s)  |A|={len(A)} |B|={len(B)}")
    return order, team


if __name__ == "__main__":
    Ns = [int(x) for x in sys.argv[1:]] or [16, 32, 48, 64, 96, 128]
    for N in Ns:
        res = run(N)
        if res is False:
            break
