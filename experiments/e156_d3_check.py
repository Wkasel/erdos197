"""e156: machine cross-check of Lemma D3 (notes/58 SS2.2).

Lemma D3 says: straddle-freeness (both teams) + (2,2,2) bounds +
(defuse-alpha: A_alpha = [2M-30, 2M] subseteq U_A) +
(defuse-beta: C = [4M+1, 5M+15] subseteq Z_A) is contradictory.
Pure coloring instances (no order vars, no fan patterns):

  lemma       : both defuses, (2,2,2)         — expect UNSAT (D3);
  ctrl_alpha  : defuse-alpha only             — expect SAT (an arm
                can be individually defused; beta-supply forced);
  ctrl_beta   : defuse-beta only              — expect SAT;
  ctrl_uB0    : both defuses, B's P0 bound dropped (U_B may be
                empty)                        — expect SAT (D3's
                |U_B| >= 1 hypothesis necessary).

A control coming back UNSAT is not a bug in D3 but a STRONGER
coloring fact — logged either way.

Run: .venv/bin/python experiments/e156_d3_check.py M [M ...]
Log: data/e156_d3_check.log
"""
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from e147_adv_cegar import core_support

from pysat.solvers import Cadical195
from pysat.card import CardEnc, EncType

LOG = os.path.join(HERE, '..', 'data', 'e156_d3_check.log')


def log(msg):
    print(msg, flush=True)
    with open(LOG, 'a') as f:
        f.write(msg + '\n')


def build(M, alpha, beta, uB_bound):
    P0, P1, P2 = core_support(M)
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
    reqs = [(1, P0, 2), (1, P1, 2), (1, P2, 2),
            (-1, P0, uB_bound), (-1, P1, 2), (-1, P2, 2)]
    for sign, B, bnd in reqs:
        if bnd <= 0:
            continue
        enc = CardEnc.atleast(lits=[sign * ai[v] for v in B], bound=bnd,
                              top_id=top, encoding=EncType.seqcounter)
        top = max(top, enc.nv)
        cls += enc.clauses
    if alpha:
        for u in range(2 * M - 30, 2 * M + 1):
            cls.append([ai[u]])
    if beta:
        for z in range(4 * M + 1, 5 * M + 16):
            cls.append([ai[z]])
    return cls


def main():
    for M in [int(x) for x in sys.argv[1:]]:
        for name, alpha, beta, ub, expect in (
                ('lemma', True, True, 2, 'UNSAT'),
                ('ctrl_alpha', True, False, 2, 'SAT'),
                ('ctrl_beta', False, True, 2, 'SAT'),
                ('ctrl_uB0', True, True, 0, 'SAT')):
            t0 = time.time()
            cls = build(M, alpha, beta, ub)
            with Cadical195(bootstrap_with=cls) as s:
                ok = s.solve()
            v = 'SAT' if ok else 'UNSAT'
            flag = 'OK' if v == expect else '*** UNEXPECTED ***'
            log(f'  e156 M={M} {name}: {v} (expect {expect}) {flag} '
                f'[{time.time()-t0:.1f}s]')


if __name__ == '__main__':
    main()
