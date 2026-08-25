"""Build a shallow human-readable refutation tree for OG(M) restricted to
the MUS triples. Recursive: at each node, test UNSAT-by-unit-propagation-ish
(solver with high conflict budget 0 → propagate only? approximate: budget
small); else pick the most-constrained undecided pair, branch on it.
Args: M [maxdepth]"""
import sys, time
import numpy as np
from pysat.solvers import Cadical195

M = int(sys.argv[1]) if len(sys.argv) > 1 else 40
MAXD = int(sys.argv[2]) if len(sys.argv) > 2 else 6
lo, hi = M, 2 * M
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
atk = []
for x in (15, 16):
    for j in range(1, x // 2 + 1):
        y = lo + j
        z = hi + 2 * j - x
        if lo < z <= hi:
            cl.append([o(z, y)])
            atk.append((z, y))
for y in V:
    d = 1
    while y + d <= hi:
        x, z = y - d, y + d
        d += 1
        if x > lo:
            cl.append([-o(x, y), -o(y, z)])
            cl.append([-o(z, y), -o(y, x)])
# full transitivity for the SUBSET of values appearing in the MUS + attacks
# (else UNSAT check needs lazy loop). Restrict to core values for speed.
core_vals = sorted(set(v for a in atk for v in a) |
                   set(range(lo + 1, hi + 1)))
# transitivity clauses among ALL values is n^3/6 = huge for M>40; M=40: 40^3/6=10666 OK
tr = 0
for a in range(n):
    for b in range(n):
        if a == b: continue
        for cc in range(n):
            if cc in (a, b): continue
            if a < b and b < cc:
                u, w, x2 = V[a], V[b], V[cc]
                # u<w & w<x2 -> u<x2  for all 6 orderings — add canonical form:
    # simpler: for each ordered triple i<j<k add 2 clauses (standard)
tr_added = 0
for i in range(n):
    for j in range(i + 1, n):
        for k in range(j + 1, n):
            a_, b_, c_ = var[(i, j)], var[(j, k)], var[(i, k)]
            cl.append([-a_, -b_, c_])
            cl.append([a_, b_, -c_])
            tr_added += 2
print(f"M={M}: clauses={len(cl)} (transitivity {tr_added})", flush=True)
sol = Cadical195(bootstrap_with=cl)

def status(assum):
    """returns 'UNSAT-easy' if refuted within tiny budget, 'UNSAT' if refuted
    at all, else 'SAT?'"""
    sol.conf_budget(50)
    r = sol.solve_limited(assumptions=assum)
    if r is False: return "UNSAT-easy"
    if sol.solve(assumptions=assum): return "SAT"
    return "UNSAT-hard"

# candidate decision pairs: among midzone values
mid = [v for v in V if lo + M // 4 <= v <= hi - M // 4]
import itertools
def pick_pair(assum):
    best = None
    # prefer AP-linked midzone pairs
    for (u, w) in itertools.combinations(mid, 2):
        lit = o(u, w)
        if lit in assum or -lit in assum: continue
        return (u, w)
    return None

lines = []
def go(assum, depth, label):
    st = status(assum)
    if st == "UNSAT-easy":
        lines.append("  " * depth + f"{label}: contradiction (unit-level)")
        return True
    if st == "UNSAT-hard":
        if depth >= MAXD:
            lines.append("  " * depth + f"{label}: UNSAT (deep)")
            return True
        p = pick_pair(assum)
        if p is None:
            lines.append("  " * depth + f"{label}: UNSAT (no split found)")
            return True
        u, w = p
        lines.append("  " * depth + f"{label}: split on {u} vs {w}")
        go(assum + [o(u, w)], depth + 1, f"[{u}<{w}]")
        go(assum + [-o(u, w)], depth + 1, f"[{w}<{u}]")
        return True
    lines.append("  " * depth + f"{label}: SAT?! (bug)")
    return False

t0 = time.time()
go([], 0, "root")
print("\n".join(lines[:200]), flush=True)
print(f"({time.time()-t0:.0f}s)", flush=True)
