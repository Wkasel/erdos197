# Field update + the unbalanced-partition idea (2026-08-24 morning)

## External development (found via #196 forum, posted Aug 18 2026)
Geneson, "Density bounds for permutations avoiding monotone APs"
(arXiv:2608.12604, Aug 12 2026): proves α_N(3) ≥ 2/3 (and α_Z(3) ≥ 2/3),
DISPROVING the LeSaulnier–Vijay tightness conjecture; also β_Z(4) = 1.
- His 2/3-construction is NOT the dyadic set: blocks of quadrupling intervals
  with rapidly growing scales — limsup 2/3, liminf → 0. Key tool = total
  AP-separation between old content and new blocks (his Lemma 3.1), plus the
  same binary/vdC rank machinery we rediscovered (his Lemma 2.1 ≡ our
  absorption theorem in interval form; cites Nathanson + Ardal–Brown–Jungić +
  Hirose–Saito [check this last one]).
- Impact on #197: the density obstruction to YES is weakening (α+β ≥ 2/3+1/4
  already; exact values open). The community's NO-lean loses its main basis.
- Competitive pressure: Adenwalla, Geneson actively publishing in this exact
  niche THIS MONTH. Our structural results (fragility, Theorem 1, tower
  characterization) are at real scoop risk. User chose to keep hunting.

## The unbalanced-partition idea (new, from Geneson's slack principle)
Our Theorem 1 killed contiguous blocks at every FIXED ratio; ray-piercing
forces alternation but NOT bounded ratios. With N_{k+1}/N_k → ∞
(A = ⋃(N_k, 2N_k], B = complement):
- A's in-team zone pressure = vanishing slivers (relative size N_k/N_{k+1});
- B's in-team pressure = slivers across huge gaps;
- B's long intervals: DEGS-style record analysis climbs to the top half in
  log-many steps — no obstruction found by hand.
Criterion: if the pure systems for A and B become ROBUSTLY SAT (radius 1) —
fragility gone — the pumping/assembly obstacle disappears and #197 = YES is
within reach via slack constructions. Tests running (note: B's first test run
has an optimistic horizon; re-run exactly if SAT. If robust-UNSAT persists,
retry with robustness required only above the finite head).
