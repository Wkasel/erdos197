"""e149: the potential dichotomy, adversarially  (notes/56 SS3).

Potential of a coloring chi:
    Phi(chi) = sum_T #{(u, z) in U_T x Z_T : u == z (mod 2)}
(the same-parity P0 x P2 exposure mass; Lemma W(d)'s parity hatch is
Phi = 0).  Proved in SS3: Phi = 0 iff chi restricted to P0 u P2 is a
PAR-family alignment (each parity class of P0 monochromatic, the
same class of P2 fully in the OTHER team).

CLAIM B (the bridge dichotomy, machine form): for the FAN-CLEAN
hypothesis only — straddle-freeness + (2,2,2) bounds + no
monochromatic block-2 (fan) pattern —

    min|Y| >= K*  ==>  Phi = 0,

i.e. ADV_fan(M) ^ (min|Y| >= K) ^ (Phi >= 1) is UNSAT from some
threshold K* on.  This script sweeps K and reports K*(M), plus the
frontier witnesses at K*(M) - 1.

Run: .venv/bin/python experiments/e149_dichotomy.py M
Out: data/e149_dichotomy_M{M}.json ; log data/e149_dichotomy_M{M}.log
"""
import json
import os
import sys
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from e147_adv_cegar import core_support, anatomy

from pysat.solvers import Cadical195
from pysat.card import CardEnc, EncType


def build_fan_clean(M, bounds=(2, 2, 2)):
    """Hard base: straddle + bounds + symmetry + block-2 patterns."""
    P0, P1, P2 = core_support(M)
    blocks = (P0, P1, P2)
    V = P0 + P1 + P2
    ai = {v: k + 1 for k, v in enumerate(V)}
    top = len(V)
    cls = []
    for y in P1:
        for u in P0:
            z = 2 * y - u
            if 4 * M + 1 <= z <= 6 * M + 15:
                cls.append([-ai[u], -ai[y], -ai[z]])
                cls.append([ai[u], ai[y], ai[z]])
    for bi, B in enumerate(blocks):
        if bounds[bi] <= 0:
            continue
        for sign in (1, -1):
            enc = CardEnc.atleast(lits=[sign * ai[v] for v in B],
                                  bound=bounds[bi], top_id=top,
                                  encoding=EncType.seqcounter)
            top = max(top, enc.nv)
            cls += enc.clauses
    with open(os.path.join(HERE, '..', 'data',
                           f'e146_catalogue_M{M}.json')) as f:
        cat = json.load(f)
    nfan = 0
    for p in cat:
        if p['blk'] != 2:
            continue
        nfan += 1
        cls.append([-ai[v] for v in p['S']])
        cls.append([ai[v] for v in p['S']])
    cls.append([ai[M + 1]])
    return ai, top, cls, nfan


def main():
    M = int(sys.argv[1]) if len(sys.argv) > 1 else 48
    P0, P1, P2 = core_support(M)
    V = P0 + P1 + P2
    ai, top, base, nfan = build_fan_clean(M)
    print(f'M={M}: fan-clean base with {nfan} fan patterns', flush=True)

    # Phi >= 1 machinery: q_uz -> (a_u <-> a_z), plus the OR clause
    pairs = [(u, z) for u in P0 for z in P2 if (u - z) % 2 == 0]
    qcls = []
    qvars = []
    for (u, z) in pairs:
        top += 1
        q = top
        qvars.append(q)
        qcls.append([-q, -ai[u], ai[z]])
        qcls.append([-q, ai[u], -ai[z]])
    print(f'  {len(pairs)} same-parity P0xP2 pairs', flush=True)

    # sanity: Phi = 0 must be SAT (the PAR family lives there)
    with Cadical195(bootstrap_with=base) as s:
        for (u, z) in pairs:
            s.add_clause([-ai[u], -ai[z]])
            s.add_clause([ai[u], ai[z]])
        ok = s.solve()
        assert ok, 'Phi=0 must be satisfiable (PAR family)'
        model = set(l for l in s.get_model() if l > 0)
        colA = [v for v in V if ai[v] in model]
        colB = [v for v in V if ai[v] not in model]
        ana = anatomy(M, colA, colB)
        print(f'  Phi=0 SAT; witness sizes A={ana["A"]["sizes"]} '
              f'B={ana["B"]["sizes"]} '
              f'U_A mod2={ana["A"]["mod2"][0]} '
              f'Z_A mod2={ana["A"]["mod2"][2]}', flush=True)

    results = {}
    Kmax = (M + 16) // 2
    frontier_witness = None
    kstar = None
    for K in range(2, Kmax + 1):
        t0 = time.time()
        with Cadical195(bootstrap_with=base) as s:
            for c in qcls:
                s.add_clause(c)
            s.add_clause(qvars)               # Phi >= 1
            for sign in (1, -1):
                enc = CardEnc.atleast(lits=[sign * ai[v] for v in P1],
                                      bound=K, top_id=top + 10000,
                                      encoding=EncType.seqcounter)
                for c in enc.clauses:
                    s.add_clause(c)
            ok = s.solve()
            el = time.time() - t0
            results[K] = 'SAT' if ok else 'UNSAT'
            if ok:
                model = set(l for l in s.get_model() if l > 0)
                colA = [v for v in V if ai[v] in model]
                colB = [v for v in V if ai[v] not in model]
                ana = anatomy(M, colA, colB)
                phi = sum(1 for (u, z) in pairs
                          if (ai[u] in model) == (ai[z] in model))
                frontier_witness = {'K': K, 'phi': phi, 'anatomy': ana}
                print(f'  K={K}: SAT (phi={phi}, sizes '
                      f'A={ana["A"]["sizes"]} B={ana["B"]["sizes"]}) '
                      f'[{el:.1f}s]', flush=True)
            else:
                kstar = K
                print(f'  K={K}: UNSAT [{el:.1f}s]  — K*({M}) = {K}',
                      flush=True)
                break
    # confirm monotone tail: verify UNSAT at Kmax too (cheap)
    if kstar is not None and kstar < Kmax:
        with Cadical195(bootstrap_with=base) as s:
            for c in qcls:
                s.add_clause(c)
            s.add_clause(qvars)
            for sign in (1, -1):
                enc = CardEnc.atleast(lits=[sign * ai[v] for v in P1],
                                      bound=Kmax, top_id=top + 10000,
                                      encoding=EncType.seqcounter)
                for c in enc.clauses:
                    s.add_clause(c)
            assert not s.solve(), 'monotone tail violated?!'
        print(f'  K={Kmax}: UNSAT (tail confirmed)', flush=True)
    out = {'M': M, 'n_fan': nfan, 'results': results, 'kstar': kstar,
           'frontier_witness': frontier_witness}
    with open(os.path.join(HERE, '..', 'data',
                           f'e149_dichotomy_M{M}.json'), 'w') as f:
        json.dump(out, f)
    print(f'e149: DONE M={M} K*={kstar}', flush=True)


if __name__ == '__main__':
    main()
