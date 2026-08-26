"""e124l_b2_schema_verify: FRONT N2-OFF -- the {11,12} lane on the
= 2 mod 8 class (a = 2 mod 4 flip class), verified end-to-end,
e113-style.  Parity dual of e124i's dyadic schema.

THE SCHEMA (pair {11, 12}, M = 2 mod 8, M >= 18; m0 = 3M/2 ODD):

  Core B2 = {t2 < b5, t5 < b3, t7 < b2}
      (t2<b5: attacker 12, j = 5;  t5<b3, t7<b2: attacker 11, j = 3, 2)

  HALF-A2:  AP + {t5<b3, t7<b2}  forces  m0 < t2.
  HALF-B2:  AP + {t2<b5, t5<b3}  forces  t2 < m0.
     Each: Lemma D on the even ladder E = (M+2, ..., 2M) and the
     quarter ladder Q1 = (M+1, M+5, ..., 2M-1) (the mod-4 value class
     of t5, the shared unit) -- 4 polarity branches, zigzag
     propagation closes every branch.
  COMPOSITION: t2 != m0 (M != 4), so AP + B2 is UNSAT: the {11,12}
     rung fires on the whole class M = 2 mod 8.
  SHARPNESS: at M = 6 mod 8 branches survive and Cadical finds
     AP + B2 SAT.

Phase battleground is t2 = 2M-2 (EVEN value, odd center m0) -- the
parity dual of the dyadic schema's odd t1 / even m0.  Note the 2+2
OVERLAPPING anatomy: the shared unit t5<b3 sits in both halves, so a
3-unit core carries two 2-unit half-flips.

Run: .venv/bin/python experiments/e124l_b2_schema_verify.py [--fast]
Output: data/e124l_b2_schema.json;  exit 1 on any failure.
"""
import itertools
import json
import sys
import time

from e124e_closure_halves import closure
from e124g_branch_closure import ladder, fiat_edges
from e124i_k4_schema_verify import solver_check

BASE = "/Users/will/Dev/personal/tasks/math/erdos197/data"


def half_branches(M, seeds, ladders):
    lads = [ladder(*l) for l in ladders]
    out = []
    for pol in itertools.product((True, False), repeat=len(lads)):
        ed = set(seeds)
        for lad, lf in zip(lads, pol):
            ed |= fiat_edges(lad, lf)
        out.append((pol, closure(M, ed)[0]))
    return out


def main():
    fast = "--fast" in sys.argv
    scales = list(range(18, 171, 8))          # 20 scales, 2 mod 8
    controls = list(range(22, 175, 8))        # 20 scales, 6 mod 8
    if fast:
        scales, controls = scales[:6], controls[:6]
    B2 = [(2, 5), (5, 3), (7, 2)]
    res = {"scales": [], "controls": [], "fail": []}
    t00 = time.time()
    for M in scales:
        m0 = 3 * M // 2
        t2, t5, t7 = 2 * M - 2, 2 * M - 5, 2 * M - 7
        b2, b3, b5 = M + 2, M + 3, M + 5
        assert M % 8 == 2 and m0 % 2 == 1 and t2 != m0
        E = (M + 2, 2, 2 * M)
        Q1 = (M + 1, 4, 2 * M - 1)
        assert (t5 - (M + 1)) % 4 == 0      # Q1 is t5's value class
        brA = half_branches(M, {(t5, b3), (t7, b2), (t2, m0)}, [E, Q1])
        brB = half_branches(M, {(t2, b5), (t5, b3), (m0, t2)}, [E, Q1])
        okA = all(v == "contradiction" for _, v in brA)
        okB = all(v == "contradiction" for _, v in brB)
        sv = solver_check(M, B2, expect_unsat=True) if M <= 96 else None
        row = {"M": M, "halfA2_closed": okA, "halfB2_closed": okB,
               "solver_unsat_xcheck": sv}
        res["scales"].append(row)
        if not (okA and okB and sv in (True, None)):
            res["fail"].append(row)
        print(f"M={M}: HALF-A2 {'4/4' if okA else 'FAIL'}, "
              f"HALF-B2 {'4/4' if okB else 'FAIL'}"
              + (f", solver xcheck {'ok' if sv else 'FAIL'}"
                 if sv is not None else "")
              + f"  ({time.time()-t00:.0f}s)", flush=True)
    for M in controls:
        m0 = 3 * M // 2
        t2, t5, t7 = 2 * M - 2, 2 * M - 5, 2 * M - 7
        b2, b3, b5 = M + 2, M + 3, M + 5
        E = (M + 2, 2, 2 * M)
        Q1 = (M + 1, 4, 2 * M - 1)
        brA = half_branches(M, {(t5, b3), (t7, b2), (t2, m0)}, [E, Q1])
        brB = half_branches(M, {(t2, b5), (t5, b3), (m0, t2)}, [E, Q1])
        survA = [p for p, v in brA if v != "contradiction"]
        survB = [p for p, v in brB if v != "contradiction"]
        sv = solver_check(M, B2, expect_unsat=False) if M <= 96 else None
        row = {"M": M, "survA2": len(survA), "survB2": len(survB),
               "solver_sat_xcheck": sv}
        res["controls"].append(row)
        if not ((survA or survB) and sv in (True, None)):
            res["fail"].append(row)
        print(f"M={M} (6 mod 8 control): survivors A2={len(survA)} "
              f"B2={len(survB)}"
              + (f", solver SAT xcheck {'ok' if sv else 'FAIL'}"
                 if sv is not None else "")
              + f"  ({time.time()-t00:.0f}s)", flush=True)
    json.dump(res, open(f"{BASE}/e124l_b2_schema.json", "w"), indent=1)
    n_ok = sum(1 for r in res["scales"]
               if r["halfA2_closed"] and r["halfB2_closed"])
    print(f"\nSCHEMA: {n_ok}/{len(res['scales'])} scales verified, "
          f"{len(res['fail'])} failures -> {BASE}/e124l_b2_schema.json")
    if res["fail"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
