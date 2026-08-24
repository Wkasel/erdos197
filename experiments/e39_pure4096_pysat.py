"""pure-complete-4096 via pysat with phase hints from doubled pure-1024."""
import sys, time, json
import numpy as np
from pysat.solvers import Cadical195

def block(v):
    k = (v - 1).bit_length()
    if 2 ** k < v: k += 1
    return k

def sa(hi):
    return [v for v in range(2, hi + 1) if block(v) % 2 == 0]

X = 4096
V = sa(X)
idx = {v: i for i, v in enumerate(V)}
n = len(V)
W = json.load(open('data/pure1024.json'))
posW = {v: i for i, v in enumerate(W)}
# heuristic: order by (posW of v//4 if defined else large, v)
def hkey(v):
    p = v
    steps = 0
    while p not in posW and p >= 4:
        p //= 4
        steps += 1
    return (posW.get(p, len(W)), steps, v)
H = sorted(V, key=hkey)
posH = {v: i for i, v in enumerate(H)}
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
        print(f"PURE-4096 (pysat): UNSAT ({time.time()-t0:.0f}s) <-- DYADIC DEAD", flush=True)
        break
    model = s.get_model()
    posb = np.zeros(top + 1, dtype=bool)
    for l in model:
        if 0 < l <= top: posb[l] = True
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
        json.dump(seq, open("data/pure4096.json", "w"))
        print(f"PURE-4096 (pysat): SAT ({time.time()-t0:.0f}s)", flush=True)
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
