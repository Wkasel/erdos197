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
