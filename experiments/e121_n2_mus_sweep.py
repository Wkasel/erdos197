"""e121_n2_mus_sweep: FRONT N2 step 1 -- MUS anatomy of the generic-pair core.

For each adjacent pair {x, x+1} (x = 11, 13, 15, 17, 19, 21) and each
M in {48, 64, 80, 96, 128} (all = 0 mod 16, the C3-friendly class), build
the single-block order gadget OG_{x,x+1}(M) on the interval (M, 2M] with a
COMPLETE encoding (AP-midpoint clauses + full 2*C(n,3) transitivity, no
CEGAR -- the g4c formulation), attack units selector-guarded:

    unit (a, j):  t_{a-2j} < b_j    (z = 2M + 2j - a  before  y = M + j),
    a in {x, x+1}, j = 1 .. a//2.

Then, per (pair, M):
  (i)   verdict of the full rung (all units);
  (ii)  EXHAUSTIVE enumeration of every minimal UNSAT core of size <= 3
        over the attack units (singles, then pairs, then triples skipping
        supersets of smaller cores) -- the complete "C3-analogue"
        catalogue.  C3 itself is {(15,5), (15,6), (16,3)} for {15,16};
  (iii) a deletion-minimal MUS from the full unit set (catches pairs
        whose minimal cores are all of size >= 4).
Units are recorded as (i, j) = (t-offset, b-offset); the attacker is
recovered as a = i + 2j.

Run: .venv/bin/python experiments/e121_n2_mus_sweep.py
Output: data/e121_n2_mus.json
"""
import itertools
import json
import sys
import time

from pysat.solvers import Cadical195

DATA = "/Users/will/Dev/personal/tasks/math/erdos197/data/e121_n2_mus.json"
PAIRS = [11, 13, 15, 17, 19, 21]
SCALES = [48, 64, 80, 96, 128]


def build(M, x):
    """Complete-encoding instance for OG_{x,x+1}(M).  Returns
    (solver, units) with units: selector-lit -> (i, j) (t-off, b-off)."""
    n = M
    var = {}
    c = 0
    for p in range(n):
        for q in range(p + 1, n):
            c += 1
            var[(p, q)] = c

    def o(u, w):
        p, q = u - M - 1, w - M - 1
        return var[(p, q)] if p < q else -var[(q, p)]

    cl = []
    for y in range(M + 2, 2 * M):
        d = 1
        while y + d <= 2 * M and y - d > M:
            a, b = y - d, y + d
            cl.append([-o(a, y), -o(y, b)])
            cl.append([-o(b, y), -o(y, a)])
            d += 1
    for p in range(n):
        for q in range(p + 1, n):
            vpq = var[(p, q)]
            for r in range(q + 1, n):
                vqr, vpr = var[(q, r)], var[(p, r)]
                cl.append([-vpq, -vqr, vpr])
                cl.append([vpq, vqr, -vpr])
    units = {}
    nv = c
    for a in (x, x + 1):
        for j in range(1, a // 2 + 1):
            z = 2 * M + 2 * j - a
            y = M + j
            if not (M < z <= 2 * M):
                continue
            nv += 1
            units[nv] = (a - 2 * j, j)
            cl.append([o(z, y), -nv])
    sol = Cadical195(bootstrap_with=cl)
    return sol, units


def min_core(sol, sel):
    """Deletion-minimal subset of sel keeping UNSAT."""
    assert not sol.solve(assumptions=sel)
    core = set(sol.get_core() or sel) & set(sel)
    work = [s for s in sel if s in core]
    i = 0
    while i < len(work):
        cand = work[:i] + work[i + 1:]
        if not sol.solve(assumptions=cand):
            c2 = set(sol.get_core() or cand) & set(cand)
            work = [s for s in cand if s in c2]
        else:
            i += 1
    return sorted(work)


def main():
    out = {"rows": []}
    for x in PAIRS:
        for M in SCALES:
            t0 = time.time()
            sol, units = build(M, x)
            sel = sorted(units)
            sat = sol.solve(assumptions=sel)
            row = {"x": x, "M": M, "n_units": len(sel),
                   "full": "SAT" if sat else "UNSAT"}
            if sat:
                print(f"pair {{{x},{x+1}}} M={M}: FULL RUNG SAT "
                      f"({time.time()-t0:.0f}s)", flush=True)
                out["rows"].append(row)
                sol.delete()
                json.dump(out, open(DATA, "w"), indent=1)
                continue
            cores = []          # minimal cores as sorted (i,j) lists
            core_sets = []      # as sets of selector lits
            nsolve = 0
            for size in (1, 2, 3):
                for comb in itertools.combinations(sel, size):
                    cs = set(comb)
                    if any(k <= cs for k in core_sets):
                        continue
                    nsolve += 1
                    if not sol.solve(assumptions=list(comb)):
                        core_sets.append(cs)
                        cores.append(sorted(units[s] for s in comb))
            mus = min_core(sol, sel)
            row["cores_le3"] = cores
            row["deletion_mus"] = sorted(units[s] for s in mus)
            row["t"] = round(time.time() - t0, 1)
            sizes = {}
            for cr in cores:
                sizes[len(cr)] = sizes.get(len(cr), 0) + 1
            pretty = " | ".join(
                "{" + ",".join(f"t{i}<b{j}" for (i, j) in cr) + "}"
                for cr in cores[:12])
            print(f"pair {{{x},{x+1}}} M={M}: UNSAT; minimal cores <=3: "
                  f"{sizes} ({nsolve} probes, {row['t']}s); del-MUS size "
                  f"{len(mus)}\n    {pretty}"
                  f"{' ...' if len(cores) > 12 else ''}", flush=True)
            out["rows"].append(row)
            sol.delete()
            json.dump(out, open(DATA, "w"), indent=1)
    print(f"-> {DATA}", flush=True)


if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    main()
