"""Erdős #197 — dyadic reduction, per-block search.

For block B = (M, 2M] (M = 2^{k-1}) find a permutation with:
  (a) no monotone 3-term AP (as a subsequence of the arrangement);
  (b) for every pair y < z in B with 2y - z in zones Z: z precedes y,
      where Z = union of same-parity dyadic blocks below M (team's own
      earlier territory), optionally including {1}.

Backtracking: build the sequence left to right. State:
  - placed: set of placed values, in order
  - banned: values that may no longer be placed (would complete a
    monotone 3-AP with an already-placed ordered pair)
  - forced: for each value v, the set of values that must precede it
    (from (b): z must precede y  =>  y requires z placed first)

Placing v at the next position:
  * legal iff v not banned and all required-predecessors of v placed
  * afterwards, for each placed u < v: ban 2v - u (if in B)  [u..v increasing pair]
                for each placed u > v: ban 2v - u (if in B)  [u..v decreasing pair]
    (both cases: the AP completion in the same direction)
"""
import sys
from functools import lru_cache

sys.setrecursionlimit(100000)


def zones(M, include_one):
    """Team's own territory below M: same-parity dyadic blocks (M/4,M/2], (M/16,M/8], ..."""
    Z = set()
    hi = M // 2
    lo = M // 4
    while lo >= 1:
        Z.update(range(lo + 1, hi + 1))
        hi //= 4
        lo //= 4
    if include_one:
        Z.add(1)
    return Z


def forced_pairs(M, Z):
    """(b): pairs y < z in B with 2y - z in Z  =>  z must precede y.
    Returns dict need[y] = set of z that must be placed before y."""
    B = range(M + 1, 2 * M + 1)
    need = {v: set() for v in B}
    for y in B:
        for z in range(y + 1, 2 * M + 1):
            if (2 * y - z) in Z:
                need[y].add(z)
    return need


def search(M, Z, order_hint=None, node_cap=20_000_000):
    B = list(range(M + 1, 2 * M + 1))
    need = forced_pairs(M, Z)
    n = len(B)
    seq = []
    placed = set()
    banned_count = {v: 0 for v in B}   # how many active bans on v
    nodes = 0

    # heuristic value order: values with many forced successors later;
    # default: try to follow "high half first" bias
    if order_hint is None:
        order_hint = sorted(B, key=lambda v: -v)

    def candidates():
        cs = []
        for v in order_hint:
            if v in placed or banned_count[v] > 0:
                continue
            if not need[v] <= placed:
                continue
            cs.append(v)
        return cs

    def place(v):
        newly = []
        for u in seq:
            w = 2 * v - u  # completion of (u, v) in the same direction
            if M < w <= 2 * M and w not in placed:
                banned_count[w] += 1
                newly.append(w)
        seq.append(v)
        placed.add(v)
        return newly

    def unplace(v, newly):
        seq.pop()
        placed.discard(v)
        for w in newly:
            banned_count[w] -= 1

    def bt():
        nonlocal nodes
        nodes += 1
        if nodes > node_cap:
            raise TimeoutError
        if len(seq) == n:
            return True
        for v in candidates():
            newly = place(v)
            if bt():
                return True
            unplace(v, newly)
        return False

    try:
        ok = bt()
    except TimeoutError:
        return None, nodes
    return (seq[:] if ok else False), nodes


def verify(M, Z, seq):
    """Independent check of (a) and (b)."""
    pos = {v: i for i, v in enumerate(seq)}
    B = set(seq)
    assert B == set(range(M + 1, 2 * M + 1))
    # (a) monotone 3-AP
    for y in seq:
        for d in range(1, M):
            x, z = y - d, y + d
            if x in B and z in B:
                if pos[x] < pos[y] < pos[z] or pos[x] > pos[y] > pos[z]:
                    return f"3-AP {x},{y},{z}"
    # (b)
    for y in B:
        for z in B:
            if z > y and (2 * y - z) in Z:
                if pos[z] > pos[y]:
                    return f"(b) violated for y={y}, z={z}, x={2*y-z}"
    return None


if __name__ == "__main__":
    import time
    for include_one in (False, True):
        print(f"=== include_one={include_one} ===")
        k = 1
        while True:
            M = 2 ** k
            if M > 512:
                break
            Z = zones(M, include_one)
            t0 = time.time()
            res, nodes = search(M, Z)
            dt = time.time() - t0
            if res is None:
                print(f"M={M}: TIMEOUT after {nodes} nodes ({dt:.1f}s)")
                break
            if res is False:
                print(f"M={M}: NO SOLUTION ({nodes} nodes, {dt:.1f}s)")
                break
            err = verify(M, Z, res)
            status = "VERIFIED" if err is None else f"BUG: {err}"
            print(f"M={M}: found ({nodes} nodes, {dt:.1f}s) {status}")
            if M <= 32:
                print("   ", res)
            k += 1
