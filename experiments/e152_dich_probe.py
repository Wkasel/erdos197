"""e152: pinned-configuration probes for the DICH(M) hand proof
(notes/57).  Pin the hatch (U_A = odds of P0, U_B = evens) and a
prescribed Z-split: Z_A = {4M+d : d in D_odd} u (evens of P2 minus
{4M+e : e in E_B}), Z_B = the complement.  Band left free.  Solve the
e149 instance (straddles + fan patterns + bounds + min|Y| >= K) under
the pin; on UNSAT extract and deletion-minimize an assumption core
over the softened straddles/fans to expose the kill mechanism; on SAT
print the witness band anatomy.

Run: .venv/bin/python experiments/e152_dich_probe.py M K D_odd [E_B]
     D_odd, E_B comma-separated offset lists, e.g. "1" or "1,3"; E_B
     defaults to empty ("-" = empty).
Log: appended to data/e152_dich_probe.log by the caller (stdout).
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
    D = [int(x) for x in sys.argv[3].split(',')] if sys.argv[3] != '-' else []
    EB = ([int(x) for x in sys.argv[4].split(',')]
          if len(sys.argv) > 4 and sys.argv[4] != '-' else [])
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

    # ---- the pin (A = true side).  U_A = odds of P0, U_B = evens.
    for u in P0:
        slv.add_clause([ai[u]] if u % 2 == 1 else [-ai[u]])
    # Z pin: odd z: in A iff offset in D; even z: in B iff offset in EB
    for z in P2:
        off = z - 4 * M
        if z % 2 == 1:
            slv.add_clause([ai[z]] if off in D else [-ai[z]])
        else:
            slv.add_clause([-ai[z]] if off in EB else [ai[z]])

    # ---- straddles (soft)
    for y in P1:
        for u in P0:
            z = 2 * y - u
            if 4 * M + 1 <= z <= 6 * M + 15:
                s = soft()
                sel[s] = ('straddle', u, y, z)
                slv.add_clause([-s, -ai[u], -ai[y], -ai[z]])
                slv.add_clause([-s, ai[u], ai[y], ai[z]])
    # ---- fan patterns (soft)
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
    # ---- hard: bounds (2,2,2) + min|Y| >= K both teams
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

    asel = sorted(sel)
    t0 = time.time()
    ok = slv.solve(assumptions=asel)
    print(f'M={M} K={K} D={D} EB={EB}: '
          f'{"SAT" if ok else "UNSAT"} [{time.time()-t0:.1f}s]', flush=True)
    if ok:
        model = set(l for l in slv.get_model() if l > 0)
        ya = sorted(y - 4 * M for y in P1 if ai[y] in model)
        yb = sorted(y - 4 * M for y in P1 if ai[y] not in model)
        print(f'  |Y_A|={len(ya)} Y_A offs: {ya}', flush=True)
        print(f'  |Y_B|={len(yb)} Y_B offs: {yb}', flush=True)
        return
    core = set(slv.get_core() or asel) & set(asel)
    print(f'  first core {len(core)} of {len(asel)}', flush=True)
    for s in sorted(core, reverse=True):
        if s not in core:
            continue
        trial = sorted(core - {s})
        if not slv.solve(assumptions=trial):
            core = set(slv.get_core() or trial) & set(trial)
    kinds = Counter(sel[s][0] for s in core)
    print(f'  minimized {len(core)} ({dict(kinds)}) '
          f'[{time.time()-t0:.0f}s]', flush=True)
    for s in sorted(core):
        item = sel[s]
        if item[0] == 'straddle':
            _, u, y, z = item
            print(f'    straddle u=M+{u-M} y=4M{y-4*M:+d} z=4M+{z-4*M}',
                  flush=True)
        else:
            _, src, S = item
            print(f'    fan {src}: offs={[v-4*M for v in S]}', flush=True)


if __name__ == '__main__':
    main()
