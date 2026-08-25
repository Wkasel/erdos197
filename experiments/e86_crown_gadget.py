"""Extract a minimal constraint-level gadget for the crown theorem at N=256.

Encoding as e85 (MODE=crown CAP=1): every clause family gets a selector;
solve under assumptions; shrink the selector core by deletion to a minimal
family set; then shrink the AP-triple families to individual triples.
Families:
  chan        - stage channeling + ladder consistency (keep always, structural)
  floor:none  - (floors are implicit)
  atk15:<k>   - triples (15, y, z) with y,z in block k  [15-attack]
  atk16:<k>   - triples (16, y, z) with y,z in block k
  atkS:<x>:<k>- triples (x, y, z), x other small (<=16), y,z in block k
  blk:<k>     - in-block triples of block k (both y,z,x in same block)
  x:<j>:<k>   - cross triples with x in block j (16<x), y,z in block k
Output: minimal family list, then minimal triple list within the union.
"""
import sys, time
import numpy as np
from pysat.solvers import Cadical195

def block(v):
    k = (v - 1).bit_length()
    if 2 ** k < v: k += 1
    return k

m = 4
CAP = 1
DMAX = 8
N = 4 ** m
V = [v for v in range(2, N + 1) if block(v) % 2 == 0]
n = len(V)
idx = {v: i for i, v in enumerate(V)}
Vs = set(V)
def cap_of(v):
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
sel = {}   # family -> selector var
def selector(fam):
    global var
    if fam not in sel:
        var += 1
        sel[fam] = var
    return sel[fam]
cl = []
def add(c, fam=None):
    if fam is None:
        cl.append(c)
    else:
        cl.append(c + [-selector(fam)])
for v in V:
    ks = sorted(L[v])
    for j in ks[1:]:
        add([-L[v][j], L[v][j - 1]])
def ge_lit(v, sigma):
    base = block(v) // 2
    if sigma <= base: return None
    j = sigma - base
    if j in L[v]: return L[v][j]
    return 0
for a in range(n):
    u = V[a]; ku = block(u) // 2; cu = cap_of(u)
    for b in range(a + 1, n):
        w = V[b]; kw = block(w) // 2; cw = cap_of(w)
        lou, hiu = ku, ku + cu
        low_, hiw = kw, kw + cw
        if hiu < low_: add([o(u, w)]); continue
        if hiw < lou: add([o(w, u)]); continue
        for sigma in range(max(lou, low_), min(hiu, hiw) + 2):
            gu = ge_lit(u, sigma); gw = ge_lit(w, sigma)
            if gu is not None and gw != 0:
                cls = [o(u, w)]
                if gu != 0: cls.append(gu)
                if gw is not None: cls.append(-gw)
                add(cls)
            if gw is not None and gu != 0:
                cls2 = [o(w, u)]
                if gw != 0: cls2.append(gw)
                if gu is not None: cls2.append(-gu)
                add(cls2)
trip_of_fam = {}
for y in V:
    d = 1
    while y + d <= N:
        x, z = y - d, y + d
        d += 1
        if x not in Vs or z not in Vs: continue
        ky, kz, kx = block(y), block(z), block(x)
        if x == 15: fam = f"atk15:{kz}"
        elif x == 16: fam = f"atk16:{kz}"
        elif x <= 16 and kx < kz: fam = f"atkS:{x}:{kz}"
        elif kx == kz: fam = f"blk:{kz}"
        else: fam = f"x:{kx}:{kz}"
        trip_of_fam.setdefault(fam, []).append((x, y, z))
        add([-o(x, y), -o(y, z)], fam)
        add([-o(z, y), -o(y, x)], fam)
print(f"families: {len(sel)}, clauses {len(cl)}", flush=True)
sol = Cadical195(bootstrap_with=cl)

def solve_with(fams):
    assum = [sel[f] for f in fams]
    while True:
        if not sol.solve(assumptions=assum):
            core = sol.get_core() or []
            return False, [f for f in fams if sel[f] in core]
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
            return True, None
        sol.append_formula(new)

t0 = time.time()
allf = list(sel)
r, core = solve_with(allf)
assert r is False, "expected UNSAT with all families"
work = list(core)
print(f"initial family core: {len(work)} ({time.time()-t0:.0f}s)", flush=True)
i = 0
while i < len(work):
    cand = work[:i] + work[i + 1:]
    r, c2 = solve_with(cand)
    if not r:
        work = [f for f in cand if f in (c2 or cand)]
        print(f"  drop {sorted(set(core)-set(work))[:3]}... -> {len(work)} "
              f"({time.time()-t0:.0f}s)", flush=True)
        core = work
    else:
        i += 1
print("MINIMAL FAMILY SET:", sorted(work), flush=True)
for f in sorted(work):
    if f in trip_of_fam:
        print(f"  {f}: {len(trip_of_fam[f])} triples", flush=True)
