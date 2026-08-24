"""Ladder rung checker (pysat): at N=4^m, cap delta(v)<=CAP for v<=16,
delta<=DMAX free for the rest. UNSAT proves L(m) >= CAP+1.
Args: m CAP [DMAX=8]"""
import sys, time
import numpy as np
from pysat.solvers import Cadical195

def block(v):
    k = (v - 1).bit_length()
    if 2 ** k < v: k += 1
    return k

m, CAP = int(sys.argv[1]), int(sys.argv[2])
DMAX = int(sys.argv[3]) if len(sys.argv) > 3 else 8
N = 4 ** m
V = [v for v in range(2, N + 1) if block(v) % 2 == 0]
n = len(V)
idx = {v: i for i, v in enumerate(V)}
Vs = set(V)
var = 0
L = {}
def cap_of(v): return CAP if v <= 16 else DMAX
for v in V:
    L[v] = {}
    for j in range(1, cap_of(v) + 1):
        var += 1
        L[v][j] = var
print("building order vars...", flush=True)
t = {}
for i in range(n):
    for j in range(i + 1, n):
        var += 1
        t[(i, j)] = var
def o(u, w):
    i, j = idx[u], idx[w]
    return t[(i, j)] if i < j else -t[(j, i)]
def ind(v, d):
    c = cap_of(v)
    if d == 0: return [-L[v][1]] if c >= 1 else []
    lits = [L[v][d]]
    if d + 1 <= c: lits.append(-L[v][d + 1])
    return lits
cl = []
for v in V:
    for j in sorted(L[v])[1:]:
        cl.append([-L[v][j], L[v][j - 1]])
for a in range(n):
    u = V[a]; ku = block(u) // 2; cu = cap_of(u)
    for b in range(a + 1, n):
        w = V[b]; kw = block(w) // 2; cw = cap_of(w)
        if kw + 0 - (ku + cu) > 0 and kw - ku > cu + 0 and (kw) - (ku + cu) > 0 and kw > ku + cu:
            # stage(u) <= ku+cu < kw <= stage(w): forced
            cl.append([o(u, w)]); continue
        for du in range(cu + 1):
            for dw in range(cw + 1):
                su, sw = ku + du, kw + dw
                if su == sw: continue
                lit = o(u, w) if su < sw else o(w, u)
                cl.append([-l for l in ind(u, du)] + [-l for l in ind(w, dw)] + [lit])
ntr = 0
for y in V:
    d = 1
    while y + d <= N:
        x, z = y - d, y + d
        d += 1
        if x in Vs and z in Vs:
            cl.append([-o(x, y), -o(y, z)])
            cl.append([-o(z, y), -o(y, x)])
            ntr += 1
print(f"m={m} CAP={CAP} DMAX={DMAX}: n={n} clauses={len(cl)} triples={ntr}", flush=True)
import resource
print(f"peak RSS MB: {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss//1024//1024}", flush=True)
sol = Cadical195(bootstrap_with=cl)
t0 = time.time()
rounds = 0
while True:
    if not sol.solve():
        print(f"RUNG m={m} CAP={CAP}: UNSAT ({time.time()-t0:.0f}s, {rounds} rounds) => L({m}) >= {CAP+1}", flush=True)
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
    for i, j in zip(ii[:30000], jj[:30000]):
        ks2 = np.nonzero(B[i] & B[:, j])[0]
        new.append([-lit(i, int(ks2[0])), -lit(int(ks2[0]), j), lit(i, j)])
    if not new:
        deltas = {v: max([0] + [j for j in L[v] if L[v][j] in model]) for v in V if v <= 16}
        print(f"RUNG m={m} CAP={CAP}: SAT ({time.time()-t0:.0f}s) low deltas={deltas}", flush=True)
        import json
        alld = {v: max([0] + [j for j in L[v] if L[v][j] in model]) for v in V}
        wins = B.sum(axis=1)
        order = [V[i] for i in sorted(range(n), key=lambda i: -int(wins[i]))]
        json.dump({"delta": {str(v): int(d) for v, d in alld.items()},
                   "order": order},
                  open(f"data/rung_{m}_{CAP}_{DMAX}.json", "w"))
        break
    sol.append_formula(new)
    rounds += 1
    if rounds % 25 == 0:
        print(f"  round {rounds} ({time.time()-t0:.0f}s)", flush=True)
