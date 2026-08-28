"""e153: single-K probes of DICH(M) and its robust variants
(notes/58 SS1, SS4).

Modes (all over the e149 fan-clean base: straddle-free + (2,2,2)
bounds + no monochromatic block-2 pattern + WLOG chi(M+1)=A):

  phi1  K      : fan-clean ^ min|Y| >= K ^ Phi >= 1        (e149's DICH)
  upure K      : fan-clean ^ min|Y| >= K ^ (U not pure)    (DICH-U)
                 "U pure" = P0 splits exactly odd/even between the
                 teams (either orientation); the constraint asserts
                 NEITHER orientation holds, via 2 deviation clauses.
  zdef  K d0   : fan-clean ^ min|Y| >= K ^ U pinned to orientation 1
                 (odds of P0 -> A, evens -> B) ^ (#Z-defectors >= d0+1)
                 where a Z-defector is z in P2 with chi(z) = A, z odd
                 or chi(z) = B, z even.                     (DICH-Z)

UNSAT verdicts are the lemma directions; SAT prints witness anatomy.
NOTE (soundness of the U pinning in zdef): by DICH-U at the same K,
U must be pure; orientation 1 is WLOG only because the fan-clean base
breaks symmetry with chi(M+1) = A — M+1 is ODD, so orientation 1
(odds -> A) is the only orientation compatible with the symmetry
clause, EXCEPT that e149's symmetry clause makes orientation 2
(odds -> B) infeasible only at the P0 level.  To keep both zdef
orientations honest we DROP the chi(M+1)=A symmetry clause in modes
upure/zdef and instead: upure asserts neither orientation, zdef pins
orientation 1 (the team-swap image of any orientation-2 coloring).

Run: .venv/bin/python experiments/e153_dich_probe.py M mode K [d0]
Log: data/e153_dich_probes.log (+ .json)
"""
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from e147_adv_cegar import core_support, anatomy
from e149_dichotomy import build_fan_clean

from pysat.solvers import Cadical195
from pysat.card import CardEnc, EncType

LOG = os.path.join(HERE, '..', 'data', 'e153_dich_probes.log')
OUT = os.path.join(HERE, '..', 'data', 'e153_dich_probes.json')


def log(msg):
    print(msg, flush=True)
    with open(LOG, 'a') as f:
        f.write(msg + '\n')


def main():
    M = int(sys.argv[1])
    mode = sys.argv[2]
    K = int(sys.argv[3])
    d0 = int(sys.argv[4]) if len(sys.argv) > 4 else None
    P0, P1, P2 = core_support(M)
    V = P0 + P1 + P2
    t0 = time.time()
    ai, top, base, nfan = build_fan_clean(M)
    if mode in ('upure', 'zdef'):
        # drop the chi(M+1)=A symmetry clause (last clause added)
        assert base[-1] == [ai[M + 1]]
        base = base[:-1]
    log(f'e153 M={M} mode={mode} K={K} d0={d0}: base ready '
        f'({nfan} fan patterns) [{time.time()-t0:.0f}s]')

    cls = []
    # min|Y| >= K, both teams
    ctop = top + 10000
    for sign in (1, -1):
        enc = CardEnc.atleast(lits=[sign * ai[v] for v in P1], bound=K,
                              top_id=ctop, encoding=EncType.seqcounter)
        ctop = max(ctop, enc.nv)
        cls += enc.clauses

    if mode == 'phi1':
        pairs = [(u, z) for u in P0 for z in P2 if (u - z) % 2 == 0]
        qvars = []
        for (u, z) in pairs:
            ctop += 1
            q = ctop
            qvars.append(q)
            cls.append([-q, -ai[u], ai[z]])
            cls.append([-q, ai[u], -ai[z]])
        cls.append(qvars)
    elif mode == 'upure':
        # orientation 1 = odds of P0 -> A, evens -> B; orientation 2 =
        # the swap.  "not orientation i" = OR of deviations.
        dev1, dev2 = [], []
        for u in P0:
            if u % 2 == 1:
                dev1.append(-ai[u])
                dev2.append(ai[u])
            else:
                dev1.append(ai[u])
                dev2.append(-ai[u])
        # deviation literal true iff chi(u) differs from orientation:
        # orientation1 wants odd->A (ai true), even->B (ai false).
        cls.append(dev1)
        cls.append(dev2)
    elif mode == 'zdef':
        assert d0 is not None
        for u in P0:                       # pin orientation 1
            cls.append([ai[u]] if u % 2 == 1 else [-ai[u]])
        dlits = []
        for z in P2:
            ctop += 1
            d = ctop
            dlits.append(d)
            # defector: z odd & chi=A, or z even & chi=B
            if z % 2 == 1:
                cls.append([-d, ai[z]])
                cls.append([d, -ai[z]])
            else:
                cls.append([-d, -ai[z]])
                cls.append([d, ai[z]])
        enc = CardEnc.atleast(lits=dlits, bound=d0 + 1, top_id=ctop,
                              encoding=EncType.seqcounter)
        ctop = max(ctop, enc.nv)
        cls += enc.clauses
    else:
        raise SystemExit(f'unknown mode {mode}')

    t0 = time.time()
    with Cadical195(bootstrap_with=base) as s:
        for c in cls:
            s.add_clause(c)
        ok = s.solve()
        el = time.time() - t0
        v = 'SAT' if ok else 'UNSAT'
        extra = ''
        if ok:
            model = set(l for l in s.get_model() if l > 0)
            colA = [v2 for v2 in V if ai[v2] in model]
            colB = [v2 for v2 in V if ai[v2] not in model]
            ana = anatomy(M, colA, colB)
            phi = sum(1 for u in P0 for z in P2
                      if (u - z) % 2 == 0
                      and ((ai[u] in model) == (ai[z] in model)))
            extra = (f' phi={phi} sizes A={ana["A"]["sizes"]} '
                     f'B={ana["B"]["sizes"]}')
    log(f'  DICH-{mode}({M}) K={K}' +
        (f' d0={d0}' if d0 is not None else '') +
        f': {v} [{el:.1f}s]{extra}')
    res = {}
    if os.path.exists(OUT):
        with open(OUT) as f:
            res = json.load(f)
    res[f'M{M}_{mode}_K{K}' + (f'_d{d0}' if d0 is not None else '')] = v
    with open(OUT, 'w') as f:
        json.dump(res, f, indent=0)


if __name__ == '__main__':
    main()
