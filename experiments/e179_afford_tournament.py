"""e179_afford_tournament: machine attacks for the five AFFORD strategies
(notes/79).  Subcommands:

  s1lemma   L-DOUBLE-DUTY check.  4-block gadget (M/2, 8M], team A forced
            to have a double-duty value u in B0 (high member of an
            inverted s0 pair AND low member of an inverted s1 pair);
            budget b on A's s0+s1 total.  Lemma predicts UNSAT for
            b < |B0 cap A| (= M/2 at bal), SAT at b >= M/2 (transitivity
            forces every B0-value of A to pay).  Scan b around M/2 at
            M = 8, 16.

  s2band    mint band map at M = 8, v = 11 (= v_min(0)(8) - 1).  Base
            cell (11, 0) is UNSAT.  Relax: s1 stays 0, s2 <= 11, s0
            inversions ALLOWED but only when the pair's low member u'
            lies in band B (subset of Bm1); all other s0 pairs banned.
            Scan B = each singleton of Bm1, plus top-half / bottom-half.
            SAT for band B  <=>  the mint can be minted on B.

  s3rot     payer identity at fresh scales: ROT4-colored coupled core
            (e131 part_coupled verbatim geometry) at m = 48, 80 --
            which team's double-block-order pattern fails.

  s4core    sparse-minority coupled core.  3 blocks (m,2m],(2m,4m],
            (4m,8m], both teams, per-team per-block lower bound k,
            block order at both seams for both teams (all seam
            inversions banned), PLUS: for a designation vector
            d in {A,B}^3, team d_i is the block-i minority
            (card <= floor(|blk_i|/2)) and is pair-sparse in block i
            (no two values at distance 1 or 2).  Cell verdict = UNSAT
            iff all 8 designations UNSAT.  Cells from CLI: --m, --k.

  s5dodger  CP-SAT dodger build on [1, 4096] (or --hor): (i) censored
            chain depth < D for reflectors <= F, both teams (reach-var
            encoding, lower-bound implications only); (ii) window
            floor: min-team count >= g(a) for every ratio-2 window
            (a, 2a], 32 <= a <= hor/2 (prefix-sum ints);
            (iii) per-dyadic-block minority pair-sparse (reified);
            everywhere-split floor f(t).  --D, --F configurable.

Artifacts: data/e179_afford.jsonl (stream), data/e179_<part>*.json.
Terse streams.
"""
import argparse
import json
import math
import os
import sys
import time

from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical195

BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
JL = os.path.join(BASE, "e179_afford.jsonl")


def stream(row):
    row["ts"] = round(time.time(), 1)
    with open(JL, "a") as f:
        f.write(json.dumps(row) + "\n")
    print(json.dumps(row), flush=True)


# ---------------------------------------------------------------- core SAT kit

class Enc:
    """Complete two-team encoding over given blocks: order vars per team,
    guarded AP clauses (whole range), full transitivity, membership ai
    (True = A).  Balance or explicit per-block cards added by caller."""

    def __init__(self, blocks):
        self.blocks = blocks
        self.V = [v for blk in blocks for v in blk]
        self.n = len(self.V)
        self.idx = {v: i for i, v in enumerate(self.V)}
        self.top = 0
        self.offA = self._mk()
        self.offB = self._mk()
        self.ai = {}
        for v in self.V:
            self.top += 1
            self.ai[v] = self.top
        self.cls = []
        Vs = set(self.V)
        for lit, g in ((self.litA, lambda v: -self.ai[v]),
                       (self.litB, lambda v: self.ai[v])):
            for b in self.V:
                for d in range(1, min(b - self.V[0], self.V[-1] - b) + 1):
                    a, c = b - d, b + d
                    if a in Vs and c in Vs:
                        gg = [g(a), g(b), g(c)]
                        self.cls.append(gg + [-lit(a, b), -lit(b, c)])
                        self.cls.append(gg + [lit(a, b), lit(b, c)])
        for off in (self.offA, self.offB):
            for i in range(self.n):
                for j in range(i + 1, self.n):
                    xij = off[(i, j)]
                    for k in range(j + 1, self.n):
                        self.cls.append([-xij, -off[(j, k)], off[(i, k)]])
                        self.cls.append([xij, off[(j, k)], -off[(i, k)]])

    def _mk(self):
        off = {}
        for i in range(self.n):
            for j in range(i + 1, self.n):
                self.top += 1
                off[(i, j)] = self.top
        return off

    def _lit(self, off, u, w):
        i, j = self.idx[u], self.idx[w]
        return off[(i, j)] if i < j else -off[(j, i)]

    def litA(self, u, w):
        return self._lit(self.offA, u, w)

    def litB(self, u, w):
        return self._lit(self.offB, u, w)

    def lit(self, team, u, w):
        return self.litA(u, w) if team == "A" else self.litB(u, w)

    def inteam(self, team, v):        # literal: v in team
        return self.ai[v] if team == "A" else -self.ai[v]

    def guard(self, team, v):         # clause guard: satisfied if v NOT in team
        return -self.inteam(team, v)

    def seam_pairs(self, i):
        return [(u, w) for u in self.blocks[i] for w in self.blocks[i + 1]]

    def xvars(self, team, seam_idx):
        """One-way inversion indicators for a seam; returns list of vars."""
        out = []
        for (u, w) in self.seam_pairs(seam_idx):
            self.top += 1
            x = self.top
            self.cls.append([self.guard(team, u), self.guard(team, w),
                             self.lit(team, u, w), x])
            out.append(x)
        return out

    def ban_seam(self, team, seam_idx, allow_low=()):
        """Ban inverted seam pairs for team, except pairs whose LOW member
        is in allow_low."""
        allow = set(allow_low)
        for (u, w) in self.seam_pairs(seam_idx):
            if u in allow:
                continue
            self.cls.append([self.guard(team, u), self.guard(team, w),
                             self.lit(team, u, w)])

    def card_atmost(self, lits, bound):
        if bound <= 0:
            self.cls += [[-l] for l in lits]
            return
        enc = CardEnc.atmost(lits=lits, bound=bound, top_id=self.top,
                             encoding=EncType.seqcounter)
        self.top = max(self.top, enc.nv)
        self.cls += enc.clauses

    def card_atleast(self, lits, bound):
        enc = CardEnc.atleast(lits=lits, bound=bound, top_id=self.top,
                              encoding=EncType.seqcounter)
        self.top = max(self.top, enc.nv)
        self.cls += enc.clauses

    def balance(self):
        for blk in self.blocks:
            base = math.ceil(len(blk) / 2)
            for sgn in (1, -1):
                self.card_atleast([sgn * self.ai[v] for v in blk], base)

    def solve(self, tb=None):
        t0 = time.time()
        with Cadical195(bootstrap_with=self.cls) as s:
            ok = s.solve()
            el = round(time.time() - t0, 1)
            model = set(l for l in s.get_model() if l > 0) if ok else None
        return ("SAT" if ok else "UNSAT"), el, model


def dyadic4(M):
    return [list(range(M // 2 + 1, M + 1)),
            list(range(M + 1, 2 * M + 1)),
            list(range(2 * M + 1, 4 * M + 1)),
            list(range(4 * M + 1, 8 * M + 1))]


def dyadic3(m):
    return [list(range(m + 1, 2 * m + 1)),
            list(range(2 * m + 1, 4 * m + 1)),
            list(range(4 * m + 1, 8 * m + 1))]


# ------------------------------------------------------------------- s1lemma

def s1lemma(Ms, budgets):
    for M in Ms:
        blocks = dyadic4(M)
        Bm1, B0 = blocks[0], blocks[1]
        u = B0[len(B0) // 2 - 1]          # a mid value of B0
        halfB0 = len(B0) // 2             # |B0 cap A| at balance
        for b in budgets(halfB0):
            e = Enc(blocks)
            e.balance()
            # force u in A
            e.cls.append([e.ai[u]])
            # d1: u is HIGH member of an inverted s0 pair (u', u): u before u'
            d1s = []
            for up in Bm1:
                e.top += 1
                d = e.top
                e.cls.append([-d, e.ai[up]])
                e.cls.append([-d, e.litA(u, up)])   # u placed before u' (< u)
                d1s.append(d)
            e.cls.append(d1s)
            # d2: u is LOW member of an inverted s1 pair (u, w): w before u
            d2s = []
            for w in blocks[2]:
                e.top += 1
                d = e.top
                e.cls.append([-d, e.ai[w]])
                e.cls.append([-d, e.litA(w, u)])
                d2s.append(d)
            e.cls.append(d2s)
            # budget on A's s0+s1 inversions
            lits = e.xvars("A", 0) + e.xvars("A", 1)
            e.card_atmost(lits, b)
            verdict, el, _ = e.solve()
            stream({"part": "s1lemma", "M": M, "u": u, "budget": b,
                    "halfB0": halfB0, "verdict": verdict, "secs": el})


# -------------------------------------------------------------------- s2band

def s2band(M, v, bands):
    blocks = dyadic4(M)
    Bm1 = blocks[0]
    for name, B in bands(Bm1):
        e = Enc(blocks)
        e.balance()
        for team in ("A", "B"):
            e.ban_seam(team, 0, allow_low=B)     # s0: only band-low mints
            e.ban_seam(team, 1)                  # s1 = 0
            e.card_atmost(e.xvars(team, 2), v)   # s2 <= v
        verdict, el, _ = e.solve()
        stream({"part": "s2band", "M": M, "v": v, "band": name,
                "B": sorted(B), "verdict": verdict, "secs": el})


# --------------------------------------------------------------------- s3rot

def octave(v):
    m = v.bit_length() - 1
    if v == 1 << m:
        m -= 1
    return m


def rot4_isA(v):
    if v <= 1:
        return True
    m = octave(v)
    p = v - (1 << m) - 1
    q = (p * 4) >> m
    return (q - m) % 4 in (0, 1)


def s3rot(ms):
    for m in ms:
        t0 = time.time()
        W = list(range(m + 1, 8 * m + 1))
        res = {}
        for team, isT in (("A", True), ("B", False)):
            vals = [x for x in W if rot4_isA(x) == isT]
            idx = {x: i for i, x in enumerate(vals)}
            n = len(vals)
            var = {}
            c = 0
            for p in range(n):
                for q in range(p + 1, n):
                    c += 1
                    var[(p, q)] = c

            def o(a, b):
                p, q = idx[a], idx[b]
                return var[(p, q)] if p < q else -var[(q, p)]

            cl = []
            vset = set(vals)
            for y in vals:
                d = 1
                while y + d <= 8 * m and y - d > m:
                    a, b = y - d, y + d
                    if a in vset and b in vset:
                        cl.append([-o(a, y), -o(y, b)])
                        cl.append([-o(b, y), -o(y, a)])
                    d += 1
            for p in range(n):
                for q in range(p + 1, n):
                    vpq = var[(p, q)]
                    for r in range(q + 1, n):
                        cl.append([-vpq, -var[(q, r)], var[(p, r)]])
                        cl.append([vpq, var[(q, r)], -var[(p, r)]])
            B0 = [x for x in vals if x <= 2 * m]
            B1 = [x for x in vals if 2 * m < x <= 4 * m]
            B2 = [x for x in vals if x > 4 * m]
            for a in B0:
                for b in B1:
                    cl.append([o(a, b)])
            for a in B1:
                for b in B2:
                    cl.append([o(a, b)])
            sol = Cadical195(bootstrap_with=cl)
            sat = sol.solve()
            sol.delete()
            res[team] = "SAT" if sat else "UNSAT"
        stream({"part": "s3rot", "m": m, "verdicts": res,
                "secs": round(time.time() - t0, 1)})


# -------------------------------------------------------------------- s4core

def s4core(m, k, designations=None, mode="sparse"):
    """mode: 'sparse' = minority cap + pair-sparse; 'cap' = minority cap
    only (control); 'none' = bare const core (control, single run)."""
    blocks = dyadic3(m)
    # global team-swap symmetry: d and its complement are isomorphic
    desigs = designations or ["AAA", "AAB", "ABA", "ABB"]
    if mode == "none":
        desigs = ["---"]
    cell = []
    for d in desigs:
        e = Enc(blocks)
        # per-team per-block lower bounds k
        for blk in blocks:
            for team in ("A", "B"):
                e.card_atleast([e.inteam(team, v) for v in blk], k)
        # block order both seams both teams
        for team in ("A", "B"):
            e.ban_seam(team, 0)
            e.ban_seam(team, 1)
        # minority designation: team d_i minority (+ pair-sparse) in block i
        if mode != "none":
            for i, blk in enumerate(blocks):
                t = d[i]
                e.card_atmost([e.inteam(t, v) for v in blk], len(blk) // 2)
                if mode in ("sparse", "sparse1"):
                    gaps = (1, 2) if mode == "sparse" else (1,)
                    for v in blk:
                        for g in gaps:
                            if v + g <= blk[-1]:
                                e.cls.append([-e.inteam(t, v),
                                              -e.inteam(t, v + g)])
        verdict, el, model = e.solve()
        row = {"part": "s4core", "m": m, "k": k, "mode": mode, "desig": d,
               "verdict": verdict, "secs": el}
        if verdict == "SAT" and model is not None:
            colA = [v for v in e.V if e.ai[v] in model]
            row["sizesA"] = [len([v for v in blk if v in set(colA)])
                             for blk in blocks]
        stream(row)
        cell.append(verdict)
    stream({"part": "s4core", "m": m, "k": k, "mode": mode, "desig": "CELL",
            "verdict": "UNSAT" if all(v == "UNSAT" for v in cell) else "SAT",
            "detail": cell})


# ------------------------------------------------------------------ s5dodger

def s5dodger(hor, D, F, gmode, fmode, budget, sparse_on=True, orbit_on=True,
             diffuse_on=True, u0=32):
    from ortools.sat.python import cp_model
    t0 = time.time()
    mdl = cp_model.CpModel()
    A = {v: mdl.NewBoolVar(f"A{v}") for v in range(1, hor + 1)}

    def team(t, v):
        return A[v] if t == "A" else A[v].Not()

    # (iii) + everywhere-split on dyadic blocks
    t_lo = 5
    t_hi = hor.bit_length() - 2          # blocks (2^t, 2^{t+1}] inside hor
    for t in range(t_lo, t_hi + 1):
        blk = list(range((1 << t) + 1, (1 << (t + 1)) + 1))
        cntA = mdl.NewIntVar(0, len(blk), f"cA{t}")
        mdl.Add(cntA == sum(A[v] for v in blk))
        if fmode == "slow":
            f = max(2, t - 5)
        else:
            f = 2
        mdl.Add(cntA >= f)
        mdl.Add(cntA <= len(blk) - f)
        if sparse_on:
            mA = mdl.NewBoolVar(f"mA{t}")    # A is minority in block t
            mdl.Add(2 * cntA <= len(blk)).OnlyEnforceIf(mA)
            mdl.Add(2 * cntA >= len(blk)).OnlyEnforceIf(mA.Not())
            for v in blk:
                for g in (1, 2):
                    if v + g <= blk[-1]:
                        mdl.AddBoolOr([A[v].Not(), A[v + g].Not(),
                                       mA.Not()])
                        mdl.AddBoolOr([A[v], A[v + g], mA])
    # (ii) window floor via prefix sums
    S = {0: mdl.NewConstant(0)}
    for v in range(1, hor + 1):
        S[v] = mdl.NewIntVar(0, v, f"S{v}")
        mdl.Add(S[v] == S[v - 1] + A[v])
    if diffuse_on:
        for a in range(32, hor // 2 + 1):
            w = 2 * a - a
            if gmode == "log":
                g = max(2, a.bit_length() - 5)
            elif gmode == "lin4":
                g = a // 4
            elif gmode == "lin8":
                g = a // 8
            else:
                g = 2
            cA = S[2 * a] - S[a]
            mdl.Add(cA >= g)
            mdl.Add(cA <= w - g)
    # (i) censored chain depth: reach vars
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
                # depth-1 step v -> w (v, f, w all in team); seed floor u0
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
    solver.parameters.log_search_progress = False
    st = solver.Solve(mdl)
    name = {cp_model.OPTIMAL: "SAT", cp_model.FEASIBLE: "SAT",
            cp_model.INFEASIBLE: "UNSAT"}.get(st, "TIMEOUT")
    row = {"part": "s5dodger", "hor": hor, "D": D, "F": F,
           "gmode": gmode, "fmode": fmode, "verdict": name,
           "sparse": sparse_on, "orbit": orbit_on, "diffuse": diffuse_on,
           "u0": u0,
           "secs": round(time.time() - t0, 1)}
    if name == "SAT":
        col = [v for v in range(1, hor + 1) if solver.Value(A[v])]
        out = os.path.join(BASE, f"e179_s5_witness_h{hor}_D{D}F{F}_{gmode}.json")
        with open(out, "w") as fo:
            json.dump({"hor": hor, "D": D, "F": F, "A": col}, fo)
        row["witness"] = out
        row["nA"] = len(col)
    stream(row)


# ---------------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["s1lemma", "s2band", "s3rot", "s4core",
                                    "s5dodger", "s4price"])
    ap.add_argument("--M", type=int, default=8)
    ap.add_argument("--v", type=int, default=11)
    ap.add_argument("--m", type=int, default=16)
    ap.add_argument("--k", type=int, default=1)
    ap.add_argument("--ms", type=str, default="48")
    ap.add_argument("--Ms", type=str, default="8")
    ap.add_argument("--budgets", type=str, default="")
    ap.add_argument("--desigs", type=str, default="")
    ap.add_argument("--hor", type=int, default=4096)
    ap.add_argument("--D", type=int, default=2)
    ap.add_argument("--F", type=int, default=12)
    ap.add_argument("--gmode", type=str, default="log")
    ap.add_argument("--fmode", type=str, default="slow")
    ap.add_argument("--budget", type=float, default=3600.0)
    ap.add_argument("--mode", type=str, default="sparse",
                    choices=["sparse", "sparse1", "cap", "none"])
    ap.add_argument("--sparse_off", action="store_true")
    ap.add_argument("--orbit_off", action="store_true")
    ap.add_argument("--diffuse_off", action="store_true")
    ap.add_argument("--u0", type=int, default=32)
    args = ap.parse_args()
    if args.cmd == "s1lemma":
        Ms = [int(x) for x in args.Ms.split(",")]
        if args.budgets:
            bs = [int(x) for x in args.budgets.split(",")]
            s1lemma(Ms, lambda h: bs)
        else:
            s1lemma(Ms, lambda h: [h - 1, h])
    elif args.cmd == "s2band":
        M = args.M
        def bands(Bm1):
            yield "none", []
            for u in Bm1:
                yield f"u{u}", [u]
            half = len(Bm1) // 2
            yield "bottomhalf", Bm1[:half]
            yield "tophalf", Bm1[half:]
            yield "all", Bm1[:]
        s2band(M, args.v, bands)
    elif args.cmd == "s3rot":
        s3rot([int(x) for x in args.ms.split(",")])
    elif args.cmd == "s4core":
        ds = args.desigs.split(",") if args.desigs else None
        s4core(args.m, args.k, ds, args.mode)
    elif args.cmd == "s4price":
        s4price(args.M, sparse_on=not args.sparse_off)
    elif args.cmd == "s5dodger":
        s5dodger(args.hor, args.D, args.F, args.gmode, args.fmode,
                 args.budget, sparse_on=not args.sparse_off,
                 orbit_on=not args.orbit_off,
                 diffuse_on=not args.diffuse_off, u0=args.u0)




# ------------------------------------------------------- s4price (escalation)

def s4price(M, sparse_on=True, maxb=24):
    """e121 price_curve verbatim + optional pair-sparse constraint on the
    donation set (B-colored values in (M, 2M]): p_sparse(k) vs p(k)."""
    from pysat.card import ITotalizer
    pairs = [(15, 16), (31, 32), (23, 24), (47, 48)]
    V = list(range(M + 1, 2 * M + 1))
    n = len(V)
    idx = {v: i for i, v in enumerate(V)}
    for k in range(1, len(pairs) + 1):
        atk = [x for p in pairs[:k] for x in p]
        var = 0
        col = {}
        for v in V + atk:
            var += 1
            col[v] = var
        ov = {'A': {}, 'B': {}}
        for T in ('A', 'B'):
            for i in range(n):
                for j in range(i + 1, n):
                    var += 1
                    ov[T][(i, j)] = var

        def o(T, u, w):
            i, j = idx[u], idx[w]
            return ov[T][(i, j)] if i < j else -ov[T][(j, i)]

        def notT(T, v):
            return -col[v] if T == 'A' else col[v]

        cl = []
        for y in V:
            d = 1
            while y + d <= 2 * M:
                x, z = y - d, y + d
                d += 1
                if x > M:
                    for T in ('A', 'B'):
                        g = [notT(T, x), notT(T, y), notT(T, z)]
                        cl.append(g + [-o(T, x, y), -o(T, y, z)])
                        cl.append(g + [-o(T, z, y), -o(T, y, x)])
        for x in atk:
            for j in range(1, x // 2 + 1):
                y, z = M + j, 2 * M + 2 * j - x
                if M < z <= 2 * M and M < y <= 2 * M:
                    cl.append([notT('A', y), notT('A', z), o('A', z, y)])
        for T in ('A', 'B'):
            for i in range(n):
                for j in range(i + 1, n):
                    oij = ov[T][(i, j)]
                    for kk in range(j + 1, n):
                        cl.append([-oij, -ov[T][(j, kk)], ov[T][(i, kk)]])
                        cl.append([oij, ov[T][(j, kk)], -ov[T][(i, kk)]])
        cl += [[col[x]] for x in atk]
        if sparse_on:                     # donation set pair-sparse
            for v in V:
                for g in (1, 2):
                    if v + g <= 2 * M:
                        cl.append([col[v], col[v + g]])
        don = [-col[v] for v in V]
        sol = Cadical195(bootstrap_with=cl)
        tot = ITotalizer(lits=don, ubound=min(maxb, len(don)), top_id=var)
        sol.append_formula(tot.cnf.clauses)
        t0 = time.time()
        p = None
        witness = None
        for b in range(0, maxb + 1):
            assum = [-tot.rhs[b]] if b < len(tot.rhs) else []
            if sol.solve(assumptions=assum):
                model = set(l for l in sol.get_model() if l > 0)
                witness = sorted(v for v in V if col[v] not in model)
                p = b
                break
        stream({"part": "s4price", "M": M, "k": k, "sparse": sparse_on,
                "p": p, "witness": witness,
                "secs": round(time.time() - t0, 1)})
        sol.delete()
        tot.delete()
        if p is None:
            break


if __name__ == "__main__":
    main()
