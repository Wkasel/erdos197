# 89 — THE CLEAN CHAIN: C3(p) → B1₀ → Lemma Q → ALT-DEAD

Self-contained statement of the campaign's unconditional chain,
prepared for external second-pass review.  Contents: full
statements of every node; full proofs for everything short (PIN,
DIAG-DENSE, B1₀, Lemma Q, ALT-DEAD, the corollaries); exact
pointers for the one long proof (Theorem C3(p)).  The final
section states the chain's one explicitly open applicability
hypothesis.  Nothing else from the campaign is used or referenced.

## 0. Definitions

**Arrangement; 3-permutable.**  For an infinite S ⊆ ℤ⁺, an
*arrangement* of S is a sequence of order type ω listing S exactly
once.  It *contains a monotone 3-AP* if some three positions
i₀ < i₁ < i₂ carry values x, y, z with x + z = 2y and either
x < y < z or x > y > z.  S is *3-permutable* if some arrangement
of S contains no monotone 3-AP.  (Restriction fact, used twice: if
π is an arrangement of S and S′ ⊆ S is infinite, the subsequence
of π on S′ is an arrangement of S′, and any monotone 3-AP of the
subsequence is one of π.)

**Blocks.**  B(t) := (2^t, 2^{t+1}].  For a window (M, 2M] write
b_j := M + j (1 ≤ j ≤ M) and t_i := 2M − i (0 ≤ i ≤ M − 1); so
b_j, t_i ∈ (M, 2M].

**The rung theory.**  For fixed a₁ < a₂ ("attackers"), a scale M
with M > a₂, and a puncture set D ⊆ (M, 2M], let R(a₁, a₂; M, D)
be the assertion that some total order ≺ of (M, 2M] ∖ D satisfies:

  (AP) no monotone 3-AP within (M, 2M] ∖ D under ≺ (both
       orientations banned);
  (U)  for each a ∈ {a₁, a₂} and each j ≥ 1 such that
       i := a − 2j ∈ [0, M − 1] and t_i, b_j ∉ D:  t_i ≺ b_j.

Semantics of (U): a, b_j, 2b_j − a is a 3-term AP with
2b_j − a = 2M − (a − 2j) = t_i; if a is already placed before the
whole window, then b_j placed before t_i would complete the
increasing monotone 3-AP (a, b_j, t_i).

## 1. The three ingredients

### 1.1 Lemma PIN (window pigeonhole) [PROVED here in full]

**Lemma PIN.**  Let T be 3-permutable via the arrangement π, let
a₁ < a₂ ∈ T be fixed, and let 𝕄 be an infinite set of scales m
with 2^m > a₂.  Write D_m := B(m) ∖ T.  Then for all but finitely
many m ∈ 𝕄, R(a₁, a₂; 2^m, D_m) holds.

*Proof.*  Let Q := max(pos_π(a₁), pos_π(a₂)), a fixed finite
number.  The first Q positions of π carry finitely many values,
which meet only finitely many blocks; discard those m from 𝕄.  For
every remaining m ∈ 𝕄, every element of B(m) ∩ T occupies a
position > Q, i.e. after both a₁ and a₂.  Let ≺ be the order
induced by π on B(m) ∩ T = B(m) ∖ D_m (positions restrict).  (AP)
holds because a monotone 3-AP of the restriction is one of π.  For
(U): take a ∈ {a₁, a₂} and j with i = a − 2j ∈ [0, M − 1],
t_i, b_j ∈ T (M = 2^m).  Then (a, b_j, t_i) is an AP with
a < b_j < t_i, and pos(a) < pos(b_j).  If also pos(b_j) < pos(t_i),
π contains the increasing monotone 3-AP (a, b_j, t_i) —
contradiction.  So pos(t_i) < pos(b_j), i.e. t_i ≺ b_j.  ∎

(Provenance: notes/52 §1.3; also paper/main.tex thm:ogred's
pigeonhole, verbatim mechanism.)

### 1.2 Lemma DIAG-DENSE (diagonal pair supply) [PROVED here in full]

Call {3p, 3p + 1} with p ≡ 1 (mod 4) a *diagonal pair*.

**Lemma DIAG-DENSE.**  B(m) contains at least (2^m − 13)/12
pairwise-disjoint diagonal pairs.

*Proof.*  {3p, 3p+1} ⊆ B(m) iff 2^m < 3p and 3p + 1 ≤ 2^{m+1},
i.e. p ∈ (2^m/3, (2^{m+1} − 1)/3], an interval of length
(2^m − 1)/3.  An interval of length L contains ≥ (L − 3)/4 ≥
(L − 3)/4 integers ≡ 1 (mod 4); here ≥ ((2^m − 1)/3 − 3)/4 =
(2^m − 10)/12 ≥ (2^m − 13)/12.  Distinct p give disjoint pairs.  ∎

(Provenance: notes/52 §2.1.)

### 1.3 Theorem C3(p) (the rigidity core) [PROVED; exact pointers]

For odd p ≥ 5 define the three-precedence core on (M, 2M]:

    C3(p) := { t_p ≺ b_p,  t_{p−2} ≺ b_{p+1},  t_{p+5} ≺ b_{p−2} }.

**Theorem C3(p).**  For every odd p ≥ 5 and every
M ≡ 2p + 6 (mod 8) with M ≥ 2p + 6, no total order of (M, 2M]
satisfying (AP) satisfies the three precedences of C3(p).
Moreover the congruence class is exact: on the complementary even
class, (AP) + C3(p) is satisfiable.

*Proof: exact pointers.*  Full uniform-in-p hand proof:
**notes/78 Part I** (Theorems L1(p) and FLIP(p); toolkit = Lemma Z
/ D / E / P of notes/33, constants affine in p; referee prose pass
notes/86 §1).  The instance p = 5 is Theorem thm:c3core of
**paper/main.tex**, with the complete hand proof in
**notes/33-og-proof.md** and independently audited machine
certificates (DRAT; reproduce.sh steps 3–4).  Machine record for
general p: strict schema execution at nine p-values × ~208 scales
(e123), independent complete-encoding solver cross-validation
(e123b), sharp applicability boundaries (e180 partMINMsharp); all
re-runnable via **reproduce2.sh** steps 1–3.

**Fact 1.3.1 (C3(p) ⊆ rung units; three-line computation).**  Let
a₁ = 3p, a₂ = 3p + 1.  Then the three C3(p) precedences are among
the (U)-units of R(3p, 3p+1; M, ∅):

- a = 3p, j = p:      i = 3p − 2p = p        → t_p ≺ b_p;
- a = 3p, j = p + 1:  i = 3p − 2(p+1) = p−2  → t_{p−2} ≺ b_{p+1};
- a = 3p+1, j = p − 2: i = 3p+1 − 2(p−2) = p+5 → t_{p+5} ≺ b_{p−2}.

Hence a total order witnessing R(3p, 3p+1; M, ∅) would satisfy
(AP) + C3(p); by Theorem C3(p), for M in the stated class no such
order exists:

**Corollary 1.3.2.**  For every odd p ≥ 5 and every
M ≡ 2p + 6 (mod 8), M ≥ 2p + 6:  R(3p, 3p+1; M, ∅) fails.

## 2. Theorem B1₀ (zero-dust bridge) [PROVED here in full]

**Theorem B1₀.**  If T ⊆ ℤ⁺ contains the complete dyadic block
B(m) for infinitely many m, then T is not 3-permutable.

*Proof.*  Suppose π is an arrangement of T with no monotone 3-AP;
let 𝕄 be the infinite set of scales with B(m) ⊆ T.

1. Fix m₀ ∈ 𝕄 with 2^{m₀} ≥ 32.  By DIAG-DENSE, B(m₀) contains a
   diagonal pair {3p, 3p+1}, p ≡ 1 (mod 4), with
   p > 2^{m₀}/3 > 10, hence p ≥ 13 ≥ 5 (odd).  Both members lie in
   T because B(m₀) ⊆ T.
2. Apply Lemma PIN with a₁ = 3p, a₂ = 3p+1 and the scale family
   {m ∈ 𝕄 : 2^m > 3p + 1}: for all but finitely many such m,
   R(3p, 3p+1; 2^m, D_m) holds — and D_m = ∅ since B(m) ⊆ T.
3. But for every m ≥ 3 with 2^m ≥ 2p + 6, the scale M = 2^m
   satisfies M ≡ 0 ≡ 2p + 6 (mod 8) (using p ≡ 1 mod 4, so
   2p + 6 ≡ 8 ≡ 0), i.e. M is in Theorem C3(p)'s class; by
   Corollary 1.3.2, R(3p, 3p+1; 2^m, ∅) fails.  This contradicts
   step 2 at every sufficiently large m ∈ 𝕄.  ∎

Inputs: Lemmas PIN and DIAG-DENSE (§1.1–1.2, proved above) and
Theorem C3(p) (§1.3) — nothing else.

*(Sanity corollary: T = ℤ⁺ contains every block, so ℤ⁺ is not
3-permutable — the classical Davis–Entringer–Graham–Simmons fact
recovered by this chain.)*

## 3. Lemma Q (quarter-tail) [PROVED here in full]

For c ∈ {0, 1, 2, 3} and t ≥ 2 let
Λ_c(t) := {v ∈ B(t) : v ≡ c (mod 4)}.

**Lemma Q.**  No 3-permutable set contains Λ_c(t) for one fixed c
and infinitely many t.

*Proof.*  Suppose T ⊇ Λ_c(t) for all t in an infinite set 𝕋, and
let π be an arrangement of T with no monotone 3-AP.

(i) *The chart.*  Define φ on c + 4ℤ by φ(x) = x/4 if c = 0 and
φ(x) = (x − c + 4)/4 if c ∈ {1, 2, 3} — an increasing affine
bijection onto a tail of ℤ⁺.  Block alignment is exact: for
c ∈ {1,2,3}, Λ_c(t) = {2^t + c, 2^t + c + 4, …, 2^{t+1} − 4 + c}
and φ maps it onto {2^{t−2} + 1, …, 2^{t−1}} = B(t − 2); for
c = 0, Λ_0(t) = {2^t + 4, …, 2^{t+1}} and φ = x/4 gives the same.
**φ(Λ_c(t)) = B(t − 2), with no boundary dust.**

(ii) *Transport.*  Restrict π to the infinite set T ∩ (c + 4ℤ)
(an arrangement of it, by the restriction fact) and push forward
by φ: an arrangement of S′ := φ(T ∩ (c + 4ℤ)).  Suppose the image
arrangement had a monotone 3-AP on values x′, y′, z′ with
x′ + z′ = 2y′.  Since φ⁻¹ is affine, the preimages x, y, z
satisfy x + z = 2y, all lie in c + 4ℤ ∩ T, and appear in π in the
same relative order with the same value-order — a monotone 3-AP
of π.  Contradiction; so **S′ is 3-permutable.**

(iii) *The kill.*  S′ ⊇ φ(Λ_c(t)) = B(t − 2) for every t ∈ 𝕋: S′
contains infinitely many complete dyadic blocks.  Theorem B1₀
says S′ is not 3-permutable.  Contradiction.  ∎

## 4. Theorem ALT-DEAD and corollaries [PROVED here in full]

Call a partition ℤ⁺ = A ⊔ B a *valid pair* if A and B are both
3-permutable.  Call a scale t *4-pure* for (A, B) if some class
Λ_c(t) is entirely contained in one of the teams.

**Theorem ALT-DEAD.**  If infinitely many scales are 4-pure for
(A, B), then (A, B) is not a valid pair.

*Proof.*  Each 4-pure scale t supplies a pair (c, S) with
c ∈ {0,1,2,3}, S ∈ {A, B}, and S ⊇ Λ_c(t).  Eight possible cells;
infinitely many scales; so some fixed cell (c, S) recurs for
infinitely many t.  Lemma Q says S is not 3-permutable.  ∎

**Corollary 1 (lattice colorings).**  Say (A, B) is a *blockwise
mod-4 lattice coloring* if for every t (equivalently: infinitely
many t) the intersection of one team with B(t) is exactly one full
class Λ_{c_t}(t).  Then every scale is 4-pure (all four classes
are monochromatic at such t), so ALT-DEAD applies: no blockwise
mod-4 lattice coloring is a valid pair — regardless of which team
holds the class at each scale (the "ownership sequence" never
enters the argument).

**Corollary 2 (on-class punctured variants).**  If for infinitely
many t the minority of block t is merely CONTAINED in one class
Λ_{c_t}(t), then at each such t the other three classes are
monochromatic (majority-owned), so t is 4-pure; ALT-DEAD applies.
Puncture counts are irrelevant.

**Corollary 3 (HSPLIT — hereditary 2-adic splitness).**  For every
valid pair (A, B), every k ≥ 1, and every c mod 2^k, the section
(c + 2^k ℤ) ∩ B(t) is bichromatic for all but finitely many t.
*Proof.*  The chart φ_k(x) = x/2^k (c = 0), (x − c + 2^k)/2^k
(else) maps the class-c section of B(t) exactly onto B(t − k), by
the §3(i) computation with 4 replaced by 2^k; steps (ii)–(iii)
transport verbatim, so no 3-permutable set contains a full
2^k-class section of infinitely many blocks; if some section were
monochromatic for infinitely many t, pigeonhole over the 2·2^k
cells (c, team) would produce such a set.  ∎

In particular every partition whose block minorities are
eventually 2^k-periodic (for any fixed k) is not a valid pair.

*Scope remark (important).*  The correct positive formulation
(second review item 4): **HSPLIT imposes hereditary 2-adic mixing;
combined with L-NOTAIL, a valid pair cannot be globally periodic.**
(A globally periodic coloring of period P gives each team a finite
union of classes mod P, hence an infinite AP, which L-NOTAIL
forbids.)  What HSPLIT does NOT give is aperiodicity of the
minority: Corollary 3 constrains only power-of-two residue
structure, and does not force aperiodicity:
e.g. a minority equal to the multiples of 3 is fully periodic yet
has every mod-2^k class-section bichromatic (gcd(2^k, 3) = 1), so
it is untouched by Corollary 3.  (That particular set contains the
infinite AP 3, 6, 9, …, and a set containing an infinite AP is not
3-permutable — restrict and chart the AP onto a tail of ℤ⁺
containing all complete blocks, then apply B1₀ — but shapes that
avoid both power-of-two purity and infinite in-team APs are not
addressed by anything in this document.)

## 5. The open applicability hypothesis (exact statement)

Theorem ALT-DEAD is conditional on its hypothesis: **infinitely
many 4-pure scales.**  For the partitions of Corollaries 1–2 the
hypothesis holds by construction, so those families are
unconditionally excluded.  For a GENERAL partition, nothing in
this document — and nothing else proved in the campaign — forces
infinitely many 4-pure scales; a partition that is 4-pure at only
finitely many scales (or none) is simply outside ALT-DEAD's reach,
as is any bichromatic-section structure not covered by the charts
above.  Accordingly:

- **Proved here, unconditional:** Theorem B1₀; Lemma Q; Theorem
  ALT-DEAD (as a conditional theorem, its proof complete); the
  exclusion of all blockwise mod-4 lattice colorings, on-class
  punctured variants, and eventually-2^k-periodic minorities.
- **Open:** whether the hypothesis of ALT-DEAD (or any of the
  chart-kill hypotheses) can be established for wider classes of
  partitions.  This chain does NOT resolve Erdős #197: partitions
  with all class-sections eventually bichromatic in every 2-adic
  chart are untouched.

## 6. Machine layer (optional corroboration)

`./reproduce2.sh` (repo root; ~2–3 min): C3(p) schema execution at
three p, independent solver cross-validation at three p, sharp
applicability boundaries, chart-exactness / AP-transport /
units-in-rung / fresh-rung spot checks for §§1.3.1–3, and a scan
of Geneson's density-2/3 permutable set for full class-sections
(finitely many, as Lemma Q requires).  These are finite
consistency checks; the proofs above stand on their own.
