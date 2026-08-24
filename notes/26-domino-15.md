# The value-15 domino (session 5, deep night)

## Machine facts
- MUS of window-1@256 infeasibility (deletion-shrunk, e72): **{15}**.
  I.e., in window-2 space at N=256, capping δ(15) ≤ 1 alone is already
  UNSAT: every window-2 scheme at 256 has δ(15) = 2. At 64 the optimum
  had δ(15) = 1. Conjecture: δ(15) ≥ m−2 at horizon 4^m.
- Pending: free-space (δ ≤ 8) version at 1024 (e74: δ(15) ≤ 2, rest free).

## Hand analysis of 15's role
15 ∈ block 4, top half (15 > 12 = 3·2^2) ⇒ by the bottom-half
characterization, deferring 15 is (A)-expensive: its witness triples
(3,9,15), (9,12,15), (11,13,15), (13,14,15) have in-team midpoints, so
s(15) > s(9) etc. forces 9 (bottom half, clean) or 3 up along with it —
a finite upward chain, but one that RECURSES as 15 climbs.

Attack structure (why every scale needs 15 displaced): for EVERY even block
k, the pairs (15, y) with y ∈ (2^{k−1}, 2^{k−1} + 15/2) have completions
z = 2y − 15 ∈ (2^k − 15, 2^k), odd values in the top sliver of the SAME
block — in team. If s(15) < stage of that block's bulk, each such pair
forces z ≺ y (completion-first): seven top-sliver-odd values pinned before
seven bottom-sliver values, at every scale above 15's stage, forever.
Small odd values x generally attack every block's bottom sliver with
⌊(x−1)/2⌋ pairs; 15 is the smallest with attack multiplicity 7, which is
apparently what tips the fiber systems over (3, 9, 11, 13 attacks alone
are absorbable).

## The NO-program via the domino
Target Lemma D: for every finite-fiber stage function, δ(15) must exceed
w at horizon 4^{w+2} — then no infinite scheme exists (δ(15) is a fixed
finite number), and by the EXACT chunk reduction, S_A is not 3-permutable.
The dyadic partition would be dead (LeSaulnier–Vijay-style route to a
2-partition YES via dyadic blocks fails); #197 itself then needs either a
different partition family or the mirror argument on both teams.

Proof obstacles: the fiber receiving the 15-attack depends on the scheme
(could be a huge merged chunk); need a scheme-independent UNSAT core
combining the 15-attack with unavoidable in-block structure. The free-space
MUS at 1024 (pending) will show what conspires with the attack.

## Alternative reading (YES-side)
If free-space at 1024 is feasible with δ(15) ≤ 2, the divergence is a
window-2 artifact and displacement growth can be spread across values —
the triangular schemes revive with 15-class stragglers absorbed higher.
