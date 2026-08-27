"""e130c_punctured_schema: GAP-N3, the two missing machine layers.

Part 1 (semantic, lane-wide): the e130b fallback lanes were swept on
INTACT blocks; here each catalogued core K is swept on the PUNCTURED
universe (M, 2M] \\ {v} for every rung-unit value v not used by K
(the puncture K is meant to dodge).  UNSAT everywhere on the dyadic
sweep ==> the anchor-freedom catalogue is semantically lane-true.

Part 2 (derivation-level): the e124e/g closure engine (R1-R4 + transitivity
fixpoint, Lemma-D fiat polarities per maximal ladder RUN) re-run on
punctured universes.  A puncture severs its ladder into two runs, each
with its own polarity (2 extra branches).  For the {11,12} K4 core at
M == 0 mod 8: seeds = 4 units + split literal on the battleground
(t1 vs m0; when m0 itself is punctured, try t1 vs m0-2 and m0+2);
branches = split x per-run polarities of [O, Q2, Q3] restricted to the
punctured universe.  ALL branches closing = a machine-witnessed
derivation of the punctured rung within the hand toolkit (Lemma D +
zigzag propagation), i.e. the severed-ladder extension works.
Controls at M == 4 mod 8 must leave survivors.

Run: .venv/bin/python experiments/e130c_punctured_schema.py [part1|part2]
Artifacts: data/e130c_punctured.json
"""
import itertools
import json
import sys
import time
from collections import defaultdict

from pysat.solvers import Cadical195

BASE = "/Users/will/Dev/personal/tasks/math/erdos197/data"
OUT = {}

CORES = {
    (15, "C3"): [(5, 5), (3, 6), (10, 3)],
    (15, "F3"): [(7, 4), (4, 6), (2, 7)],
    (15, "G6"): [(11, 2), (6, 5), (5, 5), (2, 7)],
    (11, "A4a"): [(0, 6), (1, 5), (2, 5), (3, 4)],
    (11, "A4d"): [(1, 5), (2, 5), (3, 4), (6, 3)],
    (11, "H1"): [(7, 2), (3, 4), (2, 5), (0, 6)],
    (11, "H4"): [(9, 1), (7, 2), (2, 5), (0, 6)],
    (11, "H5"): [(8, 2), (6, 3), (3, 4), (0, 6)],
}
THRESH = {"C3": 16, "F3": 16, "G6": 64, "A4a": 16, "A4d": 16,
          "H1": 16, "H4": 16, "H5": 48}


def rung_unit_values(M, x):
    vals = set()
    for a in (x, x + 1):
        for y in range(M + 1, 2 * M + 1):
            z = 2 * y - a
            if M < z <= 2 * M and z != y:
                vals |= {z, y}
    return vals


def part1():
    scales = list(range(16, 161, 8))
    for x in (11, 15):
        cores = {n: us for (xx, n), us in CORES.items() if xx == x}
        fails = defaultdict(list)
        t0 = time.time()
        for M in scales:
            n = M
            var = {}
            c = 0
            for p in range(n):
                for q in range(p + 1, n):
                    c += 1
                    var[(p, q)] = c

            def o(u, w):
                p, q = u - M - 1, w - M - 1
                return var[(p, q)] if p < q else -var[(q, p)]

            sel = {}
            for v in range(M + 1, 2 * M + 1):
                c += 1
                sel[v] = c
            cl = []
            for y in range(M + 2, 2 * M):
                d = 1
                while y + d <= 2 * M and y - d > M:
                    a, b = y - d, y + d
                    g = [-sel[a], -sel[y], -sel[b]]
                    cl.append(g + [-o(a, y), -o(y, b)])
                    cl.append(g + [-o(b, y), -o(y, a)])
                    d += 1
            for p in range(n):
                for q in range(p + 1, n):
                    vpq = var[(p, q)]
                    for r in range(q + 1, n):
                        cl.append([-vpq, -var[(q, r)], var[(p, r)]])
                        cl.append([vpq, var[(q, r)], -var[(p, r)]])
            usel = {}
            for name, us in cores.items():
                for (i, j) in us:
                    if (i, j) in usel:
                        continue
                    z, y = 2 * M - i, M + j
                    c += 1
                    usel[(i, j)] = c
                    cl.append([-c, -sel[z], -sel[y], o(z, y)])
            sol = Cadical195(bootstrap_with=cl)
            uvals = rung_unit_values(M, x)
            for name, us in cores.items():
                if M < THRESH[name]:
                    continue
                kvals = set()
                for (i, j) in us:
                    kvals |= {2 * M - i, M + j}
                for v in sorted(uvals - kvals):
                    assump = ([usel[u] for u in us]
                              + [-usel[u] for u in usel if u not in us]
                              + [(-sel[w] if w == v else sel[w])
                                 for w in range(M + 1, 2 * M + 1)])
                    if sol.solve(assumptions=assump):
                        fails[name].append((M, v))
            sol.delete()
        row = {name: ([list(t) for t in fails[name]] if fails[name]
                      else "UNSAT at every (M, puncture) tested")
               for name in cores}
        OUT[f"part1_x{x}"] = row
        print(f"[1] x={x}: {row}  ({time.time()-t0:.0f}s)", flush=True)
        dump()


# ---------- Part 2: punctured closure engine ----------

def closure(M, seeds, punct=frozenset()):
    lo, hi = M + 1, 2 * M
    alive = [v for v in range(lo, hi + 1) if v not in punct]
    aset = set(alive)
    aps = []
    for y in alive:
        d = 1
        while y + d <= hi and y - d >= lo:
            if y - d in aset and y + d in aset:
                aps.append((y - d, y, y + d))
            d += 1
    facts = set(seeds)
    rule = defaultdict(list)
    for (x, y, z) in aps:
        rule[(x, y)].append((z, y))
        rule[(z, y)].append((x, y))
        rule[(y, x)].append((y, z))
        rule[(y, z)].append((y, x))
    frontier = list(facts)
    succ = defaultdict(set)
    pred = defaultdict(set)
    for (u, v) in facts:
        succ[u].add(v)
        pred[v].add(u)
    bad = []

    def add(u, v):
        if (u, v) in facts:
            return None
        if (v, u) in facts or u == v:
            return (u, v)
        facts.add((u, v))
        succ[u].add(v)
        pred[v].add(u)
        frontier.append((u, v))
        return None

    while frontier:
        (u, v) = frontier.pop()
        for conc in rule[(u, v)]:
            if add(*conc):
                return "contradiction"
        for w in list(pred[u]):
            if add(w, v):
                return "contradiction"
        for w in list(succ[v]):
            if add(u, w):
                return "contradiction"
    return "fixpoint"


def runs_of(first, d, last, punct):
    """Maximal runs of the d-ladder avoiding punct."""
    out, cur = [], []
    v = first
    while v <= last:
        if v in punct:
            if len(cur) >= 2:
                out.append(cur)
            cur = []
        else:
            cur.append(v)
        v += d
    if len(cur) >= 2:
        out.append(cur)
    return out


def fiat_edges(run, leader_first):
    e0 = 0 if leader_first else 1
    ed = set()
    for i in range(e0, len(run), 2):
        if i > 0:
            ed.add((run[i], run[i - 1]))
        if i + 1 < len(run):
            ed.add((run[i], run[i + 1]))
    return ed


def k4_branches(M, punct, battleground):
    """All-branch closure for the full K4 core + split on battleground."""
    t0v, t1v, t2v, t3v = 2 * M, 2 * M - 1, 2 * M - 2, 2 * M - 3
    b4, b5, b6 = M + 4, M + 5, M + 6
    core = {(t0v, b6), (t1v, b5), (t2v, b5), (t3v, b4)}
    pset = frozenset(punct)
    for v in core.copy():
        assert v[0] not in pset and v[1] not in pset, "core hit by puncture"
    ladders = [(M + 1, 2, 2 * M - 1), (M + 2, 4, 2 * M - 2),
               (M + 3, 4, 2 * M - 1), (M + 4, 4, 2 * M)]
    all_runs = []
    for (f, d, l) in ladders:
        all_runs += runs_of(f, d, l, pset)
    c = battleground
    surv = 0
    tot = 0
    for split in ((t1v, c), (c, t1v)):
        for pol in itertools.product((True, False), repeat=len(all_runs)):
            tot += 1
            seeds = set(core) | {split}
            for run, lf in zip(all_runs, pol):
                seeds |= fiat_edges(run, lf)
            if closure(M, seeds, pset) != "contradiction":
                surv += 1
    return surv, tot, len(all_runs)


def part2():
    rows = {}
    for M in (48, 80, 112):
        m0 = 3 * M // 2
        cases = {
            "none": ([], m0),
            "odd_mid_hi": ([m0 + 7], m0),          # odd, severs O and Q3/Q1
            "odd_mid_lo": ([m0 - 9], m0),
            "even_mid": ([m0 + 2], m0),            # severs one even Q-ladder
            "b1": ([M + 1], m0),
            "t5": ([2 * M - 5], m0),
            "m0_c+2": ([m0], m0 + 2),              # battleground moved
            "m0_c-2": ([m0], m0 - 2),
        }
        rows[M] = {}
        for name, (punct, c) in cases.items():
            t0 = time.time()
            try:
                surv, tot, nruns = k4_branches(M, punct, c)
            except AssertionError as e:
                rows[M][name] = f"skipped: {e}"
                continue
            rows[M][name] = {"surviving": surv, "branches": tot,
                             "runs": nruns,
                             "secs": round(time.time() - t0, 1)}
            print(f"[2] M={M} {name}: {rows[M][name]}", flush=True)
            OUT["part2"] = rows
            dump()
    # controls at 4 mod 8: survivors expected
    for M in (52, 84):
        surv, tot, nruns = k4_branches(M, [], 3 * M // 2)
        rows[M] = {"control_intact": {"surviving": surv, "branches": tot}}
        print(f"[2] control M={M}: surviving {surv}/{tot}", flush=True)
    OUT["part2"] = rows
    dump()


def dump():
    json.dump(OUT, open(f"{BASE}/e130c_punctured.json", "w"), indent=1)


def main():
    which = sys.argv[1:] or ["part1", "part2"]
    if "part1" in which:
        part1()
    if "part2" in which:
        part2()
    dump()
    print(f"-> {BASE}/e130c_punctured.json", flush=True)


if __name__ == "__main__":
    main()
