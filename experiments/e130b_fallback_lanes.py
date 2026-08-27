"""e130b_fallback_lanes: do the fallback cores discovered by the e130
punctured-MUS anatomy fire lane-wide (as parametric mod-8 laws), like the
notes/49 catalogue lanes?  If yes, GAP-N3's anchor-freedom becomes a
finite catalogue statement: for every single puncture position v in the
dyadic class, some bounded core avoiding v fires at every scale.

Cores probed (units (i, j) = t_i < b_j, attacker i + 2j):

  x = 15 (pair {15,16}), discovered at M = 80 r0:
    F3   = {(7,4),(4,6),(2,7)}          the universal fallback (avoids
                                        b3,b5,t3,t5,t10,m0,m0+-1,t1)
    Q4   = {(5,5),(4,6),(3,6),(2,7)}    the b3/t10/m0/t1-puncture core
    G6   = {(11,2),(6,5),(5,5),(2,7)}   the b6-puncture core
  x = 11 (pair {11,12}), discovered at M = 80 r0:
    H5   = {(8,2),(6,3),(3,4),(0,6)}    the b5/t2-puncture core
    H4   = {(9,1),(7,2),(2,5),(0,6)}    the b4/t3-puncture core
    H1   = {(7,2),(3,4),(2,5),(0,6)}    the t1-puncture core
  plus controls C3 = {(5,5),(3,6),(10,3)} at x = 15 and
  A4a = {(0,6),(1,5),(2,5),(3,4)} at x = 11.

Sweep M = 16..168, exact firing sets, law fit mod 8.
Run: .venv/bin/python experiments/e130b_fallback_lanes.py
Artifacts: data/e130b_fallback_lanes.json
"""
import json
import time

from pysat.solvers import Cadical195

BASE = "/Users/will/Dev/personal/tasks/math/erdos197/data"

CORES = {
    (15, "C3"): [(5, 5), (3, 6), (10, 3)],
    (15, "F3"): [(7, 4), (4, 6), (2, 7)],
    (15, "Q4"): [(5, 5), (4, 6), (3, 6), (2, 7)],
    (15, "G6"): [(11, 2), (6, 5), (5, 5), (2, 7)],
    (11, "A4a"): [(0, 6), (1, 5), (2, 5), (3, 4)],
    (11, "H5"): [(8, 2), (6, 3), (3, 4), (0, 6)],
    (11, "H4"): [(9, 1), (7, 2), (2, 5), (0, 6)],
    (11, "H1"): [(7, 2), (3, 4), (2, 5), (0, 6)],
}

for (x, name), us in CORES.items():
    for (i, j) in us:
        assert i + 2 * j in (x, x + 1), (x, name, i, j)


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
                cl.append([-vpq, -var[(q, r)], var[(p, r)]])
                cl.append([vpq, var[(q, r)], -var[(p, r)]])
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


def main():
    sweep = list(range(16, 169))
    all_units = set()
    for us in CORES.values():
        all_units |= set(us)
    fires = {k: [] for k in CORES}
    t00 = time.time()
    for M in sweep:
        sol, sel = build_base(M, all_units)
        for key, us in CORES.items():
            if any(u not in sel for u in us):
                continue
            if not sol.solve(assumptions=[sel[u] for u in us]):
                fires[key].append(M)
        sol.delete()
        if M % 24 == 0:
            print(f"...M={M} ({time.time()-t00:.0f}s)", flush=True)
    out = {}
    for (x, name), ms in sorted(fires.items()):
        by_res = {}
        for m in ms:
            by_res.setdefault(m % 8, []).append(m)
        laws = {}
        for r, lst in sorted(by_res.items()):
            cand = [m for m in sweep if m % 8 == r and m >= min(lst)]
            laws[r] = ("all M == %d mod 8 from %d" % (r, min(lst))
                       if all(m in set(lst) for m in cand)
                       else f"partial: {lst}")
        out[f"{x}:{name}"] = {"units": CORES[(x, name)], "laws": laws}
        print(f"{name}(x={x}): {laws}", flush=True)
    json.dump(out, open(f"{BASE}/e130b_fallback_lanes.json", "w"), indent=1)
    print(f"-> {BASE}/e130b_fallback_lanes.json ({time.time()-t00:.0f}s)",
          flush=True)


if __name__ == "__main__":
    main()
