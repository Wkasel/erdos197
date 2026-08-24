# The skeleton theorem (session 5, night)

## Mined closed form (e61, N=256, OPTIMAL total-delay=41)
Undelayed skeleton per block: C_2 = {12,16}, C_3 = {48,56,64}:
**C_s = 2^s · [3·2^{s−2}, 2^s]** — multiples of 2^s in the top quarter
[3·4^{s−1}, 4^s] of block 2s. |C_s| = 2^{s−2}+1 (√-sparse skeleton).
Prediction for N=1024: C_4 = {192, 208, 224, 240, 256}.

## Structural lemmas (hand-proved tonight)
**L-same-block.** In every AP triple (x,y,z), z=2y−x, inside S_A: y and z lie
in the SAME even block. (z < 2y ≤ 2^{ky+1}; block ky+1 is odd.) So x is the
only element that can sit lower. Immediate corollary: if the per-block delay is
uniform (single δ_k for all non-skeleton), in-block triples see ≤ 2 distinct
stages → condition (A) holds automatically within blocks.

**L-escape (the heart).** If y ≥ 3·4^{s−1} (top quarter of block 2s) and
x ≤ 4^{s−1} (any lower even block), then z = 2y−x ≥ 5·4^{s−1} > 4^s: the
completion ESCAPES into the odd block (4^s, 2·4^s] — out of team, free.
(Margin: y ≥ 2.5·4^{s−1} suffices — the top 3/8.) Hence a skeleton value can
sit at its natural stage with lower stages arbitrary: upward completions of
(lower, skeleton) pairs never land in S_A. This is WHY the skeleton is the
top quarter: it is exactly the set immune to the (A)-danger that forces
everything else to delay.

**L-grid.** C_s is 2^s·(integer interval); pairs within C_s have downward
completions on the 2^s-grid (x = 2y−z ≡ 0 mod 2^s) — landing on lower
skeleton-chain values or out; internal structure ≅ a plain integer interval
(finite, always arrangeable, DEGS).

## Consequences for the stage program
- (A) reduces to δ-rule bookkeeping across neighboring blocks (window
  alignment); no danger cases remain given uniform per-block δ and L-escape.
- Everything else is (B): fiber s+... = C_{s+1} ∪ debris(block 2s) [∪ deeper
  debris?] must be orderable with forced pairs. The δ rule (how debris
  spreads over later stages) is being mined at N=1024 (e61 m=5, local +
  fleet2 race).
- Then: closed-form fibers are self-similar ×4 → (B) for all s by induction
  = S_A permutable; S_B analogous (same magic: odd-block completions land in
  even blocks); finite patching ⇒ **Erdős #197 = YES**.

## Status
- e61 m=5 running (local + fleet2). minladder d=3 local, d=4 fleet2.
  law_16_4 (pod1), law_64_3 (fleet2+5), ladder_256_2 (fleet5) still solving.
- Fleets 3/4/6 stopped. Annealers on fleet2 killed (cores to CP-SAT).
