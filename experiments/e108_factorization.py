"""e108_factorization: does the S1 grading factor through its own literals
at FULL scale?  (Backs Section 4 of notes/33; distinct from the killed
half-scale kernels K2/K2'' of e101/e102, which were projections.)

Questions (all at full scale M, AP = all triples):

Q1  At M == 0 mod 4: does AP + {t3<b3, t10<b6} (layer-0 literals as the
    ONLY units -- A2/A3 dropped) force the layer-1 literals t3<t5, b5<b3?
    And the flip b5<t5 at M == 0 mod 8?
Q2  At M == 0 mod 8: does AP + {t3<b3, t10<b6, t3<t5, b5<b3}
    (layers 0-1 as units) force the flip b5<t5?
Q3  Same hypotheses: are the original axioms A2 (t3<b6), A3 (t10<b3)
    recoverable (forced)?
Q4  Control at M == 4 mod 8 for Q2 (flip should NOT be forced there if
    the literal set carries the grading; if it is forced at neither or
    both, the literal set does not carry the mod-8 distinction).

If Q2 = YES at r0 and NO at r4, the grading factors through the layer
literals and the induction in notes/33 can be restated literal-to-literal.
If NO at both, that is a strengthening of S2 at full scale: even the
un-projected layer literals do not carry the flip; the forcing power of
A2+A3 exceeds its six-value shadow.  Either outcome is a step of the
notes/33 proof program and is recorded there.

Output: data/e108_factorization.json
"""
import json
import time

import numpy as np
from pysat.solvers import Cadical195

DATA = "/Users/will/Dev/personal/tasks/math/erdos197/data/e108_factorization.json"


class Interval:
    """Lazy-transitivity AP-free order machinery on (lo, 2*lo] (e89/e101)."""

    def __init__(self, lo):
        self.lo, self.hi = lo, 2 * lo
        self.V = list(range(lo + 1, 2 * lo + 1))
        self.n = len(self.V)
        self.idx = {v: i for i, v in enumerate(self.V)}
        self.var = {}
        c = 0
        for i in range(self.n):
            for j in range(i + 1, self.n):
                c += 1
                self.var[(i, j)] = c
        self.ap = []
        for y in self.V:
            d = 1
            while y + d <= self.hi:
                x, z = y - d, y + d
                d += 1
                if x > self.lo:
                    self.ap.append([-self.o(x, y), -self.o(y, z)])
                    self.ap.append([-self.o(z, y), -self.o(y, x)])
        self.pool = []

    def lit(self, i, j):
        return self.var[(i, j)] if i < j else -self.var[(j, i)]

    def o(self, u, w):
        return self.lit(self.idx[u], self.idx[w])

    def lazy(self, sol, assum=()):
        n = self.n
        while True:
            if not sol.solve(assumptions=list(assum)):
                return "UNSAT"
            model = set(l for l in sol.get_model() if l > 0)
            B = np.zeros((n, n), dtype=bool)
            for (i, j), vv in self.var.items():
                if vv in model:
                    B[i, j] = True
                else:
                    B[j, i] = True
            R2 = (B.astype(np.uint8) @ B.astype(np.uint8)) > 0
            miss = R2 & ~B & ~np.eye(n, dtype=bool) & B.T
            ii, jj = np.nonzero(miss)
            if len(ii) == 0:
                return "SAT"
            new = []
            for i, j in zip(ii[:30000], jj[:30000]):
                ks = np.nonzero(B[i] & B[:, j])[0]
                new.append([-self.lit(i, int(ks[0])),
                            -self.lit(int(ks[0]), j), self.lit(i, j)])
            sol.append_formula(new)
            self.pool.extend(new)

    def probe(self, units, pairs):
        sol = Cadical195(bootstrap_with=self.ap + [[u] for u in units]
                         + self.pool)
        try:
            if self.lazy(sol) == "UNSAT":
                return "UNSAT-BASE"
            out = {}
            for u, w in pairs:
                if self.lazy(sol, [self.o(u, w)]) == "UNSAT":
                    out[(u, w)] = "REV-FORCED"      # w<u forced
                elif self.lazy(sol, [self.o(w, u)]) == "UNSAT":
                    out[(u, w)] = "FORCED"          # u<w forced
                else:
                    out[(u, w)] = "free"
            return out
        finally:
            sol.delete()


def six(M):
    return {"t5": 2 * M - 5, "t3": 2 * M - 3, "t10": 2 * M - 10,
            "b3": M + 3, "b5": M + 5, "b6": M + 6}


def main():
    t00 = time.time()
    out = {}
    for M in (44, 48, 52, 56, 60, 64, 72, 76):
        t0 = time.time()
        iv = Interval(M)
        s = six(M)
        L0 = [iv.o(s["t3"], s["b3"]), iv.o(s["t10"], s["b6"])]
        L1 = [iv.o(s["t3"], s["t5"]), iv.o(s["b5"], s["b3"])]
        probe_pairs = [(s["t3"], s["t5"]), (s["b5"], s["b3"]),
                       (s["b5"], s["t5"]),
                       (s["t3"], s["b6"]), (s["t10"], s["b3"])]
        names = ["t3<t5(L1)", "b5<b3(L1)", "b5<t5(flip)",
                 "t3<b6(A2)", "t10<b3(A3)"]
        r1 = iv.probe(L0, probe_pairs)
        r2 = iv.probe(L0 + L1, probe_pairs[2:])
        e1 = {nm: r1[p] for nm, p in zip(names, probe_pairs)} \
            if r1 != "UNSAT-BASE" else "UNSAT-BASE"
        e2 = {nm: r2[p] for nm, p in zip(names[2:], probe_pairs[2:])} \
            if r2 != "UNSAT-BASE" else "UNSAT-BASE"
        out[str(M)] = {"mod8": M % 8, "Q1_under_L0": e1,
                       "Q2Q3_under_L0+L1": e2,
                       "time_s": round(time.time() - t0, 1)}
        print(f"M={M} (mod8={M % 8}): under L0 alone: {e1}", flush=True)
        print(f"          under L0+L1: {e2}  ({out[str(M)]['time_s']}s)",
              flush=True)
    json.dump(out, open(DATA, "w"), indent=1)
    print(f"Done ({time.time()-t00:.0f}s) -> {DATA}", flush=True)


if __name__ == "__main__":
    main()
