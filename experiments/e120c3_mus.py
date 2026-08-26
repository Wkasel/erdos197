"""e120c3_mus: deletion-minimal SUPPORT of the two-seam coupled core.

Greedy chunked deletion (descending values, chunk bisection) on the
C3 gadget with ABSOLUTE bounds: find a minimal set of window values
whose presence keeps 'no coloring with each team >= bounds per block
escapes' UNSAT.  Deleted values belong to neither team (free), so the
surviving support is the combinatorial heart of the core — the input
for a hand schema (e88/e90 discipline at the coupled level).

Vacuity guard: a deletion step is REFUSED if it would leave any block
with < 2*bound + 2 surviving values (cardinality-driven UNSAT would be
vacuous); final core re-verified under Glucose42 as well.

Usage: e120c3_mus.py M b0 b1 b2 [chunk0]
Artifacts: appended to data/e120_results.jsonl; data/e120_C3_mus_M{M}.json
"""
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
DATA = os.path.join(os.path.dirname(HERE), 'data')

import e120_density_cores as e
from e120_density_cores import stream


def run(M, bounds, chunk0=16):
    t00 = time.time()
    V = list(range(M + 1, 8 * M + 1))
    blocks = {'B0': (M, 2 * M), 'B1': (2 * M, 4 * M), 'B2': (4 * M, 8 * M)}
    bnd = dict(zip(('B0', 'B1', 'B2'), bounds))

    def blocksizes(sup):
        return {k: sum(1 for v in sup if lo < v <= hi)
                for k, (lo, hi) in blocks.items()}

    def feasible(sup):
        bs = blocksizes(sup)
        return all(bs[k] >= 2 * bnd[k] + 2 for k in bs)

    def unsat(sup):
        v, el, _ = e.solve_coupled3(M, 0, 1, abs_bounds=bounds,
                                    support=sup)
        return v == 'UNSAT', el

    ok, el = unsat(V)
    print(f'start M={M} bounds={bounds} n={len(V)}: '
          f'{"UNSAT" if ok else "SAT"} [{el}s]', flush=True)
    assert ok, 'core does not fire on the full window'
    sup = list(V)
    total_solves = 1
    # chunked greedy deletion, descending values
    chunk = chunk0
    while chunk >= 1:
        i = 0
        cand = sorted(sup, reverse=True)
        while i < len(cand):
            batch = cand[i:i + chunk]
            trial = [v for v in sup if v not in set(batch)]
            if not feasible(trial):
                i += chunk
                continue
            ok, el = unsat(trial)
            total_solves += 1
            if ok:
                sup = trial
                cand = [c for c in cand if c not in set(batch)]
                print(f'  drop {len(batch)} vals (chunk={chunk}) -> '
                      f'n={len(sup)} [{el}s]', flush=True)
            else:
                i += chunk
        chunk //= 2
    bs = blocksizes(sup)
    print(f'MINIMAL SUPPORT n={len(sup)} blocks={bs} '
          f'({total_solves} solves, {round(time.time() - t00, 1)}s)',
          flush=True)
    print('support =', sorted(sup), flush=True)
    # re-verify with Glucose42
    from pysat.solvers import Glucose42
    orig = e.Cadical195
    e.Cadical195 = Glucose42
    ok2, el2 = unsat(sup)
    e.Cadical195 = orig
    print(f'Glucose42 re-verify: {"UNSAT" if ok2 else "SAT!"} [{el2}s]',
          flush=True)
    # per-value criticality of the final support (each singleton restore
    # of SAT confirms deletion-minimality)
    crit = []
    for v in sorted(sup):
        trial = [u for u in sup if u != v]
        if not feasible(trial):
            crit.append((v, 'CARD'))
            continue
        ok3, _ = unsat(trial)
        total_solves += 1
        crit.append((v, 'NEC' if not ok3 else 'RED'))
    redundant = [v for v, s in crit if s == 'RED']
    print(f'criticality: {sum(1 for _, s in crit if s == "NEC")} necessary,'
          f' {len(redundant)} redundant, '
          f'{sum(1 for _, s in crit if s == "CARD")} cardinality-locked',
          flush=True)
    rec = {'tag': f'C3MUS M={M} bounds={list(bounds)}', 'M': M,
           'bounds': list(bounds), 'n_support': len(sup),
           'support': sorted(sup), 'block_sizes': bs,
           'glucose_reverify': bool(ok2), 'criticality': crit,
           'solves': total_solves}
    stream(rec)
    with open(os.path.join(DATA, f'e120_C3_mus_M{M}.json'), 'w') as f:
        json.dump(rec, f, indent=1)


if __name__ == '__main__':
    M = int(sys.argv[1])
    b = (int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
    c0 = int(sys.argv[5]) if len(sys.argv) > 5 else 16
    run(M, b, c0)
