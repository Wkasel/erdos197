"""e174 — band-floor extremal measurements for notes/72 (FRONT
VMIN0-GROWTH).

Coloring-only instruments for the (v,0) pump cell's sumset floor (F)
(notes/72 s.3): NO orders, NO budgets — pure extremal combinatorics
of the three demand channels

    mu_dn   = # AP triples in W x U x Y   (W=Bm1&T, U=B0&T, Y=B1&T)
    mu_up   = # AP triples in U x Y x X   (X=B2&T)
    mu_skip = # AP triples in W x Y x X

over 2-colorings of (M/2, 8M] with exact per-block balance, subject
to the T-CHAN hard constraint mu_dn(A) = mu_dn(B) = 0.

Parts:
  midcheck — Lemma L-MID verification: is there a balanced (U, W)
             for ONE team-side with (2U - W) & (2M, 3M] empty?
             Expected UNSAT (lemma true).  Single-team relaxation of
             the coloring problem (W, U free subsets of quota size).
  zeroset  — is there a balanced coloring, mu_dn = 0 both teams,
             mu_up + mu_skip = 0 both teams, DIFFERENT from the two
             parity-schedule colorings (x,x,1-x,1-x)?
  floor    — f_M(d) = min over balanced mu_dn=0 colorings at Hamming
             distance >= d from BOTH schedule colorings of
             max_T (mu_up + mu_skip)(T); reported with the argmin
             anatomy.  d = 0 sanity row must be 0 via the schedule.
  fhalf    — notes/71's f(M): min over balanced mu_dn=0 colorings
             that are NOT low-pure (team A's Bm1+B0 part contains
             both parities) of max_T (mu_up + mu_skip)(T).
             [GAP-FHALF] claims f(M) >= M/2; notes/71 measured
             f = 4/6/8 at M = 8/12/16.  This part extends the
             ladder.

Records: data/e174_band_floor.jsonl (one row per query).
"""
import json
import sys
import time

from ortools.sat.python import cp_model

OUT = "data/e174_band_floor.jsonl"


def blocks(M):
    Bm1 = list(range(M // 2 + 1, M + 1))
    B0 = list(range(M + 1, 2 * M + 1))
    B1 = list(range(2 * M + 1, 4 * M + 1))
    B2 = list(range(4 * M + 1, 8 * M + 1))
    return Bm1, B0, B1, B2


def triples(lo_blk, mid_blk, hi_blk):
    """AP triples (a, b, 2b-a) with a in lo, b in mid, 2b-a in hi."""
    hi = set(hi_blk)
    out = []
    for a in lo_blk:
        for b in mid_blk:
            c = 2 * b - a
            if c in hi:
                out.append((a, b, c))
    return out


def emit(row):
    with open(OUT, "a") as f:
        f.write(json.dumps(row) + "\n")
    print(row, flush=True)


def part_midcheck(Ms):
    """L-MID: exists balanced U in B0 (|U|=M/2), W in Bm1 (|W|=M/4)
    with (2U - W) disjoint from (2M, 3M]?  UNSAT = lemma holds."""
    for M in Ms:
        Bm1, B0, _, _ = blocks(M)
        m = cp_model.CpModel()
        u = {v: m.NewBoolVar(f"u{v}") for v in B0}
        w = {v: m.NewBoolVar(f"w{v}") for v in Bm1}
        m.Add(sum(u.values()) == M // 2)
        m.Add(sum(w.values()) == M // 4)
        nfor = 0
        for a in B0:
            for b in Bm1:
                if 2 * M < 2 * a - b <= 3 * M:
                    m.AddBoolOr([u[a].Not(), w[b].Not()])
                    nfor += 1
        sol = cp_model.CpSolver()
        sol.parameters.max_time_in_seconds = 600
        t0 = time.time()
        st = sol.Solve(m)
        verdict = {cp_model.OPTIMAL: "SAT", cp_model.FEASIBLE: "SAT",
                   cp_model.INFEASIBLE: "UNSAT"}.get(st, "UNKNOWN")
        emit({"part": "midcheck", "M": M, "forbidden_pairs": nfor,
              "verdict": verdict, "time": round(time.time() - t0, 1),
              "reading": "L-MID holds" if verdict == "UNSAT"
              else "L-MID FAILS — counterexample exists"})


def schedule_colors(vals, M):
    """The two (x,x,1-x,1-x) schedule colorings as {v: 0/1}.
    Team A of S0 = odds of (M/2, 2M] + evens of (2M, 8M]."""
    s0 = {v: (1 if ((v <= 2 * M and v % 2 == 1) or
                    (v > 2 * M and v % 2 == 0)) else 0) for v in vals}
    s1 = {v: 1 - c for v, c in s0.items()}
    return s0, s1


def base_model(M):
    Bm1, B0, B1, B2 = blocks(M)
    vals = Bm1 + B0 + B1 + B2
    m = cp_model.CpModel()
    col = {v: m.NewBoolVar(f"c{v}") for v in vals}  # 1 = team A
    for blk in (Bm1, B0, B1, B2):
        m.Add(sum(col[v] for v in blk) == len(blk) // 2)
    # mu_dn = 0 both teams (hard):
    for (a, b, c) in triples(Bm1, B0, B1):
        m.AddBoolOr([col[a].Not(), col[b].Not(), col[c].Not()])
        m.AddBoolOr([col[a], col[b], col[c]])
    chans = triples(B0, B1, B2) + triples(Bm1, B1, B2)
    return m, col, vals, chans


def mono_indicators(m, col, chans):
    """Per-team mono indicators for the paid channels."""
    monoA, monoB = [], []
    for (a, b, c) in chans:
        ia = m.NewBoolVar(f"A{a}_{b}")
        m.AddBoolAnd([col[a], col[b], col[c]]).OnlyEnforceIf(ia)
        m.AddBoolOr([col[a].Not(), col[b].Not(), col[c].Not()]
                    ).OnlyEnforceIf(ia.Not())
        ib = m.NewBoolVar(f"B{a}_{b}")
        m.AddBoolAnd([col[a].Not(), col[b].Not(), col[c].Not()]
                     ).OnlyEnforceIf(ib)
        m.AddBoolOr([col[a], col[b], col[c]]).OnlyEnforceIf(ib.Not())
        monoA.append(ia)
        monoB.append(ib)
    return monoA, monoB


def part_zeroset(Ms):
    for M in Ms:
        m, col, vals, chans = base_model(M)
        for (a, b, c) in chans:  # zero paid mass, both teams
            m.AddBoolOr([col[a].Not(), col[b].Not(), col[c].Not()])
            m.AddBoolOr([col[a], col[b], col[c]])
        s0, s1 = schedule_colors(vals, M)
        for s in (s0, s1):  # differ from both schedules somewhere
            m.AddBoolOr([col[v] if s[v] == 0 else col[v].Not()
                         for v in vals])
        sol = cp_model.CpSolver()
        sol.parameters.max_time_in_seconds = 1200
        t0 = time.time()
        st = sol.Solve(m)
        verdict = {cp_model.OPTIMAL: "SAT", cp_model.FEASIBLE: "SAT",
                   cp_model.INFEASIBLE: "UNSAT"}.get(st, "UNKNOWN")
        row = {"part": "zeroset", "M": M, "verdict": verdict,
               "time": round(time.time() - t0, 1)}
        if verdict == "SAT":
            wit = sorted(v for v in vals if sol.Value(col[v]))
            d0 = sum(1 for v in vals if sol.Value(col[v]) != s0[v])
            d1 = sum(1 for v in vals if sol.Value(col[v]) != s1[v])
            row.update(witnessA=wit, dist=(d0, d1),
                       reading="NON-schedule zero exists")
        else:
            row["reading"] = ("zero set = exactly the two parity "
                              "schedules")
        emit(row)


def part_floor(Ms, ds):
    for M in Ms:
        for d in ds:
            m, col, vals, chans = base_model(M)
            monoA, monoB = mono_indicators(m, col, chans)
            s0, s1 = schedule_colors(vals, M)
            for s in (s0, s1):
                diffs = []
                for v in vals:
                    dv = m.NewBoolVar(f"d{v}_{id(s) % 97}")
                    m.Add(col[v] != s[v]).OnlyEnforceIf(dv)
                    m.Add(col[v] == s[v]).OnlyEnforceIf(dv.Not())
                    diffs.append(dv)
                m.Add(sum(diffs) >= d)
            top = m.NewIntVar(0, len(chans), "top")
            m.Add(sum(monoA) <= top)
            m.Add(sum(monoB) <= top)
            m.Minimize(top)
            sol = cp_model.CpSolver()
            sol.parameters.max_time_in_seconds = 1800
            sol.parameters.num_workers = 8
            t0 = time.time()
            st = sol.Solve(m)
            el = round(time.time() - t0, 1)
            if st == cp_model.OPTIMAL:
                emit({"part": "floor", "M": M, "d": d,
                      "f": int(sol.ObjectiveValue()),
                      "sumAB": int(sum(sol.Value(x) for x in
                                       monoA + monoB)),
                      "time": el, "opt": True})
            elif st == cp_model.FEASIBLE:
                emit({"part": "floor", "M": M, "d": d,
                      "f_upper": int(sol.ObjectiveValue()),
                      "f_lower": int(sol.BestObjectiveBound()),
                      "time": el, "opt": False})
            else:
                emit({"part": "floor", "M": M, "d": d,
                      "verdict": "INFEASIBLE" if
                      st == cp_model.INFEASIBLE else "UNKNOWN",
                      "time": el})


def part_fhalf(Ms, timeout=3600):
    for M in Ms:
        m, col, vals, chans = base_model(M)
        monoA, monoB = mono_indicators(m, col, chans)
        low = [v for v in vals if v <= 2 * M]
        # NOT low-pure: team A's low part contains both parities.
        # (At exact balance, A-low pure parity p forces A-low = all
        # p-values of Bm1 and B0, so purity of A <=> purity of B.)
        m.AddBoolOr([col[v] for v in low if v % 2 == 0])
        m.AddBoolOr([col[v] for v in low if v % 2 == 1])
        m.AddBoolOr([col[v].Not() for v in low if v % 2 == 0])
        m.AddBoolOr([col[v].Not() for v in low if v % 2 == 1])
        top = m.NewIntVar(0, len(chans), "top")
        m.Add(sum(monoA) <= top)
        m.Add(sum(monoB) <= top)
        m.Minimize(top)
        sol = cp_model.CpSolver()
        sol.parameters.max_time_in_seconds = timeout
        sol.parameters.num_workers = 8
        t0 = time.time()
        st = sol.Solve(m)
        el = round(time.time() - t0, 1)
        row = {"part": "fhalf", "M": M, "time": el}
        if st == cp_model.OPTIMAL:
            row.update(f=int(sol.ObjectiveValue()), opt=True,
                       half=M // 2)
            wit = sorted(v for v in vals if sol.Value(col[v]))
            row["witnessA"] = wit
        elif st == cp_model.FEASIBLE:
            row.update(f_upper=int(sol.ObjectiveValue()),
                       f_lower=int(sol.BestObjectiveBound()),
                       opt=False, half=M // 2)
        else:
            row["verdict"] = ("INFEASIBLE" if st == cp_model.INFEASIBLE
                              else "UNKNOWN")
        emit(row)


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what in ("midcheck", "all"):
        part_midcheck([16, 24, 32, 40])
    if what in ("zeroset", "all"):
        part_zeroset([16, 24, 32, 40])
    if what in ("floor", "all"):
        part_floor([16, 24, 32], [0, 1, 2, 4, 8, 16])
    if what == "fhalf":
        part_fhalf([8, 12, 16, 24, 32, 40])
