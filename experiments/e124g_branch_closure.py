"""e124g_branch_closure: FRONT N2-OFF step 3e -- do the two half-flips
of the {11,12} dyadic core close under Lemma-D case analysis + pure
zigzag propagation?

For each half: assume the premises + the phase hypothesis, case-split
on the zigzag polarity of the ODD ladder (M+1, +2) and EVEN ladder
(M+2, +2) (Lemma D: every d-ladder alternates leader/trailer, exactly
two phases), add those fiat edges, close under AP rules R1-R4 +
transitivity.  Contradiction in all 4 branches = the hand schema is
pure (D + propagation).  If some branch survives, escalate: add the
mod-4 ladders lad4(M,1)/lad4(M,3) (odd values) and lad4(M,2)/lad4(M,4)
(even values) polarities as further splits and report the minimal
ladder set that closes every branch.

Controls at M = 4 mod 8: SOME branch must survive (the core is SAT
there) for each half whose phase kill is 0-mod-8-only.

Run: .venv/bin/python experiments/e124g_branch_closure.py [M ...]
"""
import itertools
import sys

from e124e_closure_halves import closure


def ladder(first, d, last):
    out = []
    v = first
    while v <= last:
        out.append(v)
        v += d
    return out


def fiat_edges(lad, leader_first):
    e0 = 0 if leader_first else 1
    ed = set()
    for i in range(e0, len(lad), 2):
        if i > 0:
            ed.add((lad[i], lad[i - 1]))
        if i + 1 < len(lad):
            ed.add((lad[i], lad[i + 1]))
    return ed


def run_half(M, name, seeds, ladders):
    """Case-split over polarity of each ladder in `ladders`; return the
    list of surviving branch polarity-tuples."""
    lads = [ladder(*l) for l in ladders]
    surviving = []
    for pol in itertools.product((True, False), repeat=len(lads)):
        ed = set(seeds)
        for lad, lf in zip(lads, pol):
            ed |= fiat_edges(lad, lf)
        r = closure(M, ed)
        if r[0] != "contradiction":
            surviving.append(pol)
    return surviving


def main():
    Ms = [int(a) for a in sys.argv[1:]] or [24, 32, 40, 28, 36]
    for M in Ms:
        m0 = 3 * M // 2
        t0, t1, t2, t3 = 2 * M, 2 * M - 1, 2 * M - 2, 2 * M - 3
        b4, b5, b6 = M + 4, M + 5, M + 6
        halves = {
            "A": {(t0, b6), (t2, b5), (t1, m0)},
            "B": {(t1, b5), (t3, b4), (m0, t1)},
        }
        lsets = {
            "odd+even": [(M + 1, 2, 2 * M - 1), (M + 2, 2, 2 * M)],
            "odd+even+g4": [(M + 1, 2, 2 * M - 1), (M + 2, 2, 2 * M),
                            (M + 1, 4, 2 * M), (M + 3, 4, 2 * M),
                            (M + 2, 4, 2 * M), (M + 4, 4, 2 * M)],
        }
        for hname, seeds in halves.items():
            for lname, ladders in lsets.items():
                surv = run_half(M, hname, seeds, ladders)
                tot = 2 ** len(ladders)
                print(f"M={M} ({M % 8} mod 8) HALF-{hname} [{lname}]: "
                      f"{tot - len(surv)}/{tot} branches closed"
                      + (f", surviving {surv[:4]}" if surv else
                         "  == ALL CLOSED =="), flush=True)
                if not surv:
                    break


if __name__ == "__main__":
    main()
