"""e159c: MONSTER-SCALE A1-A9 attack-catalogue check (notes/55 SS2)
(FRONT MEGA-SCHEMA, notes/63).

e137's brute-force AP enumeration is O(M^2) time and memory — dead at
M = 2^13+.  This checker re-derives every family ARITHMETICALLY from
the raw definitions (a < b < c, a + c = 2b, block membership), by
looping over the MIDPOINT only and computing the partner range by
exact integer-interval intersection — O(M) time, O(1) memory per
family — then asserts every A1-A9 closed form / count / range of
notes/55 SS2 numerically at the given scale.

Independence: the interval derivation here never quotes the closed
forms (all family shapes are re-derived from block membership); the
closed forms are asserted AGAINST it.  Cross-validation: with
--xval, the arithmetically-materialized families are compared
SET-FOR-SET against e137's original brute-force enum_pattern at
moderate scales (48, 64, 80, 112, 160).

Run: .venv/bin/python experiments/e159c_mega_a1a9.py [M ...] [--xval]
Output: data/e159c_mega_a1a9.json
"""
import json
import os
import resource
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '..', 'data', 'e159c_mega_a1a9.json')


def blocks(M):
    return (M + 1, 2 * M), (3 * M - 15, 4 * M), (4 * M + 1, 6 * M + 15)


def mid_rows(M, pi, pk, blo, bhi):
    """For pattern (i, j, k) with midpoint block [blo, bhi]: for each
    midpoint b, the exact a-interval {a in block_i : 2b - a in
    block_k, a < b}.  Yields (b, alo, ahi) for nonempty rows."""
    ilo, ihi = pi
    klo, khi = pk
    for b in range(blo, bhi + 1):
        alo = max(ilo, 2 * b - khi)
        ahi = min(ihi, 2 * b - klo, b - 1)
        if alo <= ahi:
            yield b, alo, ahi


def check_M(M, materialize=False):
    P0, P1, P2 = blocks(M)
    F = (6 * M + 1, 6 * M + 15)
    fams = {}

    def mat(key, rows):
        if materialize:
            fams[key] = {(a, b, 2 * b - a)
                         for (b, alo, ahi) in rows for a in range(alo, ahi + 1)}

    # ---- A1 (0,0,1): midpoint in P0 ----
    rows = list(mid_rows(M, P0, P2 if False else P1, *P0))
    # NB: pattern (0,0,1): a in P0, b in P0, c in P1
    rows = list(mid_rows(M, P0, P1, *P0))
    mat((0, 0, 1), rows)
    assert [b for b, _, _ in rows] == list(range(2 * M - 7, 2 * M + 1)), \
        (M, 'A1 b-support')
    tot = 0
    for b, alo, ahi in rows:
        assert alo == M + 1, (M, 'A1 alo', b, alo)
        assert ahi == min(M + 15, 2 * b - 3 * M + 15), (M, 'A1 ahi', b)
        assert 2 * b - ahi >= 3 * M - 15 and 2 * b - alo <= 3 * M - 1, \
            (M, 'A1 c-range', b)
        tot += ahi - alo + 1
    assert tot == 64, (M, 'A1 count', tot)

    # ---- A2 (0,1,1): midpoint in P1 ----
    rows = list(mid_rows(M, P0, P1, *P1))
    mat((0, 1, 1), rows)
    assert [y for y, _, _ in rows] == list(range(3 * M - 15, 3 * M + 1)), \
        (M, 'A2 y-support')
    tot = 0
    for y, alo, ahi in rows:
        k = 3 * M - y
        assert 0 <= k <= 15, (M, 'A2 k', y)
        assert alo == max(M + 1, 2 * M - 2 * k) and ahi == 2 * M, \
            (M, 'A2 x-range', y, alo, ahi)
        # z = 2y - x range and gap d = y - x range
        assert 4 * M - 30 <= 2 * y - ahi and 2 * y - alo <= 4 * M, \
            (M, 'A2 z', y)
        assert M - 15 <= y - ahi and y - alo <= M + 15, (M, 'A2 gap', y)
        tot += ahi - alo + 1
    assert tot == 256, (M, 'A2 count', tot)

    # ---- A3/A4 (1,1,2): midpoint in P1 ----
    rows = list(mid_rows(M, P1, P2, *P1))
    mat((1, 1, 2), rows)
    n112 = 0
    for b, alo, ahi in rows:
        cmax = 2 * b - alo
        assert cmax <= 5 * M + 15, (M, 'A3 wall', b, cmax)
        assert cmax < 6 * M + 1, (M, 'A3 flood-free', b)   # also A9
        n112 += ahi - alo + 1
    # A4: parents of 4M+s — count via the arithmetic b-interval
    for s in range(1, M + 16):
        # b in P1 with a = 2b - (4M+s) in P1 and a < b
        bmin = max(3 * M - 15, -(-(7 * M - 15 + s) // 2),
                   (4 * M + s) // 2 + 1)
        bmax = 4 * M
        cnt = max(0, bmax - bmin + 1)
        assert cnt == (M + 15 - s) // 2 + 1, (M, 'A4 count', s, cnt)
        # endpoint identity vs the (4M-s-2t, 4M-t) closed form
        assert 4 * M - bmin == (M + 15 - s) // 2, (M, 'A4 t-range', s)
        # extreme pair at s = M+15
        if s == M + 15:
            assert bmin == bmax == 4 * M and 2 * bmin - (4 * M + s) \
                == 3 * M - 15, (M, 'A4 extreme')

    # ---- A5 (0,2,2): midpoint in P2, partner a in P0 ----
    rows = list(mid_rows(M, P0, P2, *P2))
    mat((0, 2, 2), rows)
    assert [y for y, _, _ in rows] == list(range(4 * M + 1, 4 * M + 8)), \
        (M, 'A5 y-support')
    tot = 0
    for y, alo, ahi in rows:
        mm = y - 4 * M
        zlo, zhi = 2 * y - ahi, 2 * y - alo
        assert zlo == 6 * M + 2 * mm and zhi == 6 * M + 15, \
            (M, 'A5 z-range', y, zlo, zhi)
        assert zlo >= F[0], (M, 'A5 z in F', y)          # z in F
        assert 2 * M - 13 <= alo and ahi <= 2 * M, (M, 'A5 x', y)
        assert y < F[0], (M, 'A9 A5-mid not in F', y)    # A9
        tot += ahi - alo + 1
    assert tot == 56, (M, 'A5 count', tot)

    # ---- A6 (1,2,2): midpoint in P2, partner a in P1 ----
    rows = list(mid_rows(M, P1, P2, *P2))
    mat((1, 2, 2), rows)
    n122 = 0
    seen_y = set()
    for y, alo, ahi in rows:
        seen_y.add(y)
        assert y <= 5 * M + 7, (M, 'A6 midpoint cap', y)  # also A9
        n122 += ahi - alo + 1
    assert seen_y == set(range(4 * M + 1, 5 * M + 8)), (M, 'A6 y-support')
    # F tops: exact midpoint interval per f in F
    row_by_y = {y: (alo, ahi) for y, alo, ahi in rows}
    for f in range(F[0], F[1] + 1):
        lo = -(-(f + 3 * M - 15) // 2)
        hi = (f + 4 * M) // 2
        # check the predicate "f is a completion of midpoint y" exactly
        # on [lo - 3, hi + 3]
        for y in range(lo - 3, hi + 3 + 1):
            pred = y in row_by_y and \
                row_by_y[y][0] <= 2 * y - f <= row_by_y[y][1]
            assert pred == (lo <= y <= hi), (M, 'A6 F mids', f, y)
        assert lo <= hi, (M, 'A6 F top reached', f)

    # ---- A7 (0,1,2): straddles, midpoint in P1 ----
    rows = list(mid_rows(M, P0, P2, *P1))
    mat((0, 1, 2), rows)
    n7 = sum(ahi - alo + 1 for _, alo, ahi in rows)
    for y, alo, ahi in rows:
        # parity: z - u = 2(y - u) is even — identity, spot the ends
        assert (2 * y - alo - alo) % 2 == 0 and (2 * y - ahi - ahi) % 2 == 0
        # F-straddles: u range for z in F
        uflo, ufhi = max(M + 1, 2 * y - 6 * M - 15), \
            min(2 * M, 2 * y - 6 * M - 1)
        nonempty = uflo <= ufhi
        assert nonempty == (2 * y >= 7 * M + 2), (M, 'A7b onset', y)
        if nonempty:
            assert ufhi <= 2 * M - 1 and y <= 4 * M, (M, 'A7b u', y)
    # F image of the y = 4M doubling
    assert {2 * (4 * M) - u for u in range(2 * M - 15, 2 * M)} \
        == set(range(F[0], F[1] + 1)), (M, 'A7b doubling')
    # pressure zone: z = 2y - u monotone in u; check both u endpoints
    for y in range(3 * M + 1, (7 * M + 14) // 2 + 1):
        for u in (M + 1, 2 * M):
            z = 2 * y - u
            assert 4 * M + 1 <= z <= 6 * M + 15, (M, 'A7c', y, u)
    # band-edge reach
    for u in range(M + 1, 2 * M + 1):
        z = 2 * (3 * M - 15) - u
        assert (4 * M + 1 <= z <= 6 * M + 15) == (u <= 2 * M - 31), \
            (M, 'A7d', u)
    assert 2 * (3 * M - 15) - (2 * M - 31) == 4 * M + 1, (M, 'A7d edge')

    # ---- A8 (2,2,2) mirror widths ----
    if materialize:
        fams[(2, 2, 2)] = {(c - e, c, c + e)
                           for c in range(P2[0], P2[1] + 1)
                           for e in range(1, min(c - P2[0],
                                                 P2[1] - c) + 1)}
    for c in range(P2[0], P2[1] + 1):
        w = min(c - (4 * M + 1), 6 * M + 15 - c)
        # boundary membership check of the width (direct, not formulaic)
        if w >= 1:
            assert P2[0] <= c - w and c + w <= P2[1], (M, 'A8 in', c)
        assert c - (w + 1) < P2[0] or c + (w + 1) > P2[1], (M, 'A8 out', c)
    assert min(6 * M - (4 * M + 1), 15) == 15, (M, 'A8 6M window')
    assert {6 * M + e for e in range(1, 16)} \
        == set(range(F[0], F[1] + 1)), (M, 'A8 F')

    # ---- A9 (remaining halves asserted inline above) ----
    assert 5 * M + 15 < 6 * M + 1, (M, 'A9 wall strict')

    return n7, n112, n122, fams


def xval(Ms):
    """Set-for-set cross-validation vs e137's brute-force enumerator."""
    sys.path.insert(0, HERE)
    from e137_core_arith import enum_pattern
    for M in Ms:
        n7, n112, n122, fams = check_M(M, materialize=True)
        ref = enum_pattern(M)
        for key, mine in sorted(fams.items()):
            theirs = ref.get(key, set())
            assert mine == theirs, (M, key, len(mine), len(theirs),
                                    list(mine ^ theirs)[:4])
        print(f'  xval M={M}: {len(fams)} families identical to e137 '
              f'brute force '
              f'({", ".join(str(len(v)) for _, v in sorted(fams.items()))})',
              flush=True)


def main():
    args = [a for a in sys.argv[1:]]
    do_x = '--xval' in args
    Ms = [int(a) for a in args if a != '--xval']
    out = {'rows': [], 'fail': []}
    if do_x:
        print('cross-validation vs e137 enum_pattern:', flush=True)
        xval([48, 64, 80, 112, 160])
        out['xval'] = [48, 64, 80, 112, 160]
    for M in Ms or []:
        t0 = time.time()
        try:
            n7, n112, n122, _ = check_M(M)
            dt = time.time() - t0
            ru = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            mb = ru / 2 ** 20 if sys.platform == 'darwin' else ru / 1024
            row = {'M': M, 'ok': True, 's': round(dt, 2),
                   'n_straddle': n7, 'n_112': n112, 'n_122': n122,
                   'peak_rss_mb': round(mb, 1)}
            print(f'M={M}: A1..A9 arithmetic checks OK [{dt:.2f}s]  '
                  f'|straddle|={n7} |112|={n112} |122|={n122}  '
                  f'RSS {mb:.0f} MB', flush=True)
        except AssertionError as ex:
            row = {'M': M, 'ok': False, 'err': repr(ex.args[:3])}
            out['fail'].append(row)
            print(f'M={M}: FAIL {ex.args[:3]!r}', flush=True)
        out['rows'].append(row)
        json.dump(out, open(DATA, 'w'), indent=1)
    print(f"failures: {out['fail']}")
    print(f'-> {DATA}')
    if out['fail']:
        sys.exit(1)


if __name__ == '__main__':
    main()
