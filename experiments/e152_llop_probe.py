"""e152: single-K probes of L-LOP(M)  (notes/58 SS1).

Same instance as e150 part B (fan-clean + straddle-free + (2,2,2)
bounds + |Y_A| <= K-1 + guarded Th1(team B)), but probing individual
K values instead of bisecting — used at the new scales M = 112, 128,
160 to test the cap law  cap(M) = (M+16)/2 - floor(M/32) - 2
(min|Y| form; kmax_unsat = cap + 1).

Run: .venv/bin/python experiments/e152_llop_probe.py M K [K ...]
Appends one line per probe to data/e152_llop_probes.log and updates
data/e152_llop_probes.json.
"""
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from e150_wholesale import build_llop_base
from e147_adv_cegar import core_support

from pysat.solvers import Cadical195
from pysat.card import CardEnc, EncType

LOG = os.path.join(HERE, '..', 'data', 'e152_llop_probes.log')
OUT = os.path.join(HERE, '..', 'data', 'e152_llop_probes.json')


def log(msg):
    print(msg, flush=True)
    with open(LOG, 'a') as f:
        f.write(msg + '\n')


def main():
    M = int(sys.argv[1])
    Ks = [int(x) for x in sys.argv[2:]]
    P0, P1, P2 = core_support(M)
    t0 = time.time()
    ai, vp, base = build_llop_base(M)
    log(f'e152 M={M}: base vars={vp.top} clauses={len(base)} '
        f'[{time.time()-t0:.0f}s build]')
    res = {}
    if os.path.exists(OUT):
        with open(OUT) as f:
            res = json.load(f)
    for K in Ks:
        t0 = time.time()
        enc = CardEnc.atmost(lits=[ai[v] for v in P1], bound=K - 1,
                             top_id=vp.top + 100000,
                             encoding=EncType.seqcounter)
        anat = ''
        with Cadical195(bootstrap_with=base) as s:
            for c in enc.clauses:
                s.add_clause(c)
            ok = s.solve()
            if ok:
                model = set(l for l in s.get_model() if l > 0)
                YA = sorted(4 * M - v for v in P1 if ai[v] in model)
                UBa = sorted(2 * M - u for u in range(2 * M - 30, 2 * M + 1)
                             if ai[u] not in model)
                ZBC = sorted(z - 4 * M for z in range(4 * M + 1, 5 * M + 16)
                             if ai[z] not in model)
                anat = (f'\n    Y_A depths(4M-y): {YA}'
                        f'\n    U_B alpha-window depths(2M-u): {UBa}'
                        f'\n    Z_B cap-zone offsets(z-4M): '
                        f'{ZBC[:40]}{"..." if len(ZBC) > 40 else ""} '
                        f'(n={len(ZBC)})')
        el = time.time() - t0
        v = 'SAT' if ok else 'UNSAT'
        log(f'  L-LOP({M}) K={K} (min|Y| <= {K-1}, band-major >= '
            f'{M+17-K}): {v} [{el:.1f}s]{anat}')
        res[f'M{M}_K{K}'] = v
        with open(OUT, 'w') as f:
            json.dump(res, f, indent=0)
    log(f'e152 M={M}: done {Ks}')


if __name__ == '__main__':
    main()
