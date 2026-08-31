# 93 — Adversary C: final pre-publication triage + remediation

Role: consolidate adversaries A (notes/91) and B (notes/92), triage every
finding, apply BLOCKER + cheap SHOULD-FIX edits to `paper/main.tex`, recompile,
rebuild the arXiv bundle, render GO/NO-GO.

## Independent machine re-verification (fresh encoder, `experiments/e195_zone_bases.py`)

Written from the paper's definitions only; eager transitivity, Cadical195.

| check | result |
|---|---|
| `Z(M)` (lem:bases) | UNSAT for every 16 ≤ M ≤ 31; **SAT** for 12 ≤ M ≤ 15 → range is tight |
| AP ∧ C3 (thm:c3core) | UNSAT **exactly** at M ≡ 0 mod 8, all 16 ≤ M ≤ 72 |
| full `OG(M)` (prop:ogmachine) | UNSAT for every 16 ≤ M ≤ 60 |
| **L1 statement** (AP ∧ A2 ∧ A3 ∧ b3≺b5) | UNSAT at **every** M ≡ 0 mod 4, 12 ≤ M ≤ 72 — including M ≡ 4 mod 8 |
| **FLIP statement** (AP ∧ A2 ∧ A3 ∧ b5≺b3 ∧ A1) | UNSAT at M ≡ 0 mod 8; **SAT** at M ≡ 4 mod 8 (20,28,…,68) |
| densities | d̄(S_A) = 2/3, d(S_A) = 1/3; \|S_A∩[1,16]\| = 10, \|S_A∩[1,64]\| = 42 → 111/128 = 87 % ✓ |

The L1/FLIP rows independently confirm A2: the old sentence "at M ≡ 4 (mod 8)
… the proofs below evaporate" was **false for L1** and true only for FLIP.
Nothing found invalidates thm:ogred → thm:c3core → thm:main.

## Triage

**BLOCKER (false or misleading as printed) — all fixed**

| id | issue | fix |
|---|---|---|
| A2 | "at M ≡ 4 mod 8 … the proofs below evaporate" contradicts thm:l1, which is proved for all M ≡ 0 mod 4 | rewritten: centres survive with class roles *swapped*; L1 survives, only FLIP fails; mod-8 enters only via FLIP |
| A3 | "window-2 infeasible at N=1024 — hence dead at EVERY horizon; window-2 at N=256 IS FEASIBLE" (self-contradiction in one sentence) | "infeasible at every horizon ≥ 1024, so no infinite window-2 solution"; N=256 clause moved into a parenthesis |
| A8 | `L(4) = 2` asserted, only the lower bound exists in the repo (notes/27 records "L(4) ≥ 2") | now `L(4) ≥ 2`, with `L(4) ≤ 3` noted from monotonicity |
| A5 | range of k in S_A unspecified; k ≥ 0 makes "ten displacements" and "87 %" both wrong | S_A/S_B written explicitly with k ≥ 2; `L(m)` and thm:divergence now say `v ∈ S_A, v ≤ 16` |
| A4 | "3-permutable" used in the **Main Theorem** and never defined | defined in §2 |
| A1 | thm:vdc is Geneson [Gen26, Lem. 2.1] eq. (2.2) verbatim under c ↦ (c−1)/2, uncited, advertised in the abstract as a contribution | demoted to a lemma, cited to [Gen26] + [DEGS77]/[ABJ11], proof kept "for completeness", abstract softened |
| B1 | "every negative claim cross-validated by independent encodings and solvers" — false (three of ~186 OG scales; F_6 one solver; L(5) one CDCL run) | "the load-bearing negative claims …; the auxiliary sweeps were not, and are flagged where they occur" |
| B2 | "each of their **finitely many** schema instances has been machine-audited" — the schemas are ∀M, infinitely many instances | "They are ∀M schemas, with infinitely many instances; a finite but large range … an audit of the writing, not a substitute for the proofs" |
| B3 | Data availability over-promises: only 2 DRAT files, both for the *non*-dependency C3; reproduce.sh ≠ "complete verification stack"; lem:bases (a dependency of thm:contig) uncertified and unnamed | rewritten: names the two certificates, lists what reproduce.sh actually runs, explicitly says the other verdicts (lem:bases, OG sweep, cores, atlas, rungs) carry no certificates; lem:bases now names a script and states thm:contig is not used for thm:main |
| B4 | no Acknowledgements; Geneson credited only in two narrow footnotes | scoped **Acknowledgements** added: what he corrected, that his comments did **not** extend to verifying thm:main, sole responsibility disclaimed |
| B5 | author footnote "All proofs have been verified by hand unless explicitly marked as machine-checked" — the single most attackable sentence | replaced with a factual division of labour (solvers for discovery, Claude for drafting/strategy, author checked §10/13/14 line by line, solver output relied on only where marked) |

**SHOULD-FIX (cheap) — all applied**

A6 (spurious `O(1)` in lem:balance + cor:records — the proof is exact; deleting
strengthens both), A7 (thm:blockgranular's unargued "fiber boundary above block
4" — now a two-line argument via the non-increasing-stage contradiction, and
correctly stated as an *ascending* boundary), A9 ("doom-free", unbound m(M) and
k, "(A)-clean", implicit x ≤ 2^{k−2}), A10/B11 (abstract: "increasing" orbit,
"100 resp. 51 scales", "of order type ω" restored to the bold conclusion;
thm:chunk restated for arbitrary S so thm:degs's use on Z^+ is legitimate),
A11 (thm:degs / thm:blockgranular / thm:divergence proofs moved out of the
theorem bodies; unused `question`/`conjecture` environments deleted),
B6 (density paragraph added: d̄(S_A)=2/3 = Geneson's record, d̄(A)+d(B)=1 and
LV11's α+β ≥ 1, verified against notes/lesaulnier-vijay-2010.txt p.207),
B7 (g_X "expected to stabilize" rewritten with the explicit no-conflict remark;
negative-atlas progress-report prose rescoped; the unparseable "Historical note:
suffix-stacked deferral" section **deleted**), B8 (radius-1 universal, "any
single residue class", "hold verbatim for S_B", "apply to any two-set
partition", "what is new here" → all hedged; prop:cores now says "at every swept
scale … we make no claim outside the swept range" and separates the proved half
from the observed half), B11 (Geneson paragraph de-duplicated, his `m = M_{k−1}`
re-casing disclosed, "four-line proof" → "short proof"), Ho 2026
(arXiv:2602.13617, verified from `papers/3apfree-growth-2026.pdf`) cited.

**NOISE (no action)**: rem:c3machine's "35 scales" without a range; ten
label-defined-never-referenced warnings (LaTeX emits none); overfull hboxes
< 5 pt.

**CANNOT FIX FROM HERE (author action)**: B10 — the erdosproblems.com/197
comment of 26 Aug still carries the retracted unrestricted sharpness claim and
the "finitely many schema instances" wording. Post a correcting reply when the
arXiv ID is live.

## Build state

`tectonic` clean: no errors, **zero** undefined references, 20 pages.
`publish/arxiv-bundle.tar.gz` rebuilt from the edited `paper/main.tex`
(sha256-identical). Repo pushed.

## Verdict

**GO.** No blocker survives; the main chain was re-derived and re-verified
independently and is sound.

### Addendum (post-commit)

Also corrected: three places still promising "certificates in the repository"
for negative machine verdicts (deferral facts, machine atlas, the self-similar
4096 infeasibility) -- now "solver logs and witnesses ... but no proof
certificates for the negative verdicts", consistent with the rewritten Data
availability section. All dashes ASCII-ized (0 non-ASCII bytes) so the bundle
is pdflatex-safe regardless of arXiv toolchain. Tagged v1.1 at the posted
state; origin/main == local HEAD.
