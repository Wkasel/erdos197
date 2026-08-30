"""e176_derivation_meter: FRONT N2-PARAMETRIC step 3 -- how do the
branch-closure derivations SCALE in x and M?

For the uniformization discussion (notes/73 §5): the parametric lane
claim needs, at bottom, that each polarity branch of each (lane,
x mod 8) cell closes at EVERY lattice point (x, M).  The machine
verifies lattice samples; the hand write-up must supply a uniform
derivation.  This instrument measures the SIZE of the closure
derivation (facts derived before contradiction) along two axes:

  (a) x-axis: fixed lane/branch, M = thr(x) + const class offset,
      x = x0, x0+8, ..., x0+56 -- if the derivation is an x-uniform
      schema, size should track M affinely and show NO independent
      growth in x beyond the affine M-coupling;
  (b) M-axis: fixed x, in-class M sweep -- expected Θ(M) or Θ(M²)
      (ladder flood species; the Lemma-Z induction handles this).

Run: .venv/bin/python experiments/e176_derivation_meter.py
Output: data/e176_derivation_meter.{json,log}
"""
import json
import time
from collections import defaultdict

from e124g_branch_closure import ladder, fiat_edges
from e174_param_lanes import lanes_for
from e175_param_template import (pool_def, seeds_for, in_class_scales,
                                 e174_thr, OUT)

BASE = "/Users/will/Dev/personal/tasks/math/erdos197/data"


def closure_count(M, seeds):
    """e124e closure with fact counting; returns (verdict, nfacts)."""
    lo, hi = M + 1, 2 * M
    rule = defaultdict(list)
    for y in range(lo + 1, hi):
        d = 1
        while y + d <= hi and y - d >= lo:
            x, z = y - d, y + d
            rule[(x, y)].append((z, y))
            rule[(z, y)].append((x, y))
            rule[(y, x)].append((y, z))
            rule[(y, z)].append((y, x))
            d += 1
    facts = set(seeds)
    frontier = list(facts)
    succ, pred = defaultdict(set), defaultdict(set)
    for (u, v) in facts:
        succ[u].add(v)
        pred[v].add(u)

    def add(u, v):
        if (u, v) in facts:
            return None
        if (v, u) in facts:
            return (u, v)
        facts.add((u, v))
        succ[u].add(v)
        pred[v].add(u)
        frontier.append((u, v))
        return None

    while frontier:
        (u, v) = frontier.pop()
        for conc in rule[(u, v)]:
            if add(*conc):
                return ("contradiction", len(facts))
        for w in list(pred[u]):
            if add(w, v):
                return ("contradiction", len(facts))
        for w in list(succ[v]):
            if add(u, w):
                return ("contradiction", len(facts))
    return ("fixpoint", len(facts))


def cell_data():
    return {r["cell"]: r for r in
            json.load(open(OUT))["cells"] if r.get("ok")}


def measure(rec, x, M, branch=0):
    lane = rec["lane"]
    K = lanes_for(x)[lane]
    istar = rec["istar"]
    out = {}
    for hn, Sk, ph in (("hi", rec["S_hi"], "lo"),
                       ("lo", rec["S_lo"], "hi")):
        lkeys = rec["ladders"][hn]
        pool = pool_def(M)
        lads = [ladder(*pool[k]) for k in lkeys]
        pol = [(branch >> b) & 1 == 0 for b in range(len(lads))]
        ed = set(seeds_for(M, [tuple(K[k]) for k in Sk], istar, ph))
        for lad, lf in zip(lads, pol):
            ed |= fiat_edges(lad, lf)
        out[hn] = closure_count(M, ed)
    return out


def main():
    recs = cell_data()
    report = {"x_axis": {}, "M_axis": {}}
    for cell, rec in sorted(recs.items()):
        lane, xi = rec["lane"], rec["xi"]
        x0, istar, r8 = rec["x0"], rec["istar"], \
            (rec["x0"] + __import__("e174_param_lanes").LAW[lane]) % 8
        rows = []
        for k in range(0, 8):
            x = x0 + 8 * k
            K = lanes_for(x)[lane]
            if min(i for i, _ in K) < 0:
                continue
            M = in_class_scales(r8, K, istar, 2, e174_thr(lane, x))[1]
            r = measure(rec, x, M)
            rows.append((x, M, r["hi"], r["lo"]))
        report["x_axis"][cell] = rows
        print(f"{cell} x-axis: " + "; ".join(
            f"x={x} M={M} hi={h} lo={l}" for x, M, h, l in rows),
            flush=True)
        # M-axis at x0
        K = lanes_for(x0)[lane]
        rowsM = []
        for M in in_class_scales(r8, K, istar, 6, e174_thr(lane, x0)):
            r = measure(rec, x0, M)
            rowsM.append((M, r["hi"], r["lo"]))
        report["M_axis"][cell] = rowsM
        print(f"{cell} M-axis (x={x0}): " + "; ".join(
            f"M={M} hi={h} lo={l}" for M, h, l in rowsM), flush=True)
    json.dump(report, open(f"{BASE}/e176_derivation_meter.json", "w"),
              indent=1, default=list)
    print(f"-> {BASE}/e176_derivation_meter.json")


if __name__ == "__main__":
    main()
