"""e180_diag_grow: FRONT N2-DIAG + N3-GROW machine layer (notes/78).

Part 1 (N2-DIAG, companions to the notes/78 affine write-up):

  partMINM: the exact applicability boundary of the affine schema.
    For every odd p = 5..21, scan the e123 checkers (check_layer1,
    check_flip -- the strict rung-by-rung schema executors) over ALL
    small scales of their classes and record the pass/fail boundary.
    Claim under test (notes/78 SS I.5): L1(p) verifies at every
    M = 0 mod 4 with M >= 2p+10, FLIP(p) at every M of the flip class
    M/2 = p+3 mod 4 with M >= 2p+14 -- affine-in-p boundaries, no
    hidden constant.  (Below the boundary the checker may pass or
    fail depending on value collisions; we record that zone verbatim.)

  partXVAL: independent-solver cross-validation at FRESH p = 17, 21
    (e123b encoder verbatim: complete AP + transitivity encoding,
    Cadical195): C3(p) UNSAT on the flip class, SAT on the
    complementary class, full rung UNSAT on both, at 4 small scales
    per class per p plus M = 256/260.

Part 2 (N3-GROW, two FRESH (x, C) points of the growth law
d*(x) = floor((x-1)/4)):

  partK19: pair {19,20} at M = 80 -- atmost-3 punctures ANYWHERE
    UNSAT (C = 3 = d*-1), atmost-4 SAT (d*(19) = 4), witness audited
    + checked against the lane L(19) = {(t15,b2),(t11,b4),(t7,b6),
    (t3,b8)} (transversal = one endpoint per unit).
  partK23: pair {23,24} at M = 112 (fresh x AND fresh scale for this
    part) -- atmost-4 UNSAT (C = 4 = d*-1), atmost-5 SAT
    (d*(23) = 5), lane L(23) = {(t19,b2),(t15,b4),(t11,b6),(t7,b8),
    (t3,b10)}.

Run: .venv/bin/python experiments/e180_diag_grow.py [partMINM|partXVAL|partK19|partK23|all]
Artifacts: data/e180_diag_grow.json (+ .log via tee)
"""
import importlib
import json
import os
import sys
from pathlib import Path
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments"))

e123 = importlib.import_module("e123_diagonal_schema")
e123b = importlib.import_module("e123b_diagonal_solver_xval")
e174 = importlib.import_module("e174_n3_growth")

BASE = str(ROOT / "data")
OUT = {}


def dump():
    path = f"{BASE}/e180_diag_grow.json"
    try:
        old = json.load(open(path))
    except Exception:
        old = {}
    old.update(OUT)
    json.dump(old, open(path, "w"), indent=1)


# ---------------------------------------------------------------- partMINM
def partMINM(ps=range(5, 22, 2), key="partMINM"):
    """ORIGINAL boundary scan (kept for the historical record).

    KNOWN DISCREPANCY (external review item 9, remediated by
    partMINMsharp below): this part asserts only the SLACK bounds
    2p+10 / 2p+14, while the notes/78 SS I.5 prose claims the sharp
    boundaries p+7 (first 4 | M >= p+7) / 2p+6.  Use partMINMsharp
    for the audit that actually certifies the prose."""
    rows = {}
    ok_all = True
    for p in ps:
        l1_pass, l1_fail = [], []
        for M in range(8, 4 * p + 44, 4):
            try:
                e123.check_layer1(M, p)
                l1_pass.append(M)
            except Exception:
                l1_fail.append(M)
        fl_pass, fl_fail = [], []
        flip_res = (2 * (p + 3)) % 8
        for M in range(16, 4 * p + 88, 4):
            if M % 8 != flip_res:
                continue
            try:
                e123.check_flip(M, p)
                fl_pass.append(M)
            except Exception:
                fl_fail.append(M)
        bl1, bfl = 2 * p + 10, 2 * p + 14
        l1_ok = all(M in l1_pass for M in range(bl1, 4 * p + 44, 4))
        fl_ok = all(M in fl_pass
                    for M in range(16, 4 * p + 88, 4)
                    if M % 8 == flip_res and M >= bfl)
        ok_all &= l1_ok and fl_ok
        rows[p] = {
            "l1_bound_claim": bl1, "l1_ok_from_bound": l1_ok,
            "l1_below_bound_pass": [M for M in l1_pass if M < bl1],
            "l1_below_bound_fail": [M for M in l1_fail if M < bl1],
            "flip_bound_claim": bfl, "flip_ok_from_bound": fl_ok,
            "flip_below_bound_pass": [M for M in fl_pass if M < bfl],
            "flip_below_bound_fail": [M for M in fl_fail if M < bfl]}
        print(f"[MINM] p={p}: L1 from {bl1} "
              f"{'ALL PASS' if l1_ok else 'FAIL!'}"
              f" (below: pass {rows[p]['l1_below_bound_pass']},"
              f" fail {rows[p]['l1_below_bound_fail']});"
              f" FLIP from {bfl} {'ALL PASS' if fl_ok else 'FAIL!'}"
              f" (below: pass {rows[p]['flip_below_bound_pass']},"
              f" fail {rows[p]['flip_below_bound_fail']})", flush=True)
    OUT[key] = {"rows": rows, "boundaries_hold": ok_all}
    dump()
    assert ok_all, "affine boundary claim violated"


# ------------------------------------------------------------ partMINMsharp
def partMINMsharp(ps=(5, 13, 21), key="partMINM_sharp"):
    """Review-item-9 remediation (notes/88 item 6): audit the SHARP
    affine boundaries the notes/78 prose actually claims.

      L1(p):   passes at every 4 | M >= p+7, i.e. from
               sharp_l1 = first multiple of 4 >= p+7; every scanned
               4 | M BELOW sharp_l1 must FAIL (explicit check).
      FLIP(p): passes at every in-class M >= 2p+6 (class
               M = 2(p+3) mod 8; 2p+6 is in class); every scanned
               in-class M BELOW 2p+6 must FAIL (explicit check;
               vacuous when no in-class scale < 2p+6 is scanned,
               recorded as such).

    first_l1 / first_flip are COMPUTED from the scan (smallest
    scanned scale from which every later scanned scale passes) and
    ASSERTED equal to the sharp values."""
    rows = {}
    ok_all = True
    for p in ps:
        # ---- L1 scan: all multiples of 4 in [8, 4p+40]
        l1 = {}
        for M in range(8, 4 * p + 44, 4):
            try:
                e123.check_layer1(M, p)
                l1[M] = True
            except Exception:
                l1[M] = False
        scanned = sorted(l1)
        sharp_l1 = ((p + 7 + 3) // 4) * 4
        passing_suffix = [M for M in scanned
                          if all(l1[M2] for M2 in scanned if M2 >= M)]
        first_l1 = min(passing_suffix) if passing_suffix else None
        l1_first_ok = first_l1 == sharp_l1
        l1_below = [M for M in scanned if M < sharp_l1]
        l1_below_all_fail = all(not l1[M] for M in l1_below)
        # ---- FLIP scan: in-class M in [8, 4p+84]
        flip_res = (2 * (p + 3)) % 8
        sharp_fl = 2 * p + 6
        assert sharp_fl % 8 == flip_res, (p, sharp_fl, flip_res)
        fl = {}
        for M in range(8, 4 * p + 88, 4):
            if M % 8 != flip_res:
                continue
            try:
                e123.check_flip(M, p)
                fl[M] = True
            except Exception:
                fl[M] = False
        fscanned = sorted(fl)
        fsuffix = [M for M in fscanned
                   if all(fl[M2] for M2 in fscanned if M2 >= M)]
        first_fl = min(fsuffix) if fsuffix else None
        fl_first_ok = first_fl == sharp_fl
        fl_below = [M for M in fscanned if M < sharp_fl]
        fl_below_all_fail = all(not fl[M] for M in fl_below)
        ok = (l1_first_ok and l1_below_all_fail
              and fl_first_ok and fl_below_all_fail)
        ok_all &= ok
        rows[p] = {
            "sharp_l1": sharp_l1, "first_l1": first_l1,
            "l1_first_ok": l1_first_ok,
            "l1_below_sharp": l1_below,
            "l1_below_all_fail": l1_below_all_fail,
            "sharp_flip": sharp_fl, "first_flip": first_fl,
            "flip_first_ok": fl_first_ok,
            "flip_below_sharp": fl_below,
            "flip_below_all_fail": fl_below_all_fail,
            "flip_below_vacuous": not fl_below}
        print(f"[MINMsharp] p={p}: L1 first-pass {first_l1} "
              f"(sharp {sharp_l1}, {'OK' if l1_first_ok else 'MISMATCH'}), "
              f"below {l1_below} all-fail={l1_below_all_fail}; "
              f"FLIP first-pass {first_fl} (sharp {sharp_fl}, "
              f"{'OK' if fl_first_ok else 'MISMATCH'}), below {fl_below} "
              f"all-fail={fl_below_all_fail}"
              f"{' (vacuous)' if not fl_below else ''}", flush=True)
    OUT[key] = {"rows": rows, "sharp_boundaries_hold": ok_all,
                "ps": list(ps)}
    dump()
    assert ok_all, "SHARP boundary claim violated"


# ---------------------------------------------------------------- partXVAL
def partXVAL():
    out = {"rows": [], "fail": []}
    for p in (17, 21):
        x = 3 * p
        core = [(p, p), (p - 2, p + 1), (p + 5, p - 2)]
        rung = [(a - 2 * j, j) for a in (x, x + 1)
                for j in range(1, a // 2 + 1)]
        flip_mod8 = (2 * (p + 3)) % 8
        comp_mod8 = (2 * (p + 1)) % 8
        base = ((4 * p + 15) // 16) * 16
        flip_ms = [M for M in range(base, base + 130, 4)
                   if M % 8 == flip_mod8][:4] + \
                  [M for M in (256, 260) if M % 8 == flip_mod8]
        comp_ms = [M for M in range(base, base + 130, 4)
                   if M % 8 == comp_mod8][:4] + \
                  [M for M in (256, 260) if M % 8 == comp_mod8]
        for M in sorted(set(flip_ms + comp_ms)):
            t0 = time.time()
            sol, sel = e123b.build_base(M, set(core) | set(rung))
            v_core = sol.solve(assumptions=[sel[u] for u in core])
            v_rung = sol.solve(assumptions=[sel[u] for u in rung])
            sol.delete()
            cls = "flip" if M % 8 == flip_mod8 else "comp"
            exp_core = "SAT" if cls == "comp" else "UNSAT"
            got_core = "SAT" if v_core else "UNSAT"
            got_rung = "SAT" if v_rung else "UNSAT"
            row = {"p": p, "x": x, "M": M, "class": cls,
                   "core": got_core, "core_expected": exp_core,
                   "rung": got_rung, "t": round(time.time() - t0, 1)}
            out["rows"].append(row)
            ok = got_core == exp_core and got_rung == "UNSAT"
            if not ok:
                out["fail"].append(row)
            print(f"[XVAL] p={p} M={M} ({cls}, M%8={M % 8}): C3(p) "
                  f"{got_core} (exp {exp_core}), rung {got_rung} "
                  f"(exp UNSAT) [{'OK' if ok else 'MISMATCH'}, "
                  f"{row['t']}s]", flush=True)
            OUT["partXVAL"] = out
            dump()
    assert not out["fail"], out["fail"]


# ---------------------------------------------------------------- partK
def lane(M, x):
    """Even-j units of the odd attacker x: the parity-split violation
    set (notes/74 SS I.6 / notes/78 SS II)."""
    assert x % 2 == 1
    return [(2 * M - (x - 2 * j), M + j)
            for j in range(2, (x - 1) // 2 + 1, 2)]


def partK(x, M, dstar):
    from pysat.card import CardEnc, EncType
    from pysat.formula import IDPool

    from pysat.solvers import Cadical195
    ln = lane(M, x)
    assert len(ln) == (x - 1) // 4 == dstar
    g = e174.Gadget(M, x)
    # lane units must be a sub-family of the rung with disjoint supports
    sup = [v for u in ln for v in u]
    assert all(u in g.units for u in ln) and len(set(sup)) == 2 * dstar
    pool = IDPool(start_from=g.top + 10)
    neg = [-g.sel[v] for v in g.vals]
    row = {}
    for k in (dstar - 1, dstar):
        t0 = time.time()
        card = CardEnc.atmost(lits=neg, bound=k, vpool=pool,
                              encoding=EncType.seqcounter)
        sol = Cadical195(bootstrap_with=g.clauses + card.clauses)
        sol.conf_budget(60_000_000)
        r = sol.solve_limited()
        exp = "UNSAT" if k < dstar else "SAT"
        if r is True:
            model = set(l for l in sol.get_model() if l > 0)
            P = [v for v in g.vals if g.sel[v] not in model]
            assert g.query(P), "cardinality witness failed re-query"
            hit = [u for u in ln if set(u) & set(P)]
            row[k] = {"verdict": "SAT",
                      "escape": [e174.offset(v, M) for v in sorted(P)],
                      "lane_units_hit": f"{len(hit)}/{dstar}",
                      "secs": round(time.time() - t0, 1)}
        elif r is False:
            row[k] = {"verdict": "UNSAT",
                      "secs": round(time.time() - t0, 1)}
        else:
            row[k] = {"verdict": "UNKNOWN (budget)",
                      "secs": round(time.time() - t0, 1)}
        sol.delete()
        ok = row[k]["verdict"] == exp
        row[k]["expected"] = exp
        print(f"[K{x}] x={x} M={M} atmost-{k} punctures: {row[k]}"
              f" [{'OK' if ok else 'MISMATCH'}]", flush=True)
        OUT[f"partK{x}_M{M}"] = row
        dump()
    g.delete()
    assert row[dstar - 1]["verdict"] == "UNSAT", (x, M, row)
    assert row[dstar]["verdict"] == "SAT", (x, M, row)


PARTS = {"partMINM": partMINM, "partXVAL": partXVAL,
         "partMINMsharp": partMINMsharp,
         "partMINMsharpfull": lambda: partMINMsharp(
             ps=tuple(range(5, 22, 2)), key="partMINM_sharp_full"),
         "partK19": lambda: partK(19, 80, 4),
         "partK23": lambda: partK(23, 112, 5)}

if __name__ == "__main__":
    want = sys.argv[1:] or ["all"]
    names = list(PARTS) if want == ["all"] else want
    t0 = time.time()
    for nm in names:
        PARTS[nm]()
    print(f"total {time.time() - t0:.0f}s -> {BASE}/e180_diag_grow.json",
          flush=True)
