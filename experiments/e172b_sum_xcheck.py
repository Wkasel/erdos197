"""e172b: independent cross-check of e172's RC2 sum lower bounds.

A sum-LB "inv_A + inv_B >= s" is equivalent to: for every split
vA + vB = s - 1 (vA <= vB by team symmetry of the bal instance),
U(M; c; vA, vB) is UNSAT.  Those are plain DECISION queries on the
audited e127 instrument with a DIFFERENT solver (Cadical195 vs RC2's
glucose oracle) and a different encoding of the bound (two per-team
seqcounters vs RC2's relaxation sums) — an end-to-end cross-validation
of the MaxSAT pipeline at affordable milestones.

Usage: e172b_sum_xcheck.py --M 16 --sum-lb 5 [--budget 3600] [--bounds bal]
Streams to data/e172_maxsat_lb.jsonl (event 'xcheck') and prints TERSE.
"""
import argparse
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), 'data')
sys.path.insert(0, HERE)
import e127_seam_budget as e127


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--M', type=int, required=True)
    ap.add_argument('--sum-lb', type=int, required=True,
                    help='the RC2 lower bound s to verify (checks all '
                         'splits of s-1)')
    ap.add_argument('--bounds', type=str, default='bal')
    ap.add_argument('--budget', type=float, default=3600.0)
    args = ap.parse_args()
    abs_bounds = (None if args.bounds == 'bal'
                  else tuple(int(x) for x in args.bounds.split(',')))
    s = args.sum_lb
    tag = f'xcheck_{args.bounds.replace(",", "_")}_M{args.M}_s{s}'
    rows = []
    ok = True
    for vA in range(0, (s - 1) // 2 + 1):
        vB = (s - 1) - vA
        verdict, el, info = e127.solve_budget_sub(
            dict(M=args.M, abs_bounds=abs_bounds, vA=vA, vB=vB),
            args.budget)
        row = {'tag': tag, 'event': 'xcheck', 'M': args.M,
               'bounds': abs_bounds, 'vA': vA, 'vB': vB,
               'verdict': verdict, 'time': el}
        rows.append(row)
        with open(os.path.join(DATA, 'e172_maxsat_lb.jsonl'), 'a') as f:
            f.write(json.dumps(row) + '\n')
        print(f'  {tag} ({vA},{vB}): {verdict} [{el}s]', flush=True)
        if verdict == 'SAT':
            ok = False
            errs, anat = e127.audit(args.M, info['bounds'], vA, vB, info)
            print(f'  !! SAT at split ({vA},{vB}) — RC2 LB {s} is '
                  f'WRONG (audit errs {len(errs)}) — INVESTIGATE',
                  flush=True)
            break
        if verdict == 'TIMEOUT':
            ok = None
    verdictline = ('CONFIRMED sum >= %d' % s if ok else
                   'INCONCLUSIVE (timeout)' if ok is None else
                   'REFUTED — bug hunt required')
    print(f'== {tag}: {verdictline}', flush=True)
    with open(os.path.join(DATA, f'e172_{tag}.json'), 'w') as f:
        json.dump({'tag': tag, 'rows': rows, 'verdict': verdictline},
                  f, indent=1)


if __name__ == '__main__':
    main()
