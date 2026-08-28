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
- **C1 (vup=6, vdn=none) @ M=16: SAT [364 s]** [MACHINE-CHECKED,
  data/e158_c1_M16_up6.log; witness audit-passed].  THE ATTRIBUTION
  IS CLEAN — this is the PURE PUMP, not a floor raise: vup = 6
  remains payable with the dense block below (so v*_up in the
  4-block geometry stays = v*_3(16) ≤ 6 at this cell), but the
  witness pays n_dn = 38 at the lower anchor (n_s0 = 32, n_s1 = 6,
  n_s2 = 0 — BOTH teams with identical anatomy).  Mechanism on
  display, exactly the predicted donation coupling: to pay only 6
  upward the coloring VOIDS the entire upper H-family (n_H_up = 0
  for both teams — the donation dodge of e130 check 3), and the
  donation pattern that voids H_up seeds 8 monochromatic H-triples
  in the LOWER window (n_H_dn = 8 each), whose forced breaking is
  lower-anchor payment (n_dn = 38 ≥ 8 = the μ_dn floor of this
  witness's coloring).  **Donations received in the window have
  their own attack surfaces exposed one block down — measured.**
- Verdict triangle at M = 16, cell (6, ·):
  (none,0) SAT / (6,none) SAT / (6,0) UNSAT — the joint frontier is
  strictly above both componentwise floors; pump bracket
  w_min(6) ∈ [1, 38], bisection in flight.

### 3b. C1 witness anatomy (hand-readable — the schema mechanism)

The (6, none) witness is the PARITY dodge of notes/47 §3 wearing its
cost openly (both teams mirror-identical):

- Coloring: Bm1 single-parity per team (A = {10,12,14,16},
  B = odds), B0 the OPPOSITE parity (A = odds 17..31), B2
  parity-matched to B0 so that H_up z-values 2y−u defect: **n_H_up
  = 0 with 82/78 upper triples broken by donating z** — the μ = 0
  coloring dodge, upper window voided for free.
- The clash lands in B1, which serves BOTH windows: it cannot be
  parity-pure for the upper dodge and the lower dodge at once (A's
  B1 = {33,36,37,40,41,...} mixed).  Residue: **8 mono H_dn triples
  per team** (A: (10|14, odd y, 4k) e.g. (10,23,36), (10,29,48)).
- Breaking them: ALL 8 via edge 1 (y ≺ u) — realized by WHOLESALE
  s0 reversal: all 32 = 4×8 in-team s0 pairs inverted (entire
  Bm1∩T placed after B0∩T), the "reverse the low block" escape of
  the e127 asym rows — lavish because the lower anchor is unpriced.
- Upper payment: n_s1 = 6 = vup exactly, all six inversions on ONE
  advanced B1-value (37 resp. 38 pulled before six B0-values).

**The μ-decomposition this suggests for the schema.**  Since a mono
H_dn triple can only be broken by an s0 or s1 edge, and each edge
lies in exactly one triple (notes/47 §3 injectivity, which holds
verbatim for the lower window), n_dn ≥ #mono-H_dn for every model.
Hence:
    (v, 0) SAT  ⟹  some balanced coloring has μ_dn = 0 (ZERO mono
    H_dn) AND upper-window order price ≤ v.
The C2 witness is exactly such a coloring (n_H_dn = 0, upper price
392); (6,0) UNSAT says **every zero-H_dn balanced coloring of
(M/2, 8M] has upper price > 6** — the two parity dodges (zero H_dn
vs zero H_up) clash on the shared blocks B0, B1, and v_min(0)
measures the price of resolving the clash in the upper window's
favor.  This is a two-layer coloring/order decomposition of exactly
the GAP-N6a species, one block deeper.

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

### 4b. GAP-COMP resolved as posed: the threshold count does not
### exist (parity orientation) [PROVED at gadget level]

GAP-COMP asked (notes/54 §4.3): how many compliant cross-block
forced descents force an AP-composable 2-path?  Answer: **no
sub-vacuous threshold exists.**  L-COMP says a valid order carries
NO AP 2-path ever (2-path ⟺ decreasing mono AP, e130 check 5), so
the question is extremal: how many compliant descents can a valid
order carry?  A parity-ORIENTED descent digraph (all descents from
odd values to even values, say) contains no AP 2-path structurally:
a 2-path c→b→a needs b even (as head of c→b) and b odd (as tail of
b→a) simultaneously.  Density is unrestricted — Θ(N²) descents are
compatible with parity orientation.  And this is not hypothetical:
the C1 witness REALIZES it — per team it carries 419/435 in-window
APs and 334/352 forced-descent edges with ZERO AP 2-paths
(recomputed directly), and its 8 AP-forced s0 descents all point
odd→even for A ((17..31) → {10,12,14,16}), even→odd for B — parity
orientation exactly.  So the L-COMP composition trap binds STRUCTURE
(which descents may coexist), never COUNTS; any counting-form
supply ceiling is dodged by parity orientation, exactly as μ is
dodged by parity coloring.  The surviving quantitative content of
GAP-COMP is absorbed into the joint 2-scale schema: the parity
dodge is free at ONE window and priced at the window below (§3b) —
composition pressure reappears as the DOWNWARD clash, not as an
in-window count.

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
