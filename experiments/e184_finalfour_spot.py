"""e184_finalfour_spot: FINAL-FOUR adjudication spot-checks (notes/80).

One reconstruction + one fresh scale per species write-up:

  partC3SCHEMA : Theorem C3(p) — strict schema executor (e123 checkers,
     unchanged) at FRESH p = 23, 25 (both mod-4 classes beyond every
     earlier run; pmax was 21).  Full e123 grid per p: 104 layer-1
     scales, 52 flip, 52 sharpness.
  partC3XVAL   : independent complete-encoding Cadical195 solver
     cross-validation (e123b encoder verbatim) at p = 23, 25:
     C3(p) UNSAT on the flip class / SAT on the complement, full rung
     UNSAT on both, 4 scales per class per p + 256/260.
  partK19M112  : N3-GROW law at a FRESH (x, M) cell: x = 19, M = 112
     (x=19 was measured only at M=80).  atmost-3 punctures ANYWHERE
     UNSAT, atmost-4 SAT — d*(19; 112) = 4 = floor(18/4).
  partPS       : Lemma PS(x) halving identities as EXACT set equalities
     at FRESH x = 29, 31 (beyond the recorded x <= 27), M = 96/160;
     plus Lemma LANE(x) count+disjointness numerically for all odd
     x in [11, 99], M in {2x+4, 4x}.
  partS5       : independent verification of the S5 dodger witnesses
     (fresh checker, no CP-SAT, no reuse of the e179 encoding):
     axes (ii)/(iii)/split floors re-checked from the raw coloring,
     orbit chain depth census at F = 12/64/128 (exhaustive DFS),
     window sup-density, minority anatomy characterization.
  partS5CORE   : fresh-encoder (Glucose42, independent clause
     construction) double-block-order pay-check: witness coloring
     FIXED on (m, 8m], both teams block-ordered at both seams,
     per-team AP-freeness -> expect UNSAT at m = 16, 32 (they PAY).

Run: .venv/bin/python experiments/e184_finalfour_spot.py [part ...|all]
Artifacts: data/e184_finalfour.json (+ tee log data/e184_finalfour.log)
"""
import importlib
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
BASE = os.path.join(os.path.dirname(HERE), "data")

OUT = {}


def dump():
    path = os.path.join(BASE, "e184_finalfour.json")
    try:
        old = json.load(open(path))
    except Exception:
        old = {}
    old.update(OUT)
    json.dump(old, open(path, "w"), indent=1)


def log(msg):
    print(msg, flush=True)
    with open(os.path.join(BASE, "e184_finalfour.log"), "a") as f:
        f.write(msg + "\n")


# ------------------------------------------------------------ partC3SCHEMA
def partC3SCHEMA():
    e123 = importlib.import_module("e123_diagonal_schema")
    rows = []
    fails = []
    for p in (23, 25):
        flip_res = (2 * (p + 3)) % 8
        l1_scales = [M for M in list(range(4 * p, 4 * p + 400, 4))
                     + [512, 516, 1024, 1028] if M % 4 == 0]
        fl_scales = [M for M in l1_scales if (M // 2) % 4 == (p + 3) % 4]
        sh_scales = [M for M in l1_scales if (M // 2) % 4 == (p + 1) % 4]
        okL = okF = okS = 0
        t0 = time.time()
        for M in l1_scales:
            try:
                e123.check_layer1(M, p)
                okL += 1
            except AssertionError as ex:
                fails.append(["layer1", p, M, repr(ex.args[:2])])
        for M in fl_scales:
            try:
                e123.check_flip(M, p)
                okF += 1
            except AssertionError as ex:
                fails.append(["flip", p, M, repr(ex.args[:2])])
        for M in sh_scales:
            try:
                e123.sharpness(M, p)
                okS += 1
            except AssertionError as ex:
                fails.append(["sharp", p, M, repr(ex.args[:2])])
        row = {"p": p, "pair": [3 * p, 3 * p + 1],
               "flip_class_mod8": flip_res,
               "layer1": f"{okL}/{len(l1_scales)}",
               "flip": f"{okF}/{len(fl_scales)}",
               "sharp": f"{okS}/{len(sh_scales)}",
               "secs": round(time.time() - t0, 1)}
        rows.append(row)
        log(f"[C3SCHEMA] p={p} pair {{{3*p},{3*p+1}}} flip M%8={flip_res}: "
            f"layer1 {row['layer1']}, flip {row['flip']}, "
            f"sharp {row['sharp']} [{row['secs']}s]")
    OUT["partC3SCHEMA"] = {"rows": rows, "fail": fails}
    dump()
    assert not fails, fails[:5]


# ------------------------------------------------------------- partC3XVAL
def partC3XVAL():
    e123b = importlib.import_module("e123b_diagonal_solver_xval")
    out = {"rows": [], "fail": []}
    for p in (23, 25):
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
            row = {"p": p, "M": M, "class": cls, "core": got_core,
                   "core_expected": exp_core, "rung": got_rung,
                   "t": round(time.time() - t0, 1)}
            out["rows"].append(row)
            ok = got_core == exp_core and got_rung == "UNSAT"
            if not ok:
                out["fail"].append(row)
            log(f"[C3XVAL] p={p} M={M} ({cls}): C3(p) {got_core} "
                f"(exp {exp_core}), rung {got_rung} (exp UNSAT) "
                f"[{'OK' if ok else 'MISMATCH'}, {row['t']}s]")
            OUT["partC3XVAL"] = out
            dump()
    assert not out["fail"], out["fail"]


# ------------------------------------------------------------ partK19M112
def partK19M112():
    e180 = importlib.import_module("e180_diag_grow")
    e180.partK(19, 112, 4)
    # e180 writes its own JSON; mirror the row here
    d = json.load(open(os.path.join(BASE, "e180_diag_grow.json")))
    OUT["partK19M112"] = d.get("partK19_M112")
    dump()


# ----------------------------------------------------------------- partPS
def units_of(M, a):
    """Attack units (t_{a-2j}, b_j) of attacker a on (M, 2M], as value
    pairs (2M-(a-2j), M+j)."""
    out = set()
    for j in range(1, a // 2 + 1):
        i = a - 2 * j
        if 0 <= i <= M - 1:
            out.add((2 * M - i, M + j))
    return out


def partPS():
    rows = []
    for x in (29, 31):
        y = (x + 1) // 2
        for M in (96, 160):
            m = M // 2
            # even class: attacker x+1 units with both endpoints even
            ev = {(t, b) for (t, b) in units_of(M, x + 1)
                  if t % 2 == 0 and b % 2 == 0}
            ev_h = {(t // 2, b // 2) for (t, b) in ev}
            # odd class: attacker x units with both endpoints odd
            od = {(t, b) for (t, b) in units_of(M, x)
                  if t % 2 == 1 and b % 2 == 1}
            od_h = {((t + 1) // 2, (b + 1) // 2) for (t, b) in od}
            sa = units_of(m, y)
            ok = (ev_h == sa) and (od_h == sa)
            rows.append({"x": x, "M": M, "y": y,
                         "even==SA": ev_h == sa, "odd==SA": od_h == sa,
                         "n_units": len(sa)})
            log(f"[PS] x={x} M={M}: h_E(evens)==SA({y};{m}): {ev_h == sa}; "
                f"h_O(odds)==SA({y};{m}): {od_h == sa} ({len(sa)} units)")
            assert ok, (x, M)
    # LANE: count + support disjointness, all odd x in [11,99]
    lane_ok = True
    for x in range(11, 100, 2):
        for M in (2 * x + 4, 4 * x):
            ln = [(2 * M - (x - 2 * j), M + j)
                  for j in range(2, (x - 1) // 2 + 1, 2)]
            sup = [v for u in ln for v in u]
            if not (len(ln) == (x - 1) // 4 and len(set(sup)) == 2 * len(ln)):
                lane_ok = False
                log(f"[LANE] VIOLATION at x={x} M={M}")
    log(f"[LANE] count+disjointness for odd x in [11,99], M in "
        f"{{2x+4, 4x}}: {'ALL OK' if lane_ok else 'FAIL'}")
    OUT["partPS"] = {"rows": rows, "lane_ok": lane_ok}
    dump()
    assert lane_ok


# ----------------------------------------------------------------- partS5
def load_witness(path):
    d = json.load(open(path))
    hor = d["hor"]
    A = set(d["A"])
    B = set(range(1, hor + 1)) - A
    return hor, A, B, d


def chain_depth(team, hor, F, u0):
    """Max depth over in-team doubling chains v -> 2v - f (f <= F,
    f in team, 2v - f in team, seed v > u0).  Iterative DP on DAG
    (edges strictly increase value since 2v - f > v iff f < v)."""
    tv = sorted(team)
    depth = {v: 0 for v in tv}
    best = 0
    for v in tv:                       # increasing order: DP is exact
        dv = depth[v]
        base_ok = v > u0
        for f in range(1, F + 1):
            if f not in team:
                continue
            w = 2 * v - f
            if w <= v or w > hor or w not in team:
                continue
            # extend an existing chain ending at v, or start at seed v
            cand = 0
            if dv >= 1:
                cand = dv + 1
            elif base_ok:
                cand = 1
            if cand > depth[w]:
                depth[w] = cand
                if cand > best:
                    best = cand
    return best


def partS5():
    res = {}
    for tag, fn in (("h4096_F64", "e179_s5_witness_h4096_D2F64_lin4.json"),
                    ("h4096_lin4", "e179_s5_witness_h4096_D2F12_lin4.json"),
                    ("h8192_F64", "e179_s5_witness_h8192_D2F64_lin4.json")):
        path = os.path.join(BASE, fn)
        if not os.path.exists(path):
            log(f"[S5] {tag}: MISSING {fn}")
            continue
        hor, A, B, d = load_witness(path)
        D, F = d["D"], d["F"]
        u0 = 64 if F == 64 else 32
        row = {"hor": hor, "D": D, "F": F, "u0": u0, "nA": len(A)}
        # dyadic blocks
        t_hi = hor.bit_length() - 2
        blocks = []
        sparse_ok, split_ok = True, True
        for t in range(5, t_hi + 1):
            blk = list(range((1 << t) + 1, (1 << (t + 1)) + 1))
            cA = sum(1 for v in blk if v in A)
            f = max(2, t - 5)
            if not (f <= cA <= len(blk) - f):
                split_ok = False
            minority = A if 2 * cA <= len(blk) else B
            minv = [v for v in blk if v in minority]
            gaps = [minv[i + 1] - minv[i] for i in range(len(minv) - 1)]
            gmin = min(gaps) if gaps else None
            if gmin is not None and gmin < 3:
                # exactly-half block: the OTHER side may be designated
                if 2 * cA == len(blk):
                    othv = [v for v in blk if v not in minority]
                    og = [othv[i + 1] - othv[i]
                          for i in range(len(othv) - 1)]
                    if og and min(og) < 3:
                        sparse_ok = False
                else:
                    sparse_ok = False
            blocks.append({"t": t, "size": len(blk), "cA": cA,
                           "min_team": "A" if minority is A else "B",
                           "min_gapmin": gmin,
                           "min_n": len(minv)})
        row["blocks"] = blocks
        row["sparse_ok"] = sparse_ok
        row["split_ok"] = split_ok
        # windows (a, 2a]
        gname = d.get("gmode", "lin4")
        diffuse_ok = True
        supd = 0.0
        for a in range(32, hor // 2 + 1):
            w = a
            cA = sum(1 for v in range(a + 1, 2 * a + 1) if v in A)
            g = a // 4
            if not (g <= cA <= w - g):
                diffuse_ok = False
            supd = max(supd, max(cA, w - cA) / w)
        row["diffuse_ok(lin4)"] = diffuse_ok
        row["sup_window_density"] = round(supd, 4)
        row["rung_safe(<13/16)"] = supd < 13 / 16
        # orbit census
        for Ftest in (12, 64, 128):
            row[f"depthA_F{Ftest}"] = chain_depth(A, hor, Ftest, u0)
            row[f"depthB_F{Ftest}"] = chain_depth(B, hor, Ftest, u0)
        cen_ok = (row[f"depthA_F{F}"] < D) and (row[f"depthB_F{F}"] < D)
        row["censor_ok"] = cen_ok
        # minority anatomy: modal residues of minority per block
        anat = []
        for b in blocks:
            t = b["t"]
            blk = range((1 << t) + 1, (1 << (t + 1)) + 1)
            minority = A if b["min_team"] == "A" else B
            minv = [v for v in blk if v in minority]
            from collections import Counter
            c4 = Counter(v % 4 for v in minv)
            gaps = Counter(minv[i + 1] - minv[i]
                           for i in range(len(minv) - 1))
            anat.append({"t": t, "mod4": dict(c4),
                         "gap_hist": dict(sorted(gaps.items())[:6])})
        row["minority_anatomy"] = anat
        res[tag] = row
        log(f"[S5] {tag}: split_ok={split_ok} sparse_ok={sparse_ok} "
            f"diffuse_ok={diffuse_ok} supdens={row['sup_window_density']} "
            f"rung_safe={row['rung_safe(<13/16)']} "
            f"depths A/B @F12={row['depthA_F12']}/{row['depthB_F12']} "
            f"@F64={row['depthA_F64']}/{row['depthB_F64']} "
            f"@F128={row['depthA_F128']}/{row['depthB_F128']} "
            f"censor_ok={cen_ok}")
    OUT["partS5"] = res
    dump()


# ------------------------------------------------------------- partS5CORE
def partS5CORE():
    """Witness coloring FIXED; both teams block-ordered at both seams
    of (m, 2m], (2m, 4m], (4m, 8m]; per-team AP-freeness.  Fresh
    encoding: within-block order vars only; cross-block APs reduce to
    forced binary/unit constraints under block order."""
    from pysat.solvers import Glucose42

    def run(m, A, hor):
        assert 8 * m <= hor
        blks = [list(range(m + 1, 2 * m + 1)),
                list(range(2 * m + 1, 4 * m + 1)),
                list(range(4 * m + 1, 8 * m + 1))]
        win = [v for b in blks for v in b]
        bidx = {}
        for i, b in enumerate(blks):
            for v in b:
                bidx[v] = i
        team = {v: (v in A) for v in win}
        top = 0
        ovar = {}

        def o(u, v):
            """literal: u placed before v (same team, same block)."""
            nonlocal top
            if (u, v) in ovar:
                return ovar[(u, v)]
            if (v, u) in ovar:
                return -ovar[(v, u)]
            top += 1
            ovar[(u, v)] = top
            return top

        cls = []
        # transitivity per team per block
        for b in blks:
            for tm in (True, False):
                vs = [v for v in b if team[v] == tm]
                n = len(vs)
                for i in range(n):
                    for j in range(i + 1, n):
                        for k in range(j + 1, n):
                            u, v, w = vs[i], vs[j], vs[k]
                            cls.append([-o(u, v), -o(v, w), o(u, w)])
                            cls.append([o(u, v), o(v, w), -o(u, w)])
        # AP constraints, in-team triples only
        wset = set(win)
        contradiction = False
        for xv in win:
            for yv in range(xv + 1, (win[-1] + xv) // 2 + 1):
                zv = 2 * yv - xv
                if yv not in wset or zv not in wset or zv <= yv:
                    continue
                if not (team[xv] == team[yv] == team[zv]):
                    continue
                bx, by, bz = bidx[xv], bidx[yv], bidx[zv]
                # ban pos(x)<pos(y)<pos(z) and pos(z)<pos(y)<pos(x)
                if bx == by == bz:
                    cls.append([-o(xv, yv), -o(yv, zv)])
                    cls.append([-o(zv, yv), -o(yv, xv)])
                elif bx == by and by < bz:
                    # z after x,y: ban pos(x)<pos(y)
                    cls.append([-o(xv, yv)])
                elif bx < by and by == bz:
                    # x before y,z: ban pos(y)<pos(z)
                    cls.append([-o(yv, zv)])
                elif bx < by < bz:
                    contradiction = True  # increasing across blocks
                # other cross patterns cannot be monotone under block order
        if contradiction:
            return "UNSAT(structural)", 0.0
        t0 = time.time()
        with Glucose42(bootstrap_with=cls) as s:
            r = s.solve()
        return ("SAT" if r else "UNSAT"), round(time.time() - t0, 1)

    res = {}
    for tag, fn in (("h4096_F64", "e179_s5_witness_h4096_D2F64_lin4.json"),
                    ("h4096_lin4", "e179_s5_witness_h4096_D2F12_lin4.json")):
        path = os.path.join(BASE, fn)
        if not os.path.exists(path):
            continue
        hor, A, B, d = load_witness(path)
        for m in (16, 32, 64):
            v, secs = run(m, A, hor)
            res[f"{tag}_m{m}"] = {"verdict": v, "secs": secs}
            log(f"[S5CORE] {tag} m={m}: double-block-order + per-team "
                f"AP-freeness on witness coloring: {v} [{secs}s]")
    OUT["partS5CORE"] = res
    dump()


PARTS = {"partC3SCHEMA": partC3SCHEMA, "partC3XVAL": partC3XVAL,
         "partK19M112": partK19M112, "partPS": partPS,
         "partS5": partS5, "partS5CORE": partS5CORE}

if __name__ == "__main__":
    want = sys.argv[1:] or ["all"]
    names = list(PARTS) if want == ["all"] else want
    t0 = time.time()
    for nm in names:
        PARTS[nm]()
    print(f"total {time.time() - t0:.0f}s", flush=True)
