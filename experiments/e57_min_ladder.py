"""Minimal-extras ladder: how much lookahead does level-nesting REQUIRE?

Global monotone-3AP-free order on V = S_A cap [1, 4^{d-1} X] (completions from
pairs <= top land < 2 top: odd block, free => pure AP triples inside V are the
exact doom set). Level i (comp_i = 4^i X, i = 0..d-1) gets a cutoff c_i: all of
complete_i := S_A cap [1, comp_i] must sit at positions < c_i. Prefix doom-
freeness is then automatic (any needed completion z of an ascending pair in the
prefix satisfies pos z < pos y < c_i). Extras at level i: E_i = c_i - n_i.

Any genuine global solution restricts to such a ladder with SOME finite extras,
so min sum E_i measures the intrinsic lookahead cost at each scale.

Args: X d [timeout_s]  -> prints per-level minima profile + witness dump.
"""
import sys, time, json
from ortools.sat.python import cp_model

def block(v):
    k = (v - 1).bit_length()
    if 2 ** k < v: k += 1
    return k

def sa(hi):
    return [v for v in range(2, hi + 1) if block(v) % 2 == 0]

def run(X, d, timeout=7200, workers=12):
    top = 4 ** (d - 1) * X
    V = sa(top)
    n = len(V)
    Vs = set(V)
    m = cp_model.CpModel()
    pos = {v: m.NewIntVar(0, n - 1, f"p{v}") for v in V}
    m.AddAllDifferent(list(pos.values()))
    for y in V:
        dd = 1
        while y + dd <= top:
            x, z = y - dd, y + dd
            if x in Vs and z in Vs:
                b1 = m.NewBoolVar("")
                b2 = m.NewBoolVar("")
                m.Add(pos[x] < pos[y]).OnlyEnforceIf(b1)
                m.Add(pos[x] > pos[y]).OnlyEnforceIf(b1.Not())
                m.Add(pos[y] < pos[z]).OnlyEnforceIf(b2)
                m.Add(pos[y] > pos[z]).OnlyEnforceIf(b2.Not())
                m.AddBoolOr([b1, b2])
                m.AddBoolOr([b1.Not(), b2.Not()])
            dd += 1
    extras = []
    for i in range(d - 1):
        comp = 4 ** i * X
        ni = sum(1 for v in V if v <= comp)
        c = m.NewIntVar(ni, n, f"c{i}")
        for v in V:
            if v <= comp:
                m.Add(pos[v] < c)
        e = m.NewIntVar(0, n - ni, f"e{i}")
        m.Add(e == c - ni)
        extras.append((comp, ni, e))
    m.Minimize(sum(e for _, _, e in extras))
    s = cp_model.CpSolver()
    s.parameters.num_search_workers = workers
    s.parameters.max_time_in_seconds = timeout
    st = s.Solve(m)
    name = {cp_model.OPTIMAL: "OPTIMAL", cp_model.FEASIBLE: "FEASIBLE",
            cp_model.INFEASIBLE: "INFEASIBLE"}.get(st, "UNKNOWN")
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        prof = [(comp, s.Value(e)) for comp, _, e in extras]
        print(f"MINLADDER X={X} d={d} top={top}: {name} total={s.ObjectiveValue():.0f} "
              f"bound={s.BestObjectiveBound():.0f} profile={prof}", flush=True)
        order = sorted(V, key=lambda v: s.Value(pos[v]))
        # which values are the extras at each level?
        dump = {"order": order, "profile": prof}
        for i, (comp, ni, e) in enumerate(extras):
            cut = ni + s.Value(e)
            dump[f"extras_{comp}"] = sorted(v for v in order[:cut] if v > comp)
        json.dump(dump, open(f"data/minladder_{X}_{d}.json", "w"))
    else:
        print(f"MINLADDER X={X} d={d}: {name}", flush=True)

if __name__ == "__main__":
    X, d = int(sys.argv[1]), int(sys.argv[2])
    to = int(sys.argv[3]) if len(sys.argv) > 3 else 7200
    t0 = time.time()
    run(X, d, timeout=to)
    print(f"({time.time()-t0:.0f}s)", flush=True)
