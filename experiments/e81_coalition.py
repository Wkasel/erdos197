"""Deletion-based minimal cap-coalition: smallest set C of values <= 16 such
that capping delta(v)<=1 for v in C (rest free <=8) is INFEASIBLE at N=256."""
import sys, time
from ortools.sat.python import cp_model

def block(v):
    k = (v - 1).bit_length()
    if 2 ** k < v: k += 1
    return k

def solve(N, capped, timeout=1800):
    V = [v for v in range(2, N + 1) if block(v) % 2 == 0]
    n = len(V)
    Vs = set(V)
    md = cp_model.CpModel()
    pos = {v: md.NewIntVar(0, n - 1, f"p{v}") for v in V}
    md.AddAllDifferent(list(pos.values()))
    delta = {v: md.NewIntVar(0, 1 if v in capped else 8, f"d{v}") for v in V}
    stage = {}
    for v in V:
        s = md.NewIntVar(0, 100, f"s{v}")
        md.Add(s == block(v) // 2 + delta[v])
        stage[v] = s
    for a in range(n):
        u = V[a]
        for b in range(a + 1, n):
            w = V[b]
            if abs(block(w) // 2 - block(u) // 2) > 8:
                md.Add(pos[u] < pos[w]); continue
            b1 = md.NewBoolVar("")
            md.Add(stage[u] < stage[w]).OnlyEnforceIf(b1)
            md.Add(stage[u] >= stage[w]).OnlyEnforceIf(b1.Not())
            md.Add(pos[u] < pos[w]).OnlyEnforceIf(b1)
            b2 = md.NewBoolVar("")
            md.Add(stage[w] < stage[u]).OnlyEnforceIf(b2)
            md.Add(stage[w] >= stage[u]).OnlyEnforceIf(b2.Not())
            md.Add(pos[w] < pos[u]).OnlyEnforceIf(b2)
    for y in V:
        d = 1
        while y + d <= N:
            x, z = y - d, y + d
            d += 1
            if x in Vs and z in Vs:
                c1 = md.NewBoolVar(""); c2 = md.NewBoolVar("")
                md.Add(pos[x] < pos[y]).OnlyEnforceIf(c1)
                md.Add(pos[x] > pos[y]).OnlyEnforceIf(c1.Not())
                md.Add(pos[y] < pos[z]).OnlyEnforceIf(c2)
                md.Add(pos[y] > pos[z]).OnlyEnforceIf(c2.Not())
                md.AddBoolOr([c1, c2]); md.AddBoolOr([c1.Not(), c2.Not()])
    s = cp_model.CpSolver()
    s.parameters.num_search_workers = 12
    s.parameters.max_time_in_seconds = timeout
    st = s.Solve(md)
    return {cp_model.OPTIMAL: "SAT", cp_model.FEASIBLE: "SAT",
            cp_model.INFEASIBLE: "UNSAT"}.get(st, "UNKNOWN")

N = 256
low = [v for v in [3, 4, 9, 10, 11, 12, 13, 14, 15, 16]]
C = list(low)
t0 = time.time()
for v in list(low):
    if v not in C: continue
    trial = [u for u in C if u != v]
    r = solve(N, set(trial))
    print(f"drop {v}: {r} ({time.time()-t0:.0f}s)", flush=True)
    if r == "UNSAT":
        C = trial
    elif r == "UNKNOWN":
        print("  (timeout — keeping)", flush=True)
print("minimal coalition:", C, flush=True)
