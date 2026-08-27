"""e129 part 1: rigorous anchor-coordinate comparison of the two
coupled-core MUS anatomies (M=32 b333 n=116 vs M=48 b222 n=153), plus
machine verification of the arithmetic zone claims that the notes/51
schema rests on.

Outputs a comparison table (proportional + offset coordinates), an
interval decomposition of each support, run-length statistics of the
B0 anchor material (the adjacent-pair claim), and checks:

  C1  3-block APs (a in B0, b in B1, c=2b-a in B2) need b > 5M/2 exactly
      (and this is sharp).
  C2  with a > 4M/3 the 3-block image caps at c < 20M/3 (sharp as a -> 4M/3).
  C3  both MUS B2 supports lie inside (4M, 20M/3].
  C4  both MUS B1 supports lie inside (5M/2, 4M].
  C5  M=48 MUS B0 support lies inside (4M/3, 2M]; M=32 does NOT
      (records the exceptional values).
  C6  B0 support is dominated by adjacent runs of length >= 2
      (the flood-anchor pair claim); list singletons.
  C7  B2 in-block reachability: values in (7M, 8M] belong to no cross AP
      at all (degree-0 top zone) - recomputed from scratch.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), 'data')


def load(tag):
    with open(os.path.join(DATA, f'e126_mus_{tag}.json')) as f:
        return json.load(f)


def intervals(vals):
    vals = sorted(vals)
    out = []
    s = p = vals[0]
    for v in vals[1:]:
        if v == p + 1:
            p = v
        else:
            out.append((s, p))
            s = p = v
    out.append((s, p))
    return out


def fmt_iv(iv, M):
    return ' u '.join(
        (f'[{a},{b}]' if a != b else f'{{{a}}}') +
        f'({a/M:.3f}M..{b/M:.3f}M)' for a, b in iv)


def main():
    recs = {32: load('M32_b333'), 48: load('M48_b222')}
    for M, r in recs.items():
        print(f'=== M={M} bounds={r["bounds"]} n={r["n_support"]} ===')
        sup = set(r['support'])
        blocks = {'B0': (M, 2 * M), 'B1': (2 * M, 4 * M),
                  'B2': (4 * M, 8 * M)}
        for name, (lo, hi) in blocks.items():
            vals = sorted(v for v in sup if lo < v <= hi)
            iv = intervals(vals)
            print(f'  {name} n={len(vals)}: {fmt_iv(iv, M)}')
        print()

    # C1: 3-block APs need b > 5M/2, sharp.
    for M, r in recs.items():
        lo_b = None
        hi_c = 0
        for b in range(2 * M + 1, 4 * M + 1):
            for a in range(M + 1, 2 * M + 1):
                c = 2 * b - a
                if 4 * M < c <= 8 * M:
                    if lo_b is None or b < lo_b:
                        lo_b = b
        assert lo_b == (5 * M) // 2 + 1, (M, lo_b)
        print(f'C1 M={M}: min middle b of 3-block AP = {lo_b} = 5M/2+1  OK')

    # C2: a > 4M/3 => c = 2b - a < 20M/3 (b <= 4M); sharp.
    for M in (32, 48):
        amin = 4 * M // 3 + 1
        cmax = max(2 * b - a for b in range(2 * M + 1, 4 * M + 1)
                   for a in range(amin, 2 * M + 1)
                   if 4 * M < 2 * b - a <= 8 * M)
        print(f'C2 M={M}: max 3-block image with a>4M/3: {cmax} '
              f'(20M/3 = {20*M/3:.1f})  {"OK" if cmax < 20*M/3 else "FAIL"}')

    # C3/C4/C5: zone containment of the MUS supports.
    for M, r in recs.items():
        sup = set(r['support'])
        b2 = [v for v in sup if v > 4 * M]
        b1 = [v for v in sup if 2 * M < v <= 4 * M]
        b0 = [v for v in sup if v <= 2 * M]
        c3 = all(4 * M < v <= 20 * M / 3 for v in b2)
        c4 = all(5 * M / 2 < v <= 4 * M for v in b1)
        out0 = [v for v in b0 if not (4 * M / 3 < v <= 2 * M)]
        print(f'C3 M={M}: B2 subset of (4M,20M/3]: {c3} '
              f'(max {max(b2)} = {max(b2)/M:.3f}M, cap {20*M/3:.1f})')
        print(f'C4 M={M}: B1 subset of (5M/2,4M]: {c4} '
              f'(min {min(b1)} = {min(b1)/M:.3f}M, floor {5*M/2:.1f})')
        print(f'C5 M={M}: B0 values outside (4M/3,2M]: {sorted(out0)}')

    # C6: B0 adjacent-run statistics.
    for M, r in recs.items():
        sup = set(r['support'])
        b0 = sorted(v for v in sup if v <= 2 * M)
        iv = intervals(b0)
        singles = [a for a, b in iv if a == b]
        print(f'C6 M={M}: B0 runs = {iv}; singletons = {singles}; '
              f'{sum(b-a+1 for a,b in iv if b>a)}/{len(b0)} values in '
              f'runs >= 2')

    # C7: B2 values unreachable as the TOP of any 3-block AP
    # (a in B0, b in B1, c = 2b-a): expected exactly [7M, 8M]
    # (max image 2*4M - (M+1) = 7M-1).
    for M in (32, 48):
        reach = set()
        for b in range(2 * M + 1, 4 * M + 1):
            for a in range(M + 1, 2 * M + 1):
                c = 2 * b - a
                if 4 * M < c <= 8 * M:
                    reach.add(c)
        z = [v for v in range(4 * M + 1, 8 * M + 1) if v not in reach]
        exp = list(range(7 * M, 8 * M + 1))
        print(f'C7 M={M}: 3-block-unreachable B2 top zone = '
              f'[{min(z)},{max(z)}] ({len(z)} vals), expected '
              f'[7M,8M] = [{7*M},{8*M}]: '
              f'{"OK" if z == exp else "MISMATCH"}')


if __name__ == '__main__':
    main()
