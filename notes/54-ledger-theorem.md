# 54 — The T-FORCE ledger theorem (formal statement, every unproven link tagged)

Successor of GAP-G2 in the reframed form of notes/47 §2b/§4b and
notes/50 link 1.  This note states the ledger theorem the NO program
needs, in final form, ready to receive the v* data (e128 bisection
still streaming at the time of writing: data/e128_vstar.log shows the
bal@16 v=8 query running; the jsonl record used here is
data/e127_seam_budget.jsonl, 11 rows).  Structure: §1 vocabulary and
the budget-instance family; §2 the DEMAND side (proven restriction
lemma + the schema tag); §3 the regime map as a formal trichotomy
(supply-side routing); §4 the SUPPLY side — proven accounting lemmas,
proven no-go propositions (where single-team accounting dies), and the
exposure-cascade candidate for the affordability lemma; §5 the ledger
theorem and its two-line contradiction, modulo the tags; §6 machine
spot-checks (e130); §7 the link table for notes/50.

Machine companion: experiments/e130_ledger_checks.py →
data/e130_ledger_checks.json/.log (does not touch e124m/e127/e128
files).

## 1. Vocabulary

Throughout, (A, B) is a *valid pair*: a partition Z+ = A ⊔ B such that
both teams are permutable — team T has an arrangement π_T of order
type ω with no monotone 3-AP (an in-team AP a < b < c with positions
increasing along (a, b, c) or along (c, b, a)).  pos_T(v) = position of
v in π_T.

**Windows.**  For an anchor N ∈ Z+, W(N) = (N, 8N] with blocks
B_0(N) = (N, 2N], B_1(N) = (2N, 4N], B_2(N) = (4N, 8N].  Each block is
itself a ratio-2 window.  For a base anchor N₀ the scales
N_k = N₀·8^k tile (N₀, ∞) by disjoint windows.

**Inversions and prices.**  An *adjacent-seam inversion* of T at W(N)
is a pair (u, w), u ∈ B_i(N) ∩ T, w ∈ B_{i+1}(N) ∩ T (i ∈ {0,1}),
with pos_T(w) < pos_T(u).  Write

    Inv_T(N)  =  # adjacent-seam inversions of T at W(N),
    V_T(k)    =  Inv_T(N_k)          (the price T pays at window k).

Skip inversions (u ∈ B_0 placed after w ∈ B_2) are not counted
separately: one skip inversion forces ≥ |B_1 ∩ T| adjacent ones
(notes/47 §0, trichotomy argument — proven).

**Minority profile.**  μ_i(N) = min_T |T ∩ B_i(N)|, the window's
per-block minority sizes; μ(N) = (μ_0, μ_1, μ_2)(N).  Anchor-free
Case 2 (= ¬Case 1, notes/43 §4A / notes/46 §4A(a)):

    m(a) := min_T |T ∩ (a, 2a]|  →  ∞      (a → ∞).

**The budget instance** U(M; c; v_A, v_B) (e127_seam_budget.py): values
(M, 8M]; a 2-coloring with per-team per-block LOWER bounds
c = (c_0, c_1, c_2); a total order per team; no color-guarded monotone
AP in either direction (all in-window APs); inversion indicators
implied one-way by (color ∧ color ∧ order); per-team indicator
cardinality ≤ v_T.  Two bound families:

- constant bounds c (e.g. (2,2,2), (3,6,12));
- ε-linear bounds c_ε(M) = (⌈εM⌉, ⌈2εM⌉, ⌈4εM⌉); "bal" = c_{1/2}
  (exact balance).

**Price function.**  v*_c(M) := least symmetric v with U(M; c; v, v)
SAT.  Well-defined: at v = |B_0||B_1| + |B_1||B_2| the budget is
vacuous and the instance is the notes/36 finite 2-colored theory
(SAT); measured directly, bal@16 is SAT at v = 160.

**Lemma M (monotonicities — proven, two lines each).**
(a) In v: a model at budget v is a model at budget v' ≥ v, so the SAT
region is upward closed and U is UNSAT exactly for v < v*_c(M).
(b) In c: a coloring meeting bounds c' ≥ c (pointwise) meets c, so
SAT(c') ⊆ SAT(c) and v*_{c'}(M) ≥ v*_c(M).  In particular constant-
bound prices floor every ε-linear price:
v*_{c_ε(N)}(N) ≥ v*_{(3,6,12)}(N) whenever c_ε(N) ≥ (3,6,12).

**Measured price data** (data/e127_seam_budget.jsonl, 11 rows;
e128 extending):

    v*_{bal}(16)      ∈ [3, 160]   (UNSAT v = 0,1,2; SAT v = 160, 320, 480)
    v*_{(3,6,12)}(24) ≥ 2          (UNSAT v = 0, 1)
    v*_{(3,6,12)}(32) ≥ 1          (UNSAT v = 0)

and the two decisive SAT rows: asym (A unbudgeted, B ≥ (3,6,12)
budgeted) and majb (majority budgeted, minority free) are both SAT at
v = 0.  **Consequence used repeatedly below: there is no per-team
forced price.  Every demand statement is about max/sum over the two
teams; any "team X must pay" reading is refuted at v = 0 by these two
rows.**

## 2. The demand side

**Lemma T-FORCE (restriction — proven).**  Let (A, B) be a valid pair,
N an anchor with |T ∩ B_i(N)| ≥ c_i for both teams and i = 0, 1, 2.
If moreover Inv_A(N) ≤ v_A and Inv_B(N) ≤ v_B, then
U(N; c; v_A, v_B) is SAT.  Equivalently: **U(N; c; v_A, v_B) UNSAT
⟹ at anchor N, the bounds fail or some team T has Inv_T(N) > v_T.**

*Proof.*  Restrict.  The coloring of (N, 8N] is induced by the
partition; block bounds hold by hypothesis.  Let σ_T be the order
induced on T ∩ W(N) by π_T.  Any in-window AP monotone under σ_T is
monotone under π_T (σ preserves relative order), so the guarded AP
clauses hold in both directions.  σ_T is a total order, so the
transitivity clauses hold.  Set each inversion indicator to the truth
value of its defining condition (color ∧ color ∧ order): the one-way
implication clauses hold, and the indicator count for T is exactly
Inv_T(N) ≤ v_T, satisfying the cardinality constraint.  Every clause
family of U is satisfied.  ∎

Two remarks, both load-bearing.  (i) The lemma consumes only the
*definition* of the instance; its truth does not depend on any solver
run.  Solver runs supply which (M; c; v) are UNSAT.  (ii) The bounds
are lower bounds, so richer windows qualify a fortiori; with Lemma
M(b) a window's best applicable price is the one at its actual
minority profile.

**Corollary D1 (per-window forced price as a function of minority
sizes).**  For a valid pair and any anchor N,

    max(Inv_A(N), Inv_B(N))  ≥  v*_c(N)   for every bound vector
                                          c ≤ μ(N) pointwise,

hence ≥ v*_{μ(N)}(N) (the best applicable price, Lemma M(b) with
c = μ(N)).  In particular V_A(k) + V_B(k) ≥ v*_{μ(N_k)}(N_k) at every
window of the tiling.

*Proof.*  If both teams had Inv ≤ v := v*_c(N) − 1, Lemma T-FORCE
would make U(N; c; v, v) SAT, contradicting Lemma M(a).  ∎

**Lemma D2 (Case-2 floor — proven).**  In anchor-free Case 2, for any
fixed constant bounds c there is N₁(c) with μ(N) ≥ c for all
N ≥ N₁(c) (each block B_i(N) is the ratio-2 window at anchor 2^i·N and
m → ∞).  Hence in Case 2, for every large anchor N:

    max_T Inv_T(N)  ≥  v*_{(3,6,12)}(N)      (constant-bound floor),

and at every ε-linear anchor (μ(N) ≥ c_ε(N)) the stronger
ε-price applies.  ∎

**Corollary D3 (octave recurrence, integrated form — proven).**
Suppose max_T Inv_T(N) ≥ v for every anchor N ∈ [X, 2X).  Then some
team has ≥ v/4 *distinct* adjacent-seam inversion pairs (u, w) with
u ∈ (X, 8X).

*Proof.*  A pair (u, w) is an inversion at W(N) exactly for N in the
two intervals of notes/47 §0, whose union lies in [u/4, u) and has
multiplicative measure ≤ log 4 (machine-audited exactly: e127b).  Let
f_T(N) = # pairs of T that are inversions at W(N).  Pointwise
max(f_A, f_B) ≥ v, so for one team, say A, the set
{N ∈ [X, 2X) : f_A(N) ≥ v} has measure ≥ ½ log 2 (multiplicative);
∫_{[X,2X)} f_A dN/N ≥ ½ v log 2.  A pair contributes ≤ log 4 = 2 log 2
to the integral, and contributes at all only if [u/4, u) meets
[X, 2X), i.e. u ∈ (X, 8X).  Divide.  ∎

(D3 is the "inversions recur in every octave" covering law of
notes/47 §0 in counting form: per 3-octave value range, some team
carries ≥ v*/4 fresh inversion pairs.)

**The demand theorem (modulo one tag).**

> **THEOREM D (demand).**  Assume
> **[GAP-V*]**: there are bounds families and a nondecreasing curve
> v*(·) → ∞, provable by an N2-style schema, with U(N; c; v, v)
> UNSAT for all v < v*(N) — for c = c_ε(N) on ε-linear anchors
> (the balanced pump), and/or for constant c on all Case-2 anchors.
> Then every valid Case-2 pair satisfies, at every large anchor N in
> the family's regime,
>     max_T Inv_T(N) ≥ v*(N) → ∞,
> and per octave [X, 2X) some team owns ≥ v*(X)/4 fresh inversion
> pairs with low member in (X, 8X).

Everything in Theorem D except GAP-V* is proven above.  GAP-V* is
compute-supported (§1 data; e128 bisecting bal@16 between UNSAT-at-2
and SAT-at-160) but has no all-M schema and no growth measurement yet.
It splits honestly into:

- **GAP-V*-growth**: v*_{c_ε}(M) → ∞ (or even just unbounded along a
  syndetic set of M).  Wholly open; the e128 bisection is its first
  data point beyond [3, 160].
- **GAP-V*-schema**: the all-M hand proof of the UNSAT region (the
  GAP-N6a engine one budget-layer up; the M=32 MUS anatomy of
  notes/48 is the intended template).

If v* is instead BOUNDED (schema-stable constant), Theorem D still
holds with v* constant and the ledger degrades to the notes/47 §5.4
fallback: DNP(v*−1) at infinitely many anchors must fail, i.e. the §0
covering statement at a fixed finite budget — a positional invariant,
not treated here.

## 3. The regime trichotomy (formal routing of the supply side)

Let (A, B) be a valid Case-2 pair.  With m(a)/a the minority density
of the ratio-2 window (a, 2a], exactly one of:

**(I) Linear regime:** liminf_a m(a)/a = ε₀ > 0.  Then every large
anchor is ε-linear for any ε < ε₀ (each block is a ratio-2 window),
and Theorem D fires with the ε-price at EVERY large anchor.  This is
the ledger's home; the supply question (§4) is exclusively about this
regime.

**(II) Sparse-scale regime:** liminf m(a)/a = 0: for every δ > 0
there are infinitely many a with some team < δa on (a, 2a] — whose
partner has density > 1 − δ there.  Sub-split, for fixed δ ≤ 3/16, by
whether ONE team is the δ-sparse side on two consecutive octaves
(a, 2a], (2a, 4a] infinitely often:

- **(IIa) repeated-side:** yes.  The partner is ≥ 13/16-dense on two
  consecutive blocks infinitely often; thin to disjoint two-block
  windows; the N5 Part-E density rung (notes/45: fixed pair {15,16},
  window (M, 4M], UNSAT for EVERY in-team subset of per-block density
  ≥ 26/32 at M = 32) + T-PIN kill, **modulo [GAP-RHO]**: (i) the
  scale-stable schema for the ρ*-rung (machine-true at M = 32/64
  brackets only), and (ii) the per-window attacker-pair ownership
  dichotomy (the fixed low pair of each window must be usable — same
  shape as GAP-BRIDGE1, and notes/47 §4b's T-PIN remark; if the dense
  team fails to own the pair at cofinitely many of the windows, the
  minority owns/splits adjacent pairs infinitely often, which is
  landing-pad/BRIDGE1 material).
- **(IIb) no repeated side:** otherwise.  This is BROADER than the
  strict octave-alternation of notes/47 §4b: it also contains
  isolated sub-δ octaves whose neighbours carry minority densities
  above δ but below any linear floor (mixed profiles).  In the alternating sub-case the AP middle
  of every two-octave attack lands in a block where the attacker is
  sparse (notes/47 §4b caveat) and the rungs starve; in the isolated/
  mixed sub-case the two-block rung's 13/16 hypothesis fails on the
  neighbour block.  Both are **[GAP-ALT]** (NECK/d_t extension to
  unbounded dust, a coupled core adapted to alternation, or — since
  Lemma D2 fires at CONSTANT bounds on every Case-2 anchor, mixed
  profiles included — an extension of the §4 supply analysis beyond
  ε-linear anchors, using v*_{μ(N)} at the actual mixed profile).

The split is exhaustive by inspection of liminf and the definition of
(IIa).  Note that (IIa) needs no seam mathematics at all, and (IIb)'s
demand side is already covered by D2; the ledger's supply burden as
developed in §4 is regime (I), as the notes/47 §4b regime map found:
**G2 = "two Θ(M)-dense teams cannot both afford their forced
inversions at every anchor forever"** — with (IIb)'s mixed profiles
the tagged residue.

## 4. The supply side: what CAN a team pay?

The demand side never names the payer (§1, asym/majb rows).  The
supply side must therefore answer: which team can realize, inside one
fixed arrangement π_T valid at ω, the inversion counts that Theorem D
forces *somewhere*, at *every* large anchor simultaneously?

### 4.1 Proven accounting

**P1 (locality / value-single-use).**  In the 8-adic tiling, both
members of an inversion pair at window k lie in W(N_k): pairs at
different windows are distinct pairs of distinct values; the pair
supply is fresh per window.  Anchor-free: pair (u, w) covers only
anchors in [u/4, u), in ≤ 2 intervals (proven, machine-audited
e127b).  *Consequence (no-go direction): no accounting that counts
pairs or values ACROSS windows can bind — freshness is structural.
This is notes/47 §2, now a formal no-go: the ledger must charge
something other than the pairs themselves.*

**P2 (octave recurrence).**  = Corollary D3.

**P3 (displacement floor).**  If u is the low member of an inversion
(u, w) then the running-max stage of N-GEN satisfies
s(u) ≥ blk(w) ≥ blk(u) + 1, i.e. δ(u) ≥ 1: every low member of every
inversion is a displaced value in the sense of the N-GEN chunking
(notes/47 §1).  Moreover, writing D_T(N) for the set of low members at
W(N) ("the displaced set") and A_T(N) for the set of high members
("the advanced set"),

    Inv_T(N) ≤ |D_T(N) ∩ B_0|·|T ∩ B_1| + |D_T(N) ∩ B_1|·|T ∩ B_2|,
    max(|D_T(N)|, |A_T(N)|) ≥ √(Inv_T(N)/2)   (bipartite),

so growing prices force growing displaced or advanced sets:
|D_T(N)| ≥ Inv_T(N)/(4N).

**P4 (skip amplification).**  One skip inversion costs ≥ |B_1 ∩ T|
adjacent ones (notes/47 §0).  At any budget below μ_1(N), no valid
window has skip inversions: displacement depth is one block.

**P5 (unconditional descent pressure — proven).**  For every in-team
AP a < b < c of any valid team, ¬(pos(a) < pos(b) < pos(c)) forces

    pos(b) < pos(a)   or   pos(c) < pos(b):

every in-team AP forces at least one *descent* (larger value earlier)
on one of its two adjacent pairs.  Each ordered pair (x, y), x < y,
is the bottom pair of exactly one AP (x, y, 2y−x) and the top pair of
at most one ((2x−y, x, y), when 2x − y ≥ 1), so distinct APs share a
descent pair only in bounded multiplicity (≤ 2): a team with t
in-window APs carries ≥ t/2 descent pairs there.  If both adjacent
pairs of the AP cross seams of W(N) (the H-family of notes/45/47:
u ∈ B_0, y ∈ B_1, 2y − u ∈ B_2), the forced descent IS an
adjacent-seam inversion, and each seam edge lies in exactly one
H-triple, whence the proven price floor Inv_T(N) ≥ #mono-H_T(N)
(notes/47 §3).  For same-block adjacent pairs the descent is
intra-block and cheap — this is why μ (min mono-H) can be 0 at exact
balance (parity coloring) while v* > 0: v* taxes the JOINT structure
of the cheap dodges, not H alone.

**P6 (density → AP supply; Varnavides).**  A team with ≥ εM values in
an interval of length M contains ≥ c(ε)M² 3-APs (Varnavides).  So in
regime (I), both teams carry Θ(N²) in-window APs at every large
anchor, hence Θ(N²) forced descents (P5).  By contrast a 3-AP-free
team has zero.  **This is the exact wall between the counterexamples
of notes/47 §1 and the linear regime.**

**P7 (sparse payers can afford everything — proven by construction).**
X-INTERLEAVE (T = {2^j}, pairwise-swapped) realizes ≥ 1 inversion
pair covering every anchor; X-INTERLEAVE-v (greedy Behrend
octave-interleave) realizes Θ(N^{1−o(1)}) at every anchor.  Both are
single valid teams.  So: *any supply bound that ignores the payer's
density (or otherwise applies to AP-free sets) is false.*  Re-verified
by e130 (§6): the full accounting of this section, run on
X-INTERLEAVE, charges zero — the construction is legal and MUST
remain legal under any correct supply lemma.

### 4.2 No-go propositions (proven; they delimit L-AFFORD's shape)

**NG1 (no single-team supply lemma).**  P7.  The affordability lemma
must use the partition: both teams' densities (regime I) and the
single-use coloring — each value has exactly one color — are the only
joint resources.

**NG2 (positions are not a joint resource).**  π_A and π_B are
separate ω-orders; no position is shared between teams.  Hence any
"position single-use" accounting is intrinsically single-team, and by
NG1 cannot close the gap alone.  The single-use resource that IS
joint: **values and their colors** — a value donated to the partner
(to void an AP) is donated once and for every scale simultaneously;
a value's color serves all windows it attacks or shields.  (This is
where the candidate of the task prompt — "positions are single-use;
count positions vs forced prices" — lands after inspection: position
single-use survives as P1/P3 *within* one team, binds nothing alone
(P7 realizes maximal per-window prices with legal positions), and the
cross-team ledger must be denominated in colored values/APs.  The
machine confirmation that the position accounting does NOT kill
X-INTERLEAVE is e130 check 1.)

**NG3 (no cross-window pair counting).**  P1 consequence; notes/47 §2.

### 4.3 The exposure cascade (candidate mechanism for L-AFFORD)

For u ∈ T define the *top set*
Top_T(u) = {(a, b) : b ∈ T ∩ (u/2, u), a = 2b − u ∈ T} — the in-team
APs with largest element u.

**L-ORIENT (proven).**  Let u ∈ T and (a, b) ∈ Top_T(u) with both
a, b placed before u in π_T.  Then pos(b) < pos(a) is forced (else
(a, b, u) is increasing-monotone; the decreasing direction needs u
first, excluded).  Moreover:

**L-COMP (proven, the composition trap).**  If (b → a) and (c → b)
are both forced descents (pos(c) < pos(b) < pos(a)) and (a, b, c) is
an AP, the team is dead: this is exactly a decreasing monotone AP.
So the forced-descent digraph of any valid team contains no directed
2-path along an AP.  *Supply cap in embryo: forced descents are a
resource-constrained commodity — they may not compose along APs.*

**L-CASCADE (proven, the down-window forcing).**  Let u be displaced
(P3) and (a, b) ∈ Top_T(u) with a, b before u and b ∈ (4u/7, 3u/4).
Then a = 2b − u ∈ (u/7, u/2), b < 4a, and the forced descent
(b before a) is itself an adjacent-seam inversion pair (low a, high
b) at every anchor it covers, which lie in [a/4, a) ⊆ [u/28, u/2):
**exposure of a displaced value is paid in forced inversions 1–5
octaves down.**  Consecutive windows' ledgers are coupled through
these pairs even though their inversion supplies are value-disjoint —
the coupling is through the ORDER of the lower window's material,
which is a single object serving both its own window's budget anatomy
and the exposure demands from above.  (This is the precise content of
"the same value cannot serve two windows": the pair (a, b) has ONE
relative order in π_T; window k's escape anatomy and window k−1's may
demand opposite orientations, and any AP-composition among forced
descents is fatal by L-COMP.)

**The three-outflow alternative (proven as an alternative; its
quantitative version is the gap).**  Fix a displaced u ∈ D_T(N) and
any (a, b) with b ∈ T ∩ (4u/7, 3u/4), a = 2b − u.  Then exactly one
of:

1. **comply**: a ∈ T and a, b placed before u — descent b → a forced
   (a seam inversion at anchors in [a/4, a); composition-constrained
   by L-COMP);
2. **procrastinate**: a ∈ T but not both of a, b before u — some
   member of the AP is itself delayed past u.  If a is the delayed
   one, the pair (a, u) has u/a ∈ (2, 7): for u/a < 4 it is a fresh
   adjacent-seam inversion at anchors below [a/4, a) ⊂ [u/28, u/2)
   (the recursion re-enters one octave band down); for u/a ≥ 4 it is
   skip-type at the anchors where a and u sit two blocks apart, and
   P4 amplifies it to ≥ μ_1-many adjacent inversions there.  If only
   b is the delayed one (b ∈ (u/2, u), ≤ 1 block below u), the charge
   is weaker: an adjacent inversion (b, u) only at the anchors
   separating them — the cheap end of the outflow;
3. **donate**: a ∉ T — the value 2b − u is the partner's.  Summed
   over b, donations pin the partner's density UP on the arithmetic
   progression {2b − u : b ∈ T ∩ (4u/7, 3u/4)} (a structured,
   positioned gift: in regime (I) the partner is Θ-dense there
   already, and P6 applies to ITS APs through the donated values).

**[GAP-AFFORD] (THE remaining gap, successor of GAP-G2), candidate
statement.**

> **L-AFFORD (candidate).**  For every ε > 0 there is a function
> g_ε(N) = o(v*_{c_ε}(N)) (if GAP-V*-growth holds; in general
> g_ε = o(sup of the forced curve)) such that: for every valid pair
> (A, B) that is ε-linear at all large anchors,
>
>     liminf_{N→∞}  max_T Inv_T(N) / v*_{c_ε}(N)  <  1.
>
> (Weakest sufficient form: ONE arbitrarily large cheap anchor.
> Stronger candidate forms, in decreasing plausibility: liminf of
> max_T Inv_T(N)/v* < 1; max_T Inv_T(N) ≤ g_ε(N) along a syndetic
> anchor set; max_T Inv_T(N) = O(1) — surely false, given the SAT
> escapes pay hundreds already at M = 16.)

Candidate proof route (all sub-links open):

- **[GAP-COMP]** quantify L-COMP: a Θ-dense team whose forced-descent
  digraph on an ε-linear window carries ≥ h(N) compliant descents
  must contain an AP-composable 2-path once h(N) exceeds a threshold
  (extremal/Ramsey counting over Varnavides mass; the threshold's
  scaling in N is the whole question — note the intra-block descents
  of P5 already number Θ(N²) legally, so the count must be restricted
  to the CROSS-block forced descents seeded by D_T and their
  interaction with the window's own price anatomy).
- **[GAP-JOINT]** close the two-team bookkeeping: outflow 3 donates
  each value once (values single-use across the ledger — the true
  joint resource, NG2), donations are shared among many demands
  (shared-endpoint problem), and the measured p(k) growth
  (p(1..4) = 3, 7, 7, 11, notes/46 Part B) is the finite evidence
  that sharing does not collapse the price; outflow 2 recurses
  downward with P4 amplification and must terminate (well-founded on
  ratio-2 scales above N₁ only if the amplified prices eventually
  exceed supply — this is where the recursion needs GAP-COMP again
  one level down).  Measured ordering (e130 check 3, §6): on the
  bal@16 v=160 witness the operative outflow is DONATION (7/13 resp.
  8/11 of visible instances) plus a below-window surface twice the
  in-window mass — GAP-JOINT is the live sub-gap at small M, and the
  downward-extended (4-block) gadget is the instrument that would
  charge the below-window channel.

The honest status of the mechanism: L-ORIENT/L-COMP/L-CASCADE and the
three-outflow alternative are proven; every quantitative link between
them is open.  What the mechanism has that all dead routes lacked:
(i) it is void on AP-free payers (Top ≡ ∅) — consistent with NG1
rather than refuted by it; (ii) it charges a genuinely joint currency
(colored values, donations) — consistent with NG2; (iii) it couples
consecutive windows through order, not through pair supply —
consistent with NG3; (iv) its finite shadows are measurable (e130
check 3 measures the exposure mass on a real e127 witness).

## 5. The ledger theorem

> **THEOREM LT (T-FORCE ledger; conditional).**  Assume
> [GAP-V*-schema] + [GAP-V*-growth] (Theorem D's curve, unbounded on
> ε-linear anchors) and [GAP-AFFORD] (L-AFFORD, any of its
> sufficient forms).  Then no valid pair is in regime (I).
>
> *Proof.*  Let (A, B) be valid, Case 2, regime (I) with parameter
> ε₀ and ε < ε₀.  By Theorem D (proven modulo GAP-V*), for all
> N ≥ N₀:  max_T Inv_T(N) ≥ v*_{c_ε}(N).  By L-AFFORD there is an
> anchor N ≥ N₀ with max_T Inv_T(N) < v*_{c_ε}(N).  Contradiction.  ∎
>
> **Corollary (Case-2 closure, conditional).**  Adding [GAP-RHO] and
> [GAP-ALT] (regime II, §3), no valid pair is in Case 2.  With the
> Case-1 chain (GAP-N2 + GAP-N3 + GAP-BRIDGE1 + T-PIN) this yields
> Erdős #197 = NO.

Note the shape: the contradiction is PER-ANCHOR (one cheap anchor vs
demand-everywhere) — no infinite pigeonhole, no descent, no counting
across windows survives in the final step, exactly as the no-go
propositions require.  All infinitude lives inside the two curves
(v* forced up by the schema; affordability capped by the exposure
ledger), which is where it can be attacked by finite machine probes.

Degenerate branch (v* bounded): if GAP-V*-growth FAILS with a
schema-stable constant v̄, Theorem D still forces
max_T Inv_T(N) ≥ v̄ at all large Case-2 anchors, and the program
falls back to the covering-invariant route of notes/47 §5.4 at fixed
budget v̄ − 1 (attack DNP(v̄−1) via the §0 covering statement +
L1'/ledger machinery).  The e128 bisection decides which branch is
real — this note is written to receive either answer: only the
constants in Theorem D change.

## 6. Machine spot-checks (e130 — RUN, all pass)

experiments/e130_ledger_checks.py → data/e130_ledger_checks.json/.log.
Per-claim checks, none touching running solvers' files:

1. **X-INTERLEAVE survival (P7/NG1/NG2 consistency) — PASS.**
   Swapped-powers arrangement to 2^20: the set is 3-AP-free and every
   Top set is empty (audited explicitly); the arrangement is
   monotone-AP-free; its inversion pairs are exactly the family
   (4^k, 2·4^k) and cover EVERY anchor 1..4^7 (exhaustive audit by
   the direct block-membership definition, independently re-deriving
   notes/47 §1); δ = 1 exactly on every displaced value; **the §4
   accounting charges 0** (no Tops ⟹ no forced descents ⟹ no
   cascade).  The single-team counterexample is LEGAL under the
   ledger, as required: the binding resources (partner density,
   donations) do not exist for a lone AP-free team.
2. **Covering integration constant (D3) — PASS.**  43 trials (random
   pair families + the X-INTERLEAVE family, X up to 1024), count
   ≥ v/4 held in all, v computed by exhaustive per-anchor coverage.
3. **Exposure mass on the dense bal@16 v=160 witness — PASS, with an
   honest surprise.**  Recounts match the recorded anatomy exactly
   (A: 85 inversions, B: 105; both orders monotone-AP-free).
   Displaced sets |D_A| = |D_B| = 8, advanced 11/14.  Exposure of the
   displaced values: in-window Top instances only 6 (A) / 3 (B),
   L-CASCADE range mass 0, below-window exposure surface 15/17
   (unseen by the finite instance).  **The witness's displaced values
   are exposure-LIGHT, not exposure-heavy** — the escape selects
   displaced values whose Top sets are voided.  Outflow
   classification (per §4.3): A: 2 comply / 4 procrastinate /
   7 donate / 15 below-window; B: 1 / 2 / 8 / 17.  So at M = 16 the
   operative dodge is outflow 3 (donation) plus the below-window
   surface: the finite escape parks ~2/3 of its visible exposure on
   the partner's color and ~2× that mass below the window where the
   instance cannot charge it.  This sharpens the gap ordering:
   GAP-JOINT (donation bookkeeping) is the operative sub-gap at small
   M, not GAP-COMP; and the 4-block/downward-extended gadget
   (L-EXPOSE, notes/47 §5.3) is the right next instrument because the
   below-window surface is the largest single channel measured.
4. **P5/P6 sanity — PASS.**  Witness teams carry 464/338 in-window
   APs (Varnavides scale — both > M² = 256), every single AP carries
   a descent on an adjacent pair (P5 audit: zero violations),
   distinct descent pairs 368/252 ≥ #APs/2.  AP-free teams: 0.
5. **L-COMP audit — PASS.**  30 random monotone-AP-free orders
   (n ≤ 26): the forced-descent digraph contains a directed 2-path
   along an AP **iff** the AP is a decreasing monotone AP — never, on
   AP-free orders (definition audit; 2-path ⟺ fatal confirmed
   pointwise).

## 7. Link table (for notes/50)

| Tag | Statement | Status |
|-----|-----------|--------|
| GAP-V*-schema | all-M UNSAT region of U(N; c; v < v*(N)) | machine-true at listed points; N6a engine one budget-layer up |
| GAP-V*-growth | v*_{c_ε}(M) → ∞ | open; e128 bisecting bal@16 in [3, 160] |
| GAP-AFFORD | L-AFFORD (§4.3), any sufficient form | open; mechanism candidate = exposure cascade; sub-tags GAP-COMP, GAP-JOINT |
| GAP-RHO | ρ*-rung scale-stable schema + per-window pair ownership | machine-true M=32; ownership = BRIDGE1-shaped |
| GAP-ALT | regime (IIb): alternating OR isolated/mixed sparse octaves | open (NECK/d_t at unbounded dust; or supply analysis at mixed profiles v*_{μ(N)}) |
| (proven here) | Lemmas M, T-FORCE, D1–D3; P1–P7; NG1–NG3; L-ORIENT, L-COMP, L-CASCADE; three-outflow alternative; Theorem LT's derivation from the tags | hand-complete; spot-checked §6 |
