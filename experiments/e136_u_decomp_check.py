"""e136: machine check of notes/55 SS1 (Lemma U, decomposition).

Part 1  Re-derive the SS1.2 block-pattern table of CORE'(M) by brute
        enumeration of every 3-AP of the core at M = 48, 64, 80:
        - only the ten nondecreasing patterns occur;
        - (0,0,2) is empty; every other pattern is non-empty;
        - straddles (0,1,2) exist.
Part 2  Decomposed encoding of CI(M) per Lemma U -- coloring vars +
        THREE per-team per-block orders (no cross-block order vars) +
        straddle exclusion + the SS1.3 unit families + in-block APs +
        bounds -- cross-validated against the monolithic e135/e120
        encoding:
        - M = 48, bounds (2,2,2): decomposed must be UNSAT (as e135);
        - M = 48, bounds (1,1,1): verdicts of both encodings must
          agree; if SAT, the decomposed witness is re-assembled by
          concatenation and re-verified by the INDEPENDENT e120
          checker (this exercises the (<=) direction of Lemma U on a
          real model), and its coloring anatomy is dumped for SS6.

Run: .venv/bin/python experiments/e136_u_decomp_check.py
Log: data/e136_u.log (tee'd by the caller)
"""
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from e120_density_cores import solve_coupled3, check_coupled3_team

from pysat.solvers import Cadical195
from pysat.card import CardEnc, EncType


def core(M):
    P0 = list(range(M + 1, 2 * M + 1))
    P1 = list(range(3 * M - 15, 4 * M + 1))
    P2 = list(range(4 * M + 1, 6 * M + 16))
    return P0, P1, P2


def blk(M, v):
    if v <= 2 * M:
        return 0
    if v <= 4 * M:
        return 1
    return 2


# ----------------------------------------------------------------------
# Part 1: the pattern table
# ----------------------------------------------------------------------

def part1(M):
    P0, P1, P2 = core(M)
    V = sorted(P0 + P1 + P2)
    Vs = set(V)
    from collections import Counter
    pat = Counter()
    for b in V:
        for d in range(1, (V[-1] - V[0]) // 2 + 1):
            a, c = b - d, b + d
            if a in Vs and c in Vs:
                pat[(blk(M, a), blk(M, b), blk(M, c))] += 1
    ten = {(0, 0, 0), (1, 1, 1), (2, 2, 2), (0, 0, 1), (0, 0, 2),
           (0, 1, 1), (0, 1, 2), (0, 2, 2), (1, 1, 2), (1, 2, 2)}
    assert set(pat) <= ten, (M, set(pat) - ten)
    assert pat[(0, 0, 2)] == 0, (M, pat[(0, 0, 2)])
    for p in sorted(ten - {(0, 0, 2)}):
        assert pat[p] > 0, (M, p, 'unexpectedly empty')
    # nondecreasing block patterns only (sanity of the enumeration)
    for p in pat:
        assert p[0] <= p[1] <= p[2], (M, p)
    print(f'  part1 M={M}: pattern counts '
          + ' '.join(f'{p}:{pat[p]}' for p in sorted(pat)), flush=True)
    return dict((str(k), v) for k, v in pat.items())


# ----------------------------------------------------------------------
# Part 2: decomposed encoding
# ----------------------------------------------------------------------

def solve_decomposed(M, bounds, budget=None):
    """Lemma-U decomposed encoding of CI(M) on CORE'(M).
    Returns (verdict, secs, info); SAT info: colors + 6 block orders."""
    P0, P1, P2 = core(M)
    blocks = (P0, P1, P2)
    V = sorted(P0 + P1 + P2)
    Vs = set(V)
    top = 0
    # per team (0 = A, 1 = B), per block, order vars on in-block pairs
    off = {}
    for t in range(2):
        for bi, B in enumerate(blocks):
            for i in range(len(B)):
                for j in range(i + 1, len(B)):
                    top += 1
                    off[(t, bi, B[i], B[j])] = top
    ai = {}
    for v in V:
        top += 1
        ai[v] = top                                   # true = team A

    def lit(t, bi, u, w):
        if u < w:
            return off[(t, bi, u, w)]
        return -off[(t, bi, w, u)]

    guards = (lambda v: -ai[v], lambda v: ai[v])      # g[t](v): v NOT in t
    cls = []
    # straddle exclusion (both teams): u in P0, y in P1, z = 2y-u in P2
    n_straddle = 0
    for y in P1:
        for u in P0:
            z = 2 * y - u
            if 4 * M + 1 <= z <= 6 * M + 15:
                cls.append([-ai[u], -ai[y], -ai[z]])
                cls.append([ai[u], ai[y], ai[z]])
                n_straddle += 1
    # per team: in-block APs + units
    n_units = 0
    for t in range(2):
        g = guards[t]
        for bi, B in enumerate(blocks):
            Bs = set(B)
            for b in B:
                for d in range(1, min(b - B[0], B[-1] - b) + 1):
                    a, c = b - d, b + d
                    if a in Bs and c in Bs:
                        gg = [g(a), g(b), g(c)]
                        cls.append(gg + [-lit(t, bi, a, b),
                                         -lit(t, bi, b, c)])
                        cls.append(gg + [lit(t, bi, a, b),
                                         lit(t, bi, b, c)])
        # units, by pattern
        for b in V:
            for d in range(1, (V[-1] - V[0]) // 2 + 1):
                a, c = b - d, b + d
                if a in Vs and c in Vs:
                    p = (blk(M, a), blk(M, b), blk(M, c))
                    if p in ((0, 0, 1), (1, 1, 2)):
                        # unit b < a inside blk(a)
                        cls.append([g(a), g(b), g(c),
                                    lit(t, p[0], b, a)])
                        n_units += 1
                    elif p in ((0, 1, 1), (0, 2, 2), (1, 2, 2)):
                        # unit c < b inside blk(b)
                        cls.append([g(a), g(b), g(c),
                                    lit(t, p[1], c, b)])
                        n_units += 1
    # per-team per-block transitivity
    for t in range(2):
        for bi, B in enumerate(blocks):
            n = len(B)
            for i in range(n):
                for j in range(i + 1, n):
                    xij = off[(t, bi, B[i], B[j])]
                    for k in range(j + 1, n):
                        xjk = off[(t, bi, B[j], B[k])]
                        xik = off[(t, bi, B[i], B[k])]
                        cls.append([-xij, -xjk, xik])
                        cls.append([xij, xjk, -xik])
    # bounds
    cards = []
    tid = top
    for bi, B in enumerate(blocks):
        for sign in (1, -1):
            enc = CardEnc.atleast(lits=[sign * ai[v] for v in B],
                                  bound=bounds[bi], top_id=tid,
                                  encoding=EncType.seqcounter)
            tid = enc.nv if enc.nv > tid else tid
            cards += enc.clauses
    t0 = time.time()
    with Cadical195(bootstrap_with=cls) as s:
        for c in cards:
            s.add_clause(c)
        ok = s.solve()
        el = round(time.time() - t0, 1)
        if not ok:
            return 'UNSAT', el, {'straddle_clauses': n_straddle,
                                 'unit_clauses': n_units}
        model = set(l for l in s.get_model() if l > 0)
    posneg = lambda l: (l in model) if l > 0 else (abs(l) not in model)
    colA = [v for v in V if ai[v] in model]
    colB = [v for v in V if ai[v] not in model]
    info = {'A': colA, 'B': colB}
    for t, col in ((0, colA), (1, colB)):
        full = []
        for bi, B in enumerate(blocks):
            mem = [v for v in B if v in set(col)]
            wins = {v: 0 for v in mem}
            for i, u in enumerate(mem):
                for w in mem[i + 1:]:
                    if posneg(lit(t, bi, u, w)):
                        wins[u] += 1
                    else:
                        wins[w] += 1
            full += sorted(mem, key=lambda v: -wins[v])
        info[f'order{"AB"[t]}'] = full
    return 'SAT', el, info


def part2(M=48):
    print(f'  part2: decomposed vs monolithic at M={M}', flush=True)
    P0, P1, P2 = core(M)
    supp = sorted(P0 + P1 + P2)
    # (a) bounds (2,2,2): decomposed must be UNSAT like e135
    v, el, info = solve_decomposed(M, (2, 2, 2))
    print(f'    decomposed (2,2,2): {v} [{el}s] '
          f'straddle={info.get("straddle_clauses")} '
          f'units={info.get("unit_clauses")}', flush=True)
    assert v == 'UNSAT', 'decomposition must reproduce the e135 lock'
    # (b) bounds (1,1,1): verdict equality + witness cross-check
    v1, el1, info1 = solve_decomposed(M, (1, 1, 1))
    print(f'    decomposed (1,1,1): {v1} [{el1}s]', flush=True)
    v2, el2, info2 = solve_coupled3(M, None, None, budget=43200.0,
                                    seams='both', abs_bounds=(1, 1, 1),
                                    support=supp)
    print(f'    monolithic (1,1,1): {v2} [{el2}s]', flush=True)
    assert (v1 == 'SAT') == (v2 == 'SAT'), (v1, v2)
    if v1 == 'SAT':
        bounds = {'B0': 1, 'B1': 1, 'B2': 1}
        for team in 'AB':
            col = info1[team]
            order = info1[f'order{team}']
            err = check_coupled3_team(order, col, M, bounds, seams='both')
            assert err is None, (team, err)
        print('    decomposed witness re-verified by the e120 checker '
              '(both teams) — Lemma U (<=) exercised', flush=True)
        # anatomy dump for SS6
        for team in 'AB':
            col = info1[team]
            sizes = [len([x for x in col if x <= 2 * M]),
                     len([x for x in col if 2 * M < x <= 4 * M]),
                     len([x for x in col if x > 4 * M])]
            print(f'    (1,1,1) witness team {team}: sizes {sizes}',
                  flush=True)
        small = min(('A', 'B'), key=lambda t: len(info1[t]))
        print(f'    minority team {small}: {sorted(info1[small])}',
              flush=True)
        big = 'B' if small == 'A' else 'A'
        print(f'    majority order (first 40): '
              f'{info1[f"order{big}"][:40]}', flush=True)


def main():
    for M in (48, 64, 80):
        part1(M)
    part2(48)
    print('e136: ALL CHECKS PASSED', flush=True)


if __name__ == '__main__':
    main()
