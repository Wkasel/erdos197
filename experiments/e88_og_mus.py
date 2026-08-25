"""Triple-level MUS of the order gadget OG_K: minimal set of in-block AP
triples that, with the 15/16-attack pairs, is UNSAT. Args: K"""
import sys, time
import numpy as np
from pysat.solvers import Cadical195

K = int(sys.argv[1]) if len(sys.argv) > 1 else 8
lo, hi = 2 ** (K - 1), 2 ** K
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
cl = []
for x in (15, 16):
    for j in range(1, x // 2 + 1):
        y = lo + j
        z = hi + 2 * j - x
        if lo < z <= hi:
            cl.append([o(z, y)])
sel = {}
trips = []
nv = c
for y in V:
    d = 1
    while y + d <= hi:
        x, z = y - d, y + d
        d += 1
        if x > lo:
            nv += 1
            sel[(x, y, z)] = nv
            trips.append((x, y, z))
            cl.append([-o(x, y), -o(y, z), -nv])
            cl.append([-o(z, y), -o(y, x), -nv])
sol = Cadical195(bootstrap_with=cl)

def solve_with(ts):
    assum = [sel[t] for t in ts]
    while True:
        if not sol.solve(assumptions=assum):
            core = set(sol.get_core() or [])
            return False, [t for t in ts if sel[t] in core]
        model = set(l for l in sol.get_model() if l > 0)
        B = np.zeros((n, n), dtype=bool)
        for (i, j), lit in var.items():
            if lit in model: B[i, j] = True
            else: B[j, i] = True
        R2 = (B.astype(np.uint8) @ B.astype(np.uint8)) > 0
        miss = R2 & ~B & ~np.eye(n, dtype=bool) & B.T
        def lit(p, q):
            return var[(p, q)] if p < q else -var[(q, p)]
        new = []
        ii, jj = np.nonzero(miss)
        for i, j in zip(ii[:30000], jj[:30000]):
            ks2 = np.nonzero(B[i] & B[:, j])[0]
            new.append([-lit(i, int(ks2[0])), -lit(int(ks2[0]), j), lit(i, j)])
        if not new:
            return True, None
        sol.append_formula(new)

t0 = time.time()
r, core = solve_with(trips)
assert r is False
work = list(core)
print(f"K={K}: initial triple core {len(work)} ({time.time()-t0:.0f}s)", flush=True)
i = 0
while i < len(work):
    cand = work[:i] + work[i + 1:]
    r, c2 = solve_with(cand)
    if not r:
        work = [t for t in cand if t in (c2 or cand)]
    else:
        i += 1
    if i % 20 == 0:
        print(f"  ... {i}/{len(work)} ({time.time()-t0:.0f}s)", flush=True)
print(f"MUS ({len(work)} triples):", flush=True)
for t in sorted(work):
    print(f"  {t}  (offsets {t[0]-lo},{t[1]-lo},{t[2]-lo}; top-offsets "
          f"{hi-t[0]},{hi-t[1]},{hi-t[2]})", flush=True)
