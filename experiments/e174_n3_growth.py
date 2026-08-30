"""e174_n3_growth: GAP-N3 endgame machine layer (FRONT N3+L1', notes/74).

Two questions the e130/e132 layer left open:

(1) Is H1's uniform-in-C form FALSE at small p?  For pair {15,16}
    (p = 5) the known 3-escape {b2,b4,b5} is SAT at M = 64/96/112/128
    but was UNSAT at 80/144 (e130 partB control).  If OTHER 3-escapes
    exist at 80/144, then 3-puncture escapes recur at EVERY dyadic
    scale tested and H1(5, C>=3) has no threshold m* -- GAP-N3 must be
    discharged in the growth form (choose p large), not uniformly in p.
    partP15: exhaustive 3-subset census over the unit-support region,
    M = 80, 96, 128, 144.

(2) Does the tolerance d*(p) GROW along the diagonal (the N5 law
    rho* ~ 1 - x/4M predicts d*(x) ~ x/4: d*(11)=2, d*(15)=3,
    predicted d*(27) ~ 6-7)?
    partP27: pair {27,28} (p = 9, the first usable diagonal pair
    above {15,16}): intact + all support singles + ALL support
    2-subsets at M = 80, 112, 144; ALL support 3-subsets at M = 80;
    bottom 3-subsets + 300 random support 3-subsets at M = 112, 144.
    partKCRIT: cardinality bracket of d*(27) at M = 80 (atmost-k
    punctures, k ascending, conflict-budgeted).

(3) partROTB: L1' addendum -- team-B window excess for ROT4
    (max_a 6|B n (a,2a]| - 5a over a <= 2^16; e132 partU only did A).

Every SAT verdict is re-checked by an independent scanner on the
decoded order (e130-identical).

Run: .venv/bin/python experiments/e174_n3_growth.py [partP15|partP27|partKCRIT|partROTB|all]
Artifacts: data/e174_n3_growth.json (+ .log via tee)
"""
import itertools
import json
import random
import sys
import time

from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from pysat.solvers import Cadical195

BASE = "/Users/will/Dev/personal/tasks/math/erdos197/data"
OUT = {}


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


def offset(v, M):
    if v - M <= 20:
        return f"b{v - M}"
    if 2 * M - v <= 30:
        return f"t{2 * M - v}"
    return f"c{v - (3 * M) // 2:+d}"


class Gadget:
    """e130-identical selection-guarded rung instance."""

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
        self.top = c
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
        self.clauses = cl
        self.solver = Cadical195(bootstrap_with=cl)

    def query(self, P):
        P = set(P)
        assump = [(-self.sel[v] if v in P else self.sel[v])
                  for v in self.vals]
        sat = self.solver.solve(assumptions=assump)
        if sat:
            self._audit(P)
        return sat

    def _audit(self, P):
        pos_lits = set(l for l in self.solver.get_model() if l > 0)

        def before(w, u):
            lit = self.o(w, u)
            return (lit in pos_lits) if lit > 0 else (-lit not in pos_lits)

        keep = [v for v in self.vals if v not in P]
        order = sorted(keep, key=lambda u: sum(
            1 for w in keep if w != u and before(w, u)))
        pos = {v: i for i, v in enumerate(order)}
        M = self.M
        for y in order:
            d = 1
            while y + d <= 2 * M and y - d > M:
                a, b = y - d, y + d
                if a in pos and b in pos:
                    if pos[a] < pos[y] < pos[b] or pos[b] < pos[y] < pos[a]:
                        raise AssertionError(
                            f"monotone AP {(a, y, b)} in escape M={M} P={sorted(P)}")
                d += 1
        for (z, y) in self.units:
            if z in pos and y in pos and not pos[z] < pos[y]:
                raise AssertionError(
                    f"unit {(z, y)} violated in escape M={M} P={sorted(P)}")

    def delete(self):
        self.solver.delete()


def dump():
    """Merge-write: per-part runs must not clobber other parts' rows."""
    path = f"{BASE}/e174_n3_growth.json"
    try:
        old = json.load(open(path))
    except Exception:
        old = {}
    old.update(OUT)
    json.dump(old, open(path, "w"), indent=1)


def census(g, subsets, tag, budget=None):
    """budget: conflict cap per query (solve_limited); over-budget
    queries are recorded UNKNOWN (skipped), never called escapes."""
    esc = []
    unk = []
    n = 0
    for P in subsets:
        n += 1
        if budget is None:
            if g.query(P):
                esc.append(sorted(offset(v, g.M) for v in P))
        else:
            P = set(P)
            assump = [(-g.sel[v] if v in P else g.sel[v])
                      for v in g.vals]
            g.solver.conf_budget(budget)
            r = g.solver.solve_limited(assumptions=assump)
            if r is True:
                g._audit(P)
                esc.append(sorted(offset(v, g.M) for v in P))
            elif r is None:
                unk.append(sorted(offset(v, g.M) for v in P))
    print(f"  [{tag}] {n} queries, escapes={esc or 'NONE'}"
          + (f", UNKNOWN(budget)={unk}" if unk else ""), flush=True)
    return n, esc, unk


def partP15():
    x = 15
    for M in (80, 96, 128, 144):
        t0 = time.time()
        g = Gadget(M, x)
        sup = support_values(M, x)
        n3, esc3, _ = census(g, itertools.combinations(sup, 3),
                             f"P15 M={M} sup3")
        g.delete()
        OUT.setdefault("partP15", {})[str(M)] = {
            "support": [offset(v, M) for v in sup],
            "n_3subsets": n3, "escapes3": esc3,
            "secs": round(time.time() - t0, 1)}
        print(f"[P15] x=15 M={M}: {n3} 3-subsets of support, "
              f"{len(esc3)} escapes ({OUT['partP15'][str(M)]['secs']}s)",
              flush=True)
        dump()


def partP27():
    x = 27
    rng = random.Random(197)
    for M in (80, 112, 144):
        t0 = time.time()
        g = Gadget(M, x)
        sup = support_values(M, x)
        intact = g.query([])
        row = {"support_size": len(sup),
               "intact": "SAT!" if intact else "UNSAT"}
        print(f"[P27] M={M}: support {len(sup)} values, "
              f"intact={row['intact']}", flush=True)
        n1, esc1, _ = census(g, ([v] for v in sup), f"P27 M={M} sup1")
        n2, esc2, _ = census(g, itertools.combinations(sup, 2),
                             f"P27 M={M} sup2")
        row.update({"n1": n1, "escapes1": esc1,
                    "n2": n2, "escapes2": esc2})
        if M == 80:
            n3, esc3, _ = census(g, itertools.combinations(sup, 3),
                                 f"P27 M={M} sup3-ALL")
            row.update({"n3": n3, "escapes3": esc3, "sup3": "exhaustive"})
        else:
            # budgeted: a pathological UNSAT triple at M = 112 burned
            # > 7 min in the first run; cap and record UNKNOWNs
            bots = [v for v in sup if v <= M + 14]
            trip = list(itertools.combinations(bots, 3))
            seen = set(map(frozenset, trip))
            while len(trip) < len(seen) + 300:
                P = frozenset(rng.sample(sup, 3))
                if P not in seen:
                    seen.add(P)
                    trip.append(tuple(sorted(P)))
            n3, esc3, unk3 = census(g, trip, f"P27 M={M} sup3-bot+rand",
                                    budget=300_000)
            row.update({"n3": n3, "escapes3": esc3, "unknown3": unk3,
                        "sup3": "bottom-exhaustive + 300 random, "
                                "300k-conflict budget"})
        g.delete()
        row["secs"] = round(time.time() - t0, 1)
        OUT.setdefault("partP27", {})[str(M)] = row
        print(f"[P27] M={M} done ({row['secs']}s)", flush=True)
        dump()


def partKCRIT():
    x, M = 27, 80
    g = Gadget(M, x)
    pool = IDPool(start_from=g.top + 10)
    neg = [-g.sel[v] for v in g.vals]     # true iff v punctured
    row = {}
    for k in range(3, 9):
        t0 = time.time()
        card = CardEnc.atmost(lits=neg, bound=k, vpool=pool,
                              encoding=EncType.seqcounter)
        sol = Cadical195(bootstrap_with=g.clauses + card.clauses)
        sol.conf_budget(20_000_000)
        r = sol.solve_limited()
        if r is True:
            model = set(l for l in sol.get_model() if l > 0)
            P = [v for v in g.vals if g.sel[v] not in model]
            # re-verify through the audited gadget path
            assert g.query(P), "cardinality witness failed re-query"
            row[k] = {"verdict": "SAT",
                      "escape": [offset(v, M) for v in sorted(P)],
                      "secs": round(time.time() - t0, 1)}
        elif r is False:
            row[k] = {"verdict": "UNSAT",
                      "secs": round(time.time() - t0, 1)}
        else:
            row[k] = {"verdict": "UNKNOWN (budget)",
                      "secs": round(time.time() - t0, 1)}
        sol.delete()
        print(f"[KCRIT] x=27 M=80 atmost-{k} punctures: {row[k]}",
              flush=True)
        OUT["partKCRIT"] = row
        dump()
        if r is True:
            break
    g.delete()


def partKCRIT15():
    """x=15: atmost-2 punctures ANYWHERE must be UNSAT (=> d*(15)=3
    globally, closing the off-support hole in the pair censuses)."""
    x = 15
    row = {}
    for M in (80, 112, 144):
        g = Gadget(M, x)
        pool = IDPool(start_from=g.top + 10)
        neg = [-g.sel[v] for v in g.vals]
        t0 = time.time()
        card = CardEnc.atmost(lits=neg, bound=2, vpool=pool,
                              encoding=EncType.seqcounter)
        sol = Cadical195(bootstrap_with=g.clauses + card.clauses)
        r = sol.solve()
        row[M] = {"atmost2": "SAT!" if r else "UNSAT",
                  "secs": round(time.time() - t0, 1)}
        sol.delete()
        g.delete()
        print(f"[KCRIT15] x=15 M={M} atmost-2 anywhere: {row[M]}",
              flush=True)
        OUT["partKCRIT15"] = row
        dump()


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


def partROTB():
    N = 1 << 17
    isA = [False] * (N + 1)
    for v in range(1, N + 1):
        isA[v] = rot4_isA(v)
    pref = [0] * (N + 1)
    for v in range(1, N + 1):
        pref[v] = pref[v - 1] + (1 if isA[v] else 0)
    excA = max(6 * (pref[2 * a] - pref[a]) - 5 * a
               for a in range(32, N // 2 + 1))
    excB = max(6 * ((2 * a - a) - (pref[2 * a] - pref[a])) - 5 * a
               for a in range(32, N // 2 + 1))
    OUT["partROTB"] = {"maxexc_A": excA, "maxexc_B": excB,
                       "range": "32 <= a <= 2^16"}
    print(f"[ROTB] max_a 6|T n (a,2a]| - 5a: A={excA}, B={excB} "
          f"(<= 0 means sup window density <= 5/6 for both teams)",
          flush=True)
    dump()


PARTS = {"partP15": partP15, "partP27": partP27,
         "partKCRIT": partKCRIT, "partKCRIT15": partKCRIT15,
         "partROTB": partROTB}

if __name__ == "__main__":
    want = sys.argv[1:] or ["all"]
    names = list(PARTS) if want == ["all"] else want
    t0 = time.time()
    for nm in names:
        PARTS[nm]()
    print(f"total {time.time()-t0:.0f}s -> {BASE}/e174_n3_growth.json",
          flush=True)
