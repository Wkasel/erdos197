"""Pure order gadget OG_t: block (2^{K-1}, 2^K], K = 2t. Constraints:
(i) every AP triple inside the block non-monotone;
(ii) for x in {15, 16}, j in [1, x/2]: z = 2^K + 2j - x  BEFORE  y = 2^{K-1}+j.
Infeasible for all K  ==>  crowns diverge  ==>  S_A not permutable.
Args: K [drop15] [drop16]  (drop flags test necessity of each attack family)
"""
import sys, time
import numpy as np
from pysat.solvers import Cadical195

K = int(sys.argv[1])
use15 = "drop15" not in sys.argv
use16 = "drop16" not in sys.argv
if K >= 30:   # interpret as literal interval length M: interval (M, 2M]
    lo, hi = K, 2 * K
else:
    lo, hi = 2 ** (K - 1), 2 ** K
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
natk = 0
for x in ([15] if use15 else []) + ([16] if use16 else []):
    for j in range(1, x // 2 + 1):
        y = lo + j
        z = hi + 2 * j - x
        if lo < z <= hi:
            cl.append([o(z, y)])
            natk += 1
ntr = 0
for y in V:
    d = 1
    while y + d <= hi:
        x, z = y - d, y + d
        d += 1
        if x > lo:
            cl.append([-o(x, y), -o(y, z)])
            cl.append([-o(z, y), -o(y, x)])
            ntr += 1
print(f"K={K}: n={n} attacks={natk} triples={ntr}", flush=True)
sol = Cadical195(bootstrap_with=cl)
t0 = time.time()
rounds = 0
while True:
    if not sol.solve():
        print(f"OG K={K} (15:{use15} 16:{use16}): UNSAT ({time.time()-t0:.0f}s, "
              f"{rounds} rounds)", flush=True)
        break
    model = set(l for l in sol.get_model() if l > 0)
    B = np.zeros((n, n), dtype=bool)
    for (i, j), lit in var.items():
        if lit in model: B[i, j] = True
        else: B[j, i] = True
    R2 = (B.astype(np.uint8) @ B.astype(np.uint8)) > 0
    miss = R2 & ~B & ~np.eye(n, dtype=bool) & B.T
    def lit(p, q):
        return var[(p, q)] if p < q else -var[(q, p)]
    new = []
    ii, jj = np.nonzero(miss)
    for i, j in zip(ii[:30000], jj[:30000]):
        ks2 = np.nonzero(B[i] & B[:, j])[0]
        new.append([-lit(i, int(ks2[0])), -lit(int(ks2[0]), j), lit(i, j)])
    if not new:
        wins = B.sum(axis=1)
        order = [V[i] for i in sorted(range(n), key=lambda i: -int(wins[i]))]
        print(f"OG K={K} (15:{use15} 16:{use16}): SAT ({time.time()-t0:.0f}s)",
              flush=True)
        import json
        json.dump(order, open(f"data/og_{K}.json", "w"))
        break
    sol.append_formula(new)
    rounds += 1
    if rounds % 50 == 0:
        print(f"  round {rounds} ({time.time()-t0:.0f}s)", flush=True)
