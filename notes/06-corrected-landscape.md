# Session 2: bug fix + corrected landscape (2026-08-24)

## Critical bug found and fixed
e3_sat.decide() conflated "lazy-transitivity rounds exhausted" (indeterminate) with UNSAT. Genuine UNSAT results remain sound (the encoding is a relaxation: its UNSAT implies real UNSAT), but several dramatic "UNSAT" findings were bogus. Re-verified after fix (decide now raises on indeterminate; batched triangle clauses):

STANDS (genuine UNSAT, fast solver proofs):
- Lemma F base cases M = 16..31 all UNSAT → **Theorem 1 stands** (with halving descent).
- Half-zones at M = 32 UNSAT (all four variants: lo/hi/evens/odds).
- Full zone UNSAT for M = 16..256.

OVERTURNED (were bug artifacts, actually SAT):
- Single-element zones at M = 32, 64, 128: SAT (verified orders). Blocks tolerate O(1)-size zones: measured tolerance ≈ 1–2 elements (prefix families), then UNSAT. So tolerance is a constant, not a fraction: still strong.
- Sub-block grid: bottom sub-blocks (M, M+W] with FULL zone are SAT for W ≤ M/2, UNSAT from W = 5M/8. Top sub-blocks (2M−W, 2M] SAT up to W = 3M/4.

## Strengthened impossibility
If every block is a contiguous run in the team's sequence (arbitrary interleaving of other blocks AROUND runs, any run order): when block K's run plays, ≤ 2 elements of block K−2 may be placed (tolerance), so block K−2 finishes after block K: f(K−2) > f(K) for all K — infinite descending sequence of finish positions. **Impossible.** (Theorem 1 upgraded: contiguous-run schedules die even with cross-block interleaving.)

## The pipeline analysis (hand)
- Top-half-first within a block: no descents allowed at all (reflections land in the unplaced bottom half) → ascending with gap-halving → ≤ log M elements. Dead.
- Bottom-half-first: completions (x ∈ zone, y ∈ bottom) land in the unplaced top half. Dead.
- So blocks must be scattered in ≥ 2 interleaved pieces with cross-scale timing.

## The interleaving games (all SAT — the local structure is winnable)
- G(M) (blocks K−2, K merged timeline, all necessary constraints): SAT for M = 16..256. Solutions organize by mod-4 classes.
- G3(M) (blocks K−4, K−2, K): SAT for M = 64..512.
- Currently testing: chained games with carried orders (block K's order reused as lower block of the next game).

## Team B reduces to Team A
S_B = {1, 2} ∪ 2·S_A. All completions 2w − 1, 2w − 2 for w in an odd block land in the next even block (team A's), except the boundary case x = 2, w = 2^{k−1}+1 → z = 2^k (block top, own team): a single extra sliver constraint per block. Hence: S_A permutable via a template with sliver slack ⇒ S_B permutable ⇒ **#197 = YES**. Everything rides on the S_A chain-template.

## Sliver inventory (debt for the eventual proof)
Zone from block K−2j constrains only y ∈ (M, M + M·4^{−j}]: j=1 the quarter (the main game), j≥2 the bottom 1/16, 1/64, ... — geometrically vanishing; templates should place block tops early enough to absorb.
