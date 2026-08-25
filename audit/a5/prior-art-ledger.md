# Audit A5 — prior-art / novelty ledger (2026-08-25)

Machine-record of the searches behind the A5 novelty verdict. Findings and
compliance evaluation are in the A5 structured report returned to the
orchestrator; this file is the citation-sweep evidence trail.

## Complete citation sweep of DEGS 1977 (Semantic Scholar, 41 citers, all reviewed)

Paper: Davis–Entringer–Graham–Simmons, Acta Arith. 34 (1977) 81–90,
S2 paperId e507f71814c77df9ed60420e2e6c889a9a3dd3eb, DOI 10.4064/AA-34-1-81-90.
2020–2026 citers (none overlap our lemmas; per-paper notes below):

| year | paper | arXiv | overlap |
|---|---|---|---|
| 2026 | Gaiser–Horn, Subsequence sums in permutations | 2605.29011 | none (ℓ-additive subsequences, finite [n]) |
| 2026 | Geneson, Density bounds for permutations avoiding monotone APs | 2608.12604 | NEAR-MISS: Lemma 3.1/3.3 α≥2/3 witness = ratio-4 doubling blocks [L·4^j+M, 2L·4^j] (S_A-like octaves, bottom slivers removed, per-stage truncation). Positive-side counterpart of our attack calculus. Must be discussed in paper, not just cited for the density disproof. |
| 2026 | Ho, 3AP-free permutations have no exponential growth rate | 2602.13617 | none (enumeration θ(n)) |
| 2024 | Hirose–Saito, Characterization of order structures avoiding 3-APs | 2404.13510 | adjacent: chaotic order types on ALL of N/Z/Q, no subsets; their Lemma 2.5 = zigzag transfer identity (attribute in our Lemma Z) |
| 2023 | Adenwalla, Generalisation ... 4-APs with 2^k-free differences | 2302.09662 | none |
| 2022 | Adenwalla, Avoiding monotone APs in permutations of integers (DM 347 (2024) 114183) | 2211.04451 | Question 6 = #197; only published strategy is the LV density route (α+β<1 ⇒ NO). No partition-specific analysis. |
| 2022 | Sim–Wong, Minimum number of colours ... | — | none (colorings) |
| 2021 | Kumor, Uwagi do zadania 786 (Polish) | — | problem-column note; no evidence of overlap |
| 2021 | Sim–Wong, Magic square arrangement ... | — | none |
| 2020 | Goh–Zhao, Arithmetic subsequences in a random ordering | 2012.12339 | none |

Pre-2020 citers reviewed for the rigidity/ladder angle: Folkman's relation (4)
inside DEGS77 itself is the classical zigzag alternation (also Gen26 Lemma 2.1);
Nathanson (JCTA 1977) mod-2^r phenomenon; Ardal–Brown–Jungić 2011 chaotic
orders on Q/Z (origin of the order-type escape); Károlyi–Komjáth (uncountable
well-orders); Hegarty–Martinsson 2015 (finite cyclic); LeSaulnier–Vijay
1004.1740 / DM 311 (2011) 205–207 (α≥1/2, β≥1/4, conjecture; sole prior #197
strategy); Correll–Ho 2017, Sharma 2009 (counting).

Second-order sweeps: citers of Geneson 1803.06334 ⊂ citers of DEGS (nothing
new); citers of Hirose–Saito 2404.13510 = {Geneson 2608.12604} only.

## #197-specific checks (all negative for prior/parallel work)

- erdosproblems.com/197 (via r.jina.ai proxy, 2026-08-25): OPEN; remark "cannot
  be resolved with a finite computation"; no partial results, no forum posts.
- erdosproblems.com forum: no thread for 197; "AI Contributions" 1+2 threads:
  no mention of 197 or AP-permutation problems.
- teorth/erdosproblems wiki "AI contributions" ledger: ~470 problems listed,
  197 ABSENT.
- Gemini case study arXiv:2601.22401: 13 problems addressed, 197 not among.
- erdosproblemaday.com: 595 attempted problems, no 197 entry (nearby #196
  finite-counting entry 2026-08-11 only, self-labeled PARTIAL).
- Web searches for dyadic/two-set/blocks candidates for #197 (MO, Reddit,
  blogs): zero public informal discussion of the dyadic candidate found.
- arXiv keyword sweeps (monotone AP + permutation, 2024–2026): only the
  papers already in the table.

## Consequences for the paper (filed as A5 findings)

1. Add a remark engaging Gen26 Lemma 3.1 (sliver-shaved octaves are 3-permutable
   vs exact S_A is not; his upper density 2/3 = S_A's upper density).
2. Attribute zigzag alternation: DEGS77 (Folkman relation (4)), HS24 Lemma 2.5,
   Gen26 Lemmas 2.1–2.2.
3. Fix LV11 prose (intro states a universal density lower bound; LV proved the
   sup statement α_N(3) ≥ 1/2 — current wording is false as written).
4. Soften/source "adopted as the default attack in all informal discussion"
   (no public informal discussion exists to point to).
5. Consider adding cites: Ardal–Brown–Jungić 2011; Nathanson JCTA 1977.

Verdict: main theorem (S_A not 3-permutable) and the impossibility-side
machinery (chunk reduction, OG guard/attack calculus, C3 flood/mod-8 rigidity)
have no precedent found anywhere as of 2026-08-25.
