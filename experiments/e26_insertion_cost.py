"""Insertion cost: fix a pure-X arrangement sigma (relative order of old
values); solve pure-4X extending sigma; minimize the number of NEW values
placed before the last OLD value. Also report how many new values precede the
last SMALL (<=64) value."""
import sys, time, json
from ortools.sat.python import cp_model

def block(v):
    k = (v - 1).bit_length()
    if 2 ** k < v: k += 1
    return k

def sa(hi):
    return [v for v in range(2, hi + 1) if block(v) % 2 == 0]

def run(X4, sigma):
    V = sa(X4)
    n = len(V)
    old = sigma
    oldset = set(old)
    new = [v for v in V if v not in oldset]
    m = cp_model.CpModel()
    pos = {v: m.NewIntVar(0, n - 1, f"p{v}") for v in V}
    m.AddAllDifferent(list(pos.values()))
    Vs = set(V)
    for y in V:
        d = 1
        while y + d <= X4:
            x, z = y - d, y + d
            if x in Vs and z in Vs:
                b1 = m.NewBoolVar(""); b2 = m.NewBoolVar("")
                m.Add(pos[x] < pos[y]).OnlyEnforceIf(b1)
                m.Add(pos[x] > pos[y]).OnlyEnforceIf(b1.Not())
                m.Add(pos[y] < pos[z]).OnlyEnforceIf(b2)
                m.Add(pos[y] > pos[z]).OnlyEnforceIf(b2.Not())
                m.AddBoolOr([b1, b2]); m.AddBoolOr([b1.Not(), b2.Not()])
            d += 1
    # fix old relative order
    for i in range(len(old) - 1):
        m.Add(pos[old[i]] < pos[old[i + 1]])
    last_old = old[-1]
    # objective: count new values before last_old
    bs = []
    for v in new:
        b = m.NewBoolVar("")
        m.Add(pos[v] < pos[last_old]).OnlyEnforceIf(b)
        m.Add(pos[v] > pos[last_old]).OnlyEnforceIf(b.Not())
        bs.append(b)
    m.Minimize(sum(bs))
    s = cp_model.CpSolver()
    s.parameters.num_search_workers = 6
    s.parameters.max_time_in_seconds = 7200
    st = s.Solve(m)
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        cost = sum(s.Value(b) for b in bs)
        tag = "OPTIMAL" if st == cp_model.OPTIMAL else f"feasible (bound {s.BestObjectiveBound()})"
        order = sorted(V, key=lambda v: s.Value(pos[v]))
        inserted = [v for v in order if v in set(new)][:cost] if cost else []
        # positions of inserted new values relative to old smalls
        print(f"insertion cost = {cost}  [{tag}]", flush=True)
        if cost:
            firstold_small_pos = max(s.Value(pos[v]) for v in old if v <= 64)
            npre = sum(1 for v in new if s.Value(pos[v]) < firstold_small_pos)
            print(f"new-values before small-completion: {npre}", flush=True)
            ins = [v for v in new if s.Value(pos[v]) < s.Value(pos[last_old])]
            print(f"inserted values: {sorted(ins)[:40]}", flush=True)
        json.dump(order, open('data/ext1024_mincost.json', 'w'))
    else:
        print(f"status {st} (INFEASIBLE => this sigma is a dead branch)", flush=True)

if __name__ == "__main__":
    sigma = json.load(open('data/pure256_cpsat.json'))
    t0 = time.time()
    run(1024, sigma)
    print(f"({time.time()-t0:.0f}s)", flush=True)
