"""e98: witness anatomy of OG-C3 at SAT residues (TASK M1).

For each SAT M (all != 0 mod 8 in the sample), find an AP-free order of
(M, 2M] satisfying the C3 precedences
    t5 := 2M-5 before b5 := M+5
    t3 := 2M-3 before b6 := M+6
    t10 := 2M-10 before b3 := M+3
and record:
  (a) the full relative order of the six values {b3,b5,b6,t3,t5,t10};
  (b) T-positions of the six values as fractions of the order length;
  (c) for each precedence pair, the multiset of values placed strictly
      between them in T, summarized by residue class mod 8 (and by half:
      bottom (M,3M/2] vs top (3M/2,2M]).
Additionally enumerates ALL feasible relative orders of the six values
(blocking-clause enumeration over the 15 pairwise orientations; the three
precedence units cap this at 90) so that pairwise relations forced across
every witness — not incidental solver choices — can be identified, per M
and in common across all SAT M.

Output: data/c3_witness_anatomy.json.  Usage: python e98_c3_witness.py
"""
import json
import os
import sys
import time

import numpy as np
from pysat.solvers import Cadical195

MS = [41, 42, 43, 44, 45, 46, 47, 49, 50, 52, 60, 68, 76, 84, 92, 100]
ENUM_CAP = 200          # safety cap on six-order enumeration (true max is 90)
KEYS = ["b3", "b5", "b6", "t3", "t5", "t10"]


def build(M):
    lo, hi = M, 2 * M
    V = list(range(lo + 1, hi + 1))
    n = len(V)
    idx = {v: i for i, v in enumerate(V)}
    var = {}
    c = 0
    for i in range(n):
        for j in range(i + 1, n):
            c += 1
            var[(i, j)] = c

    def o(u, w):
        i, j = idx[u], idx[w]
        return var[(i, j)] if i < j else -var[(j, i)]

    six = {"b3": M + 3, "b5": M + 5, "b6": M + 6,
           "t3": 2 * M - 3, "t5": 2 * M - 5, "t10": 2 * M - 10}
    prec = [("t5", "b5"), ("t3", "b6"), ("t10", "b3")]
    cl = [[o(six[t], six[b])] for (t, b) in prec]
    ntr = 0
    for y in V:
        d = 1
        while y + d <= hi:
            x, z = y - d, y + d
            d += 1
            if x > lo:
                cl.append([-o(x, y), -o(y, z)])
                cl.append([-o(z, y), -o(y, x)])
                ntr += 1
    return V, n, idx, var, o, cl, six, prec, ntr


def solve_lazy(sol, var, n):
    """Solve with lazy transitivity; returns B (before-matrix) or None."""
    while True:
        if not sol.solve():
            return None
        model = set(l for l in sol.get_model() if l > 0)
        B = np.zeros((n, n), dtype=bool)
        for (i, j), lit in var.items():
            if lit in model:
                B[i, j] = True
            else:
                B[j, i] = True
        R2 = (B.astype(np.uint8) @ B.astype(np.uint8)) > 0
        miss = R2 & ~B & ~np.eye(n, dtype=bool) & B.T
        ii, jj = np.nonzero(miss)
        if len(ii) == 0:
            return B

        def lit_(p, q):
            return var[(p, q)] if p < q else -var[(q, p)]

        new = []
        for i, j in zip(ii[:30000], jj[:30000]):
            ks = np.nonzero(B[i] & B[:, j])[0]
            new.append([-lit_(i, int(ks[0])), -lit_(int(ks[0]), j),
                        lit_(i, j)])
        sol.append_formula(new)


def order_from_B(B, V):
    wins = B.sum(axis=1)
    return [V[i] for i in sorted(range(len(V)), key=lambda i: -int(wins[i]))]


def verify(order, M, six, prec):
    """Independent check: order is AP-free on (M,2M] and satisfies C3."""
    pos = {v: p for p, v in enumerate(order)}
    lo, hi = M, 2 * M
    for y in range(lo + 1, hi + 1):
        d = 1
        while y + d <= hi:
            x, z = y - d, y + d
            d += 1
            if x > lo:
                if pos[x] < pos[y] < pos[z] or pos[x] > pos[y] > pos[z]:
                    return False
    for (t, b) in prec:
        if pos[six[t]] >= pos[six[b]]:
            return False
    return True


def anatomy(order, M, six, prec):
    n = len(order)
    pos = {v: p for p, v in enumerate(order)}
    six_sorted = sorted(KEYS, key=lambda k: pos[six[k]])
    rec = {
        "six_values": six,
        "six_mod8": {k: six[k] % 8 for k in KEYS},
        "six_order": six_sorted,
        "six_order_str": " < ".join(six_sorted),
        "six_positions": {k: {"pos": pos[six[k]],
                              "frac": round(pos[six[k]] / (n - 1), 4)}
                          for k in KEYS},
        "between": {},
    }
    half = M + (M / 2)
    for (t, b) in prec:
        lo_p, hi_p = pos[six[t]], pos[six[b]]
        mid = [v for v in order[lo_p + 1:hi_p]]
        mod8 = {r: 0 for r in range(8)}
        for v in mid:
            mod8[v % 8] += 1
        rec["between"][f"{t}<{b}"] = {
            "count": len(mid),
            "mod8": mod8,
            "bottom_half": sum(1 for v in mid if v <= half),
            "top_half": sum(1 for v in mid if v > half),
            "values": mid,
        }
    return rec


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = {}
    for M in MS:
        t0 = time.time()
        V, n, idx, var, o, cl, six, prec, ntr = build(M)
        sol = Cadical195(bootstrap_with=cl)
        B = solve_lazy(sol, var, n)
        if B is None:
            out[str(M)] = {"status": "UNSAT"}
            print(f"M={M}: UNSAT (unexpected)", flush=True)
            continue
        order = order_from_B(B, V)
        assert verify(order, M, six, prec), f"witness check failed M={M}"
        rec = anatomy(order, M, six, prec)
        rec["status"] = "SAT"
        rec["M_mod8"] = M % 8
        rec["n"] = n
        rec["witness_order"] = order

        # enumerate all feasible relative orders of the six values
        feas = []
        while B is not None and len(feas) < ENUM_CAP:
            posn = {v: p for p, v in
                    enumerate(order_from_B(B, V))}
            so = tuple(sorted(KEYS, key=lambda k: posn[six[k]]))
            feas.append(so)
            block = []
            for a in range(6):
                for b in range(a + 1, 6):
                    u, w = six[KEYS[a]], six[KEYS[b]]
                    lit = o(u, w) if posn[u] < posn[w] else o(w, u)
                    block.append(-lit)
            sol.append_formula([block])
            B = solve_lazy(sol, var, n)
        sol.delete()
        rec["feasible_six_orders"] = [" < ".join(s) for s in feas]
        rec["n_feasible_six_orders"] = len(feas)
        rec["enumeration_complete"] = len(feas) < ENUM_CAP
        # pairwise relations forced across every feasible six-order
        forced = []
        for a in range(6):
            for b in range(6):
                if a == b:
                    continue
                ka, kb = KEYS[a], KEYS[b]
                if all(s.index(ka) < s.index(kb) for s in feas):
                    forced.append(f"{ka}<{kb}")
        rec["forced_pairs"] = sorted(forced)
        out[str(M)] = rec
        print(f"M={M} (mod8={M % 8}): n={n} witness={rec['six_order_str']} "
              f"| {len(feas)} feasible six-orders "
              f"| forced={rec['forced_pairs']} ({time.time()-t0:.0f}s)",
              flush=True)

    # cross-M summary
    sat_ms = [m for m in MS if out[str(m)].get("status") == "SAT"]
    common = None
    for m in sat_ms:
        fp = set(out[str(m)]["forced_pairs"])
        common = fp if common is None else (common & fp)
    inter = None
    for m in sat_ms:
        fo = set(out[str(m)]["feasible_six_orders"])
        inter = fo if inter is None else (inter & fo)
    out["_summary"] = {
        "sat_Ms": sat_ms,
        "forced_pairs_common_to_all_SAT_M": sorted(common or []),
        "six_orders_feasible_for_every_SAT_M": sorted(inter or []),
    }
    path = os.path.join(root, "data", "c3_witness_anatomy.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\ncommon forced pairs: {sorted(common or [])}", flush=True)
    print(f"six-orders feasible at every SAT M: {len(inter or [])}",
          flush=True)
    print(f"wrote {path}", flush=True)


if __name__ == "__main__":
    main()
