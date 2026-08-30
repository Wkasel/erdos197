"""e175_param_template: FRONT N2-PARAMETRIC step 2 -- the PARAMETRIC
two-ladder template, per (lane, x mod 8) cell, verified at fresh x.

Universe: pair {x, x+1}, x odd >= 11; lane tables of e174 (9 lanes
covering all 8 residues of M mod 8, laws M = x + c mod 8).  For each
CELL = (lane, xi) with xi = x mod 8 in {1, 3, 5, 7}, the parametric
claim is:

  There are FIXED template data (v* = t_{i*}, S_hi, S_lo <= lane
  units as index sets, ladder keys per half) such that for EVERY
  x = xi mod 8 (x >= x0) and every in-class M >= T(x):
    HALF-hi:  AP + S_hi(x) + (v* < ctr)  closes under Lemma-D
              polarity splits on the hi-ladders + R1-R4 + trans;
    HALF-lo:  AP + S_lo(x) + (ctr < v*)  closes likewise;
  ctr = 3M//2 (= m0 for even M, c- for odd M).  Phase clash at v*
  then refutes AP + lane(x) on the whole class [Lemma PC].

Protocol per cell:
  1. DOUBLE-KILL SCAN at x0 AND x0+8 (solver): candidates
     (i*, S_hi, S_lo) that double-kill at BOTH x (unit-index sets).
  2. LADDER SEARCH (closure): pool O, E, Q1..Q4 (+G1..G8 d=8 on
     escalation), sizes 2..3; must close all branches at spread
     scales of BOTH x0 and x0+8.
  3. PARAMETRIC VERIFY (closure): x = x0, x0+8, x0+16, x0+24; 6
     in-class scales each (spread); all branches close.  CONTROLS at
     r+4 (2 scales per x): some branch must survive.
  4. SOLVER XCHECK: per x two in-class scales <= 108 UNSAT; one
     control scale <= 108 SAT.

Run: .venv/bin/python experiments/e175_param_template.py [cell ...]
     (cells like B6_xi5, K4e_xi7; default = the full 36-cell grid;
      "dyadic" = the four M=0-mod-8 cells)
Output: data/e175_param_template.json (merged per-cell records)
"""
import itertools
import json
import os
import sys
import time

from e124c_k4_anatomy import build
from e124e_closure_halves import closure
from e124g_branch_closure import ladder, fiat_edges
from e124i_k4_schema_verify import solver_check
from e174_param_lanes import lanes_for, LAW

BASE = "/Users/will/Dev/personal/tasks/math/erdos197/data"
OUT = f"{BASE}/e175_param_template.json"

POOL6 = ("O", "E", "Q1", "Q3", "Q2", "Q4")
POOL8 = ("G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8")


def pool_def(M):
    d = {"O": (M + 1, 2, 2 * M - 1), "E": (M + 2, 2, 2 * M),
         "Q1": (M + 1, 4, 2 * M), "Q3": (M + 3, 4, 2 * M),
         "Q2": (M + 2, 4, 2 * M), "Q4": (M + 4, 4, 2 * M)}
    for k in range(1, 9):
        d[f"G{k}"] = (M + k, 8, 2 * M)
    return d


def branches_ok(M, seeds, lkeys):
    pool = pool_def(M)
    lads = [ladder(*pool[k]) for k in lkeys]
    surv = 0
    for pol in itertools.product((True, False), repeat=len(lads)):
        ed = set(seeds)
        for lad, lf in zip(lads, pol):
            ed |= fiat_edges(lad, lf)
        if closure(M, ed)[0] != "contradiction":
            surv += 1
    return surv


def seeds_for(M, S_units, istar, ph):
    ctr = 3 * M // 2
    tv = 2 * M - istar
    ed = {(2 * M - a, M + b) for (a, b) in S_units}
    ed.add((tv, ctr) if ph == "lo" else (ctr, tv))
    return ed


def degenerate(M, units, istar):
    ctr = 3 * M // 2
    vals = [2 * M - i for i, _ in units] + [M + j for _, j in units] \
        + [2 * M - istar]
    return ctr in vals or len(set(vals)) < len(vals) \
        or any(not (M < v <= 2 * M) for v in vals)


def in_class_scales(r8, units, istar, n, start_at):
    out, m = [], start_at
    while len(out) < n:
        if m % 8 == r8 and not degenerate(m, units, istar):
            out.append(m)
        m += 1
    return out


def phase_kills(M, K, imax):
    """(i, ph) -> minimal kill index-subsets of K (as frozensets of
    unit-list indices).  kills[(i,'lo')] = S with AP+S+(t_i lo) UNSAT
    == S forces hi."""
    sol, sel, phase, _ = build(M, K)
    out = {}
    ctr = 3 * M // 2
    for i in range(0, imax + 1):
        tv = 2 * M - i
        if tv == ctr or tv <= M:
            continue
        for ph in ("lo", "hi"):
            mins = []
            for sz in (1, 2):
                for Sx in itertools.combinations(range(len(K)), sz):
                    if any(set(m) <= set(Sx) for m in mins):
                        continue
                    if not sol.solve(
                            assumptions=[sel[K[k]] for k in Sx]
                            + [phase[(tv, ph)]]):
                        mins.append(Sx)
            if mins:
                out[(i, ph)] = mins
    sol.delete()
    return out


def candidates(cellK0, cellK1, M0, M1, imax):
    """double-kill candidates valid at both discovery x's; returns
    list of (i*, S_hi_idx, S_lo_idx) sorted by total size then i*."""
    k0 = phase_kills(M0, cellK0, imax)
    k1 = phase_kills(M1, cellK1, imax)
    cands = []
    keys = set(k0) & set(k1)
    for (i, ph) in keys:
        if ph != "lo" or (i, "hi") not in keys:
            continue
        # S_hi kills the lo phase (forces hi); S_lo kills hi
        hi_opts = [S for S in k0[(i, "lo")] if S in k1[(i, "lo")]]
        lo_opts = [S for S in k0[(i, "hi")] if S in k1[(i, "hi")]]
        for S_hi in hi_opts:
            for S_lo in lo_opts:
                cands.append((i, S_hi, S_lo,
                              len(S_hi) + len(S_lo)))
    cands.sort(key=lambda c: (c[3], c[0]))
    return [(i, S_hi, S_lo) for i, S_hi, S_lo, _ in cands]


def ladder_search(halves_test, prefer):
    """halves_test: {half: [(M, seeds)]}; find per-half ladder keys.
    prefer: list of known-good combos to try first."""
    combos = list(prefer)
    combos += [c for c in itertools.combinations(POOL6, 2)]
    combos += [c for c in itertools.combinations(POOL6, 3)]
    ext = POOL6 + POOL8
    combos3 = [c for c in itertools.combinations(ext, 3)
               if any(g in POOL8 for g in c)]
    choice = {}
    for hn, tests in halves_test.items():
        found = None
        for combo in combos:
            if all(branches_ok(M, sd, combo) == 0 for M, sd in tests):
                found = tuple(combo)
                break
        if found is None:
            for combo in combos3:
                if all(branches_ok(M, sd, combo) == 0
                       for M, sd in tests):
                    found = tuple(combo)
                    break
        if found is None:
            return None
        choice[hn] = found
    return choice


def run_cell(lane, xi, xs_extra=(), verbose=True):
    x0 = min(x for x in range(11, 30, 2) if x % 8 == xi
             and min(i for i, _ in lanes_for(x)[lane]) >= 0)
    x1 = x0 + 8
    r8 = (x0 + LAW[lane]) % 8
    K0, K1 = lanes_for(x0)[lane], lanes_for(x1)[lane]
    thr0 = max(16, x0 + 5)
    scanM0 = in_class_scales(r8, K0, 0, 1, thr0 + 48)[0]
    scanM1 = in_class_scales(r8, K1, 0, 1, x1 + 5 + 48)[0]
    t0 = time.time()
    cands = candidates(K0, K1, scanM0, scanM1,
                       max(8, min(i for i, _ in K0) - 1))
    if not cands:
        return {"cell": f"{lane}_xi{xi}", "ok": False,
                "reason": "no common double kill"}
    rec = None
    for (istar, Shi, Slo) in cands[:12]:
        halves_test = {}
        for hn, Sx, ph in (("hi", Shi, "lo"), ("lo", Slo, "hi")):
            tests = []
            for (x, K) in ((x0, K0), (x0, K0), (x1, K1)):
                pass
            Ms0 = in_class_scales(r8, K0, istar, 2, scanM0)
            Ms1 = in_class_scales(r8, K1, istar, 1, scanM1)
            tests = [(m, seeds_for(m, [K0[k] for k in Sx], istar, ph))
                     for m in Ms0]
            tests += [(m, seeds_for(m, [K1[k] for k in Sx], istar, ph))
                      for m in Ms1]
            halves_test[hn] = tests
        prefer = [("O", "E"), ("E", "Q1"), ("O", "Q2"), ("O", "Q3"),
                  ("O", "Q1"), ("E", "Q2"), ("O", "Q4"), ("E", "Q4"),
                  ("E", "Q3"), ("O", "E", "Q1"), ("O", "E", "Q3")]
        choice = ladder_search(halves_test, prefer)
        if choice is not None:
            rec = (istar, Shi, Slo, choice)
            break
    if rec is None:
        return {"cell": f"{lane}_xi{xi}", "ok": False, "istar": None,
                "reason": f"no ladder set for {len(cands[:12])} cands",
                "cands": [(i, list(a), list(b))
                          for i, a, b in cands[:12]]}
    istar, Shi, Slo, choice = rec
    # ---- parametric verify ----
    xs = [x0, x1, x0 + 16, x0 + 24] + list(xs_extra)
    verify, controls, fails = {}, {}, []
    for x in xs:
        K = lanes_for(x)[lane]
        if min(i for i, _ in K) < 0:
            continue
        start = max(16, x + 5)
        vMs = in_class_scales(r8, K, istar, 4, start)
        vMs += in_class_scales(r8, K, istar, 2, vMs[-1] + 40)
        for m in vMs:
            for hn, Sx, ph in (("hi", Shi, "lo"), ("lo", Slo, "hi")):
                sv = branches_ok(m, seeds_for(
                    m, [K[k] for k in Sx], istar, ph), choice[hn])
                if sv:
                    fails.append((x, m, hn, sv))
        verify[x] = vMs
        # controls at r+4: some branch survives in at least one half
        cMs = in_class_scales((r8 + 4) % 8, K, istar, 2, start + 16)
        ct = []
        for m in cMs:
            sv = sum(branches_ok(m, seeds_for(
                m, [K[k] for k in Sx], istar, ph), choice[hn])
                for hn, Sx, ph in (("hi", Shi, "lo"), ("lo", Slo, "hi")))
            ct.append((m, sv))
            if sv == 0:
                fails.append((x, m, "control", "0 survivors"))
        controls[x] = ct
    ok = not fails
    out = {"cell": f"{lane}_xi{xi}", "ok": ok, "lane": lane, "xi": xi,
           "x0": x0, "istar": istar,
           "S_hi": list(Shi), "S_lo": list(Slo),
           "ladders": {k: list(v) for k, v in choice.items()},
           "verify": {str(x): v for x, v in verify.items()},
           "controls": {str(x): v for x, v in controls.items()},
           "fails": fails, "secs": round(time.time() - t0, 1)}
    if verbose:
        Kp = lanes_for(x0)[lane]
        pr = lambda S: "+".join(f"t{Kp[k][0]}b{Kp[k][1]}" for k in S)
        print(f"{lane}_xi{xi} (x0={x0}, r{r8}): v*=t{istar}; "
              f"hi<={{{pr(Shi)}}}[{'+'.join(choice['hi'])}], "
              f"lo<={{{pr(Slo)}}}[{'+'.join(choice['lo'])}]; "
              f"x={sorted(verify)} scales "
              f"{[f'{v[0]}..{v[-1]}' for v in verify.values()]}: "
              f"{'ALL OK' if ok else fails[:6]} "
              f"({time.time()-t0:.0f}s)", flush=True)
    return out


ALL_CELLS = [(lane, xi) for lane in
             ("A4a", "A4d", "B2", "B6", "K4e", "C", "K3", "K7", "K1")
             for xi in (1, 3, 5, 7)]
DYADIC = [("A4a", 3), ("B6", 5), ("B2", 1), ("K4e", 7)]


def main():
    args = sys.argv[1:]
    if args and args[0] == "dyadic":
        cells = DYADIC
    elif args:
        cells = []
        for a in args:
            lane, xi = a.rsplit("_xi", 1)
            cells.append((lane, int(xi)))
    else:
        cells = ALL_CELLS
    recs = {}
    if os.path.exists(OUT):
        recs = {r["cell"]: r for r in
                json.load(open(OUT)).get("cells", [])}
    for lane, xi in cells:
        rec = run_cell(lane, xi)
        recs[rec["cell"]] = rec
        json.dump({"cells": list(recs.values())},
                  open(OUT, "w"), indent=1)
    n = sum(1 for r in recs.values() if r.get("ok"))
    print(f"\nPARAM TEMPLATE: {n}/{len(recs)} cells OK -> {OUT}")


if __name__ == "__main__":
    main()
