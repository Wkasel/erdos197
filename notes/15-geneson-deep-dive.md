# Deep dive: Geneson, "Density bounds for permutations avoiding monotone arithmetic progressions" (arXiv:2608.12604v1, 12 Aug 2026)

Source: `papers/geneson2026_density.pdf`; text extraction `notes/geneson2026.txt` (clean — verified against the PDF layout; all formulas below reconstructed from it and re-derived).
Companion paper obtained for this note: Hirose–Saito, arXiv:2404.13510 → `papers/hirose-saito-2404.13510.pdf`, text at `notes/hirose-saito.txt`.

Caution flag: the paper declares AI assistance ("Codex with GPT-5.6 Sol Ultra ... proof development"). Every lemma cited below has been re-derived here (inequality chains checked by hand); I mark the one place where the argument is subtler than the text suggests.

Notation (his): ℕ = {1,2,...}. An ω-permutation of a countably infinite S is a sequence p₀,p₁,... listing S exactly once. It contains a monotone ℓ-AP if there are indices i₀<...<i_{ℓ−1}, x∈ℤ, d∈ℤ\{0} with p_{i_j} = x+jd. (Note: d may be negative, so "monotone" covers both increasing and decreasing value-order; equivalently, the three/four terms appear in the sequence in increasing OR decreasing value order.) S is ℓ-permutable if some ω-permutation of S has none.

Densities: d̄_ℕ, d_ℕ via |S∩[1,n]|/n; d̄_ℤ, d_ℤ via |T∩[−n,n]|/(2n+1). α_X(ℓ) = sup upper density of ℓ-permutable subsets, β_X(ℓ) = sup lower density.

Results: α_ℕ(3) ≥ 2/3 and α_ℤ(3) ≥ 2/3 (Theorem 1.1; disproves the LeSaulnier–Vijay conjecture α_ℕ(3)=1/2); β_ℤ(4)=1 (Theorem 1.2 + Corollary 1.3, closing the last length-4 parameter: α_ℕ(ℓ)=β_ℕ(ℓ)=α_ℤ(ℓ)=β_ℤ(ℓ)=1 for all ℓ≥4). The four length-3 parameters remain open. Explicitly noted (his p. 4 remark after Cor. 1.3): these are SUPREMUM statements — Theorem 1.2 does NOT produce a lower-density-one set or a 4-AP-free ω-permutation of all of ℕ or ℤ.

---

## 1. The α_ℕ(3) ≥ 2/3 construction (his Section 3), complete reconstruction

### 1.1 Lemma 3.1 (AP-separation), exact statement and mechanism

**Lemma 3.1.** Let M, L be positive integers with **L > 2M**, let A ⊆ [1,M]∩ℤ, let J ≥ 0, and put
  B = ⋃_{j=0}^{J} [L·4^j + M, 2L·4^j] ∩ ℤ.
Then **no three-term arithmetic progression contained in A∪B meets both A and B.** (This is separation of APs as SETS — order-free, hence stronger than needed for monotonicity.)

Mechanism, with the inequality chains:

- Every member of B is > M ≥ max A, and min B = L·4⁰ + M = L+M > 3M (this is exactly where L > 2M is used). So in any 3-AP meeting both sets, sorted u < v < w, any B-terms sit above any A-terms.

- **Two terms in A, one in B.** The A-terms u < v ≤ M force the B-term to be the largest, w = 2v−u ≤ 2M−1. But min B = L+M > 3M > 2M−1. Impossible. (If the B-term were the middle term v of the sorted AP, then w > v > M would also lie outside A, contradicting two terms in A; so "B-term = largest" is forced.)

- **One term a ∈ A, two terms y < z in B.** Then a < y < z and the AP condition (a,y,z sorted) is z = 2y − a. Say y lies in the j-th interval:
  L·4^j + M ≤ y ≤ 2L·4^j.
  With 1 ≤ a ≤ M:
  z = 2y − a ≥ 2(L·4^j + M) − M = 2L·4^j + M, and z ≤ 2·(2L·4^j) − 1 = 4L·4^j − 1.
  So z ∈ [2L·4^j + M, 4L·4^j − 1]. This "escape window" is disjoint from B:
  - z > 2L·4^j = top of interval j;
  - if j < J: z ≤ 4L·4^j − 1 < 4L·4^j + M = L·4^{j+1} + M = bottom of interval j+1;
  - if j = J: z > 2L·4^J = max B.
  Hence z ∉ B. ∎

The two design choices: intervals [L·4^j+M, 2L·4^j] have doubling width so 2·(interval) lands strictly between the top of interval j and the bottom of interval j+1 (ratio-4 spacing gives room for the doubling map PLUS the ±M perturbation from the A-term); the +M offset at the bottom absorbs the −a shift.

### 1.2 The recursion (exact parameters)

S₀ = ∅, M₀ = 1. For k ≥ 1:
- **L_k = 4·M_{k−1}**  (so L_k > 2M_{k−1}, hypothesis of Lemma 3.1);
- **B_k = ⋃_{j=0}^{k} [L_k·4^j + M_{k−1}, 2L_k·4^j] ∩ ℤ**  (k+1 intervals — J grows with k);
- **M_k = 2L_k·4^k = 8·M_{k−1}·4^k**;  S_k = S_{k−1} ∪ B_k;  **S = ⋃_{k≥1} B_k**.

Structural facts (all verified):
- B_k ⊆ [1, M_k]; min B_k = L_k + M_{k−1} = 5M_{k−1} > M_{k−1} ≥ max S_{k−1}, so blocks are pairwise disjoint and S_k ⊆ [1, M_k].
- Intervals within B_k pairwise disjoint: 2L_k·4^j < L_k·4^{j+1} + M_{k−1}.
- Each interval has L_k·4^j − M_{k−1} + 1 elements, so
  |B_k| = L_k·(4^{k+1}−1)/3 − (k+1)(M_{k−1}−1).   (his (3.7))

### 1.3 The ordering and assembly

- **Corollary 2.3** (from Ardal–Brown–Jungić): every finite set of integers has a 3-AP-free order — restrict the ABJ order ≺ (see §2 below) to the finite set. Choose such an order σ_k of the entire finite block B_k.
- **The ω-permutation is the concatenation σ₁σ₂σ₃⋯** — all of block 1 in σ₁-order, then all of block 2, etc.
- **Fairness (why type ω):** every x ∈ B_k has all its predecessors inside B₁∪⋯∪B_k, a finite set. His Lemma 3.2 (see §2.3 below) converts "strict total order, every element has finitely many predecessors" into an order-isomorphism with (ℕ∪{0}, <), i.e. an honest ω-permutation. No interleaving/back-filling is needed because each block is finite — this is the simplest possible fairness argument.

**Lemma 3.3 (3-AP-freeness).** A monotone 3-AP either (i) lies inside one B_k — excluded by σ_k; or (ii) meets ≥ 2 blocks — let k be its largest block index; its other term(s) lie in S_{k−1} ⊆ [1, M_{k−1}]; apply Lemma 3.1 with A = S_{k−1}, M = M_{k−1}, L = L_k, J = k: no 3-AP (as a set) meets both S_{k−1} and B_k. Contradiction. Note the separation is total: cross-block APs simply do not exist inside S, so the internal orders σ_k are completely unconstrained beyond 3-AP-freeness.

### 1.4 The density count

Along n = M_k = 2L_k·4^k:
  |S∩[1,M_k]|/M_k ≥ |B_k|/M_k = (4^{k+1}−1)/(6·4^k) − (k+1)(M_{k−1}−1)/(8M_{k−1}4^k)
   = 2/3 − 1/(6·4^k) − (k+1)(M_{k−1}−1)/(8M_{k−1}·4^k) ≥ 2/3 − 1/(6·4^k) − (k+1)/(8·4^k) → 2/3.
So d̄_ℕ(S) ≥ 2/3. (The lower density of S is ~0: S∩[1, M_{k−1}·anything before B_k starts] is tiny relative to L_k; upper density only.) Each block ALONE nearly fills density 2/3 of [1,M_k]: Σ_j L_k 4^j ≈ (4/3)L_k4^k = (2/3)M_k. The earlier blocks contribute negligibly — the construction is "one giant fresh block per scale".

---

## 2. The binary-order machinery (his Section 2)

### 2.1 The bit-reversal rank ρ and identity (2.1)

For t ≥ 0, represent each residue mod 2^t by its member of {0,...,2^t−1} with t-digit binary expansion. ρ̄_{2^t}: ℤ/2^tℤ → {0,...,2^t−1} assigns each residue its rank when digits are read **least-significant first** (0 before 1 at the first difference); ρ_{2^t}(z) = ρ̄_{2^t}(z + 2^tℤ). E.g. mod 4 the residue order is 0,2,1,3. Recursion:
  **(2.1) ρ_{2^{j+1}}(z) = 2^j·(z mod 2) + ρ_{2^j}(⌊z/2⌋)**  (j ≥ 0):
odd numbers rank above all even numbers, and within a parity class the rank is inherited from ⌊z/2⌋. ν₂(z) = 2-adic valuation.

### 2.2 Lemma 2.1 (verbatim-precise)

**Lemma 2.1.** Let t ≥ 1, m = 2^t. If r, δ ∈ ℤ and δ ≢ 0 (mod m), then
  **(2.2) ρ_m(r) < ρ_m(r+δ) ⟺ ρ_m(r+δ) > ρ_m(r+2δ)**,
  **(2.3) ρ_m(r) < ρ_m(r+δ) ⟺ ρ_m(r+2δ) < ρ_m(r+3δ)**.
In particular ρ_m(r+δ) is strictly smaller than both ρ_m(r) and ρ_m(r+2δ), or strictly larger than both (strict local extremum ⇒ no rank-monotone 3-AP mod m when m ∤ δ).

Proof mechanism (induction on t): t=1: δ odd, ranks alternate 0,1,0,1 or 1,0,1,0. Step: if δ odd, parities of r, r+δ, r+2δ, r+3δ alternate; by (2.1) odd terms have rank ≥ 2^t, even terms < 2^t, so all four comparisons are decided by parity alone and both equivalences hold trivially (each side true iff r even). If δ = 2δ′, all four terms share parity; (2.1)'s leading summand 2^t((r+kδ) mod 2) is constant in k; subtracting it reduces both equivalences to the hypothesis for (⌊r/2⌋, δ′), where 2^{t+1} ∤ δ ⇒ 2^t ∤ δ′. Strictness: δ ≢ 0 mod m makes consecutive residues distinct.

(2.3) is the identity that later synchronizes the reversed positive-side order in the β_ℤ(4) construction: it says the (0,1) comparison and the (2,3) comparison always AGREE, while (2.2) says the (0,1) and (1,2) comparisons always DISAGREE.

### 2.3 The order ≺ on ℤ, Lemma 2.2, Lemma 3.2

**The ABJ order:** for distinct u,v ∈ ℤ, put q = 1 + ν₂(v−u) and declare u ≺ v ⟺ ρ_{2^q}(u) < ρ_{2^q}(v). (Well-defined strict total order = Ardal–Brown–Jungić Definitions 2.1/2.2.)

**Lemma 2.2.** For u,h ∈ ℤ, h ≠ 0: neither u ≺ u+h ≺ u+2h nor u+2h ≺ u+h ≺ u holds (no ≺-monotone 3-AP in either direction — from ABJ Theorem 2.2), and
  **u ≺ u+h ⟺ u+2h ≺ u+3h**  — cited as the case s=2, t=3 of Hirose–Saito Lemma 2.5 applied to the identity map ℤ → (ℤ,≺). (See §4 for the HS lemma. Verified: HS Lemma 2.5 with a=u, d=h, s=2 even, t=3 odd gives exactly this, and the identity map is chaotic on ℤ by the first half of Lemma 2.2; the hypothesis "a+id ∈ S for all i ∈ ℕ" holds since S = ℤ.)

**Lemma 3.2 (verbatim-precise).** Let < be an infinite strict total order on a set X such that every x ∈ X has finitely many predecessors. Then p(x) = |{y ∈ X : y < x}| is an order-preserving bijection X → ℕ∪{0}.
Proof: x < y ⇒ p(x) < p(y) (predecessors of x, plus x itself, precede y), so p is injective and order-preserving. Image is an initial segment: if p(y) = q with predecessors y₀ < ⋯ < y_{q−1}, then p(y_j) = j (the global predecessors of y_j are exactly y₀,...,y_{j−1}). Infinite injective image that is an initial segment of ℕ∪{0} = all of ℕ∪{0}. ∎
This is THE assembly lemma: any block-concatenation order in which every element sits in a finite block with finitely many earlier blocks is automatically an ω-permutation. It is completely generic (no arithmetic content).

### 2.4 The α_ℤ(3) ≥ 2/3 variant (his Section 4) — the midpoint-first trick

Lemma 4.1 replaces total separation by a weaker, order-aware statement. **Lemma 4.1:** L > 2M, A ⊆ [−M,M], I_j = [L4^j + M, 2L4^j − M] (note: trimmed by M at BOTH ends now), B = ⋃_{j=0}^J (I_j ∪ −I_j). Suppose every element of A is ordered before every element of B. Then every 3-AP in A∪B meeting both sets has its **midpoint in A and both endpoints in B** — hence appears midpoint-first, hence is **not monotone**.
Chains: min|B| = L+M > 3M. Two terms u,v in A: a third term as midpoint has |·| ≤ M; as endpoint 2u−v has |2u−v| ≤ 2|u|+|v| ≤ 3M < L+M — no. One term a∈A as an ENDPOINT with y,z ∈ B, z = 2y−a: y,z have the same sign (|y| ≥ L+M > M ≥ |a| forces sign(z)=sign(y)), and 2|y|−M ≤ |z| ≤ 2|y|+M; if |y| ∈ I_j then 2L4^j+M ≤ |z| ≤ 4L4^j−M, which is above the top 2L4^j−M of I_j, below the bottom 4L4^j+M of I_{j+1} (if j<J), and above max if j=J — so z ∉ B, contradiction. Only the midpoint-in-A configuration survives, and it is harmless by scheduling. The extra −M trim on the top of each I_j is what makes 2|y|−M clear the top of I_j.

Recursion: R₀ = 1, L_k = 4R_{k−1}, I_{k,j} = [L_k4^j + R_{k−1}, 2L_k4^j − R_{k−1}] (0≤j≤k), B_k = ⋃_j (I_{k,j} ∪ −I_{k,j}), **R_k = 2L_k4^k − R_{k−1} = (8·4^k − 1)R_{k−1}**, T = ⋃B_k ⊆ ℤ. min|B_k| = 5R_{k−1} > R_{k−1} ⇒ disjoint blocks. Same assembly: finite 3-AP-free order per block, concatenate, Lemma 3.2.
**Lemma 4.2:** cross-block progression, k = largest block index, Lemma 4.1 with A = T_{k−1} (⊆ [−R_{k−1}, R_{k−1}]), B = B_k: one term in B_k — impossible; two terms in B_k — the third is the midpoint in T_{k−1} and occurs before both endpoints ⇒ not monotone. (Here — unlike Section 3 — cross APs DO exist in T; they are killed by order, not geometry.)
Count: |B_k| = 2L_k(4^{k+1}−1)/3 − 2(k+1)(2R_{k−1}−1); with U_k = L_k4^k, R_k = 2U_k − R_{k−1}, L_k/U_k = 4^{−k}, R_{k−1}/U_k = 4^{−(k+1)}:
  |T∩[−R_k,R_k]|/(2R_k+1) ≥ [(8/3)U_k − (2/3)L_k − 4(k+1)R_{k−1} + 2(k+1)] / (4U_k − 2R_{k−1} + 1) → (8/3)/4 = 2/3.

---

## 3. Theorem 1.2: β_ℤ(4) = 1 — the S_{m,a,c} construction (his Section 5), full mechanism

This is the paper's most sophisticated infinite-assembly argument. Parameters: m = 2^t ≥ 2 a power of two, integer a ≥ 4, real c with **2 + 1/a < c < a** (5.1). Write ρ = ρ_m; r_i ∈ {0,...,m−1} is the residue with ρ(r_i) = i.

### 3.1 The set

For stage s ≥ 0 and 0 ≤ i < m:
  **N_{s,i} = { x < 0 : x ≡ r_i (mod m), a^{2ms+m−i} ≤ |x| < a^{2ms+3m−i}/c }**
  **P_{s,i} = { x > 0 : x ≡ r_i (mod m), a^{2ms+m+1+i} ≤ x < a^{2ms+3m+1+i}/c }**
S_{m,a,c} = union of all blocks. Each block: one sign, one residue class mod m, magnitudes in [a^f, a^{f+2m}/c) where f is the **lower exponent**. Per stage s the 2m lower exponents are exactly {2ms+1, ..., 2ms+2m}, each once (negatives take 2ms+1..2ms+m as i runs m−1..0; positives take 2ms+m+1..2ms+2m as i runs 0..m−1). Blocks are finite, nonempty (interval [a^f, a^{f+2m−1}) ⊆ block range has length a^f(a^{2m−1}−1) ≥ 4(4^m−1) ≥ 4m > m, so it contains a member of any residue class), and pairwise disjoint (c > 1 ⇒ a^{f+2m}/c < a^{f+2m} = next same-residue-same-sign block's start; different residue/sign are automatically disjoint).

### 3.2 The order (the assembly)

- **Block order:** stage s lists N_{s,0}, N_{s,1}, ..., N_{s,m−1}, P_{s,m−1}, P_{s,m−2}, ..., P_{s,0} (5.3); stages concatenated s = 0,1,2,....
- **Within a block** with residue r: for x, y in the block, x before y iff (x−r)/m ≺ (y−r)/m in a NEGATIVE block, and (y−r)/m ≺ (x−r)/m (reversed!) in a POSITIVE block — i.e. each block is a copy of a finite piece of (ℤ, ≺) via the affine map x ↦ (x−r)/m, with the ABJ order on negative blocks and its reverse on positive blocks.
- Every element lies in one finite block with finitely many earlier blocks ⇒ finitely many predecessors ⇒ Lemma 3.2 ⇒ ω-permutation π_{m,a,c}.

**Block rank:** q(N_{s,i}) = i, q(P_{s,i}) = m−1−i (5.4). Then in BOTH signs the lower exponent is **2ms + K − q** (5.5), K = m (negative), K = 2m (positive). Within a stage, the same-sign blocks appear in strictly increasing rank order chronologically (negatives: rank = i increasing; positives: rank m−1−i increasing as i decreases). **Outer endpoint** of a block with lower exponent f: U_f = a^{f+2m}/c (5.6), the strict sup of its magnitudes.

### 3.3 The five lemmas (mechanism)

**Lemma 5.1 (rank/stage/magnitude dichotomy).** Two distinct same-sign blocks in chronological order with ranks q then q′ ≤ q: the later block lies in a later stage (same-stage same-sign ranks increase), so its lower exponent is ≥ f + 2m + (q − q′) (from (5.5): same K, stage +≥1, rank drop q−q′), hence its magnitudes are ≥ a^{f+2m+q−q′} = c·a^{q−q′}·U_f. So: **chronologically later + rank not larger ⇒ every magnitude > c·(anything in the earlier block), and > ac·(anything) if the rank strictly drops.** This is the quantitative engine: "you may only come later with small rank if you are exponentially bigger."

**Lemma 5.2 (shrinking triples collapse).** A chronologically nondecreasing same-sign SHRINKING (decreasing magnitudes) 3-AP lies in one block. If m|d: same residue ⇒ same rank everywhere; a transition to a distinct later block would force magnitude growth by Lemma 5.1 (q′=q) — contradiction; so no transition. If m∤d: adjacent terms have distinct residues (hence distinct blocks), and by (2.2) the two successive block-rank comparisons are opposite (this holds whether ranks are read through ρ or through its reverse — reversing flips both comparisons); at the transition where the later block has strictly smaller rank, Lemma 5.1 forces larger magnitudes — contradicting shrinking. So m∤d is impossible and the triple is in one block.

**Lemma 5.3 (mixed-sign anchor).** x₀,x₁,x₂ consecutive AP terms with signs −,+,+ or +,−,−; last pair grows in magnitude; blocks chronologically nondecreasing; q(x₂) ≤ q(x₁). Then x₁,x₂ share a block. Proof: block of x₁: stage s, lower exponent f, outer U_f. Every chronologically earlier OPPOSITE-sign block has outer endpoint ≤ U_f/a: (x₁ > 0) earlier negatives in stage s have outer exponent ≤ 2ms+3m vs positive's ≥ 2ms+3m+1; (x₁ < 0) earlier positives are in stages ≤ s−1, outer exponent ≤ 2ms+2m vs ≥ 2ms+2m+1. So |x₀| < U_f/a, |x₁| < U_f, and since x₀ has sign opposite to x₁,x₂ and x₂ = 2x₁ − x₀:
  |x₂| = 2|x₁| + |x₀| < (2 + 1/a)·U_f < c·U_f  — this is exactly where **c > 2 + 1/a** enters.
If x₂ were in a distinct later block with q(x₂) ≤ q(x₁), Lemma 5.1 gives |x₂| ≥ cU_f. Contradiction. (The interleaving of exponent ranges between the signs — negatives at 2ms+1..2ms+m, positives at 2ms+m+1..2ms+2m — is precisely tuned to give the factor-a cushion U_f/a.)

**Growth bound (5.7):** consecutive same-sign growing terms satisfy |z_{j+1}| = |z_j| + |d| < 2|z_j| (since |z_j| = |z_{j−1}| + |d| > |d|).

**Lemma 5.4 (growing triples collapse).** (1) y,x₀,x₁,x₂ consecutive, blocks chron. nondecreasing, x₀,x₁,x₂ one sign growing, y the opposite sign ⇒ x₀,x₁,x₂ in one block. (2) x₀..x₃ chron. nondecreasing growing same-sign 4-AP ⇒ x₁,x₂,x₃ in one block.
Mechanism: m|d case: apply Lemma 5.3 to (y,x₀,x₁) to merge x₀,x₁; then (5.7) gives |x₂| < 2|x₁| while a distinct later same-rank block needs factor > c > 2 (Lemma 5.1) — merge x₂. In (2), two applications of (5.7)+5.1. m∤d case: by (2.2) successive rank comparisons alternate; a strict rank descent across a transition forces (Lemma 5.1) magnitude ratio > ac > 2·4 = 8 > 2, contradicting (5.7); a rank descent at the first transition of (1) contradicts Lemma 5.3 (would merge two different residues into one block). So m∤d is impossible here.

**Lemma 5.5 (structure of chronologically nondecreasing 4-APs).** Any nonconstant 4-AP in S_{m,a,c} with chronologically nondecreasing blocks has either (i) three consecutive terms in one block, or (ii) x₀,x₁ in block A and x₂,x₃ in block B, with A,B of the SAME residue mod m and OPPOSITE signs.
Mechanism: terms are strictly monotone integers avoiding 0 ⇒ sign changes at most once; magnitudes shrink before the change and grow after. Segment shapes 4+0, 3+1, 1+3, 2+2. 4+0 and 3+1: Lemma 5.2 or 5.4(2). 1+3: Lemma 5.4(1). 2+2: if m|d, the shrinking pair has equal ranks ⇒ one block (5.1); Lemma 5.3 merges the growing pair; the two blocks share the residue (m|d) and have opposite signs — case (ii). If m∤d: the shrinking pair must have strictly increasing ranks (a nonincreasing rank across a shrinking transition contradicts 5.1); then (2.3) transfers the comparison to the far pair: e.g. shrinking pair negative with ρ(x₀) < ρ(x₁) gives ρ(x₂) < ρ(x₃), so q(x₂) > q(x₃) on the positive side (reversed rank) — and symmetrically; then Lemma 5.3 (with q(x₃) ≤ q(x₂)) would merge the growing pair into one block despite distinct residues — contradiction. So m∤d cannot occur in the 2+2 case.

**Lemma 5.6 (no monotone 4-AP).** Take a monotone 4-AP x₀,x₁,x₂,x₃ in order of appearance; blocks are chronologically nondecreasing by definition of appearance order. Case (i): three consecutive terms in one block share residue r; z = (x−r)/m maps them to a nonconstant 3-AP monotone in ≺ or its reverse — forbidden by Lemma 2.2 (both directions forbidden). Case (ii): common residue r, z_i = (x_i−r)/m, h = z₁−z₀ ≠ 0, and (z₂,z₃) = (z₀+2h, z₁+2h). Lemma 2.2 (the Hirose–Saito shift identity) gives **z₀ ≺ z₁ ⟺ z₂ ≺ z₃** (5.8). If A negative, B positive: internal orders force z₀ ≺ z₁ (negative blocks use ≺, and x₀ before x₁) and z₃ ≺ z₂ (positive blocks reversed, x₂ before x₃) — contradicting (5.8). If A positive, B negative: z₁ ≺ z₀ and z₂ ≺ z₃ — again contradicts (5.8). ∎

So the reversal of ≺ on positive blocks is not decoration: it is exactly what turns the shift-invariance (2.3)/(HS 2.5) into a contradiction for the surviving 2+2 split, while (2.2) handles all same-sign collapses. The three parameters do separate jobs: **m** (power of two) enables ρ_m and controls density loss 1/m; **a ≥ 4** provides the exponent lattice and the opposite-sign cushion U_f/a; **c ∈ (2+1/a, a)** must exceed 2+1/a for Lemma 5.3's escape bound and stay below a so blocks nearly fill [a^f, a^{f+2m}).

### 3.4 The density computation

Missing integers outside [−a^{2m}, a^{2m}] are exactly the union over e ≥ e₀ = 2m+1 of one "gap" per exponent: the integers of one sign and one residue class with magnitude in [a^e/c, a^e) (his (5.9)–(5.10) bookkeeping: each block [a^f, a^{f+2m}/c) is followed by gap [a^e/c, a^e), e = f+2m; the stage-s gap exponents {2ms+2m+1,...,2ms+4m} tile ℕ_{≥2m+1} perfectly; the verification that nothing else is missing chooses, for given x with |x| > a^{2m}, the largest admissible f ≤ E where a^E ≤ |x| < a^{E+1}, and shows x is in that block or its gap). Each gap has h_e integers with |h_e − λa^e| ≤ 2, λ = (1 − 1/c)/m. Complement count H(n) = |[−n,n] ∖ S_{m,a,c}|:
- along n_K = a^{e₀+K}: H(n_K)/(2n_K+1) → L := λa/(2(a−1)) (geometric series Σa^e = (a^{e₀+K+1}−a^{e₀})/(a−1), errors C + 2(K+1) = o(n_K));
- for general n (a^E ≤ n < a^{E+1}): completed gaps ≤ λX/(a−1) + 2E with X = a^{E+1}, plus the truncated part of the current gap ≤ max{0, (y−X/c)/m} + 1, y = n+1; the key optimization: if y > X/c then λX/(a−1) + (y−X/c)/m = y/m + (c−a)X/(mc(a−1)) ≤ λay/(a−1) using c − a < 0 and X ≥ y. Both cases give ≤ 2Ly + o(n).
So limsup H(n)/(2n+1) = L = a(c−1)/(2mc(a−1)) exactly, and
  **d_ℤ(S_{m,a,c}) = 1 − a(c−1)/(2mc(a−1))**.
Corollary 1.3: a = 4, c = 5/2 (valid: 2 + 1/4 < 5/2 < 4) gives d_ℤ = 1 − 2/(5m) → 1 as m → ∞ through powers of two. Hence β_ℤ(4) = 1, and (with Adenwalla's β_ℕ(4) = 1) all length-≥4 parameters equal 1.

Note the trade-off structure: the density deficit 2/(5m) is paid ENTIRELY in the thin gaps [a^e/c, a^e) of ONE residue class each — the construction is "co-thin" rather than "thin", the opposite regime from the α(3) constructions.

---

## 4. Reference [6]: Hirose–Saito, and the full reference list

### 4.1 Hirose–Saito (downloaded: `papers/hirose-saito-2404.13510.pdf`)

M. Hirose, S. Saito, "Characterization of order structures avoiding three-term arithmetic progressions", Order 42 (2025), 231–239; arXiv:2404.13510 [math.CO], 21 Apr 2024. (Sources: [arXiv abstract](https://arxiv.org/abs/2404.13510), [Springer](https://link.springer.com/article/10.1007/s11083-024-09677-7).)

Terminology: for S ⊆ ℚ and a totally ordered set (X,⪯), an injection f: S → X is **chaotic** if there are no a,b,c ∈ S with f(a) ≺ f(b) ≺ f(c) and b−a = c−b; f is **binary** if there are no a,b,c with f(a) ≺ f(b) ≺ f(c) and ord₂(b−a) = ord₂(c−b) (2-adic valuations equal). Binary ⇒ chaotic.

**Main Theorem (HS 1.1).** For countably infinite (X,⪯): a chaotic bijection ℕ→X (resp. ℤ→X) exists iff X has **no isolated points** (in the order topology); ℚ→X exists iff additionally X lacks a maximum or lacks a minimum.

**HS Lemma 2.4.** f: S→X chaotic, t odd positive, a ∈ ℚ, d ∈ ℚ^× with a+id ∈ S for ALL i ∈ ℕ. Then f(a) ≺ f(a+d) ⟺ f(a) ≺ f(a+td). (Induction on odd t; the step uses the full alternating chain f(a) ≺ f(a+d) ≻ f(a+2d) ≺ ⋯ up to b = a+2(t+2)d, i.e. needs ~3t+5 consecutive ray members inside S.)

**HS Lemma 2.5 (the one Geneson cites).** f: S→X chaotic, **s ∈ ℕ even, t ∈ ℕ⁺ odd**, a ∈ ℚ, d ∈ ℚ^× with a+id ∈ S for all i ∈ ℕ. Then
  **f(a) ≺ f(a+d) ⟺ f(a+sd) ≺ f(a+td)**.
(Proof: shift Lemma 2.4 along the alternating chain.) Geneson's Lemma 2.2 equivalence is s=2, t=3 with f = id: ℤ → (ℤ,≺): u ≺ u+h ⟺ u+2h ≺ u+3h.

Other contents relevant to monotone-AP permutation problems:
- **HS Prop 2.6:** for S ∈ {ℕ,ℤ,ℚ}, every chaotic map is binary. (Chaotic orders on the FULL semigroup are 2-adically rigid: only the ν₂-pattern of differences matters.) Their Example 2.1 shows this FAILS for general S: on {0,1,2,3}, the order 2,3,0,1 is chaotic but not binary. **The implication is exactly what breaks for partition pieces** — see §5.
- **HS Prop 2.2 (+ Remark 2.3):** a binary bijection forces X to have no isolated points; needs only that {ord₂(b−a) : b ∈ S} is unbounded above for every a ∈ S (true for any infinite subset of a fixed residue tower, and in particular for any set of positive upper density? — no: it needs, for each a, elements b with a ≡ b mod 2^n for all n; true e.g. whenever S meets a ≡ a mod 2^n for every n).
- Consequence worth recording: **DEGS impossibility is a corollary** — an ω-order (type ω) has ALL points isolated, so no chaotic bijection ℕ → ω exists: chaotic ⇒ binary (2.6) ⇒ no isolated points (2.2), contradiction. Same for type ζ (ℤ-indexed). This is the cleanest known proof-shape of "you cannot permute all of ℕ".
- **HS Section 3 (constructions):** builds binary bijections onto any countably infinite X without isolated points by an increment scheme: S_n = subset sums of r₀,...,r_{n−1} (r_n = 2^n for ℕ; r_n = (−2)^n for ℤ, giving S_n = intervals), with ord₂ separation between S_n and the translate S_n + r_n; **HS Lemma 3.2** extends a binary map on S to S ∪ (S+r) whenever ord₂(a−b) < ord₂ r on S, interleaving the translate strictly between consecutive old values, hitting a prescribed target x ∈ X (back-and-forth surjectivity); for ℚ, alternating "interleave" (Lemma 3.2) and "append above everything" (Lemma 3.7, for ord₂(a−b) > ord₂ r) steps, driven by a ν₂-graded additive basis of ℚ (Lemmas 3.4–3.6). This is a general-purpose *extension-by-translation* assembly technique: order-extend along a doubling filtration while preserving a difference-valuation invariant. It is the abstract ancestor of Geneson's per-block ABJ-restriction + concatenation.

### 4.2 Full reference list of Geneson 2026 (with identifiers)

[1] S. Adenwalla, *Avoiding monotone arithmetic progressions in permutations of integers*, Discrete Math. 347 (2024), 114183. doi:10.1016/j.disc.2024.114183. (Local: `papers/adenwalla2022.pdf`.) Source of β_ℕ(4)=1, α_ℤ(4)=1, β_ℤ(4)≥2/3, β_ℤ(3)≥3/10; his Theorems 1/4/6/7 supply the geometric residue blocks, truncation, and alternating signed intervals that Section 5 combines.
[2] H. Ardal, T. Brown, V. Jungić, *Chaotic orderings of the rationals and reals*, Amer. Math. Monthly 118 (2011), 921–925. doi:10.4169/amer.math.monthly.118.10.921. (The order ≺; no monotone 3-AP on all of ℤ under an arbitrary linear order.)
[3] J. A. Davis, R. C. Entringer, R. L. Graham, G. J. Simmons, *On permutations containing no long arithmetic progressions*, Acta Arith. 34 (1977), 81–90. doi:10.4064/aa-34-1-81-90. (Local: `papers/DEGS77.pdf`.) Facts 3–4: every ω-permutation of ℕ has a monotone 3-AP; a 5-AP-free one exists.
[4] R. C. Entringer, D. E. Jackson, *Elementary problem E2440*, Amer. Math. Monthly 80 (1973), 1058. doi:10.2307/2318789.
[5] J. Geneson, *Forbidden arithmetic progressions in permutations of subsets of the integers*, Discrete Math. 342 (2019), 1489–1491. doi:10.1016/j.disc.2019.02.004. (Local: `papers/geneson2018.pdf`.) α_ℤ(3)≥1/2, β_ℤ(3)≥1/6, β_ℕ(4)≥1/2.
[6] M. Hirose, S. Saito, *Characterization of order structures avoiding three-term arithmetic progressions*, Order 42 (2025), 231–239. doi:10.1007/s11083-024-09677-7 = arXiv:2404.13510. (Local: `papers/hirose-saito-2404.13510.pdf`.)
[7] T. D. LeSaulnier, S. Vijay, *On permutations avoiding arithmetic progressions*, Discrete Math. 311 (2011), 205–207. doi:10.1016/j.disc.2010.10.006. (α_ℕ(3)≥1/2, β_ℕ(3)≥1/4, α_ℕ(4)=1, β_ℕ(4)≥1/3; the now-disproved equality conjecture.)
[8] M. B. Nathanson, *Permutations, periodicity, and chaos*, J. Combin. Theory Ser. A 22 (1977), 61–68. doi:10.1016/0097-3165(77)90063-2. (Power-of-two modular existence theorem behind ρ.)

---

## 5. What transfers to the two-set partition problem (Erdős #197), and exactly where it breaks

Target: partition ℤ⁺ = A ⊔ B with BOTH pieces 3-permutable. Geneson's results are single-set, slack-rich (density < 1, or ℓ = 4). Audit of each technique:

### 5.1 Directly transferable (no loss)

- **Corollary 2.3** (every finite integer set has a 3-AP-free order, by restricting ≺): applies to any finite block of either piece. Free.
- **Lemma 3.2** (finitely-many-predecessors ⇒ ω): the universal assembly step. Any block schedule for A and any for B that keeps blocks finite with finitely many earlier blocks yields honest ω-permutations of both pieces. Free.
- **Lemma 2.1 / the ρ-rank calculus**: statements about ℤ itself, partition-agnostic. Our program's "absorption theorem" is Lemma 2.1 in interval form (per note 13); (2.3) is a shift-invariance we had not been exploiting and is potentially useful wherever we pair a block with a reversed copy.
- **The midpoint-first principle (Lemma 4.1's conclusion)**: purely order-theoretic and the single most valuable import. For a 3-AP u < v < w inside one piece, the permutation contains it monotonically iff **v appears temporally between u and w**. In a block concatenation, a cross-block AP is therefore automatically safe in two of the three placement patterns: midpoint's block strictly earliest (midpoint appears first) and midpoint's block strictly latest (midpoint appears last). The ONLY dangerous cross-block pattern is block(u) ⪯ block(v) ⪯ block(w) chronologically with v's block strictly between, or ties resolved badly inside shared blocks. So the design requirement for each piece is NOT Lemma-3.1-style total AP-separation; it is:
  (a) each block internally 3-AP-free (free by Cor. 2.3), and
  (b) every 3-AP of the piece crossing blocks has its midpoint in the chronologically first or last of the (≤3) blocks involved, with within-block tie cases handled by the internal order.
  This is a strictly weaker, combinatorial "scheduling" condition compatible with pieces of density up to 1/2 or more — it does not by itself require gaps.

### 5.2 Where the α(3) construction breaks under partition

- **Lemma 3.1's mechanism is a zero-sum resource.** The Case-2 chain pushes the third term z into the escape window [2L·4^j + M, 4L·4^j − 1] — which is empty of S but, in a partition, belongs ENTIRELY to the other piece. Total AP-separation for piece A forces piece B ⊇ all escape windows and all slabs [M_{k−1}+1, L_k+M_{k−1}−1], i.e. B contains arbitrarily long intervals of length comparable to its position (the slab before B_k has length ≈ 4M_{k−1}, the intra-block gaps of B_k have length ≈ 2L_k4^j). Both pieces cannot simultaneously enjoy separation: B's own cross-block 3-APs are abundant (its consecutive long intervals are within doubling range of each other by construction — e.g. escape window j has elements y with 2y − u back in window j+1's range for u in window j). So Geneson's Section-3 geometry can serve AT MOST ONE piece, and it saddles the other piece with the exact interval-heavy structure our notes 03/04 (interval impossibility, balance law) show is the hard regime. Precisely: the step that fails is not Lemma 3.1 itself but its **premise "A ∪ B ⊆ S"** — in a partition, 2y − a ∉ S is unavailable; every escape lands in the sibling piece and becomes the sibling's problem.
- **Density mismatch:** the Section-3 set has lower density → 0 (each B_k is preceded by a gap of relative length ≈ 1 − o(1) at scale L_k). A partition piece has its density pinned by the sibling: if A mimics S, then B has upper density 1 along the pre-block slabs — B is "almost all of an interval [1, L_k]" infinitely often, and by our fragility results, ordering an almost-full initial interval while its complement-in-the-piece keeps arriving is exactly the pumping obstruction. So the SHAPE transfers only in the unbalanced-partition regime already under test (note 13: N_{k+1}/N_k → ∞), where the analogue of the escape-window emptiness is replaced by "escape window is in B but scheduled far later / handled by B's own midpoint-first layout".

### 5.3 Where the Section-4 (ℤ, midpoint-in-A) variant breaks

Lemma 4.1 needs THREE facts: (i) A is bounded ([−M,M]) and B starts above 3M; (ii) B's intervals are trimmed so the doubling map exits them; (iii) A is scheduled entirely before B. In a partition of ℤ⁺, (i)+(iii) are reproducible (A := everything seen so far, B := new block), but (ii) again forces the trimmed-out escape windows into the sibling. Moreover the trick only neutralizes APs with **midpoint in the old content**; APs with midpoint in the NEW block and one endpoint old, one endpoint new-or-later, are killed in his setting by geometry (they don't exist in S) — in a partition they exist and must be killed by scheduling: midpoint-in-new-block-appearing-last requires the far endpoint to be in a block no later than the midpoint's — a nontrivial global constraint linking the two pieces' block calendars. Concretely: the dangerous pattern (endpoint early, midpoint middle, endpoint late) must be excluded for BOTH pieces simultaneously over the SAME integer 3-APs split by the 2-coloring; this coupling has no analogue in Geneson and is where genuinely new work is needed.

### 5.4 What the β_ℤ(4) machinery offers, and its 3-AP limits

The Section-5 assembly is the model for "infinite assembly with cross-block APs present": it never separates APs; it classifies them (Lemma 5.5) and kills each class by one of three mechanisms — magnitude dichotomy (5.1, geometry), internal ABJ order (2.2 first half), or the shift identity (2.3)/(HS 2.5) against a deliberately reversed twin block. Transferable ideas:
  1. **Rank/stage bookkeeping** (lower exponent = 2ms + K − q): a scheduling scheme where "later with small rank ⇒ exponentially larger" gives a clean dichotomy usable for cross-block AP control in either piece; nothing about it needs density < 1 — his own construction has density → 1.
  2. **Reversed twin blocks synchronized by (2.3)**: if a piece contains two same-residue mirror sub-blocks scheduled at different times, giving one the ABJ order and the other its reverse makes any AP hitting each twice non-monotone. For #197 both pieces live in ℤ⁺ (no signs), but the role of "sign" can be played by any bipartition of a piece's blocks into two interleaved families with disjoint magnitude windows — the sign was only used to (a) split exponent ranges and (b) force the sign-change structure of Lemma 5.5. Point (b) is the obstacle: for one-signed sets, a monotone integer sequence's magnitudes just grow, so the 2+2 "shrink-then-grow" classification degenerates; one must re-derive a Lemma-5.5 analogue for increasing 3-APs only, which is easier (only "growing" cases survive) — for 3-APs the analogue of Lemma 5.4(2) would need to put x₁, x₂ of a growing triple in one block, and then Lemma 2.2's first half finishes. The step that does NOT survive at ℓ = 3: Lemma 5.4 and 5.5 constantly use a fourth term (or an opposite-sign anchor y) to gain the inequality |x₂| < 2|x₁| BEFORE invoking the rank dichotomy; with only three terms, a 3-AP can have x₀ tiny and x₁, x₂ in far-apart blocks (x₂ ≈ 2x₁), and c ≤ 2 would be needed to exclude the jump — but Lemma 5.3's bound needs c > 2 + 1/a. **These two constraints on c collide exactly at ℓ = 3**; this is the quantitative reason the paper's method proves β(4) = 1 but not β(3) large: the doubling map 2x₁ − x₀ sits precisely at the block-growth ratio the rank dichotomy can tolerate. Any 3-AP adaptation must break this collision, e.g. by residue bookkeeping that forbids x₁, x₂ from being same-residue-different-block at all (m | d control) — which is a covering/coloring condition, i.e., naturally a PARTITION condition. This is worth pursuing: at ℓ = 3 the "m | d" APs are the whole difficulty, and distributing residue classes mod m between the two pieces of #197 so that each piece's internal m|d-APs fall into the safe midpoint-first patterns is a concrete program.
  3. **Density accounting by exponent-tiling** (each e ≥ e₀ owns exactly one thin gap): a reusable template for showing a blocky construction has lower density 1 − ε — relevant if #197 is attacked via "A thin, B co-thin" unbalanced splits.

### 5.5 The Hirose–Saito rigidity: a constraint on ANY solution of #197

HS Prop 2.6 (chaotic ⇒ binary) holds whenever the needed rays a + id, i = 0..O(t), stay inside the set; combined with Prop 2.2 it forbids ω-orders. A partition piece escapes because rays get 2-colored — **but van der Waerden supplies arbitrarily long finite monochromatic APs**, so for each fixed odd t, one piece contains some (3t+5)-term AP {a+id} on which HS Lemma 2.4's alternation argument runs verbatim (it only uses that many consecutive ray members). Consequence: in any successful partition, each piece's chaotic ω-order must be "locally binary" along every sufficiently long monochromatic AP it contains, yet globally an ω-order (all points isolated) — the contradiction of Prop 2.2 is avoided only because the isolated-point argument needs, around a given element c, sibling elements c′ = c + 2ⁿ IN THE SAME PIECE with n arbitrarily large, at the same time as the ray structure. So: **if some element a of piece A satisfies (i) a + 2ⁿ ∈ A for infinitely many n, and (ii) enough of the finite rays through a lie in A to push Lemma 2.4's chains, then A is not 3-permutable.** Making (i)+(ii) precise and checking whether every 2-coloring must produce such a configuration is a plausible NO-route for #197; conversely, any YES-construction must consciously starve one of (i), (ii) in each piece. Our dyadic-reduction notes (02, 07) should be re-read against HS's ν₂-formulation — their "binary" condition is exactly our absorption invariant, stated for maps rather than sets.

### 5.6 Summary table

| Technique | Source | Transfers? | Breaking point under partition |
|---|---|---|---|
| Finite 3-AP-free block orders (Cor 2.3) | ABJ ≺ | yes, free | — |
| ω-assembly by finite blocks (Lem 3.2) | generic | yes, free | — |
| Total AP-separation (Lem 3.1) | geometry of gaps | NO | escape window 2y−a lands in sibling piece; separation is zero-sum |
| Midpoint-first neutralization (Lem 4.1) | scheduling | partially | only kills midpoint-in-old APs; midpoint-in-new + straddling endpoints now exist and couple the two pieces' schedules |
| Rank/stage dichotomy (Lem 5.1) | exponent bookkeeping | yes (template) | needs geometric block growth; fine for unbalanced splits |
| Reversed-twin + shift identity (2.3, HS 2.5) | binary calculus | yes (template) | sign structure must be replaced; Lemma 5.5's shrink/grow classification degenerates one-signed |
| 4-term slack (Lem 5.3–5.5) | ℓ = 4 | NO at ℓ = 3 | c > 2 + 1/a (escape bound) vs c ≤ 2 (3-term doubling jump) collide exactly at ℓ = 3 |
| HS chaotic⇒binary rigidity | rays in S | as an obstruction | vdW gives long monochromatic APs ⇒ local binarity is forced; candidate NO-route via (i)+(ii) of §5.5 |
