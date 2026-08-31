# 90 — INTEGRITY PATCH (second external adversarial review)

Terse stream; one commit per item.  Scope: integrity only — no new
mathematics; wrong statements fixed, stale statements quarantined.
First-review remediation log: notes/88.  Items numbered as in the
review.

## Item 1 — paper2 H1 → H1′ (Theorem B did not follow from its
## stated hypotheses)

The flaw: paper2's H1 quantified "for every fixed p ≡ 1 (mod 4) and
every C ≥ 0", but N3-GROW is robust only for |D| < ⌊(x−1)/4⌋ at
x = 3p — finitely much dust per fixed p — and the fixed-p uniform-C
form is machine-REFUTED at p = 5, C = 3 (e174: {15,16} admits
3-puncture escapes at every dyadic scale tested; notes/74).  So
Theorem B's proof-shape line "(H1) = C3(p) at C = 0 + N3-GROW at
C > 0" was false as written.

Fix applied to paper2/main.tex (compiles, tectonic):

* def:h1 replaced by **H1′**: for every C ≥ 0 there is x₀(C) s.t.
  for every p ≡ 1 (mod 4) with 3p ≥ x₀(C) there is m*(p, C) with
  R(3p, 3p+1; 2^m, D) inconsistent whenever m ≥ m*(p, C) and
  |D| ≤ C; under N3-GROW take x₀(C) = max{11, 4C+5} (then
  C < ⌊(3p−1)/4⌋).  New Remark rem:h1prime records the fixed-p
  refutation so the old form cannot silently return.
* B1 pair-extraction patched (matches notes/74 §I.4): require
  2^{m₀} ≥ max{12C₀+25, x₀(C₀)}; DIAG-DENSE then supplies
  ≥ C₀+1 > C₀ disjoint usable pairs, one survives the dust, and
  3p > 2^{m₀} ≥ x₀(C₀) puts it in H1′'s range.
* Assembly proof shape now derives H1′ (not H1) from C3(p) at
  C = 0 plus N3-GROW at C > 0 with the explicit x₀ arithmetic;
  dependency graph label updated.
* Theorem A / B1₀ (zero-dust) untouched — its direct proof consumes
  PIN at C = 0 + DIAG-DENSE + C3(p) only, no H1′.

## Item 2 — Lemma LAND (notes/84 §1.2) false as originally stated;
## fixed to the prescribed form + machine-checked

Reviewer counterexample (σ = −1): q = 1, p = 4, g = 3, r* = p = 4,
τ = 8, h = 14 ⟹ δ₀ = −3, δ₁ = +3 — kills any unscoped
δ_{n+1} ≤ |δ_n|/2 claim.  State of the repo: the σ = +1 scoping of
(b1)-(b2) had been added at commit a7616eb (which also completed
the S1 window bound, removing the unfinished "≤ … < w−u" fragment);
this item conforms the text EXACTLY to the reviewer's prescription
and adds the missing pieces:

* §1.2(b) now displays the general bound |δ_{n+1}| ≤ (|δ_n|+g)/2 as
  THE only both-σ bound; (b1) states the positive-deviation bound
  as an equality, σ = +1 only: δ_{n+1} = |δ_n|/2 (even) or
  (|δ_n|−g)/2 < |δ_n|/2 (odd).
* New Warning block records the σ = −1 counterexample verbatim and
  the history (earlier unscoped draft = false; caught by second
  review).
* §1.3 S1 admissibility recast per prescription: A := |δ₀| =
  (t+r₀)/2; (C1) ⟹ g | A ⟹ A ≥ g ⟹ D = A; positive deviations
  ≤ A/2; two-case A/2 < w − u = t + q (r₀ = q: A/2 = (t+q)/4;
  r₀ = p: t + q ≥ g ⟹ A/2 = (t+q+g)/4 ≤ (t+q)/2).
* Machine check experiments/e191_land_s1_check.py [PASS]:
  10⁴ random tuples per σ — general bound, σ=+1 refinements,
  landing K ≤ |δ₀/g|+2, sup, orbit min, mod-g exactness all 0
  failures; σ = −1 half-bound violations 451 485 found (scoping
  necessary; reviewer tuple reproduced through the real spiral
  map); S1 re-verified on 10⁴ fresh admissible tuples by direct
  forced-spiral simulation, 0 failures.
  data/e191_land_s1_check.json.

## Items 3-5 (HSPLIT quantifiers, aperiodicity, L-NOTAIL)

**Item 3 — HSPLIT quantifier discipline.**  Exact sanctioned
wording now carried in notes/81 §3, notes/83 §0 + §0b, notes/50,
STATUS: *"At F = 64, horizons 2048 and 4096, every coloring
satisfying the remaining proxy constraints has at least one
monochromatic mod-4 class-section among the tested blocks."*
Three scope notes stated at each site: HSPLIT-as-constraint bans
ANY coloring with even one pure tested section (not only
lattices); the hard-coded burn-in t = 6 does not capture the
correct eventual quantifier; the depth-2 orbit censor is a proxy.
notes/83 §0b's blind-drafted "every finite inhabitant is a
mod-2^k near-lattice" inference is struck in place.  paper2 makes
no machine-HSPLIT claim (only the PROVED Cor. HSPLIT) — nothing
to fix there.
**New experiment (reviewer-suggested), e186 `hsplitburn`:** HSPLIT
imposed only for T ≤ t ≤ log2(H) − 1, T ∈ {6, 8, 10} ×
H ∈ {2048, 4096}, strong censor F = 64.  **UNSAT ×6** (16.5/40.0,
19.3/38.6, 20.0/36.8 s; 172 s total).  Reading per cell is the
sanctioned finite-scope sentence with "tested blocks" =
[T, log2(H)−1]; higher T tests fewer blocks, so the cells get
weaker, not stronger.  Six instances are not the ∀T family and no
compactness step exists — ω verdict unmoved.  notes/81 §3b.

**Item 4 — "HSPLIT ⟹ aperiodic".**  The first-review pass had
already retracted it (mod-3 counterexample verified).  Added the
prescribed POSITIVE replacement at every site (notes/50 ×2,
notes/82, notes/86, notes/89, STATUS, paper2 hyp:afford):
*"HSPLIT imposes hereditary 2-adic mixing; combined with L-NOTAIL,
a valid pair cannot be globally periodic."*  (Justification, no
new mathematics: period P ⟹ each team is a finite union of
classes mod P ⟹ each team contains an infinite AP ⟹ L-NOTAIL.)

**Item 5 — L-NOTAIL's second proof was invalid.**  Lemma Q only
kills APs whose common difference is a power of two, so
"L-NOTAIL = corollary of Lemma Q" is false in general.  Replaced
in paper2 cor:notail and in notes/50, notes/82, notes/86 with:
*"Proof: DEGS77, applied after restricting to the progression and
transporting by its affine parametrization.  When the common
difference is a power of two, HSPLIT gives an alternative
proof."*  notes/80-pincer §3.1's own proof was always the DEGS77
one — unchanged.

## Item 6 — portability + boundary honesty + reproduce2

* **Portability.** e123 / e123b / e180 converted to the prescribed
  idiom `ROOT = Path(__file__).resolve().parents[1]` (they were
  already repo-root-relative via `__file__` after the first
  remediation; this makes the intent explicit and is smoke-tested
  from a foreign cwd).  e191 (new) uses it natively.
* **Boundary honesty.**  e180 DOES assert the stated boundaries:
  `partMINMsharp` computes first-pass scales FROM the scan and
  asserts them equal to the sharp affine values (L1: first
  4 | M ≥ p+7; FLIP: in-class M ≥ 2p+6), with every scanned
  below-threshold scale checked to FAIL — re-run this session at
  p = 5/13/21, 0 mismatches.  notes/78 already attributed the
  claim correctly; paper2's unattributed "e180 exact boundary
  scan" now names `partMINMsharp`, states both boundaries and the
  below-threshold check, and records that the legacy `partMINM`
  asserts only the slack bounds 2p+10 / 2p+14.
* **reproduce2.sh** already covered C3(p) at 3 values of p (e123
  schema p = 5,7,9; e123b independent solver p = 5,9,13), B1₀'s
  machine layer + Lemma Q chart checks (e186 qverify/geneson), and
  HSPLIT-as-downgraded (e186 hsplit64 + ctl).  Added **step 6** =
  e191 (LAND corrected bounds + S1).  Run end-to-end this session:
  **6/6 PASS, 115 s, exit 0.**  REPRODUCE.md package-2 section
  updated: verbatim HSPLIT reading + three scope notes, the
  hsplitburn probe, step 6, new wall time, portability note.

## Item 7 — archival banners

The first remediation (notes/88 item 4) had banners on notes 04,
05, 06, 08, 12, 16, 17, 19, but each was file-specific and none
carried the standard header line.  Prepended VERBATIM to all eight,
above the existing specific banner (which is kept — it says what
exactly is false):

  **ARCHIVAL / SUPERSEDED. Contains statements later shown false.
  Do not use as a dependency. See paper/main.tex and STATUS.md for
  the current formulation.**

Re-swept notes/01-30: no other file carries a known-false claim
without a banner.

## Item 8 — percentage + provenance

* **Percentage.** The "NO ≈ 96–97 %" text in FRONT ALT-CLOSURE is
  DELETED (it survived the first pass only as "the original
  headline is retired", i.e. the number was still on the page).
  Replaced by the prescribed sentence: *"The conditional
  architecture is increasingly constrained, but three substantial
  hypotheses remain: N3-GROW, N6a closure, and AFFORD′."*  A
  standing percentage rule at the top of STATUS makes this the
  claim-grade summary and denies claim status to every historical
  "NO ≈ X %" line.
* **Provenance.** "professor pass" / "referee prose pass" →
  **internal adversarial prose audit** (STATUS ×4 incl. the FRONT
  ALT-CLOSURE and FRONT AUDIT headings, paper2 \source, notes/86
  title).  New standing provenance rule at the top of STATUS states
  explicitly: these are SELF-reviews, no external referee involved;
  **Geneson's external review (Aug 27) covers the original paper
  (paper/main.tex) ONLY — not the Part II chain** (paper2, Case-2
  machinery, AFFORD/N6a/N3-GROW, notes above 50); the two
  adversarial reviews in notes/88 and notes/90 are critiques of the
  write-up, not endorsements of the mathematics.
