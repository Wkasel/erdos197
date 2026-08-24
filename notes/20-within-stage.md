# 20 — The within-stage order: the R-digit law (and what it does/doesn't solve)

Source data: `data/law_16_3_witness.json` (order of 666 values = S_A∩[1,1024] ∖ D(1024)).
Code: `experiments/e54_full_key.py`; mining scripts in the session scratchpad.

## 1. Stage split — the e53 stage() formula is WRONG for this witness

- The witness's `levels` are **exact prefixes of `order`**: |level_i| = 598, 654, 666
  and set(order[:|level_i|]) == level_i, all three. So the placement bands are
  order[0:598] (stage 0), order[598:654] (stage 1, 56 values, starts 618, 874,
  746, 234, …), order[654:666] (stage 2, 12 values), plus the 16 absent values
  (D(1024) = ≡2 mod 32 in block 10) as stage 3.
- e53's `stage(v) = max(depth−2, arrival(block))` mismatches the witness band on
  **651 of 666** placed values (e.g. 735: band 0, e53-stage 3). The arrival term
  is a *floor for the growing chain*, not a feature of this (static) witness.
- The formula that matches is a **cap**, not a max:

      band(v) = min( max(depth(v)−2, 0), max((block(v)−4)//2, 0) )

  This matches **670 of 682** values of S_A(1024) (mismatch = exactly the 12
  block-10 depth-4 values v ≡ 50 mod 64, i.e. m=(v−2)/16 ≡ 3 mod 4, which the
  witness releases one band early — see §3; this is the "class fattening /
  P3-spillover" noted in notes/19). Deep small-block values (10; 34, 50;
  130…242) are cap-released early, consistent with the cap form.

## 2. Stage 0 (598 values): the discovered law

Remove the 10 block-2/4 values (they are inserted at scattered positions 42,
169–170, 296, 338, 354, 363, 511–512, 594). The remaining 588 values are
**perfectly class-major mod 16** — one run per class, in the order

    15, 7, 3, 11, 1, 9, 5, 13,   0, 8, 4, 12,   6, 14        (2, 10 → later stages)

Feature-precedence on consecutive S0 pairs (first distinguishing feature):
block 179, top/bottom-half 161, none-of-those 146, R-digit3 81, R-digit2 11,
mod16 8, mod8 7, R-digit1 3, mod4 1 — i.e. inside a class run the next-feature
is essentially noise (block/position), while class boundaries follow the
digit hierarchy below.

**The recursive law.** Define the digit expansion (a bijection value ↦ finite
digit string):

    R(v):  v odd        → digit 0, recurse on (v−1)/2
           v ≡ 0 mod 4  → digit 1, recurse on v/4
           v ≡ 6 mod 8  → digit 2, recurse on (v−6)/8
           v ≡ 2 mod 8  → digit 3, recurse on (v−2)/8      (stop at v = 0)

- The mod-16 class order above is exactly ascending R on class representatives.
- **Self-similarity verified**: the odd subsequence of S0, mapped v ↦ t=(v−1)/2,
  reproduces the same class order (t mod 8: 7,3,1,5,0,4,2,6 — identical to the
  full sequence's mod-8 order), i.e. the witness recurses with the *same*
  comparator on the quotient. Predicted mod-16 odd order matches 8/8 classes.
- Consecutive-pair R-prefix monotonicity in S0: k=1: 596/597, k=2: 587/597,
  k=3: 548/597, full string: 299/597. The decay is genuine: the fine
  (deep-digit) order **differs between classes** (class 15, 7 and 0 permute
  their 42 quotients differently), so beyond ~3 digits the witness order is
  SAT-solver freedom, **not** law. The law is the digit hierarchy itself.

Each digit branch is closed under completion: with x = a·q+b, y = a·q'+b in the
same class, z = 2y − x = a(2q'−q)+b, and each branch's quotient map is affine —
so within-class doom-freeness reduces to the *same problem on quotients*
(genuine self-similar peeling, answering task Q2b: yes, but the transform is
the 4-branch affine expansion, not a single u=(v−2)/2^d shift).

## 3. Stage 1 (56 values) and stage 2 (12 values)

All stage-1 values have digit-1 = 3 (v ≡ 2 mod 8). With u = (v−2)/8 the
sequence is: 42 odd u (depth-3 values, all blocks) first, then 50, 818 (digit
(3,2)), then 34 (digit (3,1)), then the 12 block-10 depth-4 values with m ≡ 3
mod 4 (digits (3,2,…)), then 4 with (3,3,…). R-prefix monotone: k=1: 55/55,
k=2: 54/55 (one inversion: 34 after 50/818), k=3: 46/55; full: 29/55 — same
picture: leading digits lawful, tail free.

Key structural find: the stage-1/stage-2 cut splits block-10 depth-4 by
m mod 4 — **m≡3 before m≡1 — which is precisely R's "digit 2 before digit 3"
(equivalently the 3-before-1 odd rule) applied to the quotient**. The defect
classes and their release order are themselves R-structured. Stage 2 =
[210,242,146,178, 530,658,594,722, 194,226,130,162]: block-8 depth-4, then
block-10 (18 mod 64), then block-8 depth≥5 — leading-digit lawful (11/11 at
k=1), tail free.

## 4. The comparator (e54) and doom-check results

`experiments/e54_full_key.py`:

- **R-only (ascending digit strings, no banding): 0 violations at
  N = 2^12, 2^13, 2^14, and 2^16 (43690 values).**
- Why it works — the **exact reflection law** (checked in all six digit
  pairs (a,b), a<b: (0,1)(0,2)(0,3)(1,2)(1,3)(2,3)): at the first digit where
  R(x) and R(y) diverge, z = 2y−x takes x's digit; equal digits recurse
  through the affine quotient. Hence

      R(z) < R(y)  ⟺  R(x) < R(y)      (divergence case; the "R(x) is a
                                         proper prefix" case can flip, but is
                                         benign in S_A up to 2^16 — the
                                         completions leave the team).

  So ascending R is self-protecting: any constraint (x ≺ y) it creates has its
  completion automatically earlier.
- Round 1, (band, R) with the capped band of §1: **25+ violations**. Family:
  cap-released stragglers x with depth(x) = depth(y)+1 ⇒ depth(z) ≥ depth(y)+2
  ⇒ band(z) > band(y) (e.g. x=50, y=130, z=210; x=226, y=562, z=898).
- Round 2, (arrival(block), R): **25+ violations**. Family: x in an old block
  with R(x) > R(y), y in the *bottom quarter* of a new block (only there does
  z = 2y − x stay ≤ 2^b, i.e. in-team); then R(z) > R(y) by the reflection law
  (e.g. x=11, y=35, z=59; x=64, y=543, z=1022). The same law kills descending
  R symmetrically (danger flips to R(x) < R(y) pairs). **Corollary: no
  per-band R-monotone order exists — banded fairness forces a genuine
  interleave/defect discipline.**
- Round 3, greedy R-min chain (arrival bands; repeatedly place the R-smallest
  arrived value whose in-team reflections off already-placed values are all
  placed; defer the rest): **deadlocks in band 1**, e.g. the forced 3-cycle
  45 → 35 → 54 → 45 given sources {9..16} ∪ {63,55,59,61,53,57}. Order of
  early placements matters; naive R-priority is insufficient.

## 5. Status / the residual lemma

- The static within-stage law is settled: **ascending R**, with everything
  beyond the leading digits free (the witness itself uses that freedom).
- The witness `law_16_3` is a *static snapshot arrangement*; it is **not** a
  chain segment: its prefix is not LawState(64) (it opens with block-10
  values). The audited "nesting" is the class-peeling prefix structure of §1,
  not the comp-chain of notes/19. These must not be conflated.
- The remaining lemma, now exactly delimited: schedule the chain so that for
  every old-band x and new-block y with R(x) > R(y) (y necessarily in the
  bottom quarter of its block), the completion z = 2y − x (which satisfies
  R(z) > R(y)) is either deferred out of y's band-and-later (defect) or
  pre-placed before y (interleave). Any deferral rule that is monotone in R
  is automatically safe on the *other* side (if R(z) < R(y) then z is never
  deferred past y). The defect classes ≡ 2 mod 2^{k/2} are R-upper-sets of a
  shallow digit prefix, and the observed m≡3/m≡1 split shows the release
  order inside a defect is again R — so the interleave discipline should be
  formulated entirely in R-digit terms.
