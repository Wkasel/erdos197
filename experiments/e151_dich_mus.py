"""e151: MUS-mine the DICH(M) UNSAT at K = K*(M)  (notes/56 SS5.3
step 2 — the GAP-DICH uniformization seed).

Instance: straddle-freeness + (2,2,2) bounds + fan patterns +
Phi >= 1 + min|Y| >= K*.  Soften (a) each fan pattern, (b) each
straddle triple; keep bounds / Phi / cardinality hard.  Extract an
assumption core, deletion-minimize, report the load-bearing fan
patterns (as (q,p) sources and offset shapes) and straddle triples
(as (u, y, z) offset shapes).

Run: .venv/bin/python experiments/e151_dich_mus.py M K
Log: data/e151_dich_mus_M{M}.log
"""
import json
import os
import sys
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from e147_adv_cegar import core_support

from pysat.solvers import Cadical195
from pysat.card import CardEnc, EncType


def main():
    M = int(sys.argv[1])
    K = int(sys.argv[2])
    P0, P1, P2 = core_support(M)
    V = P0 + P1 + P2
    ai = {v: k + 1 for k, v in enumerate(V)}
    top = len(V)
    slv = Cadical195()
    sel = {}

    def soft():
        nonlocal top
        top += 1
        return top

    # straddles (soft, one selector per triple)
    for y in P1:
        for u in P0:
            z = 2 * y - u
            if 4 * M + 1 <= z <= 6 * M + 15:
                s = soft()
                sel[s] = ('straddle', u, y, z)
                slv.add_clause([-s, -ai[u], -ai[y], -ai[z]])
                slv.add_clause([-s, ai[u], ai[y], ai[z]])
    # fan patterns (soft)
    with open(os.path.join(HERE, '..', 'data',
                           f'e146_catalogue_M{M}.json')) as f:
        cat = json.load(f)
    for p in cat:
        if p['blk'] != 2:
            continue
        s = soft()
        sel[s] = ('fan', p['src'], tuple(p['S']))
        slv.add_clause([-s] + [-ai[v] for v in p['S']])
        slv.add_clause([-s] + [ai[v] for v in p['S']])
    # hard: bounds, symmetry, Phi >= 1, min|Y| >= K
    for B in (P0, P1, P2):
        for sign in (1, -1):
            enc = CardEnc.atleast(lits=[sign * ai[v] for v in B], bound=2,
                                  top_id=top, encoding=EncType.seqcounter)
            top = max(top, enc.nv)
            for c in enc.clauses:
                slv.add_clause(c)
    for sign in (1, -1):
        enc = CardEnc.atleast(lits=[sign * ai[v] for v in P1], bound=K,
                              top_id=top, encoding=EncType.seqcounter)
        top = max(top, enc.nv)
        for c in enc.clauses:
            slv.add_clause(c)
    pairs = [(u, z) for u in P0 for z in P2 if (u - z) % 2 == 0]
    qvars = []
    for (u, z) in pairs:
        top += 1
        qvars.append(top)
        slv.add_clause([-top, -ai[u], ai[z]])
        slv.add_clause([-top, ai[u], -ai[z]])
    slv.add_clause(qvars)

    asel = sorted(sel)
    t0 = time.time()
    assert not slv.solve(assumptions=asel), 'must be UNSAT at K*'
    core = set(slv.get_core() or asel) & set(asel)
    print(f'M={M} K={K}: first core {len(core)} of {len(asel)} '
          f'[{time.time()-t0:.1f}s]', flush=True)
    for s in sorted(core, reverse=True):
        if s not in core:
            continue
        trial = sorted(core - {s})
        if not slv.solve(assumptions=trial):
            core = set(slv.get_core() or trial) & set(trial)
    kinds = Counter(sel[s][0] for s in core)
    print(f'minimized: {len(core)} ({dict(kinds)}) '
          f'[{time.time()-t0:.0f}s]', flush=True)
    for s in sorted(core):
        item = sel[s]
        if item[0] == 'straddle':
            _, u, y, z = item
            print(f'  straddle u=M+{u-M} y=4M-{4*M-y} z=4M+{z-4*M}',
                  flush=True)
        else:
            _, src, S = item
            print(f'  fan {src}: offs={[v-4*M for v in S]}', flush=True)
    print('e151: DONE', flush=True)


if __name__ == '__main__':
    main()
