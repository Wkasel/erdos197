"""e124e_closure_halves: FRONT N2-OFF step 3c -- are the two half-flips
of the {11,12} dyadic core pure rule-closure (no case splits)?

Closure engine (independent of e113b, same rule set): facts = ordered
pairs (u, v) meaning u placed before v; for every in-block AP (x, y, z)
apply R1 (x,y)->(z,y), R3 (z,y)->(x,y), R4 (y,x)->(y,z), R2 (y,z)->(y,x);
plus transitivity; iterate to fixpoint or contradiction.

HALF-A: {t0<b6, t2<b5} + (t1 < m0)  -- expect CONTRADICTION at 0 mod 8
HALF-B: {t1<b5, t3<b4} + (m0 < t1)  -- expect CONTRADICTION at 0 mod 8
Controls at 4 mod 8: closure must NOT refute (solver says SAT there).

Run: .venv/bin/python experiments/e124e_closure_halves.py [M ...]
"""
import sys


def closure(M, seeds):
    """Returns ('contradiction', (u,v)) or ('fixpoint', facts)."""
    lo, hi = M + 1, 2 * M
    aps = []
    for y in range(lo + 1, hi):
        d = 1
        while y + d <= hi and y - d >= lo:
            aps.append((y - d, y, y + d))
            d += 1
    facts = set(seeds)
    # index rules by premise
    from collections import defaultdict
    rule = defaultdict(list)     # premise pair -> conclusion pair
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

    def add(u, v):
        if (u, v) in facts:
            return None
        if (v, u) in facts:
            return (u, v)
        facts.add((u, v))
        succ[u].add(v)
        pred[v].add(u)
        frontier.append((u, v))
        return None

    while frontier:
        (u, v) = frontier.pop()
        for conc in rule[(u, v)]:
            bad = add(*conc)
            if bad:
                return ("contradiction", bad)
        # transitivity: pred(u) x {v}, {u} x succ(v)
        for w in list(pred[u]):
            bad = add(w, v)
            if bad:
                return ("contradiction", bad)
        for w in list(succ[v]):
            bad = add(u, w)
            if bad:
                return ("contradiction", bad)
    return ("fixpoint", facts)


def main():
    Ms = [int(a) for a in sys.argv[1:]] or [24, 32, 40, 48, 56, 64,
                                            28, 36, 44, 52]
    for M in Ms:
        m0 = 3 * M // 2
        t0, t1, t2, t3 = 2 * M, 2 * M - 1, 2 * M - 2, 2 * M - 3
        b4, b5, b6 = M + 4, M + 5, M + 6
        A = closure(M, {(t0, b6), (t2, b5), (t1, m0)})
        B = closure(M, {(t1, b5), (t3, b4), (m0, t1)})
        # also probe the t3-phase versions
        A3 = closure(M, {(t0, b6), (t2, b5), (t3, m0)})
        B3 = closure(M, {(t1, b5), (t3, b4), (m0, t3)})
        def s(r):
            return ("CONTRA " + str(r[1])) if r[0] == "contradiction" \
                else f"fixpoint({len(r[1])} facts)"
        print(f"M={M} ({M % 8} mod 8): A={s(A)}  B={s(B)}  "
              f"A3={s(A3)}  B3={s(B3)}", flush=True)


if __name__ == "__main__":
    main()
