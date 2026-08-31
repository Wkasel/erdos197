# Spot-verify FRONT 85: from-scratch CP-SAT encoding (shares no code with e188).
# (a) reproduce cmin(12) = 12 and cmin(16) = 16;
# (b) Lemma BM1-VAC at the FRESH scale M = 36 (never machine-checked; record 16..32):
#     scoped query (impurity t <= floor(M/8)-1 = 3, Bm1 impurity t1 >= 1) must be UNSAT.
import sys
from ortools.sat.python import cp_model

def build(M, force_t1=None, tmax=None, minimize=True):
    md = cp_model.CpModel()
    Bm1 = list(range(M//2 + 1, M + 1))
    B0  = list(range(M + 1, 2*M + 1))
    B1  = list(range(2*M + 1, 4*M + 1))
    low = Bm1 + B0
    a = {v: md.NewBoolVar(f"a{v}") for v in low + B1}
    md.Add(sum(a[v] for v in Bm1) == M//4)
    md.Add(sum(a[v] for v in B0) == M//2)
    md.Add(sum(a[v] for v in B1) == M)
    # mu_dn = 0: no mono (w,u,y), w in Bm1, u in B0, y = 2u - w in B1
    for w in Bm1:
        for u in B0:
            y = 2*u - w
            if 2*M < y <= 4*M:
                md.AddBoolOr([a[w].Not(), a[u].Not(), a[y].Not()])
                md.AddBoolOr([a[w], a[u], a[y]])
    # low-impure: each team's low set carries both parities
    lo_odd = [a[v] for v in low if v % 2 == 1]
    lo_ev  = [a[v] for v in low if v % 2 == 0]
    md.Add(sum(lo_odd) >= 1); md.Add(sum(lo_odd) <= len(lo_odd) - 1)
    md.Add(sum(lo_ev) >= 1);  md.Add(sum(lo_ev) <= len(lo_ev) - 1)
    # canonical labeling: A owns the majority of low odds
    md.Add(2 * sum(lo_odd) >= len(lo_odd))
    if force_t1 is not None or tmax is not None:
        # t = number of low odds owned by B (canonical impurity); t1 = its Bm1 part... careful:
        # impurity: R = odds in B-low, D = evens in A-low; t = |R| = |D| (balance implies).
        tR = sum(1 - a[v] for v in low if v % 2 == 1)
        tD = sum(a[v] for v in low if v % 2 == 0)
        md.Add(tR == tD)  # sanity (implied by balance; harmless)
        if tmax is not None:
            md.Add(tR <= tmax)
        if force_t1 is not None:
            # t1 >= 1: some Bm1 impurity — an even Bm1 value in A OR an odd Bm1 value in B
            imp = []
            for v in Bm1:
                imp.append(a[v] if v % 2 == 0 else a[v].Not())
            md.AddBoolOr(imp)
    obj = None
    if minimize:
        # S = sum_z min(cA, cB), z = 2y - u in B2 = (4M, 8M], u in low, y in B1
        from collections import defaultdict
        reps = defaultdict(list)
        for u in low:
            for y in B1:
                z = 2*y - u
                if 4*M < z <= 8*M:
                    reps[z].append((u, y))
        terms = []
        for z, prs in reps.items():
            pAs, pBs = [], []
            for (u, y) in prs:
                pA = md.NewBoolVar(f"pA{z}_{u}_{y}"); pB = md.NewBoolVar(f"pB{z}_{u}_{y}")
                md.AddBoolAnd([a[u], a[y]]).OnlyEnforceIf(pA)
                md.AddBoolOr([a[u].Not(), a[y].Not()]).OnlyEnforceIf(pA.Not())
                md.AddBoolAnd([a[u].Not(), a[y].Not()]).OnlyEnforceIf(pB)
                md.AddBoolOr([a[u], a[y]]).OnlyEnforceIf(pB.Not())
                pAs.append(pA); pBs.append(pB)
            cA = md.NewIntVar(0, len(prs), f"cA{z}"); cB = md.NewIntVar(0, len(prs), f"cB{z}")
            md.Add(cA == sum(pAs)); md.Add(cB == sum(pBs))
            mz = md.NewIntVar(0, len(prs), f"m{z}")
            md.AddMinEquality(mz, [cA, cB])
            terms.append(mz)
        obj = sum(terms)
        md.Minimize(obj)
    return md

def run(md, name, timeout=1200):
    sv = cp_model.CpSolver()
    sv.parameters.max_time_in_seconds = timeout
    sv.parameters.num_search_workers = 8
    st = sv.Solve(md)
    print(name, sv.StatusName(st),
          ("obj=%d" % sv.ObjectiveValue()) if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) and md.HasObjective() else "",
          "%.1fs" % sv.WallTime())
    return sv.StatusName(st), (sv.ObjectiveValue() if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) and md.HasObjective() else None)

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which in ("all", "vac"):
        # BM1-VAC fresh scale M = 36: scoped (t <= 3, t1 >= 1) expect UNSAT
        st, _ = run(build(36, force_t1=True, tmax=3, minimize=False), "BM1-VAC scoped M=36 (expect UNSAT)")
        # control: unrestricted t, t1 >= 1 expect SAT (mixing feasible at big t)
        st2, _ = run(build(36, force_t1=True, tmax=None, minimize=False), "BM1 mixed unrestricted M=36 (expect SAT)")
    if which in ("all", "cmin12"):
        run(build(12), "cmin(12) (expect 12)")
    if which in ("all", "cmin16"):
        run(build(16), "cmin(16) (expect 16)")
