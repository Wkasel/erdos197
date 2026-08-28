"""e159d: MONSTER-SCALE H-DICH arithmetic layer (notes/57 SS2/SS4/SS5)
(FRONT MEGA-SCHEMA, notes/63).

The notes/57 DICH proof splits into a uniform ARITHMETIC layer
(Lemmas FI / ANCHOR / COLL, the H0-H2 case-tree interval collisions,
the Lemma-SP staircase-kill inequality) and a per-scale CATALOGUE
layer (F1-F4: alpha, self-service, admissible windows — these need
the fan catalogue D(M), whose construction is Theta(M^2) closures and
is out of reach at 2^13+; they are the acknowledged GAP-DICH rows).
This checker stresses the ARITHMETIC layer at monster scales:

  FI   — for EVERY z in P2: the forced interval I(z) re-derived from
         the u-range (independent derivation), then all Lemma-FI
         claims asserted: contiguity, anchor iff s <= M-31, exact
         lengths ((s+31)//2 / (s+32)//2 low, m mid, >= m-8 tail),
         ell >= 16, n_c >= 8 with n_c = 8 only at s in {1, 2M+15}
         (odd) / {2} (even).  Stratified honest brute force (looping
         actual u in P0) on a deterministic z-sample.
  A2   — pair mass f_c(D) >= 9 for every 2-element D: monotonicity
         reduction (n_c(I1 u I2) >= max part mass; = 8 impossible
         unless both members are 8-mass singletons) + the single
         surviving worst pair {4M+1, 6M+15} computed exactly + a
         randomized exact-pair sample per class.
  COLL — H1 two-sided collision closure: for every admissible
         minimum s0 <= M-1 (both classes) the interval bottom lies
         in [3M-15, 3M] and length >= 16; global min(top) >=
         max(bottom) ==> EVERY two admissible forced intervals
         intersect (the H1 contradiction), verified numerically.
  SP   — staircase kill: with the index map sigma(i+j) = 5M/2+i+j-eps
         re-derived and boundary-sampled, w1 = m-15+eps, n = m+8/m+7:
         hidden-staircase forced mass m+n-w1 == m+22 > m+14 (both
         classes), and band-top slack 3m >= max sum.

Run: .venv/bin/python experiments/e159d_mega_dich.py M [bf_stride]
     bf_stride: brute-force z-sample stride (0 = every z)
Output: data/e159d_mega_dich.json (appended per scale)
"""
import json
import os
import random
import resource
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '..', 'data', 'e159d_mega_dich.json')


def fi_closed(M, z):
    """Independent forced-interval derivation from the u-range of P0:
    same-class u in [M+1, 2M], mids (u+z)/2 clipped to the band."""
    c = z % 2
    u_min = M + 1 if (M + 1) % 2 == c else M + 2
    u_max = 2 * M if (2 * M) % 2 == c else 2 * M - 1
    lo = max(3 * M - 15, (u_min + z) // 2)
    hi = min(4 * M, (u_max + z) // 2)
    return lo, hi


def class_count(lo, hi, c):
    if lo > hi:
        return 0
    first = lo if lo % 2 == c else lo + 1
    if first > hi:
        return 0
    return (hi - first) // 2 + 1


def brute_interval(M, z):
    c = z % 2
    mids = sorted((u + z) // 2 for u in range(M + 1, 2 * M + 1)
                  if u % 2 == c and 3 * M - 15 <= (u + z) // 2 <= 4 * M)
    return mids


def check_M(M, bf_stride):
    m = M // 2
    P2 = range(4 * M + 1, 6 * M + 16)
    t0 = time.time()

    # ---------- FI: all z, arithmetic ----------
    for z in P2:
        s = z - 4 * M
        c = z % 2
        lo, hi = fi_closed(M, z)
        assert lo <= hi, (M, z, 'FI empty')
        ell = hi - lo + 1
        ncl = class_count(lo, hi, c)
        anchored = (lo == 3 * M - 15)
        assert anchored == (s <= M - 31), (M, z, 'FI anchor')
        if s <= M - 31:
            want = (s + 31) // 2 if c == 1 else (s + 32) // 2
            assert ell == want, (M, z, 'FI low len', ell, want)
        elif s <= 2 * M:
            assert ell == m, (M, z, 'FI mid len', ell)
        else:
            assert ell >= m - 8, (M, z, 'FI tail len', ell)
        assert ell >= 16 and ncl >= 8, (M, z, 'FI floor', ell, ncl)
        if ncl == 8:
            ok8 = (s in (1, 2 * M + 15)) if c == 1 else (s == 2)
            assert ok8, (M, z, 'FI 8-mass', s, c)
    t_fi = time.time() - t0

    # ---------- FI: stratified honest brute force ----------
    t0 = time.time()
    zs = list(P2)
    if bf_stride == 0:
        sample = zs
    else:
        crit = [z for z in zs
                if (z - 4 * M) <= 64
                or abs((z - 4 * M) - (M - 31)) <= 40
                or (z - 4 * M) >= 2 * M - 20]
        sample = sorted(set(crit) | set(zs[::bf_stride]))
    for z in sample:
        mids = brute_interval(M, z)
        lo, hi = fi_closed(M, z)
        assert mids and mids == list(range(mids[0], mids[-1] + 1)), \
            (M, z, 'BF contiguity')
        assert (mids[0], mids[-1]) == (lo, hi), (M, z, 'BF endpoints')
        assert sum(1 for v in mids if v % 2 == z % 2) \
            == class_count(lo, hi, z % 2), (M, z, 'BF class count')
    t_bf = time.time() - t0

    # ---------- A2: pair mass >= 9 ----------
    t0 = time.time()
    # (i) singleton masses: 8-mass members enumerated in the FI loop
    #     above; monotonicity: I1 subset of union => n_c(union) >=
    #     max part.  A 2-element D can only have mass 8 if BOTH
    #     members are 8-mass singletons of one class.
    # (ii) odd class has two 8-mass singletons: the surviving pair.
    for c, eight in ((1, (4 * M + 1, 6 * M + 15)), (0, (4 * M + 2,))):
        if len(eight) >= 2:
            z1, z2 = eight
            l1, h1 = fi_closed(M, z1)
            l2, h2 = fi_closed(M, z2)
            n_union = class_count(l1, h1, c) + class_count(l2, h2, c) \
                - class_count(max(l1, l2), min(h1, h2), c)
            assert n_union >= 9, (M, c, 'A2 worst pair', n_union)
    # (iii) randomized exact pair sample, both classes
    rng = random.Random(197)
    for c in (0, 1):
        zc = [z for z in P2 if z % 2 == c]
        for _ in range(100000):
            z1, z2 = rng.sample(zc, 2)
            l1, h1 = fi_closed(M, z1)
            l2, h2 = fi_closed(M, z2)
            n_union = class_count(l1, h1, c) + class_count(l2, h2, c) \
                - class_count(max(l1, l2), min(h1, h2), c)
            assert n_union >= 9, (M, c, z1, z2, 'A2 sample', n_union)
    t_a2 = time.time() - t0

    # ---------- COLL / H1 collision closure ----------
    t0 = time.time()
    min_top, max_bot = None, None
    for c in (0, 1):
        for s0 in range(1 if c else 2, M, 2):     # admissible s0 <= M-1
            z0 = 4 * M + s0
            lo, hi = fi_closed(M, z0)
            assert 3 * M - 15 <= lo <= 3 * M, (M, c, s0, 'H1 bottom', lo)
            if s0 > M - 31:                       # surviving-mid form
                delta = -(-(s0 - (M - 31)) // 2)
                assert lo == 3 * M - 15 + delta and delta <= 15, \
                    (M, c, s0, 'H1 delta', lo, delta)
                assert hi - lo + 1 == m, (M, c, s0, 'H1 mid len')
            assert hi - lo + 1 >= 16, (M, c, s0, 'H1 len floor')
            min_top = hi if min_top is None else min(min_top, hi)
            max_bot = lo if max_bot is None else max(max_bot, lo)
    assert min_top >= max_bot, (M, 'H1 collision', min_top, max_bot)
    t_h1 = time.time() - t0

    # ---------- SP: staircase kill ----------
    t0 = time.time()
    for eps, c in ((1, 1), (0, 0)):               # odd: eps=1, even: eps=0
        n = m + 8 if c == 1 else m + 7
        # sigma boundary samples: u = M+2i-eps, z = 4M+2j-eps,
        # midpoint = 5M/2 + i + j - eps; band window on t = i+j:
        # [m-15+eps, 3m+eps] intersect achievable sums [2, m+n]
        for (i, j) in ((1, 1), (1, n), (m, 1), (m, n),
                       (m // 2, n // 2)):
            u = M + 2 * i - eps
            z = 4 * M + 2 * j - eps
            assert M + 1 <= u <= 2 * M and 4 * M + 1 <= z <= 6 * M + 15, \
                (M, c, i, j, 'SP index range')
            mid = (u + z) // 2
            t_sum = i + j
            in_band = 3 * M - 15 <= mid <= 4 * M
            assert in_band == (m - 15 + eps <= t_sum <= 3 * m + eps), \
                (M, c, i, j, 'SP sigma window')
        w1 = m - 15 + eps
        assert m + n - w1 == m + 22, (M, c, 'SP mass', m + n - w1)
        assert m + 22 > m + 14, (M, c)
        assert 3 * m + eps >= m + n, (M, c, 'SP band-top slack')
    t_sp = time.time() - t0

    return {'fi_s': round(t_fi, 2), 'bf_s': round(t_bf, 2),
            'bf_sample': len(sample), 'a2_s': round(t_a2, 2),
            'h1_s': round(t_h1, 2), 'sp_s': round(t_sp, 4)}


def main():
    M = int(sys.argv[1])
    stride = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    out = []
    if os.path.exists(DATA):
        out = json.load(open(DATA))
    t0 = time.time()
    try:
        row = check_M(M, stride)
        row.update({'M': M, 'ok': True, 'total_s': round(time.time() - t0, 2)})
    except AssertionError as ex:
        row = {'M': M, 'ok': False, 'err': repr(ex.args[:4])}
    ru = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    row['peak_rss_mb'] = round(
        ru / 2 ** 20 if sys.platform == 'darwin' else ru / 1024, 1)
    out.append(row)
    json.dump(out, open(DATA, 'w'), indent=1)
    print(row, flush=True)
    if not row['ok']:
        sys.exit(1)


if __name__ == '__main__':
    main()
