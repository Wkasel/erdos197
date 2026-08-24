"""Domino-gadget extraction: which values MUST use displacement 2 at N=256?
e60 encoding (window 2); assume -S2[v] for all v (=> window 1): UNSAT;
the returned core lists the S2-assumptions that matter."""
import sys, time
import numpy as np
from pysat.solvers import Cadical195

def block(v):
    k = (v - 1).bit_length()
    if 2 ** k < v: k += 1
    return k

m = int(sys.argv[1]) if len(sys.argv) > 1 else 4
N = 4 ** m
V = [v for v in range(2, N + 1) if block(v) % 2 == 0]
n = len(V)
idx = {v: i for i, v in enumerate(V)}
Vs = set(V)
var = 0
S1, S2 = {}, {}
for v in V:
    S1[v] = var + 1; S2[v] = var + 2; var += 2
t = {}
for i in range(n):
    for j in range(i + 1, n):
        var += 1
        t[(i, j)] = var
def o(u, w):
    i, j = idx[u], idx[w]
    return t[(i, j)] if i < j else -t[(j, i)]
cl = []
for v in V:
    cl.append([-S2[v], S1[v]])
def ind(v, d):
    if d == 0: return [-S1[v]]
    if d == 1: return [S1[v], -S2[v]]
    return [S2[v]]
for a in range(n):
    u = V[a]; ku = block(u) // 2
    for b in range(a + 1, n):
        w = V[b]; kw = block(w) // 2
        if kw - ku > 2:
            cl.append([o(u, w)]); continue
        for du in range(3):
            for dw in range(3):
                su, sw = ku + du, kw + dw
                if su == sw: continue
                lit = o(u, w) if su < sw else o(w, u)
                cl.append([-l for l in ind(u, du)] + [-l for l in ind(w, dw)] + [lit])
for y in V:
    d = 1
    while y + d <= N:
        x, z = y - d, y + d
        d += 1
        if x in Vs and z in Vs:
            cl.append([-o(x, y), -o(y, z)])
            cl.append([-o(z, y), -o(y, x)])
sol = Cadical195(bootstrap_with=cl)
assum = [-S2[v] for v in V]
t0 = time.time()
while True:
    r = sol.solve(assumptions=assum)
    if not r:
        core = sol.get_core()
        vals = sorted(v for v in V if -S2[v] in core)
        print(f"UNSAT ({time.time()-t0:.0f}s); core size {len(vals)}")
        print("domino values (must reach displacement 2):", vals)
        break
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
        k = int(ks[0])
        new.append([-lit(i, k), -lit(k, j), lit(i, j)])
    if not new:
        print("SAT?! window-1 feasible — contradiction with CP-SAT"); break
    sol.append_formula(new)

# --- deletion-based MUS shrink (run when invoked with 'shrink') ---
