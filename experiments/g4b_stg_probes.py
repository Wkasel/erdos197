"""G4b follow-up probes on the stage rung STG (see g4b_seam_law.py).

Q1: is the 2-consecutive-block UNSAT special to ADJACENT pairs {x, x+1}
    (RUNG-IN style) or does ANY fixed pair kill?  Probes: {3,4}, {3,5},
    {19,27}, {21,25} (odd-odd), {5,9} at M = 64, 128.
Q2: do THREE consecutive blocks fall to a SINGLE attacker (the 2-block
    single rungs are SAT)?  Probes: x=3, x=15 on (M, 8M], M = 32, 64.
Q3: parity probe — odd-only pair {21, 25} vs mixed parity (an attacker
    of each parity may be the true requirement, cf. C3's g-classes).

Usage: .venv/bin/python experiments/g4b_stg_probes.py
Artifacts: data/g4b_stg_probes.json (+ stdout log).
"""
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from s2_growing_death import ap_order_sat            # noqa: E402
from g4b_seam_law import stg_units, run_sat          # noqa: E402


def main():
    budget = 2400
    rows = []
    print('== Q1: arbitrary fixed pairs on 2 consecutive blocks ==')
    for M in (64, 128):
        W = list(range(M + 1, 4 * M + 1))
        for F in ((3, 4), (3, 5), (19, 27), (21, 25), (5, 9)):
            run_sat(f'Q1 M={M} F={F}', W, stg_units(W, F), budget, rows)
    print('== Q2: single attacker on 3 consecutive blocks ==')
    for M in (32, 64):
        W = list(range(M + 1, 8 * M + 1))
        for F in ((3,), (15,)):
            run_sat(f'Q2 M={M} 3blocks F={F}', W, stg_units(W, F),
                    budget, rows)
    path = os.path.join(REPO, 'data', 'g4b_stg_probes.json')
    with open(path, 'w') as f:
        json.dump(rows, f, indent=1)
    print(f'wrote {path}')


if __name__ == '__main__':
    main()


def robustness():
    """Q3: puncture robustness of the pair rung.  Bottom-orientation
    punctures, both-member punctures, and arbitrary extra punctures."""
    budget = 2400
    rows = []
    print('== Q3: puncture robustness of STG pair rungs ==')
    for M in (64, 128):
        W0 = list(range(M + 1, 4 * M + 1))
        cfgs = [
            ('punctB', [v for v in W0 if v not in (2*M - 1, 4*M - 1)]),
            ('punct_all4', [v for v in W0
                            if v not in (2*M - 1, 2*M, 4*M - 1, 4*M)]),
            ('punct8_arb', [v for v in W0
                            if v not in (M + 7, M + 30, 2*M - 11, 2*M,
                                         2*M + 13, 3*M + 1, 4*M - 5,
                                         4*M - 1)]),
        ]
        for tag, W in cfgs:
            for F in ((21, 22), (3, 5)):
                run_sat(f'Q3 M={M} {tag} F={F}', W, stg_units(W, F),
                        budget, rows)
    path = os.path.join(REPO, 'data', 'g4b_stg_probes_q3.json')
    with open(path, 'w') as f:
        json.dump(rows, f, indent=1)
    print(f'wrote {path}')
