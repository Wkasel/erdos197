> **SUPERSEDED — THE TARGET THEOREM IS KNOWN FALSE.**  The goal
> below ("S_A is 3-permutable") is refuted: S_A is PROVEN not
> 3-permutable (paper/main.tex thm:main; STATUS.md "Bottom
> line").  The L1 mechanism sketch ("removing the defect class
> breaks all cores") was independently refuted by notes/18 §0 (no
> thin-class removal restores feasibility at M ≥ 32).  (Review
> remediation notes/88 item 4.)

# Main theorem skeleton (the YES-program endgame)

## Target
**Theorem (goal).** S_A = ⋃_{k even} (2^{k−1}, 2^k] is 3-permutable.
(Then S_B = {1} ∪ ⋃_{k odd} blocks by the shifted-copy analogue + finite
patching ⇒ Erdős #197 = YES; LeSaulnier–Vijay's conjecture falls; β_ℕ(3) ≥ 1/3.)

## The construction (defect-law states)
For each even level k (comp = 2^k): D(comp) = {v ∈ (comp/2, comp]: v ≡ 2 mod
2^{k/2}} — the defect class (2·odd values, thinning). LawState(comp) := a
doom-free order of [S_A∩[1, comp]] ∖ D(comp).

Permutation = the increasing union of a chain LawState(4) ⊂ LawState(16) ⊂ ...
(each a time-prefix of the next). Fairness: v ∈ block k is placed by stage
k/2 + 1 ⇒ order type ω. ✓ automatic.

## The three lemmas
**L1 (subset escape).** For every level, the new block minus its defect,
(2comp, 4comp] ∖ D(4comp), is arrangeable under (a) + zone-(b) w.r.t. the fully
placed lower state. [Mechanism: the fatal zone kills full blocks; removing the
defect class breaks all cores — agent analyzing the exact algebra + hand rule.]

**L2 (defect release).** The previous defect D(comp) can be appended (in a
suitable internal order, interleaved into the delta) without dooms:
- upward completions 2r − x for x < r: land in (comp, 2comp] = odd block (free)
  or in (comp/2, comp]∩S_A: placed except D-siblings (handled by within-D order);
- downward completions 2r − u for placed u > r: land below r: placed except
  D-siblings (same handling).
[To verify precisely: interactions with the concurrently-placed new block.]

**L3 (assembly/induction).** L1's arrangement and L2's release compose into
LawState(4comp) extending LawState(comp): the delta = D(comp) ∪ (newblock ∖
D(4comp)) appended in the order [interleave per L1/L2]; all cross-delta and
delta-vs-state constraint families enumerated and discharged:
- state-pairs' completions: ≤ 2comp: in-state or odd-block. ✓ (established)
- delta-internal: L1 + L2 + their interleave conditions (the only open piece:
  new-block values' pairs with D-released values; compute the completion
  geometry: r ∈ (comp/2, comp], y ∈ (2comp, 4comp]: 2y − r ∈ (3comp, 8comp):
  odd block (4comp, 8comp] free; (3comp, 4comp] ⊆ new block: constraint z ≺ y —
  in-block, handled by L1's arrangement IF the interleave schedules D late
  relative to the affected y's... to pin down).
- delta-vs-future: completions ≤ 8comp land in the next odd block. ✓

## Status ledger
- Ladders (exact necessary): SAT at (16,d2)(16,d3)(64,d2); law-pinned SAT at
  (16,d2)(16,d3); law-d4 (horizon 4096) running.
- L1: agent on the algebra (notes/18 pending); SAT instances to verify.
- L2/L3: completion geometry drafted above; needs the interleave discipline.
- Failure modes to respect: all previous "laws" died at the NEXT scale;
  the d4 verdict is the canary. If d4 UNSAT: the law needs its own correction
  at depth 4 (defect within the defect? the P3-spillover in the mined data
  hinted the class fattens: ≡2 mod 16 PLUS part of ≡10 mod 16 at 1024).

## Audit + reconciliation (evening)
- law-d3 witness independently audited: 0 violations, 0 dooms, exact nesting,
  defect classes ≡2 mod 2^{k/2} with moduli 8/16/32 at scales 64/256/1024. LAW
  CONFIRMED with modulus formula m = 2^{k/2} exactly.
- Agent's Σ system (bottom-eighth-interval reservoir in the NEW segment,
  lag-2): UNSAT at X = 4..32 → dead at all scales. Its Prop 1 (new-segment
  reservoirs forced into bottom half) stands but is orthogonal: the LAW defers
  a thin class of the OLD top block — outside Prop 1's scope. No contradiction.
- Synthesis: append-only towers with new-segment reservoirs are dead (agent's
  program); the law's old-block-deferral is the surviving (and audited) shape.

## CORRECTED LAW (from notes/18, machine-verified M=32..128)
- L1 as originally posed (B∖D vs pre-placed zone) is FALSE for M ≥ 32.
- TRUE shape: whole-state arrangements [bulk | D_old | D_new] — deferred
  classes stack as ordered suffixes; the bulk includes the next block minus
  its defect (extras/lookahead ESSENTIAL — no-extras systems UNSAT everywhere).
- Invariant = CLASS COHERENCE (any single residue class works as the deferred
  suffix; random same-size sets never; "≡2" emergent not forced). Algebra:
  attacker maps φ_r(b) = 2b − r on Z/m are trees rooted at r ⟹ one class can
  be sink; full zones impose all m roots ⟹ cycles ⟹ fatal. Odd classes can't
  be last in the pure calculus (ψ-cycles) ⟹ range truncation needed.
- Remaining localized gap: the 2·odd phase closure (truncation argument) —
  the phase recurses to the odd kernel; proof = double induction over
  (scale, class-depth). Suffix-stacking order proven forced (reversed stacking
  UNSAT via a Lemma-R configuration).

## FINAL FORM (after notes/20): the ω-ification problem
- R (recursive digit expansion: odd→0 recurse (v−1)/2; ≡0 mod 4→1 recurse v/4;
  ≡6 mod 8→2 recurse (v−6)/8; ≡2 mod 8→3 recurse (v−2)/8) is a STATIC 3-AP-free
  linear order on S_A: 0 doom violations at N = 2^12..2^16 (43,690 values),
  explained by the exact REFLECTION LAW: at the first diverging digit of (x,y),
  z = 2y − x takes x's digit ⟹ R(z)<R(y) ⟺ R(x)<R(y).
- S_A thus stands to ω-orders as ℤ stood for Ardal–Brown–Jungić: static chaotic
  order exists; the question is ω-ifiability (HS-obstruction absent: no full rays).
- KEY NEW OBSERVATION (hand, tonight): inversion triples SELF-CLOSE: if the time
  order T inverts R on (x,y) (x ≺_T y, R(x) > R(y)), the required reflection
  z = 2y−x satisfies R(z) > R(y) (reflection law), and the new inversion (z,y)'s
  own requirement is x ≺_T y — already true. No regress; obstructions are only
  finite local conflicts among overlapping triples (cf. the observed greedy
  3-cycle 45→35→54→45).
- THE FINAL LEMMA (ω-ification): the closure system {for every T-inversion
  (x,y): z ≺_T y} admits consistent finite stages with fair enumeration.
  Equivalently: orient/schedule the inversion hypergraph acyclically at every
  scale. This is the whole of Erdős #197's dyadic side, in final coordinates.
