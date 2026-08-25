#!/bin/sh
# reproduce.sh -- reproducibility package for
#   "Structural rigidity in the Erdos-Graham two-set permutation problem"
#
# Verifies the machine-checked components of the main theorem
# (S_A = union of even dyadic blocks is not 3-permutable):
#
#   step 0  build the DRAT verifier (vendored drat-trim, MIT license)
#           and check the two unsatisfiability certificates for the C3
#           core (M = 128 eager/complete encoding; M = 512 lazy-audited),
#           plus an independent clause-by-clause audit of both CNFs
#   step 1  e113 hand-proof schema checker: executes every lemma
#           application of the Layer-1 and FLIP proofs (paper sec. "C3
#           core") with strict per-step assertions, representative scales
#   step 2  e113b closure-engine cross-validation (independent R1-R4 +
#           transitivity fixpoint, no knowledge of the proof schemas)
#   step 3  fresh direct SAT checks of the theorem statements, including
#           the mod-8 sharpness controls (SAT at M = 4 mod 8)
#
# Requirements: a C compiler (cc), and the Python venv at .venv with
# python-sat installed (python3 -m venv .venv && .venv/bin/pip install
# python-sat numpy).  Total runtime ~10-15 minutes.
#
# Exit code 0 iff every check passes.

set -e
cd "$(dirname "$0")"
PY=${PY:-.venv/bin/python}

echo "== step 0: DRAT certificates =="
if [ ! -x tools/drat-trim/drat-trim ]; then
    cc -std=c99 -O2 -o tools/drat-trim/drat-trim tools/drat-trim/drat-trim.c
fi
for M in 128 512; do
    gunzip -kf data/certs/c3_M$M.cnf.gz data/certs/c3_M$M.drat.gz
    if tools/drat-trim/drat-trim data/certs/c3_M$M.cnf data/certs/c3_M$M.drat \
        | grep -q "^s VERIFIED"; then
        echo "c3_M$M: s VERIFIED"
    else
        echo "c3_M$M: DRAT verification FAILED"; exit 1
    fi
done
$PY - <<'EOF'
import sys; sys.path.insert(0, "experiments")
from repro_drat_certs import audit_cnf
audit_cnf("data/certs/c3_M128.cnf", 128)
audit_cnf("data/certs/c3_M512.cnf", 512)
print("CNF clause audits OK (every clause is a C3 unit, a genuine")
print("in-block AP constraint, or a transitivity instance)")
EOF

echo "== step 1: hand-proof schema checker (e113) =="
$PY experiments/repro_e113_subset.py

echo "== step 2: closure-engine cross-validation (e113b) =="
$PY experiments/repro_e113b_subset.py

echo "== step 3: direct SAT spot checks + mod-8 sharpness =="
$PY experiments/repro_sat_direct.py "$@"

echo
echo "ALL CHECKS PASSED"
