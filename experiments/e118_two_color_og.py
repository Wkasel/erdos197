"""H3(a): 2-COLORED ORDER GADGET on the block (M, 2M] + attackers {15, 16}.

Every value v in the block and each attacker x in {15, 16} gets a color
variable c_v (True = team A, False = team B).  Each team T has its own
order matrix o_T on the block; a constraint activates only when all values
involved are colored T:
  (i)  in-block AP triple (x, y, z=2y-x): non-monotone in o_T if all three
       are colored T;
  (ii) attack: for attacker x colored T, j in [1, x//2], y = M+j,
       z = 2M+2j-x in block: if y, z also colored T then z BEFORE y in o_T
       (residue of x sitting at a finite position: x precedes cofinitely
       many block values, so x < y < z monotone unless z precedes y).
Completions crossing teams impose nothing on the completing team; the cost
is that the crossing value now lives in (and is constrained by) the other
team.  Coupling is purely through the coloring.

Modes (arg 2, default 'free'):
  allA      force every color = A (baseline; reproduces OG(M) verdict)
  free      all colors free: is the joint system SAT?  report witness shape
  split     c15 = A, c16 = B, block colors free, minimize donations
  mindon    c15 = c16 = A; minimize total donations #{v in block : B};
            then enumerate all optimal donation sets and classify them
  nosliver  c15 = c16 = A; bottom sliver (M, M+8] forced A; minimize
            donations elsewhere (is the sliver the only cheap repair?)
  minsliver c15 = c16 = A; donations unlimited; minimize donations INSIDE
            the bottom sliver only
  free4     like free but with attackers {15, 16, 31, 32} all colored
            (multi-crown: can pair-splits be chosen consistently?)
  mindon4   all four attackers forced A; minimize donations
Usage: e118_two_color_og.py M [mode] [maxb=16]
"""
import json
import sys
import time

import numpy as np
from pysat.card import ITotalizer
from pysat.solvers import Cadical195

M = int(sys.argv[1])
mode = sys.argv[2] if len(sys.argv) > 2 else "free"
maxb = int(sys.argv[3]) if len(sys.argv) > 3 else 16
ATK = [15, 16] + ([31, 32] if mode.endswith("4") else [])
assert M > max(ATK), "attackers must sit below the block"

V = list(range(M + 1, 2 * M + 1))
n = len(V)
idx = {v: i for i, v in enumerate(V)}
SLIVER = set(range(M + 1, M + 9))            # attacked bottoms y = M+j, j<=8
TOP = set(range(2 * M - 14, 2 * M + 1))      # attack sources z = 2M+2j-x

var = 0
col = {}                                     # color vars: True = A
for v in V + ATK:
    var += 1
    col[v] = var
ov = {"A": {}, "B": {}}                      # order vars per team, i<j pairs
for T in ("A", "B"):
    for i in range(n):
        for j in range(i + 1, n):
            var += 1
            ov[T][(i, j)] = var

def o(T, u, w):
    i, j = idx[u], idx[w]
    return ov[T][(i, j)] if i < j else -ov[T][(j, i)]

def notT(T, v):                              # literal "v is NOT in team T"
    return -col[v] if T == "A" else col[v]

cl = []
ntr = natk = 0
for y in V:                                  # (i) gated in-block AP triples
    d = 1
    while y + d <= 2 * M:
        x, z = y - d, y + d
        d += 1
        if x > M:
            for T in ("A", "B"):
                gate = [notT(T, x), notT(T, y), notT(T, z)]
                cl.append(gate + [-o(T, x, y), -o(T, y, z)])
                cl.append(gate + [-o(T, z, y), -o(T, y, x)])
            ntr += 1
for x in ATK:                                # (ii) gated attacks
    for j in range(1, x // 2 + 1):
        y, z = M + j, 2 * M + 2 * j - x
        if M < z <= 2 * M:
            for T in ("A", "B"):
                cl.append([notT(T, x), notT(T, y), notT(T, z), o(T, z, y)])
            natk += 1

# mode wiring -----------------------------------------------------------
don_lits = [-col[v] for v in V]              # literal true <=> v donated to B
minimize = None                              # list of literals to minimize
if mode == "allA":
    for v in V + ATK:
        cl.append([col[v]])
elif mode in ("free", "free4"):
    pass
elif mode == "mindon4":
    cl += [[col[x]] for x in ATK]
    minimize = don_lits
elif mode == "split":
    cl += [[col[15]], [-col[16]]]
    minimize = don_lits
elif mode == "mindon":
    cl += [[col[15]], [col[16]]]
    minimize = don_lits
elif mode == "nosliver":
    cl += [[col[15]], [col[16]]] + [[col[v]] for v in sorted(SLIVER)]
    minimize = don_lits
elif mode == "minsliver":
    cl += [[col[15]], [col[16]]]
    minimize = [-col[v] for v in sorted(SLIVER)]
else:
    raise SystemExit(f"unknown mode {mode}")

print(f"M={M} mode={mode}: n={n} triples={ntr} attacks={natk} "
      f"clauses={len(cl)}", flush=True)
sol = Cadical195(bootstrap_with=cl)
tot = None
if minimize is not None:
    tot = ITotalizer(lits=minimize, ubound=min(maxb, len(minimize)), top_id=var)
    var = tot.top_id
    sol.append_formula(tot.cnf.clauses)

def bound_assump(b):
    if tot is None:
        return []
    if b >= len(tot.rhs):
        return []
    return [-tot.rhs[b]]                     # sum(minimize) <= b

def solve_transitive(assumptions, extra_block=None):
    """Solve with lazy per-team transitivity.  Returns model set or None.
    UNSAT is conclusive (clauses only ever added)."""
    rounds = 0
    while True:
        ok = sol.solve(assumptions=assumptions)
        if not ok:
            return None
        model = set(l for l in sol.get_model() if l > 0)
        new = []
        for T in ("A", "B"):
            B = np.zeros((n, n), dtype=bool)
            for (i, j), lit in ov[T].items():
                if lit in model:
                    B[i, j] = True
                else:
                    B[j, i] = True
            R2 = (B.astype(np.uint8) @ B.astype(np.uint8)) > 0
            miss = R2 & ~B & ~np.eye(n, dtype=bool) & B.T
            def lit_of(p, q, T=T):
                return ov[T][(p, q)] if p < q else -ov[T][(q, p)]
            ii, jj = np.nonzero(miss)
            for i, j in zip(ii[:30000], jj[:30000]):
                k = int(np.nonzero(B[i] & B[:, j])[0][0])
                new.append([-lit_of(i, k), -lit_of(k, j), lit_of(i, j)])
        if not new:
            return model
        sol.append_formula(new)
        rounds += 1

def coloring_of(model):
    return {v: ("A" if col[v] in model else "B") for v in V + ATK}

def shape(c):
    donB = sorted(v for v in V if c[v] == "B")
    donA = sorted(v for v in V if c[v] == "A")
    maj = "A" if len(donA) >= len(donB) else "B"
    minority = donB if maj == "A" else donA
    return {
        "attackers": {x: c[x] for x in ATK},
        "c15": c[15], "c16": c[16], "majority": maj,
        "nA": len(donA), "nB": len(donB),
        "minority_values": minority,
        "minority_in_sliver": sorted(v for v in minority if v in SLIVER),
        "minority_in_top": sorted(v for v in minority if v in TOP),
    }

t0 = time.time()
out = {"M": M, "mode": mode}
if minimize is None:
    model = solve_transitive([])
    if model is None:
        print(f"M={M} {mode}: UNSAT ({time.time()-t0:.0f}s)", flush=True)
        out["verdict"] = "UNSAT"
    else:
        s = shape(coloring_of(model))
        print(f"M={M} {mode}: SAT ({time.time()-t0:.0f}s)  {s}", flush=True)
        out["verdict"] = "SAT"
        out["shape"] = s
else:
    minb = None
    for b in range(0, maxb + 1):
        model = solve_transitive(bound_assump(b))
        if model is not None:
            minb = b
            break
        print(f"  budget {b}: UNSAT ({time.time()-t0:.0f}s)", flush=True)
    out["min_budget"] = minb
    if minb is None:
        print(f"M={M} {mode}: UNSAT for all budgets <= {maxb} "
              f"({time.time()-t0:.0f}s)", flush=True)
    else:
        print(f"M={M} {mode}: min budget = {minb} ({time.time()-t0:.0f}s)",
              flush=True)
        # enumerate optimal solutions (distinct minimized donation sets)
        var2val = {col[v]: v for v in V + ATK}
        min_vals = [var2val[abs(l)] for l in minimize]
        sets, cap = [], 64
        while len(sets) < cap and time.time() - t0 < 900:
            if model is None:
                break
            curvals = sorted(v for v in min_vals if col[v] not in model)
            sets.append(curvals)
            if not curvals:
                break
            sol.add_clause([col[v] for v in curvals])  # some v un-donated
            model = solve_transitive(bound_assump(minb))
        cnt = {}
        for s_ in sets:
            for v in s_:
                cnt[v] = cnt.get(v, 0) + 1
        out["optimal_sets"] = sets
        out["value_frequency"] = {str(k): cnt[k] for k in sorted(cnt)}
        out["sets_touching_sliver"] = sum(1 for s_ in sets
                                          if any(v in SLIVER for v in s_))
        out["sets_touching_top"] = sum(1 for s_ in sets
                                       if any(v in TOP for v in s_))
        print(f"  {len(sets)} optimal sets; touching sliver: "
              f"{out['sets_touching_sliver']}, touching top: "
              f"{out['sets_touching_top']}", flush=True)
        for s_ in sets[:12]:
            tag = ["S" if v in SLIVER else "T" if v in TOP else "-"
                   for v in s_]
            print(f"    {s_} {''.join(tag)}", flush=True)

json.dump(out, open(f"data/e118_{M}_{mode}.json", "w"), indent=1)
print(f"wrote data/e118_{M}_{mode}.json total {time.time()-t0:.0f}s",
      flush=True)
