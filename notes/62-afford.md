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
- **v*(bal,12) = 0** [MACHINE-CHECKED, data/e158_bal12_base.log]:
  the standalone half-anchor of M = 24 is free too (seam-clean
  balanced escape, audit-passed) — the M = 24 pump cells have the
  same clean shape as M = 16 (any forced vdn > 0 is pure coupling).

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

- **C2@24 (none, 0): SAT [20.6 s]** [MACHINE-CHECKED,
  data/e158_c2_M24_dn0.log].  Scale-2 replica of the M = 16 shape:
  both teams clean at the lower anchor (n_s0 = n_s1 = 0), s2 dump
  n_s2 = 894/913, n_H_dn = 0 (L-PREFIX part (i) again exact).
  Baseline lower price 0 at scale 24.
- **HEADLINE C3@24 (65, 0): UNSAT [46 s]** [MACHINE-CHECKED,
  data/e158_c3_M24_up65_dn0.log].  Scale-stability: with the pod's
  known 3-block SAT point v = 65 at anchor 24 (fleet_2026-08-28
  pod1, CP-SAT feasible) and the free standalone half-anchor
  (v*(bal,12) = 0), the joint (65, 0) cell is INFEASIBLE.
  Certified independently of the pod witness's auditability:
  **v_min(0)(24) > 65** while v_min(0)(16) > 6 — the
  free-lower-anchor price exceeds the entire measured 3-block
  bracket at 24 (v*₃(24) ∈ (4, 65]).  The 2-scale UNSAT family
  [GAP-J-schema] is machine-true at M = 16 AND 24.

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
(M/2, 8M] has upper price > 6**, and v_min(0) measures that price.
CAVEAT (important, notes/47 §3's warning applies verbatim): zero
mono-H at BOTH windows simultaneously is cheap at the coloring
level — the block-parity schedule (odd, even, even, odd) voids both
H-families outright, and the standalone bal@8 v=0 witness is
zero-H with a seam-clean order — so the (6,0) death does NOT ride H
alone; the mixed in-block shapes under the lower block-order are
what tax the upper window.  H gives the necessary-condition frame
(n_dn ≥ #mono-H_dn via edge injectivity), the MUS must expose the
mixed engine.  Still a two-layer coloring/order decomposition of
exactly the GAP-N6a species, one block deeper.

### 3c. Pre-registered MUS prediction (BEFORE e158b runs on (6,0))

By analogy with the e126 M=32 support anatomy (notes/48 prediction,
confirmed) and the §3b mechanism: the (16; 6, 0) deletion-minimal
value support should show (i) Bm1 present as seam-anchor material
(the s0 block-order clauses need Bm1×B0 in-team pairs); (ii) B0
nearly whole — it is the shared currency block (upper window's
bottom + lower window's middle); (iii) B1 weighted to its LOWER
half (both windows' active zone; upper H-middles y with 2y−u ≤ 7M
and lower H-tops); (iv) B2 confined to the reachable bottom
(support ∩ B2 ⊆ (4M, 7M] = (64, 112], the 2y−u image), top eighth
absent.  Committed before the run.

### 3d. The (16; 6, 0) MUS landed — 50 values, fully critical

e158b (data/e158b_mus_M16_up6_dn0.json): deletion-minimal support
n = 50 of 120, criticality certificate **50 necessary / 0
redundant**.  Anatomy vs the §3c blind prediction (4/4 confirmed,
(iv) much sharper):

- Bm1 = [9..16] COMPLETE (bound 4 — exact balance intact);
- B0 = [17..32] COMPLETE (bound 8) — the shared currency block is
  wholly load-bearing, as predicted;
- B1 = [33..55] minus {36, 40, 52} — the lower two-thirds with
  three punctures (bound relaxed to 4);
- B2 = [65..70] — a SIX-value stub at the very bottom of B2
  (bound 0: B2's balance is irrelevant; the stub is pure attack
  material).  The upper window's H/AP theory enters ONLY through
  z-values in (4M, 4M+6]: the upper budget 6 is charged by a thin
  boundary family, everything else is lower-window structure.

Schema reading: the (·,0) core is a LOWER-window object (complete
Bm1∪B0 + lower B1) with a six-value upper stub — the hand target is
correspondingly small.  Certified statement: no coloring of these
50 values (balance 4-4/8-8/≥4 per team as listed) admits orders
with ≤ 6 upper and 0 lower inversions; every one of the 50 values
is individually necessary.

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

### 4c. The (v, 0) family by hand: L-PREFIX and the schedule that
### voids every sumset floor

Under vdn = 0, both teams are wholesale block-ordered
[Bm1∩T] ≺ [B0∩T] ≺ [B1∩T], with B2∩T woven in at s2-inversion cost
(a B2-value advanced past k B1-values costs k; parking B2 material
before B0/Bm1 costs ≥ |B1∩T| = M — impossible for vup < M).  So the
(v, 0) instance is the 3-block anchor-M core PLUS a forced balanced
PREFIX cohort Bm1 — the first instrument that charges the
below-window prefix attacks of notes/47 §2 (the "free team's fixed
cohort" that the 3-block escapes exploited).

**Lemma L-PREFIX [PROVED — three-line forcing + edge injectivity].**
Fix a model of (v, 0) with v < M/2 ≤ |B1∩T|.  Then for each team:
(i) every mono triple (u, y, 2y−u) ∈ (Bm1×B0×B1)∩T³ is
IMPOSSIBLE — u ≺ y is forced by s0∪s1 block order, so 2y−u ≺ y is
forced, an s1 inversion, banned: **μ_dn(col) = 0 exactly**;
(ii) every mono H_up triple (u, y, z) ∈ (B0×B1×B2)∩T³ forces its
s2 edge z ≺ y (u ≺ y forced by s1 order; the y ≺ u escape is gone);
(iii) every mono SKIP triple (u, y, z) ∈ (Bm1×B1×B2)∩T³ (a family
no 3-block window ever charged: z = 2y−u ∈ B2 for y > 2M + u/2)
likewise forces its s2 edge z ≺ y.  The forced s2 edges of (ii) and
(iii) are pairwise DISTINCT across triples and across families
(edge (y, z) determines u = 2y − z, which lies in exactly one
block).  Hence  **n_s2 ≥ μ_up(col) + μ_skip(col)**, so
    v_min(0)(M) ≥ min { μ_up + μ_skip : balanced col, μ_dn = 0 }.

**But the sumset floor is 0 — by exactly one schedule class.**  For
pure block-parity schedules (p, q, r, s) (T's parity per block):
μ_dn = 0 ⟺ r ≠ p;  μ_up = 0 ⟺ s ≠ q;  μ_skip = 0 ⟺ s ≠ p.
Solution: q = p, r = s = 1−p — the schedule **(x, x, 1−x, 1−x)**
(e.g. T = odds below 2M, evens above 2M; partner = complement,
which voids its three families symmetrically).  So the pure-sumset
relaxation of the (v,0) family is again toothless (e126c's lesson
one block deeper), and the (6,0) UNSAT proves: **the
(x,x,1−x,1−x)-schedule colorings — and every other zero-sumset
coloring — fail the MIXED order theory at vup = 6.**  Note what the
schedule does: it makes Bm1 and B0 SAME-parity in-team — the
prefix cohort and the window bottom become a dense same-parity
adjacent-block pair under forced block order, the classic
Lemma-P/zigzag flood geometry of the C3 world.  The mixed tax of
this schedule is measurable directly by FIXING the coloring and
scanning vup (a tiny orders-only instance) — the next instrument
(e158c), and the natural entry point for a C3-style hand ladder.

Exact sumset masses of the two canonical schedules (computed, both
teams, M = 16..64): the both-H-voiding schedule (1,0,0,1) of §3b's
caveat has (μ_dn, μ_up, μ_skip) = (0, 0, 54|50) at M = 16 growing
to (0, 0, 840|824) at M = 64 — exact law μ_skip^A(M) = 13M²/64 +
M/8 (verified exactly at 7 scales 16..128): **Θ(M²) skip mass —
under vdn = 0 the H-dodge is slaughtered by L-PREFIX** (≥ 54 forced
s2 inversions at M = 16, vs budget 6).  The (1,1,0,0) schedule is
(0, 0, 0) for both teams at every scale tested — the unique
pure-parity zero-sumset class, whose price is purely mixed-theory.

**MEASURED (e158c, this session): the zero-sumset class is DEAD at
every budget.**  With coloring FIXED to (1,1,0,0) and vdn = 0, the
instance is UNSAT at M = 16, 24, 32 for EVERY vup scanned up to 512
(seconds per query; at M = 16, 512 is within 128 of the vacuous
budget 640).  So the unique parity class that avoids all sumset
floors cannot buy a clean half-anchor AT ANY PRICE — the mixed
flood geometry (same-parity dense adjacent blocks under wholesale
block order) kills it outright.  Consequence, with L-PREFIX: every
(·,0)-escape must be sumset-massive, and its μ_up + μ_skip is paid
unit-for-unit in s2.  **The (·,0) schema architecture is therefore
three-armed, mirroring notes/56's GAP-STRUCT trichotomy one level
up:** (a) parity/zero-sumset colorings — killed wholesale by a
C3-style flood ladder [hand target; machine-true at 3 scales, any
budget]; (b) colorings far from the parity class — carry sumset
mass ≥ f(distance), paid in s2 by L-PREFIX [extremal counting, no
orders]; (c) the near-parity interpolation — robustness layer (N3
species).  v_min(0)(M) growth = arm (b)'s extremal function at the
crossover with arm (a)'s robustness radius.

### 4d. Arm (a) PROVED: Lemma K and the schedule-death theorem

**Lemma K (prefix-chain kill) [PROVED — two exhaustive finite bases
+ two monotonicity steps].**  Consider the integer interval [1, n]
with the constraint that the k smallest values are all placed
before the n−k largest.  For k ≥ 2 and n ≥ k + 5 there is NO
monotone-3-AP-free order.  Sharp at k = 2, 3, 4: (6,2), (7,3),
(8,4) are SAT; k = 1 never kills ((12,1) SAT).
*Proof.*  Bases (7, 2) and (8, 3): exhaustive machine search
(k!·(n−k)! orders; no AP-free order exists; (9,4), (10,5), (9,5),
(8,2)..(12,5) likewise UNSAT).  Step 1 (monotone in n): deleting
the largest value preserves AP-freedom and the prefix property, so
UNSAT(n, k) ⟹ UNSAT(n+1, k).  Step 2 (diagonal): deleting the
values 1, 2 (both in the prefix, k ≥ 2) and shifting gives
SAT(N, K) ⟹ SAT(N−2, K−2), i.e. UNSAT(n, k) ⟹ UNSAT(n+2, k+2).
From (7,2): all even k ≥ 2, n ≥ k+5; from (8,3): all odd k ≥ 3,
n ≥ k+5.  ∎

**Theorem SCHED-DEAD [PROVED].**  For every M ≥ 12 (M ≡ 0 mod 4)
and EVERY budget vup, the 4-block instance with coloring (1,1,0,0)
and vdn = 0 is UNSAT.
*Proof.*  Team A = odds of (M/2, 2M] ∪ evens of (2M, 8M].  A's
in-team APs split into two independent systems: the odd chain
(M/2, 2M] ∩ odd (no AP leaves it: an (odd, even, odd) AP needs
middle (a+c)/2 ≤ 2M − 1 < 2M + 2 = min of A's even part; an
(even, odd, even) AP needs middle ≥ 2M + 3 > 2M = max of the odd
part) and the even chain.  vdn = 0 block-orders the odd chain:
its Bm1-part (M/4 values) precedes its B0-part (M/2 values).  As
an AP-structure the odd chain is the interval [1, 3M/4] with
prefix k = M/4; k ≥ 3 and n = k + M/2 ≥ k + 5 hold for M ≥ 12
(at M = 8 the chain is (6, 2) — exactly Lemma K's SAT cell,
consistent with v*(bal,8) = 0).  Lemma K kills the chain — no
budget is consumed (vup prices only s2, which the chain never
touches).  Team B is the mirror image.  ∎

This exactly explains the measured any-budget deaths at
M = 16/24/32 (§ above), and it is the first COMPLETE arm of the
(·,0) schema: the zero-sumset class dies by pure order theory at
every scale.  What remains for the schema are arms (b) — sumset
mass of non-parity colorings, paid via L-PREFIX — and (c) — the
near-parity robustness radius.  First (c) data (exhaustive, this
session): (12,4) with ONE puncture stays UNSAT at 9 of 12 hole
positions; the three escapes are exactly the mod-3 lattice holes
{3, 6, 9} — sharp finite tolerance with lattice escapes, precisely
the N3 species (single-block d* with midpoint escapes).  The
dilution version (color swaps = puncture + cross-parity APs) is the
real arm-(c) target.

Empirical confirmation of L-PREFIX on the C2 witness (recomputed):
its coloring has μ_dn = (0, 0) EXACTLY (part (i) forced it), and
μ_up + μ_skip = 87/54 (A/B) ≤ n_s2 = 392/442 ✓ (parts (ii)+(iii)).
Notably the unbudgeted-above solver did NOT choose a zero-sumset
coloring — it paid sumset floors 87/54 plus ~300 mixed overhead;
the μ_skip family (45/24 here) is live, structured mass that no
3-block instrument ever charged.

## 5. The cascade calculus: why the frontier CURVE (not the cell) is
## the quantitative target

Define forced(x)(M) := min lower-anchor payment compatible with
upper payment ≤ x (the staircase boundary), and
v_min(0)(M) := least x with (x, 0) SAT — the price of a FREE lower
anchor.  Measured brackets at M = 16: forced(6) ≥ 1 (≥ 8 for the
parity-family colorings by the H_dn floor; exact value pending),
forced(≈442) = 0 (C2), so forced is a decreasing curve from ~6× 
amplification at the floor (pay 6 → forced 38 in the C1 witness's
channel) to zero at v_min(0) ≤ ~442.

**Why this kills the naive multiplicative cascade** (checked before
anyone tries it): if forced(x) ≥ λx for ALL x up to cap scale with
λ > 4, descending anchors N → N/2 → … would multiply payment by λ
while the absolute cap 10N² divides by 4, overflowing the fixed
bottom till at N₁ — L-AFFORD would follow.  But forced is
DECREASING (C2): a payer can always go lavish at one anchor and be
free below it.  The cascade route therefore reduces to the growth
of v_min(0)(M): **if v_min(0)(M) grows near cap scale Θ(M²), the
lavish dodge itself costs cap-scale payment at every second anchor
and the dodge space pinches**; if v_min(0)(M) stays near v*(M), the
pump is a bounded surcharge and the 4-block instrument has said all
it can.  v_min(0) growth (16 vs 24) is the decisive measurement
this instrument can still make; the (6,0)-MUS is the schema
material for the cell family.

## 6. Assembly: what L-AFFORD is after this session (task step 3)

**Proven / machine-checked today.**
- [PROVED] T-FORCE-4, L-PROJ (§1); L-PREFIX (§4c); NG4 (§4);
  GAP-COMP-as-threshold refuted by parity orientation (§4b, with
  machine realization); the (1,1,0,0) zero-sumset schedule identity
  and the Θ(M²) skip mass of the H-voiding schedule (§4c, exact).
- [MACHINE-CHECKED] the M = 16 pump triangle: (none,0) SAT /
  (6,none) SAT (audited witness — which also independently confirms
  3-block bal@16 SAT at v = 6 via L-PROJ) / (6,0) UNSAT; witness
  anatomies §3b; μ_dn = 0 exactness on every (·,0) witness.

**THEOREM J (2-scale joint demand — conditional on one tag).**
[GAP-J-schema]: for all large qualifying anchors N, U4(N; v, w)
UNSAT on a staircase S(N) ∋ (v*₃(N), v*₃(N/2)) + margins (measured:
(6, 0) ∈ S(16); scale-2 instance pending at 24).  Then every valid
Case-2 pair has (I(N), I(N/2)) ∉ S(N): the pair cannot pay the
3-block demand curve at two consecutive anchors — at least every
other anchor overpays its per-anchor floor by the margin.  Proof =
T-FORCE-4 + Lemma M monotonicity, verbatim notes/54 §2.  This
STRENGTHENS Theorem D's demand side; it does not touch supply (NG4).

**What L-AFFORD now is (the honest isolate).**  Since Theorem D
(demand ≥ v* everywhere) is proven mod GAP-V*, L-AFFORD (liminf
ratio < 1) is EQUIVALENT to regime-(I) death — it was always the
whole remaining content, and notes/54 §4.3's candidate route through
GAP-COMP + GAP-JOINT is now measured out: GAP-COMP's counting form
is dead (§4b), GAP-JOINT's downward coupling is real, priced, and
demand-side only (NG4).  The surviving shape of the supply argument,
sharpened by today's instruments:

> **[GAP-AFFORD′]** — an upper bound on the OVERPAYMENT capacity of
> Θ(M)-dense teams in the donation currency: the (·,0)-family
> shows that a free lower anchor costs v_min(0)(N) ≫ v*(N) paid in
> s2 (advancement of B2-material past B1 — i.e. procrastination of
> the WINDOW ABOVE), so "lavish here, free below" pushes the
> obligation UP the chain, not away; the un-dodgeable residue must
> be a statement that a pair cannot push obligations upward forever
> — a colored-value/donation ledger at the top of the growing
> range, where P1-freshness protects the payer no longer (every
> value above any bound is eventually inside windows).  Open; NOT
> closable by budget rectangles (NG4); the v_min(0) growth curve
> and the (v,0)-MUS anatomy are its finite shadows.

**Sub-gaps introduced, with status:**
| tag | statement | status |
|-----|-----------|--------|
| GAP-J-schema | all-M staircase family S(M) ∋ (v*₃(M)+a, v*₃(M/2)+b) | machine-true at M=16; M=24 cell queued; schema target = (v,0)-family via L-PREFIX + mixed ladder on (1,1,0,0) |
| GAP-VMIN0 | growth law of v_min(0)(M) (free-lower-anchor price) | bracket (6, ≤442] at 16; sched(1100) curve = upper-bound instrument (e158c) |
| GAP-AFFORD′ | overpayment-capacity ledger (donation currency) | open — THE residual; NG4 delimits it |
