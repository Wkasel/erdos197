"""e133_catalogue_closure: GAP-N3 final machine layer (notes/53 SSA).

Claim backed [notes/53 Theorem N3-CAT]: the finite core catalogue for
pair {15,16} (resp. {11,12}) on the dyadic lane M == 0 mod 8 is
2-hitting-closed (resp. 1-hitting-closed): for EVERY puncture set P of
size <= 2 (resp. <= 1) drawn from the FULL unit-support region S, some
catalogued core K has support(K) disjoint from P and K alone (its <= 5
units + the AP/order theory of the punctured universe (M, 2M] \\ P) is
UNSAT.  This is stronger than the e130 sweeps in two ways: the
refutation is required to come from a CATALOGUED bounded core (not the
full Theta(M)-unit rung), and the scales are fresh (88, 120, 152 --
disjoint from e130/e132's 80/112/144 and e120's 64/96/128).

Catalogue: the four e130b lane cores (C3, F3, Q4, G6) + the eleven
fresh deletion-minimal cores discovered by e132 partS on the
catalogue-busting 2-sets, all in offset form (i, j) = unit
t_i < b_j, i.e. (2M - i) must precede (M + j); validity i + 2j in
{x, x+1}.

Output: for each (M, P): the first avoiding+firing core, or FAILURE
(then the full-rung verdict as fallback diagnosis).  Any FAILURE
falsifies Theorem N3-CAT as stated for that scale.

Run: .venv/bin/python experiments/e133_catalogue_closure.py
Artifacts: data/e133_catalogue_closure.json (+ .log)
"""
import itertools
import json
import time

from pysat.solvers import Cadical195

BASE = "/Users/will/Dev/personal/tasks/math/erdos197/data"
OUT = {}

CAT15 = {
    "C3":  [(5, 5), (3, 6), (10, 3)],
    "F3":  [(7, 4), (4, 6), (2, 7)],
    "Q4":  [(5, 5), (4, 6), (3, 6), (2, 7)],
    "G6":  [(11, 2), (6, 5), (5, 5), (2, 7)],
    "W1":  [(13, 1), (7, 4), (5, 5), (2, 7)],
    "W2":  [(12, 2), (6, 5), (5, 5), (3, 6)],
    "W3":  [(11, 2), (4, 6), (3, 6), (2, 7)],
    "W4":  [(11, 2), (9, 3), (7, 4), (2, 7)],
    "F3s": [(10, 3), (7, 4), (4, 6)],
    "W5":  [(9, 3), (7, 4), (3, 6), (2, 7)],
    "W6":  [(11, 2), (10, 3), (5, 5)],
    "W7":  [(12, 2), (7, 4), (6, 5)],
    "W8":  [(11, 2), (7, 4), (6, 5), (2, 7)],
    "W9":  [(11, 2), (9, 3), (5, 5), (2, 7)],
    "W10": [(7, 4), (6, 5), (3, 6), (2, 7)],
}
CAT11 = {
    "A4a": [(0, 6), (1, 5), (2, 5), (3, 4)],
    "A4d": [(1, 5), (2, 5), (3, 4), (6, 3)],
    "H1":  [(7, 2), (3, 4), (2, 5), (0, 6)],
    "H4":  [(9, 1), (7, 2), (2, 5), (0, 6)],
    "H5":  [(8, 2), (6, 3), (3, 4), (0, 6)],
}
for x, cat in ((15, CAT15), (11, CAT11)):
    for name, us in cat.items():
        for (i, j) in us:
            assert i + 2 * j in (x, x + 1), (x, name, i, j)


def unit_values(M, x):
    vals = set()
    for a in (x, x + 1):
        for y in range(M + 1, 2 * M + 1):
            z = 2 * y - a
            if M < z <= 2 * M and z != y:
                vals |= {z, y}
    return vals


class Base:
    """Guarded instance: value selectors + per-catalogue-core activators.
    Core K active + values selected ==> K's units enforced.  AP clauses
    guarded by selectors; complete transitivity unguarded (sound: a
    total order on the block restricts to any subset)."""

    def __init__(self, M, x, cat):
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
                    cl.append([-vpq, -var[(q, r)], var[(p, r)]])
                    cl.append([vpq, var[(q, r)], -var[(p, r)]])
        # full-rung units, individually activatable via one rung литерal
        self.act = {}
        self.support = {}
        for name, ij in cat.items():
            c += 1
            self.act[name] = c
            supp = set()
            for (i, j) in ij:
                z, y = 2 * M - i, M + j
                assert M < z <= 2 * M and M < y <= 2 * M and z != y
                supp |= {z, y}
                cl.append([-c, -self.sel[z], -self.sel[y], o(z, y)])
            self.support[name] = supp
        # full rung activator (fallback diagnosis)
        c += 1
        self.act_full = c
        for a in (x, x + 1):
            for y in vals:
                z = 2 * y - a
                if M < z <= 2 * M and z != y:
                    cl.append([-c, -self.sel[z], -self.sel[y], o(z, y)])
        self.solver = Cadical195(bootstrap_with=cl)

    def query_core(self, name, P):
        P = set(P)
        assump = [(-self.sel[v] if v in P else self.sel[v])
                  for v in self.vals]
        assump += [self.act[name]]
        assump += [-self.act[n2] for n2 in self.act if n2 != name]
        assump += [-self.act_full]
        return self.solver.solve(assumptions=assump)   # True = SAT

    def query_full(self, P):
        P = set(P)
        assump = [(-self.sel[v] if v in P else self.sel[v])
                  for v in self.vals]
        assump += [-self.act[n2] for n2 in self.act]
        assump += [self.act_full]
        return self.solver.solve(assumptions=assump)

    def delete(self):
        self.solver.delete()


def run(x, cat, budget, scales):
    tag = f"x{x}_budget{budget}"
    OUT[tag] = {}
    for M in scales:
        t0 = time.time()
        base = Base(M, x, cat)
        # support region = all values usable by ANY unit of the pair
        S = sorted(unit_values(M, x))
        rows = {}
        n_ok = 0
        fails = []
        subsets = (itertools.combinations(S, budget) if budget > 1
                   else [(v,) for v in S])
        for P in subsets:
            hit = None
            for name in cat:
                if base.support[name] & set(P):
                    continue
                if not base.query_core(name, P):     # UNSAT = fires
                    hit = name
                    break
            if hit is None:
                full = "UNSAT" if not base.query_full(P) else "SAT"
                fails.append({"P": [v - M for v in P],  # offsets from M
                              "full_rung": full})
            else:
                n_ok += 1
                rows[hit] = rows.get(hit, 0) + 1
        base.delete()
        rec = {"n_support_vals": len(S), "n_subsets": n_ok + len(fails),
               "closed": n_ok, "failures": fails,
               "core_usage": rows, "secs": round(time.time() - t0, 1)}
        OUT[tag][str(M)] = rec
        print(f"[{tag}] M={M}: {n_ok}/{n_ok + len(fails)} subsets closed "
              f"by catalogue; failures={fails or 'NONE'}; usage={rows} "
              f"({rec['secs']}s)", flush=True)
        json.dump(OUT, open(f"{BASE}/e133_catalogue_closure.json", "w"),
                  indent=1)


def main():
    t0 = time.time()
    run(11, CAT11, 1, [88, 120, 152])
    run(15, CAT15, 1, [88, 120, 152])
    run(15, CAT15, 2, [88, 120, 152])
    print(f"total {time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
