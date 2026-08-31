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
