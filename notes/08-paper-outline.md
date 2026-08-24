# Paper draft outline: "Structural rigidity in the Erdős–Graham two-set permutation problem"

Target: arXiv math.CO + submission to a combinatorics journal; also erdosproblems.com forum comment on #197.

## Results to include (all proved or machine-certified)

**Setting.** EG79 problem: partition ℤ⁺ into two sets each permutable with no monotone 3-AP. LV11 conjectured impossible via α(3)=1/2, β(3)=1/4 tightness.

1. **Orbit Obstruction Lemma.** Permutable S admits no infinite doubling orbit u_{k+1} = 2u_k − f_k (f_k ∈ finite F ⊆ S). [3-line proof; generalizes DEGS Fact 3.]

2. **Balanced-placement law.** At each placement of v, |#placed∩[1,v) − #placed∩(v,2v)| ≤ |S^c ∩ (v,2v)| + O(1). Corollary: records placed only when ≤ codensity-many smaller values are placed.

3. **Lemma R (ratio-ascent obstruction).** No 3-AP-free arrangement of a set ⊇ {k,2k,3k,5k} places all ratio-≥2 pairs small-first. [4 lines.]

4. **vdC absorption theorem.** Odd classes mod 2^k in van der Corput order absorb all completions into strictly earlier classes; coherent self-absorbing towers exist at all levels. [3-line proof + exhaustive counts to mod 512.]

5. **Theorem 1 (contiguous impossibility).** For the dyadic partition, no solution plays every block as a contiguous run: (a) halving self-reduction: validity of block system (M) descends to (⌊M/2⌋); (b) machine-verified UNSAT for the 16 base cases M = 16..31 (fatal zone (M/4, M/2]); (c) run-tolerance is O(1) elements, so contiguous-run schedules force an infinite descent of finish times. [Include DRAT certificates.]

6. **Partition rigidity.** Record completions must exit the team; partitions like ν-parity die immediately; viable partitions are forced toward dyadic-interval alternation. [Formalize the exact statement carefully.]

7. **Local realizability (the tension).** All finite interleaving games for the dyadic partition are SAT: two-block G(M) ≤ 256, three-block G3(M) ≤ 512, chained with carried orders ≥ 3 links; complete-truncation doom-free arrangements exist at tested scales. The solutions exhibit self-absorbing class-phase structure. So the problem is NOT locally obstructed — any impossibility proof must be genuinely global (infinite), and any construction must be genuinely fractal (non-contiguous at every scale).

8. **Team-B reduction.** S_B = {1,2} ∪ 2·S_A with sliver-absorbable corrections; the dyadic YES reduces entirely to permutability of S_A.

## Open ends stated in the paper
- The interleaving template question (our candidate mechanisms and where each fails).
- Improved-density program: α(3) upper bounds via the balance law.

## Writing plan
LaTeX, ~15 pages. Certificates + code in a public repo. Acknowledge SAT-assistance explicitly (community norm per erdosproblems.com AI-contribution practices).
