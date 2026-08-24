# Correction: fragility reinterpreted (2026-08-24)

Baseline test (should have run first): plain intervals [1,n] are robust(r=1)-
UNSAT from n = 8. Radius-1 robustness fails EVERYWHERE in 3-AP-arrangement
problems — including settings where infinite constructions are known (DEGS
5-AP). Therefore:
- "Universal fragility" is a generic feature of these constraint systems, NOT
  evidence about #197's answer, and NOT a valid obstruction to pumping (pumping
  schemes need drift-tolerance only on the thin far-pair constraint families,
  not all triples).
- Paper section to be rewritten: the correct statement is the (true, weaker)
  "no Lipschitz-type placement rules"; the sweeping anti-pumping inference is
  withdrawn.
- The unbalanced-partition robust-UNSAT (team A, 5s) is likewise uninformative.

## Where this leaves the hunt (clear-eyed)
All roads converge on ONE question: does the transition pattern between scales
stabilize to something finitely describable (uniform YES-construction), or can
an infinite priority-style construction with a maintainable invariant be built
(non-uniform YES), or does every invariant necessarily fail (NO)?

## New program: invariant search (the classic method for such problems)
Goal: an invariant I on finite prefixes s.t. (i) base: some I-prefix exists;
(ii) maintenance: every I-prefix, for every duty (least-unplaced value), has a
one-step extension placing needed values keeping I; (iii) I implies
doom-freeness. Then the infinite permutation exists by induction (and fairness
is built into the duty schedule). DEGS Fact 4 = exactly this shape.
Candidate invariant ingredients (from our measurements): complete-below-X +
one-residue-class reservoirs per active block (g-witness profile), class-phase
discipline (vdC self-absorbing orders), top-run supports.
Test method: encode maintenance as bounded SAT checks (for-all duties sampled;
exists-extension solved), iterate on invariant design against counterexamples.

## The viability hierarchy (clean formalization of the invariant method)
State_c(X) := doom-free orders of [complete-X + partial overhang extending c
blocks up, with prescribed occupancy fractions]. Chains of State_c's (restriction
semantics) with the duty schedule give SUFFICIENT conditions for S_A-permutability
(fairness is built into the state shape: v placed by stage ~ log v). The
hierarchy over c (overhang depth) converges to the true tower characterization.
Program: find the smallest c and occupancy profile whose states chain
empirically; then prove the ∀-extension lemma at that c by hand (delta-analysis
with the class/absorption machinery). Current: c = 1 with 7/8-occupancy
(free reservoir) under test (e44).
