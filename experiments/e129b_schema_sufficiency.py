"""e129 part 2: SUFFICIENCY of the notes/51 all-M schema zones for the
coupled 2-seam core.

Schema zones (parametric in M):
    Z0 = (floor(4M/3), 2M]      B0 flood-anchor zone
    Z1 = (5M/2, 4M]             B1 spine (= exact 3-block middle zone)
    Z2 = (4M, floor(20M/3)]     B2 receiver band (3-block image cap
                                 given a > 4M/3)

Claim to verify: solve_coupled3(M, abs_bounds=bnds, support=S(M)) is
UNSAT for (M, bnds) in (32,(3,3,3)), (48,(2,2,2)), (64,(2,2,2)),
(80,(2,2,2)).  Optional variants via CLI:

    e129b_schema_sufficiency.py M b0 b1 b2 [z0num z0den [z1num z1den [z2num z2den]]]

z0num/z0den override Z0's lower edge fraction (default 4/3; 1 1 =
full B0).  z1num/z1den override Z1's lower edge (default 5/2; the
coupling law floor(Z1) = (minZ0 + 4M)/2 suggests 8/3 when Z0 = 4/3).
z2num/z2den override Z2's upper edge (default 20/3).
Appends one JSON line per run to data/e129b_sufficiency.jsonl.
"""
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
DATA = os.path.join(os.path.dirname(HERE), 'data')

import e120_density_cores as e


def schema_support(M, z0num=4, z0den=3, z1num=5, z1den=2,
                   z2num=20, z2den=3):
    z0 = list(range(z0num * M // z0den + 1, 2 * M + 1))
    z1 = list(range(z1num * M // z1den + 1, 4 * M + 1))
    z2 = list(range(4 * M + 1, z2num * M // z2den + 1))
    return z0, z1, z2


def main():
    M = int(sys.argv[1])
    bnds = (int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
    fr = [int(x) for x in sys.argv[5:]]
    fr = fr + [4, 3, 5, 2, 20, 3][len(fr):]
    z0num, z0den, z1num, z1den, z2num, z2den = fr[:6]
    z0, z1, z2 = schema_support(M, *fr[:6])
    sup = z0 + z1 + z2
    print(f'M={M} bounds={bnds} Z0=({z0num}M/{z0den},2M] '
          f'Z1=({z1num}M/{z1den},4M] Z2=(4M,{z2num}M/{z2den}] '
          f'|Z0|={len(z0)} |Z1|={len(z1)} |Z2|={len(z2)} n={len(sup)}',
          flush=True)
    t0 = time.time()
    v, el, info = e.solve_coupled3(M, 0, 1, abs_bounds=list(bnds),
                                   support=sup)
    print(f'verdict: {v} [{el}s]', flush=True)
    rec = {'tag': 'e129b', 'M': M, 'bounds': list(bnds),
           'z0': [z0num, z0den], 'z1': [z1num, z1den],
           'z2': [z2num, z2den], 'n': len(sup),
           'sizes': [len(z0), len(z1), len(z2)],
           'verdict': v, 'elapsed': el}
    if v == 'SAT':
        rec['escape_A_blocks'] = {
            'B0': [x for x in info['A'] if x <= 2 * M],
            'B1': [x for x in info['A'] if 2 * M < x <= 4 * M],
            'B2': [x for x in info['A'] if x > 4 * M]}
        rec['escape_B_blocks'] = {
            'B0': [x for x in info['B'] if x <= 2 * M],
            'B1': [x for x in info['B'] if 2 * M < x <= 4 * M],
            'B2': [x for x in info['B'] if x > 4 * M]}
        print('ESCAPE A:', rec['escape_A_blocks'], flush=True)
        print('ESCAPE B:', rec['escape_B_blocks'], flush=True)
    with open(os.path.join(DATA, 'e129b_sufficiency.jsonl'), 'a') as f:
        f.write(json.dumps(rec) + '\n')
    print(f'total {round(time.time()-t0,1)}s', flush=True)


if __name__ == '__main__':
    main()
