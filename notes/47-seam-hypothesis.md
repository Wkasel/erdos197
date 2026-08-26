# 47 — FRONT G2: the double non-procrastination hypothesis

THE gap of the NO program (STATUS post-merge, gap 2).  This note (i)
formalizes the hypothesis and the violation vocabulary, (ii) settles the
normalization question — does lem:normal transport and make the
hypothesis a theorem? — **it transports as a lemma and fails as a route:
the hypothesis is FALSE as a single-team statement, with explicit
interleaving counterexamples at every anchor and at budget N^{1-o(1)}**,
(iii) identifies the exact barrier (fresh per-window supply + Behrend
teams), and (iv) quantifies the procrastination COST v*(M) by machine
(e127): what a coloring must pay in seam inversions to escape the
coupled cores.  The surviving G2 routes are at the end.

Machine: experiments/e127_seam_budget.py; data/e127_*.json/.log,
e127_seam_budget.jsonl (streaming).

## 0. The hypothesis, formalized

Partition Z+ = A ⊔ B, both teams permutable via monotone-3-AP-free
arrangements π_A, π_B of order type ω.  For an anchor N ∈ Z+ write
W(N) = (N, 8N] with blocks B0 = (N, 2N], B1 = (2N, 4N], B2 = (4N, 8N]
(anchor-free: N need not be a power of 2; the coupled core's attack
geometry only needs the ratio-2 block structure).

**Definition (seam-clean).**  Team T is *seam-clean at W(N)* if in π_T
every value of T ∩ B_i precedes every value of T ∩ B_{i+1}, for i = 0, 1.

**Definition (inversion).**  An *adjacent-seam inversion of T at W(N)*
is a pair (u, w), u ∈ B_i ∩ T, w ∈ B_{i+1} ∩ T, with pos(w) < pos(u).
T is seam-clean at W(N) iff it has zero adjacent-seam inversions there.
(*Skip inversions* (u ∈ B0 after w ∈ B2) need no separate accounting:
for each y ∈ B1 ∩ T, position trichotomy gives either pos(y) < pos(u) —
an adjacent inversion (u, y) — or pos(y) > pos(u) > pos(w), hence
pos(w) < pos(y) — an adjacent inversion (y, w); distinct y give distinct
pairs, so one skip inversion forces ≥ |B1 ∩ T| adjacent ones.)

**Hypothesis DNP (double non-procrastination).**  For every valid pair
(A, B) there are infinitely many anchors N at which BOTH teams are
seam-clean at W(N).

**Hypothesis DNP(v), the budgeted weakening.**  ... at which both teams
have ≤ v(N) adjacent-seam inversions at W(N).

DNP(v*−1) + the constant-bound coupled schema at budget v*−1 (e127
version) + G1 scale-stability closes Case 2; N1+N2 close Case 1.  The
seam controls (notes/45: every proper subset of the seam chain is SAT)
show the two-seam form cannot be thinned FURTHER than its budget.

**Anchor covering (which windows one inversion poisons).**  The pair
(u, w), u < w, pos(w) < pos(u), is an adjacent-seam inversion of W(N)
exactly for
    N ∈ [max(u/2, w/4), min(u, w/2))       (u ∈ B0, w ∈ B1)
    N ∈ [max(u/4, w/8), min(u/2, w/4))     (u ∈ B1, w ∈ B2),
both empty unless w < 4u, both contained in [u/4, u): **each inversion
pair covers at most two anchor intervals inside a fixed 2-octave range.**
(Machine: e127b_cover_check.py — formulas exact on 500 random pairs
against exhaustive anchor enumeration; the §1 X-INTERLEAVE pairs cover
every anchor below 4^6.  Both PASS.)
Consequently ¬DNP for a pair (A, B) says: the anchor sets covered by the
two teams' inversion pairs jointly contain all large N — inversions must
recur in EVERY octave.  "T re-descends at scale t infinitely often" is
exactly this covering statement; the task-prompt definition (a block-t
value placed before block-(t−1) finishes) is the (u, w) pair read at the
seam between the blocks.

## 1. Normalization: what transports (N-GEN) and what does not

**Lemma N-GEN (lem:normal is team-blind).**  Let S ⊆ Z+ be infinite with
a monotone-3-AP-free arrangement π of order type ω.  Define
s(v) = max_{q ≤ pos(v)} blk(π(q)), blk = dyadic block index.  Then s is
a stage function with finite fibers, non-decreasing along π, its
concatenation (fiber orders induced by π) is π, s(v) ≥ blk(v) for all v,
and (A) ∧ (B) of thm:chunk hold.  *Proof: verbatim lem:normal — the
proof never uses S_A: running max is non-decreasing, so fibers are
consecutive segments of π; blk(v) enters the max at v's own position;
fibers are finite because π is onto S and S meets unboundedly many
blocks; thm:chunk's equivalence is stated for arbitrary concatenations
and AP triples of the ambient set.  ∎*

So EVERY permutable team is "block-monotone up to finite fibers" with
non-negative displacement δ(v) = s(v) − blk(v) ≥ 0 — the WLOG of the
dyadic paper survives in full generality.  In particular chunk condition
(A) is unconditional for any valid team: **no in-team AP triple has
strictly increasing running-max stages.**

**But seam-cleanness does NOT follow.**  Seam-clean at W(N) is a
statement about fibers not straddling two consecutive block boundaries;
N-GEN permits every fiber to straddle forever.  The dyadic proof never
needed cleanness — its divergence criterion consumed the displacements
of the FIXED values 3..16, constants of the infinite scheme.  The
Case-2 windows at scales N·8^k share no values, so nothing is pinned
across scales: the transport that closed S_A has no invariant to ride
here.  Concretely:

**Example X-INTERLEAVE (positions CAN interleave).**  T = {2^j : j ≥ 0}
contains no 3-term AP at all (2^{b+1} = 2^a + 2^c forces a = c), so
EVERY arrangement of T is monotone-AP-free.  Arrange
    π = 2, 1, 8, 4, 32, 16, 128, 64, ...   (swap 2^{2k+1}, 2^{2k}).
Then: (i) π is a valid arrangement of a permutable team; (ii) its
inversion pairs (u, w) = (4^k, 2·4^k) cover, by the §0 formulas, the
anchor intervals [4^k/2, 4^k) ∪ [4^k/4, 4^k/2) = [4^{k−1}, 4^k) — every
anchor N ≥ 1: **T re-descends at every scale**; (iii) there is no
infinite descending position chain — every descent has depth 1, the
running-max displacement is δ(2^{2k}) = 1, δ(2^{2k+1}) = 0, all fibers
are the 2-element straddles {2^{2k+1}, 2^{2k}}.

This answers the L-DESC question of the attack plan: **an infinite
re-descent sequence does NOT force an infinite descending position
chain; interleaving is realizable, at every scale simultaneously, with
displacement 1.**  Well-founded descent (the T-REGRESS engine) is
powerless against depth-1 re-descents, exactly as T-SHARP's
procrastination is legal when each late value is fresh.

**Example X-INTERLEAVE-v (the budget version is also false single-team).**
There is a 3-AP-free set S with |S ∩ (N, 2N]| ≥ N^{1/2−o(1)} for ALL N
and spread through every sub-interval (x, 1.1x]: build greedily per
octave, placing m_k = ε·2^{k/2} values in octave k, one per equal
multiplicative cell; a new value is forbidden only if it completes an AP
with a pair of previously chosen values — at most 3·(Σ_{j≤k} m_j)² ≈
3·(3.4ε)²·2^k ≈ 35ε²·2^k < 2^k/2 forbidden positions for ε ≤ 1/9
(cells minus forbidden stay nonempty on average; discard the ≤ half of
cells that are over-forbidden and keep m_k/2 values — the counting
only loses constants).  Every arrangement of S is AP-free.  Order S
octave by octave but interleave each consecutive pair of octaves (top
half of octave k's cells placed after the bottom half of octave k+1's).
Every pair (u, w), u ∈ octave k, w ∈ octave k+1 has w/u < 4, so all
these pairs are adjacent-seam inversions of the anchors they cover, and
the cell spread gives every anchor N ∈ [2^{k−1}, 2^k) order
m_k · m_{k+1} = Θ(N) of them up to the constant-fraction cell losses of
the greedy bookkeeping.  **A single permutable team can carry
Θ(N^{1−o(1)}) adjacent-seam inversions at EVERY anchor.**  (Ceiling for
such free teams: a 3-AP-free team has ≤ r_3(8N)² = o(N²) in-window
pairs by Roth/Behrend, so o(N²) caps this construction family.)

**Verdict on the normalization route: lem:normal generalizes (N-GEN),
the hypothesis does not follow, and no single-team statement — DNP or
DNP(v) for any budget v(N) up to N^{1−o(1)} — is true.**  Any proof of DNP
must use both teams jointly and the Case-2 density floor; the
counterexample teams are AP-free-sparse, and their co-teams are dead
(the complement of {2^j} contains the reflector-1 orbit 3, 5, 9, 17,
...; density-1 co-teams of Behrend-type teams are the N7/dodger corner).

## 2. The supply barrier, stated honestly

The windows W(N·8^k) are disjoint, and an adjacent-seam inversion of
W involves only values of W: the violation supply is FRESH at every
window.  Therefore no per-window budget hypothesis can be closed by
counting/well-foundedness across windows — a team may pay v(N) fresh
inversions at every window forever (§1 realizes this).  What fresh
supply CANNOT buy is exemption from the window's own AP theory: an
inversion (u, w) with u placed after w ≥ 2u means u acts, inside its own
window, as a LATE value whose attack units (u, y, 2y−u) against the
material placed after it are live — procrastination is self-exposing
(the notes/45 caveat).  The cost of that exposure is precisely what the
e127 budget instances measure.  So the honest division of labor:

- the FINITE side (machine, this note): how much does an escape cost in
  inversions — v*(M) — and where must the inversions sit (anatomy);
- the INFINITE side (open): a mechanism that converts "every window
  charges v*" into death.  By §1 this mechanism cannot be single-team
  descent; the candidates are the covering argument of §0 (inversions
  must recur in every octave — a positional invariant on one
  permutation, where consecutive windows DO share the inversion pairs'
  anchor intervals) and the N6 ledger (violations at scale k forcing
  prices at scale k+1).

## 2b. The forced-inversion reading (the right direction of the schema)

The budget schema should not be read as "assume DNP(v), conclude
death"; it should be read FORWARD:

> **T-FORCE (per-anchor forced procrastination; immediate from
> UNSAT).**  If the budget instance at bounds (c0, c1, c2) and budgets
> (vA, vB) is UNSAT at window size M, then in ANY valid partition, at
> EVERY anchor N (window (N, 8N] scaled to the instance's M... i.e. at
> every anchor where the teams meet the bounds), NOT both teams have
> ≤ vA / ≤ vB adjacent-seam inversions: some team procrastinates
> MORE.  Validity restricted to a window is a genuine coloring + two
> AP-free orders, so it must sit in the SAT region.

With the Case-2 floor (intruder counts → ∞) the bounds hold at all
large anchors, so a valid Case-2 pair must clear the v* hurdle at
EVERY large anchor simultaneously — infinitely much procrastination,
somewhere, forever, with the covering structure of §0 (each inversion
pair serves ≤ 2 octaves of anchors, so inversions recur in every
octave for at least one team).  The open mathematics of G2 is
exclusively: **can a valid pair AFFORD the forced inversions?**  §1
says sparse free teams can afford anything; §2 says disjoint-window
counting cannot refuse them; what is NOT settled is whether a Case-2
DENSE team can afford v*(N) → ∞ (if v* grows) inversions per window in
the presence of its own AP theory — the inversions of window k live
among values that are also the attack material of windows k−1, k, k+1
(anchor overlap), which no experiment so far charges.

One more honesty point about the one-sided SAT escapes (§4): they are
FINITE-ONLY escapes.  At the infinite level the "free" team is not
free: the first k values of its permutation form a fixed cohort placed
before cofinitely all window material (positions are finite), and every
value b below a window attacks it with Θ(M) units (completions
2y − b of y ∈ (N, 2N] never leave (N, 8N] for b ≤ N) — constraints the
3-block instance does not see.  The finite theory extended downward is
notes/36's full 2-colored theory — SAT everywhere — so this cannot be
repaired by a bigger finite core; it is exactly the N6 infinite-
accounting frontier.

## 3. The exact combinatorial meaning of the budget (why v* is a
## sumset quantity)

In the coupled core the only cross-window forcing is the triple family
H = {(u, y, 2y−u) : u ∈ B0, y ∈ B1, 2y−u ∈ B2} (notes/45).  A
monochromatic triple of a seam-clean team is position-forced increasing
— fatal.  Under a budget, a monochromatic triple (u, y, z) survives iff
NOT (u ≺ y ≺ z) iff y ≺ u or z ≺ y, i.e. iff one of its two adjacent
seam EDGES (u, y), (y, z) is inverted.  Both maps (u, y) ↦ (u, y, 2y−u)
and (y, z) ↦ (2y−z, y, z) are injective — **each seam edge lies in
exactly one triple of H** — so breaking k triples costs ≥ k distinct
inversion pairs:

    v*(M, bounds) ≥ μ(M, bounds)
      := min #monochromatic H-triples over colorings meeting the bounds,

and the SAT instance charges, on top of μ, the consistency of the
chosen inversions with the full in-window AP order theory (both
monotone directions, both teams).  μ is a pure sumset/coloring
extremal quantity (no orders); v* = μ would mean inversions are cheap
once the coloring is fixed; v* > μ would mean the order theory taxes
procrastination beyond the counting minimum.

**Warning: μ = 0 is achievable even at exact balance** — the parity
coloring (one team = evens of B0 ∪ B1 + odds of B2) makes 2y − u the
wrong parity for both teams, zero H-triples — yet the balanced core is
UNSAT at v = 0.  So the two-seam death does NOT ride H alone: the
mixed shapes (two members in one block), individually order-dodgeable,
are jointly lethal under block order, and v* measures the tax on THAT
joint theory as well.  (This corrects a possible over-reading of
notes/45's escape anatomy: H is the position-FORCED family, not the
whole engine.)

## 4. Machine results (e127): the price of procrastination

Instance: coloring of (M, 8M] + per-team orders + guarded APs + block
lower bounds, seam units REPLACED by inversion indicators with
per-team cardinality ≤ v; complete transitivity; every SAT witness
independently re-audited (bounds, per-team AP-freedom, inversion
recount, and the §3 edge-audit: every monochromatic H-triple of the
witness contains an inverted seam edge).  v = 0 reproduces the e120
cores exactly.

**Constant bounds (3, 6, 12), symmetric budget:**

| M | v=0 | v=1 | v=2 | v=3 | ... | v* |
|---|-----|-----|-----|-----|-----|----|
| 24 | UNSAT 7.7s | UNSAT 189.5s | (running) | | | ≥ 2 (running) |

**Balanced (each team ≥ half of each block):**

| M | v=0 | v=1 | v=2 | higher | v* |
|---|-----|-----|-----|--------|----|
| 16 | UNSAT 2.0s | UNSAT 24.0s | UNSAT 243.6s | (running) | ≥ 3 (running) |

**Asymmetric budgets — the schema NEVER fires on one team's cleanness
alone.  Both one-sided weakenings are SAT already at v = 0:**

| variant | M | verdict | escape anatomy |
|---------|---|---------|----------------|
| asym: A free, B ≥ (3,6,12) budgeted | 24 | SAT at v=0 [1.9s] | B = minority pinned at (3,6,12), seam-clean, 0 mono-H; A = majority procrastinates freely: 2090 inversions, 520 mono-H triples (every one broken by an inverted seam edge — §3 audit passes) |
| majb: A free ≥ (3,6,12), B MAJORITY (≥ half each block) budgeted | 24 | SAT at v=0 [5.2s] | B = 13/24/48 majority, seam-clean, 0 mono-H (range-hides B1-material); A = 11/24/48 reverses nearly everything: 33 of its 35 low values late, late set gap-DENSE (28 of 32 gaps ≤ 2), 643 inversions, 113 mono-H |

Two morals.  (i) **DNP is irreducibly two-sided**: no one-team
weakening (not even "the block-majority team is clean") gives a finite
core — matching the seam controls, every one-sided hypothesis is
escapable.  The dense free team simply reverses its low blocks
wholesale.  (ii) The free team's late set is NOT pair-sparse — but a
3-block window cannot charge the exposure of late values (their attack
units (u, y, 2y−u) with u late land in the NEXT block up, outside the
instance).  The L-EXPOSE question is therefore not settled by these
escapes; it needs the 4-block overlapping-window gadget (§5).

## 4b. The regime map: where DNP is actually NEEDED

Split Case 2 by the minority's per-block count P(t) (both teams' counts
diverge; look at windows where team m is the block-minority):

- **Sub-linear minorities (P(t) = o(M), e.g. the "Behrend blocker"
  dodger: a 3-AP-free minority whose order theory is EMPTY — it can
  stay seam-clean for free and dodge every in-team order gadget):
  DNP IS NOT NEEDED.**  The majority's per-block density → 1, and
  N5's two-block density rung (notes/45 Part E: fixed pair {15, 16},
  window (M, 4M], UNSAT for EVERY in-team subset of per-block density
  ≥ 13/16 at M = 32, T-PIN-clean) fires on the majority alone: the
  adversarial-subset quantifier already includes the minority's best
  placement, the pair is early at cofinitely many disjoint windows by
  T-PIN (hand), and P(t) = o(M) puts the majority's density above any
  fixed threshold eventually.  CAVEAT (honest): the two-block rung
  needs the SAME team dense in two consecutive blocks infinitely
  often.  Shapes whose block-majority ALTERNATES every octave (i.e.
  octave-alternation with growing dust) starve it structurally — the
  AP middle y of a B(m) → B(m+2) attack always lands in the skipped
  block B(m+1), where the attacking team is sparse — so that sub-case
  stays with the legacy alternation machinery (NECK/d_t, currently
  proven only at bounded dust) or with the coupled core.  With that
  caveat: sub-linear-minority, non-alternating Case 2 is dead modulo
  the N5 ρ*-rung schema (a rung family in the N2 mold — no order
  hypothesis on anybody).  This disposes of the sharpest free-team
  dodger from §1 in its natural form: making the minority order-free
  (3-AP-free) makes the majority nearly-full, which is exactly what
  the density rungs eat.
- **Linear minorities (both teams Θ(M) per block): the only regime
  where the coupled cores and DNP carry the load.**  Here BOTH teams
  have rich in-window AP theories, the ε-balance version of the e127
  instance applies (bounds (εM, 2εM, 4εM)), and T-FORCE charges both
  teams' orders.  The balanced v* (§4) is the relevant price; its
  growth in M is the pump the N6 ledger needs.
- **Crossover (minority density between o(1)·M and the ρ* threshold
  ~3M/16..M/2): the dial laws** — N5's ρ*(x) ≈ 1 − x/(4M) with larger
  attacker pairs, chain pairs at 7/8 — cover part; locking their
  scale-stability (STATUS next-experiment 3) now serves G2 directly,
  not just N5.

So the honest reformulation of THE gap: **G2 = "two Θ(M)-dense teams
cannot both afford their forced inversions at every anchor forever."**
Everything below linear density is (modulo rung schemas already in the
N-program) not a seam question at all.

## 5. G2 route map after this note

1. **DNP as stated is unprovable single-team and unprovable by
   counting; stop attacking it head-on.**  The live weakening is
   PAIRED: "for infinitely many N, both teams have ≤ v inversions",
   attacked via v*(M) → ∞ (if true): every valid pair then pays
   diverging procrastination at every anchor — an obligation with
   anatomy, not a possibility.
2. **The asymmetric leverage point is DEAD (measured, §4)**: both
   one-sided budget variants are SAT at v = 0, so there is no
   single-team finite core at any density assignment tried.  What
   replaces it is the regime map (§4b): sub-linear minorities are not
   a seam problem at all (density rungs), and the two-sided budget at
   ε-balance is the honest remaining instrument.  The (p, v)-dial
   gadget of the old route lives on as the ε-balance v* trend.
3. **The exposure rung (L-EXPOSE, next experiment)**: an inversion pair
   with u, u±1 both late re-creates the generic-pair geometry INSIDE
   the window — check by machine whether witnesses' late sets are
   always pair-sparse (gap ≥ 3), matching the notes/46 dodger
   signature (iii).  If forced, violations consume the team's
   pair-free budget, and the supply lemma (some team has Θ(M) adjacent
   pairs) collides with it.
4. If v* is BOUNDED (schema-stable small constant): the coupled schema
   itself absorbs bounded violation — DNP(v*−1) replaces DNP, and the
   remaining question is only the §0 covering statement at budget
   v*−1, which is about inversions recurring in every octave of ONE
   pair of permutations — a positional invariant worth attacking with
   the L1'/ledger machinery rather than descent.
