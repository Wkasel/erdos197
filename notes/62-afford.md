# 62 — GAP-AFFORD: the 4-block downward gadget (GAP-JOINT first)

Task: L-AFFORD (notes/54 §4.3) — for every valid ε-linear pair,
liminf_N max_T Inv_T(N)/v*(N) < 1.  Attack per the measured gap
ordering (e130 check 3: the operative escape channel at small M is
DONATION plus a below-window exposure surface ~2× the in-window
mass): build the downward-extended gadget and measure what paying the
price at anchor N forces at anchor N/2.

Machine companion: experiments/e158_joint4.py →
data/e158_joint4.jsonl + data/e158_*.json/.log.

## 1. The instrument

Values (M/2, 8M], blocks Bm1 = (M/2, M], B0 = (M, 2M],
B1 = (2M, 4M], B2 = (4M, 8M].  Two overlapping 3-block windows:

    upper  W(M)   = (M, 8M]    seams s1 = B0→B1, s2 = B1→B2
    lower  W(M/2) = (M/2, 4M]  seams s0 = Bm1→B0, s1 = B0→B1

Per-team budgets vup on Inv(M) = #inverted s1 ∪ s2 pairs and vdn on
Inv(M/2) = #inverted s0 ∪ s1 pairs (s1 shared, counts in both).
Bounds: `bal` = exact balance in all four blocks (even sizes;
M ≡ 0 mod 4); `const` = 4-vector per-team lower bounds.  Complete
encoding (full transitivity per team; guarded APs both directions
over the WHOLE range (M/2, 8M] — this is what exposes the attack
surfaces of B0-donations from below; one-way indicators; seqcounter
cards).  Every SAT witness independently re-audited (bounds, per-team
monotone-AP freedom, per-seam recounts at both anchors, mono
cross-triple/inversion-edge cross-audit for BOTH windows'
H-families).  v = 'none' ⇒ that anchor unpriced (no indicators).

**Lemma T-FORCE-4 [PROVED — verbatim restriction, notes/54 Lemma
T-FORCE].**  A valid pair meeting the four block bounds at anchor M
with Inv_T(M) ≤ vup and Inv_T(M/2) ≤ vdn for both teams induces a
model.  Hence UNSAT(M; vup, vdn) ⟹ every valid pair meeting the
bounds has some team exceeding a budget at one of the two anchors.

**Lemma L-PROJ [PROVED — projection].**  Deleting all clauses that
mention Bm1-values from the 4-block instance yields exactly the
3-block e127 instance at anchor M (inversion indicators on s1, s2
unchanged; bounds on B0..B2 unchanged).  A 4-block model restricted
to (M, 8M] is therefore a 3-block model at the same vup.  So
SAT_4(vup, ·) ⟹ SAT_3(vup):  **v*_up-in-4-block ≥ v*_3(M)**, and
every 3-block UNSAT verdict transfers upward to the 4-block for
free.  Symmetrically, restricting to (M/2, 4M] shows
v*_dn-in-4-block ≥ v*_3(M/2).

## 2. Cell map and baselines

| cell | (vup, vdn) | question |
|------|-----------|----------|
| C0 | (none, none) | encoding sanity — finite theory SAT (notes/36) |
| C1 | (v, none) | does the dense block BELOW raise the anchor-M price past v*_3(M)? |
| C2 | (none, w) | anchor-M/2 price with B2-material present, upper unpriced (baseline) |
| C3 | (v, w) | THE PUMP — does paying at anchor M force > baseline at anchor M/2? |

Baselines measured this session:

- **v*(bal,8) = 0** [MACHINE-CHECKED, data/e158_bal8_base.log]: the
  standalone 3-block window at anchor 8 (blocks 8/16/32) is SAT at
  v = 0 — a seam-clean balanced escape exists, audit-passed.  The
  two-seam core does not yet fire at M = 8.  Consequence: at M = 16
  ANY forced vdn > 0 in the joint gadget is pure downward coupling —
  the standalone lower-anchor price is zero.
- 3-block v*(bal,16): UNSAT at v ≤ 2 (e127), pin-variant UNSAT at 4
  (pod3, data/fleet_2026-08-28/), SAT at 6 (e132 CP-SAT) ⟹
  v*(bal,16) ∈ {5,6}; Cadical SAT-side at v = 8/32 times out
  (17000/14400 s) — near-critical SAT hunting is the hard direction
  on this instance family.
- **C0 (M=16) SAT [0.3 s]**, audit clean; unpriced witness pays
  n_up = 528/358, n_dn = 44/92 (A/B) — lavish procrastination when
  free, exactly the §4 e127 asym phenomenology.

## 3. Verdicts (updated as cells land)

- **C2 (none, 0) @ M=16: SAT [0.8 s]** [MACHINE-CHECKED,
  data/e158_c2_M16_dn0.log].  With the upper anchor unpriced, BOTH
  teams are perfectly clean at the lower anchor — n_s0 = n_s1 = 0 for
  both — by dumping the entire procrastination mass onto seam s2
  (n_s2 = 392/442, far beyond any upper budget).  **The material of
  B2 alone forces nothing at anchor M/2; the baseline lower price in
  the 4-block geometry is 0.**  Every forced vdn > 0 in a priced cell
  is therefore attributable to the upper anchor's BUDGET, not to the
  presence of material — the attribution control the strong-L2
  refutation lacked.
- **C3 (vup=6, vdn=0) @ M=16: UNSAT [2.1 s]** [MACHINE-CHECKED,
  data/e158_c3_M16_up6_dn0.log].  THE HEADLINE CELL: with both
  anchors priced at values their standalone 3-block theories ALLOW
  (3-block bal@16 is SAT at v = 6, e132; standalone anchor-8 price is
  0, §2), the joint 4-block system is INFEASIBLE — and the UNSAT is
  three orders of magnitude faster than the near-critical 3-block
  queries (2 s vs hours), i.e. heavily overconstrained: the true
  joint frontier is far from the componentwise prices.  By
  T-FORCE-4: every valid balanced pair has, at anchor 16 vs 8, some
  team with Inv(16) > 6 or Inv(8) > 0.
- C1 attribution cell (vup=6, vdn=none) in flight.

## 4. What the pump can and cannot give at ω (worked out before C1
## landed; C1 only picks the channel)

Write I(N) = max_T Inv_T(N), f(N) = v*(N) (the 3-block floor).  Each
UNSAT cell (v, w) at scale M is, by T-FORCE-4, a forbidden rectangle
for the realized payment pair: ¬(I(M) ≤ v ∧ I(M/2) ≤ w).  Three
structural facts follow, one negative and two positive.

**NG4 [PROVED — inspection].  No family of forbidden RECTANGLES
(finite budgets at both anchors) can prove L-AFFORD by itself.**
Rectangles are bounded down-closed regions; the payment sequence
x_j = I(N₁·2^j) dodges every rectangle family by paying above it
(x_j = the rectangle's vup + 1 at every j — "overpay everywhere").
A contradiction at ω needs an UPPER bound on payments somewhere, and
budget cells only ever produce lower bounds.  The instrument's
ω-value is therefore demand REFINEMENT: joint floors strictly above
the per-anchor floors.  (This is the same lesson as NG1–NG3 one
level up: the ledger's closing argument must be denominated in the
joint currency — colored values / donations — not in any count of
inversions.  The C0 witness sharpens this: it pays n_up = 528 of a
possible ~640 pairs — a raw-count supply ceiling at window level is
near-VACUOUS; only priced-below inversions are expensive.  The
L-COMP/GAP-COMP raw-count route dies here as a window-level
statement: the composition trap must bind the priced structure, not
the count.)

**Floor bootstrapping (the C1 channel).**  A cell with vdn = none
(equivalently w ≥ the absolute pair cap ~10(M/2)² — the budget is
vacuous) is NOT a rectangle: UNSAT there forces I(M) > vup
unconditionally (within the 4-block bounds), i.e. it RAISES the
per-anchor floor beyond the 3-block v*.  Chains do the same one
step removed: if the forced lower payment w of a rectangle exceeds
the absolute cap at the half anchor, the rectangle degenerates to an
unconditional floor.  Deeper gadgets (5-block, 6-block …) can
bootstrap floors further.  Floors never reach the in-window cap (the
fully-unpriced instance is the notes/36 SAT theory), so bootstrapping
alone cannot close L-AFFORD either (NG4 again) — but a GROWING
sequence of true floors f₄(N) ≫ f₃(N) squeezes the eventual
donation-ledger argument from below and is measurable now.

**The pure-pump channel (the C3 − C2 difference).**  C2 SAT at
(none, 0) + C3 UNSAT at (6, 0) means: it is exactly the CHEAPNESS of
the upper payment that forces the lower payment.  Mechanism visible
in the seam anatomy: the shared seam s1 is doubly-priced currency —
every 3-block near-critical escape measured spends heavily on s1
(the v=160 witness pays 85/105 ENTIRELY on s1), and vdn = 0 outlaws
s1 spending, while cheap vup outlaws the s2 dump (the C2 escape used
n_s2 ≈ 400).  At ω: a valid pair CLEAN at anchor N/2 must overpay at
anchor N; a pair paying its bare floor at N must pay > 0 at N/2 even
where the standalone price is 0.  Payment obligations propagate DOWN
the anchor chain and cannot be everywhere-minimal.  Formally, for
every consecutive anchor pair, (I(N), I(N/2)) must clear the
measured staircase — the joint demand curve, strictly above the
componentwise floors (v*(16), v*(8)) = (5..6, 0) at the measured
point, since (6, 0) is forbidden.

**Consequence for the program.**  GAP-JOINT's machine question is
answered YES (the downward coupling IS real and priced), but the
correct reading is: the 4-block gadget is a DEMAND instrument, and
L-AFFORD cannot be closed by demand instruments (NG4).  What the
verdict buys: (i) the joint floors — every valid pair overpays
somewhere in every consecutive anchor pair — the quantitative
version of "the same value cannot serve two windows" (L-CASCADE) at
the level of budgets; (ii) the schema target is now a 2-scale UNSAT
family (the C3 cell at general M) of exactly the same species as the
N6a coupled core, one block deeper; (iii) the honest remaining
content of L-AFFORD is isolated: an upper bound on how often a
Θ(M)-dense team can overpay, which must be charged in donations
(single-use colored values), not in inversion counts.
