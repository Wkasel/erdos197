"""e103_coupling_anatomy: TASK T round 3 -- where does the parity interleave
enter the C3 refutation at M == 0 mod 8?

Rounds 1-2 (e101/e102) proved the mod-8 flip is NOT captured by any unit
projection onto a parity-branch cell at any depth: the full forced odd-odd
backbone of AP+C3, descended, is SAT at every half scale.  So the refutation
lives in the AP triples that COUPLE the parity classes.

Structure: an AP (x, y, z), y-x = z-y = d, has all three values congruent
mod 2^{v} for v = nu_2(d), and its halving images keep difference d/2.  So
the triple descends v2 = nu_2(d) levels intact inside the parity tower and
first couples the two parity cells at level nu_2(d)+1 ("act level").
Layers: L1 = odd d (couples at level 1), L2 = d == 2 mod 4 (acts at level 2),
L3 = d == 4 mod 8 (acts at level 3 -- the mod-8-critical layer),
L4+ = d == 0 mod 8.

Experiment, at M in {40, 48, 56, 64} (all == 0 mod 8; C3 UNSAT):
  1. Eager full-transitivity encoding of AP-freeness + C3 units, one
     selector per AP triple (both direction clauses share the selector).
  2. Core-shrink loop (Cadical assumptions + get_core), then greedy
     deletion => deletion-minimal triple support of the refutation.
  3. Report: support size, histogram by act level, band coordinates
     (bottom-anchored x-M and top-anchored 2M-z), cross-M stability of
     each layer in anchored coordinates.
  4. Layer-necessity: for each layer Lk, test UNSAT with the ENTIRE layer
     removed (all other triples on) => which act levels are indispensable.

Output: data/e103_coupling.json
"""
import json
import random
import time

from pysat.solvers import Cadical195

DATA = "/Users/will/Dev/personal/tasks/math/erdos197/data/e103_coupling.json"


def nu2(d):
    v = 0
    while d % 2 == 0:
        d //= 2
        v += 1
    return v


def build(M):
    """Eager order encoding with per-triple selectors. Returns (solver,
    triples, sel) where sel[t] is the selector literal for triple t."""
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
    # eager transitivity: forbid both 3-cycles on every unordered triple
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                cl.append([-lit(i, j), -lit(j, k), lit(i, k)])
                cl.append([lit(i, j), lit(j, k), -lit(i, k)])
    # C3 units (hard)
    cl.append([o(2 * M - 5, M + 5)])
    cl.append([o(2 * M - 3, M + 6)])
    cl.append([o(2 * M - 10, M + 3)])
    # AP triples with selectors
    triples = []
    sel = {}
    for y in V:
        d = 1
        while y + d <= 2 * M:
            x, z = y - d, y + d
            d += 1
            if x > M:
                c += 1
                s = c
                t = (x, y, z)
                triples.append(t)
                sel[t] = s
                cl.append([-s, -o(x, y), -o(y, z)])
                cl.append([-s, -o(z, y), -o(y, x)])
    solver = Cadical195(bootstrap_with=cl)
    return solver, triples, sel


def act_level(t):
    return nu2(t[1] - t[0]) + 1


def mus(M, seed=0):
    t0 = time.time()
    solver, triples, sel = build(M)
    assum = {sel[t]: t for t in triples}
    active = list(assum)
    st = solver.solve(assumptions=active)
    assert not st, f"M={M}: expected UNSAT with all triples active"
    # core-shrink to fixpoint
    while True:
        core = solver.get_core() or []
        core = [l for l in core if l in assum]
        if len(core) >= len(active):
            break
        active = core
        st = solver.solve(assumptions=active)
        assert not st
    # greedy deletion (deterministic shuffle for reproducibility)
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
    support = sorted(assum[s] for s in keep)
    # layer-necessity on the FULL triple set: drop whole layer, keep rest
    layer_test = {}
    for lv in (1, 2, 3, 4):
        rest = [sel[t] for t in triples if min(act_level(t), 4) != lv]
        layer_test[f"L{lv}"] = ("UNSAT" if not solver.solve(assumptions=rest)
                                else "SAT")
    solver.delete()
    dt = time.time() - t0
    return support, layer_test, dt


def describe(M, support):
    hist = {}
    for t in support:
        lv = min(act_level(t), 4)
        hist[f"L{lv}"] = hist.get(f"L{lv}", 0) + 1
    coords = [{"xyz": t, "d": t[1] - t[0], "act": act_level(t),
               "bot": [t[0] - M, t[1] - M, t[2] - M],
               "top": [2 * M - t[0], 2 * M - t[1], 2 * M - t[2]]}
              for t in support]
    return hist, coords


def main():
    out = {}
    sup_by_M = {}
    for M in (40, 48, 56, 64):
        support, layer_test, dt = mus(M)
        hist, coords = describe(M, support)
        sup_by_M[M] = coords
        out[str(M)] = {"support_size": len(support), "act_hist": hist,
                       "layer_drop_test": layer_test, "support": coords,
                       "time_s": round(dt, 1)}
        print(f"M={M}: |MUS|={len(support)} act-hist={hist} "
              f"layer-drop={layer_test} ({dt:.0f}s)", flush=True)

    # cross-M stability per layer, in bottom- and top-anchored coordinates
    stab = {}
    for lv in (1, 2, 3, 4):
        bot, top = [], []
        for M, coords in sup_by_M.items():
            sel_ = [c for c in coords if min(c["act"], 4) == lv]
            bot.append({tuple(c["bot"]) for c in sel_})
            top.append({tuple(c["top"]) for c in sel_})
        stab[f"L{lv}"] = {
            "sizes": [len(s) for s in bot],
            "bot_common": sorted(map(list, set.intersection(*bot)))
            if all(bot) else [],
            "top_common": sorted(map(list, set.intersection(*top)))
            if all(top) else [],
        }
        print(f"[stab] L{lv}: sizes={stab[f'L{lv}']['sizes']} "
              f"bot-common={len(stab[f'L{lv}']['bot_common'])} "
              f"top-common={len(stab[f'L{lv}']['top_common'])}", flush=True)
    out["_stability"] = stab
    json.dump(out, open(DATA, "w"), indent=1)
    print(f"-> {DATA}", flush=True)


if __name__ == "__main__":
    main()
