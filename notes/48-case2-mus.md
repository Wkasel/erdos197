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

## Results

(pending — filled in as the runs land; supports snapshotted in
data/e126_mus_*.resume.json, finals in data/e126_mus_M{32,48}*.json)
