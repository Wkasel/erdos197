"""e126c: how much of the Case-2 coupled core is PURE sumset combinatorics?

The forced structure of the two-seam gadget (notes/45 Part C3) is the
cross-triple hypergraph H = {(u, y, 2y-u) : u in B0, y in B1,
2y-u in B2}: under double non-procrastination a monochromatic cross
triple is position-forced increasing.  The escape condition per color
class C is (2Y - U) cap B2 cap C = empty.  The rest of the gadget is
the in-block order theory.

This diagnostic solves the PURE 2-coloring problem on a support S:
  - no cross triple inside S monochromatic (either color),
  - each team >= c_i values in block i (over S),
  - NO order variables at all.
If UNSAT: the core is purely a sumset/counting statement — the hand
schema needs no order theory beyond the seam forcing itself.
If SAT: prints the surviving pure witness (the dodge the order theory
must kill) — the exact residual obligation of the hand schema.

Also reports the cross-triple census of S (counts, per-value degrees in
anchor coordinates) — the skeleton the MUS retains.

Usage: e126c_pure_sumset.py M c0 c1 c2 [supportfile.json]
(no supportfile: run on the FULL window — baseline.)
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), 'data')

from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical195


def cross_triples(S, M):
    Ss = set(S)
    B0 = [v for v in S if M < v <= 2 * M]
    B1 = [v for v in S if 2 * M < v <= 4 * M]
    out = []
    for u in B0:
        for y in B1:
            z = 2 * y - u
            if 4 * M < z <= 8 * M and z in Ss:
                out.append((u, y, z))
    return out


def run(M, bounds, S=None):
    if S is None:
        S = list(range(M + 1, 8 * M + 1))
    S = sorted(S)
    T = cross_triples(S, M)
    blocks = (('B0', M, 2 * M), ('B1', 2 * M, 4 * M), ('B2', 4 * M, 8 * M))
    ai = {v: i + 1 for i, v in enumerate(S)}
    cls = []
    for (u, y, z) in T:
        cls.append([-ai[u], -ai[y], -ai[z]])
        cls.append([ai[u], ai[y], ai[z]])
    tid = len(S)
    for bi, (name, lo, hi) in enumerate(blocks):
        blk = [v for v in S if lo < v <= hi]
        bnd = bounds[bi]
        if bnd <= 0 or not blk:
            continue
        for sign in (1, -1):
            enc = CardEnc.atleast(lits=[sign * ai[v] for v in blk],
                                  bound=min(bnd, len(blk)), top_id=tid,
                                  encoding=EncType.seqcounter)
            tid = max(tid, enc.nv)
            cls += enc.clauses
    with Cadical195(bootstrap_with=cls) as s:
        sat = s.solve()
        model = s.get_model() if sat else None
    print(f'M={M} bounds={bounds} |S|={len(S)} cross_triples={len(T)}: '
          f'PURE-SUMSET {"SAT" if sat else "UNSAT"}')
    # census: per-value cross-triple degree
    from collections import Counter
    deg = Counter()
    for t in T:
        for v in t:
            deg[v] += 1
    for name, lo, hi in blocks:
        blk = [v for v in S if lo < v <= hi]
        print(f'  {name}: n={len(blk)} degs={[deg[v] for v in blk]}')
    if sat:
        A = sorted(v for v in S if model[ai[v] - 1] > 0)
        B = sorted(v for v in S if v not in set(A))
        for name, lo, hi in blocks:
            a = [v for v in A if lo < v <= hi]
            b = [v for v in B if lo < v <= hi]
            print(f'  {name} pure-dodge: A={a}  B={b}')
    return sat


if __name__ == '__main__':
    M = int(sys.argv[1])
    bounds = (int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
    S = None
    if len(sys.argv) > 5:
        with open(sys.argv[5]) as f:
            S = json.load(f)['support']
    run(M, bounds, S)
