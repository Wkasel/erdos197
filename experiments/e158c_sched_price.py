"""e158c: mixed-theory tax of a FIXED coloring in the 4-block gadget.

Fixes the coloring to a block-parity schedule (default the
zero-sumset schedule (x, x, 1-x, 1-x) of notes/62 SS4c: team A =
parity-1 on Bm1 u B0, parity-0 on B1 u B2) and scans vup at vdn = 0.
Orders-only instance (colors are unit clauses), so it reaches scales
the free-coloring instance cannot.  Output: the least vup with SAT —
an upper bound on v_min(0)(M) and the hand-ladder target
mixedtax(M) for the schedule.

Usage: e158c_sched_price.py --M 16 --sched 1100 --vups 0,1,2,4,8
       [--vdn 0] [--budget 600]
Artifacts: data/e158c_sched.jsonl + per-run log lines.
"""
import argparse
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
DATA = os.path.join(REPO, 'data')
sys.path.insert(0, HERE)
import importlib
e158 = importlib.import_module('e158_joint4')

JSONL = os.path.join(DATA, 'e158c_sched.jsonl')


def sched_color(M, sched):
    """sched: 4 chars in {0,1}, parity of team A per block."""
    V, blks = e158.blocks_of(M)
    colA = []
    for par, blk in zip(sched, blks):
        colA += [v for v in blk if v % 2 == int(par)]
    return sorted(colA)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--M', type=int, required=True)
    ap.add_argument('--sched', type=str, default='1100')
    ap.add_argument('--vups', type=str, required=True)
    ap.add_argument('--vdn', type=str, default='0')
    ap.add_argument('--budget', type=float, default=600.0)
    args = ap.parse_args()
    vdn = None if args.vdn.lower() == 'none' else int(args.vdn)
    colA = sched_color(args.M, args.sched)
    fixed = {'colorA': colA}
    for vs in args.vups.split(','):
        vup = None if vs.lower() == 'none' else int(vs)
        kw = dict(M=args.M, abs_bounds=None, vup=vup, vdn=vdn,
                  fixed_colorA=colA)
        verdict, el, info = e158.solve_joint_sub(kw, args.budget)
        row = {'exp': 'e158c', 'M': args.M, 'sched': args.sched,
               'vup': vup, 'vdn': vdn, 'verdict': verdict, 'time': el}
        if verdict == 'SAT':
            errs, anat = e158.audit(args.M, info['bounds'],
                                    10**9 if vup is None else vup,
                                    10**9 if vdn is None else vdn,
                                    info)
            if errs:
                row['verdict'] = 'WITNESS-FAIL'
                row['errs'] = errs[:8]
            row['anatomy'] = {t: {k: a[k] for k in
                                  ('sizes', 'n_s0', 'n_s1', 'n_s2',
                                   'n_up', 'n_dn', 'n_H_up',
                                   'n_H_dn')}
                              for t, a in anat.items()}
            if sorted(info['A']) != colA:
                row['verdict'] = 'COLOR-FAIL'
        with open(JSONL, 'a') as f:
            f.write(json.dumps(row) + '\n')
        print(f'M={args.M} sched={args.sched} vup={vs} vdn={args.vdn}:'
              f' {row["verdict"]} [{el}s] '
              + json.dumps(row.get('anatomy', {})), flush=True)
        if row['verdict'] == 'SAT':
            break


if __name__ == '__main__':
    main()
