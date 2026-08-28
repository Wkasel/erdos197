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
4. Assembly: **DONE (notes/52, Theorem B1).**  The diagonal usable
   pairs {3p, 3p+1}, p ≡ 1 mod 4, fire on exactly the dyadic class and
   appear with density 1/12 in every block, so a C₀-clean block above
   scale 12C₀+25 always contains a fully-owned pair — the ownership
   branch holds unconditionally, the split branch is vacuous
   (SPLIT-QUANT: splitting punctures every block linearly, contradicting
   cleanliness), and the planned landing-pad descent provably has no
   well-ordering (notes/52 §4.3 — finite usable families admit a
   splitter fixed point; density is necessary).  Case-1 chain is now
   N1 + B1 + (GAP-N2-DIAG, GAP-N3); GAP-BRIDGE1 discharged.

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

## Current gap inventory (updated 2026-08-26 late, synthesis session)
| Tag | Statement | Type | Status |
|-----|-----------|------|--------|
| GAP-N2 | off-diagonal lanes + uniform family proof | hand+machine | largely EXECUTED (notes/49: {11,12} all 8 residues, lane laws, template cells 13..19); remains: PARAMETRIC-in-x lane proof, cells A4d(19)/B6(21), pairs x ≡ 7 mod 8.  PRIORITY UPDATE (notes/52): the Case-1 critical path needs ONLY the diagonal parametric sub-piece **GAP-N2-DIAG** (C3(p) write-up, p ≡ 1 mod 4, dyadic scales — e123's verbatim-schema claim); off-diagonal parametrics matter only for BRIDGE1-AF |
| GAP-N3 | dust-robust C3 | hand (short) | flagged one-paragraph, unwritten |
| GAP-BRIDGE1 | ~~pair-ownership/split dichotomy in Case 1~~ **DISCHARGED** (notes/52 Theorem B1: ownership always holds via diagonal density; split branch vacuous; e152_bridge1 checks pass) — residual dependencies are GAP-N2-DIAG (parametric diagonal, p ≡ 1 mod 4, dyadic only) + GAP-N3; anchor-free variant BRIDGE1-AF still open (needs off-diagonal parametrics) | hand | CLOSED modulo N2-DIAG/N3 |
| GAP-N6a | all-M coupled schema | hand (from MUS) | compute-true M=16..80 (e125+e126_deep, (2,2,2) critical from 48); M=32 MUS FINAL (n=116, ALL necessary, anatomy = seam anchors + both-parity B2 midband run — the reduction-to-N2 shape CONFIRMED, notes/48); M=48 support in flight |
| GAP-G2 | ~~double non-procrastination~~ REFRAMED: T-FORCE affordability — two Θ(M)-dense teams cannot both afford forced > v*(M) inversions at every anchor forever | hand (THE gap, ledger-type) | DNP as stated is FALSE (single-team, all budgets to N^{1−o(1)}, irreducibly two-sided — notes/47); FORMAL LEDGER THEOREM now drafted (notes/54: Theorem LT — demand side PROVEN modulo GAP-V*-schema/growth; supply side split into GAP-AFFORD with proven mechanism lemmas L-ORIENT/L-COMP/L-CASCADE + sub-tags GAP-COMP/GAP-JOINT; regime trichotomy formal with GAP-RHO/GAP-ALT; X-INTERLEAVE machine-verified to survive the accounting — e130 all-pass); pump measured only at v*(bal,16) ∈ [3,160], e128 bisecting |
| GAP-L1' | concentration lemma | hand | measured-true, unproven |

Note the STRUCTURAL simplification bought by the MUS landing: if the
M=48 support confirms the anchor-coordinate match, GAP-N6a's schema is
the N2 schema family (GAP-N2) applied one seam up plus one layer of
sumset forcing — the program then has ONE schema engine (Z/D/E/P
ladders + rung geometry) and ONE genuinely new statement (GAP-G2's
ledger) left, with everything else short hand write-ups.

When every tag clears: Erdős #197 = NO. Any tag that BREAKS instead
re-opens a YES-shape with exact specifications.  One tag DID break
this session — GAP-G2's original DNP form (X-INTERLEAVE refutes it) —
and the re-opened specification is exactly the notes/46 dodger corner;
the reframed tag above is what must now clear instead.
