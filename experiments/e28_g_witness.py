"""Recompute g_256(64) and dump the optimal witness for structure mining."""
import sys, time, json
sys.path.insert(0, 'experiments')
from e25_cpsat import build_model, sa
from ortools.sat.python import cp_model

X, L = 256, 64
m, pos, V = build_model(X)
small = [v for v in V if v <= L]
gmax = m.NewIntVar(0, len(V) - 1, "gmax")
m.AddMaxEquality(gmax, [pos[v] for v in small])
m.Minimize(gmax)
s = cp_model.CpSolver()
s.parameters.num_search_workers = 8
s.parameters.max_time_in_seconds = 1800
st = s.Solve(m)
print("status", st, "g =", s.Value(gmax), flush=True)
order = sorted(V, key=lambda v: s.Value(pos[v]))
json.dump(order, open("data/g256_witness.json", "w"))
g = s.Value(gmax)
pre = order[:g + 1]
post = order[g + 1:]
big_pre = sorted(v for v in pre if v > 128)
big_post = sorted(v for v in post if v > 128)
print(f"bigs before small-completion: {len(big_pre)}", flush=True)
print(f"bigs after ({len(big_post)}): {big_post}", flush=True)
print(f"smalls order: {[v for v in order if v <= 64]}", flush=True)
