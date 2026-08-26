"""e126: RESUMABLE deletion-minimal SUPPORT of the Case-2 coupled cores.

Same discipline as e120c3_mus (chunked greedy deletion, descending
values, vacuity guard, Glucose42 re-verify, per-value criticality) but
CRASH-SAFE: the surviving support is snapshotted to JSON after every
successful drop, and a rerun resumes from the snapshot instead of
replaying the deletion path.  Built for the two FRONT-MUS targets:

    e126_case2_mus.py 32 3 3 3     # the (3,3,3)@M=32 balanced-core MUS
    e126_case2_mus.py 48 2 2 2     # the (2,2,2)@M=48 critical-constant MUS

Ends with an ANCHOR-COORDINATE anatomy dump: each surviving value in
offsets from its block's ends (v - lo, hi - v) and from the block
midpoint, per block — the coordinates in which the M=32 and M=48
anatomies are to be compared (notes/48).

Snapshot: data/e126_mus_M{M}_b{b0}{b1}{b2}.resume.json
Final:    data/e126_mus_M{M}_b{b0}{b1}{b2}.json  (+ e120_results.jsonl)
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


def anchor_anatomy(sup, M):
    blocks = (('B0', M, 2 * M), ('B1', 2 * M, 4 * M), ('B2', 4 * M, 8 * M))
    out = {}
    for name, lo, hi in blocks:
        vals = sorted(v for v in sup if lo < v <= hi)
        mid = (lo + hi + 1) // 2
        out[name] = {
            'n': len(vals),
            'vals': vals,
            'bot_offsets': [v - lo for v in vals],       # v = lo + off
            'top_offsets': [hi - v for v in vals],       # v = hi - off
            'mid_offsets': [v - mid for v in vals],      # v = mid + off
            'parities_mod4': sorted({v % 4 for v in vals}),
        }
    return out


def run(M, bounds, chunk0=32):
    t00 = time.time()
    tag = f'M{M}_b{"".join(map(str, bounds))}'
    resume_path = os.path.join(DATA, f'e126_mus_{tag}.resume.json')
    final_path = os.path.join(DATA, f'e126_mus_{tag}.json')
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

    def snapshot(sup, phase, extra=None):
        rec = {'M': M, 'bounds': list(bounds), 'phase': phase,
               'n': len(sup), 'support': sorted(sup),
               'elapsed': round(time.time() - t00, 1)}
        if extra:
            rec.update(extra)
        with open(resume_path, 'w') as f:
            json.dump(rec, f)

    if os.path.exists(resume_path):
        with open(resume_path) as f:
            saved = json.load(f)
        sup = list(saved['support'])
        print(f'RESUME from snapshot: n={len(sup)} phase={saved["phase"]}',
              flush=True)
        ok, el = unsat(sup)
        print(f'resume verify M={M} bounds={bounds} n={len(sup)}: '
              f'{"UNSAT" if ok else "SAT"} [{el}s]', flush=True)
        assert ok, 'resumed support is not UNSAT — snapshot corrupt'
    else:
        ok, el = unsat(V)
        print(f'start M={M} bounds={bounds} n={len(V)}: '
              f'{"UNSAT" if ok else "SAT"} [{el}s]', flush=True)
        assert ok, 'core does not fire on the full window'
        sup = list(V)
        snapshot(sup, 'start')
    total_solves = 1

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
                snapshot(sup, f'chunk{chunk}')
            else:
                i += chunk
        chunk //= 2
    bs = blocksizes(sup)
    print(f'MINIMAL SUPPORT n={len(sup)} blocks={bs} '
          f'({total_solves} solves, {round(time.time() - t00, 1)}s)',
          flush=True)
    print('support =', sorted(sup), flush=True)
    snapshot(sup, 'minimal')

    # re-verify with Glucose42
    from pysat.solvers import Glucose42
    orig = e.Cadical195
    e.Cadical195 = Glucose42
    ok2, el2 = unsat(sup)
    e.Cadical195 = orig
    print(f'Glucose42 re-verify: {"UNSAT" if ok2 else "SAT!"} [{el2}s]',
          flush=True)

    # per-value criticality (deletion-minimality certificate)
    crit = []
    for v in sorted(sup):
        trial = [u for u in sup if u != v]
        if not feasible(trial):
            crit.append((v, 'CARD'))
            continue
        ok3, _ = unsat(trial)
        total_solves += 1
        crit.append((v, 'NEC' if not ok3 else 'RED'))
        snapshot(sup, 'criticality', {'crit_done': len(crit)})
    n_nec = sum(1 for _, s in crit if s == 'NEC')
    n_red = sum(1 for _, s in crit if s == 'RED')
    n_card = sum(1 for _, s in crit if s == 'CARD')
    print(f'criticality: {n_nec} necessary, {n_red} redundant, '
          f'{n_card} cardinality-locked', flush=True)

    anat = anchor_anatomy(sup, M)
    for name in ('B0', 'B1', 'B2'):
        a = anat[name]
        print(f'{name} n={a["n"]} bot_off={a["bot_offsets"]} '
              f'top_off={a["top_offsets"]} mid_off={a["mid_offsets"]} '
              f'mod4={a["parities_mod4"]}', flush=True)

    rec = {'tag': f'e126MUS M={M} bounds={list(bounds)}', 'M': M,
           'bounds': list(bounds), 'n_support': len(sup),
           'support': sorted(sup), 'block_sizes': bs,
           'glucose_reverify': bool(ok2), 'criticality': crit,
           'anatomy': anat, 'solves': total_solves,
           'elapsed': round(time.time() - t00, 1)}
    stream(rec)
    with open(final_path, 'w') as f:
        json.dump(rec, f, indent=1)
    print(f'FINAL written to {final_path}', flush=True)


if __name__ == '__main__':
    M = int(sys.argv[1])
    b = (int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
    c0 = int(sys.argv[5]) if len(sys.argv) > 5 else 32
    run(M, b, c0)
