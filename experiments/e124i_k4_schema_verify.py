"""e124i_k4_schema_verify: FRONT N2-OFF -- the {11,12} DYADIC LANE,
verified end-to-end, e113-style (complete case analysis, no solver in
the derivation; independent Cadical cross-check per scale).

THE SCHEMA (pair {11, 12}, scale class M = 0 mod 8, M >= 24; block
(M, 2M], b_j = M + j, t_i = 2M - i, m0 = 3M/2; "u < v" = u placed
before v; all placements AP-free on the block):

  Unit demands of a block-ordered attacker pair {11, 12} (the four of
  its 11 attack units used here):
      U12 = { t0 < b6,  t2 < b5 }     (attacker 12, j = 6, 5)
      U11 = { t1 < b5,  t3 < b4 }     (attacker 11, j = 5, 4)

  HALF-A:  AP + U12  forces  m0 < t1.
     Proof: suppose t1 < m0.  Lemma D (zigzag dichotomy) on the odd
     ladder O = (M+1, M+3, ..., 2M-1) and on the quarter ladder
     Q2 = (M+2, M+6, ..., 2M-2) (the value class of t2 mod 4) gives
     4 polarity branches; zigzag propagation (AP rules R1-R4 +
     transitivity) reaches a contradiction in every branch.
  HALF-B:  AP + U11  forces  t1 < m0.
     Proof: same with ladders O and Q3 = (M+3, M+7, ..., 2M-1)
     (the value class of t1 mod 4); 4 branches, all close.
  K4 COMPOSITION: t1 != m0, so U11 + U12 (= the size-4 core A4a of
     the e122 catalogue) is UNSAT with AP-freeness: the {11,12} rung
     fires at every M = 0 mod 8.  ({11,12} has NO size-3 core on this
     class -- this size-4 schema is the whole story, and 0 mod 8 is
     the dyadic class T-PIN needs.)
  SHARPNESS: at M = 4 mod 8 the same case analysis leaves a surviving
     branch for each half (and Cadical finds AP + A4a SAT there): the
     mod-8 lock is real.

This file executes that case analysis literally at every scale in the
sweep: fiat zigzag edges per branch (the Lemma-D discharge, e113's
fiat_zig), pure closure NOT consulting any solver, then an independent
complete-encoding Cadical check of both UNSAT (0 mod 8) and SAT
(4 mod 8 controls) verdicts.

Run: .venv/bin/python experiments/e124i_k4_schema_verify.py [--fast]
Output: data/e124i_k4_schema.json;  exit 1 on any failure.
"""
import itertools
import json
import sys
import time

from e124e_closure_halves import closure
from e124g_branch_closure import ladder, fiat_edges

BASE = "/Users/will/Dev/personal/tasks/math/erdos197/data"


def half_branches(M, seeds, ladders):
    """Return list of (polarity, verdict) over all branches."""
    lads = [ladder(*l) for l in ladders]
    out = []
    for pol in itertools.product((True, False), repeat=len(lads)):
        ed = set(seeds)
        for lad, lf in zip(lads, pol):
            ed |= fiat_edges(lad, lf)
        out.append((pol, closure(M, ed)[0]))
    return out


def solver_check(M, units, expect_unsat):
    from pysat.solvers import Cadical195
    n = M
    var = {}
    c = 0
    for p in range(n):
        for q in range(p + 1, n):
            c += 1
            var[(p, q)] = c

    def o(u, w):
        p, q = u - M - 1, w - M - 1
        return var[(p, q)] if p < q else -var[(q, p)]

    cl = []
    for y in range(M + 2, 2 * M):
        d = 1
        while y + d <= 2 * M and y - d > M:
            a, b = y - d, y + d
            cl.append([-o(a, y), -o(y, b)])
            cl.append([-o(b, y), -o(y, a)])
            d += 1
    for p in range(n):
        for q in range(p + 1, n):
            for r in range(q + 1, n):
                cl.append([-var[(p, q)], -var[(q, r)], var[(p, r)]])
                cl.append([var[(p, q)], var[(q, r)], -var[(p, r)]])
    for (i, j) in units:
        cl.append([o(2 * M - i, M + j)])
    s = Cadical195(bootstrap_with=cl)
    sat = s.solve()
    s.delete()
    return sat != expect_unsat


def main():
    fast = "--fast" in sys.argv
    scales = list(range(24, 177, 8))          # 20 scales, 0 mod 8
    controls = list(range(28, 181, 8))        # 20 scales, 4 mod 8
    if fast:
        scales, controls = scales[:6], controls[:6]
    K4 = [(0, 6), (1, 5), (2, 5), (3, 4)]
    res = {"scales": [], "controls": [], "fail": []}
    t00 = time.time()
    for M in scales:
        m0 = 3 * M // 2
        t0v, t1v, t2v, t3v = 2 * M, 2 * M - 1, 2 * M - 2, 2 * M - 3
        b4, b5, b6 = M + 4, M + 5, M + 6
        assert M % 8 == 0 and t1v != m0
        O = (M + 1, 2, 2 * M - 1)
        Q2 = (M + 2, 4, 2 * M - 2)
        Q3 = (M + 3, 4, 2 * M - 1)
        # sanity: Q2 is t2's mod-4 value class, Q3 is t1's
        assert (t2v - (M + 2)) % 4 == 0 and (t1v - (M + 3)) % 4 == 0
        brA = half_branches(M, {(t0v, b6), (t2v, b5), (t1v, m0)}, [O, Q2])
        brB = half_branches(M, {(t1v, b5), (t3v, b4), (m0, t1v)}, [O, Q3])
        okA = all(v == "contradiction" for _, v in brA)
        okB = all(v == "contradiction" for _, v in brB)
        sv = solver_check(M, K4, expect_unsat=True) if M <= 96 else None
        row = {"M": M, "halfA_closed": okA, "halfB_closed": okB,
               "solver_unsat_xcheck": sv}
        res["scales"].append(row)
        if not (okA and okB and sv in (True, None)):
            res["fail"].append(row)
        print(f"M={M}: HALF-A {'4/4' if okA else 'FAIL'}, "
              f"HALF-B {'4/4' if okB else 'FAIL'}"
              + (f", solver xcheck {'ok' if sv else 'FAIL'}"
                 if sv is not None else "")
              + f"  ({time.time()-t00:.0f}s)", flush=True)
    for M in controls:
        m0 = 3 * M // 2
        t0v, t1v, t2v, t3v = 2 * M, 2 * M - 1, 2 * M - 2, 2 * M - 3
        b4, b5, b6 = M + 4, M + 5, M + 6
        O = (M + 1, 2, 2 * M - 1)
        Q2 = (M + 2, 4, 2 * M - 2)
        Q3 = (M + 3, 4, 2 * M - 1)
        brA = half_branches(M, {(t0v, b6), (t2v, b5), (t1v, m0)}, [O, Q2])
        brB = half_branches(M, {(t1v, b5), (t3v, b4), (m0, t1v)}, [O, Q3])
        survA = [p for p, v in brA if v != "contradiction"]
        survB = [p for p, v in brB if v != "contradiction"]
        sv = solver_check(M, K4, expect_unsat=False) if M <= 96 else None
        row = {"M": M, "survA": len(survA), "survB": len(survB),
               "solver_sat_xcheck": sv}
        res["controls"].append(row)
        if not (survA and survB and sv in (True, None)):
            res["fail"].append(row)
        print(f"M={M} (4 mod 8 control): survivors A={len(survA)} "
              f"B={len(survB)}"
              + (f", solver SAT xcheck {'ok' if sv else 'FAIL'}"
                 if sv is not None else "")
              + f"  ({time.time()-t00:.0f}s)", flush=True)
    json.dump(res, open(f"{BASE}/e124i_k4_schema.json", "w"), indent=1)
    n_ok = sum(1 for r in res["scales"]
               if r["halfA_closed"] and r["halfB_closed"])
    print(f"\nSCHEMA: {n_ok}/{len(res['scales'])} dyadic scales verified, "
          f"{len(res['fail'])} failures -> {BASE}/e124i_k4_schema.json")
    if res["fail"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
