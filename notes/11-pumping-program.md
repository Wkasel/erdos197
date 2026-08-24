# The pumping program (2026-08-24, late night)

## Where the construction hunt stands
Every explicit closed-form key failed on a residue of pairs (bulk/reservoir splits,
round-keys with quarter deferral: each fix exposes the next braid-level coupling).
The SAT witnesses braid blocks within class-phases at fine granularity. Two
possibilities remained: (i) finite successes are tail artifacts (top blocks absorb
conflicts; the infinite problem has no tail) → NO; (ii) genuine self-similar
solutions exist → YES via pumping.

## The self-similar test
Add to pure-complete-X the exact scale-invariance: u ≺ w ⟺ 4u ≺ 4w (whenever all
four values ≤ X in S_A). This kills the tail-freedom (the top block's internal
order = scaled copy of inner blocks').

**Result: self-similar pure-256 is SAT** (109s; witness saved; class-phase order
[6,2,0,4,3,7,1,5] — another self-absorbing mod-8 order; blocks braided within
phases). selfsim-1024 running.

## Pumping theorem (sketch; to be made rigorous)
Given a self-similar witness on two consecutive scale-layers:
1. Define the infinite order by pumping (the pattern of how non-multiples-of-4
   interleave with the scaled skeleton, applied at every scale).
2. Constraint transfer: any potential violating triple (x, y, z) at high scale
   with x divisible by 4 maps down by invariance to a verified triple. Triples
   with x not divisible by 4 have y within O(x) of a block bottom — O(1) special
   values per scale, whose treatment is itself scale-invariant → one verification
   covers all scales (boundary lemma).
3. Fairness (order type ω): pos(4v) ≈ scale-factor·pos(v) if the pattern inserts
   new values at bounded rate before any fixed element — measurable from the
   witness; geometric convergence expected.
Then S_A is permutable; with S_B = {1,2} ∪ 2·S_A (mirror + finite patch), the
Erdős–Graham problem #197 resolves YES — refuting the LeSaulnier–Vijay
conjecture.

## Status: awaiting selfsim-1024. If UNSAT: the tail-artifact interpretation
wins, and the same machinery (restriction of hypothetical global solutions is
"eventually self-similar"?? — NOT automatic; would need new ideas) — NO would
still not be immediate. If SAT: proceed to extract the pattern, verify the
boundary lemma, and write the pumping proof.

## CORRECTION (Team B)
Earlier notes claimed S_B = {1,2} ∪ 2·S_A. FALSE: 2·S_A gives only the even
values of S_B's blocks. Correct statement: S_B = {1} ∪ (odd-indexed dyadic
blocks) is structurally identical to S_A shifted one dyadic level. The
construction/machinery transfers by the same arguments (all scale-shifted), but
S_B needs its own (analogous) self-similar witness and boundary lemma — parallel
work, not a free ride. Notes 06/09 claims to be corrected in the paper.
