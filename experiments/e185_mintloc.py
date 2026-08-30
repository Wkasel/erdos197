"""e185_mintloc: the sparse-corner pincer instrument (notes/80-pincer).

  partCENSUS   cross-3-block AP family H_T per witness x anchor x team:
               |H|, distinct x/y, max-matching of the (x,y)-projection
               (Koenig displaced-value floor), class-pattern breakdown,
               block ownership.  Includes PURE-LATTICE control.
  partMINTLOC  the notes/80 SS3.3 pre-registration: anchors 32/64/128,
               both teams, budget-0 control + full one-mint enumeration
               (both seams), K1-K5 structural filter + rigid-gamma SAT
               solve on survivors; SAT-region + displaced-value location.
  partNU       minimum-payment scan (extension): per-team theory, all
               adjacent-seam pairs allowed but counted, totalizer budget
               scan; witnesses m=32 (+64 small side), control m=16/32.

Run: .venv/bin/python experiments/e185_mintloc.py [census|mintloc|nu|all]
Artifacts: data/e185_mintloc.json + .log (terse stream).
"""
import json
import os
import sys
import time

from pysat.card import ITotalizer
from pysat.solvers import Cadical195

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(os.path.dirname(HERE), "data")
OUT_PATH = os.path.join(BASE, "e185_mintloc.json")
OUT = {}


def dump():
    try:
        old = json.load(open(OUT_PATH))
    except Exception:
        old = {}
    old.update(OUT)
    json.dump(old, open(OUT_PATH, "w"), indent=1)


def log(msg):
    print(msg, flush=True)
    with open(os.path.join(BASE, "e185_mintloc.log"), "a") as f:
        f.write(msg + "\n")


def load_witnesses():
    ws = {}
    for tag, fn in (("h4096_F64", "e179_s5_witness_h4096_D2F64_lin4.json"),
                    ("h4096_lin4", "e179_s5_witness_h4096_D2F12_lin4.json"),
                    ("h8192_F64", "e179_s5_witness_h8192_D2F64_lin4.json")):
        p = os.path.join(BASE, fn)
        if os.path.exists(p):
            d = json.load(open(p))
            ws[tag] = (d["hor"], set(d["A"]))
    # pure-lattice control: A = class 3 mod 4 on [1, 2048]
    hor = 2048
    ws["pureL3"] = (hor, set(v for v in range(1, hor + 1) if v % 4 == 3))
    return ws


def blocks3(m):
    return [list(range(m + 1, 2 * m + 1)),
            list(range(2 * m + 1, 4 * m + 1)),
            list(range(4 * m + 1, 8 * m + 1))]


def team_sets(hor, A, m, team):
    T = A if team == "A" else set(range(1, hor + 1)) - A
    return [sorted(T & set(b)) for b in blocks3(m)]


def Hfam(B0, B1, B2):
    """Cross-3-block AP family: (x,y,2y-x) in B0 x B1 x B2 (in-team)."""
    S2 = set(B2)
    return [(x, y, 2 * y - x) for x in B0 for y in B1 if 2 * y - x in S2]


def max_matching(edges):
    """Hopcroft-ish augmenting-path matching on (x,y) edge list."""
    adj = {}
    for x, y in edges:
        adj.setdefault(x, []).append(y)
    matchY = {}

    def aug(x, seen):
        for y in adj.get(x, ()):
            if y in seen:
                continue
            seen.add(y)
            if y not in matchY or aug(matchY[y], seen):
                matchY[y] = x
                return True
        return False

    n = 0
    for x in adj:
        if aug(x, set()):
            n += 1
    return n


# ------------------------------------------------------------------ census

def partCENSUS():
    ws = load_witnesses()
    res = {}
    for tag, (hor, A) in ws.items():
        rows = []
        own = []
        for t in range(5, hor.bit_length() - 1):
            blk = range((1 << t) + 1, (1 << (t + 1)) + 1)
            cA = sum(1 for v in blk if v in A)
            mt = "A" if 2 * cA <= len(blk) else "B"
            T = A if mt == "A" else None
            minv = [v for v in blk if (v in A) == (mt == "A")]
            from collections import Counter
            c4 = Counter(v % 4 for v in minv)
            cls = c4.most_common(1)[0][0] if minv else None
            own.append({"t": t, "min_team": mt, "cA": cA, "size": len(blk),
                        "mod4_top": cls,
                        "pure": (len(c4) == 1 and
                                 all(minv[i+1]-minv[i] == 4
                                     for i in range(len(minv)-1)))})
        for m in (16, 32, 64, 128, 256):
            if 8 * m > hor:
                continue
            for team in ("A", "B"):
                B0, B1, B2 = team_sets(hor, A, m, team)
                H = Hfam(B0, B1, B2)
                xs = set(h[0] for h in H)
                ys = set(h[1] for h in H)
                mm = max_matching([(h[0], h[1]) for h in H]) if H else 0
                from collections import Counter
                pat = Counter((h[0] % 4, h[1] % 4, h[2] % 4) for h in H)
                rows.append({"m": m, "team": team, "H": len(H),
                             "nx": len(xs), "ny": len(ys), "matching": mm,
                             "presence": [len(B0), len(B1), len(B2)],
                             "patterns": {str(k): v
                                          for k, v in pat.most_common(6)}})
                log(f"[CENSUS] {tag} m={m} T={team}: |H|={len(H)} "
                    f"nx={len(xs)} ny={len(ys)} match={mm} "
                    f"pres={len(B0)}/{len(B1)}/{len(B2)}")
        res[tag] = {"ownership": own, "anchors": rows}
    OUT["partCENSUS"] = res
    dump()


# ---------------------------------------------------------------- mint kit

def in_team_APs(W, tset):
    """All in-team 3-APs (x,y,z), x<y<z, within value list W (sorted)."""
    out = []
    lo, hi = W[0], W[-1]
    for y in W:
        d = 1
        # iterate over in-team x < y with z = 2y - x <= hi
        for x in W:
            if x >= y:
                break
            z = 2 * y - x
            if z <= hi and z in tset:
                out.append((x, y, z))
    return out


def gamma_map(Bs, mint):
    """Group index per value under block order (+ optional mint (u,w,s)):
    rigid segments; returns dict value -> gamma."""
    g = {}
    for i, blk in enumerate(Bs):
        for v in blk:
            g[v] = 3 * i
    if mint:
        u, w, s = mint
        g[w] = 3 * s + 1
        g[u] = 3 * s + 2
    return g


def solve_rigid(Bs, mint, tset, APs):
    """Exact SAT of the block-order(+one-mint) theory for one team.
    Order vars only within blocks among non-mint values; gamma fixes
    the rest.  Returns verdict."""
    g = gamma_map(Bs, mint)
    mvals = set(mint[:2]) if mint else set()
    top = 0
    ovar = {}

    def ov(a, b):
        nonlocal top
        if (a, b) in ovar:
            return ovar[(a, b)]
        if (b, a) in ovar:
            return -ovar[(b, a)]
        top += 1
        ovar[(a, b)] = top
        return top

    def cmp_lit(a, b):
        """pos(a) < pos(b): True/False constant or literal."""
        if g[a] != g[b]:
            return g[a] < g[b]
        if a in mvals or b in mvals:
            # same gamma impossible for mint values (unique groups)
            raise AssertionError
        return ov(a, b)

    cls = []
    for (x, y, z) in APs:
        for (c1, c2) in ((cmp_lit(x, y), cmp_lit(y, z)),
                         (cmp_lit(z, y), cmp_lit(y, x))):
            if c1 is False or c2 is False:
                continue
            if c1 is True and c2 is True:
                return "UNSAT-structural"
            lits = []
            if c1 is not True:
                lits.append(-c1)
            if c2 is not True:
                lits.append(-c2)
            cls.append(lits)
    # transitivity within blocks among non-mint team values
    for blk in Bs:
        vs = [v for v in blk if v not in mvals]
        n = len(vs)
        for i in range(n):
            for j in range(i + 1, n):
                oij = ov(vs[i], vs[j])
                for k in range(j + 1, n):
                    cls.append([-oij, -ov(vs[j], vs[k]), ov(vs[i], vs[k])])
                    cls.append([oij, ov(vs[j], vs[k]), -ov(vs[i], vs[k])])
    with Cadical195(bootstrap_with=cls) as s:
        return "SAT" if s.solve() else "UNSAT"


def kfilter_slow(Bs, APs, u, w, seam):
    """Exact filter: any AP with strictly increasing gamma groups kills.
    Used for cross-validation on a sample."""
    g = gamma_map(Bs, (u, w, seam))
    for (x, y, z) in APs:
        if g[x] < g[y] < g[z]:
            return f"K({g[x]},{g[y]},{g[z]})"
        if g[z] < g[y] < g[x]:
            return f"Kdown({g[z]},{g[y]},{g[x]})"
    return None


class FastFilter:
    """Closed-form K1-K5 survival conditions (notes/80-pincer SS2.1)."""

    def __init__(self, Bs, tset, H):
        S0, S1, S2 = (set(b) for b in Bs)
        self.cntH = len(H)
        self.cxy = {}
        self.cyz = {}
        for (x, y, z) in H:
            self.cxy[(x, y)] = self.cxy.get((x, y), 0) + 1
            self.cyz[(y, z)] = self.cyz.get((y, z), 0) + 1
        # seam-0 aux families
        self.m01 = {y: set(x for x in Bs[0] if 2 * y - x in S1)
                    for y in Bs[1]}                       # (x, y, z in B1)
        self.k3 = {u: set(z for x in Bs[0] if x < u
                          for z in (2 * u - x,)
                          if z in S1 or z in S2)
                   for u in Bs[0]}                        # (x, u, z)
        self.k4bad = set(w for w in Bs[1]
                         if any(2 * y - w in S2 for y in Bs[1] if y > w))
        self.k5 = {u: set(y for y in Bs[1] if 2 * y - u in S2)
                   for u in Bs[0]}                        # (u, y, z) = N_H(u)
        # seam-1 aux families
        self.m1w = {w: set(y for y in Bs[1] if 2 * y - w in S0)
                    for w in Bs[2]}                       # (x, y, w)
        self.k3p_nonempty = set(
            u for u in Bs[1]
            if any(2 * y - u in S0 for y in Bs[1] if y < u))  # (x, y, u)
        self.k2pb_nonempty = set(
            w for w in Bs[2]
            if any(2 * w - x in S2 and 2 * w - x != w
                   for x in Bs[0]))                       # (x, w, z)
        self.k3pb = {u: set(z for x in Bs[0]
                            for z in (2 * u - x,) if z in S2)
                     for u in Bs[1]}                      # (x, u, z)
        self.k4p = {w: set(y for y in Bs[1] if 2 * w - y in S2 and y != w)
                    for w in Bs[2]}                       # (y, w, z)
        self.k5p = {u: set(z for y in Bs[1] if y < u
                           for z in (2 * u - y,) if z in S2)
                    for u in Bs[1]}                       # (y, u, z)

    @staticmethod
    def _sub1(s, a):
        return len(s) == 0 or (len(s) == 1 and a in s)

    def survives(self, u, w, seam):
        if seam == 0:
            if self.cntH != self.cxy.get((u, w), 0):
                return False
            return (self._sub1(self.m01[w], u)
                    and self._sub1(self.k3[u], w)
                    and w not in self.k4bad
                    and self._sub1(self.k5[u], w))
        if self.cntH != self.cyz.get((u, w), 0):
            return False
        return (self._sub1(self.m1w[w], u)
                and u not in self.k3p_nonempty
                and w not in self.k2pb_nonempty
                and self._sub1(self.k3pb[u], w)
                and self._sub1(self.k4p[w], u)
                and self._sub1(self.k5p[u], w))


def partMINTLOC():
    ws = load_witnesses()
    res = {}
    for tag, (hor, A) in ws.items():
        if tag == "pureL3":
            anchors = (32, 64)
        else:
            anchors = (32, 64, 128)
        for m in anchors:
            if 8 * m > hor:
                continue
            for team in ("A", "B"):
                t0 = time.time()
                Bs = team_sets(hor, A, m, team)
                W = sorted(v for b in Bs for v in b)
                tset = set(W)
                APs = in_team_APs(W, tset)
                H = Hfam(*Bs)
                # budget-0 control
                v0 = solve_rigid(Bs, None, tset, APs)
                cands = ([(u, w, 0) for u in Bs[0] for w in Bs[1]] +
                         [(u, w, 1) for u in Bs[1] for w in Bs[2]])
                ff = FastFilter(Bs, tset, H)
                surv = [c for c in cands if ff.survives(*c)]
                # cross-validate fast filter vs exact slow filter on a
                # deterministic sample + all survivors
                import random
                rnd = random.Random(185)
                sample = (rnd.sample(cands, min(150, len(cands)))
                          + surv[:100])
                xval_fail = 0
                for (u, w, s) in sample:
                    slow = kfilter_slow(Bs, APs, u, w, s) is None
                    if slow != ff.survives(u, w, s):
                        xval_fail += 1
                        log(f"[MINTLOC][XVAL-FAIL] {tag} m={m} T={team} "
                            f"cand=({u},{w},s{s}) slow={slow}")
                sat_region = []
                solved = 0
                big = max(len(b) for b in Bs) > 220
                for (u, w, s) in surv[:400]:
                    if big:
                        log(f"[MINTLOC] {tag} m={m} T={team}: survivor "
                            f"({u},{w},s{s}) UNSOLVED (blocks too large)")
                        continue
                    v = solve_rigid(Bs, (u, w, s), tset, APs)
                    solved += 1
                    if v == "SAT":
                        # displaced value u location vs minority material
                        blk = blocks3(m)[s]
                        cAb = sum(1 for x in blk if x in A)
                        mt = "A" if 2 * cAb <= len(blk) else "B"
                        minv = [x for x in blk
                                if ((x in A) == (mt == "A")) and x != u]
                        dmin = min((abs(u - x) for x in minv), default=None)
                        sat_region.append({"u": u, "w": w, "seam": s,
                                           "u_mod4": u % 4,
                                           "u_dist_minority": dmin,
                                           "u_team_is_minority": team == mt})
                row = {"m": m, "team": team, "H": len(H),
                       "budget0": v0, "n_cands": len(cands),
                       "k_survivors": len(surv), "solved": solved,
                       "sat_region_size": len(sat_region),
                       "sat_region": sat_region[:40],
                       "xval_fail": xval_fail,
                       "secs": round(time.time() - t0, 1)}
                res[f"{tag}_m{m}_{team}"] = row
                log(f"[MINTLOC] {tag} m={m} T={team}: budget0={v0} "
                    f"|H|={len(H)} cands={len(cands)} "
                    f"Ksurv={len(surv)} SATregion={len(sat_region)} "
                    f"xvalfail={xval_fail} [{row['secs']}s]")
                OUT["partMINTLOC"] = res
                dump()


# -------------------------------------------------------------------- nu

def nu_scan(Bs, budgets, deadline=None):
    """Per-team theory: full order vars over W, transitivity, AP bans,
    adjacent-seam inversion indicators, totalizer scan."""
    W = [v for b in Bs for v in b]
    tset = set(W)
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

    cls = []
    for (x, y, z) in in_team_APs(sorted(W), tset):
        cls.append([-o(x, y), -o(y, z)])
        cls.append([-o(z, y), -o(y, x)])
    for i in range(n):
        for j in range(i + 1, n):
            oij = ovar[(i, j)]
            for k in range(j + 1, n):
                cls.append([-oij, -ovar[(j, k)], ovar[(i, k)]])
                cls.append([oij, ovar[(j, k)], -ovar[(i, k)]])
    xlits = []
    for si in (0, 1):
        for u in Bs[si]:
            for w in Bs[si + 1]:
                top += 1
                cls.append([o(u, w), top])     # inverted => indicator
                xlits.append(top)
    sol = Cadical195(bootstrap_with=cls)
    tot = ITotalizer(lits=xlits, ubound=max(budgets) + 1, top_id=top)
    sol.append_formula(tot.cnf.clauses)
    out = []
    for b in budgets:
        if deadline and time.time() > deadline:
            out.append((b, "SKIP-time"))
            continue
        t0 = time.time()
        ok = sol.solve(assumptions=[-tot.rhs[b]])
        out.append((b, "SAT" if ok else "UNSAT", round(time.time() - t0, 1)))
        if ok:
            break
    sol.delete()
    tot.delete()
    return out


def partNU():
    ws = load_witnesses()
    res = {}
    jobs = []
    for tag in ("h4096_F64", "h4096_lin4", "h8192_F64"):
        if tag in ws:
            jobs.append((tag, 32, ("A", "B"), (0, 1, 2, 4, 8, 12)))
            jobs.append((tag, 64, ("A", "B"), (0, 2, 8, 12)))
    jobs.append(("pureL3", 16, ("A", "B"),
                 tuple(range(0, 25))))
    jobs.append(("pureL3", 32, ("A", "B"), (0, 4, 12, 24)))
    for tag, m, teams, budgets in jobs:
        hor, A = ws[tag]
        if 8 * m > hor:
            continue
        for team in teams:
            Bs = team_sets(hor, A, m, team)
            n = sum(len(b) for b in Bs)
            if n > 260:
                log(f"[NU] {tag} m={m} T={team}: n={n} SKIP (too large "
                    f"for local scan)")
                continue
            t0 = time.time()
            rows = nu_scan(Bs, list(budgets),
                           deadline=time.time() + 2400)
            res[f"{tag}_m{m}_{team}"] = {"n": n, "scan": rows,
                                         "secs": round(time.time()-t0, 1)}
            log(f"[NU] {tag} m={m} T={team} n={n}: {rows} "
                f"[{round(time.time()-t0,1)}s]")
            OUT["partNU"] = res
            dump()


PARTS = {"census": partCENSUS, "mintloc": partMINTLOC, "nu": partNU}


# ---------------------------------------------------------------- s5alt

def partS5ALT(hor=4096, F=12, u0=32, budget=3600.0, orbit_on=True,
              diffuse_on=True, alt_from=6):
    """e179 s5dodger verbatim + forced designation alternation
    mA_t != mA_{t+1} for t >= alt_from (notes/80-pincer SS3.5);
    orbit_on/diffuse_on controls for attribution."""
    from ortools.sat.python import cp_model
    t0 = time.time()
    D, gmode = 2, "lin4"
    mdl = cp_model.CpModel()
    A = {v: mdl.NewBoolVar(f"A{v}") for v in range(1, hor + 1)}

    def team(t, v):
        return A[v] if t == "A" else A[v].Not()

    t_lo, t_hi = 5, hor.bit_length() - 2
    mAs = {}
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
        mAs[t] = mA
        for v in blk:
            for g in (1, 2):
                if v + g <= blk[-1]:
                    mdl.AddBoolOr([A[v].Not(), A[v + g].Not(), mA.Not()])
                    mdl.AddBoolOr([A[v], A[v + g], mA])
    # THE new constraint: designation alternates from alt_from up
    # (maxrun=1); maxrun=R: every window of R+1 consecutive blocks
    # contains both designations (no ownership run longer than R)
    R = globals().get("_MAXRUN", 1)
    for t in range(alt_from, t_hi - R + 1):
        win = [mAs[s_] for s_ in range(t, t + R + 1)]
        mdl.Add(sum(win) >= 1)
        mdl.Add(sum(win) <= R)
    S = {0: mdl.NewConstant(0)}
    for v in range(1, hor + 1):
        S[v] = mdl.NewIntVar(0, v, f"S{v}")
        mdl.Add(S[v] == S[v - 1] + A[v])
    if diffuse_on:
        for a in range(32, hor // 2 + 1):
            g = a // 4
            cA = S[2 * a] - S[a]
            mdl.Add(cA >= g)
            mdl.Add(cA <= a - g)
    for tname in ("A", "B") if orbit_on else ():
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
                                   team(tname, w).Not(), reach[(1, w)]])
                for d in range(2, D + 1):
                    mdl.AddBoolOr([reach[(d - 1, v)].Not(),
                                   team(tname, f).Not(),
                                   team(tname, w).Not(), reach[(d, w)]])
        for v in range(1, hor + 1):
            mdl.Add(reach[(D, v)] == 0)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = budget
    solver.parameters.num_search_workers = 8
    st = solver.Solve(mdl)
    name = {cp_model.OPTIMAL: "SAT", cp_model.FEASIBLE: "SAT",
            cp_model.INFEASIBLE: "UNSAT"}.get(st, "TIMEOUT")
    row = {"part": "s5alt", "hor": hor, "D": D, "F": F, "u0": u0,
           "gmode": gmode, "alt_from": alt_from, "verdict": name,
           "orbit": orbit_on, "diffuse": diffuse_on,
           "maxrun": globals().get("_MAXRUN", 1),
           "secs": round(time.time() - t0, 1)}
    if name == "SAT":
        col = [v for v in range(1, hor + 1) if solver.Value(A[v])]
        fl = (f"e185_s5alt_h{hor}_F{F}_r{globals().get('_MAXRUN', 1)}"
              f"{'' if orbit_on else '_noorb'}"
              f"{'' if diffuse_on else '_nodiff'}_a{alt_from}.json")
        out = os.path.join(BASE, fl)
        json.dump({"hor": hor, "D": D, "F": F, "A": col}, open(out, "w"))
        row["witness"] = out
        row["nA"] = len(col)
        row["ownership"] = [("A" if solver.Value(mAs[t]) else "B")
                            for t in range(t_lo, t_hi + 1)]
    log(f"[S5ALT] {json.dumps(row)}")
    OUT.setdefault("partS5ALT", []).append(row)
    dump()


PARTS["s5alt"] = lambda: [partS5ALT(F=12, u0=32), partS5ALT(F=64, u0=64)]
def _runvar(R, **kw):
    globals()["_MAXRUN"] = R
    try:
        partS5ALT(**kw)
    finally:
        globals()["_MAXRUN"] = 1


PARTS["s5run"] = lambda: [
    _runvar(2, F=12, u0=32),
    _runvar(3, F=12, u0=32),
    _runvar(2, F=64, u0=64),
]
PARTS["s5altctl"] = lambda: [
    partS5ALT(F=12, u0=32, orbit_on=False),
    partS5ALT(F=12, u0=32, diffuse_on=False),
    partS5ALT(F=12, u0=32, alt_from=7),
    partS5ALT(hor=2048, F=12, u0=32),
]


if __name__ == "__main__":
    want = sys.argv[1:] or ["all"]
    names = list(PARTS) if want == ["all"] else want
    for nm in names:
        t0 = time.time()
        PARTS[nm]()
        log(f"[{nm}] done {round(time.time()-t0,1)}s")
