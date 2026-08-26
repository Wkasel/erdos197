"""e124p_odd_schema_verify: FRONT N2-OFF -- the FIRST ODD-CLASS hand
schema, verified end-to-end e113-style: lane C at x = 11,
C(11) = {t0<b6, t2<b5, t5<b3}, class M = 5 mod 8 (law M = x+2 mod 8).

No integer m0 exists for odd M; the phase battleground is
t2 = 2M-2 against the HALF-INTEGER center's left neighbour
c- = (3M-1)/2:

  HALF-hi: AP + {t2<b5, t5<b3} forces c- < t2
     (refute t2 < c-: Lemma D on D1 = (M+1, M+3, ..., 2M) [d=2] and
      Q1 = (M+1, M+5, ..., 2M) [d=4]; 4 branches, all close)
  HALF-lo: AP + {t0<b6, t2<b5} forces t2 < c-
     (refute c- < t2: Lemma D on D1, Q1, Q3 = (M+3, ...) [d=4];
      8 branches, all close)
  COMPOSITION: t2 != c- (2M-2 = (3M-1)/2 iff M = 3), so AP + C(11)
     is UNSAT on the whole class M = 5 mod 8: the {11,12} rung fires
     there.  Overlapping halves share t2<b5 (as in the B2 schema).
  SHARPNESS: at M = 1, 3, 7 mod 8 (odd controls) branches survive
     and Cadical finds AP + C(11) SAT.

Run: .venv/bin/python experiments/e124p_odd_schema_verify.py [--fast]
Output: data/e124p_odd_schema.json;  exit 1 on any failure.
"""
import itertools
import json
import sys
import time

from e124e_closure_halves import closure
from e124g_branch_closure import ladder, fiat_edges
from e124i_k4_schema_verify import solver_check

BASE = "/Users/will/Dev/personal/tasks/math/erdos197/data"
C11 = [(0, 6), (2, 5), (5, 3)]


def half_surv(M, seeds, lkeys):
    pool = {"D1": (M + 1, 2, 2 * M), "Q1": (M + 1, 4, 2 * M),
            "Q3": (M + 3, 4, 2 * M)}
    lads = [ladder(*pool[k]) for k in lkeys]
    surv = 0
    for pol in itertools.product((True, False), repeat=len(lads)):
        ed = set(seeds)
        for lad, lf in zip(lads, pol):
            ed |= fiat_edges(lad, lf)
        if closure(M, ed)[0] != "contradiction":
            surv += 1
    return surv


def run_scale(M):
    cm = (3 * M - 1) // 2
    t0, t2, t5 = 2 * M, 2 * M - 2, 2 * M - 5
    b3, b5, b6 = M + 3, M + 5, M + 6
    assert t2 != cm
    sA = half_surv(M, {(t2, b5), (t5, b3), (t2, cm)}, ("D1", "Q1"))
    sB = half_surv(M, {(t0, b6), (t2, b5), (cm, t2)},
                   ("D1", "Q1", "Q3"))
    return sA, sB


def main():
    fast = "--fast" in sys.argv
    scales = list(range(21, 166, 8))          # 19 scales, 5 mod 8
    controls = [23, 31, 39, 47, 55, 63, 25, 33, 41, 49, 57, 65,
                27, 35, 43, 51, 59, 67]      # 7, 1, 3 mod 8
    if fast:
        scales, controls = scales[:5], controls[:6]
    res = {"scales": [], "controls": [], "fail": []}
    t00 = time.time()
    for M in scales:
        sA, sB = run_scale(M)
        sv = solver_check(M, C11, expect_unsat=True) if M <= 96 else None
        row = {"M": M, "survA": sA, "survB": sB,
               "solver_unsat_xcheck": sv}
        res["scales"].append(row)
        if sA or sB or sv is False:
            res["fail"].append(row)
        print(f"M={M}: HALF-hi {'4/4' if not sA else 'FAIL ' + str(sA)}, "
              f"HALF-lo {'8/8' if not sB else 'FAIL ' + str(sB)}"
              + (f", solver xcheck {'ok' if sv else 'FAIL'}"
                 if sv is not None else "")
              + f"  ({time.time()-t00:.0f}s)", flush=True)
    for M in controls:
        sA, sB = run_scale(M)
        sv = solver_check(M, C11, expect_unsat=False) if M <= 96 else None
        row = {"M": M, "survA": sA, "survB": sB,
               "solver_sat_xcheck": sv}
        res["controls"].append(row)
        if not ((sA or sB) and sv in (True, None)):
            res["fail"].append(row)
        print(f"M={M} ({M % 8} mod 8 control): survivors hi={sA} "
              f"lo={sB}"
              + (f", solver SAT xcheck {'ok' if sv else 'FAIL'}"
                 if sv is not None else "")
              + f"  ({time.time()-t00:.0f}s)", flush=True)
    json.dump(res, open(f"{BASE}/e124p_odd_schema.json", "w"), indent=1)
    n_ok = sum(1 for r in res["scales"]
               if not r["survA"] and not r["survB"])
    print(f"\nSCHEMA: {n_ok}/{len(res['scales'])} odd-class scales "
          f"verified, {len(res['fail'])} failures")
    if res["fail"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
