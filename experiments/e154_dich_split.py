"""e154: the SPLIT branch of DICH(M)  (notes/57 SS5).

Full DICH instance (straddle-freeness both teams + block-2 fan
patterns + (2,2,2) bounds + min|Y| >= K*) with the pin "parity class
c of P0 is SPLIT" (both teams own class-c values).  Expected UNSAT
for c in {O, E} at every scale: together with Lemma T and the hatch
theorem (notes/57 SS4) this completes the DICH case analysis.

K* per scale: 48:26 64:35 80:42 96:51 112:60 128:68 (e149 + notes/58).

Run: .venv/bin/python experiments/e154_dich_split.py [M ...]
Log: data/e154_dich_split.log (caller tee).
"""
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '..', 'data')

from pysat.solvers import Cadical195
from pysat.card import CardEnc, EncType

KSTAR = {48: 26, 64: 35, 80: 42, 96: 51, 112: 60, 128: 68}


def run(M):
    K = KSTAR[M]
    P0 = list(range(M + 1, 2 * M + 1))
    P1 = list(range(3 * M - 15, 4 * M + 1))
    P2 = list(range(4 * M + 1, 6 * M + 16))
    V = P0 + P1 + P2
    ai = {v: k + 1 for k, v in enumerate(V)}
    top = len(V)
    base = []
    for y in P1:
        for u in P0:
            z = 2 * y - u
            if 4 * M + 1 <= z <= 6 * M + 15:
                base.append([-ai[u], -ai[y], -ai[z]])
                base.append([ai[u], ai[y], ai[z]])
    with open(os.path.join(DATA, f'e146_catalogue_M{M}.json')) as f:
        cat = json.load(f)
    nfan = 0
    for p in cat:
        if p['blk'] != 2:
            continue
        nfan += 1
        base.append([-ai[v] for v in p['S']])
        base.append([ai[v] for v in p['S']])
    for B in (P0, P1, P2):
        for sign in (1, -1):
            enc = CardEnc.atleast(lits=[sign * ai[v] for v in B],
                                  bound=2, top_id=top,
                                  encoding=EncType.seqcounter)
            top = max(top, enc.nv)
            base += enc.clauses
    for sign in (1, -1):
        enc = CardEnc.atleast(lits=[sign * ai[v] for v in P1], bound=K,
                              top_id=top, encoding=EncType.seqcounter)
        top = max(top, enc.nv)
        base += enc.clauses
    for c, name in ((1, 'O'), (0, 'E')):
        cl = [u for u in P0 if u % 2 == c]
        t0 = time.time()
        with Cadical195(bootstrap_with=base) as s:
            s.add_clause([ai[u] for u in cl])       # some class-c in A
            s.add_clause([-ai[u] for u in cl])      # some class-c in B
            ok = s.solve()
        print(f'M={M} K={K} split-{name}: '
              f'{"SAT (escape?!)" if ok else "UNSAT"} '
              f'[{time.time()-t0:.1f}s, {nfan} fans]', flush=True)
        assert not ok, (M, name, 'split branch escape!')
    print(f'M={M}: SPLIT branch closed (both classes)', flush=True)


if __name__ == '__main__':
    Ms = [int(a) for a in sys.argv[1:]] or [48, 64, 80, 96, 112, 128]
    for M in Ms:
        run(M)
    print('e154: DONE', flush=True)
