"""Ladder/crown rung checker v2: unary threshold channeling (compact).

L[v][j] <=> delta(v) >= j (unary ladder). For values u, w and stage threshold
sigma: (stage(u) < sigma) AND (stage(w) >= sigma) -> o(u,w), encoded as
  L[u][sigma-ku]  OR  NOT L[w][sigma-kw]  OR  o(u,w)
(one clause per threshold in the overlap window, both directions).
Args: m CAP [DMAX=8] [MODE=low|crown]
  low:   cap delta(v)<=CAP for v<=16
  crown: cap delta(v)<=CAP for v in {15,16}
UNSAT => every scheme at 4^m has max delta over the capped set >= CAP+1.
"""
import sys, time
import numpy as np
from pysat.solvers import Cadical195

def block(v):
    k = (v - 1).bit_length()
    if 2 ** k < v: k += 1
    return k

m, CAP = int(sys.argv[1]), int(sys.argv[2])
DMAX = int(sys.argv[3]) if len(sys.argv) > 3 else 8
MODE = sys.argv[4] if len(sys.argv) > 4 else "crown"
N = 4 ** m
V = [v for v in range(2, N + 1) if block(v) % 2 == 0]
n = len(V)
idx = {v: i for i, v in enumerate(V)}
Vs = set(V)

def cap_of(v):
    if MODE == "low":
        return CAP if v <= 16 else DMAX
    return CAP if v in (15, 16) else DMAX

var = 0
L = {}
for v in V:
    L[v] = {}
    for j in range(1, cap_of(v) + 1):
        var += 1
        L[v][j] = var
t = {}
for i in range(n):
    for j in range(i + 1, n):
        var += 1
        t[(i, j)] = var
def o(u, w):
    i, j = idx[u], idx[w]
    return t[(i, j)] if i < j else -t[(j, i)]

sol = Cadical195()
nc = 0
def add(c):
    global nc
    sol.add_clause(c)
    nc += 1

for v in V:
    ks = sorted(L[v])
    for j in ks[1:]:
        add([-L[v][j], L[v][j - 1]])

def ge_lit(v, sigma):
    """literal for stage(v) >= sigma; True->None(always), False->0."""
    base = block(v) // 2
    if sigma <= base: return None
    j = sigma - base
    if j in L[v]: return L[v][j]
    return 0  # impossible

t0 = time.time()
for a in range(n):
    u = V[a]; ku = block(u) // 2; cu = cap_of(u)
    for b in range(a + 1, n):
        w = V[b]; kw = block(w) // 2; cw = cap_of(w)
        lou, hiu = ku, ku + cu
        low_, hiw = kw, kw + cw
        if hiu < low_:
            add([o(u, w)]); continue
        if hiw < lou:
            add([o(w, u)]); continue
        # direction u before w when stage(u) < sigma <= stage(w)
        for sigma in range(max(lou, low_) , min(hiu, hiw) + 2):
            gu = ge_lit(u, sigma)   # stage(u) >= sigma: None=always, 0=never
            gw = ge_lit(w, sigma)
            # direction 1: stage(u) < sigma AND stage(w) >= sigma -> o(u,w)
            if gu is not None and gw != 0:
                cls = [o(u, w)]
                if gu != 0: cls.append(gu)
                if gw is not None: cls.append(-gw)
                add(cls)
            # direction 2: stage(w) < sigma AND stage(u) >= sigma -> o(w,u)
            if gw is not None and gu != 0:
                cls2 = [o(w, u)]
                if gw != 0: cls2.append(gw)
                if gu is not None: cls2.append(-gu)
                add(cls2)
ntr = 0
for y in V:
    d = 1
    while y + d <= N:
        x, z = y - d, y + d
        d += 1
        if x in Vs and z in Vs:
            add([-o(x, y), -o(y, z)])
            add([-o(z, y), -o(y, x)])
            ntr += 1
print(f"m={m} CAP={CAP} DMAX={DMAX} MODE={MODE}: n={n} clauses={nc} "
      f"triples={ntr} build={time.time()-t0:.0f}s", flush=True)
t0 = time.time()
rounds = 0
while True:
    if not sol.solve():
        print(f"RUNG2 m={m} CAP={CAP} {MODE}: UNSAT ({time.time()-t0:.0f}s, "
              f"{rounds} rounds)", flush=True)
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
        deltas = {v: max([0] + [j for j in L[v] if L[v][j] in model])
                  for v in V if v <= 16}
        print(f"RUNG2 m={m} CAP={CAP} {MODE}: SAT ({time.time()-t0:.0f}s) "
              f"low deltas={deltas}", flush=True)
        break
    for c in new:
        sol.add_clause(c)
    rounds += 1
    if rounds % 25 == 0:
        print(f"  round {rounds} ({time.time()-t0:.0f}s)", flush=True)
