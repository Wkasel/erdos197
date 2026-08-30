#!/usr/bin/env python3
"""e183: ThW1' puncture-tolerance scan (notes/77 SS5, GAP-LLOP-alpha).

Question (notes/58 SS5.1 pre-registration, now made exact): how many
punctures does the class-alpha system ThW1'[class - X] tolerate, and
what are the minimal breaking sets?  e155c showed: singles and
alive-cliques never break.  The L-LOP frontier witness at M = 128
defected the four odd E1-region values {3M-5, 3M-9, 3M-11, 3M-13}.

PRE-REGISTERED prediction (written before the run): the minimum
breaking puncture set has size 4, and every size-4 breaking set is a
packed E1-region pattern of the witness species.

Scan, for m in argv (M = 2m), each parity class:
  * all X subseteq E1cap := [3M-15, 3M-1] cap class (8 values) with
    |X| = 1..5: solve alpha system minus X (e182 fresh encoder);
    report min breaking size + all minimal breaking sets (as offsets
    from 3M);
  * control: 60 random X of sizes 3-4 drawn from the whole class
    OUTSIDE E1 — expected all UNSAT (the kill should be E1-local).

Run: python3 experiments/e183_thw1_tolerance.py m [m ...]
Log: data/e183_thw1_tolerance.log + .json
"""
import itertools
import json
import os
import random
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
DATA = os.path.join(HERE, '..', 'data')
from e182_parm_alpha_robust import alpha_unsat

LOG = []


def log(*a):
    s = ' '.join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def main():
    random.seed(183)
    summary = {}
    for marg in sys.argv[1:]:
        m = int(marg)
        M = 2 * m
        for parity in (1, 0):
            t0 = time.time()
            e1 = [v for v in range(3 * M - 15, 3 * M + 1)
                  if v % 2 == parity]
            assert len(e1) == 8, (M, parity, e1)
            min_break = None
            breakers = []
            for k in range(1, 6):
                found_k = []
                for X in itertools.combinations(e1, k):
                    uns, _ = alpha_unsat(M, parity, X)
                    if not uns:
                        found_k.append(tuple(v - 3 * M for v in X))
                if found_k and min_break is None:
                    min_break = k
                    breakers = found_k
                if found_k and k > (min_break or 99):
                    break
                if min_break is not None and k >= min_break + 1:
                    break
            nonE1 = [v for v in range(3 * M, 4 * M + 1)
                     if v % 2 == parity]
            ctrl_sat = []
            for _ in range(60):
                k = random.choice((3, 4))
                X = tuple(sorted(random.sample(nonE1, k)))
                uns, _ = alpha_unsat(M, parity, X)
                if not uns:
                    ctrl_sat.append(tuple(v - 3 * M for v in X))
            cname = 'odd' if parity else 'even'
            log(f'e183 m={m} M={M} {cname}: min E1-breaking size = '
                f'{min_break}; minimal breakers (offsets from 3M): '
                f'{breakers}; non-E1 control SAT (expect 0): '
                f'{len(ctrl_sat)} {ctrl_sat[:4]} [{time.time()-t0:.0f}s]')
            summary[f'{m}_{cname}'] = {'min_break': min_break,
                                       'breakers': breakers,
                                       'ctrl_sat': ctrl_sat}
    with open(os.path.join(DATA, 'e183_thw1_tolerance.json'), 'w') as f:
        json.dump(summary, f)
    with open(os.path.join(DATA, 'e183_thw1_tolerance.log'), 'a') as f:
        f.write('\n'.join(LOG) + '\n')
    log('e183: DONE')


if __name__ == '__main__':
    main()
