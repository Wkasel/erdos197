"""e54: explicit recursive comparator for S_A, mined from law_16_3_witness.json.

Findings feeding this key (see notes/20-within-stage.md):
- The witness's levels are exact PREFIXES of its order (598/654/666).
- Witness stage (band) = min(max(depth(v)-2,0), max((block(v)-4)//2,0))
  -- a CAP by block, not e53's max/arrival form (which mismatches 651/666).
- Within stage 0 (small blocks removed) the order is perfectly class-major
  mod 16 with class order 15,7,3,11,1,9,5,13, 0,8,4,12, 6,14 -- i.e.
  digit order: odd < (0 mod 4) < (6 mod 8) < (2 mod 8), recursing on the
  affine quotients t=(v-1)/2, v/4, (v-6)/8, (v-2)/8 respectively.
- Odd sub-order is self-similar (the t's follow the same class order);
  the deeper fine order in the witness is solver freedom (different classes
  permute their quotients differently), so it is NOT part of the law.
- The wave-1/wave-2 cut splits block-10 depth-4 by m mod 4 (m=(v-2)/16):
  m=3 mod 4 (v=50 mod 64) released before m=1 mod 4 (v=18 mod 64) --
  which is exactly the digit recursion's "3 before 1" again.

Key: K(v) = (wave(v), R(v)) with R the recursive digit string.
Class-closure algebra (z = 2y - x):
  odd/odd -> odd (quotient problem on t), F/F -> F (on v/4),
  S/S -> S (on (v-6)/8), D/D -> D (on (v-2)/8); and for classes a < b in
  the digit order, 2b - a lands in a class <= a's -- so class-major is safe
  and doom-freeness reduces to the quotient problems (self-similarity).
"""
import sys, json
from functools import lru_cache

sys.path.insert(0, __file__.rsplit('/', 1)[0])
from e53_peeling import block, depth, sa, doom_check


def wave(v):
    """Witness stage: depth peeling capped by block release schedule."""
    return min(max(depth(v) - 2, 0), max((block(v) - 4) // 2, 0))


@lru_cache(maxsize=None)
def R(v):
    """Recursive class digits: odd < 0 mod 4 < 6 mod 8 < 2 mod 8, recursing
    on the affine quotient in each branch."""
    out = []
    while v > 0:
        if v % 2 == 1:
            out.append(0); v = (v - 1) // 2
        elif v % 4 == 0:
            out.append(1); v //= 4
        elif v % 8 == 6:
            out.append(2); v = (v - 6) // 8
        else:  # v = 2 mod 8
            out.append(3); v = (v - 2) // 8
    return tuple(out)


def key(v):
    return (wave(v), R(v))


def report(N, keyf, cap=25, label=""):
    team = sa(N)
    seq = sorted(team, key=keyf)
    bad = doom_check(seq, set(team), N, cap=cap)
    print(f"[{label}] N={N} |team|={len(team)} violations: "
          f"{len(bad)}{'+' if len(bad) >= cap else ''}")
    for (x, y, z) in bad[:15]:
        print(f"  x={x}(B{block(x)},d{depth(x)},w{wave(x)}) "
              f"y={y}(B{block(y)},d{depth(y)},w{wave(y)}) "
              f"z={z}(B{block(z)},d{depth(z)},w{wave(z)})")
    return bad


def doom_check_np(seq, N):
    """Vectorized doom check (same semantics as e53.doom_check)."""
    import numpy as np
    n = len(seq)
    pos = np.full(2 * N + 2, n + 1, dtype=np.int64)
    team = np.zeros(2 * N + 2, dtype=bool)
    arr = np.array(seq)
    for i, v in enumerate(seq):
        pos[v] = i
    team[arr] = True
    bad = []
    for j in range(1, n):
        y = seq[j]
        x = arr[:j]
        z = 2 * y - x
        m = (z >= 1) & (z <= N) & (z != y)
        zz = z[m]
        viol = team[zz] & (pos[zz] > j)
        if viol.any():
            for ii in np.nonzero(viol)[0][:5]:
                bad.append((int(x[m][ii]), y, int(zz[ii])))
            if len(bad) > 40:
                return bad
    return bad


def arrival(v):
    return max(0, (block(v) - 4) // 2)


def greedy_chain(N, verbose=True):
    """Round 3: chain-compatible construction. Blocks arrive at band
    arrival(); within the arrived pool, repeatedly place the R-smallest value
    all of whose in-team reflections 2v - x (x already placed) are placed.
    Unplaceable values defer to later bands (empirical defect). Returns
    (order, defect_history)."""
    team = sa(N)
    tset = set(team)
    placed = set()
    order = []
    maxband = arrival(2 ** (N.bit_length() - 1))
    pool = []
    defects = []
    for t in range(maxband + 1):
        pool += [v for v in team if arrival(v) == t]
        pool.sort(key=R)
        progress = True
        while progress:
            progress = False
            for i, v in enumerate(pool):
                ok = True
                for x in order:
                    z = 2 * v - x
                    if z != v and 1 <= z <= N and z in tset and z not in placed:
                        ok = False
                        break
                if ok:
                    order.append(v); placed.add(v); pool.pop(i)
                    progress = True
                    break
        defects.append(sorted(pool))
        if verbose:
            print(f"  band {t}: placed so far {len(order)}, deferred {len(pool)}: "
                  f"{sorted(pool)[:14]}{'...' if len(pool) > 14 else ''}")
    return order, defects


"""RESULTS (2026-08-24):
- R-only (sort all of S_A(N) by the digit string R): 0 doom violations at
  N = 2^12, 2^13, 2^14, 2^16 (43690 values). Explanation: the exact
  reflection law -- at the first digit where R(x), R(y) diverge with digit
  a < b, z = 2y - x takes digit a; all six (a,b) cases check, so
  R(z) < R(y) <=> R(x) < R(y).  Ascending R is therefore self-protecting.
  CAVEAT: R-only is NOT an omega-order over infinite S_A (infinitely many
  values precede any digit>=1 value), so it is a static law, not the final
  permutation.
- (wave, R) with wave = min(max(depth-2,0),(block-4)//2): 25+ violations.
  Family: x a cap-released deep straggler (50,130,162,226,...) with
  depth(x) = depth(y)+1 => depth(z) >= depth(y)+2 => wave(z) > wave(y).
- (arrival, R): 25+ violations. Family: x in an old band with
  R(x) > R(y) for y in the bottom quarter of a new block; then by the
  reflection law R(z) > R(y) with z in y's block.  The same law shows
  descending R fails symmetrically, so NO per-band R-monotone order can
  work: the residual lemma is exactly the interleave/defect discipline.
- greedy R-min chain (place R-smallest value whose placed-reflections are
  complete, defer the rest): deadlocks in band 1 already, e.g. the 3-cycle
  45 -> 35 -> 54 -> 45 induced by sources {9..16} + {63,55,...}.
"""

if __name__ == "__main__":
    for N in (2 ** 12, 2 ** 13):
        report(N, key, label="wave+R")
    # control: R alone (no wave primary) -- static doom-freeness of pure digits
    report(2 ** 12, R, label="R-only")
    report(2 ** 13, R, label="R-only")
    if "--big" in sys.argv:
        for E in (14, 16):
            N = 2 ** E
            team = sa(N)
            seq = sorted(team, key=R)
            bad = doom_check_np(seq, N)
            print(f"[R-only np] N=2^{E} |team|={len(team)} violations: {len(bad)}")
    if "--chain" in sys.argv:
        N = 2 ** 12
        order, defects = greedy_chain(N)
        team = sa(N)
        left = set(team) - set(order)
        print(f"greedy chain N={N}: placed {len(order)}/{len(team)}, "
              f"final deferred: {sorted(left)[:20]}")
        bad = doom_check(order, set(team), N)
        print(f"greedy chain doom violations: {len(bad)}")
        for b in bad[:10]:
            print("  ", b)
