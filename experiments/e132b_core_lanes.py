"""e132b_core_lanes: are the fresh punctured-universe cores found by
e132 partS ({15,16} dyadic, catalogue-busting 2-subsets) LANE-stable —
i.e. does the M = 80 core (as a unit set) fire on the punctured
universe at every dyadic scale, even where the deletion-MUS happened to
return a different minimal core?  Probes AP + core-units on
(M, 2M] \\ P at M = 80..176 step 32 (dyadic class).

Run: .venv/bin/python experiments/e132b_core_lanes.py
Artifacts: data/e132b_core_lanes.json
"""
import json
import time

from pysat.solvers import Cadical195

BASE = "/Users/will/Dev/personal/tasks/math/erdos197/data"

with open(f"{BASE}/e132_spotchecks.json") as f:
    S = json.load(f)["partS"]["cores"]


def val(off, M):
    return (M + int(off[1:])) if off[0] == "b" else (2 * M - int(off[1:]))


def fires(M, P, core):
    vals = [v for v in range(M + 1, 2 * M + 1) if v not in P]
    idx = {v: i for i, v in enumerate(vals)}
    n = len(vals)
    var = {}
    c = 0
    for p in range(n):
        for q in range(p + 1, n):
            c += 1
            var[(p, q)] = c

    def o(u, w):
        p, q = idx[u], idx[w]
        return var[(p, q)] if p < q else -var[(q, p)]

    cl = []
    for y in vals:
        d = 1
        while y + d <= 2 * M and y - d > M:
            a, b = y - d, y + d
            if a in idx and b in idx:
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
    for (zo, yo) in core:
        cl.append([o(val(zo, M), val(yo, M))])
    sol = Cadical195(bootstrap_with=cl)
    r = not sol.solve()
    sol.delete()
    return r


if __name__ == "__main__":
    t0 = time.time()
    out = {}
    bad = []
    for key, byM in S.items():
        core = byM["M80"]
        P_off = key.split("+")
        row = {}
        for M in (80, 112, 144, 176):
            P = {val(o, M) for o in P_off}
            row[M] = "UNSAT" if fires(M, P, core) else "SAT"
            if row[M] == "SAT":
                bad.append((key, M))
        out[key] = {"core_M80": core, "fires": row}
        print(f"[b] {key}: core(M80)={core} -> "
              f"{[row[M] for M in (80, 112, 144, 176)]}", flush=True)
    with open(f"{BASE}/e132b_core_lanes.json", "w") as f:
        json.dump(out, f, indent=1)
    print(f"non-firing (buster, M): {bad or 'NONE'}  "
          f"({time.time()-t0:.0f}s)", flush=True)
