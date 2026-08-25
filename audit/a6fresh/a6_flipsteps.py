#!/usr/bin/env python3
"""AUDIT A6 — step-granular verification of the FLIP proof (notes/33 sec.5).

For each numbered step of Case I / Case II we check with the fresh SAT
encoder that the step's conclusion is FORCED by exactly the hypotheses the
proof claims it uses (assert the negation + those hypotheses -> UNSAT).
Case I hypotheses: AP-free, b5<b3, t5<m0 (+A3 for step 2, +A1 for step 4).
Case II hypotheses: AP-free, b5<b3, m0<t5 (+A2 for step 2, +A1 for step 4).
"""
import sys
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from a6_encoder import SatOrder, c3_pairs

def run(M):
    m0 = 3 * M // 2
    b = lambda j: M + j
    t = lambda i: 2 * M - i
    P = c3_pairs(M)
    A1, A2, A3 = P["A1"], P["A2"], P["A3"]
    b5b3 = P["b5<b3"]
    enc = SatOrder(M, eager_transitivity=True)
    CI = [b5b3, (t(5), m0)]            # Case I ambient
    CII = [b5b3, (m0, t(5))]           # Case II ambient
    checks = [
        # POLAR floods (sampled at three odd values each side)
        ("I.POLAR  odd<m0 (b9)",  CI + [(m0, b(9))]),
        ("I.POLAR  odd<m0 (t1)",  CI + [(m0, t(1))]),
        ("I.1  m0-1 < t10",       CI + [(t(10), m0 - 1)]),
        ("I.2  m0-1 < b3 (+A3)",  CI + [A3, (b(3), m0 - 1)]),
        ("I.3  m0-1 < t5 (+A3)",  CI + [A3, (t(5), m0 - 1)]),
        ("I.4  m0-1 < b5 (+A3,A1)", CI + [A3, A1, (b(5), m0 - 1)]),
        ("I.5  b5 < m0-1",        CI + [(m0 - 1, b(5))]),
        ("II.POLAR m0<odd (b9)",  CII + [(b(9), m0)]),
        ("II.1 b6 < m0+1",        CII + [(m0 + 1, b(6))]),
        ("II.2 t3 < m0+1 (+A2)",  CII + [A2, (m0 + 1, t(3))]),
        ("II.3 b5 < m0+1 (+A2)",  CII + [A2, (m0 + 1, b(5))]),
        ("II.4 t5 < m0+1 (+A2,A1)", CII + [A2, A1, (m0 + 1, t(5))]),
        ("II.5 m0+1 < t5",        CII + [(t(5), m0 + 1)]),
        # sanity: the ambient case assumptions alone are satisfiable
        ("sanity Case I ambient SAT",  ("SAT", CI)),
        ("sanity Case II ambient SAT", ("SAT", CII)),
    ]
    print(f"== FLIP step audit, M = {M} ==")
    allok = True
    for name, spec in checks:
        if isinstance(spec, tuple):
            expect, assum = spec
        else:
            expect, assum = "UNSAT", spec
        v, _ = enc.solve(assum)
        ok = "AGREE" if v == expect else "*** DISAGREE ***"
        allok &= (v == expect)
        print(f"   {name:28s} -> {v:6s} (expect {expect}) {ok}")
    return allok

if __name__ == "__main__":
    for M in [int(x) for x in sys.argv[1:]] or [48, 104]:
        run(M)
