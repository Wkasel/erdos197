"""a8_dich_probe: blind-protocol MEASUREMENT probes for K*(M) at the
untouched scales (notes/57 audit; predictions committed 0605ec8).

Instance (written fresh from notes/56 SS3 / notes/57 SS0.1):
  colorings of CORE'(M); straddle-freeness both teams (u in P0,
  y in P1, z = 2y-u in P2: no monochromatic triple); (2,2,2) bounds;
  fan-clean (no team contains a blk-2 catalogue pattern); WLOG
  M+1 in A; optional pin Phi >= 1 (some same-parity P0xP2 pair
  monochromatic); optional pin "class c split"; |Y_A| >= K and
  |Y_B| >= K.

Probes (sequential, one solver at a time):
  M=144 K=75 phi1   expect SAT  (mechanistic+flat: K*=76; dead
                    mod-32 law predicts K*=74 i.e. UNSAT here)
  M=144 K=76 phi1   expect UNSAT (confirms K*(144) = 76)
  M=144 K=76 splitO expect UNSAT (SPLIT branch at fresh scale)
  M=144 K=76 splitE expect UNSAT
  M=160 K=83 phi1   DISCRIMINATOR: mechanistic law (K*=83) => UNSAT,
                    flat law (K*=84) => SAT
  M=160 K=82 phi1   expect SAT (sharpness of whichever wins)

Run: .venv/bin/python audit/a8_referee1/a8_dich_probe.py
Log: data/a8_dich_probe.log (caller tee).
"""
import json
import os
import time

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
DATA = os.path.join(BASE, 'data')

from pysat.solvers import Cadical195
from pysat.card import CardEnc, EncType


def build(M):
    P0 = list(range(M + 1, 2 * M + 1))
    P1 = list(range(3 * M - 15, 4 * M + 1))
    P2 = list(range(4 * M + 1, 6 * M + 16))
    V = P0 + P1 + P2
    ai = {v: i + 1 for i, v in enumerate(V)}
    top = len(V)
    cls = []
    for y in P1:
        for u in P0:
            z = 2 * y - u
            if 4 * M + 1 <= z <= 6 * M + 15:
                cls.append([-ai[u], -ai[y], -ai[z]])
                cls.append([ai[u], ai[y], ai[z]])
    with open(os.path.join(DATA, f'e146_catalogue_M{M}.json')) as f:
        cat = json.load(f)
    nfan = 0
    for p in cat:
        if p['blk'] != 2:
            continue
        nfan += 1
        cls.append([-ai[v] for v in p['S']])
        cls.append([ai[v] for v in p['S']])
    for B in (P0, P1, P2):
        for sign in (1, -1):
            enc = CardEnc.atleast(lits=[sign * ai[v] for v in B], bound=2,
                                  top_id=top, encoding=EncType.seqcounter)
            top = max(top, enc.nv)
            cls += enc.clauses
    cls.append([ai[M + 1]])
    return P0, P1, P2, V, ai, top, cls, nfan


def probe(M, K, mode):
    P0, P1, P2, V, ai, top, cls, nfan = build(M)
    cls = list(cls)
    if mode == 'phi1':
        qv = []
        for u in P0:
            for z in P2:
                if (u - z) % 2:
                    continue
                top += 1
                qv.append(top)
                cls.append([-top, -ai[u], ai[z]])
                cls.append([-top, ai[u], -ai[z]])
        cls.append(qv)
    elif mode in ('splitO', 'splitE'):
        c = 1 if mode == 'splitO' else 0
        cl = [u for u in P0 if u % 2 == c]
        cls.append([ai[u] for u in cl])
        cls.append([-ai[u] for u in cl])
    ctop = top
    for sign in (1, -1):
        enc = CardEnc.atleast(lits=[sign * ai[v] for v in P1], bound=K,
                              top_id=ctop,
                              encoding=EncType.seqcounter)
        ctop = max(ctop, enc.nv)
        cls += enc.clauses
    t0 = time.time()
    with Cadical195(bootstrap_with=cls) as s:
        ok = s.solve()
        dt = time.time() - t0
        if not ok:
            print(f'M={M} K={K} {mode}: UNSAT  [{dt:.1f}s, {nfan} fans]',
                  flush=True)
            return 'UNSAT'
        model = set(l for l in s.get_model() if l > 0)
        A = [v for v in V if ai[v] in model]
        Aset = set(A)
        UA = [v for v in P0 if v in Aset]
        UB = [v for v in P0 if v not in Aset]
        YA = [v for v in P1 if v in Aset]
        YB = [v for v in P1 if v not in Aset]
        ZA = [v for v in P2 if v in Aset]
        ZB = [v for v in P2 if v not in Aset]
        phi = sum(1 for u in P0 for z in P2 if (u - z) % 2 == 0
                  and ((u in Aset) == (z in Aset)))
        assert len(YA) >= K and len(YB) >= K, 'card encoding broken'
        DA_odd = sorted(z - 4 * M for z in ZA if z % 2 == 1)
        DB_ev = sorted(z - 4 * M for z in ZB if z % 2 == 0)
        hatchA = ('O' if all(u % 2 for u in UA) else
                  'E' if all(u % 2 == 0 for u in UA) else 'mixed')
        print(f'M={M} K={K} {mode}: SAT  [{dt:.1f}s]  phi={phi} '
              f'|U_A|={len(UA)} (parity {hatchA}) |Y|=({len(YA)},{len(YB)}) '
              f'|Z|=({len(ZA)},{len(ZB)})', flush=True)
        print(f'    Z_A-odd offs (defectors if A=O-side): {DA_odd[:12]}',
              flush=True)
        print(f'    Z_B-even offs: {DB_ev[:12]}', flush=True)
        return 'SAT'


def main():
    plan = [(144, 2, 'phi1', 'SAT (sanity)'), (160, 2, 'phi1', 'SAT (sanity)'),
            (144, 75, 'phi1', 'SAT'), (144, 76, 'phi1', 'UNSAT'),
            (144, 76, 'splitO', 'UNSAT'), (144, 76, 'splitE', 'UNSAT'),
            (160, 83, 'phi1', 'DISCRIMINATOR'),
            (160, 82, 'phi1', 'SAT')]
    for M, K, mode, exp in plan:
        v = probe(M, K, mode)
        print(f'    expected {exp}; got {v}', flush=True)
    print('a8_dich_probe: DONE', flush=True)


if __name__ == '__main__':
    main()
