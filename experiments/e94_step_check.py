"""e94_step_check: machine-check of every parametric step asserted in
notes/30-og-proof-draft.md (Lemma OG proof synthesis).

Test scales: M = 44, 48, 52, 60 (all ≡ 0 mod 4), with M = 40 as anchor;
Part 3 sweeps a broad M range (both parities) for the top-level statement.

Instance OG(M): values (M, 2M]; for every AP triple (a,b,c) inside,
clauses ~(a<b & b<c) and ~(c<b & b<a); transitivity handled lazily
(cuts are order axioms, kept permanently in one incremental solver
per M); attacks and hypotheses as unit assumptions.

Attack notation: b_j = M+j, t_i = 2M-i.
  15-attack j (j=1..7):  t_{15-2j} = 2M+2j-15  before  b_j
  16-attack j (j=1..8):  t_{16-2j} = 2M+2j-16  before  b_j

Parts:
 (0) cross-validation of the lazy encoding against an eager
     full-transitivity encoding at M=40 and M=44;
 (1) prefix scan: j*(M) = least j with 15-family + 16{1..j} UNSAT;
     the top-level claim is j* <= 3 (=> Lemma OG via 10 attack units);
 (2) deletion-minimal attack cores inside 15{1..7} u 16{1..3} at each
     test M (two deletion orders), w.r.t. the FULL AP constraint set;
 (3) broad-M sweep of the 10-unit infeasibility (both parities);
 (4) bottom-vs-guard forced table under the maximal consistent prefix
     H*(M) = 15-family + 16{1..j*-1}, at each test M;
 (5) anchor-lift scan of the 27 note-28 DAG literals: which lifts
     (pM+q)/4 through the M=40 values does H*(M) force at ALL of
     M=44,48,52,60 (H* is SAT, so forcing is NON-vacuous);
 (6) deletion-minimal triple supports of the two universal invariants
     b5<t6 (under 15-family alone) at M=44 and M=60, with anchor
     comparison -- the hand-derivable kernel of the draft;
 (7) arithmetic instantiation of the P3 skeleton F1..F7 at test M.

Output: data/step_check.log (+ .json).  NOTE: this run CORRECTS the
og40 record: on the full instance, attacks 1-13 are already UNSAT at
M=40 (first conflict = 16-attack j=3), so the '47<78 vs attack #14'
pivot of notes/28 lives on the restricted 37-value MUS instance only.
"""
import json
import random
import time

import numpy as np
from pysat.solvers import Cadical195

MS_TEST = [44, 48, 52, 60]
MS_ALL = [40] + MS_TEST
OUT = "/Users/will/Dev/personal/tasks/math/erdos197/data/step_check.log"

# ---- the 27 spine literals (M=40 concrete values), DAG order (note 28) ----
SPINE = [
    (66, 53), (51, 61), (71, 61), (55, 61), (67, 61), (59, 53), (59, 65),
    (71, 65), (59, 57), (59, 61), (63, 61), (55, 65), (71, 69), (63, 65),
    (47, 61), (71, 73), (67, 65), (67, 57), (51, 65), (51, 42), (51, 60),
    (69, 60), (71, 60), (69, 78), (61, 44), (61, 78), (47, 78),
]

# values pinned by attack roles (bottoms / guards): identity NOT free
PIN = {41: 4, 42: 4, 43: 4, 44: 4, 45: 4, 46: 4, 47: 4,
       66: 8, 67: 8, 69: 8, 70: 8, 72: 8, 73: 8, 75: 8, 77: 8, 78: 8}


def lift(v0, p, M):
    """anchor form through (M=40, v0) with slope p/4, evaluated at M."""
    q = 4 * v0 - 40 * p
    num = p * M + q
    return num // 4 if num % 4 == 0 else None


def form_str(v0, p):
    q = 4 * v0 - 40 * p
    if p == 4:
        return f"M{q // 4:+d}"
    if p == 8:
        return f"2M{q // 4:+d}"
    if p == 6:
        return f"(3M{q // 2:+d})/2"
    return f"({p}M{q:+d})/4"


class OG:
    """Full OG(M) with per-triple selector literals + lazy transitivity."""

    def __init__(self, M, selectors=False):
        self.M = M
        lo, hi = M, 2 * M
        self.V = list(range(lo + 1, hi + 1))
        self.n = len(self.V)
        self.idx = {v: i for i, v in enumerate(self.V)}
        self.var = {}
        c = 0
        for i in range(self.n):
            for j in range(i + 1, self.n):
                c += 1
                self.var[(i, j)] = c
        self.triples = []
        for y in self.V:
            d = 1
            while y + d <= hi:
                x, z = y - d, y + d
                d += 1
                if x > lo:
                    self.triples.append((x, y, z))
        self.sel = {}
        cl = []
        for (x, y, z) in self.triples:
            if selectors:
                c += 1
                self.sel[(x, y, z)] = c
                cl.append([-c, -self.o(x, y), -self.o(y, z)])
                cl.append([-c, -self.o(z, y), -self.o(y, x)])
            else:
                cl.append([-self.o(x, y), -self.o(y, z)])
                cl.append([-self.o(z, y), -self.o(y, x)])
        self.sol = Cadical195(bootstrap_with=cl)

    def o(self, u, w):
        i, j = self.idx[u], self.idx[w]
        return self.var[(i, j)] if i < j else -self.var[(j, i)]

    def ilit(self, p, q):
        return self.var[(p, q)] if p < q else -self.var[(q, p)]

    def solve(self, assumps):
        """SAT/UNSAT under assumptions; lazy transitivity, cuts kept."""
        while True:
            if not self.sol.solve(assumptions=assumps):
                return False
            model = set(l for l in self.sol.get_model() if l > 0)
            B = np.zeros((self.n, self.n), dtype=bool)
            for (i, j), v in self.var.items():
                if v in model:
                    B[i, j] = True
                else:
                    B[j, i] = True
            R2 = (B.astype(np.uint8) @ B.astype(np.uint8)) > 0
            miss = R2 & ~B & ~np.eye(self.n, dtype=bool) & B.T
            ii, jj = np.nonzero(miss)
            if len(ii) == 0:
                return True
            new = []
            for i, j in zip(ii[:30000], jj[:30000]):
                ks = np.nonzero(B[i] & B[:, j])[0]
                new.append([-self.ilit(i, int(ks[0])),
                            -self.ilit(int(ks[0]), j), self.ilit(i, j)])
            self.sol.append_formula(new)

    # ---- attack units ----
    def a15(self, j):
        return self.o(2 * self.M + 2 * j - 15, self.M + j)

    def a16(self, j):
        return self.o(2 * self.M + 2 * j - 16, self.M + j)

    def fam15(self):
        return [self.a15(j) for j in range(1, 8)]

    def pre16(self, upto):
        return [self.a16(j) for j in range(1, upto + 1)]


def eager_check(M, units_fn):
    """independent eager-transitivity build; returns SAT of units."""
    V = list(range(M + 1, 2 * M + 1))
    idx = {v: i for i, v in enumerate(V)}
    n = len(V)
    var = {}
    c = 0
    for i in range(n):
        for j in range(i + 1, n):
            c += 1
            var[(i, j)] = c

    def o(u, w):
        i, j = idx[u], idx[w]
        return var[(i, j)] if i < j else -var[(j, i)]

    cl = []
    for y in V:
        d = 1
        while y + d <= 2 * M:
            x, z = y - d, y + d
            d += 1
            if x > M:
                cl.append([-o(x, y), -o(y, z)])
                cl.append([-o(z, y), -o(y, x)])

    def lit(a, b):
        return var[(a, b)] if a < b else -var[(b, a)]

    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            for k in range(n):
                if k == i or k == j:
                    continue
                cl.append([-lit(i, j), -lit(j, k), lit(i, k)])
    s = Cadical195(bootstrap_with=cl)
    res = s.solve(assumptions=units_fn(M, o))
    s.delete()
    return res


def main():
    fh = open(OUT, "w")

    def log(s=""):
        print(s, flush=True)
        fh.write(s + "\n")
        fh.flush()

    t0 = time.time()
    results = {}

    # ---------------- Part 0: encoding cross-validation ----------------
    log("== (0) lazy-vs-eager cross-validation")
    for M in (40, 44):
        g = OG(M)

        def u10(MM, o):
            a = [o(2 * MM + 2 * j - 15, MM + j) for j in range(1, 8)]
            a += [o(2 * MM + 2 * j - 16, MM + j) for j in (1, 2, 3)]
            return a

        def u15(MM, o):
            return [o(2 * MM + 2 * j - 15, MM + j) for j in range(1, 8)]

        lz10 = g.solve(g.fam15() + g.pre16(3))
        lz15 = g.solve(g.fam15())
        eg10 = eager_check(M, u10)
        eg15 = eager_check(M, u15)
        ok = (lz10 == eg10) and (lz15 == eg15)
        log(f"  M={M}: 15-family SAT lazy={lz15} eager={eg15}; "
            f"15+16(1..3) SAT lazy={lz10} eager={eg10}  "
            f"{'AGREE' if ok else 'MISMATCH!!'}  ({time.time()-t0:.0f}s)")
        g.sol.delete()

    # ---------------- Part 1: prefix scan, j*(M) ----------------
    log()
    log("== (1) prefix scan at test M: j*(M) = least j with "
        "15-family + 16{1..j} UNSAT  (claim: j* <= 3)")
    inst = {}
    jstar = {}
    for M in MS_ALL:
        g = OG(M)
        inst[M] = g
        assert g.solve(g.fam15()), f"15-family UNSAT at M={M}?!"
        js = None
        for j in range(1, 9):
            if not g.solve(g.fam15() + g.pre16(j)):
                js = j
                break
        jstar[M] = js
        log(f"  M={M:3d}: 15-family SAT; j* = {js}   "
            f"({time.time()-t0:.0f}s)")
    results["jstar"] = jstar

    # ---------------- Part 2: minimal attack cores ----------------
    log()
    log("== (2) deletion-minimal attack cores inside 15{1..7} u 16{1..3}"
        " (full AP constraints; two deletion orders)")
    results["cores"] = {}
    for M in MS_ALL:
        g = inst[M]
        units = [("15", j, g.a15(j)) for j in range(1, 8)] + \
                [("16", j, g.a16(j)) for j in (1, 2, 3)]
        cores = []
        for order in (list(range(10)), list(range(9, -1, -1))):
            keep = list(range(10))
            for i in order:
                if i not in keep:
                    continue
                trial = [units[k][2] for k in keep if k != i]
                if not g.solve(trial):
                    keep.remove(i)
            cores.append(sorted(f"{f}:{j}" for (f, j, _) in
                                [units[k] for k in keep]))
        results["cores"][M] = cores
        log(f"  M={M:3d}: fwd core {cores[0]}   bwd core {cores[1]}"
            f"   ({time.time()-t0:.0f}s)")

    # ---------------- Part 3: broad-M sweep ----------------
    log()
    log("== (3) broad sweep: 15-family + 16{1,2,3} infeasible?  "
        "(both parities)")
    sweep_fail = []
    sweep_ms = list(range(40, 101)) + [104, 108, 112, 120, 128, 150, 200]
    for M in sweep_ms:
        g = inst[M] if M in inst else OG(M)
        r = g.solve(g.fam15() + g.pre16(3))
        if r:
            sweep_fail.append(M)
        if M not in inst:
            g.sol.delete()
    log(f"  swept M in {{40..100}} u {{104,108,112,120,128,150,200}}: "
        f"UNSAT everywhere except {sweep_fail if sweep_fail else 'NONE'}"
        f"   ({time.time()-t0:.0f}s)")
    results["sweep_sat_exceptions"] = sweep_fail

    # ---------------- Part 4: bottom-vs-guard table under H* ----------
    log()
    log("== (4) bottom-vs-guard forced orders under the maximal "
        "consistent prefix H*(M) = 15-family + 16{1..j*-1}")
    results["bvg"] = {}
    for M in MS_ALL:
        g = inst[M]
        H = g.fam15() + g.pre16(jstar[M] - 1)
        assert g.solve(H)
        rows = []
        for j in range(1, 8):
            i16 = 16 - 2 * j
            b, t = M + j, 2 * M - i16
            if not g.solve(H + [g.o(t, b)]):
                rows.append(f"b{j}<t{i16}")
            elif not g.solve(H + [g.o(b, t)]):
                rows.append(f"t{i16}<b{j}")
        # also b5 vs t6 under the 15-family ALONE
        b5t6_15only = not g.solve(g.fam15() + [g.o(2 * M - 6, M + 5)])
        results["bvg"][M] = {"under_Hstar": rows,
                            "b5<t6_under_15only": b5t6_15only}
        log(f"  M={M:3d}: H* forces {rows};  b5<t6 under 15-family alone: "
            f"{b5t6_15only}   ({time.time()-t0:.0f}s)")

    # ---------------- Part 5: anchor-lift scan of DAG literals --------
    log()
    log("== (5) anchor-lift scan: which lifts (through the M=40 value) "
        "does H*(M) force at ALL of M=44,48,52,60 (non-vacuous: H* SAT)")
    lifts = {}
    for (u0, v0) in SPINE:
        key = f"{u0}<{v0}"
        lifts[key] = []
        pu_c = [PIN[u0]] if u0 in PIN else [4, 5, 6, 7, 8]
        pv_c = [PIN[v0]] if v0 in PIN else [4, 5, 6, 7, 8]
        for pu in pu_c:
            for pv in pv_c:
                ok = True
                for M in MS_TEST:
                    u, v = lift(u0, pu, M), lift(v0, pv, M)
                    if (u is None or v is None or u == v or
                            not (M < u <= 2 * M) or not (M < v <= 2 * M)):
                        ok = False
                        break
                    g = inst[M]
                    H = g.fam15() + g.pre16(jstar[M] - 1)
                    if g.solve(H + [g.o(v, u)]):
                        ok = False
                        break
                if ok:
                    lifts[key].append(
                        (form_str(u0, pu), form_str(v0, pv)))
        tag = " | ".join(f"{a} < {b}" for a, b in lifts[key]) \
            if lifts[key] else "NONE -- M40-ONLY literal"
        log(f"  {key:7s}:  {tag}   ({time.time()-t0:.0f}s)")
    results["lifts"] = lifts

    # ---------------- Part 6: minimal supports of key parametric lemmas
    log()
    log("== (6) deletion-minimal triple supports under H2(M) = 15-family"
        " + 16{1,2}, at M=44 and M=60 (selectorized instances);"
        " units then also minimized")
    targets = [
        ("b7<b21", lambda M: (M + 7, M + 21)),     # lift of 47<61
        ("b21<t2", lambda M: (M + 21, 2 * M - 2)),  # lift of 61<78
        ("m2<b4", lambda M: ((3 * M + 2) // 2, M + 4)),  # lift of 61<44
        ("b7<t2", lambda M: (M + 7, 2 * M - 2)),   # the final literal
    ]
    results["supports"] = {}
    for M in (44, 60):
        g = OG(M, selectors=True)
        units = [("15", j, g.a15(j)) for j in range(1, 8)] + \
                [("16", j, g.a16(j)) for j in (1, 2)]
        H2 = [u[2] for u in units]
        allsel = [g.sel[t] for t in g.triples]
        for name, f in targets:
            u, v = f(M)
            base = H2 + [g.o(v, u)]   # negation of the target literal
            if g.solve(base + allsel):
                log(f"  M={M} {name}: NOT forced under H2 -- skip")
                continue
            rng = random.Random(0)
            keep = list(g.triples)
            order = list(keep)
            rng.shuffle(order)
            for t in order:
                trial = [g.sel[x] for x in keep if x != t]
                if not g.solve(base + trial):
                    keep.remove(t)
            ksel = [g.sel[x] for x in keep]
            assert not g.solve(base + ksel)
            ku = list(units)
            for w in list(ku):
                trial = [x[2] for x in ku if x is not w]
                if not g.solve(trial + [g.o(v, u)] + ksel):
                    ku.remove(w)
            results["supports"].setdefault(name, {})[M] = {
                "triples": [list(t) for t in keep],
                "units": [f"{a}:{b}" for (a, b, _) in ku]}
            log(f"  M={M} {name}: |triples|={len(keep)} units="
                f"{[f'{a}:{b}' for (a, b, _) in ku]}"
                f"   ({time.time()-t0:.0f}s)")
        g.sol.delete()
    for name, _ in targets:
        d = results["supports"].get(name, {})
        if 44 in d and 60 in d:
            sb = {tuple(x - 44 for x in t) for t in d[44]["triples"]} & \
                 {tuple(x - 60 for x in t) for t in d[60]["triples"]}
            st = {tuple(x - 88 for x in t) for t in d[44]["triples"]} & \
                 {tuple(x - 120 for x in t) for t in d[60]["triples"]}
            log(f"  {name}: common bottom-offset triples {sorted(sb)};"
                f" common top-offset triples {sorted(st)}")

    # ---------------- Part 7: F1..F7 arithmetic at test M --------------
    log()
    log("== (7) P3 skeleton F1..F7 instantiation at test M "
        "(arithmetic: inside (M,2M], AP)")
    F = [
        ("F1", lambda M: (M + 1, (3 * M - 6) // 2, 2 * M - 7)),
        ("F2", lambda M: (M + 5, (3 * M + 2) // 2, 2 * M - 3)),
        ("F3", lambda M: (M + 7, (3 * M + 2) // 2, 2 * M - 5)),
        ("F4", lambda M: (M + 17, (3 * M - 2) // 2, 2 * M - 19)),
        ("F5", lambda M: (M + 19, (3 * M + 14) // 2, 2 * M - 5)),
        ("F6", lambda M: ((3 * M - 2) // 2, (3 * M + 6) // 2,
                          (3 * M + 14) // 2)),
        ("F7", lambda M: ((3 * M + 2) // 2, (7 * M - 16) // 4,
                          2 * M - 9)),
    ]
    for name, f in F:
        oks = []
        for M in MS_ALL:
            a, b, c = f(M)
            ok = (a + c == 2 * b and M < a <= 2 * M and M < b <= 2 * M
                  and M < c <= 2 * M and a != b and b != c)
            oks.append(f"M={M}:{'ok' if ok else 'FAIL'}")
        log(f"  {name}: {'  '.join(oks)}")

    # ---------------- Part 8: candidate uniform 4-unit / 3-unit cores --
    log()
    log("== (8) uniform-core sweeps (both parities, M=40..100 + big):"
        "  C4 = {15:1,15:2,15:5,16:3}   C3 = {15:5,15:6,16:3}")
    for label, spec in (("C4", [("15", 1), ("15", 2), ("15", 5),
                                ("16", 3)]),
                        ("C3", [("15", 5), ("15", 6), ("16", 3)])):
        sat_ms = []
        for M in list(range(40, 101)) + [104, 112, 120, 128, 150, 200]:
            g = inst[M] if M in inst else OG(M)
            u = [g.a15(j) if f == "15" else g.a16(j) for (f, j) in spec]
            if g.solve(u):
                sat_ms.append(M)
            if M not in inst:
                g.sol.delete()
        log(f"  {label}: SAT (i.e. NOT a core) at {sat_ms if sat_ms else 'NONE -- infeasible at every swept M'}"
            f"   ({time.time()-t0:.0f}s)")
        results[f"sweep_{label}_sat"] = sat_ms

    # ---------------- Part 9: the exceptional family M = 3 (mod 16) ----
    log()
    log("== (9) exceptional M (15-family + 16{1..3} SAT): j*(M) there,"
        " and does the FULL 16-family still refute?")
    for M in (51, 67, 83, 99, 115, 131):
        g = OG(M)
        js = None
        for j in range(1, 9):
            if not g.solve(g.fam15() + g.pre16(j)):
                js = j
                break
        full = g.solve(g.fam15() + g.pre16(8))
        log(f"  M={M} (M mod 16 = {M % 16}): j* = {js}; "
            f"15-family+16{{1..8}} SAT={full}   ({time.time()-t0:.0f}s)")
        results.setdefault("exceptional", {})[M] = js
        g.sol.delete()

    # ---------------- Part 10: final-chain route checks ----------------
    log()
    log("== (10) final-chain literals under H*(M): F = forced,"
        " R = reverse forced, - = undetermined")
    for M in MS_ALL:
        g = inst[M]
        H = g.fam15() + g.pre16(jstar[M] - 1)
        m2 = (3 * M + 2) // 2
        row = []
        for name, (u, v) in [
                ("b7<m2", (M + 7, m2)), ("m2<t2", (m2, 2 * M - 2)),
                ("m2<b4", (m2, M + 4)), ("b7<b21", (M + 7, M + 21)),
                ("b21<t2", (M + 21, 2 * M - 2)),
                ("b7<t2", (M + 7, 2 * M - 2))]:
            fa = not g.solve(H + [g.o(v, u)])
            fb = not g.solve(H + [g.o(u, v)])
            row.append(f"{name}:{'F' if fa else ('R' if fb else '-')}")
        results.setdefault("chain", {})[M] = row
        log(f"  M={M:3d}: " + "  ".join(row))

    json.dump(results, open(OUT.replace(".log", ".json"), "w"), indent=1)
    log()
    log(f"total {time.time()-t0:.0f}s")
    fh.close()


if __name__ == "__main__":
    main()
