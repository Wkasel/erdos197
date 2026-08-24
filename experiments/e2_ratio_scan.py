"""Erdős #197 — generalized alternating interval partitions.

Partition Z+ into consecutive blocks (S_{k-1}, S_k], alternating teams,
with 2*S_k <= S_{k+1} (locality: upward completions of a team's block land
in the other team's next block, never in the team's own future).

Per-block feasibility for the block (lo, hi] of a team whose own past
territory is Z (union of its earlier blocks):
  (a) arrangement has no monotone 3-AP;
  (b) for y < z in block with 2y - z in Z: z precedes y.

We scan growth schemes S_{k+1} = ceil(r * S_k) (and (a,b)-alternating
ratios) and test blocks up to a value cap, reporting which schemes
survive how far.
"""
import math
import sys
import time

sys.setrecursionlimit(100000)


def make_blocks(ratios, s0=2, cap=100000):
    """ratios: function k -> ratio for step k. Blocks[i] = (lo, hi]."""
    S = [1, s0]
    while S[-1] < cap:
        nxt = math.ceil(ratios(len(S) - 1) * S[-1])
        if nxt < 2 * S[-1]:
            nxt = 2 * S[-1]
        S.append(nxt)
    return S  # block k (1-indexed) = (S[k-1], S[k]]


def block_search(lo, hi, Z, node_cap=3_000_000):
    """Find arrangement of (lo, hi] with (a)+(b). Returns seq | False | None(timeout)."""
    B = list(range(lo + 1, hi + 1))
    n = len(B)
    need = {v: set() for v in B}
    for y in B:
        # 2y - z in Z  =>  z = 2y - x for x in Z
        for x in Z:
            z = 2 * y - x
            if y < z <= hi:
                need[y].add(z)
    seq, placed = [], set()
    banned = {v: 0 for v in B}
    nodes = 0

    def bt():
        nonlocal nodes
        nodes += 1
        if nodes > node_cap:
            raise TimeoutError
        if len(seq) == n:
            return True
        for v in sorted(B, key=lambda t: -t):
            if v in placed or banned[v] > 0 or not need[v] <= placed:
                continue
            newly = []
            for u in seq:
                w = 2 * v - u
                if lo < w <= hi and w not in placed:
                    banned[w] += 1
                    newly.append(w)
            seq.append(v)
            placed.add(v)
            if bt():
                return True
            seq.pop()
            placed.discard(v)
            for w in newly:
                banned[w] -= 1
        return False

    try:
        ok = bt()
    except TimeoutError:
        return None, nodes
    return (seq[:] if ok else False), nodes


def test_scheme(name, S, val_cap=100000, verbose=True):
    """Alternating assignment: block k -> team k%2. Test every block."""
    results = []
    for k in range(1, len(S)):
        lo, hi = S[k - 1], S[k]
        if hi > val_cap:
            break
        # team's own past blocks: k-2, k-4, ...
        Z = set()
        j = k - 2
        while j >= 1:
            Z.update(range(S[j - 1] + 1, S[j] + 1))
            j -= 2
        if k % 2 == 1:
            Z.add(1)  # team of block 1 also owns the value 1 (convention)
        t0 = time.time()
        res, nodes = block_search(lo, hi, Z)
        dt = time.time() - t0
        tag = "ok" if res not in (False, None) else ("FAIL" if res is False else "timeout")
        results.append((k, lo, hi, tag))
        if verbose:
            print(f"  block {k} ({lo},{hi}] |Z|={len(Z)}: {tag} ({nodes} nodes, {dt:.1f}s)")
        if res is False:
            break
    return results


if __name__ == "__main__":
    cap = 3000
    # constant-ratio schemes
    for r in [2.0, 2.2, 2.5, 2.8, 3.0, 3.5, 4.0]:
        S = make_blocks(lambda k: r, s0=2, cap=cap)
        print(f"scheme r={r}: S={S[:10]}...")
        rs = test_scheme(f"r={r}", S, val_cap=cap)
        worst = rs[-1]
        print(f"  => last: block {worst[0]} {worst[3]}")
    # alternating-ratio schemes (a for one team's incoming block, b for other)
    for a, b in [(2.0, 3.0), (3.0, 2.0), (2.0, 4.0), (4.0, 2.0), (2.5, 3.5)]:
        S = make_blocks(lambda k, a=a, b=b: a if k % 2 == 0 else b, s0=2, cap=cap)
        print(f"scheme a,b={a},{b}: S={S[:10]}...")
        rs = test_scheme(f"ab={a},{b}", S, val_cap=cap)
        worst = rs[-1]
        print(f"  => last: block {worst[0]} {worst[3]}")
