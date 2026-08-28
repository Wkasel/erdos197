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
