# 68 — FRONT BUDGET-MUS: anatomy of the budget cores (GAP-V*-schema seed)

Task: apply the campaign MUS playbook (e126/e158b) to the e127 BUDGET
instance U(M; bal; v, v) — the T-FORCE demand curve's UNSAT region
(notes/54 §1-2).  Near-critical decision queries are hopeless (pin16
v=5 TIMEOUT 40000 s; bal24 v=8/16 TIMEOUT); the lower-bound route is
ANATOMY: extract deletion-minimal value supports of the UNSAT at
budgets v = 2 and v = 4 at M = 16, compare, and read off WHAT GROWS
as the budget rises.  The growth mechanism of the support IS the
v*-growth mechanism (each extra affordable inversion must be re-taxed
by extra material), and the stable part across (M, v) is the
GAP-V*-schema seed.

Machine: experiments/e171_budget_mus.py →
data/e171_mus_bal_M{M}_v{v}_pin.json (+ .resume.json, .log); seeds
data/e171_seeds_M16_v4.json.

## 1. The instrument (soundness notes)

e127's solve_budget with three changes, every one carrying a proof
obligation discharged here:

- **Support restriction, restriction-monotone bounds (e158b
  verbatim).**  bound_i = max(0, |full B_i|/2 − #deleted_i).  Any
  model of the full instance restricts to a model of the support
  instance: induced colors meet the lowered bounds (at most
  #deleted_i members of a team can vanish from block i), and the
  induced order's adjacent-seam inversion pairs are a SUBSET of the
  original's (both members survive or the pair is gone), so budgets
  (v, v) still hold.  Contrapositive: support UNSAT ⟹ full UNSAT —
  every deletion step is a certified strengthening, and the final
  support is a standalone finite theorem:
  "no 2-coloring of THESE values meeting the listed per-block bounds
  admits per-team orders with ≤ v adjacent-seam inversions each."
- **Color-swap pin (the pod3_pin16 trick, WLOG).**  With symmetric
  budgets (v, v) and identical per-team bounds, the global color swap
  A ↔ B is an instance automorphism; pinning the smallest surviving
  value to team A halves the search.  Pinned UNSAT ⟺ unpinned UNSAT.
  Measured speedup ~3× (bal@16 v=1: 7.5 s pinned vs 24.0 s in e127).
  Final supports are re-verified UNPINNED (Cadical) + pinned
  (Glucose42) — two solvers, two symmetry settings.
- **Crash-safe resumability (e126 verbatim).**  Snapshot after every
  accepted drop and every criticality step; rerun re-verifies the
  snapshot UNSAT before continuing.  TIMEOUT trials = "cannot drop"
  (recorded; a timeout can only make the final support LARGER, never
  unsound).

Targets and per-solve baselines (data/e127_seam_budget.jsonl +
fleet_2026-08-28):

| target | full-window solve | status |
|--------|------------------|--------|
| bal@16 v=2 | UNSAT 243.6 s (unpinned) | local run |
| bal@16 v=4 | UNSAT ~5500 s (pinned, pod3) | pod run, seeded |
| bal@24 v=2 | UNSAT 433.5 s (pod3) | pod run |

Seeding (the "restrict cleverly" of the task): the v=4 run starts
from an ascending chain of candidate supports (first UNSAT wins,
else full window): (0) the notes/62 (16; 6,0)-MUS trace intersected
with the 3-block window, n = 42; (1) B0 + lower-3/4 B1 + bottom-3/8
B2, n = 64; (2) B0 + B1 + (4M, 6M], n = 80; (3) B0 + B1 + reachable
B2 (4M, 7M], n = 96.  A seed that verifies UNSAT is itself already a
certified restriction — the chain then continues by chunked greedy
deletion from there.

## 2. Results (filled in as runs land)

(pending)

## 3. The anatomy law: v = 2 vs v = 4 at M = 16

(pending)

## 4. Cross-scale: bal@24 v = 2 vs bal@16 v = 2

(pending)

## 5. The GAP-V*-schema seed (candidate parametric certificate family)

(pending)
