#!/bin/sh
# reproduce2.sh -- machine layer for the unconditional chain
#
#     C3(p)  ->  B1_0  ->  Lemma Q  ->  ALT-DEAD
#
# (full statements + proofs/pointers: notes/89-clean-chain.md; review
# remediation log: notes/88-review-remediation.md), plus the HSPLIT
# experiment in its DOWNGRADED reading (notes/88 item 1).
#
#   step 1  C3(p) schema executor (e123): strict rung-by-rung
#           execution of the Theorem C3(p) hand proof (Layer-1, FLIP,
#           complementary-class sharpness) at p = 5, 7, 9 -- three
#           values of p, ~100 scales each.
#   step 2  independent C3 solver (e123b): complete AP + transitivity
#           encoding, Cadical195, NO knowledge of the schema; C3(p)
#           UNSAT on the flip class / SAT on the complementary class /
#           full rung UNSAT, at p = 5, 9, 13 incl. M = 256/260.
#   step 3  sharp applicability boundaries (e180 partMINMsharp,
#           review-item-9 remediation): first-pass scales computed
#           from the scan and asserted equal to the sharp affine
#           values (L1: first 4 | M >= p+7; FLIP: in-class 2p+6),
#           below-threshold failures explicitly checked; p = 5, 13, 21.
#   step 4  Lemma Q chart checks + B1_0 machine layer (e186 qverify):
#           chart exactness phi(Lambda_c(t)) = B(t-2) (44 cells), AP
#           transport + midpoint-class (exhaustive, both directions),
#           C3(p)-units-in-rung (6 cells -- B1_0's a-fortiori step),
#           fresh rung UNSAT R(39,40;128), witness 4-purity; plus the
#           Geneson Lambda-scan (e186 geneson): Lemma Q predicts
#           finitely many full class-sections in the density-2/3
#           permutable W -- gate: no hits above the boot octaves
#           (t > 4).
#   step 5  HSPLIT experiment AS DOWNGRADED (e186 hsplit64 +
#           hsplit64ctl): strong-censor cells F = 64 at hor = 4096 and
#           2048.  Expected UNSAT.  READ AS: "every finite
#           strong-censor corner inhabitant has >= 1 monochromatic
#           residue-class section within the tested horizon" --
#           NOTHING MORE (no lattice claim, no omega claim; notes/88
#           item 1).
#   step 6  Lemma LAND + Theorem S1 recurrence check (e191, second
#           review item 2): the CORRECTED LAND bounds on 10^4 random
#           parameter tuples in BOTH sigma cases -- general bound
#           (|d|+g)/2 both signs, the halving refinement only at
#           sigma = +1 (and its FAILURE at sigma = -1 confirmed, incl.
#           the reviewer's q=1,p=4,g=3,tau=8,h=14 tuple) -- plus S1
#           re-verified by direct forced-spiral simulation on 10^4
#           fresh admissible tuples.
#
# Usage:  ./reproduce2.sh          (all steps; ~5-10 min total)
# Needs:  .venv with python-sat + ortools (see REPRODUCE.md).
# Exit code 0 iff every step passes.

cd "$(dirname "$0")" || exit 1
PY=${PY:-.venv/bin/python}
T0=$(date +%s)
FAIL=0

run_step() {
    name=$1; shift
    echo "== $name =="
    if "$@"; then
        echo "== $name: PASS =="
    else
        echo "== $name: FAIL =="
        FAIL=1
    fi
    echo
}

run_step "step1 C3(p) schema executor, p = 5,7,9" \
    "$PY" experiments/e123_diagonal_schema.py 9

run_step "step2 independent C3 solver, p = 5,9,13" \
    "$PY" experiments/e123b_diagonal_solver_xval.py 5 9 13

run_step "step3 sharp boundaries (partMINMsharp), p = 5,13,21" \
    "$PY" experiments/e180_diag_grow.py partMINMsharp

step4() {
    "$PY" experiments/e186_altclosure.py qverify geneson || return 1
    "$PY" - <<'EOF'
import json, sys
d = json.load(open("data/e186_altclosure.json"))
q = d["partQVERIFY"]
ok = True
def gate(name, cond):
    global ok
    print(f"  gate {name}: {'ok' if cond else 'FAIL'}")
    ok &= bool(cond)
gate("chart exactness 44 cells, 0 fail", q["chart_exact"]["fail"] == [])
gate("AP transport 0 fail", q["ap_transport"]["fail"] == 0)
gate("C3 units in rung, 6 cells, 0 fail", q["c3_units_in_R"]["fail"] == [])
gate("R(39,40;128) UNSAT (B1_0 rung layer)", q["R39_M128"] == "UNSAT")
g = d["partGENESON"]
gate("Geneson Lambda-scan: no full sections above boot (t > 4)",
     all(h["t"] <= 4 for h in g["hits"]))
sys.exit(0 if ok else 1)
EOF
}
run_step "step4 Lemma Q chart checks + B1_0 machine layer + Geneson scan" step4

step5() {
    "$PY" experiments/e186_altclosure.py hsplit64 hsplit64ctl || return 1
    "$PY" - <<'EOF'
import json, sys
d = json.load(open("data/e186_altclosure.json"))
rows = [r for r in d["partHSPLIT"] if r["F"] == 64 and r["k8"]]
new = {(r["hor"]): r["verdict"] for r in rows}
ok = new.get(4096) == "UNSAT" and new.get(2048) == "UNSAT"
print(f"  F=64 verdicts by horizon: {new} -> {'ok' if ok else 'FAIL'}")
if ok:
    print("  DOWNGRADED READING (notes/88 item 1): every finite")
    print("  strong-censor corner inhabitant has >= 1 monochromatic")
    print("  class-section within the tested horizon.  No lattice or")
    print("  omega conclusion follows from this experiment.")
sys.exit(0 if ok else 1)
EOF
}
run_step "step5 HSPLIT (downgraded reading), F = 64 x {4096, 2048}" step5

run_step "step6 Lemma LAND corrected bounds + Theorem S1 (10^4 x2 tuples)" \
    "$PY" experiments/e191_land_s1_check.py

echo "reproduce2 total: $(( $(date +%s) - T0 ))s; overall: $([ $FAIL -eq 0 ] && echo PASS || echo FAIL)"
exit $FAIL
