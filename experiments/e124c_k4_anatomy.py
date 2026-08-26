"""e124c_k4_anatomy: FRONT N2-OFF step 3a -- forced-relation anatomy of
the {11,12} dyadic size-4 cores at M = 0 mod 8, in search of the hand
schema (the C3 proof was discovered exactly this way: find what each
subcore forces, split on a phase, then close).

For each size-4 core K and each proper subset S of K (sizes 2, 3), and
optionally under a phase assumption t_a ~ m0: report every forced
relation u < v (i.e. AP + S + (v < u) UNSAT) over the focus values
{b_1..b_8, t_0..t_10, m0-2..m0+2}, restricted to pairs involving the
core's own endpoint values + centers (else the table drowns).

Run: .venv/bin/python experiments/e124c_k4_anatomy.py [M ...]
Output: stdout (record data/e124c_k4_anatomy.log) + json.
"""
import itertools
import json
import sys
import time

from pysat.solvers import Cadical195

BASE = "/Users/will/Dev/personal/tasks/math/erdos197/data"

CORES = {
    "A4a": [(0, 6), (1, 5), (2, 5), (3, 4)],
    "A4b": [(0, 6), (2, 5), (3, 4), (7, 2)],
    "A4c": [(0, 6), (2, 5), (7, 2), (9, 1)],
    "A4d": [(1, 5), (2, 5), (3, 4), (6, 3)],
}


def build(M, units):
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
    for (i, j) in sorted(units):
        z, y = 2 * M - i, M + j
        nv += 1
        sel[(i, j)] = nv
        cl.append([o(z, y), -nv])
    # phase selectors for every focus value w: w < m0 (lo) or m0 < w
    m0 = 3 * M // 2
    phase = {}
    for w in range(M + 1, 2 * M + 1):
        if w == m0:
            continue
        nv += 1
        phase[(w, "lo")] = nv
        cl.append([o(w, m0), -nv])
        nv += 1
        phase[(w, "hi")] = nv
        cl.append([o(m0, w), -nv])
    return Cadical195(bootstrap_with=cl), sel, phase, o


def anatomy(M, name, K, out):
    m0 = 3 * M // 2
    sol, sel, phase, o = build(M, K)
    # focus values: core endpoints + centers + neighbours
    vals = sorted({M + j for (_, j) in K} | {2 * M - i for (i, _) in K}
                  | {m0 - 2, m0 - 1, m0, m0 + 1, m0 + 2})
    names = {}
    for v in vals:
        if v == m0:
            names[v] = "m0"
        elif abs(v - m0) <= 2:
            names[v] = f"m0{v - m0:+d}"
        elif v <= m0:
            names[v] = f"b{v - M}"
        else:
            names[v] = f"t{2 * M - v}"

    def forced(S, extra, u, v):
        """AP + S + extra forces u < v?"""
        return not sol.solve(
            assumptions=[sel[w] for w in S] + extra + [o(v, u)])

    rows = []
    for sz in (len(K) - 1,):
        for S in itertools.combinations(K, sz):
            S = list(S)
            missing = [u for u in K if u not in S][0]
            base_forced = []
            for u, v in itertools.permutations(vals, 2):
                if u == m0 or v == m0:
                    continue
                if forced(S, [], u, v):
                    base_forced.append((names[u], names[v]))
            rows.append({"subset": S, "missing": missing,
                         "phase": None, "forced": base_forced})
            pretty = ",".join(f"t{i}<b{j}" for i, j in S)
            print(f"M={M} {name} minus t{missing[0]}<b{missing[1]}: "
                  f"forced = {sorted(base_forced)}", flush=True)
            # phase splits on each t-value of the core
            for (i, j) in K:
                tv = 2 * M - i
                for ph in ("lo", "hi"):
                    if not sol.solve(assumptions=[sel[w] for w in S]
                                     + [phase[(tv, ph)]]):
                        print(f"    phase t{i} {ph}: contradictory "
                              f"on its own", flush=True)
                        continue
                    extra = [phase[(tv, ph)]]
                    ff = []
                    for u, v in itertools.permutations(vals, 2):
                        if u == m0 or v == m0:
                            continue
                        if forced(S, extra, u, v):
                            ff.append((names[u], names[v]))
                    new = sorted(set(ff) - set(base_forced))
                    if new:
                        rows.append({"subset": S, "missing": missing,
                                     "phase": [i, ph], "forced_new": new})
                        print(f"    + phase t{i} {ph}: NEW forced = "
                              f"{new}", flush=True)
    sol.delete()
    out.append({"M": M, "core": name, "rows": rows})


def main():
    Ms = [int(a) for a in sys.argv[1:]] or [24, 32, 40]
    out = []
    t0 = time.time()
    for M in Ms:
        for name, K in CORES.items():
            anatomy(M, name, K, out)
            print(f"  ({time.time()-t0:.0f}s)", flush=True)
    json.dump(out, open(f"{BASE}/e124c_k4_anatomy.json", "w"), indent=1)
    print(f"-> {BASE}/e124c_k4_anatomy.json")


if __name__ == "__main__":
    main()
