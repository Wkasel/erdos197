"""Rule v2 for S_A: key(v) = (epoch, -block, vdc(odd-part)), with block-bottom
sliver deferral. Doom-check globally."""
import sys

def block(v):
    k = (v - 1).bit_length()
    if 2 ** k < v:
        k += 1
    return k

def nu(v):
    return (v & -v).bit_length() - 1

def vdc(t, bits=26):
    # van der Corput rank: reversed bits of t (LSB becomes MSB), 0-early
    r = 0
    for i in range(bits):
        r = (r << 1) | ((t >> i) & 1)
    return r

def key(v, defer_frac=16):
    K = block(v)
    n = nu(v)
    u = v >> n
    M = 2 ** (K - 1)
    r = v - M
    deferred = 1 if r <= M // defer_frac else 0
    if deferred:
        # place after all normal cells of block K: epoch = K + 3*(K) + small
        return (4 * K, -K, vdc((u - 1) // 2))
    return (K + 3 * n, -K, vdc((u - 1) // 2))

def sa(N):
    return [v for v in range(2, N + 1) if block(v) % 2 == 0]

def doom_check(seq, teamset, maxv, cap=30):
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
    N = 2 ** 13
    team = sa(N)
    seq = sorted(team, key=key)
    bad = doom_check(seq, set(team), N)
    print(f"N={N}, |S_A|={len(team)}, violations: {len(bad)}")
    for (x, y, z) in bad[:15]:
        print(f"  x={x}(K{block(x)},nu{nu(x)}) y={y}(K{block(y)},nu{nu(y)}) z={z}(K{block(z)},nu{nu(z)})")
