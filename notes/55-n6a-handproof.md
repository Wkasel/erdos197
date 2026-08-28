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
