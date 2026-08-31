#!/usr/bin/env python
"""Adversary C independent spot-checks (fresh encodings)."""
import itertools, sys
from pysat.solvers import Cadical195
from pysat.formula import IDPool

def solve(n_vals, vals, extra_units, apfree=True):
    """vals: list of ints. Order vars o[a][b] = a precedes b."""
    pool = IDPool()
    V = lambda a, b: pool.id(('o', a, b)) if a < b else -pool.id(('o', b, a))
    cls = []
    # transitivity (eager)
    for a, b, c in itertools.combinations(vals, 3):
        cls.append([-V(a, b), -V(b, c), V(a, c)])
        cls.append([V(a, b), V(b, c), -V(a, c)])
    S = set(vals)
    if apfree:
        for b in vals:
            for a in vals:
                if a >= b: continue
                c = 2 * b - a
                if c in S:
                    # forbid a<b<c and c<b<a in position order
                    cls.append([-V(a, b), -V(b, c)])
                    cls.append([-V(c, b), -V(b, a)])
    for (u, v) in extra_units:
        cls.append([V(u, v)])
    s = Cadical195(bootstrap_with=cls)
    r = s.solve()
    s.delete()
    return r

def Z(M):
    vals = list(range(M + 1, 2 * M + 1))
    units = []
    for y in vals:
        for z in vals:
            if z <= y: continue
            x = 2 * y - z
            if M // 4 < x <= M // 2 and x * 4 > M:  # x in (M/4, M/2]
                units.append((z, y))
    return solve(len(vals), vals, units)

def C3(M):
    vals = list(range(M + 1, 2 * M + 1))
    t = lambda i: 2 * M - i
    b = lambda j: M + j
    units = [(t(5), b(5)), (t(3), b(6)), (t(10), b(3))]
    return solve(len(vals), vals, units)

def OG(M):
    vals = list(range(M + 1, 2 * M + 1))
    t = lambda i: 2 * M - i
    b = lambda j: M + j
    units = []
    for x in (15, 16):
        for j in range(1, x // 2 + 1):
            units.append((t(x - 2 * j), b(j)))
    return solve(len(vals), vals, units)

if __name__ == '__main__':
    print("== lem:bases  Z(M) for 16<=M<=31 (expect all UNSAT) ==")
    bad = []
    for M in range(12, 32):
        r = Z(M)
        print(f"  Z({M}) = {'SAT' if r else 'UNSAT'}")
        if M >= 16 and r: bad.append(M)
    print("  VIOLATIONS:", bad)

    print("== C3 core: expect UNSAT iff M=0 mod 8 ==")
    for M in range(16, 73):
        r = C3(M)
        exp = (M % 8 != 0)
        flag = "" if r == exp else "   *** MISMATCH ***"
        if not r or M % 8 in (0, 4):
            print(f"  M={M:3d} {'SAT' if r else 'UNSAT'}{flag}")
        elif r != exp:
            print(f"  M={M:3d} {'SAT' if r else 'UNSAT'}{flag}")
    print("== OG(M) 16..60 (expect UNSAT) ==")
    print("  ", [M for M in range(16, 61) if OG(M)], "<- SAT scales (want empty)")

    print("== densities of S_A ==")
    SA = set()
    n = 2 ** 22
    k = 2
    while 2 ** (k - 1) < n:
        for v in range(2 ** (k - 1) + 1, min(2 ** k, n) + 1):
            SA.add(v)
        k += 2
    c = 0; up = 0.0; lo = 1.0
    for v in range(1, n + 1):
        if v in SA: c += 1
        if v > 1000:
            up = max(up, c / v); lo = min(lo, c / v)
    print(f"  k>=2:  upper={up:.6f} lower={lo:.6f}  |SA cap [1,16]|={len([v for v in SA if v<=16])}  |SA cap [1,64]|={len([v for v in SA if v<=64])}")

def L1_check(M):
    """AP-free + A2 + A3 + (b3 < b5)  should be UNSAT for M = 0 mod 4."""
    vals = list(range(M + 1, 2 * M + 1))
    t = lambda i: 2 * M - i; b = lambda j: M + j
    return solve(len(vals), vals, [(t(3), b(6)), (t(10), b(3)), (b(3), b(5))])

def FLIP_check(M):
    """AP-free + A2 + A3 + (b5 < b3) + A1  should be UNSAT for M = 0 mod 8."""
    vals = list(range(M + 1, 2 * M + 1))
    t = lambda i: 2 * M - i; b = lambda j: M + j
    return solve(len(vals), vals, [(t(3), b(6)), (t(10), b(3)), (b(5), b(3)), (t(5), b(5))])
