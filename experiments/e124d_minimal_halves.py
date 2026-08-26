"""e124d_minimal_halves: FRONT N2-OFF step 3b -- minimal premises of the
two half-flips of the {11,12} dyadic core A4a = {t0<b6,t1<b5,t2<b5,t3<b4}.

For every phase value v in {t0..t3} (position vs m0) and every subset S
of A4a's units: is AP + S + (v on the given side of m0) UNSAT?  Report
the minimal UNSAT subsets per (v, side).  Sweep several M = 0 mod 8 and
control scales M = 4 mod 8 (where A4a is SAT, so at least one side per
value must survive).

Run: .venv/bin/python experiments/e124d_minimal_halves.py [M ...]
"""
import itertools
import sys

from e124c_k4_anatomy import build, CORES


def main():
    Ms = [int(a) for a in sys.argv[1:]] or [24, 32, 40, 48, 28, 36]
    K = CORES["A4a"]
    for M in Ms:
        m0 = 3 * M // 2
        sol, sel, phase, o = build(M, K)
        print(f"M={M} ({M % 8} mod 8):")
        for (i, _) in [(0, 0), (1, 0), (2, 0), (3, 0)]:
            tv = 2 * M - i
            for ph in ("lo", "hi"):
                mins = []
                for sz in range(0, len(K) + 1):
                    for S in itertools.combinations(K, sz):
                        if any(set(m) <= set(S) for m in mins):
                            continue
                        if not sol.solve(
                                assumptions=[sel[u] for u in S]
                                + [phase[(tv, ph)]]):
                            mins.append(S)
                if mins:
                    pm = [" +".join(f"t{a}b{b}" for a, b in S) or "(none)"
                          for S in mins]
                    print(f"  t{i} {ph} (t{i} {'<' if ph == 'lo' else '>'}"
                          f" m0 positionally) killed by: {pm}")
        sol.delete()
    print("done")


if __name__ == "__main__":
    main()
