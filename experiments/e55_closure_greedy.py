"""ω-ification via closure-batch greedy guided by R.

R-comparator (from notes/20): digits: odd→0, ≡0 mod4→1, ≡6 mod8→2, ≡2 mod8→3.
Duties: values of S_A in increasing order. To place duty v: first place
(recursively) every unplaced value that MUST precede v, in R-order:
  requirement: if some placed x makes (x, v) a monotone pair whose completion
  z is in S_A and unplaced, then z must come before v (else doom when z lands).
  Requirements are computed against the CURRENT placed set + v's own pending
  batch (fixed-point iteration).
Then doom-check the whole constructed prefix exactly.
"""
import sys

def block(v):
    k = (v - 1).bit_length()
    if 2 ** k < v: k += 1
    return k

def sa(N):
    return [v for v in range(2, N + 1) if block(v) % 2 == 0]

def rkey(v, depth=40):
    digits = []
    cur = v
    for _ in range(depth):
        if cur <= 0: break
        if cur % 2 == 1:
            digits.append(0); cur = (cur - 1) // 2
        elif cur % 4 == 0:
            digits.append(1); cur = cur // 4
        elif cur % 8 == 6:
            digits.append(2); cur = (cur - 6) // 8
        elif cur % 8 == 2:
            digits.append(3); cur = (cur - 2) // 8
        else:
            digits.append(4); break
    return tuple(digits)

def construct(N):
    team = sa(N)
    teamset = set(team)
    placed = []
    placedset = set()
    pos = {}

    def requirements(v, pending):
        """unplaced values that must precede v given placed ∪ pending precede v."""
        req = set()
        ctx = placedset | pending
        for x in ctx:
            if x == v: continue
            z = 2 * v - x  # completion of pair (x placed-before, v)
            if 0 < z <= N and z != v and z in teamset and z not in ctx:
                req.add(z)
        return req

    def place_with_closure(v):
        if v in placedset:
            return True
        batch = {v}
        # fixed point: requirements of everything in the batch
        while True:
            new = set()
            for u in batch:
                for r in requirements(u, batch - {u}):
                    if r not in batch:
                        new.add(r)
            if not new:
                break
            batch |= new
            if len(batch) > 5000:
                return False  # closure explosion
        # place batch in dependency order (must-precede edges), R breaks ties
        # edge u -> w  means u must precede w:
        # for w in batch, x in placed∪batch with x≠w: z = 2w−x in batch ⟹ z→w
        edges = {u: set() for u in batch}
        indeg = {u: 0 for u in batch}
        ctx = placedset | batch
        for w in batch:
            for x in ctx:
                if x == w: continue
                z = 2 * w - x
                if z in batch and z != w and z != x:
                    if w not in edges[z]:
                        edges[z].add(w)
                        indeg[w] += 1
        import heapq
        avail = [(rkey(u), u) for u in batch if indeg[u] == 0]
        heapq.heapify(avail)
        done = 0
        while avail:
            _, u = heapq.heappop(avail)
            if u not in placedset:
                pos[u] = len(placed)
                placed.append(u)
                placedset.add(u)
            done += 1
            for w in edges[u]:
                indeg[w] -= 1
                if indeg[w] == 0:
                    heapq.heappush(avail, (rkey(w), w))
        if done < len(batch):
            cyc = [u for u in batch if indeg[u] > 0]
            print(f"CYCLE in batch (duty batch size {len(batch)}): stuck {sorted(cyc)[:10]}", flush=True)
            return False
        return True

    for i, v in enumerate(team):
        if not place_with_closure(v):
            print(f"CLOSURE EXPLOSION at duty {v}", flush=True)
            return None
        if i % 500 == 0:
            print(f"duty {v}: placed {len(placed)}", flush=True)
    return placed

def doom_check(seq, teamset, maxv, cap=20):
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
    seq = construct(N)
    if seq is None:
        sys.exit(1)
    team = set(sa(N))
    print(f"constructed n={len(seq)}; doom-checking...", flush=True)
    bad = doom_check(seq, team, N)
    print(f"violations: {len(bad)}{'+' if len(bad)>=20 else ''}")
    for t in bad[:10]:
        print("  ", t)
    if not bad:
        import json
        json.dump(seq, open('data/omega_order_4096.json', 'w'))
        print("SAVED — candidate ω-order constructed cleanly at 4096!!")
