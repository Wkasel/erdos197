"""Grow-based witness: find A subset of F-t with A SAT, A+t UNSAT
(decisive positive certificate for t in some MUS). Random greedy grows.
Args: M patidx nrounds"""
import sys, random
from pysat.solvers import Cadical195
import numpy as np

M = int(sys.argv[1]); w = int(sys.argv[2]); NR = int(sys.argv[3])
lo, hi = M, 2 * M
PATTERNS = [
    ((4, 4), (6, -12), (8, -28)),
    ((4, 20), (6, 4), (8, -12)),
    ((4, 28), (6, 4), (8, -20)),
    ((4, 68), (6, -4), (8, -76)),
    ((4, 76), (6, 28), (8, -20)),
    ((6, -4), (6, 12), (6, 28)),
    ((6, 4), (7, -16), (8, -36)),
]
pat = PATTERNS[w]
t = tuple((p * M + q) // 4 for p, q in pat)
V = list(range(lo + 1, hi + 1)); n = len(V)
idx = {v: i for i, v in enumerate(V)}
var = {}; c = 0
for i in range(n):
    for j in range(i + 1, n):
        c += 1; var[(i, j)] = c
def o(u, w2):
    i, j = idx[u], idx[w2]
    return var[(i, j)] if i < j else -var[(j, i)]
cl = []
for x in (15, 16):
    for j in range(1, x // 2 + 1):
        y = lo + j; z = hi + 2 * j - x
        if lo < z <= hi: cl.append([o(z, y)])
sel = {}; trips = []; nv = c
for y in V:
    d = 1
    while y + d <= hi:
        x, z = y - d, y + d; d += 1
        if x > lo:
            nv += 1; sel[(x, y, z)] = nv; trips.append((x, y, z))
            cl.append([-o(x, y), -o(y, z), -nv])
            cl.append([-o(z, y), -o(y, x), -nv])
sol = Cadical195(bootstrap_with=cl)
def solve_with(ts):
    assum = [sel[u] for u in ts]
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
            new.append([-lit_(i, int(ks2[0])), -lit_(int(ks2[0]), j), lit_(i, j)])
        if not new:
            return True
        sol.append_formula(new)
rng = random.Random(4242 + w * 1000 + M)
others = [u for u in trips if u != t]
found = False
for r in range(NR):
    order = others[:]; rng.shuffle(order)
    A = []
    for u in order:
        if solve_with(A + [u]):
            A.append(u)
    # A maximal satisfiable in this order; check A+t
    if not solve_with(A + [t]):
        print(f"M={M} pat{w} -> {t}: WITNESS FOUND round {r} (|A|={len(A)}) => IN-SOME-MUS", flush=True)
        found = True; break
if not found:
    print(f"M={M} pat{w} -> {t}: no witness in {NR} grow rounds", flush=True)
