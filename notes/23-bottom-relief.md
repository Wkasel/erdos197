# The (A)-characterization: bottom-half relief (session 5, late night)

## Theorem ((A)-clean deferrals).
Work in the stage frame: s(v) = block(v)/2 + δ(v), δ ≥ 0. Recall L-same-block
(notes/22): in any S_A AP triple (x,y,z) the middle y and top z share a block.

**Claim.** Suppose each block k defers a set D_k with uniform delay δ_k ≥ 1
and D_k ⊆ (2^{k−1}, 3·2^{k−2}] (the bottom half). Then condition (A) holds:
no AP triple has strictly monotone stages.

*Proof.* A strict pattern needs s(x)<s(y)<s(z) (or the mirror). Since y,z share
block k: s(y)≠s(z) forces exactly one of y,z deferred.
(i) z ∈ D_k, y ∈ bulk: y = (x+z)/2 with x ≤ 2^{k−2} (a lower even block; if x
is in block k the pattern has ≤2 stage values in {s, s+δ}, not strict). Then
y ≤ (2^{k−2} + 3·2^{k−2})/2 = 2^{k−1}, and y > z/2 > 2^{k−2}: so y lies in
the ODD block (2^{k−2}, 2^{k−1}] — not in S_A. No such triple exists.
(ii) y ∈ D_k, z ∈ bulk: s(y) > s(z), so the increasing pattern fails at
y<z-stage; the decreasing pattern s(z)<s(y)<s(x) needs s(x) > s(y) with x in a
block ≤ k − even if x is deferred, s(x) ≤ (k−2)/2 + δ_max; alignment δ_k ≥
δ_{k−2} − 1 kills it — with uniform δ ≡ 1 it's automatic (s(x) ≤ k/2 = s(y)−1
+1 = s(y), not >). Mirror cases symmetric. ∎

Conversely: deferring any z in the TOP half (z > 3·2^{k−2}) creates the strict
pattern (x, (x+z)/2, z) with a genuine in-team witness midpoint (the analysis
of notes/22: witnesses exist exactly when z > 3·2^{k−2}) — unless the witness
midpoints are themselves deferred to ≥ s(z), which cascades into bulk-scale
deferrals (machine: e64's 366–1825 violations for the ≡2-class laws).

**So in the rigid stage frame, the relief valve must live in the bottom half.**

## The fiber systems (all that remains)
fiber_s = (block 2s ∖ D_{2s}) ∪ D_{2s−2}, with:
- [F1] x at stage < s, y ∈ fiber, z = 2y−x ∈ fiber (same block as y):
  forced z ≺ y ("completions first").
- [F2] pair (x,y) in fiber∩block 2s with z = 2y−x ∈ D_{2s} (deferred):
  forced y ≺ x (ascending relief).
- [F3] pair (x,y) ⊆ D_{2s−2} with z = 2y−x landing in bulk of block 2s−2
  (already placed at stage s−1): forced x ≺ y.
- [T] in-fiber AP triples non-monotone.
Fibers independent; each finite. D_k = relief valve breaking [F1]'s fatal
chains at the cost of [F2] constraints.

## Depth-2 note
Multi-level deferral (D¹_k delay 1, D²_k delay 2, both ⊆ bottom half) stays
(A)-clean across blocks by the same proof, but adds in-block class conditions:
no in-block triple with stages (s, s+1, s+2) monotone — i.e., no AP
(bulk, D¹, D²) ascending or (D², D¹, bulk) with the value-order aligned.
This is the [bulk | D_old | D_new] suffix-stacking shape in stage language.

## Searches running
- e65 m=4/m=5: CP-SAT minimize |D| over bottom-half delay-1 reliefs.
  INFEASIBLE at 256 would prove delay-1 insufficient → depth-2 next.
- e61 m=5 (unconstrained window-2) still racing on fleet2 + local.
