"""e124k_b2_ladders: FRONT N2-OFF step 5b -- minimal Lemma-D ladder
sets closing the B2(11) halves at M = 2 mod 8 (m0 odd, phase value
t2 = 2M-2 even).

HALF-A2: {t5<b3, t7<b2} + (t2 < m0)   -> expect all branches closed
HALF-B2: {t2<b5, t5<b3} + (m0 < t2)   -> expect all branches closed

Run: .venv/bin/python experiments/e124k_b2_ladders.py [M ...]
"""
import itertools
import sys

from e124e_closure_halves import closure
from e124g_branch_closure import ladder, fiat_edges


def all_closed(M, seeds, ladders):
    lads = [ladder(*l) for l in ladders]
    for pol in itertools.product((True, False), repeat=len(lads)):
        ed = set(seeds)
        for lad, lf in zip(lads, pol):
            ed |= fiat_edges(lad, lf)
        if closure(M, ed)[0] != "contradiction":
            return False
    return True


def main():
    Ms = [int(a) for a in sys.argv[1:]] or [26, 34, 42, 50]
    for M in Ms:
        m0 = 3 * M // 2
        t2, t5, t7 = 2 * M - 2, 2 * M - 5, 2 * M - 7
        b2, b3, b5 = M + 2, M + 3, M + 5
        pool = {"O": (M + 1, 2, 2 * M - 1), "E": (M + 2, 2, 2 * M),
                "Q1": (M + 1, 4, 2 * M), "Q3": (M + 3, 4, 2 * M),
                "Q2": (M + 2, 4, 2 * M), "Q4": (M + 4, 4, 2 * M)}
        halves = {"A2": {(t5, b3), (t7, b2), (t2, m0)},
                  "B2": {(t2, b5), (t5, b3), (m0, t2)}}
        for hname, seeds in halves.items():
            found = []
            for sz in (1, 2, 3):
                for combo in itertools.combinations(pool, sz):
                    if any(set(f) <= set(combo) for f in found):
                        continue
                    if all_closed(M, seeds, [pool[k] for k in combo]):
                        found.append(combo)
                if found:
                    break
            print(f"M={M} ({M % 8} mod 8) HALF-{hname}: minimal ladder "
                  f"sets: {found}", flush=True)


if __name__ == "__main__":
    main()
