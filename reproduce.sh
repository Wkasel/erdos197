#!/bin/sh
# reproduce.sh -- one-shot reproducibility package (AUDIT A4) for
#
#   "S_A = union of even dyadic blocks (2^{k-1}, 2^k] is not 3-permutable"
#   (paper/main.tex: thm:ogred -> thm:c3core -> thm:main)
#
# Five verification steps, each ending in an explicit PASS/FAIL line:
#
#   step 1  e113 hand-proof schema checker: executes every lemma
#           application of the notes/33 Layer-1 and FLIP proofs with
#           strict per-step assertions + hypothesis-discipline audit.
#           Scales: L1 at M = 12..100 step 4 and M = 512;
#                   FLIP at M = 16..104 step 8 and M = 512;
#                   plus M = 4 mod 8 schema-inapplicability sharpness.
#   step 2  e113b closure-engine cross-validation: every branch of the
#           hand proof re-closed by the INDEPENDENT e109 closure engine
#           (R1-R4 + transitivity fixpoint, no knowledge of the schemas).
#   step 3  fresh direct SAT checks (independent e115 encoder, lazy
#           transitivity, SAT models fully validated):
#           C3 UNSAT at M = 128, 512;  SAT controls at M = 132, 516.
#   step 4  DRAT certificates: RE-EMIT both C3-UNSAT certificates from
#           scratch via CaDiCaL proof logging through pysat Cadical153
#           (with_proof=True), clause-audit the CNFs from disk, verify
#           the proofs with the independent drat-trim checker (vendored
#           C source, built here), refresh data/certs/*.gz archives.
#   step 5  e96 reduction checks: gadget boundary arithmetic, the chunk
#           case-table, attack forcing, normalization, and a fresh
#           eager-encoding OG(128) UNSAT.
#
# Usage:   ./reproduce.sh          full run (see REPRODUCE.md for timing)
#          ./reproduce.sh --fast   skip the M >= 512 work (a few minutes)
# Needs:   .venv with python-sat + numpy (see REPRODUCE.md), a C compiler.
# Exit code 0 iff every step passes.

cd "$(dirname "$0")" || exit 1
PY=${PY:-.venv/bin/python}
T0=$(date +%s)
FAST=""
[ "$1" = "--fast" ] && FAST="--fast"

step() { echo; echo "===== step $1: $2 ====="; }
pass() { echo "PASS step $1  [$(( $(date +%s) - T0 ))s elapsed]"; }
fail() { echo "FAIL step $1"; echo "REPRODUCTION FAILED"; exit 1; }

step 0 "environment"
"$PY" --version || fail 0
"$PY" -c "import pysat, numpy; print('pysat + numpy importable')" || fail 0
if [ -f requirements-frozen.txt ]; then
    if "$PY" -m pip freeze | diff -q - requirements-frozen.txt >/dev/null 2>&1
    then echo "package versions match requirements-frozen.txt"
    else echo "WARNING: installed versions differ from requirements-frozen.txt"
         echo "         (non-fatal; exact pins are in that file)"
    fi
fi
pass 0

step 1 "e113 hand-proof schema checker (L1 M=12..100+512, FLIP M=16..104+512)"
"$PY" experiments/repro_e113_subset.py || fail 1
pass 1

step 2 "e113b closure-engine cross-validation (independent fixpoint engine)"
"$PY" experiments/repro_e113b_subset.py || fail 2
pass 2

step 3 "direct SAT: C3 UNSAT at M=128,512; SAT controls at M=132,516"
"$PY" experiments/repro_sat_direct.py $FAST || fail 3
pass 3

step 4 "DRAT certificates (fresh CaDiCaL proof logging + drat-trim verify)"
if [ -n "$FAST" ]; then SCALES="128"; else SCALES="128 512"; fi
"$PY" experiments/repro_drat_certs.py $SCALES || fail 4
if [ ! -x tools/drat-trim/drat-trim ]; then
    cc -std=c99 -O2 -o tools/drat-trim/drat-trim tools/drat-trim/drat-trim.c \
        || fail 4
fi
for M in $SCALES; do
    # NB: drat-trim precedes "s VERIFIED" with a bare \r (it erases its
    # progress line), so strip CRs before the anchored match.
    DTOUT=$(tools/drat-trim/drat-trim data/certs/c3_M$M.cnf \
                data/certs/c3_M$M.drat) \
        || { echo "  drat-trim c3_M$M: nonzero exit"; fail 4; }
    if printf '%s\n' "$DTOUT" | tr -d '\r' | grep -q "^s VERIFIED"
    then echo "  drat-trim c3_M$M: s VERIFIED"
    else echo "  drat-trim c3_M$M: verification FAILED"; fail 4
    fi
    gzip -9 -kfn data/certs/c3_M$M.cnf data/certs/c3_M$M.drat || fail 4
done
pass 4

step 5 "e96 reduction checks (gadget arithmetic, case table, OG(128) eager)"
E96OUT=$(mktemp "${TMPDIR:-/tmp}/e96.XXXXXX") || fail 5
"$PY" experiments/e96_reduction_check.py 2>&1 | tee "$E96OUT"
grep -q "TOTAL failures: 0" "$E96OUT" || { rm -f "$E96OUT"; fail 5; }
rm -f "$E96OUT"
pass 5

echo
echo "ALL CHECKS PASSED   (total wall time: $(( $(date +%s) - T0 ))s)"
