"""e103b_layer_bounds: sharpen the e103 coupling-depth anatomy.

Definitions: for an AP triple with common difference d, act level = nu_2(d)+1
(the tower level at which the triple first couples the two parity cells).

Questions, at M in {40, 48, 56, 64, 72, 80} (all == 0 mod 8):
 P1 (prefix sufficiency): for k = 1..5, is AP[act<=k] + C3 UNSAT?
    Threshold k*(M) = least such k.  Conjecture from e103: k* = 4 when
    nu_2(M) = 3 (M == 8 mod 16), k* = 3 when nu_2(M) >= 4.
 P2 (exact-layer necessity): for each exact act level j <= k*, is
    AP[act<=k*, act != j] + C3 SAT (=> layer j necessary within the prefix)?
 P3 (layer-3 boundedness): biased deletion-minimal MUS of AP[act<=k*] + C3
    that eliminates HIGH act levels first => retained L3 (and L4) counts are
    (near-)minimal.  Growth of min-|L3| with M decides boundedness.
 P4 (anchoring): coordinates of retained L3/L4 triples in bottom/top frames.

Sanity at M == 4 mod 8 (44, 52): every variant SAT (C3 itself SAT).
Output: data/e103b_layers.json
"""
import json
import random
import time

from pysat.solvers import Cadical195

DATA = "/Users/will/Dev/personal/tasks/math/erdos197/data/e103b_layers.json"


def nu2(d):
    v = 0
    while d % 2 == 0:
        d //= 2
        v += 1
    return v


def act(t):
    return nu2(t[1] - t[0]) + 1


def build(M):
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
    cl.append([o(2 * M - 5, M + 5)])
    cl.append([o(2 * M - 3, M + 6)])
    cl.append([o(2 * M - 10, M + 3)])
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


def biased_mus(solver, cand, sel, hard):
    """Deletion-minimal subset of cand (given hard always on), eliminating
    in the given order (cand listed in elimination order)."""
    keep = set(cand)
    base = [sel[t] for t in hard]
    for t in cand:
        if t not in keep:
            continue
        trial = base + [sel[u] for u in keep if u != t]
        if not solver.solve(assumptions=trial):
            keep.discard(t)
    return sorted(keep)


def main():
    out = {}
    for M in (40, 48, 56, 64, 72, 80, 44, 52):
        t0 = time.time()
        solver, triples, sel = build(M)
        entry = {"nu2_M": nu2(M)}
        # P1: prefix sufficiency
        kstar = None
        pref = {}
        for k in range(1, 6):
            A = [sel[t] for t in triples if act(t) <= k]
            st = "UNSAT" if not solver.solve(assumptions=A) else "SAT"
            pref[f"act<={k}"] = st
            if st == "UNSAT" and kstar is None:
                kstar = k
        entry["prefix"] = pref
        entry["k_star"] = kstar
        if kstar is not None:
            # P2: exact-layer necessity inside the k* prefix
            nec = {}
            for j in range(1, kstar + 1):
                A = [sel[t] for t in triples if act(t) <= kstar and act(t) != j]
                nec[f"L{j}"] = ("necessary" if solver.solve(assumptions=A)
                                else "dispensable")
            entry["layer_necessity"] = nec
            # P3: biased MUS -- delete high act levels first
            cand = [t for t in triples if act(t) <= kstar]
            cand.sort(key=lambda t: (-act(t), t))
            rnd = random.Random(0)
            # shuffle within act classes to avoid positional bias
            grp = {}
            for t in cand:
                grp.setdefault(act(t), []).append(t)
            order = []
            for a in sorted(grp, reverse=True):
                g = grp[a][:]
                rnd.shuffle(g)
                order.extend(g)
            mus = biased_mus(solver, order, sel, [])
            hist = {}
            for t in mus:
                hist[f"L{act(t)}"] = hist.get(f"L{act(t)}", 0) + 1
            entry["biased_mus_size"] = len(mus)
            entry["biased_mus_hist"] = hist
            top_layers = [t for t in mus if act(t) >= 3]
            entry["retained_high"] = [
                {"xyz": t, "d": t[1] - t[0], "act": act(t),
                 "bot": [t[0] - M, t[1] - M, t[2] - M],
                 "top": [2 * M - t[0], 2 * M - t[1], 2 * M - t[2]]}
                for t in top_layers]
        solver.delete()
        out[str(M)] = entry
        print(f"M={M} (nu2={entry['nu2_M']}): prefix={pref} k*={kstar} "
              f"nec={entry.get('layer_necessity')} "
              f"mus={entry.get('biased_mus_size')} "
              f"hist={entry.get('biased_mus_hist')} ({time.time()-t0:.0f}s)",
              flush=True)
        if entry.get("retained_high"):
            hi = entry["retained_high"]
            print(f"  retained act>=3 ({len(hi)}): "
                  + "; ".join(f"{h['xyz']} d={h['d']} act={h['act']} "
                              f"bot={h['bot']} top={h['top']}" for h in hi),
                  flush=True)
    json.dump(out, open(DATA, "w"), indent=1)
    print(f"-> {DATA}", flush=True)


if __name__ == "__main__":
    main()
