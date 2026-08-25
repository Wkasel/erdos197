"""e95b: (a) extend the OG threshold scan below M=30 to find the true
SAT/UNSAT flip (instance is clean for M >= 16: guards distinct from
bottoms and inside (M,2M] require M > 15); (b) cross-validate the key
adversarial odd-M findings of e95 with the independent EAGER
full-transitivity encoding (e94_step_check.eager_check).

Cross-validated claims (from e95, lazy encoding):
  M=43 (j*=3, H2 = 15fam+16{1,2}):
    - O1b REVERSED: H2 + (t21<t27) UNSAT  and  H2 + (t27<t21) SAT
    - b7<t2 undetermined: H2 + either orientation SAT
  M=41 (j*=2, H1 = 15fam+16{1}):
    - b5<t6 undetermined: H1 + either orientation SAT
    - O4a REVERSED: H1 + (t9<t11) UNSAT and H1 + (t11<t9) SAT

Output: data/uniformity_check_b.log
"""
import sys
import time

sys.path.insert(0, "/Users/will/Dev/personal/tasks/math/erdos197/experiments")
from e94_step_check import OG, eager_check  # noqa: E402

OUT = "/Users/will/Dev/personal/tasks/math/erdos197/data/uniformity_check_b.log"
fh = open(OUT, "w")
t0 = time.time()


def log(s=""):
    print(s, flush=True)
    fh.write(s + "\n")
    fh.flush()


# ---- (a) threshold scan M = 16..29, full attack set ----
log("== (a) full OG(M) threshold, M = 16..29 ==")
for M in range(16, 30):
    g = OG(M)
    r = g.solve(g.fam15() + g.pre16(8))
    log(f"  M={M}: {'SAT' if r else 'UNSAT'}   ({time.time()-t0:.0f}s)")
    g.sol.delete()

# ---- (b) eager cross-validation of e95 odd-M findings ----
log()
log("== (b) eager-encoding cross-validation ==")


def units_H(M, o, n16, extra):
    a = [o(2 * M + 2 * j - 15, M + j) for j in range(1, 8)]
    a += [o(2 * M + 2 * j - 16, M + j) for j in range(1, n16 + 1)]
    return a + [o(*p) for p in extra]


checks = [
    # (M, n16, extra-pairs, expected SAT, label)
    (43, 2, [(2 * 43 - 21, 2 * 43 - 27)], False,
     "M=43 H2+(t21<t27) UNSAT (O1b reversed)"),
    (43, 2, [(2 * 43 - 27, 2 * 43 - 21)], True,
     "M=43 H2+(t27<t21) SAT"),
    (43, 2, [(43 + 7, 2 * 43 - 2)], True,
     "M=43 H2+(b7<t2) SAT (chain literal undetermined)"),
    (43, 2, [(2 * 43 - 2, 43 + 7)], True,
     "M=43 H2+(t2<b7) SAT"),
    (41, 1, [(41 + 5, 2 * 41 - 6)], True,
     "M=41 H1+(b5<t6) SAT (invariant undetermined)"),
    (41, 1, [(2 * 41 - 6, 41 + 5)], True,
     "M=41 H1+(t6<b5) SAT"),
    (41, 1, [(2 * 41 - 9, 2 * 41 - 11)], False,
     "M=41 H1+(t9<t11) UNSAT (O4a reversed)"),
    (41, 1, [(2 * 41 - 11, 2 * 41 - 9)], True,
     "M=41 H1+(t11<t9) SAT"),
]
allok = True
for M, n16, extra, expect, label in checks:
    r = eager_check(M, lambda MM, o: units_H(MM, o, n16, extra))
    ok = (r == expect)
    allok &= ok
    log(f"  {label}: eager SAT={r}  {'AGREE' if ok else 'MISMATCH!!'}"
        f"   ({time.time()-t0:.0f}s)")
log(f"  cross-validation {'PASSED' if allok else 'FAILED'}")
fh.close()
