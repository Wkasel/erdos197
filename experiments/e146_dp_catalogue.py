"""e146: the seed death-pattern catalogue for COV(M)  (notes/56 SS1).

A death pattern (notes/56 SS0.2) is a set S subseteq CORE'(M) whose
S-restricted block-i theory Th_i[S] is UNSAT; Lemma DP makes every
such S a forbidden monochromatic set for feasible-state colorings.

Part 1 (FG patterns, block 2): for every attacker pair
  X = (4M-p, 4M-q), 0 <= q < p <= M+15, run the e142 plain R1-R4 +
  transitivity closure of the double fan on the P2 window
  [4M+1, 6M+15].  If it refutes, extract the derivation-DAG value
  support, then deletion-minimize it against the independent
  S-restricted SAT theory (order vars on S cap P2; AP clauses inside
  S cap P2; fan units of the in-S attackers with y, z in S).  Every
  emitted pattern is SAT-validated UNSAT after minimization.

Part 2 (J patterns, block 1): S = R cup {4M+j : j in F} for each of
  the 36 minimal forbidden sets F of Lemma J (data/e138_transfer.json
  partB), SAT-validated against the S-restricted block-1 theory
  (AP clauses inside R; beta-units with completion in S).

Output: data/e146_catalogue_M{M}.json — list of
  {'blk': i, 'S': [...], 'src': ...} + stats.
Run: .venv/bin/python experiments/e146_dp_catalogue.py [M ...]
Log: data/e146_catalogue.log
"""
import json
import os
import sys
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from e142_fg_closure import close

from pysat.solvers import Cadical195


# ----------------------------------------------------------------------
# S-restricted theory solvers (the notes/56 SS0.2 definition)
# ----------------------------------------------------------------------

def _order_theory_unsat(points, ap_triples, units):
    """Order theory on `points`: transitivity + midpoint constraints on
    ap_triples (each (a,b,c) with all in points) + units (u before v).
    Returns True iff UNSAT."""
    idx = {v: i for i, v in enumerate(points)}
    n = len(points)
    off = {}
    top = 0
    for i in range(n):
        for j in range(i + 1, n):
            top += 1
            off[(i, j)] = top

    def lit(u, w):
        i, j = idx[u], idx[w]
        return off[(i, j)] if i < j else -off[(j, i)]

    cls = []
    for (a, b, c) in ap_triples:
        cls.append([-lit(a, b), -lit(b, c)])
        cls.append([lit(a, b), lit(b, c)])
    for (u, w) in units:
        cls.append([lit(u, w)])
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                x, y, z = off[(i, j)], off[(j, k)], off[(i, k)]
                cls.append([-x, -y, z])
                cls.append([x, y, -z])
    with Cadical195(bootstrap_with=cls) as s:
        return not s.solve()


def th2_restricted_unsat(M, S):
    """Th_2[S]: block-2 theory of the pattern S (fan/A5 units from
    attackers in S cap (P0 u P1), APs inside S cap P2)."""
    lo, hi = 4 * M + 1, 6 * M + 15
    S = set(S)
    Z = sorted(v for v in S if lo <= v <= hi)
    Zs = set(Z)
    att = [v for v in S if v < lo]
    aps = []
    for b in Z:
        for d in range(1, min(b - lo, hi - b) + 1):
            if b - d in Zs and b + d in Zs:
                aps.append((b - d, b, b + d))
    units = []
    for x in att:
        for y in Z:
            z = 2 * y - x
            if z != y and z in Zs:
                units.append((z, y))          # z before y
    return _order_theory_unsat(Z, aps, units)


def th1_restricted_unsat(M, S):
    """Th_1[S]: block-1 theory of the pattern S (alpha units from
    P0-attackers in S, beta units from completions in S cap P2, APs
    inside S cap P1)."""
    lo, hi = 3 * M - 15, 4 * M
    S = set(S)
    Y = sorted(v for v in S if lo <= v <= hi)
    Ys = set(Y)
    aps = []
    for b in Y:
        for d in range(1, min(b - lo, hi - b) + 1):
            if b - d in Ys and b + d in Ys:
                aps.append((b - d, b, b + d))
    units = []
    for x in S:
        if x <= 2 * M:                        # alpha: (0,1,1)
            for y in Y:
                z = 2 * y - x
                if z != y and z in Ys:
                    units.append((z, y))
    for a in Y:                               # beta: (1,1,2)
        for b in Y:
            if b <= a:
                continue
            c = 2 * b - a
            if 4 * M + 1 <= c <= 6 * M + 15 and c in S:
                units.append((b, a))
    return _order_theory_unsat(Y, aps, units)


# ----------------------------------------------------------------------
# Part 1: FG patterns
# ----------------------------------------------------------------------

def dag_support(cyc, fact):
    """All values appearing in the derivation DAG of the 2-cycle."""
    seen = set()
    vals = set()
    stack = [cyc, (cyc[1], cyc[0])]
    while stack:
        pair = stack.pop()
        if pair in seen:
            continue
        seen.add(pair)
        u, v = pair
        vals.update((u, v))
        why = fact[pair]
        if why[0] == 'unit':
            vals.add(why[1])                  # the attacker
            vals.add(why[2])                  # the midpoint
        elif why[0] == 'trans':
            _, a, b, c = why
            vals.add(b)
            stack.append((a, b))
            stack.append((b, c))
        else:                                 # R-rule
            rule, ap, prem = why
            vals.update(ap)
            stack.append(prem)
    return vals


def minimize_pattern(M, S, unsat_fn):
    """Greedy deletion minimization of pattern S against unsat_fn."""
    S = sorted(S)
    for v in sorted(S, reverse=True):
        if len(S) <= 3:
            break
        trial = [w for w in S if w != v]
        if unsat_fn(M, trial):
            S = trial
    return S


def part1(M, minimize=True):
    t0 = time.time()
    patterns = {}
    n_dead = n_alive = 0
    for p in range(1, M + 16):
        for q in range(0, p):
            X = (4 * M - p, 4 * M - q)
            cyc, fact = close(M, X, verbose=False)
            if not cyc:
                n_alive += 1
                continue
            n_dead += 1
            S = dag_support(cyc, fact)
            assert th2_restricted_unsat(M, S), (M, (q, p), 'support fails')
            if minimize:
                S = minimize_pattern(M, S, th2_restricted_unsat)
            key = tuple(sorted(S))
            if key not in patterns:
                patterns[key] = f'fg({q},{p})'
    el = time.time() - t0
    sizes = Counter(len(k) for k in patterns)
    print(f'  part1 M={M}: {n_dead} closure-dead pairs, {n_alive} alive; '
          f'{len(patterns)} distinct minimized patterns '
          f'[{el:.0f}s]', flush=True)
    print(f'    size histogram: {dict(sorted(sizes.items()))}', flush=True)
    return [{'blk': 2, 'S': list(k), 'src': v} for k, v in patterns.items()]


# ----------------------------------------------------------------------
# Part 2: J patterns
# ----------------------------------------------------------------------

def part2(M):
    with open(os.path.join(HERE, '..', 'data', 'e138_transfer.json')) as f:
        d = json.load(f)
    out = []
    R = list(range(4 * M - 15, 4 * M + 1))
    for F in d['partB']['minimal_forbidden']:
        S = sorted(R + [4 * M + j for j in F])
        assert th1_restricted_unsat(M, S), (M, F, 'J pattern fails')
        out.append({'blk': 1, 'S': S, 'src': f'J({F})'})
    print(f'  part2 M={M}: {len(out)} J patterns validated', flush=True)
    return out


def main():
    scales = [int(a) for a in sys.argv[1:]] or [48]
    for M in scales:
        cat = part1(M) + part2(M)
        path = os.path.join(HERE, '..', 'data', f'e146_catalogue_M{M}.json')
        with open(path, 'w') as f:
            json.dump(cat, f)
        print(f'M={M}: catalogue size {len(cat)} -> {path}', flush=True)
    print('e146: DONE', flush=True)


if __name__ == '__main__':
    main()
