"""e98b: which anatomy features of OG-C3 SAT witnesses are FORCED?

Companion to e98_c3_witness.py.  For each SAT M, tests by UNSAT whether the
patterns observed in the e98 witnesses hold in EVERY witness:

  T1 (M any): can some value v ~= 0 mod 4 lie strictly between t10 and b3
      in T?  (e98 witnesses at M = 1 mod 4 put ONLY 0-mod-4 values there.)
  T2 (M any): can some value v = 0 mod 4 lie strictly between t3 and b6
      in T?  (e98 witnesses at M = 4 mod 8 exclude ALL 0-mod-4 values.)
  T3 (M any): can some value lie strictly between t5 and b5?
  T4 (M any): can some value lie strictly between t10 and b3?
      (e98 witnesses at M = 4 mod 8 place both pairs adjacent.)

"exists v in S strictly between x and y" is encoded with one aux var per
v in S:  a_v -> x<v,  a_v -> v<y,  plus clause OR a_v.  UNSAT means the
negation is a law of every witness.  Results appended to
data/c3_witness_anatomy.json under "_forced_tests".
"""
import json
import os
import time

import numpy as np
from pysat.solvers import Cadical195

MS = [41, 42, 43, 44, 45, 46, 47, 49, 50, 52, 60, 68, 76, 84, 92, 100]


def build(M):
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

    six = {"b3": M + 3, "b5": M + 5, "b6": M + 6,
           "t3": 2 * M - 3, "t5": 2 * M - 5, "t10": 2 * M - 10}
    cl = [[o(six["t5"], six["b5"])],
          [o(six["t3"], six["b6"])],
          [o(six["t10"], six["b3"])]]
    for y in V:
        d = 1
        while y + d <= hi:
            x, z = y - d, y + d
            d += 1
            if x > lo:
                cl.append([-o(x, y), -o(y, z)])
                cl.append([-o(z, y), -o(y, x)])
    return V, n, var, o, cl, six, c


def solve_lazy(sol, var, n):
    while True:
        if not sol.solve():
            return False
        model = set(l for l in sol.get_model() if l > 0)
        B = np.zeros((n, n), dtype=bool)
        for (i, j), lit in var.items():
            if lit in model:
                B[i, j] = True
            else:
                B[j, i] = True
        R2 = (B.astype(np.uint8) @ B.astype(np.uint8)) > 0
        miss = R2 & ~B & ~np.eye(n, dtype=bool) & B.T
        ii, jj = np.nonzero(miss)
        if len(ii) == 0:
            return True

        def lit_(p, q):
            return var[(p, q)] if p < q else -var[(q, p)]

        new = []
        for i, j in zip(ii[:30000], jj[:30000]):
            ks = np.nonzero(B[i] & B[:, j])[0]
            new.append([-lit_(i, int(ks[0])), -lit_(int(ks[0]), j),
                        lit_(i, j)])
        sol.append_formula(new)


def exists_between(M, xkey, ykey, pred):
    """SAT iff some witness has v with pred(v) strictly between x and y."""
    V, n, var, o, cl, six, top = build(M)
    x, y = six[xkey], six[ykey]
    sixvals = set(six.values())
    S = [v for v in V if pred(v) and v != x and v != y and v not in sixvals]
    aux = {}
    for v in S:
        top += 1
        aux[v] = top
        cl.append([-top, o(x, v)])
        cl.append([-top, o(v, y)])
    cl.append([aux[v] for v in S])
    sol = Cadical195(bootstrap_with=cl)
    res = solve_lazy(sol, var, n)
    sol.delete()
    return res


TESTS = [
    ("T1_nonmult4_between_t10_b3", "t10", "b3", lambda v: v % 4 != 0),
    ("T2_mult4_between_t3_b6", "t3", "b6", lambda v: v % 4 == 0),
    ("T3_any_between_t5_b5", "t5", "b5", lambda v: True),
    ("T4_any_between_t10_b3", "t10", "b3", lambda v: True),
]


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(root, "data", "c3_witness_anatomy.json")
    out = json.load(open(path))
    res = {}
    for M in MS:
        t0 = time.time()
        row = {}
        for name, xk, yk, pred in TESTS:
            sat = exists_between(M, xk, yk, pred)
            row[name] = "possible" if sat else "FORCED-EMPTY"
        res[str(M)] = {"M_mod8": M % 8, **row}
        print(f"M={M} (mod8={M % 8}): "
              + " ".join(f"{k}={v}" for k, v in row.items())
              + f" ({time.time()-t0:.0f}s)", flush=True)
    out["_forced_tests"] = {
        "legend": {name: f"can some v with [{name}] lie strictly between "
                         f"{xk} and {yk}?  FORCED-EMPTY = no witness has one"
                   for name, xk, yk, _ in TESTS},
        "results": res,
    }
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
    print(f"updated {path}", flush=True)


if __name__ == "__main__":
    main()
