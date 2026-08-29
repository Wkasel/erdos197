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

**bal@16 v=0 — FINAL** (data/e171_mus_bal_M16_v0_pin.json): n = 76 of
112, criticality 76 necessary / 0 redundant / 0 timeouts; re-verified
UNSAT by Glucose42 (pinned) AND Cadical UNPINNED.  Anatomy (bounds
(8, 8, 4)):
- B0 = [17..32] COMPLETE (bound 8 — exact balance);
- B1 = [37..56] ∪ [61..64] — the mid-band (2M+5, 3.5M] plus the TOP
  FOUR values (seam-2 source anchor); bottom four and (3.5M, 4M−4]
  deleted;
- B2 = [65..104] − {75, 76} − {101, 102} = (4M, 6M+8] with two
  2-holes at 4M+{11,12} and 6M+{5,6}; every mod-4 class in every
  block.  Top of support = 6M+8 — the flood centre 6M plus 8, far
  below the 7M−1 reachability cap.

**bal@24 v=0 — chunk-1 partial** (n = 103, still descending): B0 keeps
[31..33] ∪ [37..48] (bottom quarter deleted), B1 = [49..96] COMPLETE,
B2 = [97..118] ∪ [121..132] ∪ [145..150] — top of support 150 = 6M+6.
**The (M, 6M+O(1)] band law repeats at the second scale** (6M+8 vs
6M+6); which block keeps its full interval flips (B0 at 16, B1 at 24 —
path/balance trade, same three-part shape).

**bal@16 v=1, v=2 — partial** (both at chunk-8, n = 88): both have
shed exactly [105..128] — i.e. at every budget tested the FIRST
certified fact is support ⊆ (M, 6M+8], the v=0 band.  Interior
deletions (where the v-levels will diverge) are in the later passes.

**bal@16 v=4 — seed-chain verdicts (pod, certified)**: seed 0 (the
(16;6,0)-trace, n=42) SAT [0.0 s]; seed 1 (B0 + lower-3/4 B1 +
(4M,5.5M], n=64) SAT [0.1 s]; seed 2 (**B0 + B1 complete +
(4M,6M]**, n=80) **SAT [19.3 s]**.  So at v = 4 there is NO core
inside B0 ∪ B1 ∪ (4M, 6M] (with restriction-monotone bounds): the
v=4 core NEEDS B2 material ABOVE 6M — while the entire v=0 core
fits inside (M, 6M+8].  Seed 3 ((4M, 7M], n=96) still solving.

**bal@24 v=2 (pod)**: full window UNSAT [351.6 s pinned]; chunk-48
deletion running.

## 2b. The interim anatomy law (to be sharpened by the v=2/v=4 finals)

1. **Band law (v = 0, two scales)**: the balanced budget core is a
   THREE-BAND object — full/near-full B0-B1 seam material + a B2 band
   (4M, 6M+O(1)] ending just past the 6M flood centre.  The top
   (6M+O(1), 8M] — including the reachable (6M, 7M) — is REDUNDANT at
   v = 0.
2. **Budget growth law (first certified rung)**: raising the budget to
   v = 4 makes the (4M, 6M] band INSUFFICIENT (seed 2 SAT) — the
   core must recruit the deeper attack material z ∈ (6M, 7M) that
   v = 0 never needed.  Cross-triple arithmetic pins where that
   recruitment must sit: z = 2y − u > 6M forces y > 3M + u/2 (B1's
   top band) with u low in B0 — exactly the seam-2-source + low-B0
   material the v=0 anatomy already flags as its anchors.
3. Reading: each extra unit of affordable inversion deletes one seam
   edge lying in exactly one H-triple (notes/47 §3 injectivity), so
   the certificate must carry FRESH edge-disjoint H-demands per
   budget unit; the supply of such demands is the reachable band
   (4M, 7M) — Θ(M) deep.  The v*-growth mechanism visible here:
   v*(M) tracks the number of band layers the balanced coloring
   theory can force, and the band has Θ(M) layers — consistent with
   the measured v* escalation 5..6 (M=16) / ≥5 (M=24, ≤65) / ≤368
   (M=32).

## 3. The anatomy law: v = 2 vs v = 4 at M = 16

(pending)

## 4. Cross-scale: bal@24 v = 2 vs bal@16 v = 2

(pending)

## 5. The GAP-V*-schema seed (candidate parametric certificate family)

**CORE-BUDGET(M, v) [candidate, to be locked by the v=2/v=4 finals]:**
support S(M, v) = P0 ∪ P1 ∪ P2(v) with

    P0    = (M, 2M]                    (B0, complete or near-complete),
    P1    = (2M + c₁, 3.5M] ∪ (4M − c₂, 4M]   (B1 mid-band + top stub;
            widening toward all of B1 as v grows),
    P2(v) = (4M, 6M + c₃ + f(v)]      (B2 band; f(0) = O(1),
            f nondecreasing, f(v) ≤ M − c₃ — capped at the 7M−1
            reachability limit),

bounds = restriction-monotone balance (§1).  **Claim family:**
U(M; bal restricted to S(M, v); v, v) is UNSAT for every
v < v*(M), where v*(M) = the number of edge-disjoint H-demand
layers the band system forces — conjecturally Θ(M) (band depth).

Proof shape (one budget-layer up from notes/55's CORE′ engine,
exactly as notes/54 §2 predicted): (i) the notes/55 decomposition +
flood kills every coloring whose mono-H mass exceeds v outright;
(ii) the parity/range dodges (μ = 0 colorings) die by the MIXED
flood geometry as at v = 0 — a budget only buys seam-edge deletions,
and each deleted edge lies in EXACTLY ONE H-triple (notes/47 §3
injectivity), so a budget-v escape must nominate v specific triples
of the P2(v) ladder to break; (iii) the ladder is longer than v
(band supply), so some layer survives position-forced — UNSAT.
GAP-V*-schema = uniformize (i)-(iii) in (M, v); GAP-V*-growth =
show the forced-layer count diverges (the band-depth Θ(M) heuristic,
supported by the v* escalation 5..6 / ≥5 / ≤368 at 16/24/32).
