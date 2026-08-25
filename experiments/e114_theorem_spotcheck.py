"""e114_theorem_spotcheck: independent end-to-end SAT corroboration of the
notes/33 theorem STATEMENTS (not the proof schemas) at fresh scales that no
discovery loop touched.

  T1 (Layer 1): AP-free + A2 + A3 + (b3 < b5) is UNSAT at M = 0 mod 4.
  T2 (C3 core): AP-free + A1 + A2 + A3 is UNSAT at M = 0 mod 8.
  T3 (sharpness): AP-free + C3 is SAT at M = 4 mod 8.

Encoding: pairwise order variables, AP non-monotonicity as 2 clauses per
triple, lazy transitivity refinement (sound for UNSAT; SAT models are
closed under the refinement loop so SAT verdicts are genuine total orders).

Run: .venv/bin/python experiments/e114_theorem_spotcheck.py
Output: data/e114_spotcheck.json
"""
import json
import sys
import time

import numpy as np
from pysat.solvers import Cadical195

DATA = "/Users/will/Dev/personal/tasks/math/erdos197/data/e114_spotcheck.json"


def solve(M, extra_units):
    """AP-freeness on (M, 2M] + given precedence units. Returns 'UNSAT' or
    'SAT' (with the model verified to be a genuine AP-free total order)."""
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

    def o(u, w):
        i, j = idx[u], idx[w]
        return var[(i, j)] if i < j else -var[(j, i)]

    cl = [[o(u, w)] for (u, w) in extra_units]
    for y in V:
        d = 1
        while y + d <= hi:
            x, z = y - d, y + d
            d += 1
            if x > lo:
                cl.append([-o(x, y), -o(y, z)])
                cl.append([-o(z, y), -o(y, x)])
    sol = Cadical195(bootstrap_with=cl)
    t0 = time.time()
    while True:
        if not sol.solve():
            return "UNSAT", time.time() - t0
        model = set(l for l in sol.get_model() if l > 0)
        B = np.zeros((n, n), dtype=bool)
        for (i, j), lit in var.items():
            if lit in model:
                B[i, j] = True
            else:
                B[j, i] = True
        R2 = (B.astype(np.uint8) @ B.astype(np.uint8)) > 0
        miss = R2 & ~B & ~np.eye(n, dtype=bool) & B.T

        def lit2(p, q):
            return var[(p, q)] if p < q else -var[(q, p)]

        new = []
        ii, jj = np.nonzero(miss)
        for i, j in zip(ii[:30000], jj[:30000]):
            ks = np.nonzero(B[i] & B[:, j])[0]
            new.append([-lit2(i, int(ks[0])), -lit2(int(ks[0]), j),
                        lit2(i, j)])
        if not new:
            # verify the model is a genuine AP-free order with the units
            wins = B.sum(axis=1)
            pos = {V[i]: -int(wins[i]) for i in range(n)}
            for y in V:
                d = 1
                while y + d <= hi:
                    x, z = y - d, y + d
                    d += 1
                    if x > lo:
                        assert not (pos[x] < pos[y] < pos[z])
                        assert not (pos[z] < pos[y] < pos[x])
            for (u, w) in extra_units:
                assert pos[u] < pos[w]
            return "SAT", time.time() - t0
        sol.append_formula(new)


def main():
    out = {"T1_layer1": [], "T2_c3": [], "T3_sharp": [], "fail": []}

    def units(M, which):
        t3, t5, t10 = 2 * M - 3, 2 * M - 5, 2 * M - 10
        b3, b5, b6 = M + 3, M + 5, M + 6
        A1, A2, A3 = (t5, b5), (t3, b6), (t10, b3)
        if which == "L1":
            return [A2, A3, (b3, b5)]
        return [A1, A2, A3]

    for M in (148, 212, 264):           # fresh, = 0 mod 4
        v, dt = solve(M, units(M, "L1"))
        print(f"T1 M={M}: {v} ({dt:.0f}s)", flush=True)
        (out["T1_layer1"] if v == "UNSAT" else out["fail"]).append(M)
    for M in (264, 328):                # fresh, = 0 mod 8
        v, dt = solve(M, units(M, "C3"))
        print(f"T2 M={M}: {v} ({dt:.0f}s)", flush=True)
        (out["T2_c3"] if v == "UNSAT" else out["fail"]).append(M)
    for M in (268, 332):                # fresh, = 4 mod 8
        v, dt = solve(M, units(M, "C3"))
        print(f"T3 M={M}: {v} ({dt:.0f}s)", flush=True)
        (out["T3_sharp"] if v == "SAT" else out["fail"]).append(M)

    json.dump(out, open(DATA, "w"), indent=1)
    print("fail:", out["fail"])
    if out["fail"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
