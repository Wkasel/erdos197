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
