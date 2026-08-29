"""e171b: anchor-coordinate comparison of budget-core MUS supports.

Loads e171 result JSONs (final or .resume snapshots), plus optionally
the e126 (3,3,3)@32 support and the e158b (16;6,0) support, and prints
per-block aligned anatomies + set deltas along the v-ladder at fixed M
+ proportional coordinates across M.

Usage: e171b_anatomy_compare.py [--files f1 f2 ...]
Default: picks up every data/e171_mus_*.json (falling back to
.resume.json when no final exists), ordered by (M, v).
"""
import argparse
import glob
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), 'data')


def blocks_of(M):
    return (('B0', M, 2 * M), ('B1', 2 * M, 4 * M), ('B2', 4 * M, 8 * M))


def load_all(paths=None):
    recs = []
    if paths is None:
        finals = glob.glob(os.path.join(DATA, 'e171_mus_*.json'))
        finals = [p for p in finals if not p.endswith('.resume.json')]
        seen = set()
        paths = []
        for p in finals:
            paths.append(p)
            seen.add(p.replace('.json', ''))
        for p in glob.glob(os.path.join(DATA, 'e171_mus_*.resume.json')):
            if p.replace('.resume.json', '') not in seen:
                paths.append(p)
    for p in sorted(paths):
        with open(p) as f:
            r = json.load(f)
        r['_path'] = os.path.basename(p)
        r['_final'] = not p.endswith('.resume.json')
        recs.append(r)
    recs.sort(key=lambda r: (r['M'], r['v']))
    return recs


def runs(vals):
    """Compress a sorted value list to interval runs."""
    if not vals:
        return []
    out = []
    a = b = vals[0]
    for x in vals[1:]:
        if x == b + 1:
            b = x
        else:
            out.append((a, b))
            a = b = x
    out.append((a, b))
    return out


def fmt_runs(vals):
    return ' '.join(f'[{a}..{b}]' if a != b else f'{{{a}}}'
                    for a, b in runs(sorted(vals)))


def describe(rec):
    M, v = rec['M'], rec['v']
    sup = set(rec['support'])
    phase = 'FINAL' if rec['_final'] else f"partial({rec.get('phase')})"
    print(f"== M={M} v={v} n={len(sup)} {phase}  [{rec['_path']}]")
    for name, lo, hi in blocks_of(M):
        vals = sorted(u for u in sup if lo < u <= hi)
        full = hi - lo
        bound = max(0, full // 2 - (full - len(vals)))
        print(f'  {name} ({lo},{hi}] n={len(vals)}/{full} bound={bound}: '
              f'{fmt_runs(vals)}')
        if vals:
            print(f'      bot_off={vals[0]-lo}..{vals[-1]-lo} '
                  f'frac=[{(vals[0]-lo)/full:.3f},{(vals[-1]-lo)/full:.3f}]'
                  f' mod4={sorted({u % 4 for u in vals})}')
    print()


def delta(r1, r2):
    s1, s2 = set(r1['support']), set(r2['support'])
    M = r1['M']
    print(f"-- DELTA M={M}: v={r1['v']} (n={len(s1)}) -> v={r2['v']} "
          f"(n={len(s2)})")
    for name, lo, hi in blocks_of(M):
        add = sorted(u for u in s2 - s1 if lo < u <= hi)
        rem = sorted(u for u in s1 - s2 if lo < u <= hi)
        n1 = len([u for u in s1 if lo < u <= hi])
        n2 = len([u for u in s2 if lo < u <= hi])
        print(f'  {name}: {n1} -> {n2}   +{fmt_runs(add) or "-"}   '
              f'-{fmt_runs(rem) or "-"}')
    print()


def cross_scale(r1, r2):
    """Same v, different M: proportional block coordinates."""
    print(f"-- CROSS-SCALE v={r1['v']}: M={r1['M']} (n={len(r1['support'])})"
          f" vs M={r2['M']} (n={len(r2['support'])})")
    for rec in (r1, r2):
        M = rec['M']
        sup = set(rec['support'])
        row = []
        for name, lo, hi in blocks_of(M):
            vals = [u for u in sup if lo < u <= hi]
            full = hi - lo
            row.append(f'{name}:{len(vals)}/{full}'
                       f'={len(vals)/full:.2f}')
        print(f'   M={M}: ' + '  '.join(row))
    print()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--files', nargs='*', default=None)
    args = ap.parse_args()
    recs = load_all(args.files)
    for r in recs:
        describe(r)
    byM = {}
    for r in recs:
        byM.setdefault(r['M'], []).append(r)
    for M, rs in sorted(byM.items()):
        for a, b in zip(rs, rs[1:]):
            delta(a, b)
    byv = {}
    for r in recs:
        byv.setdefault(r['v'], []).append(r)
    for v, rs in sorted(byv.items()):
        for a, b in zip(rs, rs[1:]):
            cross_scale(a, b)


if __name__ == '__main__':
    main()
