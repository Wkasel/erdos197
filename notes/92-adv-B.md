# 92 — ADVERSARY B: claims, citations, priority, hedges
# (final pre-publication pass on paper/main.tex EXACTLY AS IT STANDS,
#  sha256 c7ce8aca…, identical to publish/arxiv-bundle.tar.gz:main.tex)
# 2026-08-30

Remit: every sentence that asserts something beyond the paper's own
mathematics.  Sources read directly (papers/*.pdf, OCR of the DEGS77
scan, the live Lean file, erdosproblems.com), not the notes.

---

## 0. VERDICT

**Zero citation errors.**  Every attributed statement I could check is
correct, including two that are *better* than the standard attribution
(the two-set question's origin, and the p. 338 page number).  The
problems are all in the paper's *self*-description: three overclaims
about the machine layer, an under-scoped credit to a named living
mathematician, an attackable "verified by hand" line, one missing piece
of context that a referee will compute in 30 seconds, and a layer of
stale pre-theorem prose.  None invalidates the main theorem.

---

## 1. CITATION AUDIT — all verified

Method: OCR of `papers/DEGS77.pdf` (pdftoppm 250dpi + visual read of
pp. 81–90), `pdftotext -layout` of ErGr79/LV11/Gen18/Gen26/Ad24/HS24,
`curl` of the live Lean file + the formal-conjectures AP library,
`curl` of erdosproblems.com/197 and its forum thread.

| paper's claim | status |
|---|---|
| DEGS77 = Acta Arith. **34** (1977) **81–90** | ✓ (title page = p.81, refs end p.90) |
| DEGS77 proved every ω-permutation of Z⁺ has an **increasing** 3-AP | ✓ Fact 3, p.83: "we always have, in fact, an increasing 3-term A.P." |
| DEGS77 constructed the **three**-set partition | ✓ Concluding remark 3, p.89: A₁=[1,100], \|A_{k+1}\|=⌈(3/2)\|A_k\|⌉, 𝒜=A₁*A₄*A₇…, ℬ=A₂*A₅*A₈…, 𝒞=A₃*A₆*A₉… |
| DEGS77 **asked** whether two sets suffice, Concluding Remarks 3, **p. 89** | ✓ verbatim: "Whether this can be done for some partition of **Z⁺ into two sets** is not known." — note this is *better* than erdosproblems.com, which attributes #197 only to [ErGr79][ErGr80] |
| ErGr79 **p. 338** "a very annoying question" | ✓ — running heads are at page **top** in Enseign. Math.; the paragraph sits on the page headed "- 338 -" (verified by splitting on form-feeds: p.337 head then Pomerance text; p.338 head then the annoying question; p.339 head then Hoffman–Klarner–Rado) |
| parity trick "stated for intervals in DEGS77, which credits earlier notes" | ✓ DEGS77 Intro: "It has often been noted (e.g., see [1],[4],[5]) … n consecutive integers"; [1]=Entringer–Jackson Elem. Prob. 2440, [4]=Odda, [5]=Simmons |
| "for arbitrary finite sets in ErGr79" | ✓ p.337: "possible to arrange **any finite set of integers**… placing all the odd elements to the left…" |
| LV11 exhibited a set with upper density 1/2 **and** lower density 1/4 | ✓ one set: p₀=1,q₀=2, p_k=2q_{k−1}, q_k=3q_{k−1}−1, T=∪T_k, "easy to verify that d̄(T)=1/2 and d(T)=1/4" |
| LV11 "conjectured both bounds sharp" | ✓ "conjecture that the lower bounds in the above theorem are optimal, i.e., α(3)=1/2 and β(3)=1/4" |
| LV11 = Discrete Math. **311** (2011) **205–207** | ✓ |
| Gen26 disproved the upper-density conjecture, α_N(3) ≥ 2/3 | ✓ Thm 1.1 + "The first inequality disproves the equality conjecture of LeSaulnier and Vijay" |
| Gen26 witness = ratio-4 doubling blocks, bottom sliver removed, finitely many octaves per stage | ✓ B_k = ∪_{j=0}^{k}[L_k4^j + M_{k−1}, 2L_k4^j], L_k = 4M_{k−1}, M_k = 2L_k4^k |
| notation α_N(3), β_N(3) | ✓ matches **Gen26** (Gen18 uses α_{Z⁺}); no conflation of Gen18/Gen26 anywhere |
| Gen18 = Discrete Math. **342** (2019) **1489–1491**, arXiv:1803.06334 | ✓ |
| Gen18/Ad24 "constructed permutations of Z and of subsets of Z⁺ avoiding longer monotone progressions" | ✓ Gen18: perm. of Z avoiding 6-APs, β_{Z⁺}(4) ≥ 1/2; Ad24: perm. of Z avoiding 5-APs |
| Ad24 = Discrete Math. **347** (2024) **114183**, arXiv:2211.04451 | ✓ |
| HS24 = Order **42** (2025) **231–239** | ✓ |
| HS24 "characterised the order types … admitting no monotone 3-AP" | ✓ Thm 1.1: chaotic bijection N/Z→X exists iff X has no isolated points; Q→X adds "no max or no min" |
| ABJ11 "chaotic orderings of Q and R" | ✓ exact title, Amer. Math. Monthly 118 (2011) 921–925 |
| zigzag is **classical**: inside DEGS77 in **Folkman's** argument | ✓ p.85: "Proof #1 (J. H. Folkman [2])", relations (4)/(4') = A(a)<A(a+d) iff A(a+2md)<A(a+d+2md) **and** A(a+(2m+1)d)>A(a+d+(2m+1)d); [2] = "J. H. Folkman (unpublished)" |
| … as **Lemma 2.5** of HS24 | ✓ "f(a) ≺ f(a+d) ≻ f(a+2d) ≺ f(a+3d) ≻ ⋯" |
| … as **Lemmas 2.1–2.2** of Gen26 | ✓ 2.1 (2.2)/(2.3) rank alternation, 2.2 the order version |
| Bl: erdosproblems.com/197 states it for **N**, has a Lean formalisation | ✓ live page: "Can $\mathbb{N}$ be partitioned into two sets…"; "Formalised statement? Yes"; the bib entry matches the site's own recommended citation format verbatim |
| FC: path `FormalConjectures/ErdosProblems/197.lean` | ✓ resolves |
| FC statement: `IsCompl A B` on `Set ℕ`, `∃ f : ℕ ≃ A`, `¬HasMonotoneAP (Subtype.val ∘ f) 3` | ✓ verbatim |
| Remark rem:lean: "requires strictly increasing indices whose value list equals (a,a+d,a+2d) or its reverse" | ✓ `HasMonotoneAP f k := ∃ l, (l.map f).IsAPOfLength k ∧ l.Pairwise (·<·)`; `List.IsAPOfLengthWith s l a d := s = (range l).map(n↦a+n•d) ∨ s = (range l).reverse.map(…)` |
| "permits d = 0, but injectivity rules that out" | ✓ d : ℕ, d = 0 forces f(b₁)=f(b₂)=f(b₃) |
| "values live in N, so the common difference is a natural number and never negative" | ✓ α = ℕ |
| ray-piercing kills "even vs odd 2-adic valuation" | ✓ a=1∈A, d=1: v₂(1+2^k)=0 ∀k≥1, so the ray never meets B |

**Not cited, arguably should be (LOW):** Boon Suan Ho, *3AP-free
permutations have no exponential growth rate*, arXiv:2602.13617 (Feb
2026) — the newest paper in this exact niche, already sitting in
`papers/3apfree-growth-2026.pdf`, and it settles the M(n)^{1/n} question
Erdős–Graham raise on the *same page 337* the paper cites.  The intro's
"The modern literature around the problem concerns densities and longer
progressions" is now incomplete by one clause.

---

## 2. FINDINGS (ranked)

### B1 — HIGH. "every negative claim cross-validated" is false, and the paper contradicts it three lines later
§Introduction: "with **every** negative claim cross-validated by
independent encodings and solvers."  Refuted by the paper's own text:
* Prop ogmachine cross-validates the lazy encoding at **M = 40, 44, 128**
  only — 3 of the ~186 scales in the claimed 16 ≤ M ≤ 200 range;
* Thm blockgranular: "F_b … is UNSAT for b = 6 (machine, instant)" — one
  solver;
* Prop ladder rungs is headed "solver-cross-checked", but **L(5)**'s
  lower bound is a single "CDCL, 2304s";
* the machine atlas's "bottom-half relief of depth 1 and depth ≤ 2
  infeasible at N = 256 (and 1024)" lists no second solver.

Fix: "with the load-bearing negative claims cross-validated…", or
enumerate which were.

### B2 — HIGH. "finitely many schema instances" misdescribes an infinite schema
§Introduction: "the reductions and the C3 core theorem are
human-readable arguments, and each of their **finitely many** schema
instances has been machine-audited by three independently written
checkers."  Thm ogred and Thm c3core are ∀M schemas with **infinitely
many** instances; Remark c3machine says finitely many were audited (100
for L1, 51 for FLIP).  As written it reads as a complete audit.
Fix: "finitely many instances of each schema (100 resp. 51 scales,
Remark 39) have been machine-audited…".
Note: the identical wording is already public in the author's
erdosproblems.com/197 comment of 26 Aug 2026 — fix both.

### B3 — HIGH. Data availability over-promises the certificate coverage, and the one load-bearing machine step has no certificate
Repo contains exactly two DRAT files: `data/certs/c3_M{128,512}.drat`,
both certifying **C3-UNSAT** — which Remark c3machine explicitly
demotes: "The earlier exhaustive base ledgers … are now
**corroboration, not a dependency**."  Meanwhile:
* **Lemma bases** (Z(M) UNSAT, 16 ≤ M ≤ 31) *is* a dependency — Theorem
  contig consumes it — and has **no certificate, no script, no
  reproduce.sh step** (the five steps are e113-subset, e113b, e115
  direct SAT, DRAT re-emission, e96; `grep -i zone REPRODUCE.md
  reproduce.sh` → nothing);
* Prop ogmachine's 16..200 sweep, Prop cores' sweeps, the machine atlas
  (window-2 at N=1024), the ladder rungs, the deferral states, the
  self-similar witnesses, the S_B mirror at 4096 — none certified, none
  in reproduce.sh.

So "DRAT certificates for the finite base cases" / "The DRAT
certificates cover the finite base instances only" / "reproduce.sh, a
single script that re-runs **the complete verification stack**" all
overstate.  Fix: name the two C3 instances; say reproduce.sh re-runs
**the main-theorem chain**; and either certify Lemma bases or flag
Theorem contig as resting on an uncertified machine verdict.

### B4 — HIGH (integrity/optics). No Acknowledgements; Geneson's credit is under-scoped in a way that reads as endorsement
The paper has **no Acknowledgements section**.  Jesse Geneson appears
only in two footnotes, each thanking him for one specific correction
(the symmetric balance misstatement; the general-m class-sink form).
Per `STATUS.md`'s own provenance rule, his Aug 27 external review covers
`paper/main.tex` as a whole and prompted at least six fixes.  The
current arrangement simultaneously *under*-credits him and lets a reader
infer that a named expert vetted the main theorem.
Fix: an Acknowledgements section that states the scope explicitly —
what he reviewed, what he corrected, and that responsibility for all
claims including Theorem main is the author's alone.  (The scoping
sentence currently lives only in the repo's STATUS.md; it belongs in
the paper.)

### B5 — HIGH (integrity/optics). "All proofs have been verified by hand" in the same footnote as the AI disclosure
Author footnote: "With extensive machine assistance from Claude
(Anthropic) … **All proofs have been verified by hand** unless
explicitly marked as machine-checked."  A hostile reader will ask
*whose* hand.  On a solo AI-assisted preprint claiming an
Erdős-adjacent theorem this is the single most attackable line in the
document.  Fix: state what was done by whom, e.g. "the arguments of
§§7–9 are human-readable and were checked line by line by the author;
solver output is relied on only where explicitly marked."

### B6 — MEDIUM. The paper omits the two density facts that justify its own central framing
A referee computes these in 30 seconds; I verified numerically at
n = 2^21: **d̄(S_A) = 2/3, d(S_A) = 1/3** (0.666666 / 0.333333), and the
same for S_B.  Consequences the paper does not draw:
1. **S_A sits exactly at Geneson's record upper density 2/3.**  The main
   theorem therefore exhibits a *specific* set at the record density
   that is not permutable — a far sharper contrast than the current
   "the mechanisms align strikingly" paragraph.
2. **(S_A, S_B) sits exactly on LeSaulnier–Vijay's necessary condition.**
   LV11 p.207 (restated in Gen18's intro) observes the answer to #197 is
   NO if α(3)+β(3) < 1; here 2/3 + 1/3 = 1 **on the nose**.  *That* is
   the citable justification for "canonical".
Right now "the natural first candidate", "the canonical dyadic
partition", "the leading candidate", "the natural YES route" are
asserted with no citation and no computation, and "implicit already in
the parity heuristic of [DEGS77]" is an unsupported attribution.  A
hostile referee will ask "canonical according to whom?"  Two sentences
with these densities + the uncited LV α+β ≥ 1 remark converts the
weakest framing claim in the paper into the strongest.

### B7 — MEDIUM. Stale pre-theorem prose that now reads as self-contradiction
* §Local realizability: "Divergence of g_X(L) in X for fixed L would
  prove non-permutability; the mechanism is blocked by the measured
  subset-tolerance (near-total), and **g is expected to stabilize**."
  Theorem main proves S_A is *not* permutable and the Tower
  characterization is an **iff**, so the tower must fail.  It is not a
  formal contradiction (per-L stabilization of g_X(L) does not by itself
  produce a single B, because the minimizing arrangements vary with L),
  but the paper never says so, and every referee will stop here.
  Either delete, or add that one sentence.
* §Negative atlas: "The surviving candidate shapes for a YES are …; the
  surviving NO program is to close the gap …" — reads as a progress
  report written before the theorem existed.
* §"Historical note: suffix-stacked deferral" — one unsupported,
  near-unparseable paragraph ("no closed-form law survived depth 4",
  "prefix-nested semantics permit top-half deferral that rigid chunks
  forbid") that adds nothing and invites attack.  Recommend deleting.

### B8 — MEDIUM. Unhedged generalizations from finite experiments; "to our knowledge" appears **zero** times
* "Radius-1 robustness is thus **unachievable generically** in three-AP
  arrangement problems and cannot serve as a satisfiability criterion" —
  asserted from "infeasible in every setting we tested".  (The
  walk-back two sentences later makes the assertion look worse, not
  better.)  → "appears to be unachievable".
* "**any** single residue class serves as the deferred suffix, while
  generic sets of the same size do not" — universal, from M = 32,64,128.
* "the same lemmas hold **verbatim** for S_B (machine-verified mirror at
  4096)" — one data point.
* "the methods here … **apply to** any two-set partition whose parts are
  unions of intervals" — nothing in the paper proves this. → "should
  apply".
* **Prop cores** still reads as an unrestricted ∀M theorem: "infeasible
  with (i) **exactly when** M ≡ 0 (mod 4)" and "**exactly when**
  M ≡ 0 (mod 8)".  The "at every tested scale" retraction was installed
  in the abstract and intro but **not here**; the prefix "hold at every
  swept scale" is doing too much work.  Scope each clause explicitly.
* The one explicit novelty claim — "what is new here is its
  boundary-quantitative use on bounded ladders, the transfer lock, and
  the flood induction" — has no "to our knowledge".  `grep -c "to our
  knowledge" paper/main.tex` → **0**.

### B9 — MEDIUM (operational). The cited repo is 5 commits behind the paper
`git ls-remote origin HEAD` = **15339b7**; local HEAD = **8abd6b2**;
`git rev-list --count origin/main..HEAD` = **5**, plus 3 uncommitted
modified files under `data/`.  Release **v1.0** is dated 2026-08-25 —
*before* integrity-patch items 2–8, i.e. before the very corrections
this review round installed.  Posting now makes
`https://github.com/Wkasel/erdos197` resolve to a state that contradicts
the paper.  Push, and tag a v1.1 pinned to the arXiv version.

### B10 — MEDIUM. The author's own public comment still carries a retracted overclaim
erdosproblems.com/197, comment by `wkasel`, 00:38 on 26 Aug 2026, still
says the mod-8 condition is "**sharp: satisfiable at every other
residue**" — the unrestricted sharpness claim the paper has since
retracted to "at every tested scale" — and repeats the "finitely many
schema instances" wording of B2.  A referee following the paper to the
problem page sees the stronger claim.  Post a correcting reply with the
arXiv ID.

### B11 — LOW. Precision nits
* Abstract: "every step is machine-verified at **100 scales** up to
  M = 1024" — 100 is the L1 figure; FLIP is 51 (Remark c3machine).
  Say "100 resp. 51".
* Abstract's bold conclusion "**S_A admits no permutation free of
  monotone 3-APs**" drops "of order type ω", which Theorem main, Remark
  rem:lean and the HS24 paragraph all keep — and HS24 Thm 1.1 shows
  AP-free orders of *other* order types do exist on N.  Restore it.
* The Geneson paragraph says the same thing twice with two colons:
  "…lives precisely in the region Geneson's construction excises: the
  two results are consistent, and the mechanisms align strikingly: the
  attacks … are concentrated in the same bottom regions removed in
  Geneson's construction."  Collapse.
* "$[L\cdot 4^j + m,\ 2L\cdot 4^j]$" — the lowercase $m$ is undefined;
  Geneson's own symbol is $M$ (= $M_{k-1}$), silently re-cased to dodge
  the collision with the paper's $M$.  Say so.
* "the theorem of [DEGS77] … has a **four**-line proof" — Thm degs's
  proof is six lines; and it applies conditions (A)/(B), defined only
  for stage functions $s\colon S_A \to \N$, to $\Z^+$ without comment
  (the necessity direction is general — say so).
* Thm divergence: "the **ten** displacements δ(3), δ(4), …, δ(16)" — the
  ellipsis reads as fourteen values; only ten lie in S_A
  ({3,4} ∪ {9,…,16}).  Spell the set out.
* Deferral-state definition uses $2^{k/2}$ with $k$ undefined there.
* `\newtheorem{question}` and `\newtheorem{conjecture}` declared, never
  used.
* Bib [ErGr80]: the repo's copy is
  `Erdos-solo-problems-results-NT-graphs-MISLABELED-not-ErGr80.pdf`, i.e.
  the monograph was never actually consulted.  The citation is standard
  and erdosproblems.com lists it, so it is safe — but it is uncheckable
  by the author, so keep it as "see also".

---

## 3. INDEPENDENT MACHINE RE-VERIFICATION (fresh encoder, pysat/CaDiCaL,
##    lazy transitivity — written from the paper's definitions only)

| claim | scales tested | result |
|---|---|---|
| AP ∧ C3 | 16 ≤ M ≤ 72, all residues | UNSAT **exactly** at M ≡ 0 mod 8 ✓ |
| AP ∧ full OG(M) | 16 ≤ M ≤ 60 | UNSAT at every M ✓ |
| AP ∧ 4-unit core {t₁₃≺b₁,t₁₁≺b₂,t₅≺b₅,t₁₀≺b₃} | 40 ≤ M ≤ 72 | UNSAT **exactly** at M ≡ 0 mod 4 ✓ |
| AP ∧ 11-unit core 15{1..7}∪16{1..4} | 40 ≤ M ≤ 60 | UNSAT at every M ✓ |

Arithmetic re-derived by hand:
* t_{x−2j} = 2M−x+2j = 2b_j − x ✓; in-block ⟺ j ≤ x/2 ✓; 7+8 = **15**
  axioms ✓; C3 = instances (x,j) = (15,5),(15,6),(16,3) ✓.
* Degeneracy M = x−j ≤ 15 ✓ (t₁₄ = b₁ at M = 15 comes from x=16, j=1 ✓);
  guard = *other* bottom requires M = x−2j+i ≤ 16−2+8 = **22** ✓.
* Prop ogmachine's eager OG(128) clause count: 2·4032 AP + 2·C(128,3) =
  682,752 transitivity + 15 units = **690,831** — exactly the printed
  figure ✓.  (`data/certs/README.md` prints 690,819 for C3-M128;
  difference = 12 = 15−3 units ✓.  Internally consistent.)
* Remark c3machine scale counts: M ≡ 0 mod 4 in [12,400] = 98, +512,1024
  = **100** ✓; M ≡ 0 mod 8 in [16,400] = 49, +2 = **51** ✓.  The "35
  scales" for the M ≡ 4 mod 8 inapplicability check has **no stated
  range** (M ≡ 4 mod 8 in [12,400] is 49) — state it.
* d̄(S_A) = 2/3, d(S_A) = 1/3 (numerically, n = 2^21).
* Lemma orbit ⇒ DEGS: S = Z⁺, F = {1,2}, orbit u_{k+1} = 2u_k − 1 from
  u₀ = 2 ✓.

Packaging: `publish/arxiv-bundle.tar.gz` contains exactly one file,
`main.tex`, sha256-identical to `paper/main.tex` ✓.  Only non-ASCII
characters are 19 em dashes + 3 en dashes (safe under pdflatex ≥ 2018;
the shipped PDF was built with XeTeX — `Producer: xdvipdfmx`).  No
unresolved `??` references in the PDF; 18 pages.

---

## 4. PRIOR-ART / PRIORITY SWEEP — clean

Searched arXiv (`all:"monotone arithmetic progressions"` → 3 hits:
Gen26, Ad24, Adenwalla 2302.09662), the Discrete Math / Order / Monthly
line, and erdosproblems.com/197's comments and forum thread.

* **No prior work proves a specific infinite subset of Z⁺ non-permutable
  other than Z⁺ itself** (DEGS Fact 3, generalized here as Lemma orbit).
  The trivial route — an infinite reflected orbit u_{k+1} = 2u_k − f
  inside S — provably fails on S_A, since doubling carries B_{2t} into
  the odd block B_{2t+1}; the paper says this and it is correct.  The
  novelty claim is defensible.
* **No prior work proposes or eliminates the dyadic partition.**  LV11's
  witness is p_k = 2q_{k−1}, q_k = 3q_{k−1}−1 (ratio ≈ 3/2 blocks);
  Gen26's is ratio-4 blocks minus slivers; neither is S_A.
* **Nothing equivalent to the OG reduction exists in the literature.**
* Adenwalla 2302.09662 (4-APs with restricted common difference) is
  subsumed by the cited Ad24 — safe to omit.
* Priority is already established publicly: the erdosproblems.com
  comment of 26 Aug 2026 and the v1.0 release of 25 Aug 2026 predate
  the arXiv post.

---

## 5. ONE-LINE SUMMARY FOR THE AUTHOR

Citations are clean — do not touch them.  Before posting: fix the three
machine-layer overclaims (B1–B3), add a scoped Acknowledgements and
rewrite the "verified by hand" footnote (B4–B5), add the two density
sentences that justify "canonical" (B6), delete the three stale
paragraphs (B7), hedge the five universals and add one "to our
knowledge" (B8), and **push the repo** (B9).
