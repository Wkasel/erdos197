# 78 — FRONT N2-DIAG + N3-GROW: the affine C3(p) theorem and the
# growth-law uniformization

Session 2026-08-30 (final-four phase; targets = two of the four gating
gaps of notes/50 §6).  Verdicts up front:

* **GAP-N2-DIAG: DISCHARGED (pending the next audit cycle).**  Part I
  is the uniform-in-p write-up: Theorem C3(p) — the diagonal core
  C3(p) = {t_p≺b_p, t_{p−2}≺b_{p+1}, t_{p+5}≺b_{p−2}} is inconsistent
  with AP-freeness on (M, 2M] for EVERY odd p ≥ 5 and every
  M ≡ 2p+6 (mod 8), M ≥ 2p+6 — proved with the notes/33 toolkit
  (Z/D/E/P) unchanged; every constant of the p = 5 proof becomes an
  affine form in p, every residue/parity/window check is done once,
  parametrically.  Machine: the e123 strict schema executor at NINE
  p-values 5..21 (104 layer-1 + 52 flip + 52 sharpness scales each,
  0 failures — p = 15, 17, 19, 21 FRESH this session), independent
  complete-encoding solver cross-validation at fresh p = 17, 21
  (20/20 verdicts incl. M = 256/260), and the applicability
  boundaries verified EXACT: L1(p) passes at every 4 | M ≥ p+7 (first
  in-block scale) and FLIP(p) at every in-class M ≥ 2p+6, for all
  nine p (e180 partMINM).
* **GAP-N3-GROW: (N3-a) tightened to a single half-scale hypothesis
  (notes/74 correction: both parity classes halve onto the SAME
  single-attacker system SA((x+1)/2; M/2), not (x+3)/2); (N3-b)
  uniformized to a stated schema (lane pigeonhole + severed-run
  locality) with its residue tagged; the growth law
  d*(x) = ⌊(x−1)/4⌋ confirmed at TWO FRESH (x, C) points**:
  d*(19) = 4 at M = 80 (atmost-3 anywhere UNSAT, atmost-4 SAT) and
  d*(23) = 5 at M = 112 (atmost-4 anywhere UNSAT, atmost-5 SAT) —
  five exact x-points total (11, 15, 19, 23, 27), x = 23 the first
  ≡ 7 (mod 8) point.  The x = 23 witness is the predicted pure-bottom
  lane transversal; the x = 19 witness is a NON-transversal
  decoration escape ({b₃,b₅,b₆,b₇}, 1 of 4 lane units hit) — fresh
  confirmation that only the COUNT form of the law is true (notes/74
  §I.5).  (N3-b) itself remains the open link, correctly shaped, now
  with its uniform skeleton written.

Machine layer this session: experiments/e180_diag_grow.py →
data/e180_diag_grow.json + e180_minm.log / e180_xval.log /
e180_kcrit.log; rerun of e123_diagonal_schema.py at pmax = 21 →
data/e123_diagonal_schema.json + e123_diagonal_p21.log.  Also folded
in: the previously in-flight e174 partKCRIT112 landing (d*(27) = 6
at M = 112, mixed-transversal witness — data/e174_kcrit112.log).

---

## Part I — Theorem C3(p): the affine-in-p Z/D/E/P proof

### I.0 Setting and statement

Notation as in notes/33 §1: order ≺ on (M, 2M], AP-free = every 3-AP's
midpoint leads both endpoints or trails both (rules R1–R4),
b_j := M+j, t_i := 2M−i, m₀ := 3M/2, block offset ω(v) := v − M.
For odd p ≥ 5 the diagonal pair is {3p, 3p+1} and its core is

    C3(p) = { A1(p): t_p ≺ b_p,          [attacker 3p,   j = p]
              A2(p): t_{p−2} ≺ b_{p+1},  [attacker 3p,   j = p+1]
              A3(p): t_{p+5} ≺ b_{p−2} } [attacker 3p+1, j = p−2]

(C3(5) = C3 of notes/33; the unit (t_{a−2j} ≺ b_j) is attacker a's
j-th attack unit).

**Theorem C3(p).**  For every odd p ≥ 5 and every M ≡ 2p+6 (mod 8)
with M ≥ 2p+6, no AP-free order of (M, 2M] satisfies C3(p).

The class M ≡ 2p+6 (mod 8) — equivalently M ≡ 0 (mod 4) with
M/2 ≡ p+3 (mod 4) — is the **flip class** of p: for p ≡ 1 (mod 4) it
is M ≡ 0 (mod 8) (the T-PIN class consumed by Theorem B1), for
p ≡ 3 (mod 4) it is M ≡ 4 (mod 8).  At p = 5 the statement and bound
(M ≥ 16) are exactly thm:c3core.

Proof shape = notes/33 verbatim: Theorem L1(p) (layer 1, all of
M ≡ 0 mod 4) + Theorem FLIP(p) (the flip, on the flip class), glued by
Lemma E(p).  Sections I.1–I.5 give the parametric proofs; every claim
of the form "value V lies in mod-4 class c / is a leader / has mirror
W in the block" is verified by an affine identity displayed once.

### I.1 The affine constant table

Throughout M ≡ 0 (mod 4), so ω(v) ≡ v (mod 4), M/2 is even, m₀ is
even, m₀ ± 1 are odd and cover both odd mod-4 classes.  p is odd, so
{p, p+2} = the two odd residues mod 4 and 2−p ≡ p, −p ≡ p+2 (mod 4).

| object | affine form | class (mod 4) / parity |
|---|---|---|
| core values | t_p = 2M−p, t_{p−2} = 2M−p+2, b_{p−2} = M+p−2, b_p = M+p (odd); t_{p+5} = 2M−p−5, b_{p+1} = M+p+1 (even) | t_{p−2}, b_p ≡ p; t_p, b_{p−2} ≡ p+2 |
| odd d=2 ladder | w_i = M+1+2i, i = 0..M/2−1 | b_j at index (j−1)/2, t_i at index (M−i−1)/2 |
| centers | the two odd neighbors m₀−1, m₀+1 of m₀ | one ≡ p, one ≡ p+2 (mod 4) |
| POLAR mirror | 2m₀ − t_p = b_p | p-free identity |
| flip mirror APs | b_{p−2} + t_p = 3M−2 = 2(m₀−1); b_p + t_{p−2} = 3M+2 = 2(m₀+1) | p-free identities |

G4-center condition (Lemma P at g = 4): c is a center for the class
≡ c+2 (mod 4).  Hence the center ≡ p (mod 4) floods the class of
{b_{p−2}, t_p}, and the center ≡ p+2 floods the class of
{b_p, t_{p−2}}.

### I.2 The toolkit is p-free; Lemma E(p)

Lemmas Z (zigzag), D (phase dichotomy) and P (flood: POLAR, P2, G4
instances) are quoted from notes/33 §§2–3 **unchanged**: their
statements and proofs never mention the core offsets, only a ladder, a
center, a seed and a target.  The only parametric lemma is the
transfer lock:

**Lemma E(p).**  Let M be even, M ≥ 2p+2.  On the odd d=2 ladder the
four odd core values sit at indices

    b_{p−2}: (p−3)/2,   b_p: (p−1)/2,
    t_p: (M−p−1)/2,     t_{p−2}: (M−p+1)/2

— two adjacent pairs, all four distinct (the collision values are
M = 2p−4, 2p−2, 2p < 2p+2).  The index gap (M−p+1)/2 − (p−1)/2 =
M/2 − p + 1 is even iff M ≡ 0 (mod 4).  Hence by Lemma Z:

* M ≡ 0 (mod 4):  b_p ≺ b_{p−2} ⟺ t_{p−2} ≺ t_p;
* M ≡ 2 (mod 4):  b_p ≺ b_{p−2} ⟺ t_p ≺ t_{p−2}.

*Proof.*  As notes/33 Lemma E: each orientation of one adjacent pair
seeds Lemma Z; the other pair's left member is a leader iff its index
has the seed-leader parity, which the displayed gap computes.  ∎

### I.3 Theorem L1(p)

**Theorem L1(p).**  Let p ≥ 5 be odd, M ≡ 0 (mod 4), M ≥ p+7, and let
≺ be an AP-free order of (M, 2M] satisfying A2(p) and A3(p).  Then
b_p ≺ b_{p−2} and t_{p−2} ≺ t_p.

*Proof.*  It suffices to refute S: b_{p−2} ≺ b_p — then Lemma E(p)
supplies the transfer.  (The refutation below never needs Lemma E's
bound M ≥ 2p+2.  For the transfer half at p+7 ≤ M < 2p+2: within
M ≡ 0 (mod 4) the only E-collision scale is M = 2p−2, where
b_p = t_{p−2} and b_{p−2} = t_p, so the transfer statement IS the
already-forced pair and holds trivially; 2p−4 and 2p are ≡ 2 mod 4.)
Assume A2, A3, S.

**Phases and centers.**  Lemma Z on the odd ladder, seeded by S at the
adjacent indices (p−3)/2 ≺ (p−1)/2: the ODD2 leaders are the offsets
≡ p−2 ≡ p+2 (mod 4).  Let

    c*  := the element of {m₀−1, m₀+1} with c* ≡ p   (mod 4),
    c** := the other one            (c** ≡ p+2 (mod 4)).

Then (i) c* is a G4-center for the class ≡ p+2 ∋ b_{p−2}, and an ODD2
**trailer** (offset ≡ p), so its odd neighbors c*±2 (≡ p+2) are
leaders and the zigzag edges c*±2 ≺ c* are facts; (ii) c** is a
G4-center for the class ≡ p ∋ t_{p−2}, and itself an ODD2 **leader**:
c** ≺ c**±2.

Split on the comparison (t_p, m₀) — legitimate: t_p odd ≠ m₀ even.

**Case I: t_p ≺ m₀.**  POLAR-inward at m₀ (seed t_p, mirror b_p, both
in block): every odd value ≺ m₀.  Then:

1. *b_{p−2} ≺ c**  by the G4-inward flood at c* over the class ≡ p+2:
   seeds c*±2 ≺ c* at e = 2; target b_{p−2}, pair distance
   |c* − b_{p−2}| ≡ p − (p+2) ≡ 2 (mod 4), mirror 2c* − b_{p−2} ∈
   {t_{p−4}, t_p} (offsets p−4 ≥ 1 and p ≤ M−1: in block).  The
   class-(p+2) d=4 ladder's phase is unknown: Lemma D, both branches.
2. *c* ≺ t_{p+5}*  by the P2-outward flood at c* over the evens: seed
   c* ≺ m₀ (POLAR, e₀ = 1, mirror m₀ ∓ 2... ± 2 in block); target
   t_{p+5} (even since p odd; in block since p+5 ≤ M−1), mirror
   2c* − t_{p+5} ∈ {b_{p+3}, b_{p+7}} (offsets ≤ p+7 ≤ M: in block).
   Even-ladder phase unknown: both branches.
3. A3: t_{p+5} ≺ b_{p−2}.

1–3 give the 3-cycle b_{p−2} ≺ c* ≺ t_{p+5} ≺ b_{p−2}.  ⊥

**Case II: m₀ ≺ t_p.**  POLAR-outward: m₀ ≺ every odd value.  Then:

1. *c** ≺ t_{p−2}*  by the G4-outward flood at c** over the class
   ≡ p: seeds c** ≺ c**±2; target t_{p−2}, pair distance ≡ 2 (mod 4),
   mirror 2c** − t_{p−2} ∈ {b_{p−4}, b_p} (offsets ≥ p−4 ≥ 1: in
   block).  Both d=4 phases.
2. *b_{p+1} ≺ c***  by the P2-inward flood at c** over the evens:
   seed m₀ ≺ c** (POLAR, e₀ = 1); target b_{p+1} (even; in block),
   mirror 2c** − b_{p+1} ∈ {t_{p−1}, t_{p+3}} (offsets ≥ p−1 ≥ 4 and
   ≤ p+3 ≤ M−1: in block).  Both phases.
3. A2: t_{p−2} ≺ b_{p+1}.

1–3 give the 3-cycle c** ≺ t_{p−2} ≺ b_{p+1} ≺ c**.  ⊥

Both cases close, so S is impossible.  ∎

(As at p = 5: Case I consumes only A3, Case II only A2; the split
(t_p, m₀) is the one cross-parity interleave item, exactly the
S2-mandated transport.  For p = 5 this is notes/33 Theorem L1
verbatim, constants included.)

### I.4 Theorem FLIP(p)

**Theorem FLIP(p).**  Let p ≥ 5 be odd, M ≡ 2p+6 (mod 8), M ≥ 2p+6,
and let ≺ be an AP-free order of (M, 2M] satisfying A2(p), A3(p) and
b_p ≺ b_{p−2}.  Then A1(p) is impossible: b_p ≺ t_p is forced.

*Proof.*  Assume A1: t_p ≺ b_p, for contradiction.  Lemma Z on the
odd ladder, seeded by b_p ≺ b_{p−2} (index (p−1)/2 leads): the ODD2
leaders are the offsets ≡ p (mod 4).

**The mod-8 lock, p-shifted.**  M/2 ≡ p+3 (mod 4) is exactly what
makes both centers usable:

    cI  := m₀−1:  offset M/2−1 ≡ p+2 (mod 4)
           — G4-center for the class ≡ p ∋ b_p; ODD2 trailer, its odd
           neighbors m₀−3, m₀+1 (offsets M/2−3, M/2+1 ≡ p) are
           leaders: m₀−3 ≺ cI, m₀+1 ≺ cI;
    cII := m₀+1:  offset M/2+1 ≡ p (mod 4)
           — G4-center for the class ≡ p+2 ∋ t_p; itself an ODD2
           leader: cII ≺ cII±2.

Split on (t_p, m₀).

**Case I: t_p ≺ m₀.**  POLAR-inward: every odd ≺ m₀.  Then:

1. *cI ≺ t_{p+5}*  [P2-outward at cI over the evens; seed cI ≺ m₀
   (POLAR, e₀ = 1); mirror 2cI − t_{p+5} = b_{p+3} in block; both
   phases].
2. cI ≺ b_{p−2}  [1 + A3].
3. cI ≺ t_p  [mirror rule R4 on the AP (b_{p−2}, cI, t_p):
   b_{p−2} + t_p = 3M−2 = 2·cI, strict betweenness from
   p−2 < M/2−1 < M−p, i.e. M > 2p+2 — in class this is M ≥ 2p+6].
4. cI ≺ b_p  [3 + A1].
5. *b_p ≺ cI*  [G4-inward at cI over the class ≡ p; seeds m₀−3 ≺ cI,
   m₀+1 ≺ cI at e = 2; target b_p at distance |M/2 − p − 1| ≡ 2
   (mod 4) (from M/2 ≡ p+3), mirror 2cI − b_p = t_{p+2} in block;
   both phases].

4 and 5 are a 2-cycle.  ⊥

**Case II: m₀ ≺ t_p.**  POLAR-outward: m₀ ≺ every odd.  Then:

1. *b_{p+1} ≺ cII*  [P2-inward at cII over the evens; seed m₀ ≺ cII
   (POLAR, e₀ = 1); mirror 2cII − b_{p+1} = t_{p−1} in block; both
   phases].
2. t_{p−2} ≺ cII  [A2 + 1].
3. b_p ≺ cII  [mirror rule R3 on the AP (b_p, cII, t_{p−2}):
   b_p + t_{p−2} = 3M+2 = 2·cII, betweenness again from M ≥ 2p+6].
4. t_p ≺ cII  [A1 + 3].
5. *cII ≺ t_p*  [G4-outward at cII over the class ≡ p+2; seeds
   cII ≺ cII±2; target t_p at distance |M/2 − p − 1| ≡ 2 (mod 4),
   mirror 2cII − t_p = b_{p+2} in block; both phases].

4 and 5 are a 2-cycle.  ⊥  ∎

(Case I consumes A3, Case II consumes A2, A1 symmetrically in both —
the p = 5 anatomy, verbatim.  The two mirror APs ride the p-FREE
identities b_{p−2} + t_p = 3M−2, b_p + t_{p−2} = 3M+2: the diagonal
lane is precisely the family that keeps the flip's fulcrum values
m₀±1 fixed while the core slides.)

### I.5 Assembly, sharpness, boundaries

**Proof of Theorem C3(p).**  M ≡ 2p+6 (mod 8) ⟹ M ≡ 0 (mod 4) and
M ≥ 2p+6 ≥ p+7 (p ≥ 5... p+7 ≤ 2p+6 ⟺ p ≥ 1), so Theorem L1(p)
applies: A2 + A3 force b_p ≺ b_{p−2}.  Theorem FLIP(p) then refutes
A1.  ∎

**Sharpness (uniform in p).**  On the complementary even class
M/2 ≡ p+1 (mod 4): the offsets of m₀∓1 become M/2−1 ≡ p and
M/2+1 ≡ p+2 — both centers land in the WRONG mod-4 class for the
floods FLIP needs (cI would flood the class of its own mirror family,
not of b_p), and the ODD2 leader statuses invert (cII becomes a
trailer, cI's neighbors trailers): neither case's seed set exists.
And AP + C3(p) is genuinely SAT there — machine, every p tested
(e122/e123b/e180) — so the flip class is exactly right, for every p.

**Boundaries are exact and affine (machine, e180 partMINM).**  For
every p = 5..21: check_layer1(M, p) passes at every 4 | M from the
first multiple of 4 with M ≥ p+7 upward (= all six core values and
all four mirror offsets in block; below it, failures), and
check_flip(M, p) passes at every in-class M ≥ 2p+6 and fails at the
one in-class scale below with degenerate value collisions
(M = 2p−2, where t_p = b_{p−2} degenerates the hypothesis set).
The stated bounds need no slack: the write-up's window conditions ARE
the machine boundary.  (Below p+7 and off-class the theorem makes no
claim; small in-class scales are inside the verified range anyway.)

**Remark (interior coincidences are harmless).**  For M between p+7
and 2p+6 the six core values can collide with flood targets or with
each other (e.g. t_p = b_{p−2} at M = 2p−2 — outside the flip class);
L1(p)'s derivation is coincidence-tolerant (no step needs two named
values distinct unless displayed, and the checker enforces
non-reflexivity per step), which is why its verified range starts at
p+7, not 2p+10.  FLIP(p) does need t_p ≠ b_{p−2} (step I.3's strict
betweenness), which in class is free.

### I.6 Machine record (Part I)

| instrument | scope | verdict |
|---|---|---|
| e123_diagonal_schema.py pmax=21 (rerun this session) | strict rung-by-rung schema execution (e113 discipline: every AP membership, every R-rule pattern, every leader/trailer/residue claim, both branches of every phase dichotomy, per-branch hypothesis audit) | p = 5..21 (9 values, p = 15/17/19/21 FRESH): layer1 104/104 scales each (4p..4p+396 + 512/516/1024/1028 ∩ 0 mod 4), flip 52/52, sharpness 52/52 — **0 failures** (data/e123_diagonal_schema.json, e123_diagonal_p21.log) |
| e180 partMINM | applicability boundary scan, ALL scales 8 ≤ M ≤ 4p+40 (L1) / 4p+84 (flip) | boundary claims hold for all 9 p: L1 ALL PASS from the first 4 | M ≥ p+7; FLIP ALL PASS from in-class M = 2p+6; recorded pass/fail zones below verbatim (data/e180_diag_grow.json) |
| e180 partXVAL | independent complete-encoding Cadical195 (e123b encoder), FRESH p = 17, 21 | 20/20 OK: C3(p) UNSAT at 5 flip scales incl. 256, SAT at 5 complementary scales incl. 260, full rung UNSAT at all 10, per p (data/e180_xval.log) |
| e123b (prior) | same, p = 5..13 | 0 mismatches (data/e123b_diagonal_xval.json) |

**Ledger effect.**  GAP-N2-DIAG's species was "uniformization (affine
Z/D/E/P; p = 5 instance PROVED)"; Part I is that write-up.  Tag moves
to **[PROVED — this note; instance-audited at 9 p-values × 208
scales, solver-cross-validated at 6 p-values; adversarial audit
pending]**.  (H1′) part 1 of Theorem B1 is discharged; the Case-1
kill chain's residue is (H1′) part 2 = GAP-N3-GROW (N3-b) alone.

---

## Part II — N3-GROW: the growth law uniformized

### II.0 Object and statement

For odd x ≥ 11 the single-block rung R(x; M) is the AP theory of
(M, 2M] plus ALL attack units of the pair {x, x+1}:
(t_{a−2j} ≺ b_j) for a ∈ {x, x+1} and every j ≥ 1 with
0 ≤ a−2j ≤ M−1 (i = 0, i.e. t₀ = 2M, occurs for a = x+1 when
j = (x+1)/2).  R(x; M) is UNSAT at every M ≥ x+57 and every residue
(N2-COMPLETE, notes/73).  For a puncture set D ⊂ (M, 2M],
R(x; M) ∖ D is the theory restricted to (M, 2M] ∖ D (guarded units);
d*(x; M) := min{|D| : R(x; M) ∖ D is SAT}.

**N3-GROW (the growth law; notes/74 §I.3).**
d*(x; M) = ⌊(x−1)/4⌋ for every large-enough M.  The ≤-side is
(N3-a), the ≥-side is (N3-b) = **GAP-N3-GROW proper**:

    (N3-b)  For every odd x ≥ 11 and every puncture set D with
            |D| < ⌊(x−1)/4⌋:  R(x; M) ∖ D is UNSAT.

### II.1 The lane and its pigeonhole  [PROVED]

**Definition.**  The *transport lane* of x is
T(x) := {(t_{x−2j}, b_j) : j even, 2 ≤ j ≤ (x−1)/2} — the even-j
units of the ODD attacker.

**Lemma LANE(x).**  |T(x)| = ⌊(x−1)/4⌋, and for M > 2x the supports
of the lane units are pairwise disjoint (2⌊(x−1)/4⌋ distinct values).
Hence every D with |D| < ⌊(x−1)/4⌋ leaves at least one lane unit with
both endpoints alive.

*Proof.*  j ranges over the even integers in [2, (x−1)/2]: exactly
⌊(x−1)/4⌋ of them.  The t-offsets x−2j are distinct, the b-offsets j
are distinct, and a t/b collision t_{x−2j} = b_{j′} needs
(x−2j) + j′ = M ≤ 2x − 4 + (x−1)/2 < 2x, excluded.  Pigeonhole.  ∎

### II.2 (N3-a) as a one-hypothesis schema  [PROVED mod GAP-SA-HALF]
### — with a notes/74 correction

**Lemma PS(x) (parity split).**  Let M be even and let D be any
transversal of T(x) (one endpoint from each lane unit,
|D| = ⌊(x−1)/4⌋).  If the single-attacker rung SA((x+1)/2; M/2) —
the block (M/2, M] with all units of the single attacker (x+1)/2 —
is satisfiable, then R(x; M) ∖ D is satisfiable: any order placing
every even value before every odd value, each parity class ordered by
a lift of an SA((x+1)/2; M/2)-witness, works.  Hence
d*(x; M) ≤ ⌊(x−1)/4⌋.

*Proof.*  (1) A 3-AP with odd common difference has same-parity
endpoints and opposite-parity midpoint; under evens-first its midpoint
leads both or trails both automatically.  So only within-parity APs
constrain, and each parity class is an affine copy of (M/2, M]
(h_E(v) = v/2 on evens; h_O(v) = (v+1)/2 on odds — notes/33 Lemma H),
preserving and reflecting APs.  (2) Unit parities: t_{a−2j} ≡ a,
b_j ≡ j (mod 2).  Even attacker a = x+1 with j odd: even t before odd
b — satisfied by the split.  The only units the split VIOLATES are
odd-t-before-even-b: a = x, j even — exactly T(x), and D kills each
of them (a unit with a punctured endpoint is vacuous).  (3) The
residual within-class systems: under h_E, the units {a = x+1, j even}
map EXACTLY onto the unit set of SA((x+1)/2; M/2); under h_O, the
units {a = x, j odd} map EXACTLY onto the SAME set SA((x+1)/2; M/2)
(both identities machine-verified as exact set equalities at
x = 11, 15, 19, 23, 27 — see II.4; affine proof: h_E sends
(t_{(x+1)−2j}, b_j) to (t′_{(x+1)/2−j}, b′_{j/2}), h_O sends
(t_{x−2j}, b_j) to (t′_{(x−1)/2−j}, b′_{(j+1)/2}), and both index
maps are bijections onto {(t′_{(x+1)/2−2j′}, b′_{j′})}).  A witness
of SA((x+1)/2; M/2) lifts to each class; the split order is AP-free
and satisfies every surviving unit.  ∎

**Correction to notes/74 §I.6.**  There the odd class was said to
halve onto the attacker-(x+3)/2 system; the correct value is
(x+1)/2 for BOTH classes — the two residual systems are not merely
same-species but IDENTICAL, so (N3-a) rests on ONE half-scale
hypothesis:

    (GAP-SA-HALF)  SA(y; m) is SAT (single-attacker rungs never
    kill) — machine-true at every scale ever tested (g4b "singles
    always SAT", e122 lane censuses, e174c realized witnesses),
    no hand proof yet.

This explains why every lane transversal escapes (the pure-bottom
{b₂, b₄, …} at x = 27/M = 80 and x = 23/M = 112, the mixed one at
x = 27/M = 112 — any transversal works, the solver picks
arbitrarily).  It does NOT claim minimal escapes are all
transversals; they are not (II.3, II.4).

### II.3 (N3-b): the uniform skeleton and its exact residue

(N3-b) is STRICTLY stronger than "some lane unit survives ⟹ UNSAT" —
that implication is FALSE as a law (notes/74 §I.5: {b₂,b₄,b₅} at
x = 15, M = 96/112/128 leaves (t₃,b₆) alive yet escapes; fresh and
sharper this session: {b₃,b₅,b₆,b₇} at x = 19, M = 80 leaves THREE
of the four lane units fully alive and still escapes — only the
count form is true).  A small D can leave a lane unit alive AND
sabotage the derivation that would use it, by puncturing ladder
interiors.  The uniform proof shape (anchor-freedom, notes/74 §I.5)
therefore has two layers, of which the first is now a stated lemma:

**Lemma SEV (severed-run locality)  [PROVED].**  Let D be a puncture
set.  (a) A d-ladder of (M, 2M] ∖ D is severed by its ≤ |D| hit
positions into maximal runs; Lemmas Z and D hold verbatim PER RUN
(their proofs use only the three-term APs of consecutive run members).
(b) A Lemma-P flood at center c over class C with seed pair e₀ and
target e₁ remains valid whenever the class positions traversed by the
two inductions between e₀ and e₁ — the interval of admissible e's —
avoid D on BOTH sides of c, and each step's mirror AP has both
endpoints alive.  (c) Consequently every catalogued core derivation
(the C3(p) chain of Part I, the fallback-lane cores of e130b, the K4
chain of notes/49) survives any D that avoids its O(1)-value support
and the O(1) runs its floods traverse: the exposure of a core to
punctures is a union of explicitly listed intervals, affine in its
parameters.

*Proof.*  (a) is notes/33 §2 re-read on a run (the proofs of Z/D
never leave three consecutive rungs).  (b) each induction step of
Lemma P (outward-up/-down, inward-up/-down) touches the class ladder
only at distances e, e±g from c and applies one mirror rule; if those
rungs are alive on both sides and the mirror endpoints alive, the
step goes through unchanged.  (c) is (a)+(b) plus reading off which
ladders/floods the fixed derivation uses.  ∎

**The residue, stated exactly.**  With LANE + SEV, (N3-b) reduces to:

    (N3-b′)  For every D with |D| < ⌊(x−1)/4⌋ there is a core in the
    per-pair catalogue whose support AND flood exposure avoid D —
    or a bounded extra case split closes the interior-punctured
    branches.

Machine shadow of exactly this statement (all pre-existing, read into
the record in notes/74 §I.5): the fallback catalogue fires as mod-8
laws across M = 16..168 (e130b); every single anchor puncture has a
fresh dodging core (e130 partC); semantic single-puncture robustness
core-by-core, M = 16..160, zero failures (e130c part1); C = 2
lane-wide (e132 partS); severed-ladder closure of the interior
branches with bounded extra order-trichotomy splits — complete at
M = 112, 6/64 stragglers at 80, short-run artifacts at 48 (e130c
part2 + e174b).  What is NOT yet uniform: (i) the choice function
D ↦ core (the catalogue's support hypergraph has transversal number
≥ ⌊(x−1)/4⌋ — machine at x ≤ 21 via e121, no hand proof of its
growth); (ii) a uniform extra-split set for interior punctures
(e174b's is per-scale).  **GAP-N3-GROW (N3-b) remains open with
exactly this shape**; nothing else in the Case-1 chain is open.

### II.4 Machine record (Part II): two fresh points of the law

New instrument e180 partK (generic-x cardinality bracket, e174
Gadget verbatim: selection-guarded complete encoding, every SAT
witness re-verified by the independent order-decoding scanner, lane
transversality of witnesses checked against T(x)):

| point | query | verdict | time |
|---|---|---|---|
| **x = 19, M = 80** (fresh x; d* pred. ⌊18/4⌋ = 4) | atmost-3 punctures ANYWHERE | **UNSAT** | 7.7 s |
| | atmost-4 | **SAT**, witness {b₃,b₅,b₆,b₇} — a NON-transversal decoration escape (1/4 lane units hit) | 0.2 s |
| **x = 23, M = 112** (fresh x AND ≡ 7 mod 8, outside every earlier census; d* pred. ⌊22/4⌋ = 5) | atmost-4 punctures ANYWHERE | **UNSAT** | 82.6 s |
| | atmost-5 | **SAT**, witness {b₂,b₄,b₆,b₈,b₁₀} = the pure-bottom transversal of T(23) (5/5 units hit) | 13.4 s |

Also folded in from the stalled queue: e174 partKCRIT112 —
d*(27; 112) = 6 (atmost-3/4/5 UNSAT [16/77/270 s], atmost-6 SAT
[11 s], witness {b₂, b₈, b₁₂, t₁₉, t₁₅, t₇} = a MIXED transversal of
T(27), 6/6 units hit) — the x = 27 point now global at TWO scales.

Law summary after this session: d*(x) = ⌊(x−1)/4⌋ exact and global
(cardinality-exhaustive over ALL puncture positions) at
x = 11 (M = 80/112/144), 15 (80/112/144), **19 (80)**, **23 (112)**,
27 (80/112) — five x-points, two fresh, spanning both odd mod-4
classes and (with 23) the x ≡ 7 (mod 8) family.  Witness anatomy:
lane transversals escape at every point where decoded (23/112 pure-
bottom, 27/80 pure-bottom, 27/112 mixed), and decoration escapes of
the SAME size also exist at some cells (15/96..128, 19/80) — the
count is the law, the transversal family its constructive floor
(Lemma PS).  Parity-class halving identities verified as exact set
equalities at all five x-values (this session, inline check; see
II.2).

### II.5 Ledger effect (Part II)

* (H1′) part 2 = GAP-N3-GROW: (N3-a) now [PROVED mod GAP-SA-HALF]
  with ONE hypothesis (correction supersedes notes/74 §I.6's
  two-system reading); (N3-b) still [GAP] — species unchanged
  (uniformization + robustness), skeleton now stated as
  LANE + SEV + (N3-b′) with the machine shadow mapped to it.
* The law's evidence base: 3 → 5 exact x-points (2 fresh, one in the
  previously uncovered x ≡ 7 mod 8 class), d*(27) at a second scale.
* Under the law, x₀(C) = 4C+6 and Theorem B1's Step-1 patch
  (notes/74 §I.4) is unchanged.

---

## Session summary

| item | status |
|---|---|
| Theorem C3(p), affine write-up (I.1–I.5) | [PROVED — audit pending]; GAP-N2-DIAG DISCHARGED |
| e123 @ p = 5..21 (fresh 15/17/19/21) | 0 failures, 9 × 208 scales |
| e180 partMINM boundary scan | exact affine boundaries p+7 / 2p+6, all 9 p |
| e180 partXVAL fresh solver x-val p = 17/21 | 20/20 OK |
| Lemma LANE(x) + Lemma PS(x) + Lemma SEV | [PROVED] (PS mod GAP-SA-HALF) |
| notes/74 correction: both classes halve to SA((x+1)/2; M/2) | machine-verified ×5 x-values |
| d*(19; 80) = 4, d*(23; 112) = 5 (fresh); d*(27; 112) = 6 (landed) | law ⌊(x−1)/4⌋ 5/5 x-points; x=19 witness a fresh non-transversal decoration |
| GAP-N3-GROW (N3-b) | still open; uniform skeleton LANE+SEV+(N3-b′) stated, residue exact |
