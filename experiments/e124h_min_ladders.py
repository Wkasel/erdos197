"""e124h_min_ladders: FRONT N2-OFF step 3f -- minimal Lemma-D ladder
sets that close every polarity branch of the two half-flips, at several
M = 0 mod 8 (want a scale-uniform minimal set for the hand statement).

Ladder pool: O = odd d2, E = even d2, Q1/Q3/Q2/Q4 = the four mod-4
value-class d4 ladders.

Run: .venv/bin/python experiments/e124h_min_ladders.py [M ...]
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
    Ms = [int(a) for a in sys.argv[1:]] or [32, 40, 48, 56]
    for M in Ms:
        m0 = 3 * M // 2
        t0, t1, t2, t3 = 2 * M, 2 * M - 1, 2 * M - 2, 2 * M - 3
        b4, b5, b6 = M + 4, M + 5, M + 6
        pool = {"O": (M + 1, 2, 2 * M - 1), "E": (M + 2, 2, 2 * M),
                "Q1": (M + 1, 4, 2 * M), "Q3": (M + 3, 4, 2 * M),
                "Q2": (M + 2, 4, 2 * M), "Q4": (M + 4, 4, 2 * M)}
        halves = {"A": {(t0, b6), (t2, b5), (t1, m0)},
                  "B": {(t1, b5), (t3, b4), (m0, t1)}}
        for hname, seeds in halves.items():
            found = []
            for sz in (1, 2, 3, 4):
                for combo in itertools.combinations(pool, sz):
                    if any(set(f) <= set(combo) for f in found):
                        continue
                    if all_closed(M, seeds, [pool[k] for k in combo]):
                        found.append(combo)
                if found:
                    break
            print(f"M={M} HALF-{hname}: minimal closing ladder sets: "
                  f"{found}", flush=True)


if __name__ == "__main__":
    main()
