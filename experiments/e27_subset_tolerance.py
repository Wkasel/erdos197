"""f(T, M): max size of a subset S' of block (M,2M] admitting an arrangement
with (a) no monotone 3-AP and (b) zone-forced pairs w.r.t. a T-element zone
subset Z' (maximized over choices of Z' from (M/4, M/2]).

CP-SAT: include-bools + positions; pairs constrained only if both included."""
import sys, time
from itertools import combinations
from ortools.sat.python import cp_model

def maxsubset(M, Zp, timeout=600):
    B = list(range(M + 1, 2 * M + 1))
    n = len(B)
    m = cp_model.CpModel()
    inc = {v: m.NewBoolVar(f"i{v}") for v in B}
    pos = {v: m.NewIntVar(0, n - 1, f"p{v}") for v in B}
    m.AddAllDifferent(list(pos.values()))
    Bs = set(B)
    for y in B:
        d = 1
        while y + d <= 2 * M:
            x, z = y - d, y + d
            if x in Bs and z in Bs:
                b1 = m.NewBoolVar(""); b2 = m.NewBoolVar("")
                m.Add(pos[x] < pos[y]).OnlyEnforceIf(b1)
                m.Add(pos[x] > pos[y]).OnlyEnforceIf(b1.Not())
                m.Add(pos[y] < pos[z]).OnlyEnforceIf(b2)
                m.Add(pos[y] > pos[z]).OnlyEnforceIf(b2.Not())
                # forbid monotone only if all three included
                m.AddBoolOr([b1, b2, inc[x].Not(), inc[y].Not(), inc[z].Not()])
                m.AddBoolOr([b1.Not(), b2.Not(), inc[x].Not(), inc[y].Not(), inc[z].Not()])
            d += 1
    for x in Zp:
        for y in B:
            z = 2 * y - x
            if z in Bs and z != y:
                # if y,z included: z before y
                m.Add(pos[z] < pos[y]).OnlyEnforceIf([inc[y], inc[z]])
    m.Maximize(sum(inc.values()))
    s = cp_model.CpSolver()
    s.parameters.num_search_workers = 4
    s.parameters.max_time_in_seconds = timeout
    st = s.Solve(m)
    val = int(s.ObjectiveValue()) if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else -1
    return val, st == cp_model.OPTIMAL

if __name__ == "__main__":
    M = int(sys.argv[1]) if len(sys.argv) > 1 else 32
    zone = list(range(M // 4 + 1, M // 2 + 1))
    # representative T-subsets: bottom, top, spread, plus a few randoms
    import random
    random.seed(7)
    for T in [1, 2, 3, 4]:
        cands = [tuple(zone[:T]), tuple(zone[-T:]),
                 tuple(zone[::max(1, len(zone) // T)][:T])]
        for _ in range(4):
            cands.append(tuple(sorted(random.sample(zone, T))))
        best = -1; bestz = None
        for Zp in set(cands):
            v, opt = maxsubset(M, Zp)
            if v > best:
                best, bestz = v, Zp
        print(f"M={M} T={T}: max|S'| = {best} of {M} ({best/M:.2f})  worst-zone {bestz}", flush=True)
