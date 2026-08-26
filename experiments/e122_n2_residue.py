"""e122_n2_residue: FRONT N2 step 2 -- the complete core-catalogue sweep.

For EVERY M in the sweep (all residues, not just the 0-mod-16 column of
e121) and every pair {x, x+1}, x in 11..21 odd: enumerate ALL minimal
UNSAT cores of size <= 3 over the attack units (size <= 4 for pairs/scales
with no size-3 core, i.e. {11,12}), plus the full-rung verdict.  One
complete-encoding solver per M carries the selectors of every pair's
units; each probe is a solve-under-assumptions.

Post-analysis: per (pair, core-signature) the exact set of M where the
core fires, and the inferred residue law (smallest 2^r with UNSAT-set =
{M = s mod 2^r} up to threshold anomalies).  This is the generalization
of "AP + C3 UNSAT iff M = 0 mod 8" to the whole catalogue.

Run: .venv/bin/python experiments/e122_n2_residue.py
Output: data/e122_n2_residue.json
"""
import itertools
import json
import time

from pysat.solvers import Cadical195

BASE = "/Users/will/Dev/personal/tasks/math/erdos197/data"
PAIRS = [11, 13, 15, 17, 19, 21]
SWEEP = list(range(16, 145)) + [152, 160, 176, 192, 224, 256]


def build_base(M, all_units):
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
    sel = {}
    nv = c
    for (i, j) in sorted(all_units):
        z, y = 2 * M - i, M + j
        if not (M < z <= 2 * M and M < y <= 2 * M and z != y):
            continue
        nv += 1
        sel[(i, j)] = nv
        cl.append([o(z, y), -nv])
    return Cadical195(bootstrap_with=cl), sel


def enumerate_cores(sol, sel, units, max_size):
    """All minimal UNSAT cores of size <= max_size over `units`
    (list of (i,j) present in sel)."""
    cores = []
    core_sets = []
    for size in range(1, max_size + 1):
        for comb in itertools.combinations(units, size):
            cs = set(comb)
            if any(k <= cs for k in core_sets):
                continue
            if not sol.solve(assumptions=[sel[u] for u in comb]):
                core_sets.append(cs)
                cores.append(sorted(comb))
    return cores


def infer_law(unsat_ms, sweep):
    if not unsat_ms:
        return {"law": "never"}
    uset = set(unsat_ms)
    for r in (1, 2, 3, 4, 5):
        mod = 2 ** r
        S = sorted({m % mod for m in unsat_ms})
        cand = [m for m in sweep if m % mod in S]
        misses = [m for m in cand if m not in uset]
        if not misses:
            return {"law": f"M mod {mod} in {S}", "mod": mod, "S": S,
                    "from": min(unsat_ms), "anomalies": []}
        m0 = max(misses) + 1
        cand_above = [m for m in cand if m >= m0]
        if cand_above and all(m in uset for m in cand_above) \
                and len(cand_above) >= 5:
            spor = sorted(m for m in unsat_ms if m < m0)
            return {"law": f"M mod {mod} in {S}, M >= {m0}"
                           f" ({len(spor)} sporadic below)",
                    "mod": mod, "S": S, "from": m0, "anomalies": spor}
    return {"law": "irregular", "unsat_n": len(unsat_ms)}


def main():
    rung_units = {x: [(a - 2 * j, j) for a in (x, x + 1)
                      for j in range(1, a // 2 + 1)] for x in PAIRS}
    all_units = set()
    for x in PAIRS:
        all_units |= set(rung_units[x])

    per_m = []                    # raw per-M rows
    rung_unsat = {x: [] for x in PAIRS}
    core_ms = {}                  # (x, sig) -> [M...] minimal-core scales
    t00 = time.time()
    for M in SWEEP:
        t0 = time.time()
        sol, sel = build_base(M, all_units)
        row = {"M": M, "pairs": {}}
        for x in PAIRS:
            units = [u for u in rung_units[x] if u in sel]
            full_sat = sol.solve(assumptions=[sel[u] for u in units])
            if not full_sat:
                rung_unsat[x].append(M)
            cores = []
            if not full_sat:
                cores = enumerate_cores(sol, sel, units, 3)
                if not cores:
                    cores = enumerate_cores(sol, sel, units, 4)
                for cr in cores:
                    sig = tuple(map(tuple, cr))
                    core_ms.setdefault((x, sig), []).append(M)
            row["pairs"][str(x)] = {
                "full": "SAT" if full_sat else "UNSAT",
                "n_cores": len(cores),
                "cores": [[list(u) for u in cr] for cr in cores]}
        sol.delete()
        per_m.append(row)
        print(f"M={M}: " + " ".join(
            f"{x}:{row['pairs'][str(x)]['full'][0]}"
            f"{row['pairs'][str(x)]['n_cores']}" for x in PAIRS)
            + f"  ({time.time()-t0:.1f}s, total {time.time()-t00:.0f}s)",
            flush=True)
        if M % 16 == 0:
            json.dump({"per_m": per_m}, open(
                f"{BASE}/e122_n2_residue_partial.json", "w"))

    out = {"sweep": SWEEP, "rungs": {}, "cores": [], "per_m": per_m}
    for x in PAIRS:
        law = infer_law(rung_unsat[x], SWEEP)
        out["rungs"][str(x)] = {"unsat": rung_unsat[x], "law": law}
        sat_ms = [m for m in SWEEP if m not in rung_unsat[x]]
        print(f"FULL RUNG {{{x},{x+1}}}: UNSAT law: {law['law']}; "
              f"SAT at {sat_ms[:25]}{'...' if len(sat_ms) > 25 else ''}",
              flush=True)
    for (x, sig), ms in sorted(core_ms.items()):
        law = infer_law(ms, SWEEP)
        out["cores"].append({"x": x, "core": [list(u) for u in sig],
                             "ms": ms, "law": law})
        pretty = ",".join(f"t{i}<b{j}" for (i, j) in sig)
        print(f"  {{{x},{x+1}}} {{{pretty}}}: {law['law']} "
              f"[{len(ms)} scales]", flush=True)
    json.dump(out, open(f"{BASE}/e122_n2_residue.json", "w"), indent=1)
    print(f"-> {BASE}/e122_n2_residue.json", flush=True)


if __name__ == "__main__":
    main()
