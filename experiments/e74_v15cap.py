"""CP-SAT joint stage+order with MINIMAL total delay.

pos[v] all-different; delta[v] in [0,2]; stage[v] = block/2 + delta[v];
stage[u] < stage[w]  ==>  pos[u] < pos[w]  (stages are consecutive fibers);
AP triples non-monotone in pos. Minimize sum delta (then the delayed sets are
the intrinsic lookahead classes). Args: m [timeout]  (N = 4^m).
"""
import sys, time, json
from ortools.sat.python import cp_model

def block(v):
    k = (v - 1).bit_length()
    if 2 ** k < v: k += 1
    return k

def main(m, timeout=3600):
    N = 4 ** m
    V = [v for v in range(2, N + 1) if block(v) % 2 == 0]
    n = len(V)
    Vs = set(V)
    md = cp_model.CpModel()
    pos = {v: md.NewIntVar(0, n - 1, f"p{v}") for v in V}
    md.AddAllDifferent(list(pos.values()))
    delta = {v: md.NewIntVar(0, 2 if v == 15 else 8, f"d{v}") for v in V}
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
                md.Add(pos[u] < pos[w])
                continue
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
                c1 = md.NewBoolVar("")
                c2 = md.NewBoolVar("")
                md.Add(pos[x] < pos[y]).OnlyEnforceIf(c1)
                md.Add(pos[x] > pos[y]).OnlyEnforceIf(c1.Not())
                md.Add(pos[y] < pos[z]).OnlyEnforceIf(c2)
                md.Add(pos[y] > pos[z]).OnlyEnforceIf(c2.Not())
                md.AddBoolOr([c1, c2])
                md.AddBoolOr([c1.Not(), c2.Not()])
    md.Minimize(sum(delta.values()))
    s = cp_model.CpSolver()
    s.parameters.num_search_workers = 12
    s.parameters.max_time_in_seconds = timeout
    t0 = time.time()
    st = s.Solve(md)
    name = {cp_model.OPTIMAL: "OPTIMAL", cp_model.FEASIBLE: "FEASIBLE",
            cp_model.INFEASIBLE: "INFEASIBLE"}.get(st, "UNKNOWN")
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        tot = int(s.ObjectiveValue())
        print(f"MINSTAGE N=4^{m}: {name} total-delay={tot} "
              f"bound={s.BestObjectiveBound():.0f} ({time.time()-t0:.0f}s)",
              flush=True)
        byblock = {}
        for v in V:
            dv = s.Value(delta[v])
            if dv: byblock.setdefault(block(v), []).append((v, dv))
        for k in sorted(byblock):
            print(f"  block {k}: {byblock[k]}", flush=True)
        order = sorted(V, key=lambda v: s.Value(pos[v]))
        json.dump({"order": order,
                   "delta": {str(v): int(s.Value(delta[v])) for v in V}},
                  open(f"data/minstage_{m}.json", "w"))
    else:
        print(f"MINSTAGE N=4^{m}: {name} ({time.time()-t0:.0f}s)", flush=True)

if __name__ == "__main__":
    m = int(sys.argv[1])
    to = int(sys.argv[2]) if len(sys.argv) > 2 else 3600
    main(m, to)
