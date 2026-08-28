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
