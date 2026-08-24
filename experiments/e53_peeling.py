"""The class-peeling comparator: explicit candidate global order for S_A.

stage(v) = max(depth(v) - 2, (block(v) - 4) / 2)  [arrival capping]
  depth(v) = largest j >= 1 with v ≡ 2 (mod 2^j), else 0 (odd v: depth 0)
     note: v ≡ 2 mod 2 means v even: depth >= 1 for even v; odd v depth 0.
Within stage: recursive sub-key on the quotient (v-2)/2^depth-ish; first
attempt: recurse with the SAME comparator on v' = v >> 1 ... to refine from
data. Start simple: within-stage key = (block, then vdC of value) and check
where violations arise; iterate.
"""
import sys, json

def block(v):
    k = (v - 1).bit_length()
    if 2 ** k < v: k += 1
    return k

def sa(N):
    return [v for v in range(2, N + 1) if block(v) % 2 == 0]

def depth(v):
    j = 0
    while v % (2 ** (j + 1)) == 2 % (2 ** (j + 1)):
        j += 1
    return j

def stage(v):
    d = depth(v)
    arr = max(0, (block(v) - 4 + 1) // 2)
    return max(d - 2, arr)

def vdc(t, bits=24):
    r = 0
    for i in range(bits):
        r = (r << 1) | ((t >> i) & 1)
    return r

def key(v):
    return (stage(v), block(v), vdc(v))

def doom_check(seq, teamset, maxv, cap=25):
    pos = {v: i for i, v in enumerate(seq)}
    bad = []
    n = len(seq)
    for i in range(n):
        x = seq[i]
        for j in range(i + 1, n):
            y = seq[j]
            z = 2 * y - x
            if z <= 0 or z == y or z > maxv: continue
            if z in teamset and (z not in pos or pos[z] > j):
                bad.append((x, y, z))
                if len(bad) >= cap: return bad
    return bad

if __name__ == "__main__":
    N = 2 ** 12
    team = sa(N)
    seq = sorted(team, key=key)
    bad = doom_check(seq, set(team), N)
    print(f"N={N} violations: {len(bad)}{'+' if len(bad)>=25 else ''}")
    for (x, y, z) in bad[:12]:
        print(f"  x={x}(B{block(x)},d{depth(x)},s{stage(x)}) "
              f"y={y}(B{block(y)},d{depth(y)},s{stage(y)}) "
              f"z={z}(B{block(z)},d{depth(z)},s{stage(z)})")
