"""Erdős #197 — exact SAT decision of the per-block problem.

decide(B, Z): does a linear order of the set B exist with
  (a) no monotone 3-AP (x, y, z=y+d in B, positions monotone in the
      same direction as values),
  (b) for y < z in B with 2y - z in Z: z precedes y.

Encoding: boolean var p[u][v] for u < v meaning "u precedes v".
  (a): for each AP (x, y, z): NOT(x<y<z in position) and NOT(z<y<x):
       clause (~before(x,y) | ~before(y,z)) and (~before(z,y) | ~before(y,x)).
  (b): unit clause before(z, y).
Transitivity: lazy — solve, topological-check the induced tournament for
3-cycles, add triangle clauses, repeat. (The tournament on n nodes always
gives a total relation; acyclic <=> transitive here since it's a
complete relation: cycles reduce to 3-cycles.)
"""
from pysat.solvers import Cadical195
from itertools import combinations


class OrderSAT:
    def __init__(self, B):
        self.B = sorted(B)
        self.idx = {v: i for i, v in enumerate(self.B)}
        self.n = len(self.B)
        self.varmap = {}
        c = 1
        for i in range(self.n):
            for j in range(i + 1, self.n):
                self.varmap[(i, j)] = c
                c += 1
        self.clauses = []

    def before(self, u, v):
        """literal: value u precedes value v"""
        i, j = self.idx[u], self.idx[v]
        if i < j:
            return self.varmap[(i, j)]
        return -self.varmap[(j, i)]

    def add(self, *lits):
        self.clauses.append(list(lits))

    def solve(self, max_rounds=200):
        s = Cadical195(bootstrap_with=self.clauses)
        rounds = 0
        while True:
            rounds += 1
            if rounds > max_rounds:
                return None  # give up (shouldn't happen)
            if not s.solve():
                return False
            model = set(l for l in s.get_model() if l > 0)

            def bef(i, j):  # index-based
                if i < j:
                    return self.varmap[(i, j)] in model
                return self.varmap[(j, i)] not in model

            # find 3-cycles: i->j if bef(i,j). complete tournament; find a
            # directed triangle via degree argument
            # order by number of wins; a cycle exists iff not transitive
            wins = [0] * self.n
            for i in range(self.n):
                for j in range(self.n):
                    if i != j and bef(i, j):
                        wins[i] += 1
            order = sorted(range(self.n), key=lambda i: -wins[i])
            # check consistency: order[i] should beat order[j] for i<j
            bad = []
            for a in range(self.n):
                for b in range(a + 1, self.n):
                    i, j = order[a], order[b]
                    if not bef(i, j):
                        # find k to make triangle i,j,k: j beats i; need k
                        # with i beats k, k beats j
                        for c in range(self.n):
                            k = order[c]
                            if k != i and k != j and bef(i, k) and bef(k, j):
                                bad.append((j, i, k))  # j->i, i->k, k->j cycle
                                break
                        else:
                            bad.append(None)
                        break
                if bad:
                    break
            if not bad:
                # extract sequence
                seq = [self.B[i] for i in order]
                return seq
            if bad[0] is None:
                # fallback: forbid this exact inversion pattern minimally —
                # shouldn't happen in a complete tournament
                raise RuntimeError("triangle not found")
            j, i, k = bad[0]
            # cycle j->i->k->j : forbid it (add transitivity clause)
            def lit(i2, j2):
                if i2 < j2:
                    return self.varmap[(i2, j2)]
                return -self.varmap[(j2, i2)]
            # j before i AND i before k -> j before k
            s.add_clause([-lit(j, i), -lit(i, k), lit(j, k)])
            self.clauses.append([-lit(j, i), -lit(i, k), lit(j, k)])


def decide(B, Z, return_seq=False):
    """True/seq if arrangement exists, False if not."""
    Bs = sorted(B)
    Bset = set(Bs)
    enc = OrderSAT(Bs)
    # (a) monotone 3-AP clauses
    for y in Bs:
        d = 1
        while True:
            x, z = y - d, y + d
            if z > Bs[-1]:
                break
            if x in Bset and z in Bset:
                enc.add(-enc.before(x, y), -enc.before(y, z))
                enc.add(-enc.before(z, y), -enc.before(y, x))
            d += 1
    # (b) forced precedences
    for y in Bs:
        for x in Z:
            z = 2 * y - x
            if z > y and z in Bset:
                enc.add(enc.before(z, y))
    res = enc.solve()
    if res is False or res is None:
        return False
    return res if return_seq else True


def verify(B, Z, seq):
    pos = {v: i for i, v in enumerate(seq)}
    Bset = set(B)
    for y in seq:
        d = 1
        while y + d <= max(Bset):
            x, z = y - d, y + d
            if x in Bset and z in Bset:
                if pos[x] < pos[y] < pos[z] or pos[x] > pos[y] > pos[z]:
                    return f"3-AP {x},{y},{z}"
            d += 1
    for y in Bset:
        for x in Z:
            z = 2 * y - x
            if z > y and z in Bset and pos[z] > pos[y]:
                return f"(b) fail y={y} z={z} x={x}"
    return None


if __name__ == "__main__":
    import time
    # sanity: reproduce e1 results
    for M, expect in [(8, True), (16, False)]:
        Z = set(range(M // 4 + 1, M // 2 + 1))
        hi, lo = M // 8, M // 16
        while lo >= 1:
            Z.update(range(lo + 1, hi + 1))
            hi //= 4
            lo //= 4
        t0 = time.time()
        r = decide(range(M + 1, 2 * M + 1), Z, return_seq=True)
        ok = (r is not False)
        print(f"M={M}: {'SAT' if ok else 'UNSAT'} (expect {'SAT' if expect else 'UNSAT'}) {time.time()-t0:.1f}s")
        if ok:
            err = verify(range(M + 1, 2 * M + 1), Z, r)
            print("  verify:", err or "OK")
