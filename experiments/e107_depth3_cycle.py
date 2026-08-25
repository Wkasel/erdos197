"""e107_depth3_cycle: machine checks for notes/33 (TASK P hand proof).

Three parts, each backing a specific step of the notes/33 proof:

Part 1 (CELL ARITHMETIC -- backs Prop 2.1/2.2 of notes/33).
  For M == 0 mod 8, mu = M/8: every depth-3 cell (residue r mod 8,
  1<=r<=8) of (M,2M] equals {8k+r : mu <= k <= 2mu-1}; the six C3 values
  occupy cells R3, R5, R6 with roles
      b3 = min R3, t5 = max R3, b5 = min R5, t3 = max R5,
      b6 = min R6, t10 = second-max R6,
  so C3 reads: A1 = max R3 < min R5, A2 = max R5 < min R6,
  A3 = 2ndmax R6 < min R3 -- a directed 3-cycle R3 -> R5 -> R6 -> R3.
  For M == 4 mod 8 the six values fall in SIX distinct cells (no cycle).
  Checked for every M == 0 mod 8 in 40..512 and every M == 4 mod 8
  in 44..508.

Part 2 (ACT-LEVEL DECOMPOSITION -- backs Lemma 1.4 of notes/33).
  The set of AP triples of (M,2M] with nu2(d) <= 2 equals the disjoint
  union of the pullbacks, along the halving maps
  h+^{-1}(u) = 2u-1 (odd copy), hE^{-1}(u) = 2u (even copy),
  of the level-1 (odd-d) cross triples at scales M, M/2, M/4 over the
  parity tree of depth 3.  Checked exactly (set equality of triple
  lists) at M = 48, 64, 80, 96.

Part 3 (D3 VERDICTS -- backs Theorem 3.2 / [MACHINE-BASE] of notes/33).
  D3(M) := AP-triples restricted to nu2(d) <= 2 ("three interleave
  levels, no depth-3 in-cell AP constraints") + C3 units, solved as a
  genuine order problem (lazy transitivity, Cadical195).
  Expected from e103b + conjecture k*=3 iff nu2(M)>=4:
    UNSAT at nu2(M) >= 4:  M = 48, 64, 80, 96, 112, 128
    SAT   at nu2(M) == 3:  M = 40, 56, 72, 88, 104
    SAT   at M == 4 mod 8: M = 44, 52
  Fresh scales here: 88, 96, 104, 112, 128 (e103b stopped at 80).

Output: data/e107_depth3.json
"""
import json
import sys
import time

import numpy as np
from pysat.solvers import Cadical195

DATA = "/Users/will/Dev/personal/tasks/math/erdos197/data/e107_depth3.json"


def nu2(d):
    v = 0
    while d % 2 == 0:
        d //= 2
        v += 1
    return v


def six(M):
    return {"t5": 2 * M - 5, "t3": 2 * M - 3, "t10": 2 * M - 10,
            "b3": M + 3, "b5": M + 5, "b6": M + 6}


# ------------------------------------------------------------------ Part 1
def part1():
    res = {"r0_checked": [], "r4_checked": []}
    for M in range(40, 513, 8):
        mu = M // 8
        cells = {r: [8 * k + r for k in range(mu, 2 * mu)]
                 for r in range(1, 9)}
        # cells partition (M, 2M] and are index intervals of length mu
        allv = sorted(v for c in cells.values() for v in c)
        assert allv == list(range(M + 1, 2 * M + 1)), M
        for r in range(1, 9):
            assert len(cells[r]) == mu and all(v % 8 == r % 8
                                               for v in cells[r]), (M, r)
        s = six(M)
        # roles
        assert s["b3"] == min(cells[3]) and s["t5"] == max(cells[3]), M
        assert s["b5"] == min(cells[5]) and s["t3"] == max(cells[5]), M
        assert s["b6"] == min(cells[6]), M
        assert s["t10"] == sorted(cells[6])[-2], M   # second-max of R6
        res["r0_checked"].append(M)
    for M in range(44, 509, 8):
        s = six(M)
        cells_of = {k: v % 8 for k, v in s.items()}
        assert len(set(cells_of.values())) == 6, (M, cells_of)
        res["r4_checked"].append(M)
    print(f"[1] cell arithmetic OK at {len(res['r0_checked'])} scales r0 "
          f"(40..512 step 8) and {len(res['r4_checked'])} scales r4; "
          f"r0 cycle roles verified, r4 six distinct cells", flush=True)
    return {"r0_scales": len(res["r0_checked"]),
            "r4_scales": len(res["r4_checked"]), "status": "ALL-ASSERTS-PASS"}


# ------------------------------------------------------------------ Part 2
def ap_triples(lo, hi, pred=lambda d: True):
    """All APs (x,y,z), x<y<z, inside (lo,hi] with difference filter."""
    out = []
    for y in range(lo + 1, hi + 1):
        d = 1
        while y + d <= hi:
            x, z = y - d, y + d
            if x > lo and pred(d):
                out.append((x, y, z))
            d += 1
    return out


def part2(Ms=(48, 64, 80, 96)):
    res = {}
    for M in Ms:
        assert M % 8 == 0
        # target: all AP triples with nu2(d) <= 2
        target = set(t for t in ap_triples(M, 2 * M)
                     if nu2(t[1] - t[0]) <= 2)
        # build union of pullbacks of level-1 (odd-d) cross triples over
        # the depth-3 parity tree.  A node is a composition of maps
        # applied to values of (mm, 2mm].
        got = set()

        def pull(fn_chain, u):
            for f in reversed(fn_chain):
                u = f(u)
            return u

        hplus_inv = lambda u: 2 * u - 1   # odd copy
        he_inv = lambda u: 2 * u          # even copy

        nodes = [(M, [])]                 # (scale, chain of inverse maps)
        for depth in range(3):
            new = []
            for mm, chain in nodes:
                cross = ap_triples(mm, 2 * mm, pred=lambda d: d % 2 == 1)
                for (x, y, z) in cross:
                    got.add(tuple(sorted(
                        pull(chain, v) for v in (x, y, z))))
                if depth < 2:
                    new.append((mm // 2, chain + [hplus_inv]))
                    new.append((mm // 2, chain + [he_inv]))
            nodes = new
        assert got == target, (M, len(got), len(target),
                               list(got - target)[:3],
                               list(target - got)[:3])
        res[M] = {"n_triples": len(target), "identity": "EXACT"}
        print(f"[2] M={M}: act<=3 triples ({len(target)}) == union of "
              f"3-level cross pullbacks  EXACT", flush=True)
    return {str(M): v for M, v in res.items()}


# ------------------------------------------------------------------ Part 3
class LazyOrder:
    """Lazy-transitivity order solver over a value list with given
    forbidden-middle triples (per e89/e101)."""

    def __init__(self, values, triples):
        self.V = list(values)
        self.n = len(self.V)
        self.idx = {v: i for i, v in enumerate(self.V)}
        self.var = {}
        c = 0
        for i in range(self.n):
            for j in range(i + 1, self.n):
                c += 1
                self.var[(i, j)] = c
        self.cl = []
        for (x, y, z) in triples:
            self.cl.append([-self.o(x, y), -self.o(y, z)])
            self.cl.append([-self.o(z, y), -self.o(y, x)])

    def lit(self, i, j):
        return self.var[(i, j)] if i < j else -self.var[(j, i)]

    def o(self, u, w):
        return self.lit(self.idx[u], self.idx[w])

    def solve(self, units):
        sol = Cadical195(bootstrap_with=self.cl + [[u] for u in units])
        n = self.n
        try:
            while True:
                if not sol.solve():
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
        finally:
            sol.delete()


def part3(Ms=(40, 44, 48, 52, 56, 64, 72, 80, 88, 96, 104, 112, 128)):
    res = {}
    for M in Ms:
        t0 = time.time()
        triples = [t for t in ap_triples(M, 2 * M)
                   if nu2(t[1] - t[0]) <= 2]
        lo = LazyOrder(range(M + 1, 2 * M + 1), triples)
        s = six(M)
        st = lo.solve([lo.o(s["t5"], s["b5"]), lo.o(s["t3"], s["b6"]),
                       lo.o(s["t10"], s["b3"])])
        v2 = nu2(M) if M % 2 == 0 else 0
        expect = ("UNSAT" if (M % 8 == 0 and v2 >= 4) else "SAT")
        res[M] = {"nu2": v2, "mod8": M % 8, "D3+C3": st,
                  "expected(k*=3 iff nu2>=4)": expect,
                  "match": st == expect, "time_s": round(time.time() - t0, 1)}
        print(f"[3] M={M} (nu2={v2}, mod8={M % 8}): D3+C3 {st} "
              f"(expected {expect}, {'MATCH' if st == expect else 'MISMATCH'}"
              f", {res[M]['time_s']}s)", flush=True)
    return {str(M): v for M, v in res.items()}


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    out = {}
    t0 = time.time()
    if mode in ("1", "all"):
        out["part1"] = part1()
    if mode in ("2", "all"):
        out["part2"] = part2()
    if mode in ("3", "all"):
        out["part3"] = part3()
    json.dump(out, open(DATA, "w"), indent=1)
    print(f"Done ({time.time()-t0:.0f}s) -> {DATA}", flush=True)


if __name__ == "__main__":
    main()
