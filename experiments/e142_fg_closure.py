"""e142: is the double-fan refutation a PLAIN CLOSURE?  (GAP-FG)

Closure engine: facts (u, v) = "u placed before v" on the window
I = [4M+1, 6M+15]; seed with the two fans' units; close under
R1-R4 (midpoint-extremality on every AP of I) and transitivity;
UNSAT iff some 2-cycle (u, v) + (v, u) appears.  Every fact carries
provenance; on refutation the minimal derivation DAG of the cycle
is printed (pencil-checkable, e109-style).

If plain closure refutes — GAP-FG needs NO case splits and the hand
schema is a direct derivation.  Survey: pair shapes at M = 48
(adjacent top, same-parity top, band-bottom, spread) and scale
checks at M = 64, 80.

Run: .venv/bin/python experiments/e142_fg_closure.py
Log: data/e142_fg_closure.log
"""
import sys
from collections import deque


def close(M, X, verbose=True):
    lo, hi = 4 * M + 1, 6 * M + 15
    V = range(lo, hi + 1)
    # AP list
    aps = []
    for b in V:
        for d in range(1, min(b - lo, hi - b) + 1):
            aps.append((b - d, b, b + d))
    fact = {}                    # (u,v) -> provenance
    q = deque()

    def add(u, v, why):
        if (u, v) in fact:
            return None
        fact[(u, v)] = why
        q.append((u, v))
        if (v, u) in fact:
            return (u, v)
        return None

    # seeds
    for x in X:
        for y in V:
            z = 2 * y - x
            if z != y and lo <= z <= hi:
                c = add(z, y, ('unit', x, y))
                if c:
                    return c, fact
    # index APs by participating pair for rule triggering
    by_pair = {}
    for (a, b, c) in aps:
        for pr in ((a, b), (b, a), (b, c), (c, b)):
            by_pair.setdefault(pr, []).append((a, b, c))
    # succ/pred for transitivity
    succ = {}
    pred = {}
    for (u, v) in list(fact):
        succ.setdefault(u, set()).add(v)
        pred.setdefault(v, set()).add(u)

    while q:
        (u, v) = q.popleft()
        succ.setdefault(u, set()).add(v)
        pred.setdefault(v, set()).add(u)
        # transitivity: w -> u -> v  and  u -> v -> w2
        for w in list(pred.get(u, ())):
            c = add(w, v, ('trans', w, u, v))
            if c:
                return c, fact
        for w2 in list(succ.get(v, ())):
            c = add(u, w2, ('trans', u, v, w2))
            if c:
                return c, fact
        # R-rules on APs containing the pair (u, v)
        for (a, b, c3) in by_pair.get((u, v), ()):
            # patterns: premise (u,v) matches one of the four rules
            conc = None
            if (u, v) == (a, b):
                conc, rule = (c3, b), 'R1'
            elif (u, v) == (c3, b):
                conc, rule = (a, b), 'R3'
            elif (u, v) == (b, c3):
                conc, rule = (b, a), 'R2'
            elif (u, v) == (b, a):
                conc, rule = (b, c3), 'R4'
            if conc:
                cyc = add(conc[0], conc[1], (rule, (a, b, c3), (u, v)))
                if cyc:
                    return cyc, fact
    return None, fact


def provenance(fact, root_pair, M):
    """Print the derivation DAG of the 2-cycle, deduplicated."""
    seen = set()
    lines = []

    def off(v):
        return v - 4 * M

    def show(pair, depth):
        if pair in seen or depth > 40:
            return
        seen.add(pair)
        why = fact[pair]
        u, v = pair
        if why[0] == 'unit':
            lines.append(f'{"  "*depth}[{off(u)} < {off(v)}] unit: '
                         f'attacker {why[1]} at midpoint {off(why[2])}')
        elif why[0] == 'trans':
            _, a, b, c = why
            lines.append(f'{"  "*depth}[{off(u)} < {off(v)}] trans via '
                         f'{off(b)}')
            show((a, b), depth + 1)
            show((b, c), depth + 1)
        else:
            rule, ap, prem = why
            lines.append(f'{"  "*depth}[{off(u)} < {off(v)}] {rule} on AP '
                         f'({off(ap[0])},{off(ap[1])},{off(ap[2])})')
            show(prem, depth + 1)

    u, v = root_pair
    lines.append(f'2-CYCLE on ({off(u)}, {off(v)}) — offsets from 4M:')
    show((u, v), 1)
    show((v, u), 1)
    return lines, len(seen)


def main():
    M = 48
    for X in ((4 * M, 4 * M - 1), (4 * M, 4 * M - 2),
              (4 * M - 1, 4 * M - 3), (3 * M - 15, 3 * M - 14),
              (3 * M - 15, 4 * M), (140, 170), (129, 160)):
        cyc, fact = close(M, X)
        n = len(fact)
        if cyc:
            print(f'M={M} X={X}: CLOSURE REFUTES (facts={n})', flush=True)
        else:
            print(f'M={M} X={X}: closure stalls at {n} facts '
                  f'(needs case split)', flush=True)
    # scale checks, adjacent top pair
    for M in (64, 80):
        X = (4 * M, 4 * M - 1)
        cyc, fact = close(M, X)
        print(f'M={M} X={X}: '
              + ('CLOSURE REFUTES' if cyc else 'stalls')
              + f' (facts={len(fact)})', flush=True)
    # provenance of the smallest instance
    M = 48
    cyc, fact = close(M, (4 * M, 4 * M - 1))
    if cyc:
        lines, nfacts = provenance(fact, cyc, M)
        print(f'\n--- derivation ({nfacts} distinct facts) '
              f'M=48 X=(192,191) ---', flush=True)
        for ln in lines[:120]:
            print(ln, flush=True)
        if len(lines) > 120:
            print(f'... ({len(lines) - 120} more lines)', flush=True)
    print('e142: DONE', flush=True)


if __name__ == '__main__':
    main()
