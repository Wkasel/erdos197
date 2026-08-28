# 55 — GAP-N6a: hand proof of the two-seam coupled core schema (in progress)

Companion to notes/51 (the locked schema), notes/48 (MUS anatomy),
notes/33 (the C3 hand-proof toolkit Z/D/E/P), notes/54 (ledger
vocabulary).  Machine lock: data/e135_lock.log + data/e134_schema2.log
— the instance below is UNSAT at all five scales M = 32 (bounds
(3,3,3)), 48, 64, 80, 96 (bounds (2,2,2)).

**This note is written incrementally; every section ends with its
verification pointer and a status tag [PROVED] / [MACHINE-CHECKED] /
[GAP].  The gap ledger is §7.**

---

## 0. The target instance and the theorem to prove

Fix M (target residue/threshold: M ≡ 0 (mod 16), M ≥ 48; each lemma
below states the residue/threshold it actually needs, and §7 collects
them).  Blocks of the window (M, 8M]:

    B0 = (M, 2M],   B1 = (2M, 4M],   B2 = (4M, 8M].

**The core support** (exactly as in experiments/e135_schema_lock.py —
note both band ends are INCLUSIVE where the running text of notes/51
was loose):

    P0 = [M+1, 2M]        (all of B0; M values)
    P1 = [3M−15, 4M]      (top band of B1; M+16 values)
    P2 = [4M+1, 6M+15]    (bottom-to-flood band of B2; 2M+15 values)
    V  = P0 ∪ P1 ∪ P2     (the core CORE′(M); 4M+31 values)

**The coupled instance CI(M).**  A *state* is a 2-coloring
χ : V → {A, B} together with, for each team T ∈ {A, B}, a linear
order ≺_T of T := χ⁻¹(T).  A state is *feasible* iff

  (i)   [AP-freeness]  for every integer 3-AP a < b < c (a + c = 2b)
        with a, b, c ∈ T:  neither a ≺_T b ≺_T c nor c ≺_T b ≺_T a;
  (ii)  [block order, both seams + outer]  for u, w ∈ T with u in a
        lower block than w (B0 < B1, B1 < B2, B0 < B2): u ≺_T w;
  (iii) [bounds]  |T ∩ Pi| ≥ 2 for both teams and every i ∈ {0,1,2}
        (≥ 3 at M = 32).

**Theorem N6a (target).**  CI(M) has no feasible state for any
M ≡ 0 (mod 16), M ≥ 48.

[MACHINE-CHECKED at M = 32, 48, 64, 80, 96: e134/e135, CaDiCaL via
pysat, UNSAT in 5–402 s; data/e135_lock.log.]  The goal of this note
is the uniform hand proof.  Why this matters: notes/45–51 reduce the
Case-2 arm of the NO program to exactly this schema; a uniform proof
of Theorem N6a closes GAP-N6a.

Convention: "u ≺ v" = u is placed before v.  For a team T we write

    U = T ∩ P0,   Y = T ∩ P1,   Z = T ∩ P2,

and U′, Y′, Z′ for the other team T′.  A *mono* tuple is one whose
members all lie in one team.

---

## 1. Unit rules and the decomposition lemma  [PROVED]

### 1.1 Midpoint-extremal rules (port of notes/33 §1)

For a team T and an AP (a, b, c) ⊆ T with a, b, c ∈ V, constraint (i)
says the midpoint b either leads both endpoints or trails both.  With
totality of ≺_T this gives the four unit rules, verbatim notes/33:

    R1: a≺b ⟹ c≺b     R3: c≺b ⟹ a≺b     (b trails both)
    R2: b≺c ⟹ b≺a     R4: b≺a ⟹ b≺c     (b leads both)

These hold for every in-team AP regardless of blocks.  [PROVED —
identical two-line argument as notes/33 §1.]

### 1.2 Block classification of the core's APs

Every AP a < b < c of V is classified by the block pattern
(blk(a), blk(b), blk(c)) ∈ {0,1,2}³, nondecreasing.  Ten patterns are
conceivable; one is arithmetically empty in CORE′:

* (0,0,2) is EMPTY: a, b ∈ P0 gives c = 2b − a ≤ 4M − (M+1) = 3M−1
  < 4M+1.  [PROVED]

The nine remaining: (0,0,0), (1,1,1), (2,2,2) [in-block]; and six
mixed patterns.  For each mixed pattern, block order (ii) decides one
of the two forbidden monotone patterns for free, and AP-freeness
leaves exactly one *unit* (a forced orientation inside a single
block), EXCEPT the straddle pattern (0,1,2), which is fully forced
and hence outright forbidden:

| pattern  | seam gives      | AP-freeness leaves        | unit lives in |
|----------|-----------------|---------------------------|---------------|
| (0,0,1)  | a≺c, b≺c        | ¬(a≺b): **b ≺ a**         | P0            |
| (0,1,1)  | a≺b, a≺c        | ¬(b≺c): **c ≺ b**         | P1            |
| (1,1,2)  | a≺c, b≺c        | ¬(a≺b): **b ≺ a**         | P1            |
| (0,2,2)  | a≺b, a≺c        | ¬(b≺c): **c ≺ b**         | P2            |
| (1,2,2)  | a≺b, a≺c        | ¬(b≺c): **c ≺ b**         | P2            |
| (0,1,2)  | a≺b, b≺c        | nothing left: **forbidden** | —           |

(In each row the decreasing pattern c≺b≺a is already broken by the
seam constraint shown; the unit is what breaks the increasing one.)

### 1.3 The decomposition lemma

For a team T define the three *block theories*:

**Th0(T)** — order theory on U: AP-freeness on all APs ⊆ U; plus
units b ≺ a for every AP (a, b, c), a, b ∈ U, c ∈ Y ∪ Z  [(0,0,1);
(0,0,2) is empty].

**Th1(T)** — order theory on Y: AP-freeness on all APs ⊆ Y; plus
(α) units c ≺ b for every AP (a, b, c), a ∈ U, b, c ∈ Y  [(0,1,1)];
(β) units b ≺ a for every AP (a, b, c), a, b ∈ Y, c ∈ Z  [(1,1,2)].

**Th2(T)** — order theory on Z: AP-freeness on all APs ⊆ Z; plus
units c ≺ b for every AP (a, b, c), a ∈ U ∪ Y, b, c ∈ Z  [(0,2,2),
(1,2,2)].

**Lemma U (decomposition).**  A team T admits an order ≺_T
satisfying (i) and (ii) if and only if

  (S)  T contains no straddle: no u ∈ U, y ∈ Y with 2y − u ∈ Z; and
  (B)  each of Th0(T), Th1(T), Th2(T) is consistent (has a linear
       order of its block satisfying all its constraints).

*Proof.*  (⟹)  Restricting ≺_T to each block satisfies the in-block
AP constraints; the table of §1.2 derives each unit from (i) + (ii)
(each mixed AP's decreasing pattern dies by the seam order, so
AP-freeness forces the negation of the one free comparison in the
increasing pattern); a straddle (u, y, z) would have u ≺ y (seam 1)
and y ≺ z (seam 2), a monotone AP, contradicting (i).

(⟸)  Concatenate the three block orders: all of U in Th0's order,
then Y in Th1's, then Z in Th2's.  (ii) holds by construction.  For
(i): in-block APs are non-monotone by the block AP-freeness; each
mixed AP of a pattern in the table has its decreasing pattern broken
by concatenation and its increasing pattern broken by the pattern's
unit; (0,1,2) APs do not exist inside T by (S); (0,0,2) APs do not
exist in V at all.  The ten-pattern enumeration is exhaustive.  ∎

**Consequence (shape of the whole proof).**  A feasible state of
CI(M) is exactly: a 2-coloring meeting the bounds, *straddle-free for
both teams*, such that all six block theories Th_i(T), Th_i(T′) are
consistent.  Theorem N6a says: no such coloring exists.  The hand
proof must therefore intertwine coloring arguments (which units
fire / which straddles are forbidden) with order arguments (ladders
and floods refuting the fired unit systems) — unlike the C3 core of
notes/33, where the attack units were unconditional.

[MACHINE-CHECK: experiments/e136_u_decomp_check.py — (1) re-derives
the §1.2 pattern table by brute enumeration of every AP of CORE′(M)
at M = 48, 64, 80 (assertions on emptiness of (0,0,2), on the
completeness of the ten patterns, and on the exact unit family each
mixed AP contributes); (2) implements the decomposed encoding
(coloring + three per-team block orders + (S) + the §1.3 units) and
cross-validates it against the monolithic e135 encoding: UNSAT at
M = 48 bounds (2,2,2) like e135; verdict equality at M = 48 bounds
(1,1,1), with the decomposed witness re-assembled by concatenation
and re-checked by the independent e120 checker.  data/e136_u.log.]

---

## 2. The attack geometry of CORE′ (arithmetic catalogue)  [PROVED]

Named landmarks (all match the notes/51 anchor families):

    S1 = [2M−7, 2M]        B0's top-8         (crown midpoints)
    E1 = [3M−15, 3M]       P1's bottom-16     (the band edge)
    R  = [4M−15, 4M]       P1's top-16        (the top run; S2 = top-8)
    S3 = [4M+1, 4M+16]     P2's bottom-16     (doubling image of R)
    G  = [4M+1, 4M+7]      P2's bottom-7      (boundary-rung midpoints)
    F  = [6M+1, 6M+15]     the flood band     (6M = B2's centre; 6M ∈ P2)

All statements below are elementary interval arithmetic; each is
proved by the displayed inequalities and machine-checked by exact
set-comparison at M = 48, 64, 80 (e137).  Threshold: M ≥ 48 (most
hold from M ≥ 32).

**Lemma A1 (seam-1 crown; the (0,0,1) family — FINITE, 64 APs at
every scale).**  The APs (a, b, c) with a, b ∈ P0, c ∈ P1 are exactly

    a ∈ [M+1, M+15],  b ∈ S1,  c = 2b − a ∈ [3M−15, 3M−1] ⊂ E1,
    subject to a ≤ 2b − 3M + 15.

*Proof.*  c ≤ 2·2M − (M+1) = 3M−1 always; c ≥ 3M−15 forces
a ≤ 2b−3M+15 ≤ M+15 and b ≥ (a+3M−15)/2 ≥ 2M−7.  Count:
b = 2M−k (k = 0..7) admits a ∈ [M+1, M+15−2k], i.e. 15−2k values;
Σ = 64.  ∎

So Th0(T)'s ONLY units are: b ≺ a with b ∈ S1 ∩ U, a ∈ P0's
bottom-15 ∩ U, guarded by 2b − a ∈ Y ∩ E1.  The band edge 3M−15
exists exactly to keep this family alive: it is the C3 crown
{15, 16} geometry reborn at seam 1.  ((0,0,2) is empty, §1.2.)

**Lemma A2 (band-edge attack; the (0,1,1) family — FINITE, 256 APs
at every scale).**  The APs (x, y, z) with x ∈ P0, y, z ∈ P1 are
exactly

    y ∈ E1  (write y = 3M−k, k = 0..15),   x ∈ [2M−2k, 2M],
    z = 2y − x ∈ [4M−2k−15, 4M] ⊂ [4M−30, 4M],

with gap d = y−x = z−y ∈ [M−15, M+15].  Midpoints are the band's
bottom-16, tops the band's top-31, attackers B0's top-31.

*Proof.*  x ≥ 2y−4M (z ≤ 4M) and x ≤ 2M give nonemptiness iff
y ≤ 3M; y ≥ 3M−15 is the band edge; the rest is substitution.
Count: Σ_{k=0..15} (2k+1) = 256.  ∎

The α-units of Th1(T) are therefore: z ≺ y with z in the top-31,
y in the bottom-16 — a band-top value forced EARLY relative to a
band-bottom value, against numeric order, guarded by an attacker
x ∈ U ∩ [2M−30, 2M].

**Lemma A3 (high-pair closure — the seam-2 wall).**  For every pair
a < b ⊆ P1 with 2b − a ≥ 4M+1 ("high pair"), the completion
c = 2b − a lies in P2, because c ≤ 2·4M − (3M−15) = 5M+15 ≤ 6M+15.
Moreover c ≤ 5M+15 < 6M+1 (M ≥ 15): band completions NEVER reach the
flood band F; they land in [4M+1, 5M+15], the bottom M+15 values of
P2.  High-pair midpoints satisfy b ≥ ⌈(7M−14)/2⌉ (band top half).
[PROVED]  Hence the β-units of Th1(T): for every high pair
a < b ⊆ Y whose completion 2b−a lies in Z, the unit b ≺ a fires.
Contrapositive = the donation principle of §4.

**Lemma A4 (doubling image; parents of P2's bottom).**  For
s ∈ [1, M+15], the band parents of z = 4M+s (the (1,1,2) APs with
top z) are exactly

    (a, b) = (4M−s−2t, 4M−t),   t = 0, 1, …, ⌊(M+15−s)/2⌋.

In particular: S3's values 4M+j (j ≤ 15) have ⌊(M+15−j)/2⌋+1 ≈ M/2
parents each, including the top-run parents (4M−j−2t, 4M−t) ⊆ R for
j+2t ≤ 15; and the extreme value 5M+15 has the single parent
(3M−15, 4M) — the full-span pair of the band.  [PROVED: substitute
a = 2b − z.]

**Lemma A5 (boundary rung; the (0,2,2) family — FINITE, 56 APs at
every scale).**  The APs (x, y, z) with x ∈ P0, y, z ∈ P2 are exactly

    y = 4M+m ∈ G (m = 1..7),   z ∈ [6M+2m, 6M+15] ⊂ F,
    x = 2y − z = 8M+2m−z ∈ [2M+2m−15, 2M]  (B0's top-15);

count Σ_{m=1..7} (16−2m) = 56.  *Proof.*  z ≤ 6M+15 and x ≤ 2M give
y ≤ 4M+7; z = 2y−x ≥ 2(4M+1)−2M = 6M+2.  ∎
Units: z ≺ y with z ∈ F, y ∈ G — a flood-band value forced BEFORE a
bottom-of-P2 value in T's P2 order, guarded by x ∈ U ∩ B0-top.
This couples F's order position to S3's, across the whole of P2 —
the "width-15 boundary rung".

**Lemma A6 (midband attack; the (1,2,2) family).**  The APs
(x, y, z) with x ∈ P1, y, z ∈ P2 are exactly

    y ∈ [4M+1, 5M+7],   z ∈ [max(y+1, 2y−4M), min(6M+15, 2y−3M+15)],
    x = 2y − z ∈ P1,

with gap d = y−x ∈ [y−4M, y−3M+15].  Midpoints reach only 5M+7; tops
cover up to 6M+15 — in particular every F-value f is the top of
(1,2,2) APs with midpoints y ∈ [⌈(f+3M−15)/2⌉, ⌊(f+4M)/2⌋] (a
≈ M/2-deep family in P2's midband [4.5M−7, 5M+7]).  [PROVED by the
same substitutions.]

**Lemma A7 (straddle geometry; the (0,1,2) family).**  The straddles
are u ∈ P0, y ∈ P1, z = 2y−u ∈ [4M+1, 6M+15].  Facts:
  (a) z ≡ u (mod 2) — a straddle's endpoints share parity; this is
      the arithmetic room for the machine's parity dodges.
  (b) F-straddles: z ∈ F forces y ∈ [⌈(7M+2)/2⌉, 4M] (band top
      half) and u = 2y − z ∈ [M+1, 2M−1]; every F value is
      straddle-reachable, and through y = 4M the attackers are
      exactly u ∈ [2M−15, 2M−1]:  F = 2·4M − [2M−15, 2M−1] is the
      doubling image of B0's top-15 shifted run through the band top
      (the notes/51 S3 = 2×S2 coupling in its seam-crossing form).
  (c) Full-block pressure zone: for y ∈ [3M+1, ⌊(7M+14)/2⌋] every
      u ∈ P0 completes into P2 (2y−u ∈ [2y−2M, 2y−M−1] ⊆ P2).  So
      straddle-freeness for a team T with y ∈ Y in this middle zone
      reads: Z ∩ (2y − U) = ∅ — an |U|-sized punch into Z per such y.
  (d) For y ∈ E1 (band edge): completions 2y−u ∈ P2 exactly for
      u ≤ 2y−4M−1 ≤ 2M−31; the band-edge value 3M−15 completes to
      the very bottom of P2 (z = 4M+1 at u = 2M−31).

**Lemma A8 (mirror window at 6M).**  The in-P2 APs centred at 6M are
(6M−e, 6M, 6M+e) for e ∈ [1, 15] exactly (upper cap from
6M+e ≤ 6M+15).  More generally a centre c ∈ P2 has mirror width
min(c−4M−1, 6M+15−c), maximal (M+7) at c = 5M+8; at c = 6M the
width is exactly 15 and the upper mirror range is precisely F: the
flood band is BY CONSTRUCTION the mirror partner of (6M−15, 6M).
[PROVED]

**Lemma A9 (what constrains F).**  No (1,1,2) completion lands in F
(A3) and no (0,2,2)/(1,2,2) AP has its midpoint in F (midpoints
≤ 5M+7 < 6M+1).  Hence the complete list of constraints touching a
value f ∈ F is:  (i) straddle exclusions through band-top-half
midpoints (A7b);  (ii) units f ≺ y from A5 (y ∈ G, attacker in
B0-top) and from A6 (y ∈ [⌈(f+3M−15)/2⌉, 5M+7], attacker in P1);
(iii) in-P2 AP-freeness (mirror APs at 6M and the d-ladders of P2).
In particular every fired unit pushes f EARLY in T's P2 order.
[PROVED from A3, A5, A6]

**Scale-invariance summary.**  The finite families (A1: 64, A2: 256,
A5: 56) are the O(1) unit schemas of the proof; the scaling families
(A4/A6/A7: Θ(M²)) enter only through ladders and floods (Θ(M) rungs,
O(1) schema), exactly as in the C3 proof (notes/33 §7, S4).

[MACHINE-CHECK: experiments/e137_core_arith.py — exact set equality
of every catalogued family against brute AP enumeration at
M = 48, 64, 80, plus the corollary inequalities (A3 wall 5M+15 <
6M+1; A4 parent counts; A5/A6 range formulas; A7 parity & pressure
zone; A8 widths; A9 emptiness claims).  data/e137_arith.log.]

---

## 3. Ladders in the band and the seam-2 transfer

### 3.1 Ported order lemmas and the mono-run caveat  [PROVED]

The C3 toolkit lemmas are order-theoretic and block-agnostic; they
port verbatim with one proviso.

**Seesaw (midpoint lock).**  For an in-team AP (p, q, r):
p ≺ q ⟺ r ≺ q (both ⟺ "q trails both"), and q ≺ p ⟺ q ≺ r.
Orientations of the two adjacent pairs around a midpoint are locked
anti-symmetrically: (p,q) ascending ⟺ (q,r) descending.  [PROVED —
restatement of R1–R4.]

**Lemma Z′ (mono zigzag).**  Let w₀, …, w_r be consecutive rungs of
a d-ladder inside one block, ALL IN one team T.  If some adjacent
pair is oriented, then every second rung leads both its neighbours
(the zigzag).  **Lemma D′ (phase dichotomy).**  Every such mono run
is globally in one of its two zigzag phases.  [PROVED — the notes/33
§2 proofs verbatim; they use only Seesaw on consecutive rung
triples, which are in-block APs of V, and totality.]

**The mono-run caveat.**  Unlike C3, the rungs here must be
*certified same-team*: the coloring adversary can cut every ladder.
Every zigzag/flood application below therefore carries an explicit
mono-run hypothesis, and discharging those hypotheses (via the
bounds and the coloring constraints) is exactly the assembly problem
of §5–6.  This is the single structural difference from notes/33,
and it is where the remaining gaps live.

### 3.2 The seam-2 transfer lock: donation and clash  [PROVED]

**Lemma E2 (donation).**  For a team T and a high pair a < b ⊆ Y
(2b − a ≥ 4M+1):  if a ≺_T b then 2b − a ∈ Z′ (the OTHER team's P2
set).  *Proof.*  2b − a ∈ P2 by A3; if it were in Z, the β-unit of
Th1(T) fires b ≺ a, contradicting a ≺ b.  ∎

This is the analogue of C3's transfer Lemma E, with a twist: the C3
lock tied order to order inside one block; E2 ties BAND ORDER to
P2 COLORING across seam 2.  An ascending high pair *donates* its
completion to the other team.

**Lemma C (clash).**  Every z ∈ [4M+1, 5M+15] lies in exactly one
team; consequently, for every z, at least one team has ALL its mono
parent pairs (Lemma A4) of z descending: z ∈ T forces every mono-T
parent of z descending (β-units), while mono-T′ parents of z are
unconstrained by z — and vice versa.  In particular no z may be the
completion of ascending mono pairs of both teams.  [PROVED — Lemma
E2 for both teams.]

### 3.3 Unit-seeded phases  [PROVED]

Every A4 parent pair (4M−s−2t, 4M−t) of z = 4M+s is the TOPMOST
adjacent pair of its gap-(s+t) ladder in the band (the next rung up,
4M−t+(s+t) = 4M+s, exits P1); conversely each d-ladder of the band
has exactly one high adjacent pair, its topmost.  [PROVED; machine:
e138 part A at every M ≡ 0 (16) in 48..400.]  Hence:

* (membership ⟹ phase)  If z = 4M+s ∈ Z and a parent pair
  (a, b) = (4M−s−2t, 4M−t) ⊆ Y, the fired unit b ≺ a seeds, along
  the maximal mono run of the (s+t)-ladder containing it, the zigzag
  phase in which b's side descends; by Seesaw the next rung down
  ascends: a−(s+t) ≺ a whenever a−(s+t) ∈ Y, and so on down the run
  (Lemma Z′).
* (phase ⟹ membership)  If the topmost adjacent pair of a d-ladder
  mono run of T is ascending — e.g. forced by a zigzag phase seeded
  anywhere in the run — then its completion 4M + (d − (4M − top))
  belongs to T′ (Lemma E2).

Each gap-d ladder of T's band that reaches the top run thus ties its
phase bit to the team-membership of one bottom-of-P2 value; the
values 4M+1 … 4M+15 collectively interrogate the phases of the
d = 1 … 15 ladders (and, through the t-shifts, deeper ladders too).

### 3.4 Lemma J (top-run lock — finite, M-independent)
[MACHINE-CHECKED]

Offset coordinates: w_i := 4M−15+i (i = 0..15), so R = {w₀…w₁₅}.
For J ⊆ [1, 15] let T(J) be the order theory on 16 points:
AP-freeness of the integer 16-interval (56 APs) + the units

    w_{15−t} ≺ w_{15−j−2t}    for j ∈ J, t ≥ 0, j + 2t ≤ 15

(the Th1 β-units fired by S3-memberships {4M+j : j ∈ J} ⊆ Z when
R ⊆ Y).  Call J *admissible* iff T(J) is consistent.

**Lemma J.**  Admissibility is a downset; its minimal forbidden sets
are exactly 30 PAIRS and 6 TRIPLES:

    pairs   j ↔ j′:  1:{2,3,4,6,8}  2:{3,4,5,7,9,11}  3:{4,5,6,8,10,12}
                     4:{5,6,7,9,11}  5:{6,8}  6:{7,9,11}  7:{8}
                     8:{9,11}
    triples (1,10,12) (4,13,15) (5,10,12) (7,10,12) (9,10,12) (10,11,12)

and the maximum admissible size is 9 (e.g. {1,5,7,9,11,12,13,14,15}).
[MACHINE-CHECKED: e138 part B — exhaustive over all 2¹⁵ sets with
downset pruning, 1148 CaDiCaL solves on the 16-point theory;
data/e138_transfer.json.  The check is FINITE and M-independent: the
16-interval AP structure and the unit schema contain no M.]

**Corollary J1.**  If a team T contains the whole top run R, then
J_T = {j ∈ [1,15] : 4M+j ∈ Z} is admissible; hence
(a) |Z ∩ [4M+1, 4M+15]| ≤ 9;
(b) no two consecutive j ≤ 9 are both in J_T, so T′ owns at least 4
    of the nine values 4M+1 … 4M+9 (hitting set of the path 1–…–9);
(c) all the analogous run-truncated locks (e138 part C: max
    admissible size 5 already for a top run of length 9).

*Status of the finite check as "hand" material.*  Lemma J is a
finite statement verified exhaustively; each minimal forbidden set
is a 16-point UNSAT gadget that a reader can in principle refute by
the Seesaw/zigzag calculus (the units of j seed conflicting phases
of the shared-rung ladders).  Producing the 36 pencil derivations is
bounded, mechanical work; we tag it [MACHINE-CHECKED — pencil
derivations pending] rather than [PROVED].  No step of §5–6 depends
on more than (a)–(c).

### 3.5 The band-edge α-units as glue  [PROVED, descriptive]

The A2 α-units z ≺ y (z in the band top-31, y ∈ E1, attacker
x ∈ U ∩ [2M−30, 2M]) place band-TOP values before band-BOTTOM
values.  They are not ladder material (their gaps M±15 exceed half
the band width, so no third rung exists in P1): their role is
transitive glue — an α-unit z ≺ y plus a chain of §3.3 in-band facts
from y back up to z closes a cycle.  The same holds for the crown
units of Th0 (A1) and the boundary-rung units of Th2 (A5), which
connect F to G within P2.  These three finite families are the
candidate cycle-closers of the assembly, playing the role that A2/A3
(the C3 axioms) played in notes/33's 3-cycles.

[MACHINE-CHECK for §3: experiments/e138_seam2_transfer.py — part A
(ladder side conditions, 23 scales), parts B/C (Lemma J and its
run-truncations).  data/e138_transfer.log, data/e138_transfer.json.]

---
