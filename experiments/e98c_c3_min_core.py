"""e98c: minimality of the C3 core at M = 0 mod 8, + carrier classification.

Part 1: for M in {48, 56} (UNSAT residue), tests every subset of the three
C3 precedences.  Result: all proper subsets SAT, full triple UNSAT -- C3 is
a minimal core; under any two precedences the third is anti-forced.

Part 2: classifies every feasible six-order recorded by e98 (in
data/c3_witness_anatomy.json) by the interleaving pattern of the three
precedence pairs (disjoint / nested / crossing) and by carrier (a pair
containing both others strictly inside).  Appends both to the JSON under
"_min_core_mod8_0" and "_carrier_by_class".
"""
import itertools
import json
import os
import sys

import numpy as np
from pysat.solvers import Cadical195

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from e98b_c3_forced import build, solve_lazy  # noqa: E402

PREC = [("t5", "b5"), ("t3", "b6"), ("t10", "b3")]


def test(M, prec_subset, extra=()):
    V, n, var, o, cl, six, top = build(M)
    cl = cl[3:]  # strip the three baked-in precedence units
    for (t, b) in list(prec_subset) + list(extra):
        cl.append([o(six[t], six[b])])
    sol = Cadical195(bootstrap_with=cl)
    res = solve_lazy(sol, var, n)
    sol.delete()
    return res


def carrier_of(order_str):
    seq = order_str.split(" < ")
    pos = {k: i for i, k in enumerate(seq)}
    for (t, b) in PREC:
        others = [x for p in PREC if p != (t, b) for x in p]
        if all(pos[t] < pos[x] < pos[b] for x in others):
            return f"{t}<..<{b}"
    return None


def has_crossing(order_str):
    seq = order_str.split(" < ")
    pos = {k: i for i, k in enumerate(seq)}
    for (p1, p2) in itertools.combinations(PREC, 2):
        i1, j1 = pos[p1[0]], pos[p1[1]]
        i2, j2 = pos[p2[0]], pos[p2[1]]
        if not (j1 < i2 or j2 < i1 or (i1 < i2 and j2 < j1)
                or (i2 < i1 and j1 < j2)):
            return True
    return False


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(root, "data", "c3_witness_anatomy.json")
    out = json.load(open(path))

    core = {}
    for M in [48, 56]:
        row = {}
        for k in range(4):
            for sub in itertools.combinations(PREC, k):
                key = "+".join(f"{t}<{b}" for t, b in sub) or "(none)"
                row[key] = "SAT" if test(M, sub) else "UNSAT"
        row["t5<b5 + t3<b6 => b3<t10 forced"] = (
            "yes" if not test(M, [PREC[0], PREC[1]], extra=[("t10", "b3")])
            else "no")
        core[str(M)] = row
        print(f"M={M}: {row}", flush=True)
    out["_min_core_mod8_0"] = core

    carrier = {}
    for m, rec in out.items():
        if m.startswith("_") or rec.get("status") != "SAT":
            continue
        rows = []
        for o_ in rec["feasible_six_orders"]:
            rows.append({"order": o_, "carrier": carrier_of(o_),
                         "crossing": has_crossing(o_)})
        carrier[m] = rows
    out["_carrier_by_class"] = carrier

    with open(path, "w") as f:
        json.dump(out, f, indent=1)
    print(f"updated {path}", flush=True)


if __name__ == "__main__":
    main()
