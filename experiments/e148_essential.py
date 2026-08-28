"""e148: the essential catalogue — a pattern-level MUS of ADV(M)
(notes/56 SS2-3).

Load the full catalogue (e146 seed + e147 CEGAR discoveries), make
each death pattern a SOFT selector guarding its two monochromaticity
clauses; straddle-freeness + bounds + swap-symmetry-breaking stay
hard.  ADV(M) is UNSAT (e147); extract an assumption core over the
patterns and deletion-minimize it.  The result E(M) is a minimal
sub-catalogue with COV(M) still true — the load-bearing regime
structure of the bridge.

Then classify E(M): per pattern block, size, source, parity/mod-4
anatomy of the offsets.

Run: .venv/bin/python experiments/e148_essential.py M
Out: data/e148_essential_M{M}.json
Log: data/e148_essential_M{M}.log
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


def build(M, bounds=(2, 2, 2)):
    P0, P1, P2 = core_support(M)
    blocks = (P0, P1, P2)
    V = P0 + P1 + P2
    ai = {v: k + 1 for k, v in enumerate(V)}
    top = len(V)
    slv = Cadical195()
    for y in P1:
        for u in P0:
            z = 2 * y - u
            if 4 * M + 1 <= z <= 6 * M + 15:
                slv.add_clause([-ai[u], -ai[y], -ai[z]])
                slv.add_clause([ai[u], ai[y], ai[z]])
    for bi, B in enumerate(blocks):
        if bounds[bi] <= 0:
            continue
        for sign in (1, -1):
            enc = CardEnc.atleast(lits=[sign * ai[v] for v in B],
                                  bound=bounds[bi], top_id=top,
                                  encoding=EncType.seqcounter)
            top = max(top, enc.nv)
            for c in enc.clauses:
                slv.add_clause(c)
    slv.add_clause([ai[M + 1]])
    return slv, ai, top


def main():
    M = int(sys.argv[1]) if len(sys.argv) > 1 else 48
    with open(os.path.join(HERE, '..', 'data',
                           f'e146_catalogue_M{M}.json')) as f:
        cat = json.load(f)
    with open(os.path.join(HERE, '..', 'data',
                           f'e147_cegar_M{M}.json')) as f:
        ceg = json.load(f)
    assert ceg['verdict'] == 'UNSAT'
    cat = cat + [{k: p[k] for k in ('blk', 'S', 'src')}
                 for p in ceg['discovered']]
    print(f'M={M}: full catalogue {len(cat)}', flush=True)

    slv, ai, top = build(M, tuple(ceg['bounds']))
    sel = {}
    for p in cat:
        top += 1
        s = top
        sel[s] = p
        slv.add_clause([-s] + [-ai[v] for v in p['S']])
        slv.add_clause([-s] + [ai[v] for v in p['S']])
    asel = sorted(sel)
    t0 = time.time()
    assert not slv.solve(assumptions=asel), 'ADV must be UNSAT'
    core = set(slv.get_core() or asel) & set(asel)
    print(f'first core: {len(core)} patterns [{time.time()-t0:.1f}s]',
          flush=True)
    # deletion minimization
    n_solve = 0
    for s in sorted(core, reverse=True):
        if s not in core:
            continue
        trial = sorted(core - {s})
        n_solve += 1
        if not slv.solve(assumptions=trial):
            core = set(slv.get_core() or trial) & set(trial)
    print(f'minimized essential catalogue: {len(core)} patterns '
          f'({n_solve} solves, {time.time()-t0:.0f}s)', flush=True)
    ess = [sel[s] for s in sorted(core)]
    # classification
    anchor = {0: M, 1: 4 * M, 2: 4 * M}
    by_blk = Counter(p['blk'] for p in ess)
    by_src = Counter(p['src'].split('(')[0] for p in ess)
    print(f'by block: {dict(by_blk)}   by source: {dict(by_src)}',
          flush=True)
    for p in sorted(ess, key=lambda p: (p['blk'], len(p['S']))):
        offs = [v - anchor[p['blk']] for v in p['S']]
        par = Counter(o % 2 for o in offs)
        print(f'  blk{p["blk"]} |S|={len(p["S"]):3d} '
              f'par(e/o)={par.get(0,0)}/{par.get(1,0)} '
              f'src={p["src"]:22s} offs={offs}', flush=True)
    with open(os.path.join(HERE, '..', 'data',
                           f'e148_essential_M{M}.json'), 'w') as f:
        json.dump({'M': M, 'essential': ess}, f)
    print('e148: DONE', flush=True)


if __name__ == '__main__':
    main()
