# Adversary A — proof correctness, final pre-publication pass

Target: `paper/main.tex` exactly as staged (identical to `publish/arxiv-bundle.tar.gz`;
verified byte-identical). PDF has 0 undefined refs, 0 dangling `\ref`, 0 dangling
`\cite`, no duplicate labels.

## Verdict on the main chain

**No correctness defect found in thm:chunk → thm:ogred → thm:c3core (L1 + FLIP +
ladder toolkit).** Every hypothesis is used, every proof proves its stated
statement, and I found no unstated finiteness / genericity / non-degeneracy
assumption that fails at any admissible scale. All findings below are
expository, attribution, or side-theorem issues.

### Independent machine verification I ran (my own encodings, not the repo's)

Eager `O(n^3)` transitivity + AP-free + unit axioms, CaDiCaL via pysat:

| check | result |
|---|---|
| AP ∧ C3, M = 16..60 | UNSAT exactly at M ≡ 0 (mod 8); SAT at all 7 other residues |
| AP ∧ C3, M = 64,72,88,104,120,**128** | UNSAT (128 = first dyadic scale) |
| AP ∧ C4 (4-unit core), M = 40..100 | UNSAT iff M ≡ 0 (mod 4) — matches prop:cores on its swept range |
| AP ∧ 11 attack units, M = 40..100 ∪ {104,108,112,120,128,150,200} | all UNSAT |
| AP ∧ OG(M), M = 16..80 ∪ {100,128,150,200} | all UNSAT |
| Z(M) zone system, M = 16..31 | all UNSAT (lem:bases confirmed); Z(12..15) SAT, so the base window is tight |
| thm:vdc, k = 2..9 exhaustive | 0 violations |
| thm:chunk iff, 20 000 random (s, fiber-order) on {1..12} | 0 mismatches |

Hand-proof reconstruction, **independent closure engine** (R1–R4 on genuine
in-block APs + transitivity fixpoint only, phase splits by lem:phase):

* **Case-tree exhaustiveness**: for L1 (seeds A2,A3,S) and FLIP (seeds A1,A2,A3,
  b5≺b3), each of 2 cases × 8 phase branches (even-d2 × classA-d4 × classB-d4)
  is refuted at **M = 16, 24, 32, 40**. No branch survives.
* **Each individual flood step of the written proof** (POLAR in/out; L1-I(1)(2),
  L1-II(1)(2); FLIP-I(1)(5), FLIP-II(1)(5)) is derivable in **both** phase
  branches at **M = 16, 24, 32, 40, 56, 128**. Phase-blindness confirmed.
* Boundary arithmetic re-derived by hand and confirmed: mirrors
  {t1,t5}, {M+8,M+12}, {b1,b5}, {2M−8,2M−4}, t7, b7, M+8, 2M−4 all land in
  (M,2M]; pair distance M/2−6 ≡ 2 (mod 4) at M ≡ 0 (mod 8); e0 = M/2−5 odd and
  admissible for M ≥ 12; all cycle members pairwise distinct.
* thm:ogred re-derived line by line: guard identity t_{x−2j} = 2b_j − x, the
  in-block window j ≤ x/2, guard ≠ bottom (M ≠ x−j), j ≤ 8 covers both x, the
  disjointness of {M+1..M+8} across t, and the finite-position overflow. Sound.

## Findings (severity ordered)

### A1 — MEDIUM (attribution/priority). thm:vdc duplicates a cited paper's lemma.

`\begin{theorem}[van der Corput absorption]\label{thm:vdc}` (main.tex L300–314)
is mathematically **identical** to Lemma 2.1, eq. (2.2), of Geneson
[Gen26] — which the paper cites. Under the bijection c ↦ α=(c−1)/2 from odd
residues mod 2^k to Z/2^{k−1}, "a ordered before b ⇒ 2b−a strictly before b"
is exactly `ρ_m(r) < ρ_m(r+δ) ⟺ ρ_m(r+δ) > ρ_m(r+2δ)` with r=α, δ=β−α.
Geneson further attributes the underlying binary recursion to Davis et al.
[DEGS77, p. 81], Ardal–Brown–Jungić [Def. 2.1–2.2] and Nathanson.
The abstract advertises it as a contribution ("We also prove a clean absorption
theorem for van der Corput orderings of odd residue classes"). No citation
appears at the theorem. The intro **does** credit Gen26 Lemmas 2.1–2.2, but only
for lem:zigzag, in a different section.
Risk: Geneson is thanked twice in the paper and is the obvious referee.
Fix: demote to a Lemma, cite [Gen26, Lem. 2.1] (+ classical sources), keep the
short proof as "for completeness", and soften the abstract sentence.

### A2 — MEDIUM (internal inconsistency; the mod-8 narrative overreaches).

main.tex L1035–1039: *"At M ≡ 4 (mod 8) both congruences fail (and the odd-ladder
leader statuses at m0±1 invert), the flood seeds do not exist, and **the proofs
below evaporate**"*.

Theorem L1 is stated and proved immediately below for **M ≡ 0 (mod 4)**, and
explicitly covers M ≡ 4 (mod 8) via the c\*/c\*\* swap. So "the proofs below
evaporate" is false for the first of the two theorems it refers to.
Machine-confirmed: L1's two cases are refuted in all 8 phase branches at
M = 20, 28, 36, 44 (M ≡ 4 mod 8); FLIP's are not (branches survive at all four).
Second inaccuracy in the same sentence: at M ≡ 4 (mod 8) the two G4-centres
still exist — m0−1 ≡ 1 and m0+1 ≡ 3 (mod 4) — with the class-A/class-B roles
**swapped**; it is not that "the seeds do not exist". What actually breaks is
only FLIP (the closing paragraph of §flip states this correctly).
Fix: scope the sentence to thm:flip, and say the centres swap classes while the
odd-ladder leader statuses invert, so the FLIP seed set is not simultaneously
available.

### A3 — LOW/MED (literal self-contradiction in one sentence).

main.tex L616–621: *"**window-2 infeasible at N=1024** … — hence dead at every
horizon; window-2 at N=256 **is feasible** only via whole-block merges"*.
"Dead at every horizon" contradicts the clause after the semicolon. Intended:
"dead at every horizon ≥ 1024, hence no infinite window-2 solution exists".

### A4 — LOW. "$3$-permutable" is never defined.

§2 defines *permutable*. "$3$-permutable" is then used in thm:chunk (L506),
thm:degs (L559), thm:divergence (L658), thm:ogred (L725) and **thm:main (L846,
the Main Theorem statement)**. thm:main glosses it in the next clause; thm:ogred
does not. Add "ℓ-permutable" (Geneson's notation) to §2 or drop the "3-".
Related nit: thm:chunk's closing sentence should read "some stage function
*together with fiber orders* satisfies (A) and (B)".

### A5 — LOW. Range of k in the definition of S_A is unspecified, and the two
readings give different arithmetic in the paper.

`\SA = \bigcup_{k \text{ even}}(2^{k-1},2^k]` (L130, L207, L846) never says
whether k = 0 is included.
* k ≥ 0 ⇒ 1 ∈ S_A. Then S_A ∩ [1,16] has **eleven** elements, contradicting
  thm:divergence's "the **ten** displacements δ(3), δ(4), …, δ(16)" (L662–664),
  and g_256(64) = 153 gives 110/128 = 86% not the stated "eighty-seven percent"
  (L393–395).
* k ≥ 2 ⇒ 1 ∈ S_B, and then S_B = {1} ∪ B_1 ∪ B_3 ∪ … is *not* a union of
  doubling blocks, straining "each team is a union of doubling blocks" (L133).
Both the "ten" and the "87%" pin the intended convention to k ≥ 2; say so.
Immaterial to thm:main (thm:ogred uses only 15, 16 and B_{2t}, t ≥ 4), but a
referee will spot the count. Also L(m)'s `\max_{v \le 16}` should say
"v ∈ S_A, v ≤ 16".

### A6 — LOW. Spurious/undefined O(1) in lem:balance and cor:records.

L263–264 states `H − L ≤ |S^c ∩ (0,v)| + O(1)` — O(1) in *what* parameter?
The proof (L275–279) is exact: for every already-placed u ∈ (v,2v) the
completion 2v−u lies in (0,v), the map u ↦ 2v−u is injective and never hits v,
so `L ≥ H − |S^c ∩ (0,v)|` with **no** error term. Same in cor:records, where a
left-to-right maximum has H = 0 and the bound is simply
`L ≤ |S^c ∩ (v,2v)|`. Delete both O(1)s; the lemma gets *stronger*.

### A7 — LOW. thm:blockgranular omits its only infinitary step.

L603–604: *"Any block-granular scheme has a fiber boundary above block 4 and
therefore contains some F_b."* Asserted without argument. It is true and
one line — if s(B_{2k}) ≤ s(B_{2k−2}) for all large k, the stages are eventually
constant and infinitely many blocks share one fiber, contradicting finiteness —
but that is the **only** place fiber-finiteness enters the theorem, so it should
be written.

### A8 — LOW. Half of a claimed equality is undocumented.

Prop [Ladder rungs] (L646–655) asserts **L(4) = 2**, but only the lower bound is
supported (cap δ ≤ 1 on {v ≤ 16} infeasible at N = 256). The only upper-bound
witness reported anywhere is the window-3 witness at N = 1024, which gives
L(4) ≤ 3 (L is monotone in m, so L(4) ≤ L(5) = 3). Either cite a δ ≤ 2 witness
at N = 256 or write "L(4) ≥ 2".

### A9 — LOW. Undefined terminology in §"Suffix-stacked class deferral" and
lem:bottomhalf.

* "**doom-free** arrangement" (L448) — never defined anywhere in the paper.
* modulus "**m(M)**" (L446) — never defined.
* "{v ≡ 2 mod 2^{k/2}}" (L447) — **k** is unbound (presumably M = 2^k).
* lem:bottomhalf (L587): "**by uniform delay**" and "**is (A)-clean**" — neither
  defined. (The stated arithmetic is correct: for x ≤ 2^{k−2} and
  z ∈ (2^{k−1}, 3·2^{k−2}], the midpoint y = (x+z)/2 lies in (2^{k−2}, 2^{k−1}],
  the odd block below. But the hypothesis "x in a lower block" needs to be
  "x ≤ 2^{k−2}".)
* §Historical note (L1202–1206): "**the law**'s witnesses" — no antecedent.

### A10 — LOW. Abstract overstates the audit; one theorem is stated for the
wrong ground set.

* Abstract L68–69: "every step is machine-verified at 100 scales up to M = 1024".
  rem:c3machine gives **100** scales for L1 but **51** for FLIP. Say "at 100 and
  51 scales respectively".
* thm:degs applies condition (A) to **Z^+**, but thm:chunk is stated only for
  S_A ("no AP triple (x,y,z) in $\SA$"). The chunk proof is generic; state
  thm:chunk for an arbitrary S ⊆ Z^+ (costs nothing) or add a sentence.
* Abstract (i) says "no infinite doubling orbit"; lem:orbit's hypothesis is the
  *increasing* orbit u_0 < u_1 < ⋯. Say "increasing".

### A11 — COSMETIC.
thm:degs, thm:blockgranular, thm:divergence carry their proofs *inside* the
theorem environment ("\emph{Proof:} … \qed"), so they typeset in theorem body
style. Referees dislike this. Also, ten labels are defined but never `\ref`ed
(thm:vdc, thm:contig, thm:degs, thm:divergence, lem:ray, lem:balance,
cor:records, lem:sameblock, rem:lean, rem:c3open) — harmless.

## Things I checked that are FINE (do not "fix")

* lem:orbit, lem:R, lem:halving (incl. the odd-M boundary case: for M odd the
  interval ((M−1)/4, M/4] contains no integer, so no zone constraint is lost),
  thm:contig's descent, the tower characterization's König argument (levels
  finite, restriction maps well-defined by horizon collapse, per-v predecessor
  counts monotone and bounded ⇒ type ω), lem:normal, thm:restriction,
  thm:divergence's logic, prop:ogmachine's "lazy transitivity is sound for
  UNSAT", the class-sink conjugacy, ray piercing, rem:lean's 0-adjunction
  argument, the "completion lands in the adjacent block" sentence, the guard
  boundary arithmetic in §og, and thm:main's assembly.
* Literature: ErGr79 "a very annoying question" verified in the PDF (p. 338
  region); Geneson α_N(3) ≥ 2/3 verified; LeSaulnier–Vijay 1/2 & 1/4 with the
  sharpness conjecture verified; DEGS's *increasing* 3-AP form corroborated by
  LV's rendition of the argument; the description of Geneson's witness
  ([L4^j + M, 2L4^j], finitely many octaves per stage, bottom sliver removed)
  is accurate; HS24 Lemma 2.5 and Gen26 Lemma 2.2 are indeed the zigzag
  alternation. Repo URL and erdosproblems.com/197 both return HTTP 200.
* arXiv bundle main.tex is byte-identical to paper/main.tex.

## Bottom line

Nothing here invalidates the Main Theorem. A1 and A2 are the two I would fix
before posting: A1 is a priority/attribution hazard with the most likely
referee, A2 is a claim in the paper that the paper's own next theorem refutes.
A3–A5 are the sort of thing a hostile reader quotes. Everything else is polish.
