"""e124n_odd_probe: FRONT N2-OFF step 7 -- first probe of the ODD
residue classes (lane C, law M = x+2 mod 8).  No integer m0 = 3M/2
exists; test whether the phase battleground moves to the half-integer
neighbours c- = (3M-1)/2 and c+ = (3M+1)/2.

For C(11) = {t0<b6, t2<b5, t5<b3} at M = 5 mod 8 (its firing class):
for each candidate battleground value v (top t's) and each center
c in {c-, c+}: minimal subsets S with AP + S + (v before/after c)
UNSAT.  A double kill (both sides killed by subsets of the core)
means the even-class template survives the parity change with c as
the center; then search two-ladder closing sets.

Run: .venv/bin/python experiments/e124n_odd_probe.py [M ...]
"""
import itertools
import sys

from pysat.solvers import Cadical195

C11 = [(0, 6), (2, 5), (5, 3)]


def build(M, units):
    n = M
    var = {}
    c = 0
    for p in range(n):
        for q in range(p + 1, n):
            c += 1
            var[(p, q)] = c

    def o(u, w):
        p, q = u - M - 1, w - M - 1
        return var[(p, q)] if p < q else -var[(q, p)]

    cl = []
    for y in range(M + 2, 2 * M):
        d = 1
        while y + d <= 2 * M and y - d > M:
            a, b = y - d, y + d
            cl.append([-o(a, y), -o(y, b)])
            cl.append([-o(b, y), -o(y, a)])
            d += 1
    for p in range(n):
        for q in range(p + 1, n):
            for r in range(q + 1, n):
                cl.append([-var[(p, q)], -var[(q, r)], var[(p, r)]])
                cl.append([var[(p, q)], var[(q, r)], -var[(p, r)]])
    sel = {}
    nv = c
    for (i, j) in sorted(units):
        z, y = 2 * M - i, M + j
        nv += 1
        sel[(i, j)] = nv
        cl.append([o(z, y), -nv])
    return Cadical195(bootstrap_with=cl), sel, o


def main():
    Ms = [int(a) for a in sys.argv[1:]] or [21, 29, 37, 45]
    for M in Ms:
        cm, cp = (3 * M - 1) // 2, (3 * M + 1) // 2
        sol, sel, o = build(M, C11)
        print(f"M={M} ({M % 8} mod 8): c-={cm} c+={cp}")
        for i in range(0, 8):
            tv = 2 * M - i
            for cname, cv in (("c-", cm), ("c+", cp)):
                if tv == cv:
                    continue
                for side, lit in (("before", o(tv, cv)),
                                  ("after", o(cv, tv))):
                    mins = []
                    for sz in range(1, len(C11) + 1):
                        for S in itertools.combinations(C11, sz):
                            if any(set(m) <= set(S) for m in mins):
                                continue
                            if not sol.solve(
                                    assumptions=[sel[u] for u in S]
                                    + [lit]):
                                mins.append(S)
                    if mins:
                        pm = ["+".join(f"t{a}b{b}" for a, b in S)
                              for S in mins]
                        print(f"  t{i} {side} {cname}: killed by {pm}")
        sol.delete()
    print("done")


if __name__ == "__main__":
    main()
