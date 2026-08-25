"""e101_invariant: TASK T -- invariant synthesis (round 1).

CANDIDATE INVARIANTS (each machine-falsifiable; designed for halving proofs).

Notation: interval (M,2M]; A1: t5<b5, A2: t3<b6, A3: t10<b3 (x<y = x before y
in T); t_j = 2M-j, b_j = M+j.  Odd-class halving h+(v) = (v+1)/2 maps the odd
values of (M,2M] onto (m,2m], m = M/2, preserving AP-freeness and relative
order (e99).  Images: b5 -> m+3, b3 -> m+2, t3 -> 2m-1, t5 -> 2m-2.

I1 (L1 lemma, conjectured RESIDUE-FREE): for every even M, in any AP-free
   order of (M,2M]:  A2 & A3  ==>  t3<t5, b5<b3, t3<b3 (and t10<b6).
   [e100 verified this at M == 0 mod 4 only; here swept over all even M
    40..128 + odd spot checks.]

I2 (K2 kernel, conjectured DICHOTOMY CARRIER): for m == 0 mod 4, any AP-free
   order of (m,2m] with  m+3 < m+2,  2m-1 < m+2,  2m-1 < 2m-2   also has
   m+3 < 2m-2;  for m == 2 mod 4 it need not (kernel SAT with 2m-2 < m+3).
   In offset language: b3'<b2', t1'<b2', t1'<t2' ==> b3'<t2'.

I3 (factorization): the mod-8 flip at scale M is EXACTLY I1 + halving + K2
   at scale M/2:  T |= AP+C3, M == 0 mod 8  ==>  (I1) odd-class literals
   forced  ==>  (h+) level-2 O-suborder satisfies K2's three hypotheses AND
   (from A1) 2m-2 < m+3  ==>  contradiction by K2 since m = M/2 == 0 mod 4.
   Machine content: at r0, L1 verdicts + K2 UNSAT at M/2; at r4, L1 still
   holds but K2 is SAT at M/2 == 2 mod 4 -- the dichotomy lives in K2 alone.

Part D (round-2 probe): under AP + K2-hypotheses at scale m, probe forced
   literals among end-window values, split by m mod 4 -- localize the next
   descent (candidate quarter-scale kernel K1).

Usage: python e101_invariant.py [quick|A|B|C|D|all]
Output: data/e101_invariant.json
"""
import itertools
import json
import sys
import time

import numpy as np
from pysat.solvers import Cadical195

DATA = "/Users/will/Dev/personal/tasks/math/erdos197/data/e101_invariant.json"


class Interval:
    """Lazy-transitivity AP-free order machinery on (lo, 2*lo] (e89/e100)."""

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
        self.pool = []  # learned transitivity clauses (order-universal)

    def lit(self, i, j):
        return self.var[(i, j)] if i < j else -self.var[(j, i)]

    def o(self, u, w):  # value-based: positive iff u before w
        return self.lit(self.idx[u], self.idx[w])

    def solver(self, units):
        return Cadical195(bootstrap_with=self.ap + [[u] for u in units]
                          + self.pool)

    def lazy(self, sol, assum=()):
        """Solve to a genuine total order (lazy transitivity). Returns
        'SAT'/'UNSAT'; on SAT self.model_order holds the value order."""
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
                wins = B.sum(axis=1)
                self.model_order = [self.V[i] for i in
                                    sorted(range(n), key=lambda i: -int(wins[i]))]
                return "SAT"
            new = []
            for i, j in zip(ii[:30000], jj[:30000]):
                ks = np.nonzero(B[i] & B[:, j])[0]
                new.append([-self.lit(i, int(ks[0])),
                            -self.lit(int(ks[0]), j), self.lit(i, j)])
            sol.append_formula(new)
            self.pool.extend(new)

    def probe_pairs(self, units, pairs):
        """Under AP + units: for each (u,w) in pairs decide forced order.
        Returns dict (u,w) -> 'u<w' | 'w<u' | 'free', or 'UNSAT-BASE'."""
        sol = self.solver(units)
        try:
            if self.lazy(sol) == "UNSAT":
                return "UNSAT-BASE"
            out = {}
            for u, w in pairs:
                if self.lazy(sol, [self.o(u, w)]) == "UNSAT":
                    out[(u, w)] = "w<u"
                elif self.lazy(sol, [self.o(w, u)]) == "UNSAT":
                    out[(u, w)] = "u<w"
                else:
                    out[(u, w)] = "free"
            return out
        finally:
            sol.delete()

    def status(self, units):
        """SAT/UNSAT of AP + units (as a genuine order problem)."""
        sol = self.solver(units)
        try:
            return self.lazy(sol)
        finally:
            sol.delete()


def six(M):
    return {"t5": 2 * M - 5, "t3": 2 * M - 3, "t10": 2 * M - 10,
            "b3": M + 3, "b5": M + 5, "b6": M + 6}


def k2_units(iv, m):
    """K2 hypotheses at scale m: X1 = b3'<b2', X2 = t1'<b2', X3 = t1'<t2'."""
    return {"X1": iv.o(m + 3, m + 2), "X2": iv.o(2 * m - 1, m + 2),
            "X3": iv.o(2 * m - 1, 2 * m - 2)}


# --------------------------------------------------------------- Part A: I1
def part_A(Ms):
    """L1 lemma: AP + A2 + A3 -- forced status of t3<t5, b5<b3, t3<b3,
    t10<b6 and the flip pair (t5,b5), at every M in Ms."""
    res = {}
    for M in Ms:
        t0 = time.time()
        iv = Interval(M)
        s = six(M)
        units = [iv.o(s["t3"], s["b6"]), iv.o(s["t10"], s["b3"])]  # A2, A3
        pairs = [(s["t3"], s["t5"]), (s["b5"], s["b3"]), (s["t3"], s["b3"]),
                 (s["t10"], s["b6"]), (s["b5"], s["t5"])]
        names = ["t3<t5", "b5<b3", "t3<b3", "t10<b6", "b5<t5(flip)"]
        pr = iv.probe_pairs(units, pairs)
        if pr == "UNSAT-BASE":
            res[M] = {"base": "UNSAT"}
        else:
            verdicts = {}
            for (u, w), st, nm in zip(pairs, [pr[p] for p in pairs], names):
                verdicts[nm] = {"u<w": "FORCED", "w<u": "REV-FORCED",
                                "free": "free"}[st]
            res[M] = {"base": "SAT", "forced": verdicts}
        print(f"[A] M={M} (mod8={M % 8}): {res[M]} ({time.time()-t0:.1f}s)",
              flush=True)
    return res


# --------------------------------------------------------------- Part B: I2
def part_B(ms, minimality_ms=()):
    """K2 kernel: at scale m, AP + {X1,X2,X3}: base SAT? goal b3'<t2' forced?
    Kernel = AP+X1+X2+X3+[t2'<b3'] UNSAT?  Optionally subset minimality."""
    res = {}
    for m in ms:
        t0 = time.time()
        iv = Interval(m)
        ku = k2_units(iv, m)
        goal = iv.o(m + 3, 2 * m - 2)          # b3' < t2'
        neg = iv.o(2 * m - 2, m + 3)           # t2' < b3'
        base = iv.status(list(ku.values()))
        entry = {"base": base}
        if base == "SAT":
            kernel = iv.status(list(ku.values()) + [neg])
            withgoal = iv.status(list(ku.values()) + [goal])
            entry["kernel_neg"] = kernel        # UNSAT <=> goal forced
            entry["with_goal"] = withgoal
        if m in minimality_ms:
            sub = {}
            for r in (1, 2):
                for combo in itertools.combinations(sorted(ku), r):
                    st = iv.status([ku[k] for k in combo] + [neg])
                    sub["+".join(combo)] = st
            entry["subsets_with_neg"] = sub
        res[m] = entry
        print(f"[B] m={m} (mod4={m % 4}): {entry} ({time.time()-t0:.1f}s)",
              flush=True)
    return res


# --------------------------------------------------------------- Part C: I3
def part_C(Ms_r0, Ms_r4, resA, resB):
    """Factorization audit: chain composes at r0; breaks exactly at K2 at r4.
    Also re-verify direct C3 status at the sweep endpoints."""
    out = {"r0": {}, "r4": {}}
    for M in Ms_r0:
        m = M // 2
        l1 = resA.get(M, {})
        ok_l1 = (l1.get("base") == "SAT"
                 and all(l1["forced"][k] == "FORCED"
                         for k in ("t3<t5", "b5<b3", "t3<b3")))
        k2 = resB.get(m, {})
        ok_k2 = k2.get("kernel_neg") == "UNSAT"
        out["r0"][M] = {"L1": ok_l1, "K2_at_M/2": ok_k2,
                        "chain_closes": ok_l1 and ok_k2}
        print(f"[C] r0 M={M}: L1={ok_l1} K2(m={m})={ok_k2} "
              f"chain={'CLOSES' if ok_l1 and ok_k2 else 'BROKEN'}", flush=True)
    for M in Ms_r4:
        m = M // 2
        l1 = resA.get(M, {})
        ok_l1 = (l1.get("base") == "SAT"
                 and all(l1["forced"][k] == "FORCED"
                         for k in ("t3<t5", "b5<b3", "t3<b3")))
        k2sat = resB.get(m, {}).get("kernel_neg") == "SAT"
        out["r4"][M] = {"L1": ok_l1, "K2_neg_SAT_at_M/2": k2sat,
                        "break_is_exactly_K2": ok_l1 and k2sat}
        print(f"[C] r4 M={M}: L1={ok_l1} K2-neg SAT(m={m})={k2sat} "
              f"break-at-K2={'YES' if ok_l1 and k2sat else 'NO'}", flush=True)
    # direct C3 spot re-verification at the extremes of the sweep
    for M, want in ((max(Ms_r0), "UNSAT"), (max(Ms_r4), "SAT")):
        iv = Interval(M)
        s = six(M)
        st = iv.status([iv.o(s["t5"], s["b5"]), iv.o(s["t3"], s["b6"]),
                        iv.o(s["t10"], s["b3"])])
        out[f"directC3_M{M}"] = st
        print(f"[C] direct C3 at M={M}: {st} (expected {want})", flush=True)
        assert st == want, (M, st, want)
    return out


# --------------------------------------------------------------- Part D
def part_D(ms, wdb=6, wdt=6):
    """Round-2 probe: under AP + K2 hypotheses, forced literals among the
    end-window values {m+1..m+wdb} u {2m-wdt..2m}; split by m mod 4."""
    res = {}
    for m in ms:
        t0 = time.time()
        iv = Interval(m)
        ku = k2_units(iv, m)
        W = list(range(m + 1, m + wdb + 1)) + \
            list(range(2 * m - wdt, 2 * m + 1))
        pairs = list(itertools.combinations(W, 2))
        pr = iv.probe_pairs(list(ku.values()), pairs)
        if pr == "UNSAT-BASE":
            res[m] = {"base": "UNSAT"}
        else:
            forced = {}
            for (u, w), st in pr.items():
                if st == "u<w":
                    forced[f"{u}<{w}"] = True
                elif st == "w<u":
                    forced[f"{w}<{u}"] = True
            res[m] = {"base": "SAT", "forced": sorted(forced)}
        print(f"[D] m={m} (mod4={m % 4}): {len(res[m].get('forced', []))} "
              f"forced of {len(pairs)} pairs ({time.time()-t0:.1f}s)",
              flush=True)
    return res


def offsets(m, lits):
    """Rewrite value literals u<w into offset language b_j / t_j at scale m."""
    def nm(v):
        return f"b{v - m}" if v - m <= m // 2 else f"t{2 * m - v}"
    out = []
    for s in lits:
        u, w = s.split("<")
        out.append(f"{nm(int(u))}<{nm(int(w))}")
    return out


def analyze_D(resD):
    ms0 = [m for m in resD if m % 4 == 0 and resD[m].get("base") == "SAT"]
    ms2 = [m for m in resD if m % 4 == 2 and resD[m].get("base") == "SAT"]
    f0 = [set(offsets(m, resD[m]["forced"])) for m in ms0]
    f2 = [set(offsets(m, resD[m]["forced"])) for m in ms2]
    core0 = set.intersection(*f0) if f0 else set()
    core2 = set.intersection(*f2) if f2 else set()
    any0 = set.union(*f0) if f0 else set()
    any2 = set.union(*f2) if f2 else set()
    lines = [
        f"m==0(4) sample {sorted(ms0)}  stable={all(s == f0[0] for s in f0)}",
        f"m==2(4) sample {sorted(ms2)}  stable={all(s == f2[0] for s in f2)}",
        f"forced at ALL m==0(4): {sorted(core0)}",
        f"forced at ALL m==2(4): {sorted(core2)}",
        f"ONLY at 0(4): {sorted(core0 - any2)}",
        f"ONLY at 2(4): {sorted(core2 - any0)}",
        f"residue-free core: {sorted(core0 & core2)}",
    ]
    return lines


# ------------------------------------------------------------------- main
def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    t00 = time.time()
    results = {}

    if mode == "quick":
        # fast sanity: does the K2 kernel even have the dichotomy?
        part_B([20, 22, 24, 26, 28, 30])
        return

    if mode in ("A", "all"):
        Ms = list(range(40, 129, 2)) + [41, 45, 49, 53, 57]
        results["A"] = part_A(Ms)

    if mode in ("B", "all"):
        ms = list(range(16, 101, 2)) + [21, 25, 33, 41]
        results["B"] = part_B(ms, minimality_ms=(24, 26, 32, 34, 40, 48))

    if mode in ("C", "all"):
        Ms_r0 = list(range(40, 129, 8))
        Ms_r4 = list(range(44, 125, 8))
        results["C"] = part_C(Ms_r0, Ms_r4, results["A"], results["B"])

    if mode in ("D", "all"):
        ms = [24, 28, 32, 36, 40, 26, 30, 34, 38, 42]
        results["D"] = part_D(ms)
        for ln in analyze_D(results["D"]):
            print("[D-analysis] " + ln, flush=True)

    def keyed(d):
        return {str(k): v for k, v in d.items()} if isinstance(d, dict) else d
    json.dump({k: keyed(v) for k, v in results.items()},
              open(DATA, "w"), indent=1, default=str)
    print(f"\nDone ({time.time()-t00:.0f}s) -> {DATA}", flush=True)


if __name__ == "__main__":
    main()
