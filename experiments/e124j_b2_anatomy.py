"""e124j_b2_anatomy: FRONT N2-OFF step 5 -- same pipeline for the
= 2 mod 4 flip class: core B2(11) = {t2<b5, t5<b3, t7<b2}, law
M = 2 mod 8 (m0 = 3M/2 is ODD here).

Step 1 (this file): minimal phase-kill premises -- for each subset S of
the core and each core t-value v, is AP + S + (v on a side of m0)
UNSAT?  Then branch closure with Lemma-D ladder sets from the pool
O/E/Q1-4 on the minimal kills found.

Run: .venv/bin/python experiments/e124j_b2_anatomy.py [M ...]
"""
import itertools
import sys

from e124c_k4_anatomy import build
from e124e_closure_halves import closure
from e124g_branch_closure import ladder, fiat_edges

B2 = [(2, 5), (5, 3), (7, 2)]


def phase_scan(Ms):
    for M in Ms:
        sol, sel, phase, o = build(M, B2)
        print(f"M={M} ({M % 8} mod 8):")
        for (i, j) in B2 + [(1, 0), (3, 0), (9, 0), (0, 0)]:
            tv = 2 * M - i
            if tv == 3 * M // 2:
                continue
            for ph in ("lo", "hi"):
                mins = []
                for sz in range(0, len(B2) + 1):
                    for S in itertools.combinations(B2, sz):
                        if any(set(m) <= set(S) for m in mins):
                            continue
                        if not sol.solve(
                                assumptions=[sel[u] for u in S]
                                + [phase[(tv, ph)]]):
                            mins.append(S)
                if mins:
                    pm = [" +".join(f"t{a}b{b}" for a, b in S) or "(none)"
                          for S in mins]
                    print(f"  t{i} {ph}: killed by {pm}")
        sol.delete()


def branch_closure(Ms, seeds_fn, name, ladder_keys):
    for M in Ms:
        pool = {"O": (M + 1, 2, 2 * M - 1), "E": (M + 2, 2, 2 * M),
                "Q1": (M + 1, 4, 2 * M), "Q3": (M + 3, 4, 2 * M),
                "Q2": (M + 2, 4, 2 * M), "Q4": (M + 4, 4, 2 * M)}
        lads = [ladder(*pool[k]) for k in ladder_keys]
        surv = []
        for pol in itertools.product((True, False), repeat=len(lads)):
            ed = set(seeds_fn(M))
            for lad, lf in zip(lads, pol):
                ed |= fiat_edges(lad, lf)
            if closure(M, ed)[0] != "contradiction":
                surv.append(pol)
        print(f"M={M} {name} [{'+'.join(ladder_keys)}]: "
              f"{2**len(lads)-len(surv)}/{2**len(lads)} closed"
              + ("  == ALL ==" if not surv else f" surv {surv[:3]}"),
              flush=True)


if __name__ == "__main__":
    Ms = [int(a) for a in sys.argv[1:]] or [18, 26, 34, 42, 22, 30]
    phase_scan(Ms)
