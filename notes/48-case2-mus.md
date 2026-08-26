# 48 — FRONT MUS: the balanced-core anatomy (deletion-minimal supports of the Case-2 coupled cores)

GOAL (post-merge ordering, STATUS "Decisive next experiments" #1
prerequisite): extract the deletion-minimal SUPPORTS of the two firing
Case-2 cores —

- the (3,3,3)@M=32 constant-bound core (the "balanced" 2-seam core of
  notes/45 Part C3; the earlier e120c3_mus run died at n=118 of 224),
- the (2,2,2)@M=48 critical-constant core (the exact dichotomy floor:
  (2,2,2) UNSAT, (1,1,1) SAT at M=48),

then compare the two anatomies in ANCHOR COORDINATES (offsets from
block ends + midband) to read off the hand schema for the sumset/range
lemma behind the Case-2 core.  Escape anatomy already known (notes/45):
every machine escape is a sumset dodge — minority pinned at the bound
on a mod-4 lattice (2Y − U all even ⇒ the odd half of B2 is safe), or
range-hidden in B1's bottom quarter (2y − u ≤ 8M/4 never reaches B2);
bounds ≥ (3,6,12) kill every dodge.  The MUS should show WHY as a
finite pattern: which window values are load-bearing for "a small
minority cannot keep 2Y − U off itself at two seams simultaneously".

Tooling: experiments/e126_case2_mus.py — same chunked greedy deletion
as e120c3_mus (descending values, vacuity guard: every block keeps
≥ 2·bound + 2 values so cardinality-vacuous UNSAT is impossible;
Glucose42 re-verification; per-value criticality certificate) but
CRASH-SAFE: the surviving support is snapshotted to
data/e126_mus_M{M}_b{bounds}.resume.json after every successful drop
and reruns resume from the snapshot.  Ends with the anchor-coordinate
anatomy dump (per block: bottom offsets v − lo, top offsets hi − v,
midband offsets v − mid, mod-4 residues).

Runs (launched 2026-08-26, this session):

    .venv/bin/python experiments/e126_case2_mus.py 32 3 3 3 32   # → data/e126_mus_M32.log
    .venv/bin/python experiments/e126_case2_mus.py 48 2 2 2 64   # → data/e126_mus_M48.log

(Concurrently: e125_m64_stability.py — the (2,2,2)@M=64 G1 probe —
still running from the previous session, data/e125_m64.log.)

## Questions the anatomy must answer

1. Which bottom-midpoint anchors survive?  The single-block N5 escapes
   always hinged on {M+2, M+4(, M+5)}; the C3 zigzag anchors are bottom
   midpoints too.  Do the coupled cores keep the same anchor family in
   B0, or move to B1 (the sandwiched block)?
2. Is the surviving support concentrated on the mod-4 lattice classes
   that power the sumset dodge (the escape needs 2Y − U to miss C ∩ B2 —
   the core should retain exactly the values that make every lattice
   alignment fail)?
3. Is B2 support top-half-only (the range dodge hides in B1's bottom
   quarter because 2y − u then undershoots B2 — the core should retain
   the B2 values that remain reachable, i.e. the bottom of B2, plus the
   B1 values that reach them)?
4. Scale transfer: do the M=32 and M=48 supports agree in anchor
   coordinates (offsets from block ends), the way the N2 catalogues were
   scale-stable verbatim?  If yes, the support IS the schema candidate;
   if no, the schema needs midband-proportional anchors (like C3's
   flood centres at 3M/2).

## Result 0 (pre-MUS, e126c): the schema CANNOT be pure sumset — and
## what it must be instead

Diagnostic experiments/e126c_pure_sumset.py: 2-color the support with
per-block bounds forbidding monochromatic CROSS triples only (no order
variables).  **PURE-SUMSET is SAT at both targets** ((3,3,3)@M=32,
1280 cross triples; (2,2,2)@M=48, 2880 cross triples;
data/e126c_pure_M{32,48}.log) — necessarily so, because the
cross-triple hypergraph has degree-0 zones:

- max z = 2·(4M) − (M+1) = 7M − 1, so B2's top eighth (7M, 8M] is
  UNREACHABLE by cross triples (33 values at M=32);
- y ≤ (4M + M)/2 + O(1): B1's bottom values undershoot B2 entirely
  (z = 2y − u ≤ 4M), a degree-0 bottom zone in B1 (16 values at M=32).

So "a small minority cannot keep 2Y − U off itself" is FALSE at the
pure level at every scale: park the B2 quota above 7M and/or the B1
quota in the bottom zone (the machine's range-hide dodge, exactly as
notes/45 recorded).  **The order theory is load-bearing, and the pure
witness shows precisely where**: the decoded M=32 dodge gives minority
B = {62,63,64} ∪ {93,94,95} ∪ [129,223] — i.e. the dodging team is
forced to hold a ~95-value CONSECUTIVE interval in B2 while its B1
values {93,94,95} sit seam-forced EARLY below it.  That is verbatim
the generic-pair chain-rung geometry (notes/42 §4b: a pair {x, x+1}
placed early below a long consecutive run kills it — N2's single-block
collapse).  The correct hand-schema shape is therefore a DICHOTOMY,
not a sumset lemma:

> **Schema target (revised).**  Under double non-procrastination with
> per-block bounds, every coloring either (a) contains a monochromatic
> cross triple (dies by the seam forcing), or (b) range/lattice-hides —
> and every hide RECREATES a generic-pair rung one seam up (the hidden
> team's low-block members become fixed early attackers on its own
> consecutive B2 material).  Case (b) is N2-schema territory: the
> coupled core is the N2 generic-pair core WRAPPED in one layer of
> sumset forcing.

If the MUS supports confirm this (retained B2 support = a long run
below 7M + its B1 attackers + B0 seam anchors), Case 2's crux
literally REDUCES to the Case-1 crux (N2's C3(p) family + off-diagonal
lanes) plus the seam hypothesis — one schema, both cases.

Second probe (data/e126c_pure_reachable.log): excluding the degree-0
zones (support = cross-reachable values only, n = 175/263) the pure
level is STILL SAT — the PARITY/LATTICE dodge takes over (z = 2y − u
preserves u's parity, so "minority odd in B0, even in B2" kills every
mono cross triple arithmetically; decoded witnesses at both scales are
exactly this).  So BOTH known escape families are pure-level-immune,
each for its own arithmetic reason, and the order theory is what kills
each: the range-hide hands the dodger consecutive runs attacked by
gap-1 pairs (chain rung verbatim), the lattice-hide hands it gap-2
pairs + long mod-2/mod-4 lattice runs — the SAME rung after halving
(dividing a gap-2 lattice by 2 maps it to the gap-1 consecutive
geometry).  Prediction for the MUS anatomies: the retained support is
a UNION of (i) seam-anchor values in B0/B1 realizing the cross-triple
forcing, and (ii) enough of B2's midband (below 7M) in BOTH parities
to make every lattice/range hide recreate a rung — and the M=32 vs
M=48 agreement should be in BOTTOM-offset coordinates for (i) and
proportional (midband) coordinates for (ii).

## Results

(pending — filled in as the runs land; supports snapshotted in
data/e126_mus_*.resume.json, finals in data/e126_mus_M{32,48}*.json)
