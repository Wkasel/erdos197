# Master assembly: the complete NO (skeleton, session 11)

Target: **Theorem (conditional assembly).** No partition of ℤ⁺ into two
sets has both parts 3-permutable — i.e. Erdős #197 = NO — modulo the
explicitly-tagged gaps below. This document is the dependency graph; each
node cites its proof or its gap tag.

## The dichotomy (N4, proven frame)
Fix a partition (A, B). For C ∈ {A, B} and window W_t = (M·8^t, M·8^{t+1}]
(disjoint tiling), classify:
- **Case 1** (some team, infinitely many 1-clean blocks): ∃ team T and
  infinitely many dyadic blocks where T's complement-within-block has size
  ≤ C₀ (bounded dust). [Anchor-free form per e121: ratio-2 windows, any
  anchor.]
- **Case 2** (everywhere-split): both teams' within-block presence → ∞.
Every partition is in exactly one case (frame: notes/43; anchor-free
restatement: notes/46 §4A).

## Case 1 kill chain
1. **C3(p) infinite hand family** [N2, notes from e122 session; status:
   diagonal lane machine-complete M=16..135 all residues, hand schema for
   5 pairs, 0 failures; GAP-N2: off-diagonal lanes (e124) + uniform hand
   proof of the family].
2. **Bounded-dust robustness** [N3: exact single-block tolerances d*=2/3;
   scale-stable; GAP-N3: one-paragraph hand extension of C3-PUNCT].
3. **T-PIN pigeonhole** [N1, proven]: fixed attacker pair at finite
   positions + infinitely many disjoint UNSAT windows ⟹ not permutable.
4. Assembly: in Case 1 the clean-block team owns some fixed pair
   {2^j−1, 2^j} (or a lane analogue) + infinitely many nearly-clean
   blocks; 1+2+3 ⟹ that team dead. [Needs: the pair-ownership argument —
   every team owns SOME adjacent pair unless all pairs split; if all
   split, the planted-half landing-pad structure fires instead (G3 family)
   — TAG: write this bridge precisely. GAP-BRIDGE1.]

## Case 2 kill chain
1. **The coupled 2-seam core** [N6]: balanced 3-block gadget UNSAT at
   M=16/24/32; absolute-bound schema: (2,2,2) UNSAT at M=48, 64
   (e125: 304s), M=80/96 running (e126). [GAP-N6a: all-M schema (hand,
   from the MUS anatomy — notes/48 in progress).]
2. **Window composition** [trivial, verified]: windows (M·8^t, M·8^{t+1}]
   tile; constraints are window-local; T-PIN-style pigeonhole applies to
   the window family.
3. **Everywhere-split ⟹ (2,2,2) eventually**: by definition of Case 2,
   both teams eventually have ≥ 2 in every block of every window. ✓
   definitionally.
4. **Double non-procrastination** [GAP-G2 — THE gap]: the core's
   hypothesis that both teams are block-ordered at both seams, at
   infinitely many window scales. Candidate routes: (i) generalize
   lem:normal (running-max chunking) — any permutable team WLOG
   block-monotone up to finite fibers; (ii) v*(M) violation-budget +
   L-PROC procrastination accounting. notes/47 in progress.

## Support layer (proven)
- lem:orbit + T-SHARP sharpness (kills doubling-supercritical teams
  directly — iid-like colorings die here; L1' concentration lemma for the
  subcritical remainder [GAP-L1': hand proof — measured true everywhere]).
- d_t law, Lemma NECK, seam 7-channel law (octave/stage-alternating
  shapes — subsumed by Case 1 once GAP-BRIDGE1 lands, kept as independent
  confirmation).
- Price ledger: supply lemma + p(k) → ∞ [GAP-p(k): needs N2-style schema;
  possibly dispensable if Case 2 closes via the seam core alone].

## Current gap inventory (2026-08-26)
| Tag | Statement | Type | Status |
|-----|-----------|------|--------|
| GAP-N2 | off-diagonal lanes + uniform family proof | hand+machine | e124 front running |
| GAP-N3 | dust-robust C3 | hand (short) | flagged one-paragraph |
| GAP-BRIDGE1 | pair-ownership/split dichotomy in Case 1 | hand | unwritten |
| GAP-N6a | all-M coupled schema | hand (from MUS) | notes/48 front running |
| GAP-G2 | double non-procrastination | hand (THE gap) | notes/47 front running |
| GAP-L1' | concentration lemma | hand | measured-true |

When every tag clears: Erdős #197 = NO. Any tag that BREAKS instead
(especially G2) re-opens a YES-shape with exact specifications.
