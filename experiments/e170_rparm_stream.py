"""e170: memory-streaming runner for RP-ARM at large M (notes/66).

Same instance as e154_robust_parm (imports its build()), but feeds
clauses to Cadical by popping from the clause list so the python-side
memory is released as the solver ingests — peak RSS ~= the built list
alone, not list + bootstrap copy.  Needed because the pod container
has a 62 GB cgroup cap (e154 at M = 256 = 112M clauses OOM-killed).

Run: python3 experiments/e170_rparm_stream.py M d0 [--blocks 012]
Log: appends to data/e154_rparm.log + data/e154_rparm.json (same
     tags as e154, suffix _stream).
"""
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import e154_robust_parm as e154

from pysat.solvers import Cadical195


def main():
    M = int(sys.argv[1])
    d0 = int(sys.argv[2])
    args = sys.argv[3:]
    blocks = (0, 1, 2)
    if '--blocks' in args:
        blocks = tuple(int(c) for c in args[args.index('--blocks') + 1])
    t0 = time.time()
    vp, cls, n_units = e154.build(M, d0, blocks, None)
    ncls = len(cls)
    tb = time.time() - t0
    e154.log(f'  RP-ARM({M}, d0={d0}) blocks={blocks} STREAM: '
             f'vars={vp.top} clauses={ncls} units={n_units} '
             f'[built {tb:.0f}s]')
    t0 = time.time()
    with Cadical195() as s:
        while cls:
            s.add_clause(cls.pop())
        tl = time.time() - t0
        e154.log(f'  ... loaded into solver [{tl:.0f}s]')
        ok = s.solve()
    el = time.time() - t0
    v = 'SAT' if ok else 'UNSAT'
    e154.log(f'  RP-ARM({M}, d0={d0}) blocks={blocks} STREAM: {v} '
             f'[{el:.1f}s]')
    res = {}
    if os.path.exists(e154.OUT):
        with open(e154.OUT) as f:
            res = json.load(f)
    tag = f'M{M}_d{d0}_b{"".join(map(str, blocks))}_stream'
    res[tag] = {'verdict': v, 'secs': round(el, 1), 'clauses': ncls}
    with open(e154.OUT, 'w') as f:
        json.dump(res, f, indent=0)


if __name__ == '__main__':
    main()
