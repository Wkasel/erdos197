# 64 — FRONT LAW-CONSISTENCY: the exact laws stressed against each other at massive scales

Mandate: cross-check every exact law against every other at M = 2^k
(k = 6..40) and spot values to 2^1000 — **formulas and exact big-int
arithmetic only, no solving**.  Instrument:
experiments/e167_law_consistency.py → data/e167_law_consistency.log
(ALL CHECKS PASS).  Laws stressed: K* mechanistic law (notes/57),
L-LOP flat cap law (notes/58/61), DICH thresholds, skip-mass law +
v* witness curve (notes/62), CORE′ band schema (notes/51/56/57),
window tiling M·8^t + C3 mod-8 + SCHED-DEAD (notes/50/62).

**Headline: no law contradicts any other at any scale — but the
matrix has exactly ONE seam that is not closed-form, and it is the
seam the whole Case-2 chain hangs on: the overlap width
W(M) = 3 − α_max(M) for M ≥ 96, with α a per-scale catalogue scan,
not a formula.  W has already hit 0 (112/128/144), returned to 1
(160), and goes NEGATIVE the first time a shallow alive 4-clique
exists — an event no certified law excludes, and whose half-scale
analogue is ALREADY realized (e155b max cliques = 4 at m = 24/28/32).
The margin is one alive value.**

---

## (a) K* law × L-LOP cap law × DICH thresholds — the overlap width

### a.1 Reproduction layer (all pass)

* K*(M) = m + 9 + max(α_E − f_O, α_O − f_E) reproduces all EIGHT
  measured thresholds 26/35/42/51/60/68/76/83 at 48..160 from the
  catalogue inputs (α_E, α_O, f_O, f_E) of notes/57 F1/F2 + audits.
* Flat cap law cap(M) = (M+16)/2 − 5 exact at 96..160
  (51/59/67/75/83); OUT of scope below 96 (misses by +2/+1/+1 at
  48/64/80 — the flat law must never be quoted below 96).
* Both dead laws re-confirmed dead by formula: ⌊M/32⌋ cap law fails
  at 128 (66 ≠ 67); mod-32 K* law fails at 112/128/144.
* Measured width series W = cap − K* + 1 = C − K*:
  **4 / 2 / 3 / 1 / 0 / 0 / 0 / 1** at 48..160.

### a.2 The recomputation at M = 2^k — and what it can and cannot say

For M ≥ 96, combining the two laws:

    W(M) = C − K* = (m+4) − (m+9+max(α_E−f_O, α_O−f_E))
         = min(f_O−α_E, f_E−α_O) − 5
         = 3 − α_max(M)          in the F2 regime f_O = f_E = 8
                                 (measured at every scale ≥ 96),

which is **k-independent**: at every M = 2^k (k = 6..40) and at
2^100/2^500/2^1000 the scenario table is the same —

    α_max = 2  →  W = 1     (measured at 160)
    α_max = 3  →  W = 0     (measured at 112, 128, 144)
    α_max = 4  →  W = −1    (HOLE: min|Y| = m+4 covered by neither arm)

(f reverting to 9 only widens W; f < 8 is impossible by definition,
f_c ∈ {8,9}.)  Integrality is clean at every scale checked including
2^1000 (301-digit C, exact).

### a.3 Verdict on THE backward-from-bounds question

**W does not stay ≥ 1 — it already hit zero at 112/128/144.**  The
feared monotone narrowing did NOT continue (α is non-monotone:
2,3,2,2,3,3,3,2 at 48..160; W came back to 1 at 160), but the
certified laws CANNOT decide "W ≥ 0 forever":

* The cap side is closed-form (flat law, 5 consecutive scales).  The
  K* side is **mechanistic, not closed-form** — its inputs α_c(M),
  f_c(M) are per-scale catalogue scans (GAP-DICH-ALPHA / GAP-DICH-F2).
  So "recompute the width from the laws at 2^40" is only possible as
  the scenario table above; the matrix cannot certify which row
  applies at any unmeasured scale.
* Nothing proven bounds α_max ≤ 3.  The closest measured object —
  the half-scale SAT-alive clique number (notes/58 §3.5d, the
  explicitly-flagged cousin of α) — is ALREADY 4 at m = 24, 28, 32.
  If the shallow zone ever realizes a mod-8-aligned alive 4-clique
  while f = 8, W = −1 at that scale.
* **Where it bites**: first unmeasured 16-multiple M = 176; first
  unmeasured dyadic M = 256 = 2^8 (i.e. EVERY 2^k of the mandate
  range beyond k = 7 is uncertified); first COMPOSED window scale is
  already out of range at t = 1 (48·8 = 384 > 160) — the Case-2
  chain applied to any window family (M·8^t)_{t≥1} rides entirely on
  (OV-∀) or on the robust chain.
* The insurance is real but also per-scale: COV-W′ (d₀ = 4 robust
  P-arm) is verified at 128 AND 160 and does not consume (OV) — and
  notes/58 §3.5d's clique ≤ 4 measurement is exactly the statement
  that would cap the hole at width 1 (the size the d₀ = 4 chain was
  built to absorb) IF it transfers to the shallow zone.  **Concrete
  recommendation: prove α_max(M) ≤ 4 via the H-LAT lattice recursion
  (alive gaps ≡ 0 mod 8, halving fixed points) — then W ≥ −1
  unconditionally and the robust chain schema closes the hole at
  every scale; proving ≤ 3 would restore (OV-∀) outright.**

## (b) Skip-mass law × v* witness curve

### b.1 The skip-mass law re-derived independently (and extended)

Exact recount of the (1,0,0,1)-schedule skip triples
(Bm1×B1×B2 mono triples z = 2y−u), pure counting, no solver:

    μ_skip^A(M) = 13M²/64 + M/8   CONFIRMED at 16/24/32/48/64/96/128
                                  and at two FRESH scales 192, 256
    μ_skip^B(M) = 13M²/64 − M/8   (NEW closed form — notes/62 only
                                  listed B's values 50/824; this
                                  formula fits all nine scales;
                                  A−B = M/4 exactly)

Integrality holds at every window scale (64 | 13M² and 8 | M for all
M ≡ 0 mod 8, hence at every M·8^t and every 2^k, k ≥ 3, checked
symbolically to 2^1000).

### b.2 The witness curve does NOT follow the skip-mass law

Fit of the 3-block SAT-point witnesses v_wit = 6 / 65 / 368 at
M = 16 / 24 / 32:

* Local power exponents: 5.876 (16→24), 6.026 (24→32); global 5.939.
  An exponential fit is worse (log-increments 0.298 vs 0.217 per
  unit M, non-constant).  Striking near-form:
  **v_wit(M) ≈ (3/32)·(M/8)^6 = 3M^6/2^23** — exact at 16 (6.0),
  within 5 % at 24 (68.3 vs 65) and 32 (384 vs 368).
* The skip-mass law is Θ(M²): growth factor 3.9 over 16→32 vs the
  witnesses' 61.3.  **13M²/64 does not predict the witness growth —
  wrong exponent by ≈ M^4.**  The two curves CROSS at M ≈ 28
  (skip 120 > wit 65 at 24; skip 212 < wit 368 at 32), so neither
  bounds the other; they are different quantities (a per-schedule
  4-block s2 sumset floor vs a 3-block joint budget), and no note
  ever asserted a link — the check passes vacuously, but kills any
  temptation to quote μ_skip as a v* model.

### b.3 Implied v*(M) asymptotic — with the honest caveat

Upper envelope from witnesses: **v*₃(M) = O(M^6)** with constant
≈ 3/2^23 (fit exponent 5.9–6.0 on three points).  The lower brackets
are 5 / 5 / 3 at 16 / 24 / 32 — essentially FLAT — so the data are
consistent with anything from v* = Θ(1)..Θ(M^6): the M^6 curve may
be a CP-SAT-search artifact (near-critical SAT hunting times out;
the witness is merely the first budget a solver could certify), not
the true frontier.  For the T-FORCE ledger the two readings diverge
enormously at composed scales (v*(M·8^t) multiplying by ≈ 8^{6t}
per window vs staying bounded); GAP-V*-growth remains the open dial
and the witness curve should be quoted only as an upper bound.
Cheapest discriminator: push the v*(bal,16) bracket {5,6} to an
exact value and get ANY nontrivial lower bound at 32 (> 3); a lower
bound ≥ 30 at 32 would already separate the flat reading from the
power law.

## (c) Schema-band arithmetic across the window tiling M·8^t

Canonical bands re-pinned from the instruments (experiments/e153
core_support): P0 = [M+1, 2M], **P1 = [3M−15, 4M] (CLOSED left end,
M+16 values)**, P2 = [4M+1, 6M+15] (2M+15 values), |CORE′| = 4M+31
(= 287 at M = 64, matching e134 exactly).

All 23 affine residue/integrality/containment conditions of the
stack — DICH mod 16, C3-core mod 8, P-ARM halved line m ≡ 0 mod 8,
SCHED-DEAD scope (M ≥ 12, M ≡ 0 mod 4), Lemma K (n = 3M/4 ≥
M/4 + 5), band containments 2M < 3M−15 ≤ 4M < 4M+1 ≤ 6M+15 ≤ 8M,
P1/P2 parity counts, E1 window + droppable completions ⊂ P1,
flood centre 6M interior to P2, seam-2 doubling image
(6M, 6M+15] = 2·4M − (2M−15, 2M], skip-mass integrality, core
disjointness from the next window's core — were verified with exact
big ints at 12 bases (16, 48..160 step 16, 2^6, 2^20, 2^40) × every
t ≤ 1000.  **Zero failures: no residue clash for any k up to 1000.**
Structural reason (also verified): every condition is affine in M
with threshold ≤ 48 and its residue class is preserved by ×8; any
mod-2^j condition (j ≤ 4 in the stack) is satisfied at M·8^t once
3t + v₂(M) ≥ j, so the ONLY constraints live at t = 0: the base
window scale must have M ≡ 0 mod 16 and M ≥ 48 (bases 8/24/40/56
fail exactly the mod-16/halved-line rows at t = 0 and are clean from
t = 1 on).  Composition is arithmetically safe forever; what is NOT
safe is the certification range — see (a.3): every composed scale
beyond t = 0 exceeds M = 160.

## Inconsistencies found (all prose-level; no theorem touched)

1. **notes/51 headline vs canonical CORE′ (off-by-one).**  notes/51
   (and the campaign shorthand) writes B1-support "(3M−15, 4M]"
   (M+15 values); the instruments and notes/56/57 use the CLOSED
   [3M−15, 4M] (M+16 values).  e134's |support| = 287 = 4M+31 at 64
   arbitrates: **closed is canonical**; notes/51's "last M+15 values
   of B1" should read M+16.
2. **notes/57 §0.1 P2 parity counts wrong by a factor ~2.**  "P2 has
   m+8 odd and m+7 even values" — for the canonical
   P2 = [4M+1, 6M+15] the counts are **M+8 odd, M+7 even**.  (The
   m+8/m+8 counts for P1 are correct; the P2 line copied the m-scale.
   Not load-bearing: e153 computes from the actual P2, and the §4
   counting uses only P1's m+8.)
3. **notes/57 §0.2 trend prose** ("both monotone-in-M trends") —
   already flagged by the audits; re-confirmed by formula: α is
   non-monotone (2,3,2,2,3,3,3,2).  Kept here because the (a.2)
   scenario table is the formal replacement for that prose.
4. **Flat-cap-law scope creep hazard.**  The flat law quoted without
   its "M ≥ 96" scope is FALSE at 48/64/80 (misses by +2/+1/+1).
   Any assembly text quoting "cap = (M+16)/2 − 5" must carry the
   scope (STATUS.md's current phrasing does; the task-brief shorthand
   "caps 29/36/44/51/75/83 at 48..160" also silently skips the
   112/128 values 59/67).
5. **Narrow margin (the real finding, not an inconsistency):**
   (OV-∀) is exactly the statement α_max(M) ≤ 3 for all M ≥ 96 under
   the flat cap law; W = 3 − α_max; the measured cousin of α already
   reaches 4.  One alive value separates the assembly from a hole at
   every unmeasured scale — including every M = 2^k, k ≥ 8, and every
   composed window scale M·8^t, t ≥ 1.

## Status ledger

| check | verdict |
|---|---|
| K* law × cap law × DICH, 8 scales | consistent (reproduced exactly) |
| W at 2^k, k = 6..40, spots to 2^1000 | scenario-determined only: W = 3 − α_max; NOT closed-form — (OV-∀) open, margin 1 |
| skip-mass law, 9 scales + integrality to 2^1000 | exact; new B-team closed form 13M²/64 − M/8 |
| skip-mass vs witness curve | independent quantities; curves cross at M ≈ 28; no predictive link |
| v* asymptotic | upper envelope ≈ 3M^6/2^23 (exp 5.9–6.0); lower brackets flat — growth UNDECIDED |
| band composition M·8^t, t ≤ 1000 | zero residue clashes; constraints live only at t = 0 (M ≡ 0 mod 16, M ≥ 48) |
