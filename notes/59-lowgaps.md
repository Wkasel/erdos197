# 59 — Low-gap closures: FG-schema, J-pencil, FG-deep, ASM′

Night-shift companion to notes/55 (the N6a proof skeleton and its gap
ledger §7) and notes/56 (the GAP-STRUCT bridge and its scoped gaps
§5.2).  Targets, in order: (a) GAP-FG-schema — the uniform schema
behind the double-fan closure certificates; (b) GAP-J-pencil — the 36
finite derivations of Lemma J's minimal forbidden sets; (c) GAP-FG-deep
— assessment and partials; (d) GAP-ASM′ — the composition-soundness
theorem for the notes/56 §4b three-case bridge, with the overlap-width
bookkeeping.  Notes are written incrementally; every section carries
its verification pointer and a status tag [PROVED] / [MACHINE-CHECKED]
/ [GAP].

Experiment-number disambiguation: this shift's scripts are
e152_mc_schema / e152b_residual_dags / e152c_affine_families /
e152d_fanwalk / e153_j_pencil / e154_deep_classify / e154b_deep_splits
— distinct from the CONCURRENT e152_bridge1 (notes/52),
e152_llop_probe and e153_dich_* (notes/57–58) series; always cite by
full filename.

---

## A. GAP-FG-schema: the fan-walk calculus and its affine families

### A.0 Setting and conventions

Work in offsets from 4M: the window O = [1, N], N = 2M+15, so that
P2-core = [4M+1, 6M+15] = 4M + O.  Fix the attacker pair
x₁ = 4M−p, x₂ = 4M−q with 0 ≤ q < p ≤ M+15.  The *double-fan theory*
ThFG(q,p;M) is the S-restricted block-2 theory (notes/56 §0.2) of
S = {x₁, x₂} ∪ P2-core: a linear order of P2-core, AP-freeness
(midpoint leads both or trails both) for every AP inside P2-core, and
the fan units

    (2a+r) ≺ a    for r ∈ {p, q}, a ≥ 1, 2a+r ≤ N       (offsets)

(the (1,2,2)-units of the two attackers; notes/55 A6).  By Lemma DP
(notes/56 §0.2), an inconsistency of ThFG(q,p;M) makes
S = {x₁,x₂} ∪ P2-core a death pattern: no feasible-state team may
contain both attackers and all of P2-core; the guarded/robust versions
follow the same certificates (only the value support matters).

At M = 48 the ground truth (independent engine, e152) is: of the 2016
pairs, 1851 are refuted by R1–R4+transitivity closure, 165 are not —
matching e142o exactly.  [MACHINE-CHECKED, data/e152_mc_schema.log]

### A.1 The closure calculus  [PROVED]

**Lemma CC.**  Let ≺ be any order satisfying ThFG(q,p;M).  Then the
fact set {u ≺ v} is closed under

    T  :  u ≺ v, v ≺ w   ⟹  u ≺ w
    RL :  u ≺ v          ⟹  u ≺ 2u−v      (if 1 ≤ 2u−v ≤ N, ≠ u)
    RT :  u ≺ v          ⟹  2v−u ≺ v      (if 1 ≤ 2v−u ≤ N, ≠ v)

and contains no u ≺ u.  Consequently any derivation of a 2-cycle
u ≺ v, v ≺ u from the fan units under T/RL/RT refutes ThFG(q,p;M).

*Proof.*  T is transitivity.  For RL, (v, u, 2u−v) — sorted — is an
integer AP inside O with midpoint u; u ≺ v says the midpoint leads one
endpoint, so by AP-freeness (R2/R4 of notes/55 §1.1) it leads the
other: u ≺ 2u−v.  For RT, (u, v, 2v−u) is an AP with midpoint v which
trails the endpoint u; by R1/R3 it trails the other: 2v−u ≺ v.
Irreflexivity is antisymmetry of a linear order.  ∎

Every machine "closure kill" (e142/e152) is a finite T/RL/RT
derivation DAG; the uniformization question is which derivations
organize into M-independent schemas.

### A.2 The fan-walk schema FW  [PROVED]

For h ∈ O define the *descent set* D(h) ⊆ O as the least set with

    seed :  h = 2a+r, a ≥ 1, r ∈ {p,q}                  ⟹  a ∈ D(h)
    (i)  :  x ∈ D(h), 2h−x ≤ N, 2h−x = 2y+r, y ≥ 1      ⟹  y ∈ D(h)
    (ii) :  x ∈ D(h), x = 2b+r, b ≥ 1, 2x−b ≤ N         ⟹  2x−b ∈ D(h)
    (iii):  x ∈ D(h), x = 2b+r, b ≥ 1                   ⟹  b ∈ D(h)

(r ranges over {p,q} in each rule; h itself is removed).  Define the
edge set E(q,p;M): h → x for every x ∈ D(h), and h → 2h−x for every
x ∈ D(h) with 1 ≤ 2h−x ≤ N, 2h−x ≠ h.

**Lemma FW.**  (a) For every x ∈ D(h), ThFG ⊢ h ≺ x.  (b) Every edge
h → z of E is a derivable fact h ≺ z.  (c) If E(q,p;M) contains a
directed cycle, ThFG(q,p;M) is inconsistent.

*Proof.*  (a) Induction on generation.  Seed: h ≺ a is a fan unit.
(i): from h ≺ x, RL gives h ≺ 2h−x; the fan unit gives 2h−x ≺ y
(since 2h−x = 2y+r ≤ N); T closes.  (ii): the fan unit gives x ≺ b;
RL on x ≺ b gives x ≺ 2x−b; T with h ≺ x closes.  (iii): fan unit
x ≺ b, T with h ≺ x.  (b) Descent edges are (a); head edges h → 2h−x
are RL applied to h ≺ x.  (c) A directed cycle concatenates by T to
u ≺ u, contradicting Lemma CC.  ∎

The rules never mention M except through the window bound N; D(h) and
E are computable in O(N) resp. O(N²) time per pair.

### A.3 Affine uniformization  [PROVED]

**Theorem AFF.**  Fix a finite FW *shape*: a cyclic sequence of formal
heads h₁, …, h_m, for each head a formal descent word (a sequence of
seed/(i)/(ii)/(iii) applications with formal residue choices
r ∈ {p,q}), head links h_{i+1} = 2h_i − (chosen descent node of h_i),
and a closing descent node of h_m equal to h₁.  Then every node value
is an affine form c₀ + c₁p + c₂q with dyadic rational coefficients in
the head-1 seed parameter and (p,q), and validity of the datum at
scale M is equivalent to: finitely many linear equations (the head
links and the closing), finitely many integrality congruences (from
the /2 in seed/(i)/(iii)), positivity constraints, and window
inequalities ℓ(p, q) ≤ N = 2M+15.  Consequently a shape valid at one
(q, p, M) is valid at every (q′, p′, M′) satisfying the same
congruences and inequalities: every FW shape is an M-uniform schema.

*Proof.*  Each rule application maps affine forms to affine forms
(x ↦ (x−r)/2, x ↦ (2h−x−r)/2, x ↦ 2x−b, h ↦ 2h−x) and contributes
exactly one integrality/positivity/window condition; the cycle
conditions are linear.  Validity is the conjunction, which mentions M
only through N.  ∎

### A.4 The proved families

**Γ₁ (FG-high; notes/55 §5.3b) [PROVED].**  Region p ≥ 2q+1,
5p−6q ≤ N.  As an FW shape: three heads m₁ = 2p−3q, m₂ = 3p−4q,
m₃ = 5p−6q with single-step descents to the common base s = p−2q;
the closing descent of m₃ is its direct p-unit to m₁ — explicitly,
units m₁ = 2s+q ≺ s, m₂ = 2s+p ≺ s, m₃ = 2m₁+p ≺ m₁;
RL on the first two through s gives m₁ ≺ m₂ ≺ m₃; the third closes.

**Γ₂′ (halving-fan family) [PROVED — new; subsumes e142n].**  Let
a ≥ 1 with p = 5a + 6q and 13a + 12q ≤ N.  Then ThFG(q,p;M) is
inconsistent.  *Derivation:* set m₁ = 4a+3q, m₂ = 7a+6q, m₃ = 13a+12q.
Chain: (2a+q) ≺ a and m₁ = 2(2a+q)+q ≺ (2a+q), so m₁ ≺ a by T.
Since m₂ = 2m₁ − a, RL gives m₁ ≺ m₂.  Since m₂ = 2a+p, the p-unit
gives m₂ ≺ a; RL gives m₂ ≺ 2m₂−a = m₃.  Since m₃ = 2m₁+p, the
p-unit gives m₃ ≺ m₁.  Cycle m₁ ≺ m₂ ≺ m₃ ≺ m₁.  ∎
At q = 0 this is exactly the e142n family (p = 5s: units 2s≺s, 4s≺2s,
7s≺s, 13s≺4s).  Machine: closure-dead and MC-witnessed at
(M,q,p) = (48,1,11), (48,2,27), (64,3,43), (80,4,59), (96,5,40)
[MACHINE-CHECKED, e152 log].

**MC(k) towers (single-anchor subfamily) [PROVED].**  Base a, chain
value m₁ ∈ Chain(a) (iterated fan units), tower m_i = 2^{i−1}(m₁−a)+a
with m₁, …, m_{k−1} ∈ Chain(a) and closing unit m_k = 2m₁ + r.  Then
m_i ≺ m_{i+1} by RL from m_i ≺ a, and m_k ≺ m₁ closes.  Validity per
Theorem AFF.  At M = 48 the tower shapes that fire are (k; depths):
(3; 1,1) — Γ₁ — 297 pairs, (3; 2,1) — Γ₂′ — 39, (3; 3,1) 6, (3; 4,1)
1; total MC coverage 343 of the 1851 dead pairs.  [MACHINE-CHECKED]

**Γ₃ (mirror-pair family) [PROVED].**  A *D-unit* D(a; r, r′) is the
derived fact (2a+r) ≺ b, b = (3a+2r−r′)/2, valid when b ≥ 1 is an
integer and 3a+2r ≤ N [unit (2a+r) ≺ a; RL to 3a+2r = 2b+r′; unit to
b; T].  Two D-units (u ≺ v) = D(a; r₁, r₁′) and (u′ ≺ u) =
D(a′; r₂, r₂′) with u′ = 2u−v ≤ N give the 2-cycle {u ≺ u′ (RL),
u′ ≺ u}.  Solving the linear system:

    a  = −2r₁ + 3r₁′ + 2r₂ − 4r₂′,     a′ = (4a + 2r₁ − 2r₂ + r₂′)/3,

with the integrality of a′, of v = (3a+2r₁−r₁′)/2, positivity, and
the two windows 3a+2r₁ ≤ N, 3a′+2r₂ ≤ N.  Of the 16 residue sign
patterns (r₁,r₁′,r₂,r₂′) ∈ {p,q}⁴, six fire at M = 48 (counts:
ppqq 170, pppq 120, qppp 103, qqpq 91, qppq 48, qpqq 40), with base
values a ∈ {p−2q, 2p−3q, 3p−4q, 5p−6q} — the FG-high orbit reflected
once more.  Γ₃ adds 264 pairs beyond MC (union 607).
[MACHINE-CHECKED, e152c]

### A.5 Coverage and the exact residual map at M = 48
[MACHINE-CHECKED]

    ground truth: 1851 closure-dead / 165 not (matches e142o)
    MC towers:            343 covered
    MC ∪ Γ₃:              607
    FW (full walk):      1467
    FW residual:          384

Soundness cross-check at every stage: NONE of the 165 non-closure
pairs admits an MC / Γ₃ / FW certificate (their theories include SAT
instances, so any hit would disprove the schema; 0/165 at all three
levels — the strongest correctness test we have for the calculus).

The FW residual is sharply structured:

* **The deep block q ≥ M−12 (= 36 at M=48):** ALL 279 dead pairs
  with q ≥ 36 are FW-residual (FW covers ZERO there) — attackers in
  the bottom 28 values of the band kill by closure but their
  certificates need the RT-glue fragment (facts seeded on elements
  below the walk heads, cf. the (48,49) DAG in e152b: RT turns a
  head fact 51 ≺ 26 into 1 ≺ 26 and re-enters through the unit
  50 ≺ 1).  This is a THIRD rule family, not reachable by one-sided
  walks.
* **The mid set (105 pairs, q ≤ 35):** concentrated at q ∈ [32,35]
  (68 of 105) — the shoulder of the deep block — plus the line
  p = q+40 (q = 8..15) and scattered near-resonant neighbours.
* Everything else with q ≤ 35 — 1467 of 1572 dead pairs, including
  ALL close pairs (p−q ≤ 15) with q ≤ 35 — is FW-covered.

[MACHINE-CHECK: experiments/e152_mc_schema.py, e152b_residual_dags.py,
e152c_affine_families.py, e152d_fanwalk.py → data/e152_mc_schema.json/
.log, e152c_affine.json/.log, e152d_fanwalk.json/.log.]

### A.6 What this closes and what remains of GAP-FG-schema

Closed: the certificates in hand (FG-high, e142n) are now instances
of ONE proved uniform calculus (Lemma CC + Lemma FW + Theorem AFF),
with two new proved families (Γ₂′ off the q = 0 line; Γ₃'s six
patterns) and machine-verified coverage of 79% of the dead grid at
M = 48, including the assembly-relevant close pairs away from the
deep block.  The honest correction to the notes/55 §7 ledger row
("mechanical taxonomy, low risk"): a FIXED finite list of affine
gadgets does NOT cover the dead grid — coverage requires the walk
calculus (unbounded shape size, but one uniform soundness lemma), and
the deep block q ≥ M−12 needs the RT-glue fragment on top.  Remaining
work, precisely scoped:

    GAP-FG-schema (narrowed): (1) extend FW by the RT-glue rule
    family (facts (2x−h) ≺ x entering other heads' descents) and
    re-measure — expected to absorb the deep block; (2) a
    cross-scale audit of the FW boundary (is the deep-block edge
    q = M−12 scale-stable?).  Species: same walk calculus, one more
    sound rule; risk: low-medium (mechanical but no longer
    "taxonomy-only").

Status: schema layer [PROVED]; coverage map [MACHINE-CHECKED at 48];
cross-scale stability of the boundary [GAP — cheap compute].

---

## B. GAP-J-pencil: the 36 derivations, closed

### B.0 Setting

Offsets from the TOP of the run: k = 0..15, v_k := w_{15−k} (the
value 4M−k).  T(J) = AP-freeness on the 16 consecutive values + the
units v_t ≺ v_{j+2t} (j ∈ J, t ≥ 0, j+2t ≤ 15).  The 16 points are
consecutive integers, so integer APs of [0,15] are exactly the value
APs, and **Lemma CC applies verbatim with window [0, 15]** — the
same T/RL/RT calculus as §A, now with unit family t ↦ j+2t.  A
derivation of a 2-cycle refutes T(J); by Lemma DP the corresponding
J-pattern R ∪ {4M+j : j ∈ J} is a death pattern.

### B.1 The 6-fact schema S6 and its two residue patterns  [PROVED]

Every 6-fact derivation in the catalogue below is an instance of ONE
shape.  **Schema S6.**  Three units A: t_A ≺ a, B: t_B ≺ b,
C: t_C ≺ c (each of the form t ≺ j*+2t, j* ∈ {j, j′}), subject to

    b = 2a − t_A,     t_C = a,     c = 2b − t_B .

Then RT(A): b ≺ a; RT(B): c ≺ b; T(b ≺ a, a ≺ c): b ≺ c — a
2-cycle on (b, c).  Solving the constraints with residues
(j_A, j_B, j_C) ∈ {j, j′}³ forces t_A = 2j_C − 2j_A − j_B, and
exactly TWO residue patterns give t_A ≥ 0:

**Lemma JP (pattern (j, j′, j′) — the doubling pair).**  For
j′ ≥ 2j with 5j′−6j ≤ 15, set t := j′−2j.  Then t_A = t_B = t,
a = j+2t, b = j′+2t = 2a−t, c = j′+2a = 5j′−6j, and S6 refutes
T({j, j′}).  Window: 5j′−6j ≤ 15.  Instances: (1,2), (1,3), (1,4),
(2,4), (2,5), (3,6).  ∎

**Lemma JP′ (pattern (j, j, j′) — the mirror pair).**  For
2j′ ≥ 3j with 9j′−10j ≤ 15, set t_A = 2j′−3j, t_B = 3j′−4j
(= (j+3t_A)/2, automatically an integer since j+3t_A = 6j′−8j is
even), a = 4j′−5j, b = 6j′−7j = 2a−t_A, c = 9j′−10j = 2b−t_B, and
S6 refutes T({j, j′}).  Instances: (2,3), (3,5), (4,6) (and (1,2)
again).  ∎

Note JP's region {j′ ≥ 2j, 5j′−6j ≤ 15} is EXACTLY the FG-high
family Γ₁ (§A.4) read at run scale, with (q, p) = (j, j′) and window
15 — Lemma J's pair conflicts are the same affine species as the
double-fan gadget, confirming once more the notes/48 "one schema
family" reduction; JP′ is its one-step RT-mirror, its window
9j′−10j being the next term of the same doubling-reflection orbit
(both c-values are 2b − t with b one reflection deeper).

### B.2 The complete pencil catalogue  [PROVED — machine-generated,
hand-checkable]

experiments/e153_j_pencil.py runs the provenance-tracked T/RL/RT
closure on each of the 36 minimal forbidden sets of Lemma J
(data/e138_transfer.json) and prints a complete pencil derivation for
each; every step is an application of a Lemma-CC rule, so validity is
by construction (proof by reflection), and each printout is short
enough to re-check by hand.  Results:

* **29/36 die by pure closure**, derivation sizes 6–33 facts:
  all pairs except (7,8), (8,9), (8,11) — sizes: 6 facts × 9 pairs
  (EXACTLY the JP ∪ JP′ instances), 8–16 facts × 13, 20–27 facts
  × 5 — and the triples (1,10,12), (4,13,15) at 33 facts each.
* **7/36 need totality splits** (a case split u ≺ v vs v ≺ u is a
  legitimate pencil step): (7,8) splits on (v₀,v₁); (5,10,12) and
  (7,10,12) split on (v₀,v₂) — both branches then die by closure
  (17–50 facts per branch); (8,9), (9,10,12) double-split on
  (v₀,v₁)×(v₀,v₂); (8,11) on (v₀,v₁)×(v₀,v₆); (10,11,12) on
  (v₀,v₁)×(v₁,v₃) — all four branches die by closure in each case.

Complete derivations: data/e153_j_pencil.log.  This closes
GAP-J-pencil: Lemma J's status upgrades from [MACHINE-CHECKED —
pencil derivations pending] to [PROVED — finite catalogue with
per-item pencil derivations in the sound calculus of Lemma CC].
The load-bearing subsets for the assembly (J({1,2}), J({1,3}),
J({2,4}) — the only three in the essential catalogues E(48)/E(64),
notes/56 §4.2) are all in the 6-fact JP family.

[MACHINE-CHECK: experiments/e153_j_pencil.py →
data/e153_j_pencil.log; split search exhaustive over single and
double totality splits, 7/7 closed, none open.]

---

## C. GAP-FG-deep: the exact map, the certificates, the halving core

### C.1 Complete classification of the closure-alive pairs at M = 48
[MACHINE-CHECKED]

e154 SAT-classifies all 165 closure-alive (q,p) pairs (one
incremental CaDiCaL instance: full order + AP theory on [1,111],
fans as assumptions; 165 sequential solves, 26 s):

    R(48) — genuine escapes (SAT):     90 pairs
    D(48) — deep stalls (UNSAT):       75 pairs

**The resonance law at 48.**  EVERY pair of R(48) has p − q ≡ 0
(mod 8) (gaps realized: 8, 16, 24, 32, 40, 48, 56).  The mod-8
divisibility is NECESSARY for escape (not sufficient — most mod-8
pairs are closure-dead; cf. notes/55's g = M+8 failure at 64, and
72 ≡ 0 mod 8).  This refines and partly CORRECTS notes/55 §5.3b:
"every escape has gap ≥ 16" is FALSE at full depth — gap-8 escapes
exist, and all of them have BOTH attackers in the band edge E1
(q ≥ 48, i.e. x₂ ≤ 3M).

**The deep law at 48.**  D(48) is EXACTLY the set of UNSAT stalls
with both attackers in E1 = [3M−15, 3M] (q ranges over [48, 62]),
with 8 ∤ (p−q) (the mod-8 members of E1×E1 are in R).  The deep
cluster is the E1×E1 corner — the α-unit midpoint zone attacking
itself.

**Assembly consequence (clean close-pair law at 48).**  For band
values at distance ≤ 15: the only distance-≤15 escapes are the
gap-8 pairs inside E1×E1.  Hence: *a team owning two band values at
distance ≤ 15, at least one of them above 3M, has a dead double fan
at M = 48* — the corrected form of the notes/55 §5.3b close-pair
kill hypothesis (previously stated without the E1 exclusion).
[MACHINE-CHECKED at 48; cross-scale verification pending.]

### C.2 Split certificates for D(48)  [MACHINE-CHECKED]

e154b searches branch certificates (each branch dying by T/RL/RT
closure) for all 75 deep pairs:

    L1  (d=1 zigzag phase dichotomy, 2 branches):        7 pairs
    L2  (d=1 × d=2 × d=2′ phase fiats, 8 branches):     35 pairs
    L3  (single adaptive totality split, 2 branches):   13 pairs
    OPEN (none of the above):                           20 pairs

The L3 splits are low-window pairs ((4,12), (3,11), (2,10), (1,9),
(2,6), (1,5) — offset pairs at gap 8 resp. 4 near the bottom).  The
L1/L2 kills are Lemma-D′ species (phase dichotomies + closure), i.e.
the same flood/zigzag machinery already proved in notes/55 §3–4; a
uniform write-up per family is bounded work of the e142b shape.

**The OPEN core.**  All 20 open pairs have EVEN gap ∈ {2, 4, 6} and
q ≥ 52: the parity-locked corner of E1×E1.  Structural explanation
(heuristic, precise statement below): for r = p, q of equal parity,
the fan-unit sub-theory restricted to one parity class HALVES —
e.g. for p, q both even, sources 2a+r are even and the even-class
units with a even map under v ↦ v/2 to the fan units of the pair
(q/2, p/2) on the half window; for p, q both odd, the odd class
maps under v ↦ (v+1)/2 onto the pair ((q−1)/2, (p−1)/2).  The open
core is thus (a guarded superset of) the halving image of the
deep-adjacent family at half scale — the same recursion that
produced H(m)/H1(m) and the mod-4 quartet.  Its uniformization
belongs with GAP-PARM/GAP-H1, not with the affine fan taxonomy.

### C.3 Assessment: what is provable, what remains

* PROVABLE NOW (bounded work, species already proved): uniform
  schemas for the L1/L2 phase-split kills (Lemma D′ + closure —
  notes/55 §3.1/§4 machinery; 42 of 75 pairs) and for the L3
  totality splits (13 pairs, 6 distinct split anchors).
* MACHINE-TRUE, uniformization = GAP-PARM species: the 20-pair
  parity-locked core (even gaps, deepest E1 corner).
* The resonance law (8 | gap necessary) and the E1×E1
  characterization of the deep cluster are exact at 48 and cheap to
  audit at 64/80/96 (the e154 instrument is scale-generic);
  notes/55's escape lists at 64/80/96 (all gaps ≡ 0 mod 8) are
  consistent with the law.

GAP-FG-deep status: mapped exactly at 48; 55/75 with finite branch
certificates [MACHINE-CHECKED, replayable]; risk re-rated
medium-low → medium ONLY for the 20-pair halving core, which merges
into GAP-PARM; the rest is e142b-shaped bounded write-up.

[MACHINE-CHECK: experiments/e154_deep_classify.py,
e154b_deep_splits.py → data/e154_deep_classify.json/.log,
e154b_deep_splits.json/.log.]

---

## D. GAP-ASM′: the composition-soundness theorem for the F/L/P bridge

This section states notes/56 §4b as ONE theorem with explicit
hypotheses and the overlap arithmetic isolated, so that the remaining
content of GAP-ASM′ is a single displayed inequality.

### D.1 The data at scale M

Fix M ≡ 0 (mod 16), M ≥ 48, the core CORE′(M), and:

* **(H-F)** a *fan catalogue* 𝔉(M): a finite set of block-2 death
  patterns (each S ∈ 𝔉(M) has Th₂[S] unsatisfiable, per the
  notes/56 §0.2 definition, with an independent validation).  A
  coloring χ is *fan-clean* if no team of χ contains any S ∈ 𝔉(M).
* **(H-D)** DICH(M) at threshold K*(M): the instance [coloring vars;
  straddle-freeness both teams; (2,2,2) bounds; fan-cleanness w.r.t.
  the SAME 𝔉(M); min|Y| ≥ K*(M); Φ ≥ 1] is UNSAT, where Φ is the
  same-parity P0×P2 exposure mass (notes/56 §3.1).
* **(H-L)** L-LOP(M) at cap C(M): the instance [coloring vars;
  straddle-freeness; bounds; fan-cleanness w.r.t. 𝔉(M);
  |Y_A| ≤ C(M) − 1; Th1(B) as a guarded order theory] is UNSAT.
* **(H-P)** P-ARM(M): the instance [P0/P2 pinned to the Lemma-PH
  alignment (U_A = odds of P0, U_B = evens, Z_A = evens of P2,
  Z_B = odds); band coloring free with ≥ 2 per team; the six guarded
  block theories jointly] is UNSAT.

All four are per-scale machine items; (H-D), (H-L), (H-P) are single
UNSAT verdicts, (H-F) is a list of small validated certificates.

### D.2 The theorem

**Theorem ASM′(M).**  Assume (H-F), (H-D), (H-L), (H-P) and the
*overlap condition*

    (OV)      K*(M)  ≤  C(M).

Then CI(M) has no feasible state (Theorem N6a at scale M).

*Proof.*  Suppose (χ, ≺_A, ≺_B) is feasible.  By Lemma U (notes/55
§1.3), χ is straddle-free for both teams, meets the (2,2,2) bounds,
and all six block theories Th_i(T) are consistent.  Write
m := min(|Y_A|, |Y_B|).

**Case F.**  Some team T ⊇ S for an S ∈ 𝔉(M).  By Lemma DP
(notes/56 §0.2 — pure restriction), Th₂(T) is inconsistent:
contradiction.  So χ is fan-clean (w.r.t. 𝔉(M) — the same catalogue
appearing in (H-D), (H-L)).

**Case L: m ≤ K*(M) − 1.**  By (OV), m ≤ C(M) − 1.  After the team
swap that names the band-minor team A (every constraint family in
the L-LOP instance — straddles, bounds, fan patterns as
monochromaticity prohibitions for BOTH teams, and the guarded Th1 of
the OTHER team — is invariant under the simultaneous swap), χ lies
in the coloring space of the (H-L) instance.  Its UNSAT says no
coloring of that space extends to a model of Th1(B); since the
instance existentially quantifies Th1(B)'s order variables over
exactly the guarded theory Th1 of χ's band-major team, Th1(band-
major) is inconsistent: contradiction with Lemma U.

**Case P: m ≥ K*(M).**  χ satisfies all constraints of the (H-D)
instance except possibly Φ ≥ 1; UNSAT forces Φ(χ) = 0.  Both teams
have |U_T| ≥ 1 (bounds), so Lemma PH (notes/56 §3.1, PROVED) pins
χ|_{P0∪P2} to the complementary parity alignment, up to team swap;
apply the swap so that U_A = odds.  χ's band split is one of the
band colorings quantified in the (H-P) instance (it has ≥ 2 band
values per team by the bounds); UNSAT says every such split has some
guarded block theory inconsistent — and the guarded theories
evaluated at χ are exactly Th_i(T) of χ (the guards fire precisely
on χ's member sets).  Contradiction with Lemma U.

Cases L and P are exhaustive over m by (OV) (m ≤ K*−1 or m ≥ K*),
and Case F is the prior filter.  ∎

The two WLOG steps are discharged by swap-invariance: every
constraint family used (straddle, bounds, fan-pattern prohibition,
guarded theories, Φ, the PH pinning pair) maps to itself under the
simultaneous exchange of teams, and Lemma PH's two pinnings are
exchanged by it.

### D.3 The overlap bookkeeping

L-arm coverage: m ∈ [2, C(M)−1] (the bounds force m ≥ 2).  P-arm
coverage: m ∈ [K*(M), ⌊(M+16)/2⌋] (m cannot exceed the balance
point).  Overlap interval [K*(M), C(M)−1], width

    W(M) := C(M) − K*(M)   ( ≥ 0  ⟺  (OV) ).

Measured values [MACHINE-CHECKED, e149/e150]:

    M      K*(M)   C(M)   W(M)   overlap interval
    48      26      30      4       26..29
    64      35      37      2       35..36
    80      42      45      3       42..44
    96      51      52      1       {51}

Drift laws relative to balance b(M) = (M+16)/2: K*(M) − b(M) = −6
on M ≡ 16 (mod 32), −5 on M ≡ 0 (mod 32) (four data points; the
CONCURRENT notes/57 §0–2 derives the corrected non-residue law for
K* from the forced-interval calculus — that law supersedes the
mod-32 reading here, and Theorem ASM′ is agnostic to which law
holds); (C(M)−1) − b(M) = −3, −4, −4, −5 at 48/64/80/96 —
approximately −1 per 32 but NOT yet a clean periodic law.
Extrapolation reaches W = 0 near M = 128 (still exhaustive) and
could cross below zero near M = 160.

### D.4 What remains of GAP-ASM′

With Theorem ASM′ proved, GAP-ASM′ reduces to exactly:

    (OV-∀)   K*(M) ≤ C(M)   for every M ≡ 0 (mod 16), M ≥ 48,

plus per-scale supply of the four machine items (which the
uniformization gaps GAP-DICH / GAP-LLOP / GAP-PARM will replace by
proofs).  Two routes, per the notes/56 §4b probes (both negative
levers already measured at 96): (i) sharpen the drift laws with
M = 112/128 data and prove (OV-∀) directly if the laws stabilize;
(ii) the designated fix — ROBUST P-ARM: replace Φ = 0 by Φ ≤ φ₀ in
(H-D)/(H-P), lowering the P-arm's entry threshold K* and restoring
overlap for large M regardless of the C(M) drift; the CONCURRENT
notes/58 §4 (Lemma PH+, COV-W′, RP-ARM) is exactly this fix in
progress — its composition slots into Theorem ASM′ by replacing
(H-D)+(H-P) with the robust pair and the PH step with PH+.  Status:
Theorem ASM′ [PROVED]; (OV) [MACHINE-CHECKED at 48/64/80/96];
(OV-∀) [GAP — arithmetic of two thresholds, compute-extendable].

---

## E. Shift summary and ledger deltas

Proved this shift (uniform in M unless noted):

| item | statement | where |
|------|-----------|-------|
| Lemma CC | T/RL/RT closure calculus sound for ThFG | §A.1 |
| Lemma FW | fan-walk descent sets + cycles refute ThFG | §A.2 |
| Theorem AFF | every FW shape is an M-uniform affine schema | §A.3 |
| Γ₂′ | p = 5a+6q family (subsumes e142n) | §A.4 |
| Γ₃ | mirror-pair D-unit cycles, 6 residue patterns | §A.4 |
| Lemmas JP/JP′ | the uniform 6-fact Lemma-J pair schemas | §B.1 |
| Lemma J | upgraded MACHINE-CHECKED → PROVED (36 pencil derivations) | §B.2 |
| Theorem ASM′ | F/L/P composition soundness; GAP-ASM′ ⟶ (OV-∀) | §D.2 |

Machine-checked this shift (all with soundness cross-checks):

* e152/e152c/e152d: independent closure grid at 48 (= e142o);
  MC/Γ₃/FW coverage 343/607/1467 of 1851; 0/165 false positives.
* e153: full pencil catalogue for Lemma J (29 closure + 7 split).
* e154: complete SAT classification of the 165 closure-alive pairs —
  R(48) = 90 (all gaps ≡ 0 mod 8), D(48) = 75 (= non-resonant
  E1×E1).
* e154b: branch certificates for 55/75 of D(48); the 20-pair open
  core is parity-locked (even gaps, q ≥ 52) and halves onto
  half-scale fan pairs.

Ledger deltas applied: notes/55 §3.4 + §7 (J-pencil closed;
FG-schema and FG-deep rows rewritten), notes/56 §5.2 (ASM′ row →
(OV-∀)), notes/50 inventory (N6a row + night-shift delta block).

Honest corrections recorded: (1) notes/55's "every fan escape has
gap ≥ 16" is false at depth — gap-8 escapes exist, all inside
E1×E1; the close-pair kill law needs the E1 exclusion.  (2) The
"mechanical taxonomy, low risk" rating of GAP-FG-schema was wrong:
a fixed affine list provably cannot cover the dead grid (the walk
calculus with parametric shapes is needed, and the deep block needs
one more rule family).

Next steps (ranked): (1) FW + RT-glue extension, re-measure the
deep block (cheap, likely absorbs the 279); (2) e154 at M = 64/96
to audit the resonance law and the E1×E1 deep characterization
cross-scale; (3) fold the 20-pair halving core into the GAP-PARM
schema work (notes/58); (4) M = 112/128 K*/C data for (OV-∀).
