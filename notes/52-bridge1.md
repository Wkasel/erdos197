# 52 — GAP-BRIDGE1: the Case-1 assembly bridge (pair ownership vs split)

Companion to notes/50 (assembly graph; this note is its Case-1 item 4),
notes/43 (the N1–N7 program and the Case dichotomy N4), notes/49 (the
N2 off-diagonal catalogue + the diagonal C3(p) family), notes/38/40
(the G3 landing-pad observations), STATUS.md "What remains" ledger.

Third session on this front; **no prior partial exists** — `git log
--all -- notes/52-bridge1.md` is empty, so the two earlier attempts
stalled before committing anything.  This note is written incrementally
and committed section by section.

**Overall status: `BRIDGE1 CLOSED as an assembly argument —
conditional on two pre-existing tags (GAP-N2-DIAG, GAP-N3), with the
split branch proved VACUOUS; no descent/well-ordering is needed, and
§4.3 shows the planned landing-pad descent could never have worked.`**

Every step is tagged [PROVED] / [MACHINE-CHECKED] / [GAP].  The
machine checks are experiments/e152_bridge1_check.py (§6).

---

## 0. What BRIDGE1 must deliver, and the shape of the answer

### 0.1 The task as ledgered (notes/50 item 4, STATUS.md link 4)

In Case 1 of the N4 dichotomy, some team T has infinitely many
C₀-clean dyadic blocks.  The Case-1 kill chain is N2 (single-block
rungs, UNSAT per scale) + N3 (dust robustness) + N1 (T-PIN
pigeonhole); but T-PIN fires only if T owns BOTH members of a usable
attacker pair at finite positions.  GAP-BRIDGE1 = the missing
ownership argument: "every Case-1 team owns some adjacent pair over
its clean blocks, else the split/planted-half landing-pad structure
fires" — sketched across notes/40/42/43, never written.

### 0.2 The answer delivered here

The expected proof shape was a dichotomy with a hard second branch
(every usable pair split → the partner inherits a landing-pad
configuration → descent on pair assignments).  The actual resolution
is simpler and stronger, and the simplification is a theorem, not a
shortcut:

1. The usable pairs are not scarce.  The diagonal family
   {3p, 3p+1}, p ≡ 1 (mod 4), fires on exactly the dyadic residue
   class M ≡ 0 (mod 8) (e123 flip-class law, re-confirmed §2), and
   its pairs appear with LINEAR DENSITY (spacing 12) inside every
   dyadic block.  A C₀-clean block therefore contains, above a
   computable scale, a fully-in-T usable pair — branch "T owns a
   pair" holds ALWAYS (§3).
2. Consequently the split branch is VACUOUS: "every usable pair
   meets the partner" already contradicts the existence of a single
   large clean block, by counting alone (§4.2).  The partner's
   quantified inheritance (one value of each crown pair
   {2^j−1, 2^j}, j even — the 2-adic structure the task predicted)
   is real but is used against the HYPOTHESIS, not against the
   partner: it destroys T's cleanliness.
3. The planned descent on pair assignments has NO well-ordering: the
   landing-pad inheritance moves strictly UP in scale, and for every
   finite usable family the splitter adversary has a fixed point (a
   coloring that dodges forever).  So a well-founded descent along
   that route does not exist — an infinite usable family with
   unbounded per-block pair counts is NECESSARY for any BRIDGE1
   argument, and the diagonal family is exactly such a family (§4.3).

The two conditions the bridge rests on are the two pre-existing
ledger tags, in sharpened form (§1.4): GAP-N2-DIAG (the parametric
diagonal schema — e123's "generalizes verbatim" claim, written up)
and GAP-N3 (puncture robustness at fixed C).  **GAP-BRIDGE1 itself is
discharged: no assembly-level gap remains in Case 1 beyond those two
rung-side tags.**

---

## 1. Definitions, the pigeonhole lemma, and the rung hypothesis

### 1.1 Conventions

Blocks: B(m) = (2^m, 2^{m+1}], m ≥ 0.  For a set T ⊆ ℤ⁺ and C ≥ 0,
B(m) is *C-clean for T* iff |B(m) ∖ T| ≤ C; D_m := B(m) ∖ T is the
*dust*.  An *arrangement* of T is a bijection π : ℕ → T; pos(v) =
π⁻¹(v).  A 3-AP (a, b, c), a < b < c, a + c = 2b, all in T, is
*monotone* under π iff pos(a) < pos(b) < pos(c) or
pos(a) > pos(b) > pos(c).  T is *3-permutable* iff some arrangement
of T has no monotone 3-AP.  (Notation as notes/43; "clean" always
means bounded dust, the notes/50 Case-1 sense.)

### 1.2 The punctured rung theory

For attackers a₁ < a₂, a scale M, and a puncture set
D ⊆ (M, 2M], let S := (M, 2M] ∖ D and define the finite constraint
system **R(a₁, a₂; M, D)** on linear orders ≺ of S:

  (i)  [in-block AP-freeness]  for every 3-AP (u, y, z) ⊆ S:
       ¬(u ≺ y ≺ z) and ¬(z ≺ y ≺ u);
  (ii) [fired units]  for every 3-AP (a, y, z) with a ∈ {a₁, a₂}
       and y, z ∈ S:  z ≺ y.

(In the (i, j) coordinates of notes/49: the units of (ii) are exactly
t_i ≺ b_j for i + 2j ∈ {a₁, a₂}, restricted to unpunctured values.)
R is *consistent* iff some linear order satisfies (i) + (ii).

### 1.3 Lemma PIN (the T-PIN pigeonhole, restated)  [PROVED]

**Lemma PIN.**  Let T be 3-permutable, let a₁ < a₂ ∈ T be fixed, and
let 𝕄 be an infinite set of scales such that for each m ∈ 𝕄 the block
B(m) is C-clean for T and 2^m > a₂.  Then for all but finitely many
m ∈ 𝕄, the theory R(a₁, a₂; 2^m, D_m) is consistent.

*Proof.*  Fix an arrangement π of T with no monotone 3-AP.  Let
Q := max(pos(a₁), pos(a₂)) and F := {v ∈ T : pos(v) ≤ Q}, a finite
set (|F| = Q + 1).  Each v ∈ F lies in at most one block, so at most
|F| scales m ∈ 𝕄 have B(m) ∩ F ≠ ∅.  For any other m ∈ 𝕄, every
element of S := B(m) ∖ D_m = B(m) ∩ T has position > Q.  Order S by
position: u ≺ v iff pos(u) < pos(v).  Constraint (i) holds because a
positionally monotone AP inside S ⊆ T would be a monotone AP of π.
For (ii): let (a, y, z) be an AP with a ∈ {a₁, a₂}, y, z ∈ S.  All
three lie in T; pos(a) ≤ Q < pos(y), pos(z).  The decreasing pattern
pos(z) < pos(y) < pos(a) is impossible; forbidding the increasing one
forces pos(z) < pos(y), i.e. z ≺ y.  ∎

Contrapositive form (how it is used): if for infinitely many m ∈ 𝕄
the theory R(a₁, a₂; 2^m, D_m) is INconsistent, then T is not
3-permutable.  This is thm:ogred's pigeonhole verbatim (N1 of
notes/43, [HAND] there); it is restated in full so this note is
self-contained at the assembly layer.

### 1.4 The rung hypothesis (H1), with exact status

**Hypothesis (H1) = RUNG-DIAG-PUNCT.**  For every p ≡ 1 (mod 4),
p ≥ 5, and every C ≥ 0, there is a threshold m*(p, C) such that for
every m ≥ m*(p, C) and EVERY puncture set D ⊆ (2^m, 2^{m+1}] with
|D| ≤ C, the theory R(3p, 3p+1; 2^m, D) is inconsistent.

Status, exactly:

* p = 5, C = 0: **PROVED by hand** — thm:c3core (notes/33) at
  M ≡ 0 (mod 8), and every 2^m with m ≥ 3 is ≡ 0 (mod 8).
* p ∈ {9, 13}, C = 0: **MACHINE** — e123/e123b: the diagonal core
  C3(p) = {t_p ≺ b_p, t_{p−2} ≺ b_{p+1}, t_{p+5} ≺ b_{p−2}} (a
  subset of the (ii) units: attackers 3p, 3p, 3p+1 respectively)
  fires on flip class M ≡ 2p+6 ≡ 0 (mod 8) for p ≡ 1 (mod 4);
  data/e123_diagonal_schema.json re-read this session: p = 5, 9, 13
  all flip_class_mod8 = 0, 104/104 L1-scales + 52/52 flip scales +
  52/52 sharpness controls, fail list empty.
* small C: **MACHINE** — the puncture batteries (notes/42 §4, g4c
  parts B/D: C3 puncture states, STG ≤ 8-puncture tortures,
  truncation to 36 %); plus THIS note's e152: p = 9 with |D| = 3
  placed adversarially ON the minimal core's values, UNSAT at
  M = 128 and 256 (§6).
* uniform in p: **[GAP-N2-DIAG]** — e123's schema claim ("the C3
  hand proof Z/D/E/P generalizes verbatim to C3(p), every odd
  p ≥ 5") awaits its parametric write-up.  This is a sub-tag of the
  existing GAP-N2(a); the bridge needs ONLY the diagonal lane, not
  the off-diagonal parametrics.
* uniform in C: **[GAP-N3]** — the pre-existing dust-robustness tag,
  needed here in exactly its ledgered form.

(H1) is deliberately threshold-free: any finite m*(p, C) suffices,
because Case 1 supplies infinitely many clean blocks above every
threshold.  No linear "M ≥ 4x" bound is load-bearing.

[Commit checkpoint — §0–1.]

---

## 2. The supply lemmas: usable pairs are dense in every block

### 2.1 Lemma DIAG-DENSE  [PROVED]

Call {3p, 3p+1} with p ≡ 1 (mod 4), p ≥ 5 a *diagonal usable pair*
(usable at every dyadic scale ≥ its (H1) threshold, by §1.4).  Let
N(m) := #{p ≡ 1 (mod 4) : {3p, 3p+1} ⊆ B(m)}.

**Lemma DIAG-DENSE.**  N(m) ≥ (2^m − 13)/12 for every m ≥ 0.

*Proof.*  {3p, 3p+1} ⊆ B(m) ⟺ 2^m < 3p and 3p + 1 ≤ 2^{m+1} ⟺ p
lies in the real interval I = (2^m/3, (2^{m+1} − 1)/3], of length
(2^m − 1)/3.  Any real interval of length ℓ contains at least
⌊ℓ/4⌋ ≥ ℓ/4 − 1 integers ≡ 1 (mod 4).  So N(m) ≥ (2^m − 1)/12 − 1 =
(2^m − 13)/12.  ∎

The pairs are pairwise disjoint (consecutive-integer pairs at
distinct 3p), which is what the counting below uses.

### 2.2 Lemma CROWN-2ADIC (the crown pairs sit on the diagonal)
[PROVED]

**Lemma CROWN-2ADIC.**  For every EVEN j ≥ 4, the crown pair
{2^j − 1, 2^j} is a diagonal usable pair: 2^j − 1 = 3p_j with

    p_j = (2^j − 1)/3 = 1 + 4 + 4² + … + 4^{j/2 − 1} ≡ 5 (mod 8).

For every ODD j ≥ 3, 2^j − 1 ≡ 7 (mod 8) and 3 ∤ 2^j − 1: the
odd-index crown pairs are exactly instances of the open
x ≡ 7 (mod 8) off-diagonal cells of notes/49 §8 (outside the e122
catalogue) and are NOT currently usable.

*Proof.*  j even: 4^k ≡ 1 (mod 3) gives 3 | 2^j − 1 and the geometric
sum; mod 8 the terms are 1, 4, 0, 0, …, so p_j ≡ 5 (mod 8) once
j/2 ≥ 2, hence p_j ≡ 1 (mod 4) and p_j ≥ 5.  j odd: 2^j ≡ 2 (mod 3)
so 3 ∤ 2^j − 1; and 2^j − 1 ≡ 7 (mod 8) for j ≥ 3.  ∎

This is the "exact 2-adic structure" the task brief predicted for the
split branch: the even-index crowns are the p ≡ 5 (mod 8) members of
the diagonal family.  The bridge does not need them specifically —
DIAG-DENSE supplies twelve-fold denser material — but the crowns are
the members the landing-pad geometry of §4.3 talks about, and the
odd-index crowns mark precisely where the catalogue is still open.

---

## 3. The theorem: Case-1 teams die outright

### 3.1 Theorem B1  [PROVED modulo (H1)]

**Theorem B1.**  Assume (H1).  Let T ⊆ ℤ⁺ have infinitely many
C₀-clean dyadic blocks, for any constant C₀.  Then T is not
3-permutable.

*Proof.*  Suppose π is an arrangement of T with no monotone 3-AP.
Let 𝕄 be the infinite set of C₀-clean scales.

STEP 1 (pair extraction — the ownership branch always fires).
Choose m₀ ∈ 𝕄 with 2^{m₀} ≥ 12·C₀ + 25.  By Lemma DIAG-DENSE,
B(m₀) contains N(m₀) ≥ (2^{m₀} − 13)/12 ≥ C₀ + 1 pairwise-disjoint
diagonal usable pairs.  The dust D_{m₀} = B(m₀) ∖ T has ≤ C₀
elements, and each element punctures at most one of the disjoint
pairs; so some diagonal pair {3p, 3p+1} ⊆ B(m₀) ∩ T ⊆ T, with
p ≡ 1 (mod 4) and p > 2^{m₀}/3 ≥ 8, hence p ≥ 9 ≥ 5.

STEP 2 (windows).  Let 𝕄′ := {m ∈ 𝕄 : m ≥ m*(p, C₀) and
2^m > 3p + 1}, still infinite (only finitely many scales removed;
m*(p, C₀) is the (H1) threshold).

STEP 3 (pigeonhole + rung).  Apply Lemma PIN with a₁ = 3p,
a₂ = 3p + 1 (both in T by Step 1, both < 2^m for m ∈ 𝕄′), C = C₀,
scale family 𝕄′: for some (indeed cofinitely many) m ∈ 𝕄′ the theory
R(3p, 3p+1; 2^m, D_m) is consistent.  But every m ∈ 𝕄′ has
m ≥ m*(p, C₀) and |D_m| ≤ C₀, so (H1) makes that theory
inconsistent.  Contradiction.  ∎

Remarks on the proof's economy:

* No hypothesis on the partner T′ is used anywhere — the "dichotomy"
  of the task brief has collapsed: the ownership branch holds
  unconditionally because the usable supply is denser (linear in the
  block) than any bounded dust.
* The (2,…) bounds of the Case-2 machinery, punctures hitting the
  minimal core, residues, thresholds — all are absorbed into (H1)'s
  quantifiers; the assembly layer is pure pigeonhole and counting.
* The pair produced in Step 1 has p growing with m₀ (p > 2^{m₀}/3).
  This is exactly why the PARAMETRIC diagonal schema (GAP-N2-DIAG) is
  load-bearing and cannot be replaced by the p ≤ 13 machine layer:
  with C₀ dust the adversary can puncture any FIXED finite pair
  list, but cannot puncture linearly many disjoint pairs.

### 3.2 Corollaries  [PROVED modulo (H1), except B1.2 unconditional]

**Corollary B1.1 (Case 1 is fatal).**  Assume (H1).  In any partition
ℤ⁺ = A ⊔ B, if some team is in Case 1 of the N4 dichotomy
(infinitely many C-clean dyadic blocks for some C), that team is not
3-permutable — so no Case-1 partition is a YES-instance, and every
YES-partition must be everywhere-split (Case 2).  *Proof.*  Theorem
B1 applied to the Case-1 team.  ∎

**Corollary B1.2 (sanity anchor, unconditional).**  ℤ⁺ itself is not
3-permutable.  *Proof.*  Every block is 0-clean and {15, 16} ⊆ ℤ⁺;
run Steps 2–3 with the fixed pair {15, 16} = {3·5, 3·5+1} and C₀ = 0,
where (H1) is the PROVED instance thm:c3core (p = 5, C = 0, §1.4).
No open tag is touched.  ∎

(B1.2 recovers, through this program's machinery, the classical fact
that motivates Erdős #197 — the full integers cannot be permuted
3-AP-monotone-free, so the content of the problem is whether TWO
teams can share the burden.  That the campaign's proven layer already
contains this is a consistency check on the whole chain: any
formalization under which B1.2 failed would have been wrong.)


---

## 4. The dichotomy form, the split quantification, and why there is
## no descent

Theorem B1 makes the task's dichotomy unnecessary; this section
records the dichotomy anyway — partly because the ledger asked for it
in that shape, mostly because the analysis of the FAILED branch is
load-bearing knowledge: it proves the previously-planned proof
strategy could not have worked, which future sessions should not
rediscover.

### 4.1 The dichotomy, stated as tasked  [PROVED modulo (H1)]

**Proposition B2.**  Let T be a Case-1 team with clean-scale set 𝕄
and dust bound C₀, and let T′ be its partner.  Then exactly one of:

  (a) some diagonal usable pair is entirely contained in T — and then
      T is not 3-permutable (Lemma PIN + (H1), Steps 2–3 of B1);
  (b) every diagonal usable pair meets T′.

And (b) is VACUOUS: it contradicts Case-1 membership outright (§4.2).
Hence (a) holds for every Case-1 team.  ∎ (given §4.2)

### 4.2 The split quantification, and the one-shot contradiction
[PROVED]

**Lemma SPLIT-QUANT.**  Suppose every diagonal usable pair meets T′.
Then for every m,

    |B(m) ∩ T′|  ≥  N(m)  ≥  (2^m − 13)/12,

and in particular T′ contains at least one value of every crown pair
{2^j − 1, 2^j} with j even ≥ 4 (Lemma CROWN-2ADIC) — the task brief's
"one value of each pair {2^j−1, 2^j}, an infinite set with exact
2-adic structure".

*Proof.*  The N(m) diagonal pairs inside B(m) are pairwise disjoint
and each contributes at least one T′-element of B(m).  ∎

**Corollary B2-VAC (branch (b) is impossible for a Case-1 team).**
If T has even ONE C₀-clean block at a scale with 2^m ≥ 12·C₀ + 26,
branch (b) fails: it would force |B(m) ∖ T| = |B(m) ∩ T′| ≥
(2^m − 13)/12 > C₀.  ∎

Note what happened to the task's expected structure: the partner's
inherited set is real (SPLIT-QUANT), but it is not used to build a
kill against T′ — it is used against the HYPOTHESIS.  The inheritance
is so dense that it is incompatible with T's cleanliness, and the
whole second branch evaporates before any order theory is needed.
The partner needs no windows, no landing pads, no unsplit pair of its
own; nothing about T′'s permutability is ever invoked.

### 4.3 Why the planned descent could never have worked  [PROVED
(the obstruction); recorded to prevent re-attempts]

The task brief (and notes/50 item 4) envisaged, for the split branch:
"the partner inherits a usable configuration — the G3 landing-pad
family (x, 2^j−1, 2^{j+1}−2−x), or its own unsplit pair", closed by
"a well-ordering argument on pair assignments".  This subsection
shows that in the only regime where the split branch is non-vacuous —
namely when the usable family is restricted to a FINITE list (e.g.
today's unconditional layer: the verified cells of notes/49 §6 plus
p ≤ 13) — no such descent exists, for structural reasons.

First the landing-pad geometry itself, made exact (all elementary):

**Lemma LP (landing-pad arithmetic).**  Fix j ≥ 3.
  (α) For every 1 ≤ x ≤ 2^j − 3, (x, 2^j − 1, 2^{j+1} − 2 − x) is a
      3-AP whose completion lies in B(j); as x varies the completions
      sweep (2^j, 2^{j+1} − 3] downward from the top.  Likewise
      through the hi half: (x, 2^j, 2^{j+1} − x) for 1 ≤ x ≤ 2^j − 1.
      (The G3 kill instances (2, 31, 60), (2, 127, 252),
      (2, 511, 1020) of notes/38 are (α) at x = 2, j = 5, 7, 9.)
  (β) (1, 2^j, 2^{j+1} − 1) is a 3-AP linking the hi half at level j
      to the lo half at level j+1.
  (γ) Within the crown-half set 𝒞 = {2^j − 1, 2^j : j ≥ 3}, the ONLY
      3-APs with all members in 𝒞 ∪ {1} are the (β) family and the
      degenerate in-level triple (2^j − 2, 2^j − 1, 2^j) (whose low
      endpoint is not in 𝒞): for an AP (u, v, w) with v, w ∈ 𝒞 at
      levels k ≤ l, w ≤ 2v − 1 forces l ∈ {k, k+1}, and the four
      cross-level combinations give u = 1 (hi_k, lo_{k+1}),
      u = 0, −1, −2 (impossible) respectively.

*Proof.*  Substitution throughout; (γ): if v ∈ {2^k−1, 2^k} and
w ∈ {2^l−1, 2^l}, l ≥ k+2 gives w ≥ 2^{k+2}−1 > 2v ≥ u + w, absurd;
the l = k and l = k+1 cases enumerate as displayed.  ∎

Now the obstruction.  Suppose the usable family is a fixed finite
list 𝒫₀ (pairs and their attacker cohorts), and consider the SPLITTER
ADVERSARY: the coloring that (i) splits every pair of 𝒫₀ and every
crown pair (T′ gets the lo halves 2^j − 1, say, T gets the hi), and
(ii) assigns to T every other value — in particular every completion
2^{j+1} − 2 − x, x ∈ A′, of every fan (α) through a T′-owned lo half,
for every finite attacker cohort A′ ⊆ T′ the argument might try to
fix.  Then:

* T is Case-1 (dust per block ≤ 1 + |𝒫₀|-material at low blocks:
  eventually exactly one dust value per block, the planted lo half);
* T′ owns one value of each pair of 𝒫₀ and each crown pair — the
  full SPLIT-QUANT inheritance restricted to this sparse family;
* yet NO fixed finite attacker cohort of either team ever fires an
  unsatisfiable per-window system: T never owns a full 𝒫₀-pair; T′'s
  landing-pad fans are starved (every completion is in T), and by
  Lemma LP(γ) the crown halves alone support only the (β) chain
  units lo_{j+1} ≺ hi_j — one unit per level on FRESH values, which
  any order satisfies (e.g. place each level's material in
  decreasing numeric order); and T′ has no clean windows, so Lemma
  PIN never applies to T′ at all.

So with a finite usable family the split branch has a genuine FIXED
POINT — a coloring the entire mechanism never contradicts.  It
follows that:

1. **Any BRIDGE1 argument MUST use an infinite usable family whose
   per-block pair count is unbounded** (else the splitter adversary
   above, applied to the finite list of pairs the argument actually
   cites below any given scale... more precisely: a family with
   bounded per-block counts b can be split while keeping T
   (b + 1)-clean, dodging both branches forever).  Density is not a
   convenience of §3 — it is necessary.
2. **The descent had no well-ordering to run on.**  The imagined
   inheritance step hands the partner a configuration at a STRICTLY
   HIGHER level j (the landing pad lives above the split pair that
   created it), so any potential decreasing along the inheritance
   chain would have to decrease along a strictly-increasing-scale
   sequence of fresh configurations — and the fixed point shows no
   bottom is ever reached.  There is nothing to found the induction
   on.  The correct replacement is the SIMULTANEOUS counting of
   SPLIT-QUANT: quantify over all pairs at once, and the split
   branch self-destructs against the cleanliness hypothesis in one
   step, with no ordering at all.

This is the honest discharge of the task's "write the well-ordering
argument with full care": written with full care, the well-ordering
does not exist, and the argument that replaces it needs none.

### 4.4 What remains true of the landing pads

The landing-pad family is not dead weight: Lemma LP(α) is the
mechanism by which SPLITTING IS COSTLY IN EXACT PARTITIONS (notes/38:
it killed geo_alt/A, whose planted halves had in-team attackers AND
in-team completions).  In the present frame that observation becomes:
the splitter adversary of §4.3 is FORCED to hand T every fan
completion — i.e. forced to make T cleaner and more uniform, pushing
T deeper into Case 1 and into the teeth of Theorem B1's density
argument.  The pads lose their role as a kill mechanism and reappear
as the reason the adversary cannot decorate its dodge: every dodge of
the fan geometry is a donation to the clean team.  No step of §3
depends on this remark.


---

## 5. Residue bookkeeping: dyadic vs anchor-free  [PROVED / GAP map]

Theorem B1 is stated for DYADIC blocks, matching the notes/50 Case-1
frame.  There every window scale is M = 2^m ≡ 0 (mod 8) (m ≥ 3), and
the diagonal family at p ≡ 1 (mod 4) fires on exactly that class
(flip law M ≡ 2p + 6 (mod 8): p ≡ 1 (mod 4) ⟹ 0, p ≡ 3 (mod 4) ⟹ 4).
This is the only residue fact the proof uses, and it is why the
p ≡ 1 (mod 4) sub-family — not the full diagonal — is the usable set.

The ANCHOR-FREE Case-1 form (e121 / notes/50: ratio-2 clean windows
(N, 2N] at arbitrary anchors N) needs more, recorded so the residue
arithmetic is not re-derived wrong later:

* Pigeonhole the infinite clean-window family onto a single residue
  r = N mod 8.
* r = 0: the dyadic argument verbatim (p ≡ 1 mod 4).
* r = 4: diagonal again, now the p ≡ 3 (mod 4) sub-family (flip
  class 4) — same density 1/12, same (H1) shape at class-4 scales.
* r = 2, 6: the diagonal cannot fire (2p + 6 ≡ 2p + 6 with p odd
  covers only {0, 4}).  Needed: the parametric B2(x) lane (law
  M ≡ x + 7 (mod 8), so x ≡ r + 1 (mod 8), odd ⟺ r even ✓) or
  B6(x) (law M ≡ x + 3, x ≡ r + 5).  For r = 2: B2 with
  x ≡ 3 (mod 8); for r = 6: B2 with x ≡ 7 (mod 8) — the OPEN
  catalogue class — so use B6 with x ≡ 3 (mod 8) instead.  Both
  lanes are verified per-cell (x ≤ 21) only: the parametric forms
  are GAP-N2(a) proper.
* r odd: only the C(x) lane has odd laws (M ≡ x + 2 (mod 8),
  x ≡ r − 2 odd ✓); verified at x = 11 only (notes/49 §7).
* In every case the supply count matches: pairs {x, x+1} with x in a
  fixed odd residue class mod 8 have one representative per 16
  consecutive integers, so a clean window (N, 2N] contains ≥
  (N − c)/16 disjoint such pairs — DIAG-DENSE's counting ports
  verbatim, and Steps 1–3 of B1 go through once the lane's (H1)
  analogue is granted.

**Tag: BRIDGE1-AF** (anchor-free version) = the above, blocked on the
parametric off-diagonal lanes (B2/B6 for r ≡ 2, 6; C for r odd) —
strictly harder input than the dyadic version's GAP-N2-DIAG, and NOT
needed for the notes/50 assembly, whose Case 1 is dyadic.  The
anchor-free strengthening only matters if a future reframing of the
dichotomy (e.g. the notes/54 IIa windows) wants Case-1 kills at
arbitrary anchors; notes/54 §"IIa" should cite BRIDGE1-AF, not
BRIDGE1, for that.


---

## 6. Machine checks (e152)  [MACHINE-CHECKED — all pass]

experiments/e152_bridge1_check.py, as the task brief mandates: each
branch on 3 constructed colorings at 2 scales.  Complete encodings
(all transitivity triples — UNSAT needs no soundness argument),
Cadical195, one query at a time.  data/e152_bridge1.{json,log}.

* **χ1 (branch (a), the direct kill).**  Case-1 team, C₀ = 3, dust
  placed adversarially ON the C3(9) minimal-core values of each
  window (b₉, b₁₀, t₉ punctured — the known 3-unit core is destroyed
  on purpose).  Step-1 extraction finds exactly p = 9 ({27, 28}) in
  B(4) ∖ dust; R(27, 28; 128, {137,138,247}) UNSAT (n = 125, 643 163
  clauses, 0.3 s); R(27, 28; 256, {265,266,503}) UNSAT (n = 253,
  5 365 979 clauses, 3.2 s).  The kill reroutes through the full
  fired-unit family — a live instance of the N3 robustness (C = 3)
  that (H1) packages.  Controls at M = 128: AP-only SAT and
  single-attacker-27 SAT (encoding polarity + "singles SAT"
  reconfirmed).
* **χ2 (branch (b), the splitter).**  T′ = {3p : p ≡ 1 (mod 4)}:
  exact counts |B(7) ∩ T′| = 11 ≥ 9.58 = (2⁷−13)/12 and
  |B(8) ∩ T′| = 21 ≥ 20.25; all 11 resp. 21 diagonal pairs inside
  each block meet T′; BOTH teams' per-block dust exceeds 8 —
  the split branch forces Case-2 shape, Cor B2-VAC verified
  numerically at two scales.
* **χ3 (the §4.3 fixed point, and its limits).**  Catalogue pairs
  x = 11..21 and all crown pairs split 1-1 (T′ = lo halves); T is
  Case-1 with dust exactly 1 per block from m = 5; the landing-pad
  facts LP(α) (completions donated to T at j = 5, 7, 9), LP(β), and
  LP(γ) (brute AP classification over the crown set ∪ {1} up to 512:
  the β family is ALL of it — 6 APs) verified by enumeration.  The
  finite-family dodge stalls exactly as §4.3 says — and then the
  diagonal supply kills anyway: {27, 28} ⊆ T survives the split, and
  R(27, 28; M, {2M−1}) is UNSAT at M = 128 and 256 (the window dust
  being χ3's actual crown-half dust).

Total: 6 solver verdicts (4 UNSAT kills, 2 SAT controls) + the
arithmetic assertions, 7 s.


---

## 7. Status summary and ledger impact

### Proved in this note

| item | statement | where |
|------|-----------|-------|
| Lemma PIN | T-PIN pigeonhole, full restatement + proof | §1.3 |
| DIAG-DENSE | ≥ (2^m − 13)/12 disjoint diagonal usable pairs per block | §2.1 |
| CROWN-2ADIC | even-j crowns = p ≡ 5 (mod 8) diagonal members; odd-j crowns = the open x ≡ 7 (mod 8) cells | §2.2 |
| **Theorem B1** | Case-1 teams are not 3-permutable [modulo (H1)] | §3.1 |
| Cor B1.1 | Case 1 fatal ⟹ every YES-partition is everywhere-split | §3.2 |
| Cor B1.2 | ℤ⁺ not 3-permutable — UNCONDITIONAL (p = 5 instance) | §3.2 |
| Prop B2 + SPLIT-QUANT + B2-VAC | the tasked dichotomy; split branch quantified and proved vacuous | §4.1–4.2 |
| Lemma LP + the descent obstruction | landing-pad arithmetic; finite usable families have a splitter fixed point; no well-ordering exists; density is necessary | §4.3 |

### Machine-checked

e152 (§6): 3 colorings × 2 scales, 4 UNSAT kills (incl. core-targeted
C = 3 punctures), 2 SAT controls, all arithmetic lemma instances.

### Ledger impact (for notes/50 and STATUS.md)

**GAP-BRIDGE1 is DISCHARGED as an assembly gap.**  The notes/50 Case-1
chain item 4 ("Needs: the pair-ownership argument — TAG:
GAP-BRIDGE1") is replaced by Theorem B1, whose only inputs are:

| dependency | = existing tag | exact form needed here |
|------------|----------------|------------------------|
| (H1), uniform p | GAP-N2-DIAG ⊂ GAP-N2(a) | parametric write-up of the e123 diagonal schema, p ≡ 1 (mod 4) only, dyadic scales only |
| (H1), uniform C | GAP-N3 | punctured-rung robustness for the diagonal family at fixed C |

No NEW gap is created; the Case-1 kill chain is now
N1 [HAND] + B1 [HAND, this note] + (GAP-N2-DIAG, GAP-N3).  The
off-diagonal lanes, the x ≡ 7 (mod 8) cells, and the last dyadic
template cells (A4d(19), B6(21)) are NOT on the Case-1 critical path
any more — they matter only for BRIDGE1-AF (anchor-free windows, §5)
and for per-pair completeness of the N2 catalogue.  Conversely
GAP-N2-DIAG is now upgraded from "one of several lane write-ups" to
THE load-bearing rung schema of Case 1 — the parametric diagonal
write-up should be the next N2-front target, ahead of the remaining
off-diagonal cells.

