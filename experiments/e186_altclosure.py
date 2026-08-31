"""e186_altclosure: GAP-AFFORD''-ALT instrument (notes/81 SS0).

  partLATRUNG  R(x;M) \\ class-c: full pair rung {x,x+1}, guarded
               units, punctures = one residue class mod 4 in window.
  partJOINT    2-pair menus under full class punctures.
  partSPARSE   existential gap->=3 punctures vs single pair (control)
               and joint menus.
  partROB      class-c + existential <=C extra off-class punctures.
  partRSCAN    S5-ALT F=64 maxrun R scan (pods; import from e185).
  partF12      F=12 run<=2/<=3 long budgets (pods).
  partNUGROW   nu scans at m=64 on alternating witness; pureL3 m=32.

Run: .venv/bin/python experiments/e186_altclosure.py <part> [args]
Artifacts: data/e186_altclosure.json + .log (terse stream).
"""
import json
import os
import sys
import time

from pysat.card import ITotalizer
from pysat.solvers import Cadical195

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(os.path.dirname(HERE), "data")
OUT_PATH = os.path.join(BASE, "e186_altclosure.json")
OUT = {}


def dump():
    try:
        old = json.load(open(OUT_PATH))
    except Exception:
        old = {}
    for k, v in OUT.items():
        if isinstance(v, list) and isinstance(old.get(k), list):
            seen = {json.dumps(r, sort_keys=True) for r in old[k]}
            old[k].extend(r for r in v
                          if json.dumps(r, sort_keys=True) not in seen)
        else:
            old[k] = v
    json.dump(old, open(OUT_PATH, "w"), indent=1)


def log(msg):
    print(msg, flush=True)
    with open(os.path.join(BASE, "e186_altclosure.log"), "a") as f:
        f.write(msg + "\n")


# ------------------------------------------------------------ rung kit

def rung_clauses(M, attackers, alive):
    """Complete encoding of the punctured rung: order vars over the
    alive set S subset (M, 2M], full transitivity, in-window AP bans,
    fired units z<y for APs (a,y,z), a in attackers, y,z in S.
    Returns (clauses, nvars)."""
    S = sorted(alive)
    n = len(S)
    idx = {v: i for i, v in enumerate(S)}
    ovar = {}
    top = 0
    for i in range(n):
        for j in range(i + 1, n):
            top += 1
            ovar[(i, j)] = top

    def o(a, b):
        i, j = idx[a], idx[b]
        return ovar[(i, j)] if i < j else -ovar[(j, i)]

    cls = []
    aset = set(S)
    # in-window AP bans
    for y in S:
        for x in S:
            if x >= y:
                break
            z = 2 * y - x
            if z <= 2 * M and z in aset:
                cls.append([-o(x, y), -o(y, z)])
                cls.append([-o(z, y), -o(y, x)])
    # fired units
    for a in attackers:
        for y in S:
            z = 2 * y - a
            if z > y and z <= 2 * M and z in aset:
                cls.append([o(z, y)])
    # transitivity
    for i in range(n):
        for j in range(i + 1, n):
            oij = ovar[(i, j)]
            for k in range(j + 1, n):
                cls.append([-oij, -ovar[(j, k)], ovar[(i, k)]])
                cls.append([oij, ovar[(j, k)], -ovar[(i, k)]])
    return cls, top


def solve_rung(M, attackers, D, tag):
    t0 = time.time()
    alive = [v for v in range(M + 1, 2 * M + 1) if v not in D]
    cls, _ = rung_clauses(M, attackers, alive)
    with Cadical195(bootstrap_with=cls) as s:
        v = "SAT" if s.solve() else "UNSAT"
    secs = round(time.time() - t0, 1)
    row = {"tag": tag, "M": M, "attackers": sorted(attackers),
           "nD": len(D), "n": len(alive), "verdict": v, "secs": secs}
    log(f"[{tag}] M={M} att={sorted(attackers)} |D|={len(D)} "
        f"n={len(alive)}: {v} [{secs}s]")
    return row


def class_D(M, c):
    return set(v for v in range(M + 1, 2 * M + 1) if v % 4 == c)


def partLATRUNG(Ms=(128, 256), xs=(15, 17, 25, 27)):
    res = OUT.setdefault("partLATRUNG", [])
    for M in Ms:
        for x in xs:
            # unpunctured control once per (x, M)
            res.append(solve_rung(M, (x, x + 1), set(), "LATRUNG-ctl"))
            dump()
            for c in (0, 1, 2, 3):
                res.append(solve_rung(M, (x, x + 1), class_D(M, c),
                                      f"LATRUNG-c{c}"))
                dump()


def partJOINT(Ms=(128, 256)):
    res = OUT.setdefault("partJOINT", [])
    menus = {"15+27": (15, 16, 27, 28), "17+25": (17, 18, 25, 26)}
    for M in Ms:
        for nm, att in menus.items():
            for c in (0, 1, 2, 3):
                res.append(solve_rung(M, att, class_D(M, c),
                                      f"JOINT-{nm}-c{c}"))
                dump()


# ------------------------------------- existential-puncture encoding

def sparse_exist(M, attackers, tag, sparse=True, extra_cap=None,
                 base_D=(), deadline=None):
    """Membership vars m_v (True = alive) on (M, 2M]; punctures D =
    {v: not m_v} constrained gap->=3 within D (if sparse); base_D
    forced punctured; extra_cap = totalizer cap on punctures outside
    base_D.  Order vars over ALL window values (constraints guarded
    by membership).  SAT => decode D."""
    t0 = time.time()
    W = list(range(M + 1, 2 * M + 1))
    n = len(W)
    idx = {v: i for i, v in enumerate(W)}
    top = 0
    ovar = {}
    for i in range(n):
        for j in range(i + 1, n):
            top += 1
            ovar[(i, j)] = top

    def o(a, b):
        i, j = idx[a], idx[b]
        return ovar[(i, j)] if i < j else -ovar[(j, i)]

    mvar = {}
    for v in W:
        top += 1
        mvar[v] = top
    cls = []
    base = set(base_D)
    for v in base:
        cls.append([-mvar[v]])
    if sparse:
        for v in W:
            for g in (1, 2):
                if v + g in mvar:
                    cls.append([mvar[v], mvar[v + g]])
    wset = set(W)
    for y in W:
        for x in W:
            if x >= y:
                break
            z = 2 * y - x
            if z <= 2 * M and z in wset:
                g = [-mvar[x], -mvar[y], -mvar[z]]
                cls.append(g + [-o(x, y), -o(y, z)])
                cls.append(g + [-o(z, y), -o(y, x)])
    for a in attackers:
        for y in W:
            z = 2 * y - a
            if z > y and z <= 2 * M and z in wset:
                cls.append([-mvar[y], -mvar[z], o(z, y)])
    for i in range(n):
        for j in range(i + 1, n):
            oij = ovar[(i, j)]
            for k in range(j + 1, n):
                cls.append([-oij, -ovar[(j, k)], ovar[(i, k)]])
                cls.append([oij, ovar[(j, k)], -ovar[(i, k)]])
    assum = []
    tot = None
    if extra_cap is not None:
        xlits = []
        for v in W:
            if v not in base:
                top += 1
                cls.append([mvar[v], top])   # punctured => indicator
                xlits.append(top)
        tot = ITotalizer(lits=xlits, ubound=extra_cap + 1, top_id=top)
        cls.extend(tot.cnf.clauses)
        assum = [-tot.rhs[extra_cap]]
    with Cadical195(bootstrap_with=cls) as s:
        ok = s.solve(assumptions=assum)
        model = s.get_model() if ok else None
    if tot:
        tot.delete()
    v = "SAT" if ok else "UNSAT"
    secs = round(time.time() - t0, 1)
    row = {"tag": tag, "M": M, "attackers": sorted(attackers),
           "sparse": sparse, "extra_cap": extra_cap,
           "nbase": len(base), "verdict": v, "secs": secs}
    if ok:
        pos = set(l for l in model if l > 0)
        D = sorted(v_ for v_ in W if mvar[v_] not in pos)
        gaps = [D[i + 1] - D[i] for i in range(len(D) - 1)]
        row["D"] = D
        row["D_size"] = len(D)
        row["min_gap"] = min(gaps) if gaps else None
        row["D_mod4"] = sorted(set(d % 4 for d in D))
    log(f"[{tag}] M={M} att={sorted(attackers)} sparse={sparse} "
        f"cap={extra_cap}: {v} "
        f"{('D=' + str(row.get('D_size')) + ' mingap=' + str(row.get('min_gap')) + ' mod4=' + str(row.get('D_mod4'))) if ok else ''} "
        f"[{secs}s]")
    return row


def partSPARSE(Ms=(64, 96, 128)):
    res = OUT.setdefault("partSPARSE", [])
    # positive control: known mixed-transversal escape
    res.append(sparse_exist(112, (27, 28), "SPARSE-ctl27"))
    dump()
    menus = {"15+27": (15, 16, 27, 28), "17+25": (17, 18, 25, 26)}
    for M in Ms:
        for nm, att in menus.items():
            res.append(sparse_exist(M, att, f"SPARSE-{nm}"))
            dump()


MENUS3 = {"x3-k3": (15, 23, 27), "x3-k4": (15, 23, 27, 31),
          "x3-k6": (15, 23, 27, 31, 35, 39),
          "x1-k3": (17, 21, 25), "x1-k4": (17, 21, 25, 29),
          "x1-k6": (17, 21, 25, 29, 33, 37)}


def partKMENU(Ms=(256,), which=None):
    """k-pair menus under full class punctures, extractable cells only:
    x=3 mod 4 menus vs c in {1,2}; x=1 mod 4 menus vs c in {0,3}."""
    res = OUT.setdefault("partKMENU", [])
    for M in Ms:
        for nm, xs in MENUS3.items():
            if which and nm not in which:
                continue
            att = tuple(a for x in xs for a in (x, x + 1))
            cs = (1, 2) if nm.startswith("x3") else (0, 3)
            for c in cs:
                res.append(solve_rung(M, att, class_D(M, c),
                                      f"KMENU-{nm}-c{c}"))
                dump()
    # complete the mod-8 map: x=21,23,29,31 single cells
    for M in Ms:
        for x in (21, 23, 29, 31):
            res.append(solve_rung(M, (x, x + 1), set(),
                                  "KM1-ctl"))
            dump()
            for c in (0, 1, 2, 3):
                res.append(solve_rung(M, (x, x + 1), class_D(M, c),
                                      f"KM1-x{x}-c{c}"))
                dump()


def partSPARSEK(Ms=(96, 128)):
    """existential gap->=3 punctures vs k=3/4/6 menus."""
    res = OUT.setdefault("partSPARSEK", [])
    for M in Ms:
        for nm in ("x3-k3", "x3-k4", "x3-k6"):
            xs = MENUS3[nm]
            att = tuple(a for x in xs for a in (x, x + 1))
            res.append(sparse_exist(M, att, f"SPARSEK-{nm}"))
            dump()


def partROB(Ms=(128,), caps=(4, 8)):
    """class-c + existential <=C extra punctures (off-class free),
    only for cells whose base LATRUNG verdict is UNSAT."""
    res = OUT.setdefault("partROB", [])
    base_rows = {(r["M"], tuple(r["attackers"]), r["tag"]): r["verdict"]
                 for r in OUT.get("partLATRUNG", [])}
    grid = [(x, c) for x in (15, 17, 25, 27) for c in (0, 1, 2, 3)]
    for M in Ms:
        for x, c in grid:
            bv = base_rows.get((M, (x, x + 1), f"LATRUNG-c{c}"))
            if bv != "UNSAT":
                continue
            for cap in caps:
                res.append(sparse_exist(
                    M, (x, x + 1), f"ROB-x{x}-c{c}-C{cap}",
                    sparse=False, extra_cap=cap,
                    base_D=sorted(class_D(M, c))))
                dump()


# ---------------------------------------------- pre-registered parts

def _s5(R, F, u0, budget, hor=4096):
    sys.path.insert(0, HERE)
    import e185_mintloc as e185
    e185.__dict__["_MAXRUN"] = R
    try:
        e185.partS5ALT(hor=hor, F=F, u0=u0, budget=budget)
    finally:
        e185.__dict__["_MAXRUN"] = 1


def partRSCAN(budget=14400.0):
    for R in (3, 4, 5):
        _s5(R, 64, 64, budget)


def partF12(budget=21600.0):
    for R in (2, 3):
        _s5(R, 12, 32, budget)


def partNUGROW():
    sys.path.insert(0, HERE)
    import e185_mintloc as e185
    res = OUT.setdefault("partNUGROW", [])
    # alternating witness (censor-off run<=1 coloring, e185)
    p = os.path.join(BASE, "e185_s5alt_h4096_F12_r1_noorb_a6.json")
    d = json.load(open(p))
    hor, A = d["hor"], set(d["A"])
    for m, budgets in ((64, (12, 16, 24, 32)),):
        for team in ("A", "B"):
            Bs = e185.team_sets(hor, A, m, team)
            n = sum(len(b) for b in Bs)
            t0 = time.time()
            rows = e185.nu_scan(Bs, list(budgets),
                                deadline=time.time() + 20000)
            res.append({"col": "altw", "m": m, "team": team, "n": n,
                        "scan": rows,
                        "secs": round(time.time() - t0, 1)})
            log(f"[NUGROW] altw m={m} T={team} n={n}: {rows}")
            dump()
    # pure lattice m=32 minority frontier push
    horL = 2048
    AL = set(v for v in range(1, horL + 1) if v % 4 == 3)
    Bs = e185.team_sets(horL, AL, 32, "A")
    n = sum(len(b) for b in Bs)
    t0 = time.time()
    rows = e185.nu_scan(Bs, [24, 48, 96, 144, 192, 216, 228, 240, 252],
                        deadline=time.time() + 40000)
    res.append({"col": "pureL3", "m": 32, "team": "A", "n": n,
                "scan": rows, "secs": round(time.time() - t0, 1)})
    log(f"[NUGROW] pureL3 m=32 T=A n={n}: {rows}")
    dump()


# ------------------------------------------- notes/82 verification

def lam(c, t):
    return [v for v in range((1 << t) + 1, (1 << (t + 1)) + 1)
            if v % 4 == c]


def phi(x, c):
    return x // 4 if c == 0 else (x - c + 4) // 4


def partQVERIFY():
    """Adversarial verification of Lemma Q (notes/82 SS2.1):
    (a) chart exactness phi(Lambda_c(t)) = B(t-2), all c, t=4..14;
    (b) AP transport both directions + midpoint-class, exhaustive;
    (c) C3(p) units subset of R(3p,3p+1;M,0) fired units, p=5/9/13;
    (d) R(39,40; M, 0) UNSAT direct (p=13 fresh; p=5/9 = ctl rows);
    (e) witnesses: 4-purity per block per class + transported image
        clean blocks at >=2 scales each."""
    res = {}
    # (a) chart exactness
    bad = []
    for c in range(4):
        for t in range(4, 15):
            img = sorted(phi(x, c) for x in lam(c, t))
            want = list(range((1 << (t - 2)) + 1, (1 << (t - 1)) + 1))
            if img != want:
                bad.append((c, t))
    res["chart_exact"] = {"cells": 4 * 11, "fail": bad}
    log(f"[QVER] chart exactness: {4*11} cells, fail={bad}")
    # (b) AP transport, exhaustive on [1, 600]
    fails = 0
    checked = 0
    for c in range(4):
        vals = [v for v in range(1, 601) if v % 4 == c]
        vs = set(vals)
        for i, x in enumerate(vals):
            for y in vals[i + 1:]:
                z = 2 * y - x
                if z in vs:
                    checked += 1
                    fx, fy, fz = phi(x, c), phi(y, c), phi(z, c)
                    if fx + fz != 2 * fy:
                        fails += 1
        # reverse: image APs pull back with midpoint in class
        imgs = sorted(phi(v, c) for v in vals)
        iset = set(imgs)
        for i, a in enumerate(imgs):
            for b in imgs[i + 1:]:
                zz = 2 * b - a
                if zz in iset:
                    checked += 1
                    X = 4 * a + (c - 4 if c else 0)
                    Y = 4 * b + (c - 4 if c else 0)
                    Z = 4 * zz + (c - 4 if c else 0)
                    if X + Z != 2 * Y or Y % 4 != c:
                        fails += 1
    res["ap_transport"] = {"checked": checked, "fail": fails}
    log(f"[QVER] AP transport: {checked} triples, fail={fails}")
    # (c) unit membership
    umf = []
    for p in (5, 9, 13):
        for M in (128, 256):
            fired = set()
            for a in (3 * p, 3 * p + 1):
                for j in range(1, M):
                    i = a - 2 * j
                    if 0 <= i <= M - 1:
                        fired.add((2 * M - i, M + j))
            core = [(2 * M - p, M + p), (2 * M - (p - 2), M + p + 1),
                    (2 * M - (p + 5), M + p - 2)]
            if not all(u in fired for u in core):
                umf.append((p, M))
    res["c3_units_in_R"] = {"cells": 6, "fail": umf}
    log(f"[QVER] C3(p) units in R fired set: 6 cells, fail={umf}")
    # (d) fresh rung UNSAT p=13
    r = solve_rung(128, (39, 40), set(), "QVER-R39")
    res["R39_M128"] = r["verdict"]
    # (e) witnesses: 4-purity + transported clean blocks
    sys.path.insert(0, HERE)
    import e185_mintloc as e185
    ws = e185.load_witnesses()
    p_alt = os.path.join(BASE, "e185_s5alt_h4096_F12_r1_noorb_a6.json")
    if os.path.exists(p_alt):
        d = json.load(open(p_alt))
        ws["altw"] = (d["hor"], set(d["A"]))
    wres = {}
    for tag, (hor, A) in ws.items():
        rows = []
        for t in range(5, hor.bit_length() - 1):
            pure = []
            for c in range(4):
                sec = lam(c, t)
                inA = sum(1 for v in sec if v in A)
                if inA == len(sec):
                    pure.append((c, "A"))
                elif inA == 0:
                    pure.append((c, "B"))
            rows.append({"t": t, "pure": pure,
                         "n_pure": len(pure)})
        # transported image check at the two largest all-pure scales
        allp = [r_ for r_ in rows if r_["n_pure"] == 4]
        img_ok = []
        for r_ in allp[-2:]:
            t = r_["t"]
            c, team = r_["pure"][0]
            T = A if team == "A" else None
            Tset = A if team == "A" else set(
                range(1, hor + 1)) - A
            img = set(phi(v, c) for v in Tset
                      if v % 4 == c and v <= hor)
            B_img = set(range((1 << (t - 2)) + 1,
                              (1 << (t - 1)) + 1))
            img_ok.append({"t": t, "c": c, "team": team,
                           "clean": B_img <= img})
        wres[tag] = {"blocks": rows, "img": img_ok}
        np = [r_["n_pure"] for r_ in rows]
        log(f"[QVER] {tag}: n_pure per block t>=5: {np}; "
            f"img clean blocks: {img_ok}")
    res["witnesses"] = wres
    OUT["partQVERIFY"] = res
    dump()


def partGENESON(t_max=200):
    """Lemma Q adversarial audit on Geneson's W (density-2/3
    permutable): count full class-sections Lambda_c(t) inside W.
    Q predicts finitely many (an infinite family would indict
    B1/C3(p))."""
    sys.path.insert(0, HERE)
    import h1_complement as h1
    ivs = h1.w_intervals(1 << (t_max + 2))
    res = []
    for t in range(2, t_max + 1):
        blo, bhi = (1 << t) + 1, 1 << (t + 1)
        # C-gaps inside the block
        cov = [(max(lo, blo), min(hi, bhi)) for lo, hi in ivs
               if hi >= blo and lo <= bhi]
        cov.sort()
        gaps = []
        cur = blo
        for lo, hi in cov:
            if lo > cur:
                gaps.append((cur, lo - 1))
            cur = max(cur, hi + 1)
        if cur <= bhi:
            gaps.append((cur, bhi))
        killed = set()
        for lo, hi in gaps:
            if hi - lo + 1 >= 4:
                killed = {0, 1, 2, 3}
                break
            for v in range(lo, hi + 1):
                killed.add(v % 4)
        full = sorted(set(range(4)) - killed)
        if full:
            res.append({"t": t, "full_classes": full})
    OUT["partGENESON"] = {"t_max": t_max, "hits": res,
                          "n_hits": len(res)}
    log(f"[GENESON] t<=%d: full-section hits=%d %s" %
        (t_max, len(res), res[:12]))
    dump()


def partHSPLIT(hor=4096, F=12, u0=32, budget=7200.0, k8=True):
    """The GAP-AFFORD'''-SPLIT instrument: e179 s5dodger axes
    (i-proxy)+(ii)+(iii)+split floor, PLUS Cor. HSPLIT as a
    constraint: every class mod 4 (and mod 8 if k8) is bichromatic
    within every dyadic block t >= 6.

    INTERPRETATION (downgraded per external review, notes/88 item
    1): UNSAT here proves ONLY that every finite corner inhabitant
    on [1, hor] at these parameters has >= 1 monochromatic
    residue-class section at some tested scale 6 <= t <= t_max.
    It does NOT show inhabitants are lattices, and licenses NO
    omega conclusion (no compactness step; ALT-DEAD needs
    infinitely many 4-pure scales).  The omega-relevant open
    statement is the shifted-window family: for every T >= 6,
    infeasibility with bichromaticity imposed only at scales
    >= T.  This function imposes T = 6 only."""
    from ortools.sat.python import cp_model
    t0 = time.time()
    D = 2
    mdl = cp_model.CpModel()
    A = {v: mdl.NewBoolVar(f"A{v}") for v in range(1, hor + 1)}

    def team(t, v):
        return A[v] if t == "A" else A[v].Not()

    t_lo, t_hi = 5, hor.bit_length() - 2
    for t in range(t_lo, t_hi + 1):
        blk = list(range((1 << t) + 1, (1 << (t + 1)) + 1))
        cntA = mdl.NewIntVar(0, len(blk), f"cA{t}")
        mdl.Add(cntA == sum(A[v] for v in blk))
        f = max(2, t - 5)
        mdl.Add(cntA >= f)
        mdl.Add(cntA <= len(blk) - f)
        mA = mdl.NewBoolVar(f"mA{t}")
        mdl.Add(2 * cntA <= len(blk)).OnlyEnforceIf(mA)
        mdl.Add(2 * cntA >= len(blk)).OnlyEnforceIf(mA.Not())
        for v in blk:
            for g in (1, 2):
                if v + g <= blk[-1]:
                    mdl.AddBoolOr([A[v].Not(), A[v + g].Not(),
                                   mA.Not()])
                    mdl.AddBoolOr([A[v], A[v + g], mA])
        # HSPLIT: class sections bichromatic (t >= 6)
        if t >= 6:
            mods = (4, 8) if k8 else (4,)
            for md in mods:
                for c in range(md):
                    sec = [v for v in blk if v % md == c]
                    if len(sec) >= 2:
                        mdl.AddBoolOr([A[v] for v in sec])
                        mdl.AddBoolOr([A[v].Not() for v in sec])
    S = {0: mdl.NewConstant(0)}
    for v in range(1, hor + 1):
        S[v] = mdl.NewIntVar(0, v, f"S{v}")
        mdl.Add(S[v] == S[v - 1] + A[v])
    for a in range(32, hor // 2 + 1):
        g = a // 4
        cA = S[2 * a] - S[a]
        mdl.Add(cA >= g)
        mdl.Add(cA <= a - g)
    for tname in ("A", "B"):
        reach = {}
        for d in range(1, D + 1):
            for v in range(1, hor + 1):
                reach[(d, v)] = mdl.NewBoolVar(f"r{tname}{d}_{v}")
        for v in range(1, hor + 1):
            for f in range(1, F + 1):
                w = 2 * v - f
                if w <= v or w > hor:
                    continue
                if v > u0:
                    mdl.AddBoolOr([team(tname, v).Not(),
                                   team(tname, f).Not(),
                                   team(tname, w).Not(),
                                   reach[(1, w)]])
                for d in range(2, D + 1):
                    mdl.AddBoolOr([reach[(d - 1, v)].Not(),
                                   team(tname, f).Not(),
                                   team(tname, w).Not(),
                                   reach[(d, w)]])
        for v in range(1, hor + 1):
            mdl.Add(reach[(D, v)] == 0)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = budget
    solver.parameters.num_search_workers = 8
    st = solver.Solve(mdl)
    name = {cp_model.OPTIMAL: "SAT", cp_model.FEASIBLE: "SAT",
            cp_model.INFEASIBLE: "UNSAT"}.get(st, "TIMEOUT")
    row = {"part": "hsplit", "hor": hor, "D": D, "F": F, "u0": u0,
           "k8": k8, "verdict": name,
           "secs": round(time.time() - t0, 1)}
    if name == "SAT":
        col = [v for v in range(1, hor + 1) if solver.Value(A[v])]
        out = os.path.join(BASE,
                           f"e186_hsplit_h{hor}_F{F}"
                           f"{'_k8' if k8 else ''}.json")
        json.dump({"hor": hor, "D": D, "F": F, "A": col},
                  open(out, "w"))
        row["witness"] = out
        row["nA"] = len(col)
    log(f"[HSPLIT] {json.dumps(row)}")
    OUT.setdefault("partHSPLIT", []).append(row)
    dump()


PARTS = {"latrung": partLATRUNG, "joint": partJOINT,
         "sparse": partSPARSE, "rob": partROB,
         "rscan": partRSCAN, "f12": partF12, "nugrow": partNUGROW,
         "kmenu": partKMENU, "sparsek": partSPARSEK,
         "qverify": partQVERIFY, "geneson": partGENESON,
         "hsplit": partHSPLIT}

if __name__ == "__main__":
    want = sys.argv[1:] or ["latrung"]
    for nm in want:
        t0 = time.time()
        if nm == "latrung512":
            partLATRUNG(Ms=(512,))
        elif nm == "joint512":
            partJOINT(Ms=(512,))
        elif nm == "hsplit64":
            # the strong-censor cell, DOWNGRADED reading (notes/88
            # item 1) -- see partHSPLIT docstring
            partHSPLIT(hor=4096, F=64, u0=64, k8=True)
        elif nm == "hsplit64ctl":
            partHSPLIT(hor=2048, F=64, u0=64, k8=True)
        else:
            PARTS[nm]()
        dump()
        log(f"[{nm}] done {round(time.time()-t0,1)}s")
