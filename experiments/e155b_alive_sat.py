"""e155b: SAT adjudication of the closure-alive attacker pairs on the
halved windows (notes/58 SS3; follow-up to e155 part B).

Closure is incomplete on the deep cluster (notes/55 SS5.3b), so
e155's "alive" pairs split into SAT-alive (true escapes) and
closure-stalled-but-UNSAT.  For each stored alive pair, solve the
double-fan order theory directly.  Reports, per (m, window):
  * the SAT-alive pair list (the TRUE half-scale resonance set),
  * its min gap and min-depth statistics — the quantities the
    P-ARM' Case split needs (H-FG6' = no SAT-alive pair at gap <= 6;
    DEEP = are there SAT-alive pairs with a member in the CW zone
    [3m-7, 3m-1]?).

Run: .venv/bin/python experiments/e155b_alive_sat.py m [m ...]
Log: data/e155_parm_hyp.log (+ JSON keys 'B_sat' per m)
"""
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from e155_parm_hypotheses import fan_sat_unsat, log, OUT


def main():
    with open(OUT) as f:
        res = json.load(f)
    for m in [str(int(x)) for x in sys.argv[1:]]:
        mi = int(m)
        deep_hi = 3 * mi - 1
        for name, hi in (('W2e', 6 * mi + 7), ('W2o', 6 * mi + 8)):
            lo = 4 * mi + 1
            alive = res[m]['B'][name]['alive']
            assert len(alive) == res[m]['B'][name]['n_alive'], \
                'stored alive list truncated — rerun e155 with more'
            t0 = time.time()
            sat_alive = []
            for (x1, x2) in alive:
                if not fan_sat_unsat(lo, hi, (x1, x2)):
                    sat_alive.append((x1, x2))
            gaps = sorted(set(p[1] - p[0] for p in sat_alive))
            deep = [p for p in sat_alive if p[0] <= deep_hi]
            log(f'  e155b m={m} {name}: {len(alive)} closure-alive -> '
                f'{len(sat_alive)} SAT-alive; gaps {gaps[:10]}; '
                f'with CW-zone member: {len(deep)} {deep[:10]} '
                f'[{time.time()-t0:.0f}s]')
            res[m]['B'][name]['sat_alive'] = sat_alive
            res[m]['B'][name]['hfg6_sat'] = all(
                p[1] - p[0] > 6 for p in sat_alive)
            with open(OUT, 'w') as f:
                json.dump(res, f, indent=0)
    log('e155b: done')


if __name__ == '__main__':
    main()
