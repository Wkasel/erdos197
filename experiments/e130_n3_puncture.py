"""e130_n3_puncture: GAP-N3 machine layer -- adversarial puncture placement
on the MUS support of the single-block generic-pair rungs.

Object: full rung OG_{x,x+1}(M) on (M, 2M] \\ P -- AP-freeness (monotone
3-AP forbidden) over surviving values + ALL attack units (z = 2y - a,
a in {x, x+1}, z != y, both surviving) + total order.

Encoding: e120-style selection guards.  One base instance per (x, M):
order vars o(u,w) on the FULL block, COMPLETE transitivity (unguarded --
sound: a total order on the block restricts to a total order on any
subset), AP clauses and units guarded by per-value selectors s_v.
A puncture set P is queried as assumptions {-s_v : v in P} +
{s_w : w not in P}.  UNSAT ==> the punctured rung is UNSAT.  Every SAT
verdict is re-checked by an independent scanner on the decoded order.

Parts:
  A  {11,12}, M = 80, 112, 144 (all == 0 mod 8, disjoint from e120's
     64/96/128): EVERY single puncture v in (M, 2M].  Expected: all
     UNSAT (e120 d* = 2).  Controls: P = {M+2, M+4} expected SAT.
  B  {15,16}, same scales: every single puncture; every 2-subset of the
     SUPPORT REGION S = {M+1..M+8} u {m0-3..m0+3} u {2M-14..2M}
     (the C3 schema anchors + flood centers + full attack surface);
     plus 40 random off-region 2-subsets.  Expected: all UNSAT
     (e120 d* = 3).  Controls: {M+2,M+4,M+5} expected SAT.
  C  MUS anatomy: for each anchor puncture (C3 values b3,b5,b6,t3,t5,
     t10, centers m0,m0+-1, top t1 for {15,16}; K4 values b4,b5,b6,
     t0..t3, m0 for {11,12}) at M = 80: minimal UNIT core of the
     punctured instance (deletion minimization over unit list), and
     which of the catalogued lane cores (A4a-d, B2, B6, C, D3) still
     fire on the punctured universe.
  D  {11,12} at M == 2 mod 8 (B2 schema class), M = 82, 114: every
     single puncture -- is 1-puncture robustness class-uniform?

Run: .venv/bin/python experiments/e130_n3_puncture.py [partA|partB|partC|partD|all]
Artifacts: data/e130_n3_puncture.json (+ .log via tee in caller)
"""
import json
import random
import sys
import time

from pysat.solvers import Cadical195

BASE = "/Users/will/Dev/personal/tasks/math/erdos197/data"
OUT = {}


def rung_units(M, x):
    """All attack units of pair {x, x+1} on (M, 2M]: (z, y) meaning
    the completion forces z < y (z placed before y)."""
    us = []
    for a in (x, x + 1):
        for y in range(M + 1, 2 * M + 1):
            z = 2 * y - a
            if M < z <= 2 * M and z != y:
                us.append((z, y))
    return sorted(set(us))


class Gadget:
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
        # guarded AP clauses (midpoint-extremal rule)
        for y in vals:
            d = 1
            while y + d <= 2 * M and y - d > M:
                a, b = y - d, y + d
                g = [-self.sel[a], -self.sel[y], -self.sel[b]]
                cl.append(g + [-o(a, y), -o(y, b)])
                cl.append(g + [-o(b, y), -o(y, a)])
                d += 1
        # complete transitivity, unguarded
        for p in range(n):
            for q in range(p + 1, n):
                vpq = var[(p, q)]
                for r in range(q + 1, n):
                    vqr, vpr = var[(q, r)], var[(p, r)]
                    cl.append([-vpq, -vqr, vpr])
                    cl.append([vpq, vqr, -vpr])
        # guarded units
        self.units = rung_units(M, x)
        for (z, y) in self.units:
            cl.append([-self.sel[z], -self.sel[y], o(z, y)])
        self.solver = Cadical195(bootstrap_with=cl)

    def query(self, P, budget=None):
        """SAT/UNSAT of the rung on (M,2M] \\ P."""
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


def mus_units(M, x, P):
    """Deletion-minimal set of units keeping AP+units UNSAT on
    (M,2M] \\ P.  Fresh instance with unit-assumption literals."""
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
    if sol.solve(assumptions=[amap[u] for u in live]):
        sol.delete()
        return None  # punctured rung is SAT: no core
    for u in list(live):
        trial = [w for w in live if w != u]
        if not sol.solve(assumptions=[amap[w] for w in trial]):
            live = trial
    sol.delete()
    return live


def lane_cores(M, x):
    """Catalogued small cores in value form for this pair at this M."""
    m0 = 3 * M // 2
    d = {}
    if x == 11:
        d = {"A4a": [(0, 6), (1, 5), (2, 5), (3, 4)],
             "A4b": [(0, 6), (2, 5), (3, 4), (7, 2)],
             "A4c": [(0, 6), (2, 5), (7, 2), (9, 1)],
             "A4d": [(1, 5), (2, 5), (3, 4), (6, 3)],
             "B2": [(2, 5), (5, 3), (7, 2)],
             "B6": [(3, 4), (5, 3), (10, 1)],
             "C": [(0, 6), (2, 5), (5, 3)]}
    elif x == 15:
        d = {"D3=C3": [(5, 5), (3, 6), (10, 3)],
             "B6(15)": [(7, 4), (9, 3), (14, 1)]}
    out = {}
    for name, ij in d.items():
        out[name] = [(2 * M - i, M + j) for (i, j) in ij]
    return out, m0


def fmt_val(M, v):
    m0 = 3 * M // 2
    if v <= M + 20:
        return f"b{v - M}"
    if v >= 2 * M - 20:
        return f"t{2 * M - v}"
    if abs(v - m0) <= 4:
        s = v - m0
        return f"m0{'+' if s >= 0 else ''}{s}" if s else "m0"
    return str(v)


def part_single(x, scales, tag, controls):
    res = {}
    for M in scales:
        t0 = time.time()
        g = Gadget(M, x)
        bad = []
        for v in range(M + 1, 2 * M + 1):
            if g.query([v]):
                bad.append(v)
        ctrl = {}
        for P in controls(M):
            ctrl[str(sorted(P))] = "SAT" if g.query(P) else "UNSAT"
        g.delete()
        res[M] = {"n_single": M, "escapes": bad, "controls": ctrl,
                  "secs": round(time.time() - t0, 1)}
        print(f"[{tag}] x={x} M={M}: single-puncture escapes={bad or 'NONE'}"
              f" controls={ctrl} ({res[M]['secs']}s)", flush=True)
        OUT.setdefault(tag, {})[str(M)] = res[M]
        dump()
    return res


def partA():
    part_single(11, [80, 112, 144], "A_11_r0",
                lambda M: [[M + 2, M + 4]])


def partD():
    part_single(11, [82, 114], "D_11_r2",
                lambda M: [[M + 2, M + 4]])


def partB():
    x = 15
    for M in [80, 112, 144]:
        t0 = time.time()
        g = Gadget(M, x)
        m0 = 3 * M // 2
        bad1 = [v for v in range(M + 1, 2 * M + 1) if g.query([v])]
        S = (list(range(M + 1, M + 9)) + list(range(m0 - 3, m0 + 4))
             + list(range(2 * M - 14, 2 * M + 1)))
        S = sorted(set(S))
        bad2 = []
        pairs = [(u, v) for i, u in enumerate(S) for v in S[i + 1:]]
        for (u, v) in pairs:
            if g.query([u, v]):
                bad2.append((u, v))
        rng = random.Random(197)
        others = [v for v in range(M + 1, 2 * M + 1) if v not in S]
        rnd = []
        for _ in range(40):
            u, v = rng.sample(others, 2)
            if g.query([u, v]):
                rnd.append((u, v))
        ctrl = {"esc3": "SAT" if g.query([M + 2, M + 4, M + 5]) else "UNSAT"}
        g.delete()
        row = {"singles_escapes": bad1,
               "support_region": [fmt_val(M, v) for v in S],
               "n_support_pairs": len(pairs),
               "support_pair_escapes":
                   [[fmt_val(M, u), fmt_val(M, v)] for u, v in bad2],
               "rand_pair_escapes": rnd, "controls": ctrl,
               "secs": round(time.time() - t0, 1)}
        OUT.setdefault("B_15_r0", {})[str(M)] = row
        print(f"[B] x=15 M={M}: singles esc={bad1 or 'NONE'}; "
              f"{len(pairs)} support-pairs esc={bad2 or 'NONE'}; "
              f"rand esc={rnd or 'NONE'}; ctrl={ctrl} ({row['secs']}s)",
              flush=True)
        dump()


def partC():
    for x, M, anchors in [
            (15, 80, ["b3", "b5", "b6", "t3", "t5", "t10",
                      "m0", "m0-1", "m0+1", "t1"]),
            (11, 80, ["b4", "b5", "b6", "t0", "t1", "t2", "t3", "m0"])]:
        m0 = 3 * M // 2
        name2val = {}
        for j in range(0, 21):
            name2val[f"b{j}"] = M + j
            name2val[f"t{j}"] = 2 * M - j
        name2val["m0"] = m0
        name2val["m0-1"] = m0 - 1
        name2val["m0+1"] = m0 + 1
        cores, _ = lane_cores(M, x)
        rows = {}
        for a in anchors:
            v = name2val[a]
            t0 = time.time()
            core = mus_units(M, x, [v])
            if core is None:
                rows[a] = {"verdict": "SAT (escape!)"}
            else:
                vals_used = sorted(set([z for z, y in core]
                                       + [y for z, y in core]))
                surviving = [nm for nm, us in cores.items()
                             if all(z != v and y != v for (z, y) in us)]
                rows[a] = {
                    "core_units": [[fmt_val(M, z), fmt_val(M, y)]
                                   for (z, y) in sorted(core)],
                    "core_vals": [fmt_val(M, w) for w in vals_used],
                    "catalogued_cores_avoiding_v": surviving,
                    "secs": round(time.time() - t0, 1)}
            print(f"[C] x={x} M={M} puncture {a}: {rows[a]}", flush=True)
            OUT.setdefault(f"C_{x}", {})[a] = rows[a]
            dump()


def dump():
    json.dump(OUT, open(f"{BASE}/e130_n3_puncture.json", "w"), indent=1)


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    t0 = time.time()
    if which in ("partA", "all"):
        partA()
    if which in ("partB", "all"):
        partB()
    if which in ("partC", "all"):
        partC()
    if which in ("partD", "all"):
        partD()
    dump()
    print(f"total {time.time() - t0:.0f}s -> {BASE}/e130_n3_puncture.json",
          flush=True)


if __name__ == "__main__":
    main()
