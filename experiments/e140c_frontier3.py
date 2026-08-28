"""e140c: completing the SS5 frontier map.

  - bounds (2,1,0) and (2,0,1) on CORE'(48) (the untested corners of
    the frontier law "escape iff min|U| = 0 or min|U| = min|Y| = 1");
  - H1(m): the seam-1 halved core [m+1, 2m] u [3m-7, 4m] (block
    order, AP-free, single team) — the reduction of the second
    parity alignment (notes/55 SS5.4) predicts UNSAT; a SAT here
    would falsify the reduction;
  - FG at M=64: double-fan kill scale-stability (top pair and
    band-bottom pair).

Run: .venv/bin/python experiments/e140c_frontier3.py
Log: data/e140c_frontier3.log
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from e136_u_decomp_check import solve_decomposed
from e140_bounds_probes import order_theory, fan_units


def main():
    print('== corners ==', flush=True)
    for bounds in ((2, 1, 0), (2, 0, 1)):
        v, el, info = solve_decomposed(48, bounds)
        line = f'  bounds {bounds}: {v} [{el}s]'
        if v == 'SAT':
            for team in 'AB':
                col = info[team]
                line += f' {team}[{len([x for x in col if x <= 96])},' \
                        f'{len([x for x in col if 96 < x <= 192])},' \
                        f'{len([x for x in col if x > 192])}]'
        print(line, flush=True)
    print('== H1(m): seam-1 halved core ==', flush=True)
    for m in (16, 24, 32, 40):
        W0 = list(range(m + 1, 2 * m + 1))
        W1 = list(range(3 * m - 7, 4 * m + 1))
        v, el = order_theory(W0 + W1, [], block_split=(W0, W1))
        print(f'  H1({m}) |W0|={len(W0)} |W1|={len(W1)}: {v} [{el}s]',
              flush=True)
    print('== FG at M=64 ==', flush=True)
    M = 64
    core = list(range(4 * M + 1, 6 * M + 16))
    for X in ((4 * M, 4 * M - 1), (3 * M - 15, 3 * M - 14),
              (4 * M,)):
        units = []
        for x in X:
            units += fan_units(M, x)
        v, el = order_theory(core, units)
        print(f'  FG(64; X={X}) units={len(units)}: {v} [{el}s]',
              flush=True)
    print('e140c: DONE', flush=True)


if __name__ == '__main__':
    main()
