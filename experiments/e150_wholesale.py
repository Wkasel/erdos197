"""e150: the two wholesale arm-kill lemmas  (notes/56 SS4b).

Part A — P-ARM(M): under the parity hatch (Phi = 0, WLOG U_A = odds
  of P0, U_B = evens, Z_A = evens of P2, Z_B = odds; Lemma PH), with
  the band coloring FREE (band bounds >= 2 per team), the block-0 and
  block-1 theories of both teams — encoded as genuine guarded order
  theories, not patterns — are jointly inconsistent: the hybrid
  instance is UNSAT.  This is the notes/55 SS5.4 "mixed band => at
  least as dead" statement in machine form; it contains Lemma PAR +
  Theorem H / the H1 double death as the aligned special cases.
  (Straddles are vacuous under the hatch — checked and skipped; the
  escalation path adds the block-2 theories if blocks {0,1} were SAT.)

Part B — L-LOP(M): if one team's band part has size <= K-1 (so the
  other team owns >= M+17-K band values), the band-major team's Th1
  alone is inconsistent with straddle-freeness + (2,2,2) bounds +
  fan-cleanness: coloring vars + guarded Th1(B) order theory +
  |Y_A| <= K-1 is UNSAT.  Reports Ymin*(M) = the least band-major
  size for which the kill fires (largest UNSAT K by bisection).

Run: .venv/bin/python experiments/e150_wholesale.py M [A|B|AB]
Out: data/e150_wholesale_M{M}.json ; log data/e150_wholesale_M{M}.log
"""
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from e147_adv_cegar import core_support

from pysat.solvers import Cadical195
from pysat.card import CardEnc, EncType


class Vars:
    def __init__(self, start=0):
        self.top = start

    def new(self):
        self.top += 1
        return self.top


def order_block(vp, points):
    """Order vars + transitivity clauses on `points`."""
    idx = {v: k for k, v in enumerate(points)}
    off = {}
    n = len(points)
    for i in range(n):
        for j in range(i + 1, n):
            off[(i, j)] = vp.new()

    def lit(u, w):
        i, j = idx[u], idx[w]
        return off[(i, j)] if i < j else -off[(j, i)]

    cls = []
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                x, y, z = off[(i, j)], off[(j, k)], off[(i, k)]
                cls.append([-x, -y, z])
                cls.append([x, y, -z])
    return lit, cls


# ----------------------------------------------------------------------
# Part A: P-ARM
# ----------------------------------------------------------------------

def part_A(M, blocks=(0, 1)):
    P0, P1, P2 = core_support(M)
    U = {'A': [v for v in P0 if v % 2 == 1],
         'B': [v for v in P0 if v % 2 == 0]}
    Z = {'A': [v for v in P2 if v % 2 == 0],
         'B': [v for v in P2 if v % 2 == 1]}
    vp = Vars()
    yA = {v: vp.new() for v in P1}

    def yT(t, v):
        return yA[v] if t == 'A' else -yA[v]

    cls = []
    # band bounds >= 2 per team
    for sign in (1, -1):
        enc = CardEnc.atleast(lits=[sign * yA[v] for v in P1], bound=2,
                              top_id=vp.top, encoding=EncType.seqcounter)
        vp.top = max(vp.top, enc.nv)
        cls += enc.clauses
    n_units = 0
    for t in 'AB':
        Us, Zs = set(U[t]), set(Z[t])
        if 0 in blocks:
            lit0, tr = order_block(vp, U[t])
            cls += tr
            for b in U[t]:
                for d in range(1, min(b - (M + 1), 2 * M - b) + 1):
                    a, c = b - d, b + d
                    if a in Us and c in Us:
                        cls.append([-lit0(a, b), -lit0(b, c)])
                        cls.append([lit0(a, b), lit0(b, c)])
                for a in U[t]:
                    if a >= b:
                        continue
                    c = 2 * b - a
                    if 3 * M - 15 <= c <= 4 * M:      # (0,0,1) unit b < a
                        cls.append([-yT(t, c), lit0(b, a)])
                        n_units += 1
        if 1 in blocks:
            lit1, tr = order_block(vp, P1)
            cls += tr
            lo1, hi1 = 3 * M - 15, 4 * M
            for b in P1:
                for d in range(1, min(b - lo1, hi1 - b) + 1):
                    a, c = b - d, b + d
                    g = [-yT(t, a), -yT(t, b), -yT(t, c)]
                    cls.append(g + [-lit1(a, b), -lit1(b, c)])
                    cls.append(g + [lit1(a, b), lit1(b, c)])
            for b in P1:                               # alpha: c < b
                for c in P1:
                    if c <= b:
                        continue
                    a = 2 * b - c
                    if M + 1 <= a <= 2 * M and a in Us:
                        cls.append([-yT(t, b), -yT(t, c), lit1(c, b)])
                        n_units += 1
            for a in P1:                               # beta: b < a
                for b in P1:
                    if b <= a:
                        continue
                    c = 2 * b - a
                    if 4 * M + 1 <= c <= 6 * M + 15 and c in Zs:
                        cls.append([-yT(t, a), -yT(t, b), lit1(b, a)])
                        n_units += 1
        if 2 in blocks:
            lit2, tr = order_block(vp, Z[t])
            cls += tr
            for b in Z[t]:
                for d in range(1, (2 * M + 15) // 2 + 1):
                    a, c = b - d, b + d
                    if a in Zs and c in Zs:
                        cls.append([-lit2(a, b), -lit2(b, c)])
                        cls.append([lit2(a, b), lit2(b, c)])
                for c in Z[t]:
                    if c <= b:
                        continue
                    a = 2 * b - c
                    if 3 * M - 15 <= a <= 4 * M:       # (1,2,2) unit c < b
                        cls.append([-yT(t, a), lit2(c, b)])
                        n_units += 1
    t0 = time.time()
    with Cadical195(bootstrap_with=cls) as s:
        ok = s.solve()
    el = round(time.time() - t0, 1)
    print(f'  P-ARM({M}) blocks={blocks}: '
          f'{"SAT" if ok else "UNSAT"} [{el}s] '
          f'(vars={vp.top}, clauses={len(cls)}, units={n_units})',
          flush=True)
    return ('SAT' if ok else 'UNSAT'), el


# ----------------------------------------------------------------------
# Part B: L-LOP
# ----------------------------------------------------------------------

def build_llop_base(M):
    """Everything except the |Y_A| <= K-1 cardinality."""
    P0, P1, P2 = core_support(M)
    V = P0 + P1 + P2
    vp = Vars()
    ai = {v: vp.new() for v in V}
    cls = []
    for y in P1:
        for u in P0:
            z = 2 * y - u
            if 4 * M + 1 <= z <= 6 * M + 15:
                cls.append([-ai[u], -ai[y], -ai[z]])
                cls.append([ai[u], ai[y], ai[z]])
    for B in (P0, P1, P2):
        for sign in (1, -1):
            enc = CardEnc.atleast(lits=[sign * ai[v] for v in B], bound=2,
                                  top_id=vp.top,
                                  encoding=EncType.seqcounter)
            vp.top = max(vp.top, enc.nv)
            cls += enc.clauses
    with open(os.path.join(HERE, '..', 'data',
                           f'e146_catalogue_M{M}.json')) as f:
        cat = json.load(f)
    for p in cat:
        if p['blk'] != 2:
            continue
        cls.append([-ai[v] for v in p['S']])
        cls.append([ai[v] for v in p['S']])
    # Th1 of team B (guard: value in B <=> ai false)
    lit1, tr = order_block(vp, P1)
    cls += tr
    lo1, hi1 = 3 * M - 15, 4 * M
    for b in P1:
        for d in range(1, min(b - lo1, hi1 - b) + 1):
            a, c = b - d, b + d
            g = [ai[a], ai[b], ai[c]]
            cls.append(g + [-lit1(a, b), -lit1(b, c)])
            cls.append(g + [lit1(a, b), lit1(b, c)])
    for b in P1:                                       # alpha
        for c in P1:
            if c <= b:
                continue
            a = 2 * b - c
            if M + 1 <= a <= 2 * M:
                cls.append([ai[a], ai[b], ai[c], lit1(c, b)])
    for a in P1:                                       # beta
        for b in P1:
            if b <= a:
                continue
            c = 2 * b - a
            if 4 * M + 1 <= c <= 6 * M + 15:
                cls.append([ai[a], ai[b], ai[c], lit1(b, a)])
    return ai, vp, cls


def part_B(M):
    P0, P1, P2 = core_support(M)
    ai, vp, base = build_llop_base(M)
    print(f'  L-LOP({M}) base: vars={vp.top} clauses={len(base)}',
          flush=True)

    def verdict(K):
        t0 = time.time()
        enc = CardEnc.atmost(lits=[ai[v] for v in P1], bound=K - 1,
                             top_id=vp.top + 100000,
                             encoding=EncType.seqcounter)
        with Cadical195(bootstrap_with=base) as s:
            for c in enc.clauses:
                s.add_clause(c)
            ok = s.solve()
        el = round(time.time() - t0, 1)
        print(f'    K={K} (|Y_A| <= {K-1}, |Y_B| >= {M+17-K}): '
              f'{"SAT" if ok else "UNSAT"} [{el}s]', flush=True)
        return ok

    # bisect: largest K with UNSAT
    lo, hi = 2, (M + 16) // 2 + 1                      # lo assumed UNSAT
    if verdict(hi):
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if verdict(mid):
                hi = mid
            else:
                lo = mid
        assert not verdict(lo) if lo == 2 else True
        kmax_unsat = lo
    else:
        kmax_unsat = hi
    print(f'  L-LOP({M}): UNSAT for all K <= {kmax_unsat} '
          f'(band-major size Ymin* = {M + 17 - kmax_unsat})', flush=True)
    return kmax_unsat


def main():
    M = int(sys.argv[1]) if len(sys.argv) > 1 else 48
    parts = sys.argv[2] if len(sys.argv) > 2 else 'AB'
    out = {'M': M}
    if 'A' in parts:
        v, el = part_A(M, (0, 1))
        out['P_ARM_blocks01'] = v
        if v == 'SAT':
            v2, el2 = part_A(M, (0, 1, 2))
            out['P_ARM_blocks012'] = v2
    if 'B' in parts:
        out['L_LOP_kmax_unsat'] = part_B(M)
    path = os.path.join(HERE, '..', 'data', f'e150_wholesale_M{M}.json')
    with open(path, 'w') as f:
        json.dump(out, f)
    print(f'e150: DONE {out}', flush=True)


if __name__ == '__main__':
    main()
