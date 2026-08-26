"""e124o_odd_ladders: FRONT N2-OFF step 7b -- two-ladder Lemma-D
closure for the ODD-class schema candidate (lane C at x = 11,
M = 5 mod 8, center c- = (3M-1)/2, battleground t2 = 2M-2):

  HALF-hi: {t2<b5, t5<b3} + (t2 < c-)   [expect closed]
  HALF-lo: {t0<b6, t2<b5} + (c- < t2)   [expect closed]

Controls at the other odd classes (1, 3, 7 mod 8) where C(11) is SAT:
some branch must survive.

Run: .venv/bin/python experiments/e124o_odd_ladders.py [M ...]
"""
import itertools
import sys

from e124e_closure_halves import closure
from e124g_branch_closure import ladder, fiat_edges


def branches(M, seeds, lkeys, pool):
    lads = [ladder(*pool[k]) for k in lkeys]
    surv = 0
    for pol in itertools.product((True, False), repeat=len(lads)):
        ed = set(seeds)
        for lad, lf in zip(lads, pol):
            ed |= fiat_edges(lad, lf)
        if closure(M, ed)[0] != "contradiction":
            surv += 1
    return surv


def main():
    Ms = [int(a) for a in sys.argv[1:]] or [29, 37, 45, 53]
    for M in Ms:
        cm = (3 * M - 1) // 2
        t0, t2, t5 = 2 * M, 2 * M - 2, 2 * M - 5
        b3, b5, b6 = M + 3, M + 5, M + 6
        pool = {"D1": (M + 1, 2, 2 * M), "D2": (M + 2, 2, 2 * M),
                "Q1": (M + 1, 4, 2 * M), "Q2": (M + 2, 4, 2 * M),
                "Q3": (M + 3, 4, 2 * M), "Q4": (M + 4, 4, 2 * M)}
        halves = {"hi": {(t2, b5), (t5, b3), (t2, cm)},
                  "lo": {(t0, b6), (t2, b5), (cm, t2)}}
        for hn, seeds in halves.items():
            found = []
            for sz in (2, 3):
                for combo in itertools.combinations(pool, sz):
                    if any(set(f) <= set(combo) for f in found):
                        continue
                    if branches(M, seeds, combo, pool) == 0:
                        found.append(combo)
                if found:
                    break
            print(f"M={M} ({M % 8} mod 8) HALF-{hn}: closing ladder "
                  f"sets: {found}", flush=True)


if __name__ == "__main__":
    main()
