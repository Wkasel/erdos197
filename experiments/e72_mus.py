"""Deletion-based MUS over S2-assumptions: minimal set of values whose
window-1 caps are jointly contradictory at N=256."""
import sys, time
import numpy as np
from pysat.solvers import Cadical195
exec(open('experiments/e71_core.py').read().split("sol = Cadical195")[0])
sol = Cadical195(bootstrap_with=cl)

def solve_with(assum):
    while True:
        if not sol.solve(assumptions=assum):
            return False, [v for v in V if -S2[v] in (sol.get_core() or [])]
        model = set(l for l in sol.get_model() if l > 0)
        B = np.zeros((n, n), dtype=bool)
        for (i, j), lit in t.items():
            if lit in model: B[i, j] = True
            else: B[j, i] = True
        R2 = (B.astype(np.uint8) @ B.astype(np.uint8)) > 0
        miss = R2 & ~B & ~np.eye(n, dtype=bool) & B.T
        def lit(p, q):
            return t[(p, q)] if p < q else -t[(q, p)]
        new = []
        ii, jj = np.nonzero(miss)
        for i, j in zip(ii[:20000], jj[:20000]):
            ks = np.nonzero(B[i] & B[:, j])[0]
            new.append([-lit(i, int(ks[0])), -lit(int(ks[0]), j), lit(i, j)])
        if not new:
            return True, None
        sol.append_formula(new)

t0 = time.time()
r, core = solve_with([-S2[v] for v in V])
assert not r
work = list(core)
print(f"start core {len(work)} ({time.time()-t0:.0f}s)", flush=True)
i = 0
while i < len(work):
    cand = work[:i] + work[i+1:]
    r, c2 = solve_with([-S2[v] for v in cand])
    if not r:
        work = [v for v in cand if v in (c2 or cand)]
        print(f"  drop -> {len(work)} ({time.time()-t0:.0f}s)", flush=True)
    else:
        i += 1
print("MUS values:", sorted(work), flush=True)
