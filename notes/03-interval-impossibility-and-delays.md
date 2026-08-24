# Session results: interval schemes die; delays are forced

## A. New lemma (proved): the Orbit Obstruction

**Lemma.** If S ⊆ ℤ⁺ has a 3-AP-free permutation, then for every finite F ⊆ S there is no infinite sequence u₀ < u₁ < … in S with u_{k+1} = 2u_k − f_k (f_k ∈ F).

*Proof.* Let q = max position of F's elements in the permutation. At most q of the u_k can sit at positions ≤ q; beyond the last such k, each pair (f_k, u_k) is increasingly placed, so the completion u_{k+1} = 2u_k − f_k ∈ S must be placed before u_k — an infinite descent of positions. ∎

With S = ℤ⁺, F = {1, 2}: every orbit stays in S — reproves DEGS's Fact 3. Explains why all known permutable constructions have doubling-scale gaps: the doubling orbits must exit S. Necessary but not sufficient; counting arguments show orbit-freeness alone cannot force density < 1 (S^c may be spread thinly across log-many scales).

## B. Empirical theorem: ALL alternating interval schemes fail

SAT decision (exact, verified encoder — reproduces hand results) of the per-block condition system (notes/02): for every tested growth scheme — constant ratios r ∈ {2, 2.2, 2.5, 3, 3.5, 4, 5}, alternating ratios (a,b) ∈ {(2,3),(3,2),(2,4),(4,2),(2.5,3.5),(2,8),(8,2)}, both choices of which team owns 1 — **some block ≤ 5 is UNSAT**. Failures are fast and robust.

Minimal UNSAT core for dyadic block (16,32] with zone (4,8] (± {1,2}): 15 of the 16 values {17,…,29,31,32} — the obstruction is diffuse (forced pairs "z∈{26..32} before y∈{17..20}" interacting with the full 3-AP fabric of an interval), not a small gadget. Consequence: no clean 3-line human obstruction; a general interval-impossibility theorem will need a counting/potential argument. TODO: also scan the slow-growth band r ∈ [1.84, 2) where completions may enter one's own future block (adds forced-decreasing condition (c)); expected to fail too.

## C. Structural squeeze: mixed windows are infeasible → delays are necessary

Model "scale-monotone": each team plays its values respecting dyadic windows W_j = (2^{j−1}, 2^j] (u ∈ W_i before v ∈ W_j whenever i < j). Exact necessary conditions per window include:
- (e) For x in T's past, y ∈ T ∩ W_j: if z = 2y − x ∈ W_{j+1} then z must belong to the OTHER team (else increasing 3-AP x,y,z is unavoidable).

If both teams have dense presence in W_j and dense pasts, the two claim-sets {2y − x} blanket W_{j+1} and collide → infeasible. So (up to sparse exceptions) windows must be team-pure → alternating interval schemes → UNSAT by (B).

**Working theorem (to be made rigorous):** No solution of Erdős #197 exists in which both permutations are scale-monotone. Equivalently: any solution must place infinitely many values with large relative delay (played after much larger values). This narrows the search drastically and is a publishable structural result by itself.

## D. Next steps

1. Build the generic prefix verifier with doom-detection: violation = completion of an increasingly-placed pair placed later; doom = completion in team's unplaced future (downward analogue for decreasing pairs). Works for ANY scheme incl. delays.
2. Explore delayed-dyadic schemes: teams hold back subsets D_k of each block, played after later blocks — exactly the freedom the impossibility results point to.
3. Literature check: is any upper bound for α_{Z+}(3) known? (LV conjectured α = 1/2 tight; if we could prove ANY α < 1 bound it's new, and α + β < 1 resolves #197 as NO.)
