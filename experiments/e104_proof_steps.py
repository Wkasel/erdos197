"""e104_proof_steps: TASK P support -- anatomy of the individual proof steps
of the graded forcing law S1 (notes/32), as candidates for hand derivation.

The hand-proof program (notes/33) needs, for each layer of S1, the forcing
step *conditioned on the previous layers as axioms*:

  L0a: AP + A2 + A3           |- t3 < b3      (every even M)
  L0b: AP + A2 + A3           |- t10 < b6     (every even M)
  L1a: AP + A2 + A3 + L0      |- t3 < t5      (M == 0 mod 4)
  L1b: AP + A2 + A3 + L0      |- b5 < b3      (M == 0 mod 4)
  L2 : AP + A2 + A3 + L0 + L1 |- b5 < t5      (M == 0 mod 8)  [= NOT-A1]

For each step at each scale: assert the negation of the conclusion, extract
a deletion-minimal AP-triple MUS (eager transitivity, per-triple selectors,
core-shrink + greedy deletion), and record:
  - MUS size (bounded across M <=> hand case-tree plausible),
  - act-level histogram (nu2(d)+1),
  - bottom-anchored (v-M) and top-anchored (2M-v) triple coordinates,
  - cross-scale coordinate intersections per step.

Part 2: halving bookkeeping check (hand lemma H of notes/33): at even M the
maps h+(v)=(v+1)/2 on odds and hE(v)=v/2 on evens are AP-preserving
bijections onto (m,2m], m=M/2, and REFLECT APs (image AP => preimage AP).

Part 3: base ledger. Direct AP+C3 status at every M == 0 mod 8 in 16..256
(UNSAT expected) and M == 4 mod 8 in 20..100 (SAT expected), lazy encoding.

Usage: .venv/bin/python experiments/e104_proof_steps.py [1|2|3|all]
Output: data/e104_proof_steps.json
"""
import json
import random
import sys
import time

sys.path.insert(0, "/Users/will/Dev/personal/tasks/math/erdos197/experiments")
from e101_invariant import Interval  # lazy-transitivity machinery

DATA = "/Users/will/Dev/personal/tasks/math/erdos197/data/e104_proof_steps.json"

from pysat.solvers import Cadical195


def nu2(d):
    v = 0
    while d % 2 == 0:
        d //= 2
        v += 1
    return v


def build(M, hard_units):
    """Eager order encoding; hard_units = list of (u,w) meaning u before w.
    Returns (solver, triples, sel, o)."""
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
    for (u, w) in hard_units:
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
    return Cadical195(bootstrap_with=cl), triples, sel, o


def step_mus(M, hard_units, seed=0):
    """Deletion-minimal AP-triple MUS of AP + hard_units (expected UNSAT)."""
    solver, triples, sel, _ = build(M, hard_units)
    assum = {sel[t]: t for t in triples}
    active = list(assum)
    st = solver.solve(assumptions=active)
    if st:
        solver.delete()
        return None  # not UNSAT: the step does not hold at this M
    while True:
        core = [l for l in (solver.get_core() or []) if l in assum]
        if len(core) >= len(active):
            break
        active = core
        st = solver.solve(assumptions=active)
        assert not st
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
    solver.delete()
    return sorted(assum[s] for s in keep)


def units_for(step, M):
    t3, t5, t10 = 2 * M - 3, 2 * M - 5, 2 * M - 10
    b3, b5, b6 = M + 3, M + 5, M + 6
    A2, A3 = (t3, b6), (t10, b3)
    L0 = [(t3, b3), (t10, b6)]
    L1 = [(t3, t5), (b5, b3)]
    if step == "L0a":
        return [A2, A3, (b3, t3)]
    if step == "L0b":
        return [A2, A3, (b6, t10)]
    if step == "L1a":
        return [A2, A3] + L0 + [(t5, t3)]
    if step == "L1b":
        return [A2, A3] + L0 + [(b3, b5)]
    if step == "L2":
        return [A2, A3] + L0 + L1 + [(t5, b5)]
    raise ValueError(step)


STEP_SCALES = {
    "L0a": [40, 42, 44, 46, 48, 50, 52, 56, 58, 60, 64, 72, 80, 96],
    "L0b": [40, 42, 44, 46, 48, 50, 52, 56, 58, 60, 64, 72, 80, 96],
    "L1a": [40, 44, 48, 52, 56, 60, 64, 72, 80, 96],
    "L1b": [40, 44, 48, 52, 56, 60, 64, 72, 80, 96],
    "L2": [40, 48, 56, 64, 72, 80, 96],
}


def part1():
    out = {}
    for step, Ms in STEP_SCALES.items():
        out[step] = {}
        bots, tops = [], []
        for M in Ms:
            t0 = time.time()
            sup = step_mus(M, units_for(step, M))
            if sup is None:
                out[step][str(M)] = "STEP-FAILS(SAT)"
                print(f"[1] {step} M={M}: SAT -- step does not hold!",
                      flush=True)
                continue
            hist = {}
            for t in sup:
                lv = min(nu2(t[1] - t[0]) + 1, 4)
                hist[f"L{lv}"] = hist.get(f"L{lv}", 0) + 1
            bot = sorted(tuple(v - M for v in t) for t in sup)
            top = sorted(tuple(2 * M - v for v in t) for t in sup)
            bots.append(set(bot))
            tops.append(set(top))
            out[step][str(M)] = {"size": len(sup), "act_hist": hist,
                                 "bot": [list(t) for t in bot],
                                 "top": [list(t) for t in top]}
            print(f"[1] {step} M={M}: |MUS|={len(sup)} hist={hist} "
                  f"({time.time()-t0:.1f}s)", flush=True)
        if bots:
            bc = set.intersection(*bots)
            tc = set.intersection(*tops)
            out[step]["_common"] = {
                "sizes": [len(b) for b in bots],
                "bot_common": sorted(map(list, bc)),
                "top_common": sorted(map(list, tc))}
            print(f"[1] {step}: sizes={[len(b) for b in bots]} "
                  f"bot-common={len(bc)} top-common={len(tc)}", flush=True)
    return out


def part2(Ms=(40, 44, 46, 48, 56, 64)):
    """Halving bookkeeping: h+ on odds / hE on evens are AP-preserving AND
    AP-reflecting bijections onto (m,2m]."""
    out = {}
    for M in Ms:
        assert M % 2 == 0
        m = M // 2
        odds = [v for v in range(M + 1, 2 * M + 1) if v % 2 == 1]
        evens = [v for v in range(M + 1, 2 * M + 1) if v % 2 == 0]
        img_o = sorted((v + 1) // 2 for v in odds)
        img_e = sorted(v // 2 for v in evens)
        tgt = list(range(m + 1, 2 * m + 1))
        ok = (img_o == tgt) and (img_e == tgt)
        # AP triples map both ways
        def aps(vals):
            s = set(vals)
            return {(x, y, z) for y in vals for d in range(1, M)
                    for x, z in [(y - d, y + d)] if x in s and z in s}
        def h(v, odd):
            return (v + 1) // 2 if odd else v // 2
        for odd, vals in ((True, odds), (False, evens)):
            src = aps(vals)
            im = {tuple(h(v, odd) for v in t) for t in src}
            tgt_aps = aps(tgt)
            ok = ok and (im == tgt_aps)
        out[str(M)] = "OK" if ok else "FAIL"
        print(f"[2] M={M}: halving bookkeeping {'OK' if ok else 'FAIL'}",
              flush=True)
    return out


def part3():
    out = {}
    for M in list(range(16, 257, 8)):
        t0 = time.time()
        iv = Interval(M)
        t3, t5, t10 = 2 * M - 3, 2 * M - 5, 2 * M - 10
        b3, b5, b6 = M + 3, M + 5, M + 6
        st = iv.status([iv.o(t5, b5), iv.o(t3, b6), iv.o(t10, b3)])
        out[str(M)] = st
        print(f"[3] C3 at M={M} (mod8={M % 8}): {st} "
              f"({time.time()-t0:.1f}s)", flush=True)
    for M in list(range(20, 101, 8)):
        iv = Interval(M)
        t3, t5, t10 = 2 * M - 3, 2 * M - 5, 2 * M - 10
        b3, b5, b6 = M + 3, M + 5, M + 6
        st = iv.status([iv.o(t5, b5), iv.o(t3, b6), iv.o(t10, b3)])
        out[str(M)] = st
        print(f"[3] C3 at M={M} (mod8={M % 8}): {st}", flush=True)
    return out


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    res = {}
    t0 = time.time()
    if mode in ("1", "all"):
        res["steps"] = part1()
    if mode in ("2", "all"):
        res["halving"] = part2()
    if mode in ("3", "all"):
        res["bases"] = part3()
    try:
        old = json.load(open(DATA))
    except Exception:
        old = {}
    old.update(res)
    json.dump(old, open(DATA, "w"), indent=1)
    print(f"Done ({time.time()-t0:.0f}s) -> {DATA}", flush=True)


if __name__ == "__main__":
    main()
