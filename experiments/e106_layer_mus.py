"""e106_layer_mus: are the individual S1 layer lemmas hand-provable as
fixed parametric case trees?  (Backs Section 4 / gap G-A of notes/33.)

For each layer lemma, extract a deletion-minimal AP-triple support of the
FORCING (hypothesis units + negated conclusion unit => UNSAT), at several
scales, and measure (a) support size growth, (b) cross-scale stability in
bottom-anchored (v-M) and top-anchored (2M-v) offset coordinates.

Lemmas (hyp units => forced conclusion), per S1/e101:
  L0a: A2, A3            => t3 < b3     (every even M)
  L0b: A2, A3            => t10 < b6    (every even M)
  L1a: A2, A3, L0        => t3 < t5     (M == 0 mod 4)   [incremental]
  L1b: A2, A3, L0        => b5 < b3     (M == 0 mod 4)   [incremental]
  L2 : A2, A3, L0, L1    => b5 < t5     (M == 0 mod 8)   [incremental]
where L0 = {t3<b3, t10<b6}, L1 = {t3<t5, b5<b3} added as units.

Interpretation for the hand proof: if some lemma's support is small and
its offset-coordinate triple list is IDENTICAL across scales (in either
anchor frame), a fixed parametric case tree exists and the lemma is
hand-provable by finite case analysis; if the support grows with M, no
such fixed-list hand proof exists (in this architecture) and the lemma
stays [MACHINE-BASE].

Method: eager full-transitivity encoding + per-triple selectors,
core-shrink to fixpoint, then greedy deletion (deterministic shuffle),
as e103.  One elimination order per (lemma, scale): the minima are upper
bounds; cross-scale commonality is a lower bound.

Output: data/e106_layer_mus.json
"""
import json
import random
import time

from pysat.solvers import Cadical195

DATA = "/Users/will/Dev/personal/tasks/math/erdos197/data/e106_layer_mus.json"


def nu2(d):
    v = 0
    while d % 2 == 0:
        d //= 2
        v += 1
    return v


def six(M):
    return {"t5": 2 * M - 5, "t3": 2 * M - 3, "t10": 2 * M - 10,
            "b3": M + 3, "b5": M + 5, "b6": M + 6}


def build(M, units):
    """Eager order encoding, hard unit clauses, per-AP-triple selectors."""
    V = list(range(M + 1, 2 * M + 1))
    n = len(V)
    idx = {v: i for i, v in enumerate(V)}
    var = {}
    c = 0
    for i in range(n):
        for j in range(i + 1, n):
            c += 1
            var[(i, j)] = c

    def lit(i, j):
        return var[(i, j)] if i < j else -var[(j, i)]

    def o(u, w):
        return lit(idx[u], idx[w])

    cl = []
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                cl.append([-lit(i, j), -lit(j, k), lit(i, k)])
                cl.append([lit(i, j), lit(j, k), -lit(i, k)])
    for (u, w) in units:
        cl.append([o(u, w)])
    triples, sel = [], {}
    for y in V:
        d = 1
        while y + d <= 2 * M:
            x, z = y - d, y + d
            d += 1
            if x > M:
                c += 1
                t = (x, y, z)
                triples.append(t)
                sel[t] = c
                cl.append([-c, -o(x, y), -o(y, z)])
                cl.append([-c, -o(z, y), -o(y, x)])
    return Cadical195(bootstrap_with=cl), triples, sel


def mus(M, units, seed=0):
    solver, triples, sel = build(M, units)
    try:
        assum = {sel[t]: t for t in triples}
        active = list(assum)
        st = solver.solve(assumptions=active)
        if st:
            return None  # not UNSAT: lemma not forced here
        while True:
            core = [l for l in (solver.get_core() or []) if l in assum]
            if len(core) >= len(active):
                break
            active = core
            assert not solver.solve(assumptions=active)
        rnd = random.Random(seed)
        order = active[:]
        rnd.shuffle(order)
        keep = set(active)
        for s in order:
            if s not in keep:
                continue
            trial = [x for x in keep if x != s]
            if not solver.solve(assumptions=trial):
                keep = set(trial)
                core = [l for l in (solver.get_core() or []) if l in keep]
                if core and len(core) < len(keep):
                    keep = set(core)
        return sorted(assum[s] for s in keep)
    finally:
        solver.delete()


def lemma_units(M, name):
    s = six(M)
    A2 = (s["t3"], s["b6"])
    A3 = (s["t10"], s["b3"])
    L0 = [(s["t3"], s["b3"]), (s["t10"], s["b6"])]
    L1 = [(s["t3"], s["t5"]), (s["b5"], s["b3"])]
    hyp = {
        "L0a": [A2, A3], "L0b": [A2, A3],
        "L1a": [A2, A3] + L0, "L1b": [A2, A3] + L0,
        "L2": [A2, A3] + L0 + L1,
    }[name]
    goalneg = {
        "L0a": (s["b3"], s["t3"]), "L0b": (s["b6"], s["t10"]),
        "L1a": (s["t5"], s["t3"]), "L1b": (s["b3"], s["b5"]),
        "L2": (s["t5"], s["b5"]),
    }[name]
    return hyp + [goalneg]


SCALES = {
    "L0a": [42, 46, 50, 44, 52, 60, 48, 56, 64],
    "L0b": [42, 46, 50, 44, 52, 60, 48, 56],
    "L1a": [44, 52, 60, 48, 56, 64],
    "L1b": [44, 52, 60, 48, 56],
    "L2": [48, 56, 64, 72],
}


def main():
    t00 = time.time()
    out = {}
    for name, Ms in SCALES.items():
        out[name] = {}
        bots, tops = [], []
        for M in Ms:
            t0 = time.time()
            sup = mus(M, lemma_units(M, name))
            if sup is None:
                out[name][str(M)] = {"status": "NOT-FORCED"}
                print(f"[{name}] M={M} (mod8={M % 8}): NOT FORCED",
                      flush=True)
                continue
            coords = [{"xyz": t, "d": t[1] - t[0], "act": nu2(t[1]-t[0]) + 1,
                       "bot": [t[0] - M, t[1] - M, t[2] - M],
                       "top": [2*M - t[0], 2*M - t[1], 2*M - t[2]]}
                      for t in sup]
            hist = {}
            for cds in coords:
                k = f"L{min(cds['act'], 4)}"
                hist[k] = hist.get(k, 0) + 1
            bots.append({tuple(c["bot"]) for c in coords})
            tops.append({tuple(c["top"]) for c in coords})
            out[name][str(M)] = {"size": len(sup), "act_hist": hist,
                                 "support": coords,
                                 "time_s": round(time.time() - t0, 1)}
            print(f"[{name}] M={M} (mod8={M % 8}): |MUS|={len(sup)} "
                  f"hist={hist} ({out[name][str(M)]['time_s']}s)",
                  flush=True)
        if bots:
            bc = set.intersection(*bots)
            tc = set.intersection(*tops)
            out[name]["_stability"] = {
                "sizes": [len(b) for b in bots],
                "bot_common": sorted(map(list, bc)),
                "top_common": sorted(map(list, tc)),
            }
            print(f"[{name}] sizes={out[name]['_stability']['sizes']} "
                  f"bot-common={len(bc)} top-common={len(tc)}", flush=True)
    json.dump(out, open(DATA, "w"), indent=1)
    print(f"Done ({time.time()-t00:.0f}s) -> {DATA}", flush=True)


if __name__ == "__main__":
    main()
