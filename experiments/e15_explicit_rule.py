"""Explicit candidate rule for a 3-AP-free permutation of S_A (even dyadic
blocks). key(v) = (epoch, -block, rkey(odd part)); verify by doom-check.
"""
import sys

def block(v):
    k = (v - 1).bit_length()
    if 2 ** k < v:
        k += 1
    return k

def nu(v):
    return (v & -v).bit_length() - 1

def rkey(t, bits=24):
    # bit-reversed key of t with 1-bits earlier: tuple low-to-high, 1 -> 0
    return tuple(0 if (t >> i) & 1 else 1 for i in range(bits))

def key(v):
    K = block(v)
    n = nu(v)
    u = v >> n
    return (K + 3 * n, -K, rkey((u - 1) // 2))

def sa(N):
    return [v for v in range(2, N + 1) if block(v) % 2 == 0]

def doom_check(seq, team, maxv):
    """violations: monotone pair completion placed later, or in team unplaced
    (within maxv); completions beyond maxv assumed handled by block parity."""
    pos = {v: i for i, v in enumerate(seq)}
    teamset = set(team)
    bad = []
    n = len(seq)
    for i in range(n):
        x = seq[i]
        for j in range(i + 1, n):
            y = seq[j]
            z = 2 * y - x
            if z <= 0 or z == y or z > maxv:
                continue
            if z in teamset:
                if z not in pos or pos[z] > j:
                    bad.append((x, y, z))
                    if len(bad) >= 20:
                        return bad
    return bad

if __name__ == "__main__":
    N = 2 ** 14
    team = sa(N)
    seq = sorted(team, key=key)
    bad = doom_check(seq, team, N)
    print(f"N={N}, |S_A|={len(team)}")
    if not bad:
        print("NO VIOLATIONS — explicit rule passes at this scale!")
    else:
        print(f"{len(bad)}+ violations; first ones:")
        for (x, y, z) in bad[:12]:
            print(f"  x={x}(K{block(x)},nu{nu(x)}) y={y}(K{block(y)},nu{nu(y)})"
                  f" z={z}(K{block(z)},nu{nu(z)})")
