"""P3 support: protected-deletion test. For candidate parametric patterns,
instantiate at M and decide whether the concrete triple lies in SOME MUS of
OG(M): protect candidates during deletion-minimization of everything else;
if final set S is UNSAT and S-{t} is SAT then t is in a MUS. Args: M"""
import sys, time
from pathlib import Path
import numpy as np
from pysat.solvers import Cadical195

M = int(sys.argv[1])
lo, hi = M, 2 * M

# the 7 M≡0 (mod 4) common patterns as (p,q) with v=(p*M+q)/4
PATTERNS = [
    ((4, 4), (6, -12), (8, -28)),      # (M+1, (3M-6)/2, 2M-7)
    ((4, 20), (6, 4), (8, -12)),       # (M+5, (3M+2)/2, 2M-3)
    ((4, 28), (6, 4), (8, -20)),       # (M+7, (3M+2)/2, 2M-5)
    ((4, 68), (6, -4), (8, -76)),      # (M+17, (3M-2)/2, 2M-19)
    ((4, 76), (6, 28), (8, -20)),      # (M+19, (3M+14)/2, 2M-5)
    ((6, -4), (6, 12), (6, 28)),       # ((3M-2)/2, (3M+6)/2, (3M+14)/2)
    ((6, 4), (7, -16), (8, -36)),      # ((3M+2)/2, (7M-16)/4, 2M-9)
]
def inst(pat):
    vs = []
    for p, q in pat:
        num = p * M + q
        if num % 4:
            return None
        v = num // 4
        if not (lo < v <= hi):
            return None
        vs.append(v)
    return tuple(vs)

cands = []
for pat in PATTERNS:
    t = inst(pat)
    if t is None:
        print(f"  pattern {pat}: NOT INSTANTIABLE at M={M}")
    else:
        cands.append((pat, t))

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
        def lit_(p, q):
            return var[(p, q)] if p < q else -var[(q, p)]
        new = []
        ii, jj = np.nonzero(miss)
        for i, j in zip(ii[:30000], jj[:30000]):
            ks2 = np.nonzero(B[i] & B[:, j])[0]
            new.append([-lit_(i, int(ks2[0])), -lit_(int(ks2[0]), j),
                        lit_(i, j)])
        if not new:
            return True, None
        sol.append_formula(new)

t0 = time.time()
prot = set(t for _, t in cands)
work = list(trips)
r, core = solve_with(work)
assert r is False
work = [t for t in work if t in core or t in prot]
i = 0
while i < len(work):
    if work[i] in prot:
        i += 1
        continue
    cand2 = work[:i] + work[i + 1:]
    r, c2 = solve_with(cand2)
    if not r:
        work = [t for t in cand2 if t in (c2 or cand2) or t in prot]
    else:
        i += 1
print(f"M={M}: protected-min set {len(work)} ({time.time()-t0:.0f}s)",
      flush=True)
for pat, t in cands:
    r, _ = solve_with([u for u in work if u != t])
    verdict = "IN-SOME-MUS" if r else "inconclusive"
    print(f"  {pat} -> {t}: {verdict}", flush=True)
