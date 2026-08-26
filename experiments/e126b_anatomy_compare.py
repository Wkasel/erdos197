"""e126b: compare Case-2 MUS anatomies across scales in anchor coordinates.

Loads the deletion-minimal supports (final JSONs, or resume snapshots if
the finals are not yet written) for (M, bounds) pairs and prints, per
block, the support in the three anchor systems:
  bottom  : v = lo + off   (offsets from the block's low end)
  top     : v = hi - off   (offsets from the block's high end)
  midband : v = mid + off  (offsets from the block midpoint)
plus mod-4 residue classes (the sumset-dodge lattice), and the overlap
of the two scales' offset sets in each system (the scale-stability
verdict: which anchor system makes the supports agree?).

Usage: e126b_anatomy_compare.py M1 b1 M2 b2   (b = e.g. 333 or 222)
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), 'data')


def load(M, btag):
    for suffix in ('.json', '.resume.json'):
        p = os.path.join(DATA, f'e126_mus_M{M}_b{btag}{suffix}')
        if os.path.exists(p):
            with open(p) as f:
                rec = json.load(f)
            sup = rec.get('support', [])
            phase = rec.get('phase', 'final')
            return sorted(sup), phase, p
    raise SystemExit(f'no support file for M={M} b={btag}')


def blocks_of(M):
    return (('B0', M, 2 * M), ('B1', 2 * M, 4 * M), ('B2', 4 * M, 8 * M))


def coords(sup, M):
    out = {}
    for name, lo, hi in blocks_of(M):
        vals = sorted(v for v in sup if lo < v <= hi)
        mid = (lo + hi + 1) // 2
        out[name] = {
            'vals': vals,
            'bot': [v - lo for v in vals],
            'top': [hi - v for v in vals],
            'mid': [v - mid for v in vals],
            'mod4': [v % 4 for v in vals],
        }
    return out


def main(M1, b1, M2, b2):
    s1, ph1, p1 = load(M1, b1)
    s2, ph2, p2 = load(M2, b2)
    print(f'M={M1} b={b1} [{ph1}] n={len(s1)}  ({p1})')
    print(f'M={M2} b={b2} [{ph2}] n={len(s2)}  ({p2})')
    c1, c2 = coords(s1, M1), coords(s2, M2)
    for name in ('B0', 'B1', 'B2'):
        a, b = c1[name], c2[name]
        print(f'\n== {name} ==  n: {len(a["vals"])} vs {len(b["vals"])}')
        print(f'  M={M1} vals: {a["vals"]}')
        print(f'  M={M2} vals: {b["vals"]}')
        for sysname in ('bot', 'top', 'mid'):
            A, B = set(a[sysname]), set(b[sysname])
            inter = sorted(A & B)
            jac = len(A & B) / max(1, len(A | B))
            print(f'  {sysname:>4}: M{M1}={sorted(A)}')
            print(f'        M{M2}={sorted(B)}')
            print(f'        common={inter}  jaccard={jac:.2f}')
        from collections import Counter
        print(f'  mod4 hist: M{M1}={dict(Counter(a["mod4"]))} '
              f'M{M2}={dict(Counter(b["mod4"]))}')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
