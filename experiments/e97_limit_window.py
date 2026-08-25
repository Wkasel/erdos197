"""Finite windows of the compactness limit of OG-C3.

Limit structure: bands q in dyadic rationals of [1,2], denominator <= 2^r.
Element (q, a) represents value qM + a (integer for M divisible by 2^r).
Window: band 1 has a in [1, R]; band 2 has a in [-R, 0]; interior bands
a in [-R, R]. AP triples: (q1,a1),(q2,a2),(q3,a3) with q1+q3 = 2*q2 and
a1+a3 = 2*a2 (all in window) — this is EXACTLY the AP structure among these
values in (M, 2M] for all sufficiently large M (band separation kills all
other APs; boundary: for large M no cross-band coincidences).
Precedences (C3): t5 < b5, t3 < b6, t10 < b3, i.e.
(2, -5) before (1, 5); (2, -3) before (1, 6); (2, -10) before (1, 3).
If some window is UNSAT: OG-C3(M) infeasible for all sufficiently large
M ≡ 0 mod 2^r  ==>  with the machine sweep, all dyadic block lengths
==> S_A not 3-permutable. Args: r R
"""
import sys, time
from fractions import Fraction
import numpy as np
from pysat.solvers import Cadical195

r = int(sys.argv[1]) if len(sys.argv) > 1 else 1
R = int(sys.argv[2]) if len(sys.argv) > 2 else 20

bands = sorted(set(Fraction(p, 2 ** r) for p in range(2 ** r, 2 ** (r + 1) + 1)))
els = []
for q in bands:
    if q == 1:
        rng = range(1, R + 1)
    elif q == 2:
        rng = range(-R, 1)
    else:
        rng = range(-R, R + 1)
    for a in rng:
        els.append((q, a))
idx = {e: i for i, e in enumerate(els)}
n = len(els)
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
# C3 precedences
prec = [((Fraction(2), -5), (Fraction(1), 5)),
        ((Fraction(2), -3), (Fraction(1), 6)),
        ((Fraction(2), -10), (Fraction(1), 3))]
for (u, w) in prec:
    assert u in idx and w in idx, "window too small for precedences"
    cl.append([o(u, w)])
# AP triples
ntr = 0
es = set(els)
for i in range(n):
    q1, a1 = els[i]
    for j in range(n):
        if j == i: continue
        q2, a2 = els[j]
        q3, a3 = 2 * q2 - q1, 2 * a2 - a1
        # (q1,a1) < (q2,a2) < (q3,a3) in VALUE order requires q,a lex-ish:
        # value = qM + a: for large M the value order is (q, then a).
        if (q3, a3) not in es: continue
        v1, v2, v3 = (q1, a1), (q2, a2), (q3, a3)
        # ensure v1 < v2 < v3 by (q,a) lex (value order for large M)
        if not ((q1, a1) < (q2, a2) < (q3, a3)): continue
        cl.append([-o(v1, v2), -o(v2, v3)])
        cl.append([-o(v3, v2), -o(v2, v1)])
        ntr += 1
print(f"r={r} R={R}: n={n} triples={ntr}", flush=True)
sol = Cadical195(bootstrap_with=cl)
t0 = time.time()
rounds = 0
while True:
    if not sol.solve():
        print(f"LIMIT WINDOW r={r} R={R}: UNSAT ({time.time()-t0:.0f}s, "
              f"{rounds} rounds)  <<< THEOREM-GRADE", flush=True)
        break
    model = set(l for l in sol.get_model() if l > 0)
    B = np.zeros((n, n), dtype=bool)
    for (i, j), lit in var.items():
        if lit in model: B[i, j] = True
        else: B[j, i] = True
    R2 = (B.astype(np.uint8) @ B.astype(np.uint8)) > 0
    miss = R2 & ~B & ~np.eye(n, dtype=bool) & B.T
    def lit(p, q_):
        return var[(p, q_)] if p < q_ else -var[(q_, p)]
    new = []
    ii, jj = np.nonzero(miss)
    for i, j in zip(ii[:30000], jj[:30000]):
        ks2 = np.nonzero(B[i] & B[:, j])[0]
        new.append([-lit(i, int(ks2[0])), -lit(int(ks2[0]), j), lit(i, j)])
    if not new:
        print(f"LIMIT WINDOW r={r} R={R}: SAT ({time.time()-t0:.0f}s)", flush=True)
        break
    sol.append_formula(new)
    rounds += 1
    if rounds % 50 == 0:
        print(f"  round {rounds} ({time.time()-t0:.0f}s)", flush=True)
