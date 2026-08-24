# Erdős #197 — Sources and first structural insight

**Problem.** Can ℤ⁺ be partitioned into two sets, each of which can be permuted (as a one-sided infinite sequence using all its elements) to contain no monotone 3-term AP as a subsequence?

Source: DEGS = Davis, Entringer, Graham, Simmons, *On permutations containing no long arithmetic progressions*, Acta Arith. 34 (1977) 81–90 (`papers/DEGS77.pdf`). Restated Erdős–Graham 1979 p. 338 ("very annoying question"), = erdosproblems.com #197.

## Extracted facts from DEGS77

- **Fact 1.** M(n) = # of 3-AP-free permutations of [n] satisfies M(n) ≥ 2^{n−1}; via doubling maps A ↦ (2A)(2A−1) and (2A′)(2A). Parity trick: endpoints of a 3-AP share parity. Table of M(n) up to n=20 on p. 82 (matches OEIS A003407).
- **Fact 2.** M(2n−1) ≤ (n!)², M(2n) ≤ (n+1)(n!)². Proof mechanism: element a_i with ⌈(n+3)/2⌉ ≤ a_i ≤ n forbids a placement of n+1 (the trio n+1, a_i, 2a_i−n−1). **This "each big element blocks a slot for the newcomer" counting is a quantitative version of the obstruction — potentially reusable for a 2-set impossibility argument.**
- **Fact 3 (𝒮₃ = ∅).** Every permutation of ℤ⁺ contains an *increasing* 3-AP. Proof: a₁ first element; a_i first element > a₁; then 2a_i − a₁ > a_i is somewhere, and everything before position i is < a₁ < 2a_i−a₁, so it is after position i. Trio (a₁, a_i, 2a_i−a₁). ∎
  - **Leverage for #197: the proof consumes the fact that the completion 2a_i−a₁ lies in the SAME sequence. In a 2-partition the completion may belong to the other part. The whole game: can two sets absorb each other's completions forever?**
- **Fact 4 (𝒮₅ ≠ ∅).** Interval blocks of length 10^k arranged B₀*A₀*B₁*A₁*… beat monotone 5-APs (large-gap growth argument).
- **Fact 5 (𝒟₃ = ∅).** Doubly infinite arrangements of ℤ⁺ still contain monotone 3-APs. Proof #1 (Folkman): parity/induction on index comparisons — relation (4): A(a) < A(a+d) iff A(a+2md) < A(a+d+2md) and A(a+(2m+1)d) > A(a+d+(2m+1)d). Establishes A(a) < A(a+d) for all odd a,d by induction, then finds increasing 3-AP among evens. **Folkman's index-relation formalism (position function A(·), parity of multiples of d) is a reusable proof engine.**
- **Fact 6 (𝒟₄ ≠ ∅).** Blocks B_{i+1} = (2B_{2i})′(2B_{2i}+1)′ doubling construction: doubly infinite permutation of ℤ⁺ with no monotone 4-AP.
- **Remark 2.** Nathanson: mod-n analogues; permutations of [n] avoiding 3-APs mod n exist iff n = 2^r.
- **Remark 3 (THE 3-set construction).** A₁ = [1,100], |A_{k+1}| = ⌈(3/2)|A_k|⌉, consecutive intervals. 𝒜 = A₁*A₄*A₇*…, ℬ = A₂*A₅*A₈*…, 𝒞 = A₃*A₆*A₉*… each block internally 3-AP-free. "Easily checked."
- **Remark 4.** Which infinite A ⊆ ℤ⁺ admit a 3-AP-free permutation ("permutable" sets)? DEGS ask for sup liminf and sup limsup of density of permutable sets — **directly relevant: if every permutable set had upper density < 1/2, the answer to #197 is NO.** Modern work: Geneson 2018 (arXiv:1803.06334), LeSaulnier–Vijay Discrete Math 2019 study exactly this.
- **Remark 5.** ℤ version: only preliminary results (no monotone 7-AP achievable).

## First insight: why 3 works and 2 is exactly marginal (derived 2026-08-23)

Generalize Remark 3: intervals with geometric size ratio r > 1 (so cumulative maxima S_k ≈ C·r^k), dealt round-robin to s teams (team gets blocks k, k+s, k+2s, …), each block internally 3-AP-free. The two conditions needed to kill cross-block increasing APs within a team:

1. **Completions must overshoot the current block.** For x from a team block ≤ A_{k−s} and y ∈ A_k with x < y, need z = 2y − x > max(A_k) whenever z would land in A_k after y. Worst case: 2·min(A_k) − max(A_{k−s}) > max(A_k), i.e. 2·S_{k−1} − S_{k−s} > S_k. Geometric: **2r^{s−1} − 1 > r^s**.
2. **Completions must undershoot the team's next block.** For x < y both in team blocks ≤ A_k: z = 2y−x < 2·max(A_k) ≤ min(A_{k+s}), i.e. 2S_k < S_{k+s−1}: roughly **r^{s−1} ≥ 2**.

- s = 3: need 2r² − 1 > r³ and r² ≳ 2. At r = 3/2: 2(2.25) − 1 = 3.5 > 3.375 = r³ ✓ (barely! slack 0.125) and r² = 2.25 ≥ 2 ✓. This is exactly DEGS's choice — and it is tight, which explains the odd-looking ratio 3/2.
- **s = 2: conditions become 2r − 1 > r² ⇔ (r − 1)² < 0. IMPOSSIBLE for every r.** The boundary case (r−1)² = 0 is equality — the construction fails *marginally*, not badly.

**Consequences.**
- No interval-block round-robin construction with any growth rate can solve #197. Any YES answer needs genuinely different structure: non-interval sets (e.g. parity/digit classes), non-geometric growth, or blocks engineered so the marginal equality cases (z exactly = max, arising when d ≈ y − x with x near the previous block's top) are killed by the *internal ordering* of blocks rather than by size gaps.
- The marginality suggests the problem sits on a knife edge (consistent with 1 impossible / 3 possible). Both directions remain live.
- Next: (a) read Geneson 2018 + LeSaulnier–Vijay for permutable-subset criteria and density bounds; (b) formalize the "completion pressure" bookkeeping from Fact 2/Fact 3 for two interacting sequences; (c) experiment: search for 2-partitions of [1,N] into sets that are "prefix-extendable" in a strong online sense, and for self-similar candidates (parity-like, base-3-like splits) test cross-completion structure.
