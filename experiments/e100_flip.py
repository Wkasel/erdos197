"""e100_flip: TASK M3 -- what exactly flips at mod 8.

For M in 40..120 step 4 (residues 0 and 4 mod 8), compute the FORCED
consequences (failed-literal probing over the six C3 values' 15 pair orders)
of AP-freeness + each subset of the C3 axioms (sizes 1, 2, 3).

Six values:  t5 = 2M-5, t3 = 2M-3, t10 = 2M-10, b3 = M+3, b5 = M+5, b6 = M+6.
C3 axioms:   A1: t5 < b5   A2: t3 < b6   A3: t10 < b3   ("x < y" = x before y in T).

For each subset: bootstrap AP clauses + axiom units, lazy-transitivity loop
(as e89), then for each of the 15 unordered pairs probe both orientations
under assumptions; an UNSAT probe means the opposite orientation is forced.
Learned transitivity clauses (valid for every total order) are pooled and
shared across subsets at the same M.

Then compare residue 0 vs residue 4: which forced literals are
residue-dependent, which 2-subset carries the flip, and in particular
whether A1+A2 force NOT A3 (i.e. b3 < t10) exactly at M == 0 mod 8.

Output: data/e100_flip.json + printed analysis.
"""
import itertools
import json
import sys
import time

import numpy as np
from pysat.solvers import Cadical195

AXIOMS = {"A1": ("t5", "b5"), "A2": ("t3", "b6"), "A3": ("t10", "b3")}
CONFIGS = [("A1",), ("A2",), ("A3",),
           ("A1", "A2"), ("A1", "A3"), ("A2", "A3"),
           ("A1", "A2", "A3")]


def run_M(M):
    lo, hi = M, 2 * M
    V = list(range(lo + 1, hi + 1))
    n = len(V)
    idx = {v: i for i, v in enumerate(V)}
    var = {}
    c = 0
    for i in range(n):
        for j in range(i + 1, n):
            c += 1
            var[(i, j)] = c

    def lit(i, j):  # index-based: true iff position(V[i]) before position(V[j])
        return var[(i, j)] if i < j else -var[(j, i)]

    def o(u, w):  # value-based
        return lit(idx[u], idx[w])

    ap = []
    for y in V:
        d = 1
        while y + d <= hi:
            x, z = y - d, y + d
            d += 1
            if x > lo:
                ap.append([-o(x, y), -o(y, z)])  # no rising x,y,z
                ap.append([-o(z, y), -o(y, x)])  # no falling x,y,z
    six = {"t5": 2 * M - 5, "t3": 2 * M - 3, "t10": 2 * M - 10,
           "b3": M + 3, "b5": M + 5, "b6": M + 6}
    pairs = list(itertools.combinations(sorted(six), 2))
    pool = []  # learned transitivity clauses, valid for any total order

    def lazy(sol, assum):
        while True:
            if not sol.solve(assumptions=assum):
                return "UNSAT"
            model = set(l for l in sol.get_model() if l > 0)
            B = np.zeros((n, n), dtype=bool)
            for (i, j), vv in var.items():
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
                new.append([-lit(i, int(ks[0])), -lit(int(ks[0]), j), lit(i, j)])
            sol.append_formula(new)
            pool.extend(new)

    out = {}
    for cfg in CONFIGS:
        t0 = time.time()
        units = [[o(six[AXIOMS[a][0]], six[AXIOMS[a][1]])] for a in cfg]
        sol = Cadical195(bootstrap_with=ap + units + pool)
        base = lazy(sol, [])
        forced = []
        if base == "SAT":
            for p, q in pairs:
                u, w = six[p], six[q]
                if lazy(sol, [o(u, w)]) == "UNSAT":
                    forced.append(f"{q}<{p}")
                elif lazy(sol, [o(w, u)]) == "UNSAT":
                    forced.append(f"{p}<{q}")
        sol.delete()
        key = "+".join(cfg)
        out[key] = {"base": base, "forced": sorted(forced)}
        print(f"  M={M} {key}: {base} forced={sorted(forced)} "
              f"({time.time()-t0:.1f}s)", flush=True)
    return out


def analyze(results):
    lines = []
    Ms = sorted(int(m) for m in results)
    r0 = [m for m in Ms if m % 8 == 0]
    r4 = [m for m in Ms if m % 8 == 4]
    lines.append(f"M sweep: residue0={r0}  residue4={r4}")
    flips = {}
    for cfg in ["+".join(c) for c in CONFIGS]:
        f0 = [set(results[str(m)][cfg]["forced"]) for m in r0]
        f4 = [set(results[str(m)][cfg]["forced"]) for m in r4]
        b0 = {results[str(m)][cfg]["base"] for m in r0}
        b4 = {results[str(m)][cfg]["base"] for m in r4}
        stable0 = all(s == f0[0] for s in f0)
        stable4 = all(s == f4[0] for s in f4)
        core0 = set.intersection(*f0) if f0 else set()
        any4 = set.union(*f4) if f4 else set()
        core4 = set.intersection(*f4) if f4 else set()
        any0 = set.union(*f0) if f0 else set()
        only0 = core0 - any4   # forced at EVERY res-0 M, at NO res-4 M
        only4 = core4 - any0
        flips[cfg] = (only0, only4)
        lines.append(f"[{cfg}] base r0={sorted(b0)} r4={sorted(b4)} | "
                     f"stable within residue: r0={stable0} r4={stable4}")
        lines.append(f"  forced@r0 (all M): {sorted(core0)}")
        lines.append(f"  forced@r4 (all M): {sorted(core4)}")
        lines.append(f"  ONLY at r0: {sorted(only0)}   ONLY at r4: {sorted(only4)}")
    lines.append("")
    minimal = None
    for cfg in ["A1+A2", "A1+A3", "A2+A3"]:
        o0, o4 = flips[cfg]
        if o0 or o4:
            minimal = (cfg, sorted(o0), sorted(o4))
            break
    lines.append(f"Minimal 2-subset with residue-dependent forced set: {minimal}")
    # the headline test: do A1+A2 force NOT A3 (= b3<t10) exactly at r0?
    neg_a3 = "b3<t10"
    at0 = all(neg_a3 in results[str(m)]["A1+A2"]["forced"] for m in r0)
    at4 = any(neg_a3 in results[str(m)]["A1+A2"]["forced"] for m in r4)
    lines.append(f"A1+A2 force NOT-A3 (b3<t10) at every M=0 mod 8: {at0}; "
                 f"at any M=4 mod 8: {at4}")
    return "\n".join(lines)


if __name__ == "__main__":
    Ms = list(range(40, 121, 4))
    if len(sys.argv) > 1:  # optional explicit M list for spot checks
        Ms = [int(a) for a in sys.argv[1:]]
    results = {}
    for M in Ms:
        t0 = time.time()
        results[str(M)] = run_M(M)
        print(f"M={M} done ({time.time()-t0:.1f}s)", flush=True)
        json.dump(results, open(
            "/Users/will/Dev/personal/tasks/math/erdos197/data/e100_flip.json",
            "w"), indent=1)
    print()
    print(analyze(results), flush=True)
