"""pysat cross-check of e77: at N=256, delta(v)<=1 for v<=16, delta<=8 free
for the rest. Unary ladder encoding: L[v][j] <=> delta(v)>=j."""
import sys, time
import numpy as np
from pysat.solvers import Cadical195

def block(v):
    k = (v - 1).bit_length()
    if 2 ** k < v: k += 1
    return k

N = 256
DMAX = 8
V = [v for v in range(2, N + 1) if block(v) % 2 == 0]
n = len(V)
idx = {v: i for i, v in enumerate(V)}
Vs = set(V)
var = 0
L = {}
for v in V:
    cap = 1 if v <= 16 else DMAX
    L[v] = {}
    for j in range(1, cap + 1):
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
cl = []
for v in V:
    ks = sorted(L[v])
    for j in ks[1:]:
        cl.append([-L[v][j], L[v][j - 1]])
def stage_ge(v, s):
    # literal list meaning stage(v) >= s  (conjunction; here single lit or [])
    base = block(v) // 2
    if s <= base: return []          # always true
    j = s - base
    if j in L[v]: return [L[v][j]]
    return None                       # impossible
def stage_lt(v, s):
    r = stage_ge(v, s)
    if r == []: return None
    if r is None: return []
    return [-r[0]]
# channeling: for each pair u,w and threshold s: stage(u)<s AND stage(w)>=s -> o(u,w)
for a in range(n):
    u = V[a]
    for b in range(a + 1, n):
        w = V[b]
        bu, bw = block(u) // 2, block(w) // 2
        lo = min(bu, bw); hi = max(bu + (1 if u <= 16 else DMAX), bw + (1 if w <= 16 else DMAX)) + 1
        for s in range(lo + 1, hi + 1):
            gu = stage_ge(u, s); gw = stage_ge(w, s)
            # u<s, w>=s -> u before w
            if gu is not None and gw is not None:
                ante = []
                if gu != []: ante.append(gu[0])   # NOT(u>=s) needed: -gu
                # u < s  <=>  not stage_ge(u,s)
                if gu == []:
                    pass_u = None  # u always >= s: antecedent false
                else:
                    pass_u = -gu[0]
                if pass_u is not None:
                    ant = [pass_u] + gw
                    if gw == []:
                        cl.append([-pass_u * -1] and [ -(-pass_u), o(u,w)] if False else [ -pass_u*0+pass_u*0+o(u,w), -pass_u ] )
                    else:
                        cl.append([-pass_u if False else 0])
        # too fiddly — bail to direct pairwise level comparison below
cl = [c for c in cl if 0 not in c]
# Direct: enumerate delta levels per pair (like e60 ind()).
def ind(v, d):
    cap = 1 if v <= 16 else DMAX
    if d > cap: return None
    lits = []
    if d >= 1: lits.append(L[v][d])
    if d + 1 <= cap: lits.append(-L[v][d + 1])
    if d == 0 and 1 <= cap: lits = [-L[v][1]]
    return lits
cl2 = []
for v in V:
    ks = sorted(L[v])
    for j in ks[1:]:
        cl2.append([-L[v][j], L[v][j - 1]])
for a in range(n):
    u = V[a]; ku = block(u) // 2; capu = 1 if u <= 16 else DMAX
    for b in range(a + 1, n):
        w = V[b]; kw = block(w) // 2; capw = 1 if w <= 16 else DMAX
        for du in range(capu + 1):
            for dw in range(capw + 1):
                su, sw = ku + du, kw + dw
                if su == sw: continue
                lit = o(u, w) if su < sw else o(w, u)
                iu = ind(u, du); iw = ind(w, dw)
                cl2.append([-l for l in iu] + [-l for l in iw] + [lit])
for y in V:
    d = 1
    while y + d <= N:
        x, z = y - d, y + d
        d += 1
        if x in Vs and z in Vs:
            cl2.append([-o(x, y), -o(y, z)])
            cl2.append([-o(z, y), -o(y, x)])
sol = Cadical195(bootstrap_with=cl2)
t0 = time.time()
rounds = 0
while True:
    if not sol.solve():
        print(f"UNSAT ({time.time()-t0:.0f}s, {rounds} repair rounds) — CROSS-CHECK CONFIRMS e77", flush=True)
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
        ks2 = np.nonzero(B[i] & B[:, j])[0]
        new.append([-lit(i, int(ks2[0])), -lit(int(ks2[0]), j), lit(i, j)])
    if not new:
        print(f"SAT ({time.time()-t0:.0f}s) — CONTRADICTS e77!", flush=True)
        break
    sol.append_formula(new)
    rounds += 1
