"""e174d_scale_checks: finish the x = 27 scale grid (notes/74).

  (a) M = 144: intact + all support singles + ALL support 2-subsets
      (the batch both census runs were interrupted before reaching).
  (b) d*(27) <= 6 at M = 112 and 144: direct SAT queries on the
      pure-bottom transversal {b2, b4, ..., b12} (and the mixed
      all-top transversal {t23, t19, t15, t11, t7, t3} as a bonus),
      models audited.

Run: .venv/bin/python experiments/e174d_scale_checks.py
Artifacts: merged into data/e174_n3_growth.json (key partD_scale)
"""
import itertools
import json
import sys
import time

sys.path.insert(0, "/Users/will/Dev/personal/tasks/math/erdos197/experiments")
from e174_n3_growth import BASE, Gadget, census, offset, support_values  # noqa: E402


def dump(out):
    path = f"{BASE}/e174_n3_growth.json"
    try:
        old = json.load(open(path))
    except Exception:
        old = {}
    old.update(out)
    json.dump(old, open(path, "w"), indent=1)


out = {"partD_scale": {}}
x = 27

# (a) M = 144 singles + pairs
M = 144
t0 = time.time()
g = Gadget(M, x)
sup = support_values(M, x)
intact = g.query([])
n1, esc1, _ = census(g, ([v] for v in sup), f"D M={M} sup1")
n2, esc2, _ = census(g, itertools.combinations(sup, 2), f"D M={M} sup2")
out["partD_scale"]["144_census"] = {
    "intact": "SAT!" if intact else "UNSAT",
    "n1": n1, "escapes1": esc1, "n2": n2, "escapes2": esc2,
    "secs": round(time.time() - t0, 1)}
print(f"[D] M=144 census: intact="
      f"{'SAT!' if intact else 'UNSAT'}, singles/pairs esc="
      f"{esc1 or 'NONE'}/{esc2 or 'NONE'} "
      f"({out['partD_scale']['144_census']['secs']}s)", flush=True)
g.delete()
dump(out)

# (b) transversal escapes at 112 / 144
for M in (112, 144):
    g = Gadget(M, x)
    for name, P in (("bottom", [M + j for j in (2, 4, 6, 8, 10, 12)]),
                    ("top", [2 * M - i for i in (23, 19, 15, 11, 7, 3)])):
        t0 = time.time()
        sat = g.query(P)  # audits the model if SAT
        out["partD_scale"][f"{M}_{name}_transversal"] = {
            "P": [offset(v, M) for v in P],
            "verdict": "SAT (escape, audited)" if sat else "UNSAT",
            "secs": round(time.time() - t0, 1)}
        print(f"[D] M={M} {name} transversal {out['partD_scale'][f'{M}_{name}_transversal']}",
              flush=True)
    g.delete()
    dump(out)
print("D_EXIT", flush=True)
