"""Class-split pipeline test: block (M,2M] minus class (1 mod 8), with full
zone placed — the 'bulk system'. And the reservoir system separately."""
import sys, time
from ortools.sat.python import cp_model

def zone_of(M):
    Z = set()
    lo, hi = M // 4, M // 2
    while lo >= 1:
        Z.update(range(lo + 1, hi + 1))
        hi //= 4
        lo //= 4
    return Z

def system(B, P, timeout=900):
    """arrange set B with pre-placed P: (a) + both-direction forced pairs."""
    B = sorted(B)
    n = len(B)
    m = cp_model.CpModel()
    pos = {v: m.NewIntVar(0, n - 1, f"p{v}") for v in B}
    m.AddAllDifferent(list(pos.values()))
    Bs = set(B)
    mx = B[-1]
    for y in B:
        d = 1
        while y + d <= mx:
            x, z = y - d, y + d
            if x in Bs and z in Bs:
                b1 = m.NewBoolVar(""); b2 = m.NewBoolVar("")
                m.Add(pos[x] < pos[y]).OnlyEnforceIf(b1)
                m.Add(pos[x] > pos[y]).OnlyEnforceIf(b1.Not())
                m.Add(pos[y] < pos[z]).OnlyEnforceIf(b2)
                m.Add(pos[y] > pos[z]).OnlyEnforceIf(b2.Not())
                m.AddBoolOr([b1, b2]); m.AddBoolOr([b1.Not(), b2.Not()])
            d += 1
    for x in P:
        for y in B:
            z = 2 * y - x
            if z in Bs and z != y:
                m.Add(pos[z] < pos[y])
    s = cp_model.CpSolver()
    s.parameters.num_search_workers = 6
    s.parameters.max_time_in_seconds = timeout
    return s.Solve(m)

if __name__ == "__main__":
    names = {cp_model.OPTIMAL: "SAT", cp_model.FEASIBLE: "SAT",
             cp_model.INFEASIBLE: "UNSAT"}
    for Mexp in [5, 6, 7, 8]:
        M = 2 ** Mexp
        blockv = list(range(M + 1, 2 * M + 1))
        bulk = [v for v in blockv if v % 8 != 1]
        Z = zone_of(M)
        t0 = time.time()
        st = system(bulk, Z)
        print(f"M={M} BULK (minus 1mod8) w/ full zone: {names.get(st,st)} ({time.time()-t0:.0f}s)", flush=True)
        # reservoir system: class 1 mod 8, with everything else placed
        res = [v for v in blockv if v % 8 == 1]
        P2 = set(Z) | set(bulk)
        t0 = time.time()
        st2 = system(res, P2)
        print(f"M={M} RESERVOIR (1mod8) w/ zone+bulk placed: {names.get(st2,st2)} ({time.time()-t0:.0f}s)", flush=True)
