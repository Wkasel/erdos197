"""e158b: deletion-minimal value SUPPORT of the 4-block joint core.

Target: the C3 cell (bal, M; vup, vdn) — e.g. (16; 6, 0), UNSAT in
2.1 s.  Restriction-monotone deletion semantics for balance bounds:
deleting a value from block i lowers that block's per-team lower
bound by one (bound_i = max(0, ceil(|full blk_i|/2) − #deleted_i)),
so any model of the FULL instance restricts to a model of the
support instance — support UNSAT is a certified strengthening chain
back to the full core.  Chunked greedy deletion (descending values),
crash-safe snapshot after every accepted deletion; final per-value
criticality pass.

Usage: e158b_joint_mus.py --M 16 --vup 6 --vdn 0 [--budget 300]
Artifacts: data/e158b_mus_M{M}_up{vup}_dn{vdn}.json (+ .resume.json)
"""
import argparse
import json
import math
import os
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
DATA = os.path.join(REPO, 'data')
import sys
sys.path.insert(0, HERE)
import importlib
e158 = importlib.import_module('e158_joint4')


def bounds_for(M, support):
    _, blks = e158.blocks_of(M)
    sset = set(support)
    out = []
    for blk in blks:
        full = math.ceil(len(blk) / 2)
        deleted = len([v for v in blk if v not in sset])
        out.append(max(0, full - deleted))
    return tuple(out)


def is_unsat(M, vup, vdn, support, budget):
    kw = dict(M=M, abs_bounds=bounds_for(M, support), vup=vup,
              vdn=vdn, support=sorted(support))
    verdict, el, _ = e158.solve_joint_sub(kw, budget)
    return verdict == 'UNSAT', verdict, el


def run(M, vup, vdn, budget, chunk0=16):
    tag = f'M{M}_up{vup}_dn{vdn}'
    path = os.path.join(DATA, f'e158b_mus_{tag}.json')
    rpath = os.path.join(DATA, f'e158b_mus_{tag}.resume.json')
    Vfull, _ = e158.blocks_of(M)
    if os.path.exists(rpath):
        with open(rpath) as f:
            saved = json.load(f)
        sup = list(saved['support'])
        ok, verdict, el = is_unsat(M, vup, vdn, sup, budget)
        print(f'resume n={len(sup)}: {verdict} [{el}s]', flush=True)
        assert ok, 'resumed support not UNSAT — snapshot corrupt'
    else:
        sup = list(Vfull)
        ok, verdict, el = is_unsat(M, vup, vdn, sup, budget)
        print(f'start n={len(sup)}: {verdict} [{el}s]', flush=True)
        assert ok, 'full instance not UNSAT'

    def snap(phase):
        with open(rpath, 'w') as f:
            json.dump({'M': M, 'vup': vup, 'vdn': vdn, 'phase': phase,
                       'n': len(sup), 'support': sorted(sup)}, f)

    chunk = chunk0
    while chunk >= 1:
        # descending passes: try deleting chunks of values
        i = 0
        order = sorted(sup, reverse=True)
        while i < len(order):
            cand = [v for v in order[i:i + chunk] if v in sup]
            if not cand:
                i += chunk
                continue
            trial = [v for v in sup if v not in set(cand)]
            ok, verdict, el = is_unsat(M, vup, vdn, trial, budget)
            if ok:
                sup = trial
                snap(f'chunk{chunk}')
                print(f'  -{len(cand)} (n={len(sup)}) [{el}s]',
                      flush=True)
            i += chunk
        chunk //= 2
    # criticality certificate
    crit = {'necessary': [], 'redundant': []}
    for v in sorted(sup):
        trial = [x for x in sup if x != v]
        ok, verdict, el = is_unsat(M, vup, vdn, trial, budget)
        if ok:
            crit['redundant'].append(v)
            sup = trial
            snap('crit')
        else:
            crit['necessary'].append(v)
    _, blks = e158.blocks_of(M)
    names = ('Bm1', 'B0', 'B1', 'B2')
    anat = {}
    for nm, blk in zip(names, blks):
        inb = sorted(set(sup) & set(blk))
        anat[nm] = {'n': len(inb), 'vals': inb,
                    'bound': bounds_for(M, sup)[names.index(nm)]}
    rec = {'tag': f'e158bMUS {tag}', 'M': M, 'vup': vup, 'vdn': vdn,
           'n_support': len(sup), 'support': sorted(sup),
           'criticality': {k: len(v) for k, v in crit.items()},
           'necessary': crit['necessary'],
           'redundant_late': crit['redundant'], 'anatomy': anat}
    with open(path, 'w') as f:
        json.dump(rec, f, indent=1)
    print(f'FINAL n={len(sup)} necessary={len(crit["necessary"])} '
          f'redundant-in-pass={len(crit["redundant"])}', flush=True)
    for nm in names:
        print(f'  {nm} (bound {anat[nm]["bound"]}): '
              f'{anat[nm]["vals"]}', flush=True)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--M', type=int, default=16)
    ap.add_argument('--vup', type=int, default=6)
    ap.add_argument('--vdn', type=int, default=0)
    ap.add_argument('--budget', type=float, default=600.0)
    ap.add_argument('--chunk', type=int, default=16)
    args = ap.parse_args()
    run(args.M, args.vup, args.vdn, args.budget, args.chunk)
