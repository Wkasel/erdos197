"""selfsim-4096 witness-fixed, with solver phases seeded from a pumped guess."""
import sys, time, json
import numpy as np
from pysat.solvers import Cadical195
from collections import defaultdict

def block(v):
    k = (v - 1).bit_length()
    if 2 ** k < v: k += 1
    return k

def sa(hi):
    return [v for v in range(2, hi + 1) if block(v) % 2 == 0]

X = 4096
W = json.load(open('data/selfsim1024.json'))
posW = {v: i for i, v in enumerate(W)}
Wset = set(W)
V = sa(X)
idx = {v: i for i, v in enumerate(V)}
n = len(V)

# ---- heuristic pumped order (band-structure guess) ----
# skeleton: v = 4u, u in W  -> key (posW[u], 0, v)
# new: anchor a(v) = 4*(v//4) if in skeleton else nearest skeleton by value;
#      band offset by tower class (v mod 4, (v//4) mod 8) from measured bands.
key = {}
for v in V:
    if v % 4 == 0 and v // 4 in Wset:
        key[v] = (posW[v // 4] * 1000, 0, v)
# band bases measured at 1024 (approximate; only ordering matters)
BASE = {}
Wskel = sorted([v for v in W if v % 4 == 0 and v // 4 in Wset], key=lambda v: posW[v])
skelpos = [posW[s] for s in Wskel]
import bisect
def slotW(v):
    return bisect.bisect_left(skelpos, posW[v])
bands = defaultdict(list)
for v in W:
    if v % 4 == 0 and v // 4 in Wset: continue
    u4 = 4 * (v // 4)
    if u4 in set(Wskel):
        bands[(v % 4, (v // 4) % 8)].append(slotW(v) - slotW(u4))
for k2, vals in bands.items():
    BASE[k2] = int(np.median(vals))
for v in V:
    if v in key: continue
    u4 = 4 * (v // 4)
    b = BASE.get((v % 4, (v // 4) % 8), 0)
    if u4 in key:
        key[v] = (key[u4][0] + b * 1000 // max(1, len(Wskel)) * 100 + 500, 1, v)
    else:
        # anchor by nearest smaller skeleton value
        key[v] = (posW.get(v // 4, len(W)) * 1000 + 500, 2, v)
H = sorted(V, key=lambda v: key[v])
posH = {v: i for i, v in enumerate(H)}
print("heuristic order built", flush=True)

# ---- SAT ----
top = 0
t = {}
for i in range(n):
    for j in range(i + 1, n):
        top += 1
        t[(i, j)] = top
def before(u, w):
    i, j = idx[u], idx[w]
    return t[(i, j)] if i < j else -t[(j, i)]
cl = []
Vs = set(V)
for y in V:
    d = 1
    while y + d <= X:
        a, c = y - d, y + d
        if a in Vs and c in Vs:
            cl.append([-before(a, y), -before(y, c)])
            cl.append([-before(c, y), -before(y, a)])
        d += 1
for a in V:
    for b in V:
        if b <= a: continue
        c = 2 * b - a
        if c in Vs:
            cl.append([-before(a, b), before(c, b)])
        d2 = 2 * a - b
        if d2 >= 1 and d2 in Vs:
            cl.append([-before(b, a), before(d2, a)])
for u in V:
    if 4 * u > X or 4 * u not in Vs: continue
    for w in V:
        if w <= u or 4 * w > X or 4 * w not in Vs: continue
        cl.append([-before(u, w), before(4 * u, 4 * w)])
        cl.append([before(u, w), -before(4 * u, 4 * w)])
for i in range(len(W)):
    for j in range(i + 1, len(W)):
        cl.append([before(W[i], W[j])])
print(f"n={n} clauses={len(cl)}", flush=True)
s = Cadical195(bootstrap_with=cl)
phases = []
for (i, j), var in t.items():
    u, w = V[i], V[j]
    phases.append(var if posH[u] < posH[w] else -var)
s.set_phases(phases)
t0 = time.time()
rounds = 0
while True:
    rounds += 1
    if not s.solve():
        print(f"selfsim-4096 hinted: UNSAT ({time.time()-t0:.0f}s)", flush=True)
        break
    model = s.get_model()
    posb = np.zeros(top + 1, dtype=bool)
    for l in model:
        if 0 < l <= top:
            posb[l] = True
    B = np.zeros((n, n), dtype=bool)
    for (i, j), var in t.items():
        if posb[var]: B[i, j] = True
        else: B[j, i] = True
    wins = B.sum(axis=1)
    order = np.argsort(-wins, kind='stable')
    R = B[np.ix_(order, order)]
    iu = np.triu_indices(n, 1)
    bad_idx = np.nonzero(~R[iu])[0]
    if len(bad_idx) == 0:
        seq = [V[i] for i in order]
        json.dump(seq, open("data/selfsim4096.json", "w"))
        print(f"selfsim-4096 hinted: SAT ({time.time()-t0:.0f}s)", flush=True)
        break
    added = 0
    for bi in bad_idx[:80000]:
        a_, b_ = iu[0][bi], iu[1][bi]
        i, j = int(order[a_]), int(order[b_])
        ks = np.nonzero(B[i] & B[:, j])[0]
        if len(ks):
            k = int(ks[0])
            s.add_clause([-before(V[i], V[k]), -before(V[k], V[j]),
                          before(V[i], V[j])])
            added += 1
            if added > 60000: break
    if rounds % 10 == 0:
        print(f"round {rounds}: {len(bad_idx)} viol ({time.time()-t0:.0f}s)", flush=True)
