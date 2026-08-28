"""e137: machine check of notes/55 SS2 (arithmetic catalogue A1-A9).

Pure enumeration, no solver.  For M = 48, 64, 80 (and a long sweep of
the pure inequalities at every M = 0 mod 16 in 48..400):

  A1  (0,0,1) family == closed form; |family| == 64; c-range E1 cap.
  A2  (0,1,1) family == closed form; |family| == 256; gap range.
  A3  every high band pair completes into [4M+1, 5M+15]; wall < 6M+1.
  A4  parents of 4M+s == closed form; counts; extreme pair.
  A5  (0,2,2) family == closed form; |family| == 56; z in F.
  A6  (1,2,2) family == closed form; midpoint cap 5M+7; F tops.
  A7  straddle parity; F-straddle ranges; F == 2*4M - [2M-15, 2M-1]
      via y = 4M; full-block pressure zone; band-edge reach.
  A8  mirror widths at every centre of P2; 6M window == 15; upper
      range == F.
  A9  no (1,1,2) completion in F; no (0,2,2)/(1,2,2) midpoint in F.

Run: .venv/bin/python experiments/e137_core_arith.py
Log: data/e137_arith.log
"""
import sys


def blocks(M):
    P0 = range(M + 1, 2 * M + 1)
    P1 = range(3 * M - 15, 4 * M + 1)
    P2 = range(4 * M + 1, 6 * M + 16)
    return P0, P1, P2


def enum_pattern(M):
    """All APs of CORE'(M), keyed by block pattern."""
    P0, P1, P2 = blocks(M)
    V = sorted(set(P0) | set(P1) | set(P2))
    Vs = set(V)

    def blk(v):
        return 0 if v <= 2 * M else (1 if v <= 4 * M else 2)

    fam = {}
    for b in V:
        for d in range(1, (V[-1] - V[0]) // 2 + 1):
            a, c = b - d, b + d
            if a in Vs and c in Vs:
                fam.setdefault((blk(a), blk(b), blk(c)), set()).add(
                    (a, b, c))
    return fam


def check_M(M):
    P0, P1, P2 = blocks(M)
    fam = enum_pattern(M)
    F = set(range(6 * M + 1, 6 * M + 16))

    # ---- A1
    a1 = fam.get((0, 0, 1), set())
    closed = set()
    for b in range(2 * M - 7, 2 * M + 1):
        for a in range(M + 1, min(M + 15, 2 * b - 3 * M + 15) + 1):
            closed.add((a, b, 2 * b - a))
    assert a1 == closed, (M, 'A1', len(a1), len(closed))
    assert len(a1) == 64, (M, 'A1 count', len(a1))
    assert all(3 * M - 15 <= c <= 3 * M - 1 for (_, _, c) in a1), (M, 'A1 c')
    assert all(2 * M - 7 <= b for (_, b, _) in a1), (M, 'A1 b')
    assert all(a <= M + 15 for (a, _, _) in a1), (M, 'A1 a')

    # ---- A2
    a2 = fam.get((0, 1, 1), set())
    closed = set()
    for k in range(0, 16):
        y = 3 * M - k
        for x in range(max(M + 1, 2 * M - 2 * k), 2 * M + 1):
            z = 2 * y - x
            closed.add((x, y, z))
    assert a2 == closed, (M, 'A2', len(a2), len(closed))
    assert len(a2) == 256, (M, 'A2 count', len(a2))
    for (x, y, z) in a2:
        d = y - x
        assert M - 15 <= d <= M + 15, (M, 'A2 gap', d)
        assert 4 * M - 30 <= z <= 4 * M, (M, 'A2 z', z)
        assert 3 * M - 15 <= y <= 3 * M, (M, 'A2 y', y)

    # ---- A3 + A4 via (1,1,2)
    a112 = fam.get((1, 1, 2), set())
    # every high pair completes, completion in [4M+1, 5M+15]
    P1l = list(P1)
    high = set()
    for i, a in enumerate(P1l):
        for b in P1l[i + 1:]:
            c = 2 * b - a
            if c >= 4 * M + 1:
                assert c <= 5 * M + 15, (M, 'A3 wall', a, b, c)
                assert c < 6 * M + 1, (M, 'A3 flood-free', c)
                high.add((a, b, c))
    assert a112 == high, (M, 'A3 family', len(a112), len(high))
    # A4 closed form of parents of 4M+s
    from collections import defaultdict
    par = defaultdict(set)
    for (a, b, c) in a112:
        par[c - 4 * M].add((a, b))
    for s in range(1, M + 16):
        closed = set()
        t = 0
        while 2 * t + s <= M + 15:
            closed.add((4 * M - s - 2 * t, 4 * M - t))
            t += 1
        assert par[s] == closed, (M, 'A4', s)
        assert len(par[s]) == (M + 15 - s) // 2 + 1, (M, 'A4 count', s)
    assert par[M + 15] == {(3 * M - 15, 4 * M)}, (M, 'A4 extreme')

    # ---- A5
    a5 = fam.get((0, 2, 2), set())
    closed = set()
    for m in range(1, 8):
        y = 4 * M + m
        for z in range(6 * M + 2 * m, 6 * M + 16):
            closed.add((8 * M + 2 * m - z, y, z))
    assert a5 == closed, (M, 'A5', len(a5), len(closed))
    assert len(a5) == 56, (M, 'A5 count', len(a5))
    for (x, y, z) in a5:
        assert z in F, (M, 'A5 z', z)
        assert 2 * M - 13 <= x <= 2 * M, (M, 'A5 x', x)

    # ---- A6
    a6 = fam.get((1, 2, 2), set())
    closed = set()
    for y in range(4 * M + 1, 5 * M + 8):
        zlo = max(y + 1, 2 * y - 4 * M)
        zhi = min(6 * M + 15, 2 * y - 3 * M + 15)
        for z in range(zlo, zhi + 1):
            closed.add((2 * y - z, y, z))
    assert a6 == closed, (M, 'A6', len(a6), len(closed))
    ftops = {z for (_, _, z) in a6 if z in F}
    assert ftops == F, (M, 'A6 F tops', F - ftops)
    for f in F:
        mids = {y for (_, y, z) in a6 if z == f}
        lo = -(-(f + 3 * M - 15) // 2)          # ceil (x <= 4M... x>=3M-15)
        hi = (f + 4 * M) // 2                   # floor (x >= ... x<=4M)
        assert mids == set(range(lo, hi + 1)), (M, 'A6 F mids', f)

    # ---- A7 straddles
    a7 = fam.get((0, 1, 2), set())
    for (u, y, z) in a7:
        assert (z - u) % 2 == 0, (M, 'A7 parity')
        if z in F:
            assert 2 * y >= 7 * M + 2 and y <= 4 * M, (M, 'A7b y', y)
            assert M + 1 <= u <= 2 * M - 1, (M, 'A7b u', u)
    # F reachability + the y=4M doubling image
    via4M = {z for (u, y, z) in a7 if y == 4 * M and z in F}
    assert via4M == F, (M, 'A7b image', F - via4M)
    assert ({2 * (4 * M) - u for u in range(2 * M - 15, 2 * M)} == F), \
        (M, 'A7b doubling')
    # pressure zone: for y in [3M+1, (7M+14)//2] every u in P0 completes
    for y in range(3 * M + 1, (7 * M + 14) // 2 + 1):
        for u in (M + 1, (3 * M) // 2, 2 * M):
            z = 2 * y - u
            assert 4 * M + 1 <= z <= 6 * M + 15, (M, 'A7c', y, u, z)
    # band edge reach (A7d)
    for u in P0:
        z = 2 * (3 * M - 15) - u
        inside = 4 * M + 1 <= z <= 6 * M + 15
        assert inside == (u <= 2 * M - 31), (M, 'A7d', u)
    assert 2 * (3 * M - 15) - (2 * M - 31) == 4 * M + 1, (M, 'A7d edge')

    # ---- A8 mirror widths
    a222 = fam.get((2, 2, 2), set())
    for c in P2:
        wid = max((e for e in range(0, 2 * M + 16)
                   if (c - e, c, c + e) in a222 or e == 0), default=0)
        assert wid == min(c - (4 * M + 1), 6 * M + 15 - c), (M, 'A8', c)
    assert min(6 * M - (4 * M + 1), 15) == 15, M
    assert {6 * M + e for e in range(1, 16)} == F, (M, 'A8 F')

    # ---- A9
    assert not any(c in F for (_, _, c) in a112), (M, 'A9 (1,1,2)')
    assert not any(y in F for (_, y, _) in a5), (M, 'A9 (0,2,2) mid')
    assert not any(y in F for (_, y, _) in a6), (M, 'A9 (1,2,2) mid')

    print(f'  M={M}: A1..A9 exact-set checks OK '
          f'(|straddle|={len(a7)}, |112|={len(a112)}, |122|={len(a6)})',
          flush=True)


def sweep_inequalities():
    """The pure inequalities at every M = 0 mod 16 in 48..400."""
    for M in range(48, 401, 16):
        assert 5 * M + 15 < 6 * M + 1                      # A3 wall
        assert 2 * (2 * M) - (M + 1) == 3 * M - 1          # A1 cap
        assert 2 * (3 * M - 15) - (2 * M - 31) == 4 * M + 1  # A7d
        assert 3 * M - 15 > 2 * M                          # band in B1
        assert 6 * M + 15 < 8 * M                          # P2 in B2
        assert 6 * M - 15 > 4 * M + 1                      # A8 lower room
    print('  inequality sweep M=48..400 step 16: OK', flush=True)


def main():
    for M in (48, 64, 80):
        check_M(M)
    sweep_inequalities()
    print('e137: ALL CHECKS PASSED', flush=True)


if __name__ == '__main__':
    main()
