# The van der Corput absorption theorem (proved) and the YES-program

## Theorem (vdC absorption — new, 3-line proof)
Order the odd residues mod 2^k by the van der Corput (bit-reversal) rank of (c−1)/2. Then for ANY two classes a placed-before b, the completion class 2b − a mod 2^k strictly precedes b.

*Proof.* With α = (a−1)/2, β = (b−1)/2, the completion has ζ = 2β − α mod 2^{k−1}. Inductively ζ inherits α's low bits as long as α and β agree; at the first differing bit, rev-order rank(α) < rank(β) forces α's bit (hence ζ's) to be 0 and β's to be 1, so rank(ζ) < rank(β), strictly. ∎

Corollaries: coherent towers of "self-absorbing" class orders exist at every level (verified additionally by exhaustive search to mod 512: hundreds of refinements at every level; the canonical vdC tower is one). The SAT chain-game solutions follow exactly such orders (mod-16 [7,15,11,3,9,1,5,13] observed = a self-absorbing order projecting onto [7,3,1,5] → [3,1] → [1]).

## Where the YES-construction stands
Established (hand analysis, this session):
- The normal part (5M/4, 2M] of each block, with the bottom quarter deferred, faces NO cross-block dangers (all would-be attackers x satisfy x ∈ (M/2, M] = other team) — its requirement reduces to plain internal 3-AP-freeness plus overflow (>2M lands in odd blocks: free).
- All quarter-deferral cross-interactions check out (deferred quarters vs later blocks, quarters vs quarters, sliver values as future zones) EXCEPT the internal scheduling of {top, middle, quarter} within a block:
  - quarter after full-normal ⇒ quarter system with 3×-adjacent above-zone: UNSAT at M=32;
  - top-first ⇒ Lemma R structure (ratio-2 pairs must ascend): UNSAT for size ≥ 5.
- Conclusion: the block's internal order is irreducibly interleaved (fractal); the two-block/three-block chain games (all SAT to large sizes, orders carryable at least 3 links) are the witnesses. Closed-form extraction of the interleaving template = the last missing piece of a YES-proof.

Failed closed-form candidates so far: plain rkey (both polarities), epoch = block + 3ν alone, epoch + vdC + 1/16-deferral (30 structured violations at 2^13), quarter-deferral with monolithic parts.

## Assessment
The local consistency at every tested scale + carryability + the exact algebraic absorption mechanism strongly suggest the dyadic partition IS realizable (answer YES, contradicting LeSaulnier–Vijay's conjecture) — but the infinite assembly requires a genuinely fractal interleaving we have not yet captured. Alternative: the obstruction to closing the form is real and the answer is NO; in that case the accumulated impossibility machinery (Lemma R, fatal zones, tolerance-O(1), balance law) is the seed of the proof.

Next steps: (1) large-scale exact incremental global solve (2-level lookahead) to obtain a genuine deep prefix of a global solution; (2) mine the interleaving as a function of scaled position (fractal profile); (3) formalize; or (4) if lookahead solving hits UNSAT at some level with all reservoirs — that is a finite certificate for dyadic-impossibility, redirecting to other partitions or the NO-program.
