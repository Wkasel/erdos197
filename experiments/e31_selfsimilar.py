"""Pure-complete-X SAT + exact scale-invariance: u<w order iff 4u<4w order."""
import sys, time, json
from ortools.sat.python import cp_model

def block(v):
    k = (v - 1).bit_length()
    if 2 ** k < v: k += 1
    return k

def sa(hi):
    return [v for v in range(2, hi + 1) if block(v) % 2 == 0]

def run(X, timeout=7200):
    V = sa(X)
    n = len(V)
    m = cp_model.CpModel()
    pos = {v: m.NewIntVar(0, n - 1, f"p{v}") for v in V}
    m.AddAllDifferent(list(pos.values()))
    Vs = set(V)
    for y in V:
        d = 1
        while y + d <= X:
            x, z = y - d, y + d
            if x in Vs and z in Vs:
                b1 = m.NewBoolVar(""); b2 = m.NewBoolVar("")
                m.Add(pos[x] < pos[y]).OnlyEnforceIf(b1)
                m.Add(pos[x] > pos[y]).OnlyEnforceIf(b1.Not())
                m.Add(pos[y] < pos[z]).OnlyEnforceIf(b2)
                m.Add(pos[y] > pos[z]).OnlyEnforceIf(b2.Not())
                m.AddBoolOr([b1, b2]); m.AddBoolOr([b1.Not(), b2.Not()])
            d += 1
    # scale-invariance: for u,w in V with 4u,4w in V: (pos u < pos w) <=> (pos 4u < pos 4w)
    cnt = 0
    for u in V:
        if 4 * u > X: continue
        for w in V:
            if w <= u or 4 * w > X: continue
            b = m.NewBoolVar("")
            m.Add(pos[u] < pos[w]).OnlyEnforceIf(b)
            m.Add(pos[u] > pos[w]).OnlyEnforceIf(b.Not())
            m.Add(pos[4 * u] < pos[4 * w]).OnlyEnforceIf(b)
            m.Add(pos[4 * u] > pos[4 * w]).OnlyEnforceIf(b.Not())
            cnt += 1
    print(f"n={n}, invariance pairs: {cnt}", flush=True)
    s = cp_model.CpSolver()
    s.parameters.num_search_workers = 6
    s.parameters.max_time_in_seconds = timeout
    st = s.Solve(m)
    names = {cp_model.OPTIMAL: "SAT", cp_model.FEASIBLE: "SAT",
             cp_model.INFEASIBLE: "UNSAT"}
    print(f"self-similar pure-{X}: {names.get(st, st)}", flush=True)
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        order = sorted(V, key=lambda v: s.Value(pos[v]))
        json.dump(order, open(f"data/selfsim{X}.json", "w"))
        print("saved witness", flush=True)

if __name__ == "__main__":
    X = int(sys.argv[1]) if len(sys.argv) > 1 else 256
    t0 = time.time()
    run(X)
    print(f"({time.time()-t0:.0f}s)", flush=True)
