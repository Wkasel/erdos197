"""CP-SAT engine for Erdős #197 systems: position variables + reified APs.

Modes:
  decide X          — pure-complete-X SAT?
  g X L             — minimize max position of values <= L (completion pressure)
"""
import sys, time
from ortools.sat.python import cp_model

def block(v):
    k = (v - 1).bit_length()
    if 2 ** k < v: k += 1
    return k

def sa(hi):
    return [v for v in range(2, hi + 1) if block(v) % 2 == 0]

def build_model(X):
    V = sa(X)
    n = len(V)
    m = cp_model.CpModel()
    pos = {v: m.NewIntVar(0, n - 1, f"p{v}") for v in V}
    m.AddAllDifferent(list(pos.values()))
    Vs = set(V)
    # For each ordered pair (a<b): if completion c=2b-a in set:
    #   NOT (pos a < pos b < pos c)   [increasing 3-AP a,b,c]
    # handled uniformly via triples: for each AP triple (x,y,z) in set:
    #   NOT (px<py<pz) and NOT (pz<py<px)
    for y in V:
        d = 1
        while y + d <= X:
            x, z = y - d, y + d
            if x in Vs and z in Vs:
                b1 = m.NewBoolVar("")
                b2 = m.NewBoolVar("")
                # b1 <=> px < py ; b2 <=> py < pz
                m.Add(pos[x] < pos[y]).OnlyEnforceIf(b1)
                m.Add(pos[x] > pos[y]).OnlyEnforceIf(b1.Not())
                m.Add(pos[y] < pos[z]).OnlyEnforceIf(b2)
                m.Add(pos[y] > pos[z]).OnlyEnforceIf(b2.Not())
                # forbid b1==b2 (monotone either way)
                m.AddBoolOr([b1, b2])
                m.AddBoolOr([b1.Not(), b2.Not()])
            d += 1
    # doom pairs where completion exists in set but triple isn't a "triple in
    # range" is already covered: completions c=2b-a with c in set form the AP
    # (a,b,c) with y=b, d=b-a: covered above only when all three in set — which
    # is exactly the condition. Completions outside the set are free. OK.
    return m, pos, V

def decide(X, workers=8, timeout=3600):
    m, pos, V = build_model(X)
    s = cp_model.CpSolver()
    s.parameters.num_search_workers = workers
    s.parameters.max_time_in_seconds = timeout
    st = s.Solve(m)
    return st, s, pos, V

def gmeasure(X, L, workers=8, timeout=3600):
    m, pos, V = build_model(X)
    small = [v for v in V if v <= L]
    gmax = m.NewIntVar(0, len(V) - 1, "gmax")
    m.AddMaxEquality(gmax, [pos[v] for v in small])
    m.Minimize(gmax)
    s = cp_model.CpSolver()
    s.parameters.num_search_workers = workers
    s.parameters.max_time_in_seconds = timeout
    st = s.Solve(m)
    return st, s, gmax

if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "decide":
        X = int(sys.argv[2])
        t0 = time.time()
        st, s, pos, V = decide(X)
        name = {cp_model.OPTIMAL: "SAT", cp_model.FEASIBLE: "SAT",
                cp_model.INFEASIBLE: "UNSAT"}.get(st, "UNKNOWN")
        print(f"pure-{X}: {name} ({time.time()-t0:.0f}s)", flush=True)
        if name == "SAT":
            import json
            order = sorted(V, key=lambda v: s.Value(pos[v]))
            json.dump(order, open(f"data/pure{X}_cpsat.json", "w"))
    elif mode == "g":
        X, L = int(sys.argv[2]), int(sys.argv[3])
        t0 = time.time()
        st, s, gmax = gmeasure(X, L)
        if st == cp_model.OPTIMAL:
            print(f"g_{X}({L}) = {s.Value(gmax)}  OPTIMAL ({time.time()-t0:.0f}s)", flush=True)
        elif st == cp_model.FEASIBLE:
            print(f"g_{X}({L}) <= {s.Value(gmax)}  (feasible, bound {s.BestObjectiveBound()}) ({time.time()-t0:.0f}s)", flush=True)
        else:
            print(f"g_{X}({L}): status {st} ({time.time()-t0:.0f}s)", flush=True)
