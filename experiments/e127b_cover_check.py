"""e127b: brute-force audit of the notes/47 SS0 anchor-covering formulas
and the X-INTERLEAVE every-anchor claim.

Checks:
  1. For random pairs u < w, the set of integer anchors N whose window
     W(N) = (N, 8N] has (u, w) in adjacent blocks equals
        [max(u/2, w/4), min(u, w/2)) u [max(u/4, w/8), min(u/2, w/4))
     intersected with Z (500 random pairs, exhaustive N).
  2. The inversion pairs (4^k, 2*4^k) of the pairwise-swapped powers of
     two cover EVERY anchor N below 4^6.
"""
import math
import random


def covered(u, w, Nmax):
    out = []
    for N in range(1, Nmax):
        b0 = N < u <= 2 * N and 2 * N < w <= 4 * N
        b1 = 2 * N < u <= 4 * N and 4 * N < w <= 8 * N
        if b0 or b1:
            out.append(N)
    return out


def formula(u, w, Nmax):
    s = set()
    a, b = max(u / 2, w / 4), min(u, w / 2)
    s |= set(N for N in range(1, Nmax) if a <= N < b)
    a2, b2 = max(u / 4, w / 8), min(u / 2, w / 4)
    s |= set(N for N in range(1, Nmax) if a2 <= N < b2)
    return sorted(s)


def main():
    random.seed(1)
    bad = 0
    for _ in range(500):
        u = random.randint(2, 800)
        w = random.randint(u + 1, min(8 * u, 3000))
        if covered(u, w, 4000) != formula(u, w, 4000):
            bad += 1
    assert bad == 0, f'{bad} formula mismatches'
    print('PASS: covering formulas exact on 500 random pairs')
    allN = set()
    for k in range(1, 8):
        allN |= set(covered(4 ** k, 2 * 4 ** k, 4 ** 7))
    missing = [N for N in range(1, 4 ** 6) if N not in allN]
    assert not missing, f'X-INTERLEAVE misses anchors {missing[:5]}'
    print('PASS: X-INTERLEAVE inversions cover every anchor < 4^6')


if __name__ == '__main__':
    main()
