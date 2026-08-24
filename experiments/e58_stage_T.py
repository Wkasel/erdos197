"""Candidate omega-order T on S_A: stages + within-stage R-order.

stage(v) = max(depth(v) - DSHIFT, block(v)//2) where depth(v) = v2(v - 2)
(2-adic valuation; v = 2 gets depth INF -> but 2 is not in S_A: blocks are
(2^{k-1}, 2^k] for k even, smallest is (2,4] = {3,4}).
Within a stage, order by the R-comparator digit string (lexicographic).
Exact at horizons N = 4^m: completions of pairs <= N land <= 2N in the odd
block (N, 2N], outside S_A -> the triple set inside [1,N] is complete.

Reports monotone-3AP violations of T. Args: m [DSHIFT]  (N = 4^m).
"""
import sys
import numpy as np

def block(v):
    k = (v - 1).bit_length()
    if 2 ** k < v: k += 1
    return k

def rdigits(v):
    d = []
    while v > 2:
        if v % 2 == 1:
            d.append(0); v = (v - 1) // 2
        elif v % 4 == 0:
            d.append(1); v = v // 4
        elif v % 8 == 6:
            d.append(2); v = (v - 6) // 8
        else:  # v % 8 == 2
            d.append(3); v = (v - 2) // 8
    d.append(v)  # terminal 1 or 2
    return tuple(d)

def depth(v):
    w = v - 2
    if w == 0: return 10 ** 9
    return (w & -w).bit_length() - 1

def main(m, dshift=2):
    N = 4 ** m
    V = [v for v in range(2, N + 1) if block(v) % 2 == 0]
    stg = {v: max(depth(v) - dshift, block(v) // 2) for v in V}
    order = sorted(V, key=lambda v: (stg[v], rdigits(v)))
    pos = np.full(N + 1, -1, dtype=np.int64)
    for i, v in enumerate(order):
        pos[v] = i
    inset = pos >= 0
    viol = 0
    examples = []
    for d in range(1, N // 2 + 1):
        y = np.arange(d + 1, N - d + 1)
        ok = inset[y] & inset[y - d] & inset[y + d]
        y = y[ok]
        if len(y) == 0: continue
        px, py, pz = pos[y - d], pos[y], pos[y + d]
        mono = ((px < py) & (py < pz)) | ((px > py) & (py > pz))
        c = int(mono.sum())
        viol += c
        if c and len(examples) < 12:
            idx = np.nonzero(mono)[0][:12 - len(examples)]
            for i in idx:
                examples.append((int(y[i] - d), int(y[i]), int(y[i] + d)))
    print(f"N=4^{m} DSHIFT={dshift}: n={len(V)} stages<= {max(stg.values())} "
          f"violations={viol}", flush=True)
    for e in examples:
        x, y, z = e
        print(f"  viol {e} stages=({stg[x]},{stg[y]},{stg[z]}) "
              f"depths=({depth(x)},{depth(y)},{depth(z)})", flush=True)

if __name__ == "__main__":
    m = int(sys.argv[1])
    ds = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    main(m, ds)
