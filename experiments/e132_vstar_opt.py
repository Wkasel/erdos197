"""v* by direct optimization (CP-SAT): minimize the symmetric seam-inversion
budget v with inv_A <= v and inv_B <= v, balanced 3-block window (M, 8M].
One run per M gives v*(bal, M) exactly (or tight bounds on timeout).
Args: M [timelimit_s]"""
import sys, math, time
from ortools.sat.python import cp_model

M = int(sys.argv[1])
TL = float(sys.argv[2]) if len(sys.argv) > 2 else 43200.0
V = list(range(M + 1, 8 * M + 1))
n = len(V)
B0 = [v for v in V if v <= 2 * M]
B1 = [v for v in V if 2 * M < v <= 4 * M]
B2 = [v for v in V if v > 4 * M]
md = cp_model.CpModel()
a = {v: md.NewBoolVar(f"a{v}") for v in V}
prec = {}
for team in ("A", "B"):
    for i in range(n):
        for j in range(i + 1, n):
            prec[(team, V[i], V[j])] = md.NewBoolVar("")
def plit(team, u, w, neg=False):
    if u < w:
        b = prec[(team, u, w)]
    else:
        b = prec[(team, w, u)]
        neg = not neg
    return b.Not() if neg else b
def inteam(team, v):
    return a[v] if team == "A" else a[v].Not()
# transitivity per team (complete)
for team in ("A", "B"):
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                u, w, x = V[i], V[j], V[k]
                md.AddBoolOr([plit(team, u, w, True), plit(team, w, x, True), plit(team, u, x)])
                md.AddBoolOr([plit(team, u, w), plit(team, w, x), plit(team, u, x, True)])
# guarded APs both directions
Vs = set(V)
for b in V:
    d = 1
    while b - d >= V[0] and b + d <= V[-1]:
        aa, c = b - d, b + d
        if aa in Vs and c in Vs:
            for team in ("A", "B"):
                g = [inteam(team, t).Not() for t in (aa, b, c)]
                md.AddBoolOr(g + [plit(team, aa, b, True), plit(team, b, c, True)])
                md.AddBoolOr(g + [plit(team, aa, b), plit(team, b, c)])
        d += 1
# balance bounds
for blk in (B0, B1, B2):
    bnd = math.ceil(len(blk) / 2)
    md.Add(sum(a[v] for v in blk) >= bnd - (len(blk) - bnd))  # loose lower; exact below
for blk in (B0, B1, B2):
    bnd = math.ceil(len(blk) / 2)
    sA = sum(a[v] for v in blk)
    md.Add(sA >= len(blk) - bnd)  # team B ceil-balance => A >= floor
    md.Add(sA <= bnd)             # A <= ceil  (balance both ways)
# seam inversion indicators
xs = {"A": [], "B": []}
seampairs = [(u, w) for u in B0 for w in B1] + [(u, w) for u in B1 for w in B2]
for team in ("A", "B"):
    for (u, w) in seampairs:
        x = md.NewBoolVar("")
        md.AddBoolOr([inteam(team, u).Not(), inteam(team, w).Not(),
                      plit(team, u, w), x])
        xs[team].append(x)
vvar = md.NewIntVar(0, len(seampairs), "v")
md.Add(sum(xs["A"]) <= vvar)
md.Add(sum(xs["B"]) <= vvar)
md.Minimize(vvar)
s = cp_model.CpSolver()
s.parameters.num_search_workers = 8
s.parameters.max_time_in_seconds = TL
t0 = time.time()
st = s.Solve(md)
name = {cp_model.OPTIMAL: "OPTIMAL", cp_model.FEASIBLE: "FEASIBLE",
        cp_model.INFEASIBLE: "INFEASIBLE"}.get(st, "UNKNOWN")
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    print(f"VSTAR bal M={M}: {name} v*={s.ObjectiveValue():.0f} "
          f"lower-bound={s.BestObjectiveBound():.0f} ({time.time()-t0:.0f}s)",
          flush=True)
else:
    print(f"VSTAR bal M={M}: {name} ({time.time()-t0:.0f}s)", flush=True)
