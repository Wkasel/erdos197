# notes/33 — Lemma OG, C3 core: the complete hand proof (TASK P, v2)

Companion to notes/30 (S1–S16), notes/31 (compactness verdict), notes/32
(invariants S1–S4).  Version 1 of this note (see git history) proved
layer 0 by hand and reduced layers 1–2 to closure certificates with two
open uniformization gaps (GAP-1, GAP-2).  **Both gaps are now closed.**
This version contains a complete hand proof of the mod-8 rigidity:

> **Target (C3 core of Conjecture OG).**  For every M ≡ 0 (mod 8),
> M ≥ 16, there is no AP-free linear order of (M, 2M] satisfying the
> three axioms C3 = {A1: t₅≺b₅, A2: t₃≺b₆, A3: t₁₀≺b₃}
> (t_i := 2M−i, b_j := M+j; "AP-free" = no monotone in-block 3-AP).

**Overall status: `complete`.**  Every step of the chain
[C3 core ⟹ Lemma OG on the mod-8 class ⟹ (with paper thm:ogred)
S_A is not 3-permutable ⟹ the canonical dyadic partition fails
Erdős #197] is hand-proved below or cites the paper's unconditional
reduction theorem.  Every lemma schema is machine-verified step-by-step
at 51–100 scales including 512 and 1024 (e113), and independently
cross-validated by the closure engine at 51 + 27 scales including 512
(e113b).  No [GAP] tags remain in the Target chain.

**What changed relative to v1.**  The old layers-1/2 case trees (e111,
2-split closure certificates, non-uniform) are replaced by a new proof
built from two reusable hand lemmas: the **transfer lemma E** (the odd
d=2 ladder locks the C3 pair orientations across the block) and the
**flood lemma P** (an alternating mirror/zigzag induction that
polarizes a whole arithmetic class around a center).  The mod-8 lock
appears exactly once, as a residue condition on the flood centers
m₀ ± 1.  Layer 0 (Lemma L0 of v1) is *no longer needed* for the
Target — it survives as the independent proof of S1's layer-0 row.

---

## 1. Setting and rules

Order ≺ ("u≺v" = u placed before v) on the integer interval (M, 2M].
**AP-free**: for every arithmetic progression a < b < c in (M, 2M]
(a + c = 2b), neither a≺b≺c nor c≺b≺a.  As in notes/30 S1–S2 this is
the **midpoint-extremal rule** — on every AP the midpoint either leads
both endpoints or trails both — and gives four unit rules used with
transitivity throughout (b the midpoint of AP (a, b, c)):

* R1: a≺b ⟹ c≺b   R3: c≺b ⟹ a≺b   (b trails both)
* R2: b≺c ⟹ b≺a   R4: b≺a ⟹ b≺c   (b leads both)

Notation: m₀ := 3M/2 (M even), the arithmetic midpoint of the block:
for every j < M/2, (b_j, m₀, t_j) is an AP, since b_j + t_j = 3M.
A **d-ladder** is a maximal run of values of (M, 2M] in arithmetic
progression with difference d; the d=2 ladders are the parity classes,
the d=4 ladders the four mod-4 classes (we use the two odd ones:
**class A** = values ≡ M+1 (mod 4), **class B** = values ≡ M+3
(mod 4); at M ≡ 0 (mod 4) these are the values ≡ 1 resp. 3 (mod 4)).

## 2. Lemma Z (zigzag) and Lemma D (phase dichotomy)  [PROVED]

**Lemma Z.**  Let w₀, …, w_r be consecutive rungs of a d-ladder.  If
w_e ≺ w_{e'} for some adjacent |e − e'| = 1, then every rung w_i with
i ≡ e (mod 2) *leads* both its neighbors (w_i ≺ w_{i±1}).

*Proof.*  Any three consecutive rungs form an AP with the middle rung
as midpoint, so each rung either leads or trails both neighbors
(R1–R4).  The seed makes w_e a leader; if w_i leads, then from
w_i ≺ w_{i+1}, R1 on (w_i, w_{i+1}, w_{i+2}) gives w_{i+2} ≺ w_{i+1},
so w_{i+2} precedes a neighbor and leads both (R4).  Downward is the
mirror argument.  ∎

**Lemma D (phase dichotomy).**  In any linear order, every d-ladder is
globally in one of its two zigzag phases: either the even-index rungs
all lead, or the odd-index rungs all lead.

*Proof.*  The order orients the adjacent pair (w₀, w₁) one way or the
other; apply Lemma Z to that seed.  ∎

Consequently the **leader set** of a d-ladder is one of the two
half-classes mod 2d, and adjacent rungs strictly alternate
leader/trailer.  A proof may case-split on the phase of any ladder
("phase dichotomy") and detach any conclusion derived in both branches.

**Lemma E (transfer).**  M even, M ≥ 12 (below 12 the four rungs
named here collide, e.g. t₅ = b₃ at M = 8; every use is at M ≥ 12).
On the odd d=2 ladder
w_i = M + 1 + 2i (i = 0 … M/2 − 1) the four odd C3 values sit at
b₃ = w₁, b₅ = w₂, t₅ = w_{M/2−3}, t₃ = w_{M/2−2}.  Lemma Z therefore
locks the orientations of the pairs (b₃, b₅) and (t₅, t₃) together:

* M ≡ 0 (mod 4):  b₅≺b₃ ⟺ t₃≺t₅   (indices 2 and M/2−2 both even);
* M ≡ 2 (mod 4):  b₅≺b₃ ⟺ t₅≺t₃   (indices 2 and M/2−3 both even).

*Proof.*  Each orientation of an adjacent pair seeds Lemma Z; read off
whether the other pair's left member is a leader.  E.g. at
M ≡ 0 (mod 4), b₅≺b₃ (= w₂≺w₁) makes even indices leaders, and
t₃ = w_{M/2−2} with M/2−2 even leads: t₃≺t₅.  Conversely t₃≺t₅ seeds
even-index leaders and w₂ = b₅ leads: b₅≺b₃.  The two orientations of
(b₃,b₅) force opposite orientations of (t₅,t₃), giving the
biconditional; at M ≡ 2 (mod 4) the parity of M/2 shifts the lock by
one rung.  ∎

Lemma E immediately gives the v1 entanglement facts E1/E2 (the layer-1
literals t₃≺t₅ and b₅≺b₃ are equivalent in every model at
M ≡ 0 mod 4) *without any other hypotheses*, and explains the e112
sharpness rows at M ≡ 2 (mod 4) (there JN = {t₅≺t₃, b₃≺b₅} is
self-contradictory by the lock — the "no-split closure" of ledger B).

[MACHINE-CHECK: e113 `check_layer1` final block verifies the Lemma-E
schema (seed b₅≺b₃ ⟹ t₃≺t₅) rung-by-rung at every M ≡ 0 (mod 4) in
12..400 plus 512, 1024.]

## 3. Lemma P (flood)  [PROVED — the master lemma]

Fix g ∈ {2, 4} and a g-class C (a parity class for g = 2; one of the
odd mod-4 classes for g = 4) whose d=g ladder is, by Lemma D, in a
definite zigzag phase with leader set L (one residue class mod 2g
inside C; adjacent rungs alternate leader/trailer).  Let c be a value
(a **center**) with

>  c ≡ (C + g/2)  (mod g)      (center condition)

i.e. the mirror pairs u_e = c − e, v_e = c + e with **e ≡ g/2 (mod g)**
have both members in C, and (u_e, c, v_e) is an AP with midpoint c
whenever both members lie in (M, 2M].  Call e **admissible** when both
c ± e ∈ (M, 2M].

**Lemma P.**  Suppose some admissible e₀ carries a seed relation
between c and a pair member v ∈ {c ± e₀}.  Then:

* (outward)  if c ≺ v, then c ≺ w for **every** w ∈ C with
  2c − w ∈ (M, 2M];
* (inward)   if v ≺ c, then w ≺ c for every such w.

Moreover the conclusion does not depend on which zigzag phase the
C-ladder is in (**phase-blindness**): the induction below succeeds for
either leader set, so combined with Lemma D the flood may be asserted
after a two-branch case split that derives the same conclusion twice.

*Proof.*  First, at each admissible e exactly one of c+e, c−e is a
leader: they differ by 2e ≡ g (mod 2g), so they lie in the two
different half-classes mod 2g of C, and L is one of them — whichever
phase holds.  Second, in a zigzag, a trailer's neighbors are leaders
and lead it (Lemma Z / D).

Seed step: from the relation at v, the mirror rule on the AP
(u_{e₀}, c, v_{e₀}) yields the same-direction relation at the other
pair member (R2/R4 outward, R1/R3 inward).  So both members of pair e₀
are related to c, in the flood direction.

Induction outward-up (pair e → pair e+g, both admissible): let
x ∈ {c±e} be the leader of pair e (exactly one, shown above).  Its
outward ladder-neighbor x' (|x' − c| = e + g, same side) satisfies
x ≺ x' (leaders lead both neighbors), and c ≺ x is known, so c ≺ x';
the mirror rule (R2/R4) on (2c − x', c, x') gives c ≺ 2c − x'.  Both
members of pair e+g are now flooded.

Induction outward-down (pair e → pair e−g): let w ∈ {c±(e−g)} be the
**trailer** of pair e−g (exactly one).  Its outward neighbor
w' (|w' − c| = e, same side) is a leader (adjacent rungs alternate)
and leads it: w' ≺ w; combined with the known c ≺ w' this gives
c ≺ w; the mirror rule floods the other member.

Induction inward-up (pair e → e+g): let x ∈ {c±(e+g)} be the leader
of pair e+g.  It leads its inward neighbor x_in (distance e, same
side): x ≺ x_in, and x_in ≺ c is known, so x ≺ c; mirror (R1/R3)
floods the other member.

Induction inward-down (pair e → e−g): let x ∈ {c±(e−g)} be the leader
of pair e−g.  It leads its outward neighbor (distance e, same side)
x_out: x ≺ x_out ≺ c, so x ≺ c; mirror floods the other member.

The admissible-e range is an interval of the residue class g/2 mod g
(it shrinks as |e| grows), so the two inductions from e₀ cover every
admissible e, i.e. every w ∈ C with mirror 2c − w in the block.  Every
step used only R1–R4 on genuine APs, transitivity, and the zigzag
edges of the given phase; and the choice of side at each step is
forced by the phase but exists in both phases.  ∎

The three instances used below (names as in the scripts):

* **POLAR** (g = 2, center m₀, class = odds; M ≡ 0 mod 4 so m₀ is
  even).  Seed: the split literal t₅ vs m₀ (mirror b₅ = 2m₀ − t₅ is in
  the block).  Outward: m₀ ≺ t₅ floods m₀ ≺ every odd value.  Inward:
  t₅ ≺ m₀ floods every odd value ≺ m₀.  (Mirror of any odd b_l is t_l:
  the flood covers *all* odds.)  The odd ladder's phase is *pinned* by
  the layer's seed literal (no dichotomy needed).
* **P2-floods at odd centers** (g = 2, center c odd, class = evens).
  Seed: c vs m₀ at e₀ = |c − m₀| (from POLAR), mirror 2c − m₀ in the
  block whenever c is in the middle half.  Floods c against every even
  w with 2c − w in the block.  The even ladder's phase is unknown:
  phase dichotomy, both branches.
* **G4-floods** (g = 4, center c ≡ (class + 2) (mod 4), class A or B).
  Seeds at e = 2: the ODD2 zigzag edges between c and c ± 2 (the odd
  d=2 ladder's phase is pinned, and c ± 2 are exactly the odd
  neighbors of c at distance 2).  Floods c against every class value
  with mirror in the block.  The d=4 ladder's phase is unknown: phase
  dichotomy, both branches.

The **mod-8 lock** of the whole problem sits in the center condition
of the G4-floods: at M ≡ 0 (mod 8) the two odd values adjacent to m₀,
namely m₀ − 1 and m₀ + 1, satisfy m₀−1 ≡ 3 and m₀+1 ≡ 1 (mod 4) — so
m₀−1 is a G4-center for class A and m₀+1 for class B.  At
M ≡ 4 (mod 8) both congruences fail (and the ODD2 leader statuses at
m₀ ± 1 invert), and the flip proof below correctly evaporates.
[MACHINE-CHECK: e113 `sharpness_4mod8`, every M ≡ 4 (mod 8) in
28..300.]

## 4. Layer 1 by hand  [PROVED]

**Theorem L1.**  Let M ≡ 0 (mod 4), M ≥ 12, and let ≺ be an AP-free
order of (M, 2M] satisfying A2: t₃≺b₆ and A3: t₁₀≺b₃.  Then b₅≺b₃
and t₃≺t₅.

(This is rows 0–1 of the S1 grading in their strongest form: no other
hypotheses — not even layer 0 — are needed.  Lemma L0 of v1 remains
the independent hand proof of the layer-0 row t₃≺b₃, t₁₀≺b₆ for all
even M ≥ 74.)

*Proof.*  It suffices to refute S: b₃≺b₅ — given b₅≺b₃, Lemma E
supplies t₃≺t₅.  So assume A2, A3, S.  By Lemma Z (seed S), the odd
ladder's leaders are the offsets ≡ 3 (mod 4).  Define

* c\* := m₀+1 if M ≡ 0 (mod 8), else m₀−1  — then c\* ≡ 1 (mod 4),
  so c\* is a G4-center for class B, and its odd neighbors c\*±2
  (≡ 3 mod 4) are ODD2 **leaders**;
* c\*\* := m₀−1 if M ≡ 0 (mod 8), else m₀+1  — then c\*\* ≡ 3 (mod 4),
  a G4-center for class A, and itself an ODD2 **leader**.

Split on the pair (m₀, t₅) — a genuine comparison in a linear order.

**Case I: t₅ ≺ m₀.**  POLAR-inward: every odd value ≺ m₀.  Then:

1. *b₃ ≺ c\**  by the G4-inward flood at c\* over class B: seeds
   c\*±2 ≺ c\* (ODD2 edges — the leaders c\*±2 lead their trailer
   neighbor c\*); b₃ ∈ class B with mirror 2c\* − b₃ ∈ {t₁, t₅} in the
   block; pair distance c\* − b₃ ∈ {M/2−2, M/2−4} ≡ 2 (mod 4) by the
   choice of c\* per residue of M mod 8.  Both d=4 phases.
2. *c\* ≺ t₁₀*  by the P2-outward flood at c\* over the evens: seed
   c\* ≺ m₀ (POLAR, e₀ = 1); t₁₀ is even with mirror 2c\* − t₁₀
   (= M+8 or M+12) in the block.  Both even phases.
3. A3: t₁₀ ≺ b₃.

1–3 give the 3-cycle b₃ ≺ c\* ≺ t₁₀ ≺ b₃.  ⊥

**Case II: m₀ ≺ t₅.**  POLAR-outward: m₀ ≺ every odd value.  Then:

1. *c\*\* ≺ t₃*  by the G4-outward flood at c\*\* over class A: seeds
   c\*\* ≺ c\*\*±2 (c\*\* is an ODD2 leader); t₃ = 2M−3 ∈ class A
   (2M−3 ≡ M+1 mod 4) with mirror 2c\*\* − t₃ ∈ {b₁, b₅}; pair
   distance ≡ 2 (mod 4) by the choice of c\*\*.  Both phases.
2. *b₆ ≺ c\*\**  by the P2-inward flood at c\*\* over the evens: seed
   m₀ ≺ c\*\* (POLAR, e₀ = 1); b₆ even with mirror 2c\*\* − b₆
   (= 2M−8 or 2M−4) in the block.  Both phases.
3. A2: t₃ ≺ b₆.

1–3 give the 3-cycle c\*\* ≺ t₃ ≺ b₆ ≺ c\*\*.  ⊥

Both cases are contradictory, so S is impossible: b₅≺b₃, and Lemma E
gives t₃≺t₅.  ∎

Remarks.  (a) Case I uses only A3, Case II only A2 — the two C3
"guards" are consumed on opposite sides of the polarization split.
(b) The split (m₀, t₅) is a **cross-parity (interleave) comparison** —
exactly the information that S2 (notes/32) proved every
parity-descent proof must transport.  (c) The boundary arithmetic
(mirrors in the block, seed admissibility) holds down to M = 12.

[MACHINE-CHECK: e113 `check_layer1` — every lemma application verified
step-by-step (every AP's membership and arithmetic, every rule
pattern, every leader/trailer claim, both branches of every phase
dichotomy) at every M ≡ 0 (mod 4) in 12..400 plus 512, 1024 (100
scales).  Cross-validation: e113b — the closure engine independently
refutes all 8 (split × phase-axiom) branches at every M ≡ 0 (mod 4)
in 12..200 plus 256, 400, 512.  Consistency: the forced literals match
the e101 S1 sweep at every common scale.]

## 5. The flip by hand  [PROVED]

**Theorem FLIP.**  Let M ≡ 0 (mod 8), M ≥ 16, and let ≺ be an AP-free
order of (M, 2M] satisfying A2, A3 and b₅≺b₃.  Then t₅≺b₅ is
impossible: b₅ ≺ t₅ (= ¬A1) is forced.

*Proof.*  Assume A1: t₅≺b₅ as well, for contradiction.  By Lemma Z
(seed b₅≺b₃) the odd ladder's leaders are the offsets ≡ 1 (mod 4).
Since M ≡ 0 (mod 8):  m₀−1 ≡ 3 (mod 4) is a G4-center for class A
whose odd neighbors m₀+1, m₀−3 (offsets ≡ 1 mod 4) are ODD2 leaders;
m₀+1 ≡ 1 (mod 4) is a G4-center for class B and itself an ODD2
leader.  Split on (m₀, t₅).

**Case I: t₅ ≺ m₀.**  POLAR-inward: every odd ≺ m₀.  Then:

1. *m₀−1 ≺ t₁₀*  [P2-outward flood at m₀−1 over evens; seed
   m₀−1 ≺ m₀ (POLAR, e₀ = 1); mirror of t₁₀ is M+8; both phases].
2. m₀−1 ≺ b₃  [1 + A3].
3. m₀−1 ≺ t₅  [mirror rule R4 on the AP (b₃, m₀−1, t₅):
   b₃ + t₅ = 3M−2 = 2(m₀−1)].
4. m₀−1 ≺ b₅  [3 + A1].
5. *b₅ ≺ m₀−1*  [G4-inward flood at m₀−1 over class A; seeds
   m₀+1 ≺ m₀−1 and m₀−3 ≺ m₀−1 (ODD2 leader edges); b₅ ∈ class A at
   pair distance M/2−6 ≡ 2 (mod 4) with mirror t₇ in the block; both
   phases].

4 and 5 are a 2-cycle.  ⊥

**Case II: m₀ ≺ t₅.**  POLAR-outward: m₀ ≺ every odd.  Then:

1. *b₆ ≺ m₀+1*  [P2-inward flood at m₀+1 over evens; seed
   m₀ ≺ m₀+1 (POLAR, e₀ = 1); mirror of b₆ is 2M−4; both phases].
2. t₃ ≺ m₀+1  [A2 + 1].
3. b₅ ≺ m₀+1  [mirror rule R3 on the AP (b₅, m₀+1, t₃):
   b₅ + t₃ = 3M+2 = 2(m₀+1)].
4. t₅ ≺ m₀+1  [A1 + 3].
5. *m₀+1 ≺ t₅*  [G4-outward flood at m₀+1 over class B; seeds
   m₀+1 ≺ m₀+3 and m₀+1 ≺ m₀−1 (m₀+1 is an ODD2 leader);
   t₅ = 2M−5 ∈ class B at pair distance M/2−6 ≡ 2 (mod 4)
   with mirror b₇; both phases].

4 and 5 are a 2-cycle.  ⊥  ∎

Remarks.  (a) Again Case I consumes A3 and Case II consumes A2; A1 is
consumed symmetrically in both (step 4).  (b) The proof visibly fails
at M ≡ 4 (mod 8) in *both* cases: the centers m₀∓1 land in the wrong
mod-4 classes for their G4-floods and the ODD2 leader statuses at
m₀±1 invert, so neither seed set exists — matching the machine fact
that AP+C3 is satisfiable there (e104).  (c) Layer 0 is not used.

[MACHINE-CHECK: e113 `check_flip`, every M ≡ 0 (mod 8) in 16..400
plus 512, 1024 (51 scales), same strictness as layer 1;
cross-validation e113b (closure engine, 4 branches) at every
M ≡ 0 (mod 8) in 16..200 plus 256, 400, 512.]

## 6. Assembly

**Theorem (C3 core).**  For every M ≡ 0 (mod 8) with M ≥ 16, no
AP-free order of (M, 2M] satisfies C3 = {A1, A2, A3}.

*Proof.*  A2 + A3 force b₅≺b₃ (Theorem L1; M ≡ 0 mod 8 ⊆ 0 mod 4).
Then A1 contradicts Theorem FLIP.  ∎

(Hand bound: the schemas verify from M = 16 up; M = 16 is also the
smallest scale at which the order gadget is well-formed, notes/30 §0.
The machine base ledger — AP+C3 UNSAT at every M ≡ 0 (mod 8) in
16..256 and at 512, e104 part 3 — is now corroboration, not a
dependency.  e89 and e96 P5 verify the full 15-attack gadget OG(M)
UNSAT, a strictly weaker statement than AP+C3 UNSAT; they corroborate
the corollaries below, not the C3 core itself.)

**Corollary (Lemma OG on the mod-8 class).**  The order gadget OG(M)
(paper def:og) contains among its attack units the three C3 axioms
(A1 = 15-attack j=5, A2 = 15-attack j=6, A3 = 16-attack j=3), and its
constraint (i) is AP-freeness.  Hence OG(M) is infeasible for every
M ≡ 0 (mod 8), M ≥ 16.

**Corollary (the dyadic partition).**  Every scale of the dyadic
family M = 2^{2t−1} (t ≥ 4, the family used by thm:ogred) is
≡ 0 (mod 8) and ≥ 128.  By the paper's
unconditional reduction (thm:ogred, audited by e96), infeasibility of
OG(2^{2t−1}) for infinitely many t implies that S_A admits no
3-AP-free permutation.  **Hence S_A is not 3-permutable and the
canonical dyadic partition does not resolve Erdős #197.**

**Corollary (S1 grading, layers 0–2, hand status).**  Row 0 of S1:
Lemma L0 (v1 §4 below, M even ≥ 74 by hand + machine base 16..72).
Rows 1–2: Theorems L1 and FLIP above (M ≥ 12 resp. 16 by hand).  The
sharpness half of S1 (nothing forced at odd M; layer-2 free at
M ≡ 4 mod 8; layer-1 free at M ≡ 2 mod 4) remains machine-verified
(e101) with the structural explanations: seam-CRT parity (L0), the
Lemma-E lock shift (layer 1), the G4 center-class condition (flip).

## 7. Why this is the S2-predicted shape

Notes/32 S2 proved that no unit-projection (parity-descent) proof of
the flip exists: cross-parity interleave information must be
transported.  The proof above transports exactly two interleave items:
the split (m₀, t₅) — one even-vs-odd comparison — and the P2-floods,
whose mirror APs (2c−w, c, w) have an odd center and even endpoints.
The G4-floods are within-parity and carry the tower/halving content:
under the halving map h₊ the class-A/B d=4 ladders descend to the odd
and even d=2 ladders of the half block (m, 2m], and the (b₁,b₅)-style
phase dichotomies are the half-scale layer-1 orientations.  The
"three halvings" of the mod-8 flip are visible as: ODD2 phase (one),
G4 class phase (two), and the center-parity of m₀±1 (three).  This
also matches S3 (coupling depth ≤ 3: the proof's APs have
ν₂(d) ∈ {0, 1, 2} — mirror APs with d odd, POLAR/P2 hops d = 2,
G4 hops d = 4) and S4 (no bounded certificate: the floods' supports
are Θ(M) many triples — ladder length — while the *schema* is O(1)).

## 8. Machine verification (all committed)

* **e113_c3_hand_proof.py** — the strict schema checker for Sections
  2–5: executes every lemma instance rung-by-rung/pair-by-pair
  (assertions on every AP's membership and arithmetic, every R-rule
  pattern, every leader/trailer/residue claim, every mirror bound,
  both branches of every phase dichotomy), then the case chains and
  final cycles.  Verified: layer 1 at every M ≡ 0 (mod 4) in 12..400
  + {512, 1024}; flip at every M ≡ 0 (mod 8) in 16..400 + {512,
  1024}; sharpness (schema inapplicability) at every M ≡ 4 (mod 8) in
  28..300.  data/e113_hand_proof.json.
* **e113b_closure_crossval.py** — independent cross-validation: the
  e109 closure engine (plain R1–R4 + transitivity fixpoint, no
  knowledge of the schemas) refutes every branch of both case trees
  (split × one phase axiom per relevant ladder) at every M ≡ 0 (mod
  4) in 12..200 + {256, 400, 512} (layer 1, 8 branches) and every
  M ≡ 0 (mod 8) in 16..200 + {256, 400, 512} (flip, 4 branches).
  data/e113b_crossval.json.
* Prior ledgers, now corroboration: e104 part 3 (AP+C3 UNSAT at
  M ≡ 0 mod 8 in 16..256, SAT at 4 mod 8 in 20..100), e112 (the v1
  closure trees), e101 (the S1 forced/free sweep, every even M in
  40..128 + odd spot checks), e100 (the original flip), e89/e96
  (OG UNSAT 16..200, 512).
* Discovery-phase scripts kept for the record: e105–e112 (v1), and
  the e109 tracer that this task used to mine the flood mechanisms.

## 9. What remains open (outside the Target)

* The full Lemma OG (all M ≥ 16, every residue class) — notes/30
  G1/G2/G6.  Not needed for the dyadic partition answer.  The natural
  attack now: per-residue analogues of Theorems L1/FLIP for the C4
  core (M ≡ 0 mod 4) and the residue cores of notes/30 S8–S9, using
  the same flood toolkit; the crossed-pair residue table (notes/32
  bonus law) is the likely source of the per-class seeds.
* S3's k* = 3 ⟺ ν₂(M) ≥ 4 conjecture and the ν₂(M) = 3 anomaly
  (k* ∈ {4, 5}) — the flood proof uses coupling depth ≤ 3 uniformly,
  so the anomaly is a property of *closure* refutations, not of the
  theorem; understanding it is no longer on the critical path.

---

# Appendix (from v1): Lemma L0 and the halving bookkeeping

The following sections are retained verbatim from v1 — they prove S1's
layer-0 row by an independent mechanism (ladder–seam–gadget with a CRT
seam) and record the halving bookkeeping used by the tower program.

## A.1 Halving: exact bookkeeping [PROVED; MACHINE-BASE: e104 part 2, M = 40, 44, 46, 48, 56, 64]

Let M be even, m = M/2.

**Lemma H.**  The maps h_E(v) = v/2 on the even values of (M, 2M] and
h_O(v) = (v+1)/2 on the odd values are bijections onto (m, 2m], and
both *preserve and reflect* 3-APs: a value triple in one parity class
is an AP iff its image is an AP of (m, 2m].

*Proof.*  Evens of (M, 2M] are M+2, M+4, …, 2M; halving gives
m+1, …, 2m exactly.  Odds are M+1, …, 2M−1; (v+1)/2 gives m+1, …, 2m
exactly.  Both maps are affine injective, and an affine injection
preserves and reflects x + z = 2y.  ∎

Descended images of the six C3 values (M even, offsets at half scale):
t₃, t₅, b₃, b₅ odd ↦ t₁′, t₂′, b₂′, b₃′;  t₁₀, b₆ even ↦ t₅′, b₃′.
The kill list of notes/32 (K2, K2″) shows no unit-projection kernel
exists at any depth; the v2 proof above respects this by transporting
interleave data (Section 7).

## A.2 Lemma L0 (layer 0 by hand)  [PROVED for even M ≥ 74]

**Lemma L0.**  Let M be even, M ≥ 74, and let ≺ be an AP-free order of
(M, 2M] satisfying A2: t₃≺b₆ and A3: t₁₀≺b₃.  Then t₃≺b₃ (L0a) and
t₁₀≺b₆ (L0b).

(For even M with 16 ≤ M ≤ 72 the forcings are [MACHINE-BASE: e101
Part A]; layer 0 is not needed by the v2 Target chain.)

### Proof of L0a

Assume b₃≺t₃ and derive a contradiction.

**Step 1 (seeds).**  A3 and b₃≺t₃ give t₁₀≺t₃ (transitivity); b₃≺t₃
and A2 give b₃≺b₆.

**Step 2 (bottom ladder B).**  Apply Lemma Z to the difference-3 AP
w_i = b_{3+3i}, seeded by w₀ = b₃ ≺ w₁ = b₆.  Leaders are the even
indices, i.e. offsets ≡ 3 (mod 6):

> (B)  b_l ≺ b_{l−3} and b_l ≺ b_{l+3} for every l ≡ 3 (mod 6)
> (existing neighbors; plus the seed b₃≺b₆).

**Step 3 (top ladder T).**  Apply Lemma Z to the difference-7 AP
w_i = t_{3+7i}, seeded by w₁ = t₁₀ ≺ w₀ = t₃.  Leaders are the odd
indices, i.e. top offsets ≡ 10 (mod 14):

> (T)  t_i ≺ t_{i−7} and t_i ≺ t_{i+7} for every i ≡ 10 (mod 14).

In bottom coordinates (b_l = t_{M−l}): b_l ≺ b_{l±7} for every
l ≡ M−10 (mod 14) with l ≥ 8.

**Step 4 (seam).**  Choose an offset p with

> p ≡ 0 (mod 6),  p ≡ M−10 (mod 14),  8 ≤ p ≤ M−24.

Both congruences are even (here M even is used — the *only* place), so
they are compatible mod gcd(6,14) = 2 and have a solution mod 42; the
window [8, M−24] has length M−31 ≥ 42 for M ≥ 73, so p exists for
every even M ≥ 74.  By construction p+3 ≡ 3 (mod 6) is a B-leader and
p is a T-leader; all offsets used below lie in [p−7, p+23] ⊆ [1, M−1],
and the ladder inductions reach them.

**Step 5 (tail gadget: sixteen forced literals).**

| # | literal | justification |
|---|---------|---------------|
| 1 | b_{p+3} ≺ b_{p+7} | trans: b_{p+3} ≺ b_p (B), b_p ≺ b_{p+7} (T) |
| 2 | b_{p+11} ≺ b_{p+7} | Z on the d=4 AP (b_{p+3}, b_{p+7}, …, b_{p+23}) seeded by 1: leaders b_{p+3}, b_{p+11}, b_{p+19} |
| 3 | b_{p+11} ≺ b_{p+15} | same Z |
| 4 | b_{p+19} ≺ b_{p+15} | same Z |
| 5 | b_{p+19} ≺ b_{p+23} | same Z |
| 6 | b_{p+15} ≺ b_{p+12} | (B) at l = p+15 |
| 7 | b_{p+11} ≺ b_{p+12} | trans: 3, 6 |
| 8 | b_{p+13} ≺ b_{p+12} | Z on the d=1 AP (b_{p+11}, …, b_{p+14}) seeded by 7: leaders b_{p+11}, b_{p+13} |
| 9 | b_{p+13} ≺ b_{p+14} | same Z |
| 10 | b_{p+13} ≺ b_{p+7} | trans: 9, then (T) at l = p+14: b_{p+14} ≺ b_{p+7} |
| 11 | b_{p+3} ≺ b_{p−7} | trans: b_{p+3} ≺ b_p (B), b_p ≺ b_{p−7} (T) |
| 12 | b_{p+3} ≺ b_{p+13} | Z on the d=10 AP (b_{p−7}, b_{p+3}, b_{p+13}, b_{p+23}) seeded by 11: leaders b_{p+3}, b_{p+23} |
| 13 | b_{p+23} ≺ b_{p+13} | same Z |
| 14 | b_{p+19} ≺ b_{p+13} | trans: 5, 13 |
| 15 | b_{p+7} ≺ b_{p+13} | R3 on the d=6 AP (b_{p+7}, b_{p+13}, b_{p+19}) from 14 |
| 16 | ⊥ | 10 and 15: b_{p+13} ≺ b_{p+7} ≺ b_{p+13} |

∎ (L0a)

### Proof of L0b

Assume b₆≺t₁₀.  Seeds: t₃≺t₁₀ (A2 + assumption), b₆≺b₃ (assumption +
A3).  Ladder B (same d=3 AP, seeded by the *fall* b₆≺b₃): leaders at
offsets ≡ 0 (mod 6).  Ladder T (same d=7 AP, seeded by the *rise*
t₃≺t₁₀): leaders at top offsets ≡ 3 (mod 14).  Seam: p ≡ 3 (mod 6),
p ≡ M−3 (mod 14) (both odd — again solvable exactly because M is
even), 8 ≤ p ≤ M−24.  The tail gadget of A.2 applies verbatim.  ∎

[MACHINE-CHECK: e110_l0_uniform.py — the complete schema verified at
every even M in 74..300 and at M = 512, 1024, 4096 (117 scales), with
the odd-M seam obstruction confirmed.  data/e110_l0_uniform.json.]

* The refutation is *not* fixed-support: the ladders lengthen with M
  (≈ M/3 and M/7 rungs) — the linear MUS growth of S4 is growth by
  *ladder length*, fully compatible with a uniform hand proof.  The
  same is true of the v2 floods (Θ(M) rungs, O(1) schema).

## A.3 The v1 closure trees (historical)

v1 reduced layers 1–2 to fixed 2-split closure trees (e111/e112:
splits (m₀,t₅)+(b₁,b₅) for layer 1, (b₁,b₅)+(t₂,t₄) for the flip),
verified at 55+1 resp. 28+1 scales, with the uniformization left open
as GAP-1/GAP-2.  Those ledgers (data/e112_layer_trees.json) remain
valid machine facts and are now subsumed by Sections 4–5.  The
explanation of the old splits: (b₁,b₅) pins the class-A d=4 phase and
(t₂,t₄) the even d=2 phase — information the v2 proof obtains
phase-blindly through Lemma D, at the cost of the (m₀,t₅) interleave
split, which closure certificates cannot exploit because phase
dichotomies are not unit propagations.

## 10. Verification pointers (all committed)

* e113_c3_hand_proof.py / data/e113_hand_proof.json — the v2 schema
  checker (Sections 2–5).
* e113b_closure_crossval.py / data/e113b_crossval.json — independent
  closure cross-validation of every case-tree branch.
* e110_l0_uniform.py / data/e110_l0_uniform.json — Lemma L0 schema
  (117 scales).
* e109_l0_trace.py — provenance-tracking closure engine (discovery
  tool for both v1 and v2; prints pencil-checkable derivations).
* e112_layer_trees.py, e111_l1_splits.py, e105–e108 — v1 exploration
  and ledgers (historical).
* e104_proof_steps.py — Lemma H check; the AP+C3 base ledger.
* Prior bases: e101 (S1 sweep), e100 (flip discovery), e102 (S2
  kills), e103/e103b (coupling depth), e89/e96 (OG UNSAT incl. 512).
