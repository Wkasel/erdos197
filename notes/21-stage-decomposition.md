# The stage-decomposition reduction (session 5)

## Theorem (Stage Reduction) — proved by case analysis
Let s: S_A → ℕ have finite fibers F_0, F_1, ... For an AP triple (x,y,z)
(z = 2y−x, all in S_A), with T = concatenation of internally-ordered fibers:

| stage pattern                | consequence                          |
|------------------------------|--------------------------------------|
| s(x), s(z) both < s(y)       | safe (y last of the triple's stages) |
| s(x), s(z) both > s(y)       | safe (y first)                       |
| s(x) < s(y) < s(z)           | AUTO-VIOLATION — condition (A)       |
| s(z) < s(y) < s(x)           | AUTO-VIOLATION — condition (A)       |
| s(x) < s(y) = s(z)           | forced z ≺ y in F_{s(y)}             |
| s(z) < s(y) = s(x)           | forced x ≺ y                         |
| s(x) = s(y) < s(z)           | forced y ≺ x                         |
| s(y) = s(z) < s(x)           | forced y ≺ z                         |
| s(x) = s(y) = s(z)           | within-fiber triple (both dirs forbidden) |

**If (A): no AP triple has strictly monotone stages, and (B): every fiber
admits a linear order containing its forced pairs and avoiding monotone
within-fiber triples — then S_A is permutable.** Fibers are INDEPENDENT
finite problems (no committed-prefix regress, no compactness): each fiber's
constraint set is finitely determined by s alone. Same reduction applies
verbatim to S_B (completions from odd blocks land in even blocks = out of
team — same magic).

This replaces the ω-ification lemma: the search is now for a closed-form s.

## Facts established (machine, e59–e61)
1. Pure block stages (s = block/2): (A) holds VACUOUSLY (z = 2y−x < 2y can't
   reach a later even block; value-monotonicity kills the decreasing pattern).
   But (B) fails: stage-3 fiber (block (32,64], 51 forced pairs from
   earlier-block completions + 240 triples) UNSAT — this is Theorem 1 / the
   fatal zone rediscovered in stage coordinates. So delays are NECESSARY.
2. Delay danger zone (hand proof): delaying z ∈ block k breaks (A) via some
   pair (x, y=(x+z)/2, y in block k, x in an earlier even block) iff
   z > 3·2^{k−2} (top half of block k), unless every witness midpoint y is
   delayed to ≥ s(z) as well. Verified: (256, 513, 770) is exactly this
   (770 > 768). Mined stage formula (depth-based) breaks (A) this way AND
   has UNSAT fibers → dead as stated.
3. Joint stage+order SAT (delay window ≤ 2), N=256: SAT but degenerate —
   solver delays whole blocks uniformly (stage relabeling + truncation
   artifact). Minimal-delay version (e61, CP-SAT) running.
4. Minimal-extras ladder E*(X,d) (e57): E*(16, d=2) = 16 OPTIMAL — half of
   block 6 must be pulled ahead of the level boundary. Intrinsic lookahead is
   proportional, not O(1). d=3 local, d=4 on fleet2.

## The plan
- Mine minimal delay sets at N=256, 1024 → closed form for D_k ⊆ block k
  (expect: bottom-half classes by the danger-zone constraint, cf. defect ≡2
  mod 2^{k/2} classes — those live in bottom half? ≡2 mod m values spread
  everywhere — reconcile!).
- Then (A) for closed form: hand proof via danger-zone closure.
- (B) for closed form: fibers become self-similar at scale 4 → induction.
