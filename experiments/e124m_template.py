"""e124m_template: FRONT N2-OFF step 6 -- the uniform two-ladder
template, tested mechanically across even-class lane cells.

TEMPLATE (per cell = (pair core K, residue class r mod 8)):
  1. PHASE SCAN (solver, small M in class): find a value v* and two
     half premise-sets S_lo, S_hi <= K with AP + S_hi + (v* < m0)
     UNSAT and AP + S_lo + (m0 < v*) UNSAT.  [Kill names: S_hi forces
     the hi phase... i.e. S_hi kills v*-lo.]
  2. LADDER SEARCH (closure, 2 scales): find ONE ladder pair from the
     pool {O, E, Q1..Q4} closing all 4 polarity branches of BOTH
     halves at both scales.
  3. VERIFY (closure, 8+ scales in class): all branches close at every
     scale; CONTROLS at the complementary class r+4: some branch
     survives (where the core is SAT there -- checked by solver).

Cells: the lane instances with even-class laws from e124b, including
the alternative dyadic (0 mod 8) cores for pairs {13,14}, {17,18},
{19,20}, {21,22}.

Run: .venv/bin/python experiments/e124m_template.py
Output: data/e124m_template.json
"""
import itertools
import json
import time

from e124c_k4_anatomy import build
from e124e_closure_halves import closure
from e124g_branch_closure import ladder, fiat_edges
from e124i_k4_schema_verify import solver_check

BASE = "/Users/will/Dev/personal/tasks/math/erdos197/data"

# (name, x, units, residue mod 8, first M to use)
CELLS = [
    # K11_r4: the e122 catalogue law is "M = 4 mod 8, M >= 61" -- the
    # cell genuinely starts late; scan/verify from 68.
    ("K11_r4", 11, [(0, 6), (3, 4), (6, 3)], 4, 68),
    ("B6(11)_r6", 11, [(3, 4), (5, 3), (10, 1)], 6, 22),
    ("B2(13)_r4", 13, [(4, 5), (7, 3), (9, 2)], 4, 28),
    ("B6(13)_r0", 13, [(5, 4), (7, 3), (12, 1)], 0, 24),
    ("B6(15)_r2", 15, [(7, 4), (9, 3), (14, 1)], 2, 26),
    ("B2(17)_r0", 17, [(8, 5), (11, 3), (13, 2)], 0, 24),
    ("B2(19)_r2", 19, [(10, 5), (13, 3), (15, 2)], 2, 34),
    ("A4d(19)_r0", 19, [(9, 5), (10, 5), (11, 4), (14, 3)], 0, 32),
    ("B6(21)_r0", 21, [(13, 4), (15, 3), (20, 1)], 0, 32),
    ("A4d(13)_r2", 13, [(3, 5), (4, 5), (5, 4), (8, 3)], 2, 26),
]


def phase_kills(M, K, v_is):
    """-> {(i, side): [minimal kill subsets]}"""
    sol, sel, phase, o = build(M, K)
    out = {}
    m0 = 3 * M // 2
    for i in v_is:
        tv = 2 * M - i
        if tv == m0:
            continue
        for ph in ("lo", "hi"):
            mins = []
            for sz in range(1, len(K) + 1):
                for S in itertools.combinations(K, sz):
                    if any(set(m) <= set(S) for m in mins):
                        continue
                    if not sol.solve(assumptions=[sel[u] for u in S]
                                     + [phase[(tv, ph)]]):
                        mins.append(S)
            if mins:
                out[(i, ph)] = mins
    sol.delete()
    return out


def branches_ok(M, seeds, lkeys):
    pool = {"O": (M + 1, 2, 2 * M - 1), "E": (M + 2, 2, 2 * M),
            "Q1": (M + 1, 4, 2 * M), "Q3": (M + 3, 4, 2 * M),
            "Q2": (M + 2, 4, 2 * M), "Q4": (M + 4, 4, 2 * M)}
    lads = [ladder(*pool[k]) for k in lkeys]
    surv = 0
    for pol in itertools.product((True, False), repeat=len(lads)):
        ed = set(seeds)
        for lad, lf in zip(lads, pol):
            ed |= fiat_edges(lad, lf)
        if closure(M, ed)[0] != "contradiction":
            surv += 1
    return surv


def seeds_for(M, S, phase_pair):
    i, ph = phase_pair
    m0 = 3 * M // 2
    tv = 2 * M - i
    ed = {(2 * M - a, M + b) for (a, b) in S}
    ed.add((tv, m0) if ph == "lo" else (m0, tv))
    return ed


def degenerate(M, K):
    """A unit's t-value coincides with m0 (or two unit values clash)."""
    m0 = 3 * M // 2
    vals = [2 * M - i for i, _ in K] + [M + j for _, j in K]
    return m0 in vals or len(set(vals)) < len(vals)


def in_class_scales(M0, K, n, start_at=None):
    out = []
    m = start_at if start_at is not None else M0
    while len(out) < n:
        if not degenerate(m, K):
            out.append(m)
        m += 8
    return out


def main():
    import sys
    only = set(sys.argv[1:])
    out = {"cells": []}
    t00 = time.time()
    for name, x, K, r, M0 in CELLS:
        if only and name not in only:
            continue
        scan_M = in_class_scales(M0, K, 1, start_at=M0 + 32)[0]
        kills = phase_kills(scan_M, K, list(range(0, max(i for i, _ in K)
                                                  + 3)))
        # double-killed phase values, smallest total premise size
        best = None
        for i in sorted({i for (i, _) in kills}):
            if (i, "lo") in kills and (i, "hi") in kills:
                for Slo in kills[(i, "hi")]:      # kills lo?? naming:
                    pass
        # naming: kills[(i,'lo')] = subsets S with AP+S+(t_i lo) UNSAT
        #   == S forces hi.  For the clash we need one S forcing hi and
        #   one forcing lo: S_hi in kills[(i,'lo')], S_lo in
        #   kills[(i,'hi')].
        for i in sorted({i for (i, _) in kills}):
            if (i, "lo") in kills and (i, "hi") in kills:
                for S_hi in kills[(i, "lo")]:
                    for S_lo in kills[(i, "hi")]:
                        sz = len(S_hi) + len(S_lo)
                        if best is None or sz < best[3]:
                            best = (i, S_hi, S_lo, sz)
        if best is None:
            print(f"{name}: NO double phase kill -- template fails",
                  flush=True)
            out["cells"].append({"cell": name, "ok": False,
                                 "reason": "no double kill"})
            continue
        i, S_hi, S_lo, _ = best
        # HALF-hi: S_hi + (t_i lo) must close;  HALF-lo: S_lo + (t_i hi)
        halves = [("hi", S_hi, (i, "lo")), ("lo", S_lo, (i, "hi"))]
        # ladder search at spread scales (small scales close
        # accidentally -- the K4 lesson from e124g at M = 24 -- but a
        # pair chosen ONLY at large scales can fail at a small one:
        # the B6(13) M=40 lesson)
        testMs = [in_class_scales(M0, K, 1, start_at=M0 + 8)[0]] + \
            in_class_scales(M0, K, 2, start_at=M0 + 32)
        choice = {}
        for hn, S, pp in halves:
            found = None
            for sz in (2, 3):
                for combo in itertools.combinations(
                        ("O", "E", "Q1", "Q3", "Q2", "Q4"), sz):
                    if all(branches_ok(m, seeds_for(m, S, pp),
                                       combo) == 0 for m in testMs):
                        found = combo
                        break
                if found:
                    break
            choice[hn] = found
        if None in choice.values():
            print(f"{name}: v*=t{i}, halves {S_hi}/{S_lo}: no 2-ladder "
                  f"set closes -- template fails", flush=True)
            out["cells"].append({"cell": name, "ok": False, "vstar": i,
                                 "reason": "no ladder pair"})
            continue
        # verify at 8 scales + 4 controls
        vMs = in_class_scales(M0, K, 8)
        cMs = in_class_scales(M0 + 4, K, 4)
        fails = []
        for m in vMs:
            for hn, S, pp in halves:
                sv = branches_ok(m, seeds_for(m, S, pp), choice[hn])
                if sv:
                    fails.append((m, hn, sv))
            if m <= 80 and not solver_check(m, K, expect_unsat=True):
                fails.append((m, "solver", "expected UNSAT"))
        ctrl = []
        for m in cMs:
            sv = sum(branches_ok(m, seeds_for(m, S, pp), choice[hn])
                     for hn, S, pp in halves)
            sat = solver_check(m, K, expect_unsat=False) if m <= 80 \
                else None
            ctrl.append((m, sv, sat))
            if sat is False:
                fails.append((m, "control", "expected SAT"))
        ok = not fails
        pr_hi = "+".join(f"t{a}b{b}" for a, b in S_hi)
        pr_lo = "+".join(f"t{a}b{b}" for a, b in S_lo)
        print(f"{name} (x={x}, r={r}): v*=t{i}; hi<={{{pr_hi}}} "
              f"[{'+'.join(choice['hi'])}], lo<={{{pr_lo}}} "
              f"[{'+'.join(choice['lo'])}]; verified {len(vMs)} scales "
              f"{vMs[0]}..{vMs[-1]}: {'ALL OK' if ok else fails}; "
              f"controls {[(m, s) for m, s, _ in ctrl]} "
              f"({time.time()-t00:.0f}s)", flush=True)
        out["cells"].append({
            "cell": name, "ok": ok, "vstar": i,
            "S_hi": [list(u) for u in S_hi],
            "S_lo": [list(u) for u in S_lo],
            "ladders": {k: list(v) for k, v in choice.items()},
            "verified_Ms": vMs, "controls": ctrl, "fails": fails})
    path = f"{BASE}/e124m_template.json" if not only else \
        f"{BASE}/e124m_template_rerun.json"
    json.dump(out, open(path, "w"), indent=1)
    n = sum(1 for c in out["cells"] if c["ok"])
    print(f"\nTEMPLATE: {n}/{len(out['cells'])} cells closed -> {path}")


if __name__ == "__main__":
    main()
