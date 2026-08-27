"""e132_n3_l1_spotchecks: per-claim machine spot-checks for notes/53
(GAP-N3 hand extension + GAP-L1' refutation).

Parts (each backs a named claim of notes/53):

  partR  [N3 SSA.4]  per-residue single-puncture escape census: pairs
         {11,12} and {15,16}, ALL 8 residue classes mod 8, 3 scales per
         class (M in 72..127).  For each (x, r, M): intact verdict +
         the exact set of escape punctures v (recorded as offsets from
         M / 2M).  Claim backed: every residue class has at least one
         1-robust pair among {11,12}, {15,16}; the bad cells' escape
         offsets are scale-stable laws.

  partT  [N3 SSA.2]  {11,12} dyadic (r0): exhaustive 2-subset census
         over the unit-support region at M = 80, 112, 144.  Claim
         backed: d* = 2 with the UNIQUE minimal escape {M+2, M+4}
         (bottom receiver pair) at every dyadic scale.

  partS  [N3 SSA.3]  {15,16} dyadic: catalogue-busting 2-subsets
         (2-subsets of the unit support hitting the supports of ALL
         four catalogued cores C3/F3/Q4/G6) are still UNSAT, and each
         has a fresh deletion-minimal unit core; core patterns compared
         across M = 80, 112, 144 for lane stability.

  partU  [L1' SSB.2/3]  ROT4 hand-formula checks, exact arithmetic:
         (1) per-octave max ratio-2 window densities equal the 4-phase
             hand values 4/7, 1/2, 4/5, 5/6 (cycle by m mod 4), team A
             and B, octaves 5..15; global excess |A n (a,2a]| - 5a/6
             bounded by a small constant over all a <= 2^16.
         (2) chain finiteness, adversarial reflectors: BFS over chains
             u -> 2u - f staying in one ROT4 team, f ANY value in
             [1,64] (membership of f not required -- stronger than
             lem:orbit's F subset T), seeds u0 in (2^10, 2^11],
             horizon 2^22: all chains die; max depth recorded.
         (3) controls: ROT2 (half-rotation) has EXACT density-1
             windows (Case-1 feed, anchors 3*2^(m-1)); ROT8 census sup.

  partV  [L1' SSB.4]  ROT4 adjacent-pair supply: per-octave gap-1 pair
         counts for both teams (claim: Theta(M) -- GATE inapplicable,
         dodger requirement (iii) fails for rotation partitions).

Run: .venv/bin/python experiments/e132_n3_l1_spotchecks.py [partR|partT|partS|partU|partV|all]
Artifacts: data/e132_spotchecks.json (+ .log via tee)
"""
import itertools
import json
import sys
import time
from fractions import Fraction

from pysat.solvers import Cadical195

BASE = "/Users/will/Dev/personal/tasks/math/erdos197/data"
OUT = {}


# ---------------------------------------------------------------- rungs
def rung_units(M, x):
    us = []
    for a in (x, x + 1):
        for y in range(M + 1, 2 * M + 1):
            z = 2 * y - a
            if M < z <= 2 * M and z != y:
                us.append((z, y))
    return sorted(set(us))


def support_values(M, x):
    vals = set()
    for (z, y) in rung_units(M, x):
        vals |= {z, y}
    return sorted(vals)


class Gadget:
    """e130-identical selection-guarded rung instance (fresh code path
    kept byte-comparable with e130_n3_puncture.Gadget)."""

    def __init__(self, M, x):
        self.M, self.x = M, x
        vals = list(range(M + 1, 2 * M + 1))
        self.vals = vals
        idx = {v: i for i, v in enumerate(vals)}
        n = len(vals)
        var = {}
        c = 0
        for p in range(n):
            for q in range(p + 1, n):
                c += 1
                var[(p, q)] = c

        def o(u, w):
            p, q = idx[u], idx[w]
            return var[(p, q)] if p < q else -var[(q, p)]

        self.o = o
        self.sel = {}
        for v in vals:
            c += 1
            self.sel[v] = c
        cl = []
        for y in vals:
            d = 1
            while y + d <= 2 * M and y - d > M:
                a, b = y - d, y + d
                g = [-self.sel[a], -self.sel[y], -self.sel[b]]
                cl.append(g + [-o(a, y), -o(y, b)])
                cl.append(g + [-o(b, y), -o(y, a)])
                d += 1
        for p in range(n):
            for q in range(p + 1, n):
                vpq = var[(p, q)]
                for r in range(q + 1, n):
                    vqr, vpr = var[(q, r)], var[(p, r)]
                    cl.append([-vpq, -vqr, vpr])
                    cl.append([vpq, vqr, -vpr])
        self.units = rung_units(M, x)
        for (z, y) in self.units:
            cl.append([-self.sel[z], -self.sel[y], o(z, y)])
        self.solver = Cadical195(bootstrap_with=cl)

    def query(self, P):
        P = set(P)
        assump = [(-self.sel[v] if v in P else self.sel[v])
                  for v in self.vals]
        sat = self.solver.solve(assumptions=assump)
        if sat:
            pos_lits = set(l for l in self.solver.get_model() if l > 0)

            def before(w, u):
                lit = self.o(w, u)
                return (lit in pos_lits) if lit > 0 else (-lit not in pos_lits)

            keep = [v for v in self.vals if v not in P]
            order = sorted(keep, key=lambda u: sum(
                1 for w in keep if w != u and before(w, u)))
            self._check(order, P)
        return sat

    def _check(self, order, P):
        pos = {v: i for i, v in enumerate(order)}
        M = self.M
        for y in order:
            d = 1
            while y + d <= 2 * M and y - d > M:
                a, b = y - d, y + d
                if a in pos and b in pos:
                    if pos[a] < pos[y] < pos[b] or pos[b] < pos[y] < pos[a]:
                        raise AssertionError(
                            f"monotone AP {(a, y, b)} in escape M={M} P={P}")
                d += 1
        for (z, y) in self.units:
            if z in pos and y in pos and not pos[z] < pos[y]:
                raise AssertionError(
                    f"unit {(z, y)} violated in escape M={M} P={P}")

    def delete(self):
        self.solver.delete()


def offset(v, M):
    """Human-readable position: b<j> = M+j (bottom), t<i> = 2M-i (top),
    else interior signed offset from 3M/2 written c<+/-d>."""
    if v - M <= 16:
        return f"b{v - M}"
    if 2 * M - v <= 16:
        return f"t{2 * M - v}"
    return f"c{v - (3 * M) // 2:+d}"


# ---------------------------------------------------------------- partR
def partR():
    rows = {}
    t0 = time.time()
    for x in (11, 15):
        for r in range(8):
            scales = [b + ((r - b) % 8) for b in (72, 96, 120)]
            for M in scales:
                g = Gadget(M, x)
                intact = g.query([])
                esc = []
                for v in range(M + 1, 2 * M + 1):
                    if g.query([v]):
                        esc.append(v)
                g.delete()
                key = f"x{x}_r{r}_M{M}"
                rows[key] = {
                    "intact": "SAT" if intact else "UNSAT",
                    "escapes": [offset(v, M) for v in esc],
                }
                print(f"[R] {key}: intact="
                      f"{'SAT!' if intact else 'UNSAT'} "
                      f"1-escapes={rows[key]['escapes'] or 'NONE'}",
                      flush=True)
    OUT["partR"] = rows
    print(f"partR done ({time.time()-t0:.0f}s)", flush=True)


# ---------------------------------------------------------------- partT
def partT():
    rows = {}
    t0 = time.time()
    x = 11
    for M in (80, 112, 144):
        sup = support_values(M, x)
        g = Gadget(M, x)
        esc2 = []
        for P in itertools.combinations(sup, 2):
            if g.query(P):
                esc2.append([offset(v, M) for v in P])
        # also every {support value, arbitrary block value} pair would be
        # 17*(M-1) queries; sample the bottom-region cross pairs which is
        # where the d* escapes live:
        cross = []
        for b in range(M + 1, M + 9):
            for v in range(M + 1, 2 * M + 1):
                if v > b and (b in sup or v in sup):
                    if g.query([b, v]):
                        pr = sorted([offset(b, M), offset(v, M)])
                        if pr not in esc2:
                            cross.append(pr)
        g.delete()
        rows[f"M{M}"] = {"support_2subset_escapes": esc2,
                         "bottom_cross_escapes": cross,
                         "n_support": len(sup)}
        print(f"[T] x=11 M={M}: support-2-escapes={esc2} "
              f"bottom-cross-escapes={cross}", flush=True)
    OUT["partT"] = rows
    print(f"partT done ({time.time()-t0:.0f}s)", flush=True)


# ---------------------------------------------------------------- partS
CORE_SUPPORTS_15 = {          # bottom/top offsets of the catalogued cores
    "C3": {"b3", "b5", "b6", "t3", "t5", "t10"},
    "F3": {"b4", "b6", "b7", "t2", "t4", "t7"},
    "Q4": {"b5", "b6", "b7", "t2", "t3", "t4", "t5"},
    "G6": {"b2", "b5", "b7", "t2", "t5", "t6", "t11"},
}


def mus_units(M, x, P):
    P = set(P)
    vals = [v for v in range(M + 1, 2 * M + 1) if v not in P]
    idx = {v: i for i, v in enumerate(vals)}
    n = len(vals)
    var = {}
    c = 0
    for p in range(n):
        for q in range(p + 1, n):
            c += 1
            var[(p, q)] = c

    def o(u, w):
        p, q = idx[u], idx[w]
        return var[(p, q)] if p < q else -var[(q, p)]

    cl = []
    for y in vals:
        d = 1
        while y + d <= 2 * M and y - d > M:
            a, b = y - d, y + d
            if a in idx and b in idx:
                cl.append([-o(a, y), -o(y, b)])
                cl.append([-o(b, y), -o(y, a)])
            d += 1
    for p in range(n):
        for q in range(p + 1, n):
            vpq = var[(p, q)]
            for r in range(q + 1, n):
                vqr, vpr = var[(q, r)], var[(p, r)]
                cl.append([-vpq, -vqr, vpr])
                cl.append([vpq, vqr, -vpr])
    units = [(z, y) for (z, y) in rung_units(M, x)
             if z not in P and y not in P]
    amap = {}
    for (z, y) in units:
        c += 1
        amap[(z, y)] = c
        cl.append([-c, o(z, y)])
    sol = Cadical195(bootstrap_with=cl)
    live = list(units)
    assert not sol.solve(assumptions=[amap[u] for u in live]), \
        f"punctured rung SAT?! M={M} P={P}"
    for u in list(live):
        trial = [uu for uu in live if uu != u]
        if not sol.solve(assumptions=[amap[t] for t in trial]):
            live = trial
    sol.delete()
    return live


def partS():
    x = 15
    sup_off = sorted(set().union(*CORE_SUPPORTS_15.values()))
    busters = [set(P) for P in itertools.combinations(sup_off, 2)
               if all(set(P) & s for s in CORE_SUPPORTS_15.values())]
    print(f"[S] catalogue-busting 2-subsets (hit all 4 core supports): "
          f"{[sorted(b) for b in busters]}", flush=True)
    rows = {"busters": [sorted(b) for b in busters], "cores": {}}
    t0 = time.time()
    for M in (80, 112, 144):
        def val(off):
            return (M + int(off[1:])) if off[0] == "b" else \
                   (2 * M - int(off[1:]))
        for b in busters:
            P = [val(o) for o in sorted(b)]
            core = mus_units(M, x, P)
            key = "+".join(sorted(b))
            rows["cores"].setdefault(key, {})[f"M{M}"] = [
                [offset(z, M), offset(y, M)] for (z, y) in core]
            print(f"[S] M={M} P={sorted(b)}: UNSAT, fresh core "
                  f"{rows['cores'][key][f'M{M}']}", flush=True)
    OUT["partS"] = rows
    print(f"partS done ({time.time()-t0:.0f}s)", flush=True)


# ---------------------------------------------------------------- ROTk
def octave(v):
    m = v.bit_length() - 1
    if v == 1 << m:
        m -= 1
    return m


def rotk_isA(v, k):
    if v <= 1:
        return True
    m = octave(v)
    p = v - (1 << m) - 1
    q = (p * k) >> m
    return (q - m) % k < k // 2


def partU():
    rows = {}
    # (1) exact per-octave window-density maxima, both teams, ROT4
    N = 1 << 17
    isA = [False] * (N + 1)
    for v in range(1, N + 1):
        isA[v] = rotk_isA(v, 4)
    pref = [0] * (N + 1)
    for v in range(1, N + 1):
        pref[v] = pref[v - 1] + (1 if isA[v] else 0)
    phase = {0: Fraction(4, 7), 1: Fraction(1, 2),
             2: Fraction(4, 5), 3: Fraction(5, 6)}
    per_oct = {}
    ok = True
    for m in range(5, 16):
        bA = Fraction(0)
        bB = Fraction(0)
        for a in range(1 << m, 1 << (m + 1)):
            cA = pref[2 * a] - pref[a]
            fA = Fraction(cA, a)
            if fA > bA:
                bA = fA
            fB = 1 - fA
            if fB > bB:
                bB = fB
        expA, expB = phase[m % 4], phase[(m + 2) % 4]
        near = (abs(bA - expA) <= Fraction(4, 1 << m)
                and abs(bB - expB) <= Fraction(4, 1 << m))
        ok = ok and near
        per_oct[m] = {"maxA": str(bA), "handA": str(expA),
                      "maxB": str(bB), "handB": str(expB),
                      "match": near}
    excess = max(6 * (pref[2 * a] - pref[a]) - 5 * a
                 for a in range(32, (N // 2) + 1))
    rows["rot4_phase_maxima"] = per_oct
    rows["rot4_all_match"] = ok
    rows["rot4_max_excess_6dens_minus5a"] = excess
    print(f"[U1] ROT4 phase maxima match hand values 4/7,1/2,4/5,5/6 "
          f"(cycle m mod 4): {ok}; max_a 6|A∩(a,2a]|-5a = {excess}",
          flush=True)

    # (2) adversarial-reflector chain BFS, both teams
    H = 1 << 22
    for team in (True, False):
        def inT(v, team=team):
            return rotk_isA(v, 4) == team
        maxdep = 0
        total = 0
        for u0 in range((1 << 10) + 1, (1 << 11) + 1):
            if not inT(u0):
                continue
            frontier = {u0}
            dep = 0
            while frontier:
                nxt = set()
                for u in frontier:
                    for f in range(1, 65):
                        w = 2 * u - f
                        if w > u and w <= H and inT(w):
                            nxt.add(w)
                total += len(nxt)
                frontier = nxt
                if frontier:
                    dep += 1
                assert dep < 40, "chain runaway"
            maxdep = max(maxdep, dep)
        rows[f"rot4_chainBFS_{'A' if team else 'B'}"] = {
            "max_depth": maxdep, "nodes_touched": total}
        print(f"[U2] ROT4 team {'A' if team else 'B'}: adversarial "
              f"f in [1,64], seeds (2^10,2^11], horizon 2^22: all chains "
              f"die, max depth {maxdep}", flush=True)

    # (3) controls: ROT2 clean windows; ROT8 sup census
    for k in (2, 8):
        isk = [False] * (N + 1)
        for v in range(1, N + 1):
            isk[v] = rotk_isA(v, k)
        pk = [0] * (N + 1)
        for v in range(1, N + 1):
            pk[v] = pk[v - 1] + (1 if isk[v] else 0)
        best = Fraction(0)
        arg = None
        for a in range(32, (N // 2) + 1):
            f = Fraction(pk[2 * a] - pk[a], a)
            if f > best:
                best, arg = f, a
        rows[f"rot{k}_sup_density"] = {"sup": str(best), "arg": arg}
        print(f"[U3] ROT{k} sup window density = {best} at a={arg}",
              flush=True)
    OUT["partU"] = rows


def partV():
    rows = {}
    for m in range(6, 15):
        lo, hi = (1 << m), (1 << (m + 1))
        pA = pB = 0
        for v in range(lo + 1, hi):
            a1, a2 = rotk_isA(v, 4), rotk_isA(v + 1, 4)
            if a1 and a2:
                pA += 1
            if (not a1) and (not a2):
                pB += 1
        rows[m] = {"M": lo, "pairsA": pA, "pairsB": pB}
    OUT["partV"] = rows
    print("[V] ROT4 gap-1 pair supply per octave:",
          {m: (r['pairsA'], r['pairsB']) for m, r in rows.items()},
          flush=True)


PARTS = {"partR": partR, "partT": partT, "partS": partS,
         "partU": partU, "partV": partV}

if __name__ == "__main__":
    want = sys.argv[1:] or ["all"]
    names = list(PARTS) if want == ["all"] else want
    t0 = time.time()
    for nm in names:
        PARTS[nm]()
        with open(f"{BASE}/e132_spotchecks.json", "w") as f:
            json.dump(OUT, f, indent=1)
    print(f"total {time.time()-t0:.0f}s -> {BASE}/e132_spotchecks.json",
          flush=True)
