"""Explicit round-key schedule for S_A, doom-checked.

key(v) = (round, subkey) where:
  round(v) = block(v)/2 + rank8(v mod 8)   [rank8 over order 4,0,6,2,7,3,5,1]
  within round: recursive refinement mod 64 by the same principle + block order
Sliver deferral: values within M/16 of block bottom get round += 2 (tunable).
"""
import sys

RANK8 = {4: 0, 0: 1, 6: 2, 2: 3, 7: 4, 3: 5, 5: 6, 1: 7}

def block(v):
    k = (v - 1).bit_length()
    if 2 ** k < v: k += 1
    return k

def sa(N):
    return [v for v in range(2, N + 1) if block(v) % 2 == 0]

def rank64(v):
    # refine: within class c mod 8, order sub-classes (c + 8j mod 64) by the
    # absorbing principle: reuse pattern via (v div 8) mod 8 mapped through RANK8
    # of a derived class; simplest coherent choice: vdC on j = (v mod 64 - v mod 8)//8
    j = (v % 64) // 8
    # bit-reversal of j (3 bits)
    return ((j & 1) << 2) | (j & 2) | ((j & 4) >> 2)

def key(v, defer_frac=16, defer_rounds=2):
    K = block(v)
    M = 2 ** (K - 1)
    r = K // 2 + RANK8[v % 8]
    if v - M <= M // defer_frac:
        r += defer_rounds
    return (r, rank64(v), K, v)

def doom_check(seq, teamset, maxv, cap=40):
    pos = {v: i for i, v in enumerate(seq)}
    bad = []
    n = len(seq)
    for i in range(n):
        x = seq[i]
        for j in range(i + 1, n):
            y = seq[j]
            z = 2 * y - x
            if z <= 0 or z == y or z > maxv:
                continue
            if z in teamset and (z not in pos or pos[z] > j):
                bad.append((x, y, z))
                if len(bad) >= cap:
                    return bad
    return bad

if __name__ == "__main__":
    N = 2 ** 12
    team = sa(N)
    seq = sorted(team, key=key)
    bad = doom_check(seq, set(team), N)
    print(f"N={N} |S_A|={len(team)} violations: {len(bad)}{'+' if len(bad)>=40 else ''}")
    for (x, y, z) in bad[:15]:
        print(f"  x={x}(B{block(x)},c{x%8}) y={y}(B{block(y)},c{y%8}) z={z}(B{block(z)},c{z%8})")
