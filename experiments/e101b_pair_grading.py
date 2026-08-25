"""e101b_pair_grading: supplement to e101 Part A -- do the OTHER axiom pairs
(A1+A2, A1+A3) have graded (2-adic) forced layers like A2+A3 does?

For each pair, probe all 15 six-value pair orders under AP + the two units,
at M covering all even classes mod 8 plus odd spot checks.
Output: data/e101b_pair_grading.json
"""
import itertools
import json
import time

import numpy as np
from pysat.solvers import Cadical195

DATA = "/Users/will/Dev/personal/tasks/math/erdos197/data/e101b_pair_grading.json"

AX = {"A1": ("t5", "b5"), "A2": ("t3", "b6"), "A3": ("t10", "b3")}


def run(M, cfg):
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

    def lit(i, j):
        return var[(i, j)] if i < j else -var[(j, i)]

    def o(u, w):
        return lit(idx[u], idx[w])

    ap = []
    for y in V:
        d = 1
        while y + d <= hi:
            x, z = y - d, y + d
            d += 1
            if x > lo:
                ap.append([-o(x, y), -o(y, z)])
                ap.append([-o(z, y), -o(y, x)])
    six = {"t5": 2 * M - 5, "t3": 2 * M - 3, "t10": 2 * M - 10,
           "b3": M + 3, "b5": M + 5, "b6": M + 6}
    units = [[o(six[AX[a][0]], six[AX[a][1]])] for a in cfg]
    sol = Cadical195(bootstrap_with=ap + units)

    def lazy(assum=()):
        while True:
            if not sol.solve(assumptions=list(assum)):
                return "UNSAT"
            model = set(l for l in sol.get_model() if l > 0)
            B = np.zeros((n, n), dtype=bool)
            for (i, j), vv in var.items():
                B[i, j] = vv in model
                B[j, i] = vv not in model
            R2 = (B.astype(np.uint8) @ B.astype(np.uint8)) > 0
            miss = R2 & ~B & ~np.eye(n, dtype=bool) & B.T
            ii, jj = np.nonzero(miss)
            if len(ii) == 0:
                return "SAT"
            new = []
            for i, j in zip(ii[:30000], jj[:30000]):
                ks = np.nonzero(B[i] & B[:, j])[0]
                new.append([-lit(i, int(ks[0])), -lit(int(ks[0]), j),
                            lit(i, j)])
            sol.append_formula(new)

    if lazy() == "UNSAT":
        sol.delete()
        return "UNSAT-BASE"
    forced = []
    for p, q in itertools.combinations(sorted(six), 2):
        u, w = six[p], six[q]
        if lazy([o(u, w)]) == "UNSAT":
            forced.append(f"{q}<{p}")
        elif lazy([o(w, u)]) == "UNSAT":
            forced.append(f"{p}<{q}")
    sol.delete()
    return sorted(forced)


def main():
    Ms = [40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60, 62, 64,
          41, 43, 45, 47]
    out = {}
    for cfg in (("A1", "A2"), ("A1", "A3")):
        key = "+".join(cfg)
        out[key] = {}
        for M in Ms:
            t0 = time.time()
            f = run(M, cfg)
            out[key][str(M)] = f
            units = {f"{AX[a][0]}<{AX[a][1]}" for a in cfg}
            extra = f if f == "UNSAT-BASE" else sorted(set(f) - units)
            print(f"[{key}] M={M} (mod8={M % 8}): extra={extra} "
                  f"({time.time()-t0:.1f}s)", flush=True)
    json.dump(out, open(DATA, "w"), indent=1)
    print(f"-> {DATA}", flush=True)


if __name__ == "__main__":
    main()
