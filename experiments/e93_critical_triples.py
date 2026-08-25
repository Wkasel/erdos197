"""P3 support: order-independent backbone. A triple t is CRITICAL for OG(M)
if removing t alone from the full triple set makes the instance SAT; critical
triples lie in EVERY MUS (and every critical triple lies inside any single
MUS, so we only test members of the e90 MUS). Args: M [musfile]"""
import sys, re, time
from pathlib import Path
import numpy as np
from pysat.solvers import Cadical195

M = int(sys.argv[1])
DATA = Path(__file__).resolve().parent.parent / "data"
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
            return False
        model = set(l for l in sol.get_model() if l > 0)
        B = np.zeros((n, n), dtype=bool)
        for (i, j), lit in var.items():
            if lit in model: B[i, j] = True
            else: B[j, i] = True
        R2 = (B.astype(np.uint8) @ B.astype(np.uint8)) > 0
        miss = R2 & ~B & ~np.eye(n, dtype=bool) & B.T
        def lit_(p, q):
            return var[(p, q)] if p < q else -var[(q, p)]
        new = []
        ii, jj = np.nonzero(miss)
        for i, j in zip(ii[:30000], jj[:30000]):
            ks2 = np.nonzero(B[i] & B[:, j])[0]
            new.append([-lit_(i, int(ks2[0])), -lit_(int(ks2[0]), j),
                        lit_(i, j)])
        if not new:
            return True
        sol.append_formula(new)

# parse the e90 MUS
mus = []
grab = False
for line in (DATA / f"og_mus_{M}.log").read_text().splitlines():
    if line.startswith("MUS ("):
        grab = True
        continue
    if grab:
        m = re.match(r"\s+\((\d+), (\d+), (\d+)\)", line)
        if m:
            mus.append(tuple(int(g) for g in m.groups()))

t0 = time.time()
assert solve_with(trips) is False
crit = []
for t in mus:
    if solve_with([u for u in trips if u != t]):
        crit.append(t)
print(f"M={M}: {len(crit)} critical triples of {len(mus)} MUS members "
      f"({time.time()-t0:.0f}s)", flush=True)
for t in sorted(crit):
    print(f"  {t}")
