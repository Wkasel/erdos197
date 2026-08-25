"""repro_sat_direct: step 3 of the reproducibility package (AUDIT A4).

Fresh direct SAT checks of the C3 core statement, using the independent
e115 audit encoder (own encoding + lazy transitivity refinement; SAT
verdicts are only accepted after full model validation -- total order
reconstruction, exhaustive AP scan, unit check):

    C3 UNSAT at M = 128 and M = 512   (M = 0 mod 8: the theorem)
    C3 SAT   at M = 132 and M = 516   (M = 4 mod 8: sharpness controls)

Run: .venv/bin/python experiments/repro_sat_direct.py [--fast]
     (--fast skips the two large scales; the package default runs all 4,
      ~7 minutes total)
Exit code 0 iff every verdict matches.
"""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from e115_audit_sat import solve


def C3(M):
    return [(2 * M - 5, M + 5), (2 * M - 3, M + 6), (2 * M - 10, M + 3)]


tests = [(128, "UNSAT"), (132, "SAT")]
if "--fast" not in sys.argv:
    tests += [(512, "UNSAT"), (516, "SAT")]

fails = []
for M, expect in tests:
    t0 = time.time()
    try:
        verdict, info = solve(M, C3(M))
    except AssertionError as ex:
        verdict, info = "ASSERT", repr(ex.args[:2])
    ok = verdict == expect
    print(f"  C3 at M={M}: {verdict} (expected {expect}) "
        f"[{time.time()-t0:.0f}s]{'' if ok else '  <-- MISMATCH'}",
        flush=True)
    if not ok:
        fails.append((M, verdict, expect))
if fails:
    print("FAILURES:", fails)
    sys.exit(1)
print("all verdicts match")
