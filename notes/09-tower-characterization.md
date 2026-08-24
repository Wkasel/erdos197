# The tower characterization (proved) — the problem's exact finite content

## Setup
Pure-complete-X system: arrangements of S_A ∩ [1, X] (X an A-block top) with (a) no monotone 3-AP and (b) every monotone-placed pair's completion, when in S_A∩[1,X], placed before the pair's later element. (Completions in (X, 2X] lie in an odd block: free. **Horizon collapse lemma:** values above X never help — deleting them from any valid arrangement preserves validity — so pure systems capture everything.)

## Facts
1. The restriction of any global 3-AP-free permutation of S_A to S_A∩[1,X] is a valid pure-complete-X arrangement. (Constraints are restriction-closed; completions of in-range pairs stay ≤ 2X.)
2. Pure-complete-X is SAT for X = 16, 64, 256, 1024 (1024: 108s, 682 values).
3. **Characterization.** S_A is permutable ⟺ there exists B: ℕ→ℕ such that for every X, the system [pure-complete-X ∧ ∀v: #predecessors(v) ≤ B(v)] is SAT.
   (⇒ take B(v) = position of v in the global permutation. ⇐ the restriction sets are finite and nested; König's lemma yields a consistent tower whose limit order has every v with ≤ B(v) predecessors, hence order type ω = a genuine permutation; constraints are local and inherited in the limit.)
4. **NO-criterion.** If d_X(v) := min over pure-complete-X arrangements of #predecessors(v) diverges as X → ∞ for some fixed v, then S_A is NOT permutable. Combined with partition rigidity (records force dyadic-like partitions), this is the concrete route to #197 = NO with machine-verifiable growth certificates.

## Corrected assessment of earlier evidence
- The two-block/three-block/odd-chain games admitted the degenerate "lower block last" solutions (cannot assemble: infinite descent) — that evidence was weak. What stands: pure-complete truncations exist; all STRUCTURED extension schemes (contiguous, two-phase pipelines at every split ratio s ∈ {5/4, 4/3, 7/5, 3/2, 8/5}) are UNSAT for m ≥ 32.
- The problem's difficulty is exactly the fairness/order-type-ω condition — invisible to any single finite SAT instance, but exactly captured by the growth of d_X(·).

## Measurements in progress
d_X(3) for X = 16..1024; then max over v ≤ 16 of d_X(v), and d_X at block bottoms/tops (where hand analysis predicts pressure concentrates).
