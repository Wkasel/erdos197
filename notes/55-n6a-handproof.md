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

## 4. Floods inside P2: centre 6M and the core centre 5M+8
[PROVED as conditional lemmas; mechanics MACHINE-CHECKED]

### 4.1 Lemma P′ (interval flood)  [PROVED]

Let I be an integer interval, T a team, c ∈ T ∩ I a centre, g ∈
{2, 4}, and C the class {v : v ≡ c + g/2 (mod g)}.  Assume the
*mono hypothesis*: every C-value of I within the flood's reach
below (call the reach set W = {w ∈ C ∩ I : 2c − w ∈ I}, plus one
g-step beyond on each side where it exists inside I) belongs to T,
and the d = g ladder on those rungs is in a definite zigzag phase
(Lemma D′ branch).  If a seed relation between c and one member of a
mirror pair holds, then

  (outward: c ≺ v₀)  c ≺ w for every w ∈ W;
  (inward:  v₀ ≺ c)  w ≺ c for every w ∈ W;

and the conclusion holds in BOTH zigzag phases (phase-blindness).

*Proof.*  Verbatim notes/33 §3 (Lemma P): the block (M, 2M] enters
that proof only through "mirror inside the block" and "rung inside
the block" checks, which become "inside I"; every induction step
(seed mirroring, outward-up, outward-down, inward-up, inward-down)
uses only R1–R4 on APs of I, transitivity, and zigzag edges of the
given phase, all of which are available for in-team APs by §1.1 and
Z′/D′.  The admissible-e range is the interval of the class
{g/2 mod g} cut by "c ± e ∈ I"; both inductions from e₀ cover it.  ∎

### 4.2 The instances  [MACHINE-CHECKED at 48/64/80, 4 branches each]

With I = P2-core = [4M+1, 6M+15], mirror widths from A8:

| name    | centre | g | class          | window            | residue need |
|---------|--------|---|----------------|-------------------|--------------|
| F6-g2   | 6M     | 2 | odds           | e ≤ 15 (CLIPPED)  | —            |
| F6-g4   | 6M     | 4 | ≡ 6M+2 (mod 4) | e ∈ {2,6,10,14}   | M even       |
| MIDg2−  | 5M+7   | 2 | evens          | e ≤ M+5 (FULL)    | M even       |
| MIDg2+  | 5M+9   | 2 | evens          | e ≤ M+5 (FULL)    | M even       |
| MIDg4−  | 5M+7   | 4 | ≡ 1 (mod 4)    | e ≤ M+6 (FULL)    | M ≡ 0 (4)    |
| MIDg4+  | 5M+9   | 4 | ≡ 3 (mod 4)    | e ≤ M+6 (FULL)    | M ≡ 0 (4)    |

The flood at 6M is width-15 CLIPPED — its covered set is exactly
the class values of [6M−15, 6M+15], i.e. F together with its lower
mirror (6M−15, 6M): this is the "width-15 boundary rung" of the
schema.  The wide floods live at P2-core's own arithmetic centre
(4M+1+6M+15)/2 = 5M+8: its odd neighbours 5M+7 ≡ 3, 5M+9 ≡ 1
(mod 4) (at M ≡ 0 mod 4) reproduce the C3 pattern of centres m₀∓1 —
but here only M ≡ 0 (mod 4) is needed, not mod 8, because 5M+8's
residue is pinned by the +8 offset rather than by M alone.  Note
6M ∈ P2-core is itself a value (unlike C3's m₀ which was mid-block):
the seeds of the MID floods can be taken on the interleave pair
(5M+7, 6M) — the mirror of 6M through 5M+7 is 4M+14, through 5M+9
is 4M+18, both in P2-core.

[MACHINE-CHECK: experiments/e139_flood6M.py — the e113 schema engine
generalized to intervals (same audit discipline: every AP, rule
pattern, leader/trailer claim, mirror bound asserted; hypothesis log
must equal the declared fiat set), executing all six instances in
all 4 (phase × direction) branches at M = 48, 64, 80, plus the
residue sweep at every M ≡ 0 (16) in 48..400.  data/e139_flood.log.]

### 4.3 The F ↔ S3 mirror coupling  [PROVED]

Through the near-centre odd centres, the flood band mirrors onto
P2's bottom run:

    2(5M+7) − (6M+j) = 4M + 14 − j     (j = 1..13 ↦ S3-values)
    2(5M+9) − (6M+j) = 4M + 18 − j     (j = 3..15 ↦ S3-values)

So every mirror AP that a MID flood uses to reach an F-value has its
other endpoint in S3 ∪ [4M+17, 4M+18) — the two seam-coupled bands
(F = the seam-1×2 doubling image, S3 = the seam-2 doubling image)
are MIRROR IMAGES of each other through P2-core's centre.  Combined
with the A5 boundary-rung units (F before G) and Lemma J (S3
memberships lock band phases), this is the geometric closure the
schema was fitted to: everything the two seams inject into P2 meets
at the centre 5M+8.

### 4.4 What the floods need (the honest accounting)

Each instance above is CONDITIONAL on its mono hypothesis: Θ(M)
same-team rungs (the MID floods) or 16 same-team rungs around 6M
(the F6 floods).  In the C3 proof the block was unicolored and the
hypotheses were free; here they are the crux.  Two regimes discharge
them naturally:

* LOPSIDED colorings (one team near the (2,2,2) floor): the
  majority team's P2 material is P2 minus O(1) values; all six
  floods survive puncturing if their rungs avoid the minority's
  ≤ |Z′| values — and the MID centres can be MOVED (any centre in
  the midband has width ≥ M−O(1), A8), giving the robustness
  freedom the assembly will use.
* LATTICE colorings (each team a union of residue classes): a team
  owning a full parity class of P2 owns entire d = 2 ladders — the
  mono hypotheses hold verbatim.  §5 reduces this family by halving
  to an UNGUARDED single-team core.

The general interpolation between the regimes is the open part
(§6).

---

## 5. Where (2,2,2) enters: the frontier map and the reduction cores

### 5.1 Lemma W (quantitative straddle pressure)  [PROVED]

For a straddle-free team T and u ∈ U, let
Mid(u, Z) := {(u+z)/2 : z ∈ Z, z ≡ u (mod 2)} ∩ P1.

(a) Mid(u, Z) ∩ Y = ∅ for every u ∈ U; hence Mid(U, Z) ⊆ Y′ ∩ P1
    and the two teams' forbidden-midpoint sets are DISJOINT subsets
    of the band.
(b) HOT ZONE.  For u ∈ H0 := [2M−31, 2M−15] (17 values), the window
    {z : (u+z)/2 ∈ P1} ⊇ P2 entirely; hence u ∈ U ∩ H0 forces
        |Z ∩ (u + 2ℤ)| = |Mid(u, Z)| ≤ |P1| − |Y| = M + 16 − |Y|.
(c) If T owns hot values of both parities, |Z| ≤ 2(M + 16 − |Y|):
    a team cannot be band-heavy and P2-heavy while touching the hot
    zone in both parities — the trade-off curve behind every escape.
(d) The parity hatch: (b) caps only SAME-PARITY material; a team
    with Z entirely opposite in parity to U feels no pressure.  This
    is exactly the machine's lattice dodge, and it is why the
    lattice regime (§5.4) needs its own kill.

*Proof.*  (a) is the definition of straddle-freeness ((u, mid, z)
would be a mono (0,1,2) triple); (b): (u+z)/2 ∈ P1 ⟺ z ∈
[6M−30−u, 8M−u] ⊇ [4M+1, 6M+15] ⟺ u ∈ [2M−31, 2M−15]; (c) sum (b)
over one u of each parity.  ∎

### 5.2 The machine frontier: which bounds are load-bearing
[MACHINE-CHECKED at M = 48]

All on CORE′(48), decomposed encoding (e136), bounds = per-team
per-block lower bounds:

    (1,1,1) SAT     (2,1,1) UNSAT    (2,2,1) UNSAT   (0,2,0) SAT
    (1,1,2) SAT     (1,2,1) UNSAT    (2,1,2) UNSAT   (0,2,1) SAT
                    (1,2,0) UNSAT    (1,2,2) UNSAT   (2,0,0) SAT
                    (2,1,0) UNSAT                    (0,0,2) SAT
                    (2,0,1) SAT                      (2,2,2) UNSAT

((2,1,0) UNSAT and (2,0,1) SAT were PREDICTED by the law below
before the run — the law's first genuine test.  e140c.)

**Frontier law (machine, M = 48).**  An escape exists iff

    min|U| = 0   ∨   min|Y| = 0   ∨   (min|U| = 1 ∧ min|Y| = 1),

where min is over the two teams.  Equivalently: the coloring is dead
as soon as both teams touch P0, both touch the band, and at least
one of the two seams is doubly supplied (min|U| ≥ 2 or min|Y| ≥ 2).
The P2 bound is IRRELEVANT — every UNSAT row above stays UNSAT with
third bound 0, and every SAT row has both teams with ≥ 1 P2 value
anyway.  This corrects the working hypothesis of notes/51 §"bounds":
the (2,2,2) minority supply enters ONLY through B0 and the band.

Two clean sufficient targets for Theorem N6a follow (each implies
the (2,2,2) lock by bound monotonicity):

    T1:  min|U| ≥ 2 ∧ min|Y| ≥ 1  ⟹  infeasible      [= (2,1,0)]
    T2:  min|U| ≥ 1 ∧ min|Y| ≥ 2  ⟹  infeasible      [= (1,2,0)]

**Anatomy of the surviving escapes.**  Every SAT witness realizes
one of two dodges:
  E∅  a P0-empty or band-empty team (the (0,·,·)/(·,0,·) rows);
  E1  the singleton dodge: one team's P0 part is the single value
      {2M}, the other team's band part is the single value {4M}
      (the (1,1,·) rows) — team A = {2M} ∪ (band ∖ {4M}) ∪
      (F ∪ odd-lattice), team B = (P0 ∖ {2M}) ∪ {4M} ∪ (rest of
      P2).  B escapes straddles by ceding ALL of F (= 2·4M −
      [2M−15, 2M−1], A7b) to A; A escapes by parity (its only P0
      value 2M is even, its sub-6M P2 values all odd — Lemma W(d)).

### 5.3 The double-fan core: what the second band value buys
[MACHINE-CHECKED; uniform proof = GAP-FG]

For x ∈ P1 the *fan* of x is the unit family of Th2:
{z ≺ y : y, z = 2y − x ∈ P2-core} (Θ(M) units, A6).  Machine facts
(e140/e140b, M = 48; FG := AP-freeness on [4M+1, 6M+15] + fans):

* ONE fan is satisfiable (X = {4M}: SAT — realized by the E1
  escape, where team B holds one band value and 70 P2 values).
* TWO fans are UNSAT for EVERY tested placement — 13 pairs at
  M = 48 including adjacent, same-parity, band-bottom (129, 130),
  and spread (129, 160), (140, 170) pairs; scale-stable at M = 64
  (top pair AND band-bottom pair UNSAT, single fan still SAT —
  e140c).
* Robustness: the adversarial-subset version (fan units and APs
  guarded by membership; |S| ≥ k) for X = (4M, 4M−1): UNSAT at
  k = 97, SAT at k = 83, so k_crit ∈ [83, 96] of 111 values — a
  double fan survives any ≤ 14 deletions and some escape exists
  with ≤ 28; the machine's escape punctures are mod-2/mod-4 lattice
  patterns in P2's lower middle (bisection stopped inside the
  bracket; exact k_crit not load-bearing).

### 5.3b The double-fan landscape, corrected (e141–e143)

The naive target "any two fans kill" is **FALSE**; the truth has
three regimes, mapped by MUS extraction (e141), a provenance-
tracking R1–R4+transitivity closure engine (e142, e142b), and SAT
tests (e142c–i).  Write the attackers as x₁ = 4M−p, x₂ = 4M−q,
0 ≤ q < p ≤ M+15.

**Lemma FG-high  [PROVED + MACHINE-CHECKED].**  If p ≥ 2q+1 (i.e.
the attacker pair is itself a HIGH pair: 2x₂ − x₁ ≥ 4M+1) and
5p − 6q ≤ 2M+15, the two fans are inconsistent with AP-freeness on
P2-core.  *Proof* (discovered from the e141 MUS, which is the FOUR
values {4M+s, 4M+2p−3q, 4M+3p−4q, 4M+5p−6q}, s := p−2q,
scale-invariant): the fan units

    A(s):  4M+2p−3q ≺ 4M+s        (fan of x₂ at midpoint 4M+s)
    B(s):  4M+3p−4q ≺ 4M+s        (fan of x₁ at midpoint 4M+s)
    B(s′): 4M+5p−6q ≺ 4M+2p−3q    (fan of x₁, s′ := 2p−3q)

with R4 on the in-window APs (s, 2p−3q, 3p−4q) and
(s, 3p−4q, 5p−6q) (offsets from 4M) give

    2p−3q ≺ 3p−4q ≺ 5p−6q ≺ 2p−3q      — a 3-cycle.  ∎

[MACHINE-CHECK: e143 — the e139 ICtx executes the gadget with full
audit at every admissible (q, p) at every M ≡ 0 (16) in 48..400:
149 169 instances.  data/e143_fg_gadget.log.]

**Closure kills (non-resonant pairs)  [MACHINE-CHECKED derivations,
uniform schema pending].**  Plain R1–R4 + transitivity closure from
the fan units alone (NO case splits) refutes 1851 of the 2016
(q, p) pairs at M = 48, and the whole q = 0 line at M = 64, 80, 96
except the resonant escapes below.  EVERY such refutation is a
small pencil certificate: the full M = 48 survey (e142o) gives
derivation-DAG sizes 6..125 facts, median ≈ 14; 418 pairs need
exactly the 6-fact FG-high proof; every DAG ≥ 80 facts is a deep
pair (q ≥ 42).  A second affine gadget family is already
extracted: at q = 0, 5 | p, s := p/5, the units 2s≺s, 4s≺2s
(halving tree of x₂ = 4M) and 7s≺s, 13s≺4s (fan of x₁) close the
3-cycle 4s ≺ 7s ≺ 13s ≺ 4s via R4 on (s, 4s, 7s) and (s, 7s, 13s)
— offsets from 4M (e142n).  GAP-FG-schema = classify these affine
cycle families over (q, p) — mechanical, certificates in hand.
The deep cluster (p, q near M+15) dies too but needs Lemma-D phase
splits on top of closure (8-branch d=1 × d=2 kills the
deep-adjacent pair at M = 64; every SAT-tested deep pair IS
UNSAT).

**The resonant escapes  [machine; FALSIFIES the naive lemma].**
Certain pairs genuinely ESCAPE the pure double fan.  Top-anchored
(q = 0) SAT gaps (each = exactly the closure-stall set at its
scale; everything else on the q = 0 line is UNSAT):

    M = 48: g ∈ {32, 48, 56}      M = 80: g ∈ {64, 80}
    M = 64: g ∈ {32, 48, 64}      M = 96: g ∈ {64, 96}

Verified facts about the escape region: (i) every observed escape
lies BEYOND the FG-high reach (5g > 2M+15 on the q = 0 line — the
gadget provably kills everything within reach); (ii) it is
depth-dependent (at M = 96 the top-anchored gap-32 pair dies while
the deeper (4M−96, 4M−64) escapes inside a SAT triple; at M = 48
the non-anchored (q, p) = (16, 32), (1, 33), (15, 47) escape);
(iii) it is NOT simply "16 | gap" — 56 = 48+8 escapes at M = 48
(and g = M+8 fails at M = 64), an early 16-divisibility reading of
the grid was WRONG; (iv) g = M (attacker at 3M exactly) escapes at
every scale; (v) TRIPLE fans can co-escape at every scale
((192,160,144)@48, (256,224,192)@64, (384,320,288)@96), and triple
escape is not governed by pairwise resonance ((192,176,144)@48 is
UNSAT though all three pairwise gaps are resonant at 48).  No
closed form fits the present 12 data points; mapping R(M) exactly
(a cheap closure scan per scale) is prerequisite work for
GAP-STRUCT.  data/e142*_*.log.

**Consequences for the assembly.**  (a) Fan pressure alone cannot
carry T2 at ANY band-bound level: a team may park 2–3 band values
on a resonant configuration.  Such teams must be killed by the
other constraints (straddle pressure, B0 units, Lemma J, floods) —
the resonant regime joins the structured arm of GAP-STRUCT.  On
all data so far every escape pair has gap ≥ 16 (q = 0 escapes have
gap ≥ M/2): band pairs at distance ≤ 15 ALWAYS died in our tests —
if that survives a full-grid audit per scale, "some team has two
band values within 15" becomes a clean fan-kill hypothesis, and
GAP-STRUCT only owes the spread-out configurations.  (b) The (0,2,0) SAT witness already
showed fans alone do not close T2 even off-resonance (a P0-empty
team escapes on punctured P2): Lemma W's B0-side pressure is
co-load-bearing, matching the frontier law ((0,2,0) SAT vs (1,2,0)
UNSAT).

### 5.4 The lattice regime: halving reduction  [PROVED] and the
halved cores  [MACHINE-CHECKED UNSAT]

**Lemma PAR (parity reduction).**  Let M be even, m = M/2.
Consider the complementary parity colorings: U = odds of P0,
Z = evens of P2 (team T), U′/Z′ their complements, band split by
parity in either alignment.

(i)  Alignment Y = evens: T = (odd, even, even).  Then T's α, crown
     and A5 families are arithmetically EMPTY (their completions
     have the wrong parity), T's β and A6 units ALL fire, and T's
     feasibility is equivalent (via Lemma H of notes/33 A.1, the
     halving bijections) to the consistency of

         H(m):  a single AP-free order of W1 ∪ W2,
                W1 = [3m−7, 4m], W2 = [4m+1, 6m+7],
                with all of W1 before all of W2,

     (the even halved image; T′ = (even, odd, odd) gives the odd
     image with W2 = [4m+1, 6m+8]).
(ii) Alignment Y = odds: T = (odd, odd, even).  Then β/A6/A5 are
     empty, α and crown ALL fire, Th2 is unconstrained, and T is
     equivalent to

         H1(m): a single AP-free order of W0 ∪ W1,
                W0 = [m+1, 2m], W1 = [3m−7, 4m],
                with all of W0 before all of W1

     (and T′ = (even, even, odd) to the even image of the same).

*Proof.*  Parity bookkeeping on each family of §2 (a completion
2b − a has the parity of a; a straddle needs u ≡ z (mod 2), which
the parity coloring makes cross-team, so NO straddle constraints
exist for either team); halving (h_E(v) = v/2, h_O(v) = (v+1)/2)
preserves and reflects APs (notes/33 Lemma H) and maps the
surviving in-team AP system onto exactly the stated two-block
systems; Th0 (alignment i) resp. Th2 (alignment ii) is an
unconstrained AP-free order of an interval image, which exists by
the classical odd-even recursive construction.  ∎

**Machine verdicts.**  H_even(m) and H_odd(m) UNSAT at
m = 16, 24, 32, 40 (0.0–0.2 s each); H1(m) UNSAT at the same four
scales (predicted by the reduction before the run).  Note the
self-similarity: H(m) is CORE′(m) minus its P0 block and flood
band — the halving recursion the tower program (notes/31)
predicted.

### 5.4b THEOREM H: the H(m) cores die by hand  [PROVED]

**Theorem H.**  For every m ≥ 6, H(m) is infeasible — for both
W2 = [4m+1, 6m+7] (even image) and W2 = [4m+1, 6m+8] (odd image).

*Proof.*  By the two-block version of Lemma U, H(m) is feasible
only if its W2 block theory (AP-freeness on W2 + the units
z ≺ y for x ∈ W1, y, z ∈ W2, z = 2y − x) is consistent.  That
theory contains the FG-high gadget of §5.3b for the attacker pair
(x₁, x₂) = (4m−1, 4m) ⊆ W1, i.e. (q, p) = (0, 1), s = 1, s′ = 2:

    units  4m+2 ≺ 4m+1  (x₂),  4m+3 ≺ 4m+1  (x₁),  4m+5 ≺ 4m+2 (x₁)
    R4 on (4m+1, 4m+2, 4m+3):  4m+2 ≺ 4m+3
    R4 on (4m+1, 4m+3, 4m+5):  4m+3 ≺ 4m+5
    with the third unit:  4m+2 ≺ 4m+3 ≺ 4m+5 ≺ 4m+2.  ⊥

All six values 4m−1, …, 4m+5 lie in W1 ∪ W2 for m ≥ 6, and both
W2 variants contain [4m+1, 4m+5].  ∎

[MACHINE-CHECK: the ThW2-only UNSAT verified independently at
m = 16, 24, 32, 40 with ONLY the top-pair fans retained
(data/e142j_corrections.log) — and Theorem H's gadget is the e143
instance (q, p) = (0, 1) of the audited sweep.]

**Corollary PAR-i.**  The alignment-(i) members of the
complementary parity family (T = (odd P0, even band, even P2) and
its mirror) are infeasible for every even M ≥ 12, by Lemma PAR(i)
+ Theorem H at m = M/2.  UNCONDITIONALLY PROVED — no machine tag
needed on this branch any more.

### 5.4c H1(m): doubly dead, one uniformization owed
[MACHINE-CHECKED; GAP-H1]

For H1(m) (alignment ii) BOTH block theories are INDIVIDUALLY
unsatisfiable at m = 16, 24, 32, 40 (e142k):

* ThW0 = AP-freeness on [m+1, 2m] + the 16 halved crown units
  {2m−k ≺ m+j : k ≤ 3, j ≤ 7−2k} — a SCALE-INVARIANT unit family
  of exactly the C3-core species (t_k ≺ b_j units on a block; the
  notes/33 toolkit's home ground).  UNSAT also at m = 8, 10, 12,
  20, 48, 64; SAT at m = 14 (a sharpness point — the kill is
  residue-sensitive off the needed line).  For Lemma PAR we need
  only m = M/2 ≡ 0 (mod 8), where every probe is UNSAT.
* ThW1′ = AP-freeness on [3m−7, 4m] + a scale-invariant 64-unit
  family (window-top values before window-bottom values, the A2
  α-geometry).

Plain closure stalls on both (m ≥ 24): the kills need Lemma-D
phase machinery.  NEGATIVE schema-search results (e144, e144b/c),
recorded so the next session does not repeat them: ThW0 is NOT
refuted branchwise by the C3-L1 profile — O/E/A4/B4 zigzag fiats
(16 branches) fail from m = 32, adding an (m₀, x) interleave split
(x ∈ {t1, b1, t0, b2}; 32 branches) still fails, and pure mod-8
phase fiats (8 ladders, 256 branches) fail; ThW1′ similarly resists
O/E and d=1 phase fiats.  So H1's kill mechanism is deeper than
C3-L1's (candidates: mixed-depth splits, L0-style CRT ladder pairs,
or DRAT-mining the SAT refutation).  GAP-H1 := uniformize EITHER
kill on m ≡ 0 (mod 8); this replaces the former GAP-H, with
Theorem H closing the H(m) half outright.
(data/e142k_h1_blocks.log, data/e142l_h1_closure.log,
data/e142m_thw0_threshold.log, data/e144*.log.)

Mixed band splits inside the parity family fire STRICT SUPERSETS of
one alignment's unit families plus cross-parity in-band APs; they
do not reduce cleanly, but every fired system contains one of the
aligned systems' images.  [Formalizing "mixed ⟹ at least as dead"
is part of GAP-STRUCT below; it is NOT automatic, because the
mixed team's Y is smaller than the aligned team's.]

---

## 6. Assembly attempt and the obstruction map  [PARTIAL]

### 6.1 The skeleton for target T2

Fix a coloring with min|U| ≥ 1, min|Y| ≥ 2 (the T2 hypothesis;
implied by the (2,2,2) bounds).  Both teams are straddle-free
(Lemma U) and each team carries: a restricted double fan on its own
Z (§5.3), Lemma-W windows from each of its P0 values, the Lemma-J /
E2 / C locks at the band top, and (wherever it owns the mono
material) the §4 floods.  Regime split:

* **R1 (fan-complete).**  Some team's Z is rich enough that its two
  fans + AP-freeness restricted to Z are already inconsistent —
  dead by Lemma FG-high (PROVED) when it holds a high band pair
  with room, and by the closure schemas (machine-verified
  derivations, uniform extraction pending) for every non-resonant
  pair; the robustness data (§5.3) covers Z missing up to ~15–28
  values for the top pair.  NOT covered: 16-resonant band
  configurations (§5.3b) — those are rerouted to R2.
* **R2 (lattice-aligned).**  The complementary parity family — dead
  modulo GAP-H (uniform H(m)/H1(m)), by Lemma PAR.  [The mod-4 and
  higher lattice alignments halve once more into quarter-scale
  images; same species.]  NOW ALSO INCLUDES the resonant band
  configurations of §5.3b: teams whose band values sit on a
  fan-resonant pattern escape the fans and must die here.
* **R3 (the interpolation).**  Z and Z′ both fan-escaping (each
  must be lattice-patterned in its own fan geometry — the machine's
  escape punctures are mod-2/mod-4 patterns), yet jointly they
  PARTITION P2-core, and Lemma W forces their band-midpoint shadows
  into disjoint parts of the band.  No proof; see the obstruction
  statement below.

### 6.2 The obstruction, precisely stated

What is missing is a bridge from R3 to R2: a demonstration that two
COMPLEMENTARY fan-escaping sets under straddle pressure must
converge to a lattice alignment (which R2 kills).  Concretely, the
adversary in R3 plays: puncture team T's fan lattice using exactly
the values donated to T′, and vice versa; each puncture obeys the
OTHER team's Lemma-W windows and Lemma-J locks.  The C3 experience
suggests the right tool is a POTENTIAL (a ledger quantity that
every pass-the-parcel step strictly decreases, bottoming out at the
aligned colorings); the notes/54 exposure-cascade candidate is the
natural template, with the cascade now running over fan punctures
instead of seam inversions.  We did NOT find the potential in this
session.  This — not any single order-theoretic step — is the
honest crux left in GAP-N6a:

    GAP-STRUCT: every T2-coloring is in R1 ∪ R2, OR admits a
    strictly-decreasing potential step toward R2.

Everything else in the chain is either proved here or is a bounded
finite/schematic extraction (GAP-FG, GAP-H, GAP-J-pencil below).

### 6.3 Concrete next machine-to-hand steps

1. **GAP-FG (updated after e141–e143; §5.3b)**: FG-high is now
   PROVED (the 4-point gadget); what remains is (i) the uniform
   schema extraction for the closure-refutable non-resonant pairs
   (each instance already has a machine derivation DAG using only
   R1–R4 + transitivity — bounded work, K4-style: notes/49
   §4.2–4.3), and (ii) the deep-pair splits schema.  Species
   identification: a fan is exactly an N2 attack rung, so this is
   notes/48 Result 0's prediction verbatim ("Case-2 crux = the
   Case-1 crux wrapped in one sumset layer") — with the honest
   correction that the pair rung does NOT fire on 16-resonant
   pairs, which belong to the lattice arm.
2. **GAP-H**: hand-prove H(m)/H1(m) with the ported toolkit — a
   single-team two-block core, so Z′/D′/P′ apply UNGUARDED; this is
   the notes/42 chain-rung geometry in its cleanest form.
3. Frontier law at M = 64/80 (cheap decomposed runs) to certify T2
   as scale-stable before investing in GAP-STRUCT.
4. GAP-J-pencil: 36 sixteen-point derivations (mechanical).

---

## 7. Status summary, residue ledger, gap count

### Proved by hand in this note (uniform in M, thresholds noted)

| item | statement | where |
|------|-----------|-------|
| Lemma U | decomposition into 6 block theories + straddle exclusion | §1 |
| A1–A9 | complete attack-geometry catalogue; finite families 64/256/56 | §2 |
| Seesaw, Z′, D′ | order toolkit ported with mono-run caveat | §3.1 |
| Lemma E2, C | seam-2 donation/clash transfer lock | §3.2 |
| §3.3 | unit-seeded phases; parents = topmost ladder pairs | §3.3 |
| Lemma P′ | interval flood; 6 instances incl. clipped 6M flood | §4 |
| F ↔ S3 | mirror coupling through P2-core's centre 5M+8 | §4.3 |
| Lemma W | quantitative straddle pressure; hot zone | §5.1 |
| Lemma PAR | parity family ⟹ halved cores H(m)/H1(m) | §5.4 |
| Lemma FG-high | 4-point double-fan kill for high attacker pairs | §5.3b |
| Theorem H | H(m) infeasible for all m ≥ 6 (via FG-high (0,1)) | §5.4b |
| Cor. PAR-i | parity alignment (i) dead at every even M ≥ 12 | §5.4b |

Residue ledger: everything above needs at most M ≡ 0 (mod 4) (the
G4 centres at 5M+7/5M+9) and M ≥ 48; no mod-8/mod-16 obstruction
appeared anywhere.  The M ≡ 0 (mod 16) restriction in the Theorem
N6a statement is inherited from the tower program's scales, not
from any lemma here; the machine lock includes M = 48 ≡ 0 (mod
16)… all five locked scales are ≡ 0 (mod 16), and nothing in this
note distinguishes them from other M ≡ 0 (mod 4).

### Machine-checked (finite, M-independent)

* Lemma J: the 30-pair + 6-triple conflict system on S3-memberships
  under a mono top run; max admissible 9/15 (e138).

### Machine-checked (per-scale)

* The lock itself: (2,2,2)/(3,3,3) UNSAT at 32/48/64/80/96 (e134/5).
* Encoding equivalence for Lemma U (e136, M=48 both SAT and UNSAT
  sides).  Catalogue exactness (e137, three scales + sweep).
* Flood mechanics, 6 instances × 4 branches × 3 scales (e139).
* The §5.2 frontier map and law (e140/e140b/e140c, M=48).
* H(m)/H1(m) UNSAT at m = 16..40; FG kills and robustness (e140x).
* The fan landscape (e141 MUS; e142/e142b closure grid, 2016 pairs;
  e142c–j resonance maps at 48/64/80/96; e143 gadget audit,
  149 169 instances × 23 scales).
* H1's double death + thresholds (e142k/l/m: both block theories
  UNSAT at 4 scales; closure stalls; ThW0 sharpness at m = 14).

### Open gaps (the honest count: 5)

| gap | statement | species | risk |
|-----|-----------|---------|------|
| GAP-FG-schema | classify the affine cycle certificates over (q, p) (two families already extracted; all DAGs ≤ 125 facts, median 14) | mechanical taxonomy | low |
| GAP-FG-deep | deep-pair (band-bottom) fan schema (needs phase splits) | Lemma-D branch schema | medium-low |
| GAP-H1 | uniformize ONE of H1(m)'s two dead block theories on m ≡ 0 (8) (H(m) itself now PROVED, §5.4b); resists C3-L1-profile branch closure (e144) | deeper than L1-profile; L0/CRT or DRAT-mining | MEDIUM (upgraded after e144) |
| GAP-J-pencil | 36 finite 16-point derivations | mechanical | negligible |
| GAP-STRUCT | R3 → R1∪R2 bridge, now incl. the 16-resonant band configurations (structure theorem / potential) | genuinely open | HIGH — the crux |
| GAP-ASM | assemble T1-or-T2 from the above into Theorem N6a | bookkeeping over the case split | low once STRUCT falls |

Bottom line: the C3-style toolkit ports cleanly and every
mechanism the schema was fitted around (crown, band ladders, seam-2
transfer, 6M flood + width-15 rung, F↔S3 mirror) is now proved or
machine-finite.  The (2,2,2) bounds enter ONLY as: one P0 value per
team (straddle pressure supply, Lemma W) + two band values per team
(double-fan supply) — the P2 bound is dead weight.  The remaining
mathematical content of GAP-N6a is concentrated in GAP-STRUCT: why
complementary fan-escapes cannot coexist without collapsing into a
(dead) structured alignment — where "structured" includes both the
parity/lattice families (killed via halving, §5.4) and the
fan-resonant spread configurations of §5.3b, whose exact law is
still unmapped (the once-suspected clean mod-16 story was
falsified by the g = M+8 escape at M = 48; what survives is that
every escape needs band values ≥ 16 apart and beyond the FG-high
reach).

